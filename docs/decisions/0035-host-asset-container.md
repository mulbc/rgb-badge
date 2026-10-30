<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0035: Versioned host asset pipeline

- Date: 2026-10-21
- Status: Accepted for host software development; production storage/transfer format remains provisional
- Scope: DSP-003 and STO-001 software preparation; no electrical or fabrication change

## Decision

Implement a deterministic, lossless RGB888 asset compiler and a bounded C++17 sequential decoder before target drivers. Version 1 supports 16 × 16 coupon and 48 × 16 final frames, explicit positive microsecond durations and independent raw, RGB-run or palette-run frames. Select the smallest exact encoding, breaking ties by codec number. Never quantize colours, resample frames or change durations to meet a size target.

Use explicit little-endian fields, strict reserved/version checks, an IEEE CRC-32 over the body and a separate CRC-32 over each decoded RGB frame. CRC detects accidental corruption; it does not authenticate uploads. Enforce a 16 MiB encoded-file limit and 16 million decoded pixels per asset to bound work/expansion. These parser limits do not allocate flash partitions or establish the five-minute storage requirement.

The decoder borrows immutable input, writes into a caller-owned frame buffer and allocates no heap memory. Validate frame structure, pixel/run bounds and duration totals before opening an asset; validate decoded CRC when producing a frame. On a decoded-CRC failure clear the frame buffer and return an error without advancing. This is a software error contract, not a hardware blanking mechanism.

The [format specification](../../firmware/asset-format.md) controls both implementations. Asset compilation/decoding must be compared across languages using exact bytes and durations, malformed inputs, truncation/mutation tests and host sanitizers. No GPIO or display-arm interface is added.

## Remaining evidence

Measure target decode throughput, integrate scheduling/driver encoding and flash/update recovery, choose optical calibration and test representative content alongside dual application slots. Version 1 does not implement deltas, procedural text or phone transfer. It must not be used as proof of STO-001, 60 Hz target playback, display electrical operation or Gate A acceptance.
