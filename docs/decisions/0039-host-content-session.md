<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0039: Compose host playback, colour and mode control

- Date: 2026-10-21
- Status: Accepted for host software development; target integration unqualified
- Scope: DSP-003/004/005/006 and RF-001/002 software preparation

## Decision

Compose the validated asset reader/playback, immutable colour transform and mode-button model in a no-heap C++17 content session. Borrow immutable encoded bytes, own software RGB888/reference and normalized RGB16 buffers, and retain a fixed copied colour/brightness configuration. Do not expose GPIO, current-limit, driver encoding, radio resources or hardware-arm interfaces.

Start/reset in AwaitRelease with black output and BLE not requested. Process the button before playback on each timestamped step. Raw press immediately stops software playback and clears normalized output; release qualification returns to Ready without automatic playback. Only an explicit Start command in eligible Ready/Complete state begins frame zero. Start while already playing or inhibited is rejected. Stop in eligible playback mode clears output and returns Ready. Programming holds black output and requests BLE exclusively in that state; only explicit reset exits programming.

Admit frames according to ADR 0037 and convert every validated source pixel using the copied colour transform. Waiting preserves the converted output, source deadlines and fixed brightness. Completion clears output and waits for an explicit Start. Input inhibit or explicit Stop takes priority over polling the interrupted playback timeline. A backward mode clock or playback error latches a session Fault, clears both software outputs and withdraws BLE request. Ordinary commands cannot clear Fault; only full session reset does, requiring initial release again. Preserve underlying playback/asset errors as diagnostics.

`display_inhibit` is true unless the session is actively playing a validated frame in eligible mode. False is software eligibility only, never a hardware-arm command. The future target adapter must implement reviewed physical blanking, independent heartbeat/arm sequencing, actual radio lifecycle and timer/decode/latch scheduling. It must not infer hardware state from software requests. Keep all existing electrical defaults and fabrication gates.

Verify the composition with native sanitizers and compiler/native traces of both asset versions and dimensions, including gamma/white-balance/fixed-brightness output, button interruption, explicit resume, programming, deadline/decode/clock faults, fault reset and exact completion. Record the full combined object's host size; qualify target memory placement and timing separately. No representative storage or electrical acceptance follows from these host traces.

## Integration finding

The composition trace reproduced an ADR 0038 implementation gap: a raw press shorter than debounce returned its inhibit request low immediately on raw release because neither candidate nor stable input was pressed. Preserve the existing decision's release-qualification contract by latching inhibit on every raw press and clearing it only on a qualified release. Add a focused short-pulse regression and change the independent waveform oracle to require consecutive released samples, rather than inferring inhibit from the stable press state. No hold threshold, current limit or physical interlock changes.
