<!-- SPDX-License-Identifier: Apache-2.0 -->

# Firmware

Production firmware will use ESP-IDF and native C/C++. Initial scope is hardware validation: deterministic matrix scan timing, safe rail defaults, USB diagnostics, telemetry, test patterns, button state handling and a minimal BLE programming-mode transfer.

Host-test asset parsing, gamma conversion, frame scheduling and runtime-estimator maths before relying on target hardware. Do not create production drivers until exact devices and the machine-readable board pin map are frozen.

## Colour conversion core

The first implementation is a platform-independent C++17 [colour transform](core/include/rgb_badge/color_transform.h), supporting the software portion of DSP-003/005. It converts RGB888 art into three normalized 16-bit linear intensities. It has no GPIO, charger, current-limit, radio or driver-register interfaces.

Create a transform from a 256-entry gamma table, RGB white-balance attenuations and an explicit fixed brightness. All factors use unsigned normalized 16-bit values: 0 means off and 65535 means unity/full scale. White balance attenuates channels; it does not amplify beyond the table's output. Each channel computes `round(gamma[input] × balance × brightness / 65535²)` with 64-bit integer arithmetic and a single final rounding. No floating point or heap allocation is required by the core.

Creation rejects tables with nonzero black, incomplete full scale or decreasing entries; monotonic plateaus are allowed. The table is copied, and existing transforms have no setting mutators, so changing caller data cannot silently change brightness or gamma. `identity_gamma()` is a linear software helper; neither it nor the synthetic quadratic test table is a measured optical calibration. Choose the production table/white balance from coupon measurements. The normalized result still needs reviewed driver encoding, scan timing and hardware current limits.

Run the host check from the repository root:

```sh
./tools/check-firmware-core.sh
```

The runner uses the local C++ compiler (`CXX` may select another executable), strict warnings, AddressSanitizer and UndefinedBehaviorSanitizer, with sanitizer recovery disabled so findings fail the run. Build output stays in ignored `firmware/build/host/`. Tests cover all 256 source levels, channel independence, nonlinear golden values, zero/full brightness, attenuation bounds, monotonicity, copied settings, invalid tables, low-intensity rounding and maximum arithmetic.

[Validation evidence](review/color-transform-host-check-2026-10-21.json) records the source hashes, compiler and actual host result. There is no ESP-IDF application/target build or hardware test yet. The asset pipeline below extends the host preparation; scheduling, storage, telemetry and the reviewed board pin map remain separate work.

## Lossless asset pipeline

The [RGBB v1 specification](asset-format.md) and [ADR 0035](../docs/decisions/0035-host-asset-container.md) define the provisional host container. The standard-library-only [compiler](../tools/compile-assets.py) preserves exact RGB888 pixels and microsecond durations, choosing the smallest raw, RGB-run or palette-run frame. The [opt-in v2 extension](asset-format-v2.md), under ADR 0036, also considers lossless XOR residuals from the preceding validated frame. Frames with more than 256 colours remain exact. No gamma, brightness, resampling or quantization is applied during compilation.

The C++17 [sequential reader](core/include/rgb_badge/asset_reader.h) validates file structure, checksums, dimensions, frame/pixel counts and work limits. It borrows immutable input and writes into a caller-owned buffer without heap allocation. Errors are distinct from end-of-asset; checksum failure clears the affected frame to black without advancing. There are no GPIO, radio, filesystem or flash-writing interfaces in the core. CRC is not upload authentication.

```sh
python3 tools/compile-assets.py input.json firmware/build/example.rgbb
./tools/check-assets.sh
```

Input JSON has version 1 or 2, width 16 or 48, height 16, and a `frames` list. Each frame contains `duration_us` and `rgb888` (hex-encoded packed pixels). Unknown/duplicate keys and invalid scalar types are rejected. The Python `encode_asset(width, height, frames)` API defaults to version 1; `version=2` opts into deltas. Image import is a later layer. Output binaries belong in the ignored build directory.

Version 2 requires an independent first frame and at most 59 consecutive deltas; the compiler forces keys at indices 0, 60, 120, …. Full frames win size ties, so opting into v2 never increases encoded size. The reader snapshots validated RGB into its own 768-pixel reference array, independent of caller output. Structural/checksum failures invalidate the reference; rewind rebuilds it. Argument errors permit retry. The reader object is 2,368 bytes on the tested Apple arm64 host, including 2,304 RGB reference channel bytes. Even v1 reader instances contain this array. Target stack/object placement and decode latency are still unqualified.

The host suite includes native malformed/truncated/mutated input checks, all codecs, output guards, a decode-to-colour golden pixel and Python/C++ byte-and-duration comparisons. [Retained evidence](review/asset-pipeline-host-check-2026-10-21.json) identifies compiler, source hashes and results. The [host-software workflow](../.github/workflows/host-software.yml) runs both software suites on GitHub with read-only repository access. It does not validate KiCad, target timing or hardware.

The format bounds (16 MiB encoded, 16 million decoded pixels per asset) are parser limits, not flash-partition allocations. Representative five-minute content capacity alongside dual application slots, target decode speed, frame scheduling, flash/update recovery and production calibration remain unverified.

The [synthetic capacity screen](asset-capacity.md) encodes 24 clips totalling five minutes at 60 source frames/s. Changing solids and moving bars occupy about 0.430/1.510 MiB in both versions. The high-colour no-run set drops from 39.826 MiB in v1 to 1.113 MiB in v2. These generated families are not representative art or STO-001 acceptance. Run `python3 tools/screen-asset-capacity.py --version 2 --report firmware/build/asset-capacity-v2.json` to reproduce v2 sizes; omit `--version` for the v1 baseline. CI reproduces both reports.
