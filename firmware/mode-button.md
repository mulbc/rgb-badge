<!-- SPDX-License-Identifier: Apache-2.0 -->

# Host mode-button state machine

[ADR 0038](../docs/decisions/0038-host-mode-button.md) controls the [ModeButton](core/include/rgb_badge/mode_button.h) C++17 core. It models RF-001/002, CTL-001 and the software inhibit boundary; it does not configure a GPIO, run a BLE stack or drive display hardware. Supply logical `pressed` and unsigned 64-bit monotonic microsecond timestamps to `update()`. Physical pin/polarity mapping remains a target adapter responsibility. The existing controller's ROM boot strapping is separate.

## States and requests

| State | Entry | BLE requested | Display inhibit |
|---|---|---|---|
| AwaitRelease | Construction/reset | False | True |
| Playback | Initial release qualifies | False | Until release qualifies after any raw press |
| Programming | Qualified hold completes | True | True |
| Fault | Clock moves backward | False | True |

Requests are software outputs, not observations of actual hardware/radio state. False `display_inhibit` is never an arm command. Target integration must preserve the independent interlock, stop/blank playback on inhibit, deliberately rearm only after reviewed conditions, and explicitly start/stop BLE resources. The captured ADR 0032 hardware mode-button clear must remain independent of software debounce. These modules have no display-arm or current-limit API.

`create()` validates positive debounce/hold intervals and hold at least debounce. Defaults are a **30,000 µs debounce** and **3,000,000 µs hold after press qualification**. They are explicit development policy, not measured switch timing. A continuously sampled default press therefore requests programming 3.03 seconds after its first pressed sample. Target cadence, bounce, perceived timing and GPIO polarity remain unqualified.

Every raw change restarts candidate qualification. A candidate becomes stable after its debounce duration. Startup requires a qualified release even if the button has been held for an arbitrarily long time; only a subsequent press can begin a hold. A qualified release cancels the hold, so short presses cannot accumulate. A raw press requests display inhibit immediately, and release must qualify before that request clears.

A pending raw release suppresses programming entry immediately. If it qualifies, the hold is canceled; if it bounces back before qualifying, the prior stable press is retained, but pressed input must qualify again before entry. This handles sampled bounce without counting a new hold for every short raw excursion. The hold origin is the first press candidate's qualification boundary, including when the caller observes that boundary later. Sparse observations cannot establish the physical input remained continuous between samples; this model is not a hardware debounce measurement.

`ModeEvent` is an edge: PlaybackReady, EnterProgramming or ClockFault is emitted once on transition. State, requests and `ModeError` persist. Programming remains active through release and later holds; explicit reset is the only exit in this host increment. No inactivity timeout or second gesture is silently selected. Reset clears timing history and permits a new clock origin but returns to AwaitRelease. Equal timestamps are permitted. Backward time, including unsigned clock wrap, latches Fault until reset, withdrawing BLE request and asserting inhibit. Elapsed comparisons avoid deadline addition overflow.

## Verification and integration limits

Run `./tools/check-mode-button.sh`. Native checks use strict C++17 warnings and fail-fast AddressSanitizer/UndefinedBehaviorSanitizer. They cover default timing boundaries, startup held/released, bounce, repeated short presses, pending release at threshold, event persistence, immediate inhibit, clock faults, reset and 32/64-bit arithmetic extremes. An independent sample-window oracle exhausts all **4,096 twelve-sample binary waveforms** with small test intervals, checking mode, events and both requests at every sample.

The object occupies **48 bytes** on the tested Apple arm64 host and allocates no heap memory. [Original evidence](review/mode-button-host-check-2026-10-21.json) records the initial source/result. The [session integration](content-session.md) found and fixed a short-pulse inhibit gap: any raw press now latches inhibit until a qualified release, even when the press itself never qualifies. The [current regression evidence](review/mode-button-release-inhibit-host-check-2026-10-21.json) records corrected source hashes, the focused pulse test and the updated independent consecutive-release oracle. Target builds, actual BLE-off current/resource release, three-metre range, hold timing, ROM recovery, and physical display clear/rearm remain open. The source board remains unbuilt and no hardware enable connection changes here.
