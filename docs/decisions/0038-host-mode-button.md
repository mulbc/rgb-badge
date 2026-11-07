<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0038: Host mode-button qualification before target radio integration

- Date: 2026-10-21
- Status: Accepted for host software development; target button/radio/interlock behavior unqualified
- Scope: RF-001/002, CTL-001 and DSP-006 software preparation

## Decision

Implement a no-heap C++17 sampled-button state machine, independent of GPIO, BLE and display drivers. Supply monotonic unsigned 64-bit microseconds and a logical `pressed` input; the target adapter must map physical polarity. Start/reset in AwaitRelease and require a debounced release before normal Playback eligibility. A button already held at startup cannot request BLE programming. This does not alter the controller's separate ROM-recovery strapping behavior.

Use explicit validated host configuration: positive debounce and hold durations, with hold at least debounce. Initial development defaults are 30,000 µs debounce and 3,000,000 µs hold after press qualification; these are software policy, not measured switch timing. Qualify a candidate after the debounce interval. A qualified release cancels a pending hold. Suppress entry while a raw release is pending; brief bounce does not create an additional press. Once a qualified press has been held for the hold interval, emit one EnterProgramming event and remain in Programming until explicit reset. No automatic radio timeout or exit gesture is selected here.

Expose requests only: BLE requested exclusively in Programming; display inhibit asserted in AwaitRelease/Programming/Fault and immediately on a raw press, persisting through release qualification. Withdrawing inhibit is never an arm command. Preserve ADR 0032's independent heartbeat/arm and hardware mode-button clear requirements. Target integration must stop playback, blank through reviewed hardware, and manage actual BLE resources explicitly; this core cannot prove either action occurred.

A backward clock latches Fault, withdraws the BLE request and asserts display inhibit. Reset discards debounce/hold history and allows a new clock origin. Use elapsed-time comparisons to avoid timestamp overflow. Poll events are edges, while state/requests/error persist. Sampled input cannot prove there was no unobserved bounce or release between samples; qualify target sampling cadence and real button behavior separately.

Host tests must cover startup held/released, press/release bounce, short/repeated holds, exact boundaries, programming persistence, raw-press inhibit, backward time, overflow and reset. Actual BLE-off current, three-second user behavior, display blanking/arming, ROM recovery and hardware interlock qualification remain acceptance work.
