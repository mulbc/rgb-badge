<!-- SPDX-License-Identifier: Apache-2.0 -->

# Host library and asset inspection

[ADR 0040](../../docs/decisions/0040-reusable-host-build-and-inspector.md) adds a separate host build for the five existing C++17 core modules. It builds one `rgb_badge_core` static library and links native tests, integration adapters and the `rgbb-inspect` utility to it. No ESP-IDF application, GPIO, radio, matrix scan or hardware-arm path is added.

Prerequisites are CMake 3.20 or newer and a GNU/Clang-family C++17 compiler. The complete test build also requires Python 3.9 or newer, using only its standard library. No third-party package download is part of configuration or build. Build output belongs in ignored `firmware/build/`.

## Complete verification

From the repository root:

```sh
./tools/check-host-firmware.sh
```

The runner configures a Debug build, builds with two parallel jobs and runs eleven CTest entries: five native suites, three compiler/native integration suites, inspection CLI checks and both byte-identical capacity reproductions. The core compiles with `-fno-exceptions -fno-rtti`; host tools/test fixtures may allocate and use normal host runtime facilities. Strict warnings and fail-fast AddressSanitizer/UndefinedBehaviorSanitizer are enabled. This checks host compatibility with exception/RTTI-free core compilation, not ESP-IDF linkage or target behavior.

`CXX` selects a compiler executable, for example `CXX=clang++ ./tools/check-host-firmware.sh`. The wrapper passes it explicitly to CMake so a cached compiler cannot silently override that selection. Focused `check-firmware-core.sh`, `check-assets.sh`, `check-playback.sh`, `check-mode-button.sh` and `check-content-session.sh` runners remain available. GitHub's host workflow runs the unified verification independently with GCC and Clang, plus an optimized inspection build without test targets or sanitizers.

## Inspect an encoded asset

After the complete build:

```sh
firmware/build/cmake-host/rgbb-inspect firmware/build/example.rgbb
```

`rgbb-inspect --help` prints usage. The tool bounds encoded input at 16 MiB before allocation, reads an owned byte snapshot and uses the canonical reader for both RGBB versions. It sequentially decodes **every frame**, including XOR references and keyframes, before emitting a single JSON success summary. The summary contains format/version, dimensions, decoded frame count, exact total microseconds, encoded size, total expanded RGB888 bytes and `all_frame_checksums_valid: true`. No pixels, timing, brightness or file bytes are changed.

On failure it returns 1, reports a readable I/O/container/frame error on stderr and emits no success summary on stdout. A later decoded CRC failure identifies the zero-based frame index. Usage errors return 2; help and complete validation return 0. The tool accepts file paths, including spaces; it does not read stdin or write an output asset. CRC integrity is not upload authentication, optical calibration, representative capacity or hardware qualification.

For a standalone optimized utility without Python discovery or test targets:

```sh
cmake -S firmware/host -B firmware/build/cmake-release -DCMAKE_BUILD_TYPE=Release -DBUILD_TESTING=OFF -DRGB_BADGE_SANITIZERS=OFF
cmake --build firmware/build/cmake-release --parallel 2
firmware/build/cmake-release/rgbb-inspect --help
```

Consumers inside this host project link to `rgb_badge_core`, which exports its include path and C++17 requirement. The configured host warning/sanitizer options propagate to linked host executables; exception/RTTI disable flags apply only to the core. This is a reusable in-tree host target, not an installed SDK package or a target toolchain configuration.

## Retained evidence and remaining work

[Local validation evidence](../review/host-build-inspection-check-2026-10-21.json) records exact source hashes, compiler/CMake/Python versions, generated compile flags and raw logs. The inspection tests cover both dimensions/versions and encodings, 64-bit durations, 125 high-colour v2 frames, early/late decoded corruption, malformed input, an oversized sparse file, Unicode/spaced paths, missing input and usage behavior. Existing source assets and capacity reports are unchanged.

Target memory placement/copy costs, decode/latch/scan timing, actual BLE/blanking/arming, authenticated transfer/update recovery, partitions, representative art and independent hardware review remain open. No board has been built or measured by these host checks, and no fabrication release is produced.
