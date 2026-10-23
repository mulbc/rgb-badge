// SPDX-License-Identifier: Apache-2.0
// Host-only composition trace adapter. Test button policy: 10 us / 30 us.
#include "rgb_badge/content_session.h"

#include <charconv>
#include <fstream>
#include <iostream>
#include <iterator>
#include <limits>
#include <string>
#include <vector>

namespace {
bool number(const std::string& text,std::uint64_t& value) {
    const auto parsed=std::from_chars(text.data(),text.data()+text.size(),value);
    return parsed.ec==std::errc{} && parsed.ptr==text.data()+text.size();
}
void emit(const rgb_badge::ContentSession& s,const rgb_badge::SessionResult& r) {
    std::cout << "{\"state\":" << static_cast<unsigned>(r.state)
              << ",\"fault\":" << static_cast<unsigned>(r.fault)
              << ",\"mode_event\":" << static_cast<unsigned>(r.mode_event)
              << ",\"command_accepted\":" << r.command_accepted << ",\"frame_ready\":" << r.frame_ready
              << ",\"ble_requested\":" << r.ble_requested << ",\"display_inhibit\":" << r.display_inhibit
              << ",\"brightness\":" << s.brightness()
              << ",\"playback_status\":" << static_cast<unsigned>(r.playback.status)
              << ",\"playback_error\":" << static_cast<unsigned>(r.playback.error)
              << ",\"asset_error\":" << static_cast<unsigned>(r.playback.asset_error)
              << ",\"frame_index\":" << r.playback.frame_index
              << ",\"duration_us\":" << r.playback.duration_us
              << ",\"scheduled_start_us\":" << r.playback.scheduled_start_us
              << ",\"scheduled_end_us\":" << r.playback.scheduled_end_us
              << ",\"lateness_us\":" << r.playback.lateness_us << ",\"rgb16\":[";
    for(std::size_t i=0;i<s.pixel_count();++i) {
        if(i) std::cout << ',';
        const auto c=s.pixels()[i];
        std::cout << '[' << c.red << ',' << c.green << ',' << c.blue << ']';
    }
    std::cout << "]}\n";
}
} // namespace
int main(int argc,char** argv) {
    std::uint64_t brightness=0,budget=0;
    if(argc!=4 || !number(argv[2],brightness) || brightness>65535 ||
       !number(argv[3],budget) || budget>std::numeric_limits<std::uint32_t>::max()) return 2;
    std::ifstream input(argv[1],std::ios::binary); if(!input) return 2;
    const std::vector<std::uint8_t> bytes((std::istreambuf_iterator<char>(input)),{});
    rgb_badge::AssetError error;
    const auto reader=rgb_badge::AssetReader::open(bytes.data(),bytes.size(),error);
    if(!reader) { std::cerr << "open error " << static_cast<unsigned>(error) << '\n'; return 1; }
    rgb_badge::GammaTable gamma{};
    for(std::uint64_t i=0;i<256;++i) gamma[i]=static_cast<std::uint16_t>((i*i*65535+32512)/65025);
    const auto transform=rgb_badge::ColorTransform::create(gamma,{65535,32768,16384},static_cast<std::uint16_t>(brightness));
    auto session=rgb_badge::ContentSession::create(*reader,*transform,{10,30},static_cast<std::uint32_t>(budget));
    std::string timestamp,pressed,command;
    while(std::cin>>timestamp>>pressed>>command) {
        std::uint64_t now=0;
        if(!number(timestamp,now) || (pressed!="0" && pressed!="1")) return 2;
        auto action=rgb_badge::SessionCommand::None;
        if(command=="start") action=rgb_badge::SessionCommand::Start;
        else if(command=="stop") action=rgb_badge::SessionCommand::Stop;
        else if(command=="reset") session->reset();
        else if(command!="none") return 2;
        emit(*session,session->step(now,pressed=="1",action));
    }
    return 0;
}
