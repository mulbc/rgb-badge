<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0040: Reusable host build and complete asset inspection

- Date: 2026-10-21
- Status: Accepted for host software; ESP-IDF/target qualification pending
- Scope: Repeatable DSP-003/004/005/006 and STO-001 software verification

## Decision

Build the five existing C++17 core modules as one reusable static library in a separate `firmware/host` CMake project. Keep the future ESP-IDF application entry point separate. Compile the core without exceptions or RTTI on supported GNU/Clang-family host compilers; this is a host compatibility check, not a target build. Use strict warnings, optional host sanitizers enabled by default and CTest for all native and cross-language suites plus byte-identical v1/v2 capacity reproduction. Preserve focused shell runners for individual checks.

Add a host-only `rgbb-inspect` executable linked to this library. Bound input before allocation by the existing encoded-file limit, open through the canonical reader, decode every frame sequentially and verify the entire asset before emitting a JSON success summary. This catches decoded-frame CRC failures that header/body validation alone cannot detect. Report dimensions, wire version, frame count, exact duration and encoded/decoded byte counts. Return nonzero and emit no success summary for invalid/missing/oversized input or a bad later frame. CRC verifies accidental integrity, not authenticity or suitability for hardware.

Run the unified host build with both GCC and Clang in CI. Record actual compiler/build configuration, source hashes, raw test logs and unresolved findings. No new wire format, calibration, partition, device driver, GPIO/radio/arm path or current limit is introduced. No target timing, representative art, physical blanking or fabrication gate is closed.
