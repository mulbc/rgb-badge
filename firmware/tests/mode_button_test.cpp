// SPDX-License-Identifier: Apache-2.0
#include "rgb_badge/mode_button.h"

#include <array>
#include <cstdlib>
#include <iostream>
#include <limits>

using namespace rgb_badge;
namespace {
unsigned checks=0;
void expect(bool condition, const char* message) {
    ++checks;
    if (!condition) { std::cerr << "FAIL: " << message << '\n'; std::exit(EXIT_FAILURE); }
}
void check_requests(const ModeResult& r) {
    expect(r.ble_requested==(r.state==ModeState::Programming), "BLE requested exclusively in programming");
    expect(r.state==ModeState::Playback || r.display_inhibit, "every other state inhibits display");
}
ModeButton make(ModeButtonConfig config={}) {
    auto button=ModeButton::create(config);
    expect(button.has_value(), "valid configuration accepted");
    return *button;
}
} // namespace

int main() {
    expect(!ModeButton::create({0,3000000}), "zero debounce rejected");
    expect(!ModeButton::create({1,0}), "zero hold rejected");
    expect(!ModeButton::create({31,30}), "hold below debounce rejected");
    expect(ModeButton::create({1,1}).has_value(), "minimum equal positive durations accepted");
    auto button=make();
    auto r=button.update(0,false);
    expect(r.state==ModeState::AwaitRelease && r.event==ModeEvent::None && r.display_inhibit && !r.ble_requested,
           "initial release must qualify before playback eligibility");
    expect(button.update(29999,false).state==ModeState::AwaitRelease, "release boundary minus one waits");
    r=button.update(30000,false);
    expect(r.state==ModeState::Playback && r.event==ModeEvent::PlaybackReady && !r.display_inhibit && !r.ble_requested,
           "initial release qualifies exactly at debounce boundary");
    expect(button.update(30000,false).event==ModeEvent::None, "ready event emitted once");
    r=button.update(40000,true);
    expect(r.state==ModeState::Playback && r.display_inhibit && !r.ble_requested,
           "raw press immediately inhibits without waiting for debounce or hold");
    button.update(69999,true); button.update(70000,true);
    r=button.update(3069999,true);
    expect(r.state==ModeState::Playback && !r.ble_requested, "hold boundary minus one cannot enter");
    r=button.update(3070000,true);
    expect(r.state==ModeState::Programming && r.event==ModeEvent::EnterProgramming && r.ble_requested && r.display_inhibit,
           "three seconds after qualified press requests programming exactly once");
    expect(button.update(3070000,true).event==ModeEvent::None, "programming event cannot repeat at same timestamp");
    r=button.update(3100000,false);
    expect(r.state==ModeState::Programming && r.ble_requested && r.display_inhibit, "release cannot implicitly exit programming");
    r=button.update(10000000,true); check_requests(r);
    expect(r.event==ModeEvent::None && r.state==ModeState::Programming, "another hold does not toggle mode");
    r=button.update(9999999,true);
    expect(r.state==ModeState::Fault && r.event==ModeEvent::ClockFault && r.error==ModeError::ClockReversed &&
           !r.ble_requested && r.display_inhibit, "backward clock revokes programming request");
    r=button.update(11000000,false);
    expect(r.state==ModeState::Fault && r.event==ModeEvent::None && r.error==ModeError::ClockReversed,
           "clock fault latches while its edge event does not repeat"); check_requests(r);
    button.reset(); r=button.update(0,true);
    expect(r.state==ModeState::AwaitRelease && r.error==ModeError::None && !r.ble_requested && r.display_inhibit,
           "reset clears fault and permits a new clock origin but requires release");
    r=button.update(1000000000,true);
    expect(r.state==ModeState::AwaitRelease && !r.ble_requested, "stuck boot button cannot enter programming");
    button.update(1000000001,false);
    expect(button.update(1000030000,false).state==ModeState::AwaitRelease, "held-start release must fully debounce");
    expect(button.update(1000030001,false).event==ModeEvent::PlaybackReady, "held-start release eventually readies playback");

    // A released sample at the hold deadline suppresses entry immediately;
    // qualified release cancels the hold rather than accumulating short presses.
    auto short_press=make({10,30});
    short_press.update(0,false); short_press.update(10,false);
    short_press.update(20,true); short_press.update(30,true);
    r=short_press.update(60,false);
    expect(r.state==ModeState::Playback && r.display_inhibit && !r.ble_requested, "pending release suppresses threshold entry");
    r=short_press.update(70,false);
    expect(!r.display_inhibit && !r.ble_requested, "qualified release cancels press");
    short_press.update(80,true); short_press.update(90,true);
    expect(!short_press.update(119,true).ble_requested, "second short press cannot accumulate previous hold");
    expect(short_press.update(120,true).event==ModeEvent::EnterProgramming, "second full hold enters at its own deadline");
    short_press.reset(); short_press.update(0,false); short_press.update(10,false);
    short_press.update(20,true); short_press.update(29,false); short_press.update(35,true);
    short_press.update(44,true); short_press.update(45,true);
    expect(!short_press.update(74,true).ble_requested, "press bounce restarts qualification before hold begins");
    expect(short_press.update(75,true).ble_requested, "bounced press gets full qualified hold");

    // Release bounce shorter than debounce is ignored; pending raw release
    // still inhibits and suppresses entry until pressed samples requalify.
    auto bounce=make({10,30}); bounce.update(0,false); bounce.update(10,false);
    bounce.update(20,true); bounce.update(30,true); bounce.update(55,false);
    expect(!bounce.update(60,false).ble_requested, "release bounce at deadline suppresses entry");
    bounce.update(61,true);
    expect(!bounce.update(70,true).ble_requested, "bounced-back raw press must requalify");
    expect(bounce.update(71,true).ble_requested, "unqualified release does not cancel an already qualified hold");
    auto release_bounce=make({10,30}); release_bounce.update(0,false); release_bounce.update(9,true);
    release_bounce.update(18,false);
    expect(release_bounce.update(27,false).state==ModeState::AwaitRelease, "boot release bounce restarts qualification");
    expect(release_bounce.update(28,false).event==ModeEvent::PlaybackReady, "stable startup release accepted after bounce");

    auto pulse=make({10,30}); pulse.update(0,false); pulse.update(10,false);
    pulse.update(20,true);
    expect(pulse.update(21,false).display_inhibit, "sub-debounce press latches inhibit through raw release");
    expect(pulse.update(30,false).display_inhibit, "short-pulse release boundary minus one remains inhibited");
    expect(!pulse.update(31,false).display_inhibit, "short-pulse inhibit clears only after qualified release");

    constexpr auto maximum=std::numeric_limits<std::uint64_t>::max();
    auto upper=make({10,30}); upper.update(maximum-100,false); upper.update(maximum-90,false);
    upper.update(maximum-80,true); upper.update(maximum-70,true);
    expect(!upper.update(maximum-41,true).ble_requested, "high-origin boundary minus one");
    expect(upper.update(maximum-40,true).ble_requested, "high-origin hold uses elapsed arithmetic without wrapping");
    expect(upper.update(maximum,true).state==ModeState::Programming, "maximum clock remains representable");
    expect(upper.update(0,false).error==ModeError::ClockReversed, "timestamp wrap is an explicit fault");
    const auto maximum32=std::numeric_limits<std::uint32_t>::max();
    auto wide=make({maximum32,maximum32});
    wide.update(0,false); wide.update(maximum32,false); wide.update(std::uint64_t{maximum32}+1,true);
    const auto qualified=std::uint64_t{maximum32}*2+1;
    wide.update(qualified,true);
    expect(!wide.update(qualified+maximum32-1,true).ble_requested, "maximum config duration does not truncate to 32 bits");
    expect(wide.update(qualified+maximum32,true).ble_requested, "maximum configuration hold qualifies without addition overflow");
    for (bool pressed : {false,true}) {
        auto reversed=make(); reversed.update(100,pressed);
        expect(reversed.update(99,pressed).state==ModeState::Fault, "backward clock also faults before initial release");
        check_requests(reversed.update(101,!pressed));
    }

    // Exhaust every 12-sample binary waveform. Independent oracle uses a
    // three-sample window rather than the core's candidate timestamps.
    constexpr unsigned samples=12;
    for (unsigned waveform=0; waveform<(1U<<samples); ++waveform) {
        auto tested=make({2,4});
        std::array<bool,samples> raw{};
        ModeState state=ModeState::AwaitRelease;
        bool stable=true;
        unsigned pressed_at=0;
        unsigned consecutive_released=0;
        for (unsigned t=0; t<samples; ++t) {
            raw[t]=(waveform&(1U<<t))!=0;
            consecutive_released=raw[t] ? 0 : consecutive_released+1;
            const bool qualified_window=t>=2 && raw[t]==raw[t-1] && raw[t]==raw[t-2];
            if (qualified_window && stable!=raw[t]) {
                stable=raw[t];
                if (stable) pressed_at=t;
            }
            auto event=ModeEvent::None;
            if (state==ModeState::AwaitRelease && qualified_window && !stable) {
                state=ModeState::Playback; event=ModeEvent::PlaybackReady;
            } else if (state==ModeState::Playback && qualified_window && stable && raw[t] && t-pressed_at>=4) {
                state=ModeState::Programming; event=ModeEvent::EnterProgramming;
            }
            const auto actual=tested.update(t,raw[t]);
            expect(actual.state==state && actual.event==event && actual.error==ModeError::None,
                   "exhaustive sampled-state/window oracle agrees");
            expect(actual.display_inhibit==(state!=ModeState::Playback || consecutive_released<3),
                   "every waveform inhibits immediately and through release qualification");
            check_requests(actual);
        }
    }
    std::cout << "Mode button: " << checks << " checks passed\n"
              << "ModeButton host object bytes: " << sizeof(ModeButton) << '\n';
}
