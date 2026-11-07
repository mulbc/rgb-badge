<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0037: Explicit host playback deadlines and failure state

- Date: 2026-10-21
- Status: Accepted for host software development; target scheduling remains unqualified
- Scope: DSP-003/004/006 software preparation; no hardware enable or current-limit change

## Decision

Build a platform-independent, one-shot C++17 playback controller over the validated RGBB v1/v2 reader. Accept caller-supplied unsigned 64-bit monotonic microseconds; use absolute frame boundaries anchored at explicit start time, adding each original duration without rounding or drift. Start emits frame zero immediately. Polling before the next boundary keeps the current frame. At the boundary emit exactly one next frame, or complete and clear the software output after the final duration. Restart explicitly rewinds, including delta reference state. Stop clears output and returns to idle.

Expose original frame duration, scheduled start/end and admission lateness. A caller supplies an explicit maximum lateness in microseconds (default zero); this is a development policy, not a qualified target tolerance. A late frame within that budget retains its original scheduled end, so its actual visible interval can be shorter by the reported lateness. Never silently drop source frames, rebase the clock or issue a catch-up burst. If the budget is exceeded, the next frame's entire interval has expired, time moves backward, decoding fails or the complete asset timeline would overflow, latch an error and clear software pixels. Only explicit start/stop leaves the fault state.

Keep one owned 768-pixel output buffer in addition to the reader's owned reference, without heap allocation. Borrowed asset bytes must remain alive and immutable. A const output view is valid until the controller is mutated/destroyed; software clearing is not an electrical display-blanking mechanism. There are no GPIO, radio, current-limit, brightness or hardware-arm interfaces.

Validate boundary timing, fractional 60 fps durations, variable durations, tolerated/missed deadlines, no frame skipping, end/stop/restart, backward clocks, overflow and corrupt decoded frames with host sanitizers and actual compiler-produced v1/v2 assets. Keep this separate from the matrix scan engine: DSP-004 still requires target timing traces and camera tests, including at least 1 kHz visual refresh. Target decode-before-latch integration, memory placement, fault propagation to reviewed hardware blanking and representative-content storage remain open.
