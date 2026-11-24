// SPDX-License-Identifier: Apache-2.0
#include "rgb_badge/content_session.h"

#include <cstdlib>
#include <iostream>
#include <limits>
#include <vector>

using namespace rgb_badge;
namespace {
unsigned checks=0;
using Bytes=std::vector<std::uint8_t>;
void expect(bool condition,const char* message) {
    ++checks;
    if (!condition) { std::cerr << "FAIL: " << message << '\n'; std::exit(EXIT_FAILURE); }
}
void put(Bytes& b,std::size_t at,std::uint64_t value,unsigned count) {
    for(unsigned i=0;i<count;++i) b[at+i]=static_cast<std::uint8_t>(value>>(8*i));
}
void seal(Bytes& b) { put(b,28,crc32_ieee(b.data()+32,b.size()-32),4); }
Bytes fixture(unsigned version=1,unsigned width=16,bool corrupt=false) {
    Bytes b(32,0); b[0]='R'; b[1]='G'; b[2]='B'; b[3]='B';
    put(b,4,version,2); put(b,6,32,2); put(b,8,width,2); put(b,10,16,2);
    put(b,12,3,4); put(b,16,60,8);
    const Rgb8 colours[]={{51,102,153},{204,255,0},{17,34,51}};
    Rgb8 previous{};
    for (unsigned i=0;i<3;++i) {
        const auto at=b.size(); b.resize(at+16,0);
        put(b,at,10*(i+1),4); b[at+4]=version==2 && i ? 3 : 1;
        put(b,at+8,width/16*4,4);
        const auto c=colours[i]; Bytes decoded;
        for (unsigned pixel=0;pixel<width*16;++pixel) decoded.insert(decoded.end(),{c.red,c.green,c.blue});
        put(b,at+12,crc32_ieee(decoded.data(),decoded.size()) ^ (corrupt && i==1 ? 1U : 0U),4);
        Rgb8 residual=c;
        if (version==2 && i) residual={static_cast<std::uint8_t>(c.red^previous.red),
            static_cast<std::uint8_t>(c.green^previous.green),static_cast<std::uint8_t>(c.blue^previous.blue)};
        for(unsigned run=0;run<width/16;++run) b.insert(b.end(),{255,residual.red,residual.green,residual.blue});
        previous=c;
    }
    put(b,24,b.size()-32,4); seal(b); return b;
}
ContentSession make(const Bytes& b,std::uint32_t budget=0) {
    AssetError error;
    const auto reader=AssetReader::open(b.data(),b.size(),error);
    const auto transform=ColorTransform::create(identity_gamma(),{65535,65535,65535},32768);
    expect(reader.has_value() && transform.has_value(),"fixture inputs valid");
    auto s=ContentSession::create(*reader,*transform,{10,30},budget);
    expect(s.has_value(),"session created"); return *s;
}
void black(const ContentSession& s) {
    bool all_black=true;
    for(std::size_t i=0;i<s.pixel_count();++i) {
        const auto c=s.pixels()[i]; all_black=all_black && c.red==0 && c.green==0 && c.blue==0;
    }
    expect(all_black,"every normalized software pixel is black");
}
void first_colour(const ContentSession& s) {
    bool matches=true;
    for(std::size_t i=0;i<s.pixel_count();++i) {
        const auto c=s.pixels()[i]; matches=matches && c.red==6554 && c.green==13107 && c.blue==19661;
    }
    expect(matches,"all first-frame channels use fixed half-brightness golden values");
}
void ready(ContentSession& s) {
    expect(s.step(0,false).state==SessionState::AwaitRelease,"boot awaits qualified release");
    expect(s.step(10,false).state==SessionState::Ready,"qualified release readies without automatic playback");
}
} // namespace

int main() {
    for(unsigned version : {1U,2U}) for(unsigned width : {16U,48U}) {
        const auto bytes=fixture(version,width); auto s=make(bytes);
        expect(s.info().version==version && s.pixel_count()==width*16,"reader metadata preserved"); black(s);
        auto r=s.step(0,false,SessionCommand::Start);
        expect(r.state==SessionState::AwaitRelease && !r.command_accepted && r.display_inhibit && !r.ble_requested,
               "boot start rejected"); black(s);
        r=s.step(10,false);
        expect(r.state==SessionState::Ready && r.mode_event==ModeEvent::PlaybackReady && !r.frame_ready && r.display_inhibit,
               "initial release is eligibility, not start"); black(s);
        r=s.step(100,false,SessionCommand::Start);
        expect(r.state==SessionState::Playing && r.command_accepted && r.frame_ready && !r.display_inhibit &&
               !r.ble_requested && r.playback.frame_index==0 && r.playback.scheduled_end_us==110,
               "explicit start decodes and converts first frame"); first_colour(s);
        r=s.step(109,false);
        expect(r.state==SessionState::Playing && !r.frame_ready && r.playback.status==PlaybackStatus::Waiting,
               "waiting does not duplicate frame event"); first_colour(s);
        r=s.step(110,false,SessionCommand::Start);
        expect(!r.command_accepted && r.frame_ready && r.playback.frame_index==1 && r.playback.scheduled_end_us==130,
               "start while playing rejected without rewinding or delaying next source frame");
        r=s.step(130,false); expect(r.playback.frame_index==2 && r.frame_ready,"third source frame admitted");
        r=s.step(160,false);
        expect(r.state==SessionState::Complete && r.display_inhibit && !r.frame_ready && !r.ble_requested &&
               r.playback.status==PlaybackStatus::End,"completion clears software output"); black(s);
        expect(s.step(1000,false).state==SessionState::Complete,"completion cannot implicitly loop");
        r=s.step(2000,false,SessionCommand::Start);
        expect(r.frame_ready && r.playback.frame_index==0,"explicit restart after completion rebuilds v2 reference"); first_colour(s);
        r=s.step(2001,false,SessionCommand::Stop);
        expect(r.state==SessionState::Ready && r.command_accepted && r.display_inhibit,"explicit stop clears and readies"); black(s);
        s.step(3000,false,SessionCommand::Start);
        r=s.step(3001,true,SessionCommand::Start);
        expect(r.state==SessionState::Inhibited && !r.command_accepted && !r.frame_ready && r.display_inhibit && !r.ble_requested,
               "raw press stops immediately before debounce/hold"); black(s);
        s.step(3002,false);
        r=s.step(3012,false);
        expect(r.state==SessionState::Ready && !r.frame_ready && r.display_inhibit,"release never automatically resumes"); black(s);
        r=s.step(4000,false,SessionCommand::Start); expect(r.frame_ready && r.playback.frame_index==0,"explicit resume restarts first frame");
        s.step(4001,true); s.step(4011,true);
        r=s.step(4041,true,SessionCommand::Start);
        expect(r.state==SessionState::Programming && r.mode_event==ModeEvent::EnterProgramming && r.ble_requested &&
               r.display_inhibit && !r.command_accepted,"qualified hold enters black programming state"); black(s);
        r=s.step(5000,false,SessionCommand::Stop);
        expect(r.state==SessionState::Programming && r.ble_requested && !r.command_accepted,
               "stop command cannot exit programming"); black(s);
        r=s.step(4999,false);
        expect(r.state==SessionState::Fault && r.fault==SessionFault::ModeClock && !r.ble_requested && r.display_inhibit,
               "clock fault withdraws programming request"); black(s);
        r=s.step(6000,false,SessionCommand::Start);
        expect(r.state==SessionState::Fault && !r.command_accepted && r.mode_event==ModeEvent::None,
               "fault ignores start and does not repeat edge event");
        s.reset(); ready(s); black(s);
        r=s.step(20,false,SessionCommand::Start); first_colour(s);
        r=s.step(31,false,SessionCommand::Start);
        expect(r.state==SessionState::Fault && r.fault==SessionFault::Playback &&
               r.playback.error==PlaybackError::DeadlineMiss && !r.ble_requested && r.display_inhibit,
               "repeated start cannot hide missed playback deadline"); black(s);
        expect(s.step(32,false,SessionCommand::Stop).state==SessionState::Fault,"stop cannot clear session fault");
        s.reset(); ready(s);
        s.step(20,false,SessionCommand::Start);
        r=s.step(100,true);
        expect(r.state==SessionState::Inhibited && r.fault==SessionFault::None,
               "intentional button interruption takes priority over polling old timeline"); black(s);
        s.reset(); ready(s); s.step(20,false,SessionCommand::Start);
        r=s.step(100,false,SessionCommand::Stop);
        expect(r.state==SessionState::Ready && r.fault==SessionFault::None,"explicit stop interrupts without catch-up"); black(s);
        expect(s.brightness()==32768,"fixed brightness survives all session states and resets");
    }
    const auto bytes=fixture();
    auto s=make(bytes,2); ready(s); s.step(20,false,SessionCommand::Start);
    auto r=s.step(32,false);
    expect(r.frame_ready && r.playback.lateness_us==2 && r.playback.scheduled_end_us==50,"explicit lateness policy is preserved");
    r=s.step(50,false); expect(r.playback.scheduled_end_us==80,"tolerated lateness never rebases deadlines");
    expect(s.step(82,false).state==SessionState::Complete,"completion retains inclusive lateness budget"); black(s);
    for(unsigned version : {1U,2U}) {
        const auto corrupt=fixture(version,48,true); auto c=make(corrupt); ready(c);
        c.step(20,false,SessionCommand::Start); r=c.step(30,false);
        expect(r.state==SessionState::Fault && r.fault==SessionFault::Playback &&
               r.playback.asset_error==AssetError::BadFrameChecksum,"decoded CRC failure retains underlying diagnosis"); black(c);
        expect(c.step(100,true).state==SessionState::Fault,"button cannot clear decode fault");
    }
    auto overflow=make(bytes); ready(overflow);
    r=overflow.step(std::numeric_limits<std::uint64_t>::max()-59,false,SessionCommand::Start);
    expect(r.state==SessionState::Fault && r.playback.error==PlaybackError::TimeOverflow,"whole session rejects timeline overflow"); black(overflow);

    AssetError error; const auto reader=AssetReader::open(bytes.data(),bytes.size(),error);
    auto gamma=identity_gamma(); auto transform=ColorTransform::create(gamma,{65535,65535,65535},32768);
    expect(!ContentSession::create(*reader,*transform,{0,30}),"invalid button configuration rejected by composition");
    auto immutable=ContentSession::create(*reader,*transform,{10,30});
    gamma[51]=0; transform=ColorTransform::create(identity_gamma(),{0,0,0},0);
    ready(*immutable); immutable->step(20,false,SessionCommand::Start);
    first_colour(*immutable); expect(immutable->brightness()==32768,"session owns copied immutable colour settings");

    // Seeded adversarial input/command/timestamp traces verify cross-module
    // invariants, including faults followed by arbitrary attempted commands.
    std::uint32_t random=0x391c0deU;
    auto next=[&]() { random^=random<<13; random^=random>>17; random^=random<<5; return random; };
    for(unsigned trial=0;trial<200;++trial) {
        auto tested=make(bytes,2); std::uint64_t now=0; bool faulted=false;
        for(unsigned sample=0;sample<100;++sample) {
            now+=next()%20;
            if ((next()%31)==0) { tested.reset(); now=0; faulted=false; }
            const bool pressed=next()%4==0;
            const auto command=static_cast<SessionCommand>(next()%3);
            const auto event=tested.step(now,pressed,command);
            expect(!event.ble_requested || event.state==SessionState::Programming,"trace BLE exclusive to programming");
            expect(event.state==SessionState::Playing || event.display_inhibit,"trace all nonplaying states inhibited");
            expect(!event.frame_ready || (event.state==SessionState::Playing && !event.display_inhibit),"trace frame events require playing eligibility");
            if(pressed) expect(event.display_inhibit && !event.frame_ready,"trace raw press blocks frame admission");
            if(faulted) expect(event.state==SessionState::Fault,"trace commands cannot leave latched fault");
            if(event.state==SessionState::Fault) faulted=true;
            if(event.state!=SessionState::Playing) black(tested);
            expect(tested.brightness()==32768,"trace no automatic brightness change");
        }
    }
    std::cout << "Content session: " << checks << " checks passed\n"
              << "ContentSession host object bytes: " << sizeof(ContentSession) << '\n';
}
