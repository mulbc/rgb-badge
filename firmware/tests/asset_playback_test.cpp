// SPDX-License-Identifier: Apache-2.0
#include "rgb_badge/asset_playback.h"

#include <cstdlib>
#include <iostream>
#include <limits>
#include <vector>

using namespace rgb_badge;
namespace {
unsigned checks = 0;
using Bytes = std::vector<std::uint8_t>;
void expect(bool value, const char* message) {
    ++checks;
    if (!value) { std::cerr << "FAIL: " << message << '\n'; std::exit(EXIT_FAILURE); }
}
void put(Bytes& b, std::size_t at, std::uint64_t value, unsigned count) {
    for (unsigned i = 0; i < count; ++i) b[at+i] = static_cast<std::uint8_t>(value >> (8*i));
}
void seal(Bytes& b) { put(b, 28, crc32_ieee(b.data()+32, b.size()-32), 4); }
Bytes fixture(const std::vector<std::uint32_t>& durations, unsigned width = 16) {
    Bytes b(32, 0);
    b[0]='R'; b[1]='G'; b[2]='B'; b[3]='B';
    put(b, 4, 1, 2); put(b, 6, 32, 2); put(b, 8, width, 2); put(b, 10, 16, 2);
    put(b, 12, durations.size(), 4);
    std::uint64_t total = 0;
    for (std::size_t index = 0; index < durations.size(); ++index) {
        total += durations[index];
        const auto colour = static_cast<std::uint8_t>(index%255+1);
        Bytes pixels(width*16*3, colour);
        const auto at = b.size(); b.resize(at+16, 0);
        put(b, at, durations[index], 4); b[at+4] = 1;
        put(b, at+8, width/16*4, 4);
        put(b, at+12, crc32_ieee(pixels.data(), pixels.size()), 4);
        for (unsigned run = 0; run < width/16; ++run) b.insert(b.end(), {255,colour,colour,colour});
    }
    put(b, 16, total, 8); put(b, 24, b.size()-32, 4); seal(b);
    return b;
}
AssetPlayback player(const Bytes& bytes, std::uint32_t budget = 0) {
    AssetError error;
    auto reader = AssetReader::open(bytes.data(), bytes.size(), error);
    expect(reader.has_value() && error == AssetError::None, "valid fixture opened");
    return AssetPlayback(*reader, budget);
}
void black(const AssetPlayback& p) {
    for (std::size_t i=0; i<p.pixel_count(); ++i) {
        const auto v = p.pixels()[i];
        expect(v.red==0 && v.green==0 && v.blue==0, "software output cleared");
    }
}
void colour(const AssetPlayback& p, std::uint8_t expected) {
    for (std::size_t i=0; i<p.pixel_count(); ++i) {
        const auto v = p.pixels()[i];
        expect(v.red==expected && v.green==expected && v.blue==expected, "all source pixels retained");
    }
}
} // namespace

int main() {
    const auto bytes = fixture({10,20,30});
    auto p = player(bytes);
    expect(p.poll(999).status==PlaybackStatus::Idle, "poll cannot implicitly start"); black(p);
    auto r=p.start(100);
    expect(r.status==PlaybackStatus::Frame && r.frame_index==0 && r.duration_us==10 &&
           r.scheduled_start_us==100 && r.scheduled_end_us==110 && r.lateness_us==0,
           "start emits first original interval"); colour(p,1);
    expect(p.poll(100).status==PlaybackStatus::Waiting, "same timestamp does not advance");
    expect(p.poll(109).status==PlaybackStatus::Waiting, "one microsecond before boundary waits"); colour(p,1);
    r=p.poll(110);
    expect(r.status==PlaybackStatus::Frame && r.frame_index==1 && r.duration_us==20 &&
           r.scheduled_start_us==110 && r.scheduled_end_us==130, "exact boundary advances once"); colour(p,2);
    expect(p.poll(110).status==PlaybackStatus::Waiting, "repeated boundary cannot duplicate a frame");
    r=p.poll(130); expect(r.frame_index==2 && r.scheduled_end_us==160, "variable durations accumulate"); colour(p,3);
    expect(p.poll(159).status==PlaybackStatus::Waiting, "final frame holds its entire interval");
    r=p.poll(160); expect(r.status==PlaybackStatus::End && r.error==PlaybackError::None, "end distinct from failure"); black(p);
    expect(p.poll(0).status==PlaybackStatus::End, "completion remains terminal until explicit restart");
    expect(p.start(0).frame_index==0, "explicit start rewinds after completion"); colour(p,1);
    p.stop(); expect(p.poll(0).status==PlaybackStatus::Idle, "stop returns idle"); black(p);
    expect(p.start(100).status==PlaybackStatus::Frame, "restart after stop");
    r=p.poll(111); expect(r.status==PlaybackStatus::Error && r.error==PlaybackError::DeadlineMiss && r.lateness_us==1,
                         "default zero budget exposes one-microsecond miss"); black(p);
    expect(p.poll(110).error==PlaybackError::DeadlineMiss, "miss remains latched with no automatic catch-up");
    expect(p.start(100).status==PlaybackStatus::Frame, "explicit restart clears fault");
    expect(p.poll(105).status==PlaybackStatus::Waiting, "clock advances while waiting");
    expect(p.poll(104).error==PlaybackError::ClockReversed, "backward time while waiting fails"); black(p);
    p.stop(); expect(p.poll(1000).status==PlaybackStatus::Idle, "stop clears fault");

    auto tolerant=player(bytes,5);
    tolerant.start(100); r=tolerant.poll(115);
    expect(r.status==PlaybackStatus::Frame && r.frame_index==1 && r.lateness_us==5 &&
           r.duration_us==20 && r.scheduled_start_us==110 && r.scheduled_end_us==130,
           "inclusive lateness budget preserves absolute boundaries and source duration");
    r=tolerant.poll(130); expect(r.frame_index==2 && r.lateness_us==0 && r.scheduled_end_us==160,
                               "admission delay does not accumulate drift");
    expect(tolerant.poll(165).status==PlaybackStatus::End, "completion accepts inclusive budget"); black(tolerant);
    tolerant.start(100); expect(tolerant.poll(116).error==PlaybackError::DeadlineMiss, "budget plus one fails");
    auto expired=player(bytes,1000); expired.start(100);
    r=expired.poll(130); expect(r.status==PlaybackStatus::Error && r.error==PlaybackError::DeadlineMiss &&
                              r.frame_index==1, "entirely expired next frame fails instead of skipping"); black(expired);
    expired.start(100); expect(expired.poll(1000000).error==PlaybackError::DeadlineMiss, "large jumps cannot catch up");
    auto completion=player(bytes); completion.start(0); completion.poll(10); completion.poll(30);
    expect(completion.poll(61).error==PlaybackError::DeadlineMiss, "missed completion deadline is explicit"); black(completion);

    constexpr auto maximum=std::numeric_limits<std::uint64_t>::max();
    r=p.start(maximum-59); expect(r.error==PlaybackError::TimeOverflow, "whole timeline overflow rejected before decoding"); black(p);
    r=p.start(maximum-60); expect(r.status==PlaybackStatus::Frame, "exactly representable timeline accepted");
    p.poll(maximum-50); p.poll(maximum-30);
    expect(p.poll(maximum).status==PlaybackStatus::End, "maximum timestamp completes without wrapping");
    const auto tiny=fixture({1,1,1}); auto q=player(tiny);
    q.start(0); expect(q.poll(1).frame_index==1 && q.poll(2).frame_index==2 && q.poll(3).status==PlaybackStatus::End,
                       "minimum duration supported");
    const auto long_bytes=fixture({std::numeric_limits<std::uint32_t>::max(),1}); auto l=player(long_bytes);
    l.start(1); r=l.poll(std::uint64_t{1}<<32);
    expect(r.status==PlaybackStatus::Frame && r.scheduled_end_us==(std::uint64_t{1}<<32)+1,
           "maximum frame duration accumulates beyond 32-bit time");

    // Body CRC is valid but reconstructed CRC is wrong: opening succeeds,
    // decoding fails and no stale/partial pixels survive.
    auto corrupt=bytes; corrupt[44]^=1; seal(corrupt); auto c=player(corrupt);
    r=c.start(0); expect(r.error==PlaybackError::DecodeFailure && r.asset_error==AssetError::BadFrameChecksum,
                        "first decode failure retains underlying error"); black(c);
    corrupt=bytes; corrupt[64]^=1; seal(corrupt); auto d=player(corrupt);
    d.start(0); r=d.poll(10);
    expect(r.error==PlaybackError::DecodeFailure && r.asset_error==AssetError::BadFrameChecksum,
           "later decode failure clears prior output and latches"); black(d);
    expect(d.poll(10).error==PlaybackError::DecodeFailure, "decode failure is terminal");
    expect(d.start(500).status==PlaybackStatus::Frame, "restart replays from validated first frame");

    auto deltas=bytes; put(deltas,4,2,2);
    deltas[56]=3; deltas[69]=3; deltas[70]=3; deltas[71]=3; // 1 XOR 2
    deltas[76]=3; deltas[89]=1; deltas[90]=1; deltas[91]=1; // 2 XOR 3
    seal(deltas); auto delta=player(deltas);
    for (unsigned repeat=0; repeat<3; ++repeat) {
        const auto origin=std::uint64_t{repeat}*1000;
        expect(delta.start(origin).status==PlaybackStatus::Frame, "v2 restart rebuilds independent reference"); colour(delta,1);
        expect(delta.poll(origin+10).frame_index==1, "first delta admitted"); colour(delta,2);
        expect(delta.poll(origin+30).frame_index==2, "second delta admitted"); colour(delta,3);
        expect(delta.poll(origin+61).error==PlaybackError::DeadlineMiss, "v2 missed completion latches"); black(delta);
    }
    delta.stop(); black(delta);

    // Sweep lateness on either side of two unequal intervals, with a separate
    // expected state derived from source durations and configured budget.
    for (unsigned budget=0; budget<25; ++budget) {
        for (unsigned arrival=0; arrival<65; ++arrival) {
            auto sweep=player(bytes,budget); sweep.start(100);
            const auto event=sweep.poll(100+arrival);
            const auto expected=arrival<10 ? PlaybackStatus::Waiting :
                arrival-10<=budget && arrival<30 ? PlaybackStatus::Frame : PlaybackStatus::Error;
            expect(event.status==expected, "arrival/budget matrix matches interval oracle");
            if (expected==PlaybackStatus::Frame) {
                expect(event.frame_index==1 && event.scheduled_end_us==130 && event.lateness_us==arrival-10,
                       "matrix never skips a source frame or rebases deadline");
            } else if (expected==PlaybackStatus::Error) {
                expect(event.error==PlaybackError::DeadlineMiss, "matrix rejects expired intervals even within budget");
                expect(sweep.pixels()[0].red==0 && sweep.pixels()[255].blue==0, "matrix fault clears both output ends");
            }
        }
    }

    // Five minutes at exactly 60 frames/s, using the integer duration pattern.
    // Expected boundaries use a separate integer-rational oracle, not summation.
    std::vector<std::uint32_t> durations;
    for (unsigned i=0; i<18000; ++i) durations.push_back(i%3==2 ? 16666 : 16667);
    const auto five_minutes=fixture(durations,48); auto f=player(five_minutes);
    expect(f.info().duration_us==300000000 && f.pixel_count()==768, "five-minute final-size fixture metadata");
    constexpr std::uint64_t origin=1234567890123ULL;
    r=f.start(origin);
    for (unsigned i=0; i<18000; ++i) {
        const auto begin=origin+(std::uint64_t{i}*1000000+59)/60;
        const auto end=origin+(std::uint64_t{i+1}*1000000+59)/60;
        if (i) r=f.poll(begin);
        expect(r.status==PlaybackStatus::Frame && r.frame_index==i && r.scheduled_start_us==begin &&
               r.scheduled_end_us==end && r.duration_us==end-begin && r.lateness_us==0,
               "rational 60-fps oracle matches every frame without drift or skipping");
        const auto v=f.pixels()[767];
        expect(v.red==i%255+1 && v.green==v.red && v.blue==v.red, "final pixel follows every original frame");
        expect(f.poll(end-1).status==PlaybackStatus::Waiting, "every frame holds until final microsecond");
    }
    expect(f.poll(origin+300000000).status==PlaybackStatus::End, "five-minute exact completion"); black(f);
    std::cout << "Asset playback: " << checks << " checks passed\n"
              << "AssetPlayback host object bytes: " << sizeof(AssetPlayback) << '\n';
}
