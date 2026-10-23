<!-- SPDX-License-Identifier: Apache-2.0 -->

# Integrated host content session

[ADR 0039](../docs/decisions/0039-host-content-session.md) defines the no-heap C++17 [ContentSession](core/include/rgb_badge/content_session.h). It composes the existing RGBB reader/playback, copied colour transform and mode-button model. This lets host tests follow exact source art through timing, gamma, white balance and fixed brightness while interrupting playback with button/mode/fault events. It has no GPIO, BLE stack, driver encoding, current-limit or hardware-arm interface.

Create a session from an opened `AssetReader`, validated `ColorTransform`, button policy and explicit maximum playback lateness. Invalid button policy rejects creation. The session copies configuration/state but borrows encoded asset bytes, which must remain alive and immutable. The original reader cursor and caller's colour settings remain independent. Inputs and the const pixel view must be used from one execution context; no concurrency synchronization is provided.

Call `step(now_us, pressed, command)` with monotonic unsigned 64-bit microseconds, logical button state and one explicit None/Start/Stop command. `reset()` is a separate deliberate operation, clears all history/output and permits a new clock origin. Button timing defaults to ADR 0038; the lateness budget defaults to zero under ADR 0037. These are development policies, not qualified target settings.

## State and command contract

| State | Entry/behavior | Software output | BLE requested |
|---|---|---|---|
| AwaitRelease | Construction/reset; require debounced release | Black | False |
| Ready | Eligible mode, stopped; wait for explicit Start | Black | False |
| Playing | Start accepted; validated frames follow source deadlines | Converted normalized RGB16 | False |
| Inhibited | Raw press; release must qualify | Black | False |
| Complete | Final interval finishes; no implicit loop | Black | False |
| Programming | Qualified hold; persists until reset | Black | True |
| Fault | Mode clock or playback failure; persists until reset | Black | False |

An initial release only readies the session. Start is accepted in eligible Ready/Complete state, including the same step that qualifies release. It always begins at frame zero. Start while already Playing is rejected and the existing timeline is polled, so repeated commands cannot conceal a missed deadline or silently rewind. Stop in eligible playback mode is accepted, clears output and returns Ready. Start/Stop in AwaitRelease/Inhibited/Programming/Fault are rejected. Stop cannot clear a latched Fault or exit Programming. Explicit reset requires release again.

The button is processed first. Any raw press immediately stops playback and clears software output, even when the press never lasts long enough to qualify. Its inhibit remains until release qualifies. Release does not automatically restart interrupted content. A pending inhibit or an explicit Stop intentionally interrupts the old timeline before it is polled; this is a deliberate stop, not a frame-dropping catch-up path.

Each Frame result is decoded/CRC-validated, then converted exactly once with the copied gamma/white-balance/fixed-brightness settings. `frame_ready` is an edge for a newly converted frame, not every poll. Waiting retains pixels and source timing metadata. There is no automatic dimming or setting mutator. Stop/end/inhibit/reset/fault clear the complete normalized output and stop/clear the underlying RGB888 playback buffer. Only the first `pixel_count()` entries belong to the selected 16 × 16 or 48 × 16 dimensions. The const pixel view lasts until mutation/destruction; copy it if needed longer.

`SessionResult.playback` retains source deadlines/durations/lateness under the existing playback contract; completion retains the final interval. Inhibit/Stop/reset discard old playback metadata. Playback errors retain their underlying playback/asset diagnostics even though internal playback is stopped. A mode-clock error reports `SessionFault::ModeClock`; other mode events remain edges. Commands cannot clear a session fault: subsequent steps remain black and withdraw BLE request until full reset. `command_accepted` and `frame_ready` are false on fault.

`display_inhibit` is true except while actively Playing a validated frame. False is software eligibility, **never physical arm permission**. BLE requested is a software request, not a report that a radio is running. The future target adapter must manage actual BLE resources, physical blanking and deliberate independent heartbeat/arm sequencing, plus real timer/decode/colour/latch latency. Clearing software buffers cannot blank a display that already latched data. The captured hardware mode-button clear remains independent of debounce.

## Integration finding and validation

The first compiler/native interruption trace exposed a pre-existing ADR 0038 gap: a press shorter than debounce dropped its inhibit on raw release because stable press had never qualified. The button core now latches inhibit on every raw press and clears it only on qualified release. A focused regression covers a one-microsecond pulse; the independent 4,096-waveform oracle now counts consecutive released samples for inhibit instead of deriving it from stable press. Hold timing and the physical interlock are unchanged.

Run `./tools/check-content-session.sh`. It uses strict warnings and fail-fast AddressSanitizer/UndefinedBehaviorSanitizer. Native checks cover both asset versions/dimensions, copied settings, explicit commands, interruption, completion, programming, deadline/CRC/clock/overflow faults and 200 seeded 100-step adversarial traces. Seven Python integration tests compile real assets and compare every normalized channel to independent integer gamma/white-balance/brightness calculations, including zero/full brightness and 125 high-colour delta frames across key boundaries. They verify requests, waiting pixels, interruptions, explicit resume, corruption and fault/reset behavior. The workflow runs all constituent suites and both capacity reproductions too.

The combined object occupies **9,984 bytes** on the tested Apple arm64 host. It owns RGB reference/output and normalized output buffers plus copied configuration; no heap allocation occurs in the core. Host test fixtures/trace adapters do allocate. Target object placement, construction/copy stack cost and timing are unqualified. [Retained session evidence](review/content-session-host-check-2026-10-21.json) and [button regression evidence](review/mode-button-release-inhibit-host-check-2026-10-21.json) identify exact source hashes, setup and logs. No ESP-IDF application, physical BLE/blanking, representative-content acceptance or hardware qualification is established here.
