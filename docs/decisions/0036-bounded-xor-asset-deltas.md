<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0036: Bounded lossless XOR frame deltas

- Date: 2026-10-21
- Status: Accepted for host software development; target/storage qualification pending
- Scope: DSP-003 and STO-001 software preparation, extending ADR 0035

## Decision

Add opt-in RGBB version 2, preserving version 1 encoding/decoding. Keep the existing headers and full-frame codecs. Add XOR RGB-run and XOR palette-run codecs over the immediately preceding decoded RGB frame. The decoded CRC remains over final RGB bytes, never the residual. Choose a delta only when its payload is smaller than the best independent frame; ties prefer lower codec numbers/full frames. Raw fallback remains available without colour reduction.

Require an independent first frame and at most 59 consecutive delta frames. The compiler forces independent frames at indices divisible by 60. This bounds dependency length; it does not implement random seeking or automatic corruption recovery. A reader owns one 768-pixel reference buffer (2,304 RGB bytes), allocated inside its object with no heap allocation, so callers may reuse or modify output buffers. This additional object/stack footprint requires target integration review.

Only a successfully decoded and CRC-validated frame may become a reference. Structural/checksum failures invalidate the reference and do not advance the cursor. A checksum failure clears output pixels as before; subsequent deltas require rewind/replay or a new reader. Output-argument errors allow retry and retain the reference. Rewind discards reference validity.

Compare both versions on identical source frames/durations using native sanitizers, cross-language exact-byte tests, keyframe-boundary/corruption tests and reproducible capacity evidence. Keep version 1 as the default Python API mode; JSON/CLI select version explicitly. No source data, frame rate or brightness may be degraded to improve capacity.

## Remaining evidence

Synthetic gains do not establish representative five-minute content capacity. Target decode/stack/latency checks, scheduler and flash integration, actual application slots, real art, optical calibration and hardware validation remain open. No GPIO, current limit or fabrication gate changes here.
