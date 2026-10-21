<!-- SPDX-License-Identifier: Apache-2.0 -->

# Synthetic asset-capacity screen, 2026-10-21

Status: actual host-encoded byte counts for generated patterns, not representative-content acceptance, a flash image or a target performance measurement.

Each case contains 24 distinct synthetic clips of 750 frames at 48 × 16 pixels. Durations repeat 16,667 / 16,667 / 16,666 microseconds, giving exactly 12.5 seconds per clip, 18,000 frames and 300 seconds per set. Frames are encoded independently by the real RGBB v1 compiler, without dropping, quantizing or resampling pixels. No target hardware is involved.

| Synthetic family | Encoded bytes, all 24 files | MiB | Within illustrative 8/10 MiB content budgets? |
|---|---:|---:|---|
| Changing solid-colour frames | 450,768 | 0.430 | Yes / yes |
| Moving two-colour six-pixel bar | 1,583,274 | 1.510 | Yes / yes |
| 768 unique colours with no repeated adjacent pixels | 41,760,768 | 39.826 | No / no |

The high-colour case is a structured gradient with changing blue, not random noise. It exercises the current encoder's exact raw fallback: 750 × (2,304 RGB bytes + 16 frame-header bytes) + 32 file-header bytes = 1,740,032 bytes per clip. All files stay within the per-file parser limit, but their combined size exceeds the project's approximate content-space plan. The table includes container headers, not filesystem/catalog overhead, application slots or calibration/settings storage. The 8/10 MiB comparisons are explicit planning assumptions, not allocated partitions.

The [machine-readable report](review/asset-capacity-synthetic-2026-10-21.json) records every clip's byte count, duration, frame count and encoded SHA-256, plus source hashes. Two complete screen runs produced byte-identical reports. Reproduce from the repository root:

```sh
python3 tools/screen-asset-capacity.py --report firmware/build/asset-capacity.json
```

The script retains only its JSON report; it does not write asset binaries. Its source defines the deterministic pattern families. GitHub CI reproduces and compares the complete report, including source hashes. This screen complements the sanitized decoder and Python/C++ exact-byte tests; it does not measure decode throughput.

STO-001 remains open. Next, obtain the intended representative art, evaluate delta/procedural or additional lossless compression against it, and link actual application slots/filesystem overhead before freezing partitions. Never silently lower colour depth, frame rate or brightness to make content fit. Synthetic low-colour success must not be reported as five-minute representative-content acceptance.
