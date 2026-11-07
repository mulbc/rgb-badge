<!-- SPDX-License-Identifier: Apache-2.0 -->

# Host playback controller

[ADR 0037](../docs/decisions/0037-host-playback-deadlines.md) defines the C++17 [AssetPlayback](core/include/rgb_badge/asset_playback.h) contract. This is one-shot software playback over either RGBB version. It has no clock service, thread, sleep, filesystem, GPIO, BLE, brightness or hardware-arm interface. The caller opens an `AssetReader`, constructs a controller and supplies monotonic unsigned 64-bit microsecond timestamps.

## States and timing

| Call/state | Result | Software pixels |
|---|---|---|
| Construct or `stop()` | Idle | Black |
| `start(now)` | Frame zero, or Error | Validated frame, or black |
| `poll(now)` before scheduled end | Waiting; no decode | Current validated frame |
| Poll at scheduled end | Exactly one next Frame | Next validated frame |
| Final scheduled end | End | Black |
| Backward clock, missed budget, expired next interval, overflow or decode failure | Latched Error | Black |
| Poll in Idle/End/Error | Same terminal result | Unchanged |

`start()` explicitly rewinds the reader, discards old delta references and begins a new timeline. It is permitted from any state and may use a new clock origin. `stop()` discards playback state and clears output. Poll never starts, loops or restarts implicitly. Timestamps must be nondecreasing while playing, including polls that return Waiting. Equal timestamps are permitted.

For Frame/Waiting results, `frame_index` is zero-based, `duration_us` is the original source duration and the intended display interval is `[scheduled_start_us, scheduled_end_us)`. End retains the final frame's metadata. Error latches `error` and, for decoder failures, `asset_error`; frame/timing metadata on Error is diagnostic only and must not be used to display pixels. Every terminal state has black software pixels.

Deadlines accumulate from the start origin, never from late polls. The repeating integer durations 16667, 16667, 16666 µs therefore cover exactly 50,000 µs per three frames and 300,000,000 µs per 18,000 frames. The complete timeline is checked against 64-bit overflow at start, before decoding. This is integer scheduling simulation, not a wall-clock performance measurement.

## Explicit lateness

The constructor's `max_lateness_us` is an explicit caller policy, defaulting to zero. The inclusive budget applies to frame transitions and completion. No target value has been qualified. If a transition is admitted late, `lateness_us` reports the delay from its scheduled start; Waiting preserves that admission value. The original scheduled end is retained, so actual visibility can be shorter by the reported lateness. No compensation by dimming, frame dropping, timeline rebasing or catch-up bursts occurs.

For example, durations 10/20/30 µs started at 100 give intervals `[100,110)`, `[110,130)`, `[130,160)`. With a 5 µs budget, a poll at 115 admits frame one, reports 5 µs late and still ends it at 130. A poll at 116 exceeds the budget. Even a 1000 µs budget cannot admit frame one at 130: that frame's entire interval has expired, so the controller faults instead of skipping it. A missed final completion boundary also faults if outside the budget.

The caller must consume Error and perform reviewed physical blanking. Clearing this object's RGB array cannot blank a latched display or replace the independent hardware interlock. Target integration must account for decode/colour-conversion/latch latency, predecode or buffering needs and actual timer precision before adopting a lateness budget. This controller does not implement the separate matrix scan engine or its ≥1 kHz visual-refresh requirement.

## Ownership and validation

The controller copies the reader, owns its 768-pixel output array and exposes a const pixel view. The original reader's cursor is independent. Borrowed encoded bytes must stay alive and immutable for the controller's lifetime. The view remains valid until mutation/destruction; copy pixels if they must outlive a transition. Only the first `pixel_count()` pixels belong to the selected dimensions. A failed decoder cannot expose partial or stale output: the complete array is cleared on all controller errors, stop and end.

No heap allocation occurs in the core. The controller occupies **4,736 bytes** on the tested Apple arm64 host, including the reader/reference and output arrays. Host test fixtures/trace adapters do allocate. Target object placement, stack/copy costs and timing remain unqualified; this is not an ESP-IDF application.

Run `./tools/check-playback.sh`. The runner uses strict warnings and fail-fast AddressSanitizer/UndefinedBehaviorSanitizer. Native checks exercise boundaries, a 1,625-case arrival/budget matrix, a five-minute 48 × 16 timeline against an independent integer-rational oracle, long durations, overflow, clock reversal, stop/restart, delta reference rebuild and decoded corruption. Python tests compile actual v1/v2 assets and compare all pixels and original durations through the native controller, including both dimensions, 60-frame key boundaries, waiting output, lateness and latched faults. The workflow runs this alongside the unchanged colour/asset suites and both capacity-report reproductions. [Host evidence](review/asset-playback-host-check-2026-10-21.json) records exact source hashes, setup, logs and limitations.
