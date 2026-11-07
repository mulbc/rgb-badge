<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0042: Exact PNG and GIF import for host assets

- Date: 2026-10-21
- Status: Accepted for host content preparation; target transfer/storage pending
- Scope: DSP-003/STO-001; no electrical change

## Decision

Add a separate optional Pillow-based importer feeding the existing RGBB compiler.
Accept static 8-bit PNG and GIF canvases already sized 16 × 16 or 48 × 16.
Preserve decoded RGB values, composited GIF frame order and positive GIF delays
(milliseconds converted exactly to microseconds). Import one animation cycle;
report source loop metadata without expanding repeats. Static images require
an explicit duration. Reject absent/zero GIF delays rather than guess playback
timing. No resize, crop, frame merging, quantization, gamma or brightness change.

Require an explicit RGB background whenever a decoded frame has nonopaque
alpha; otherwise reject. Composite each channel using integer rounding:
`(source × alpha + background × (255 − alpha) + 127) // 255`.
Treat RGB sample values as source art; reject embedded ICC/EXIF metadata rather
than silently discard colour management or orientation. Reject 16-bit PNG and
APNG in this first importer instead of truncating samples or omitting frames.

Snapshot input with a 16 MiB read bound. Enforce the existing decoded-work and
encoded-asset limits while iterating, without first scanning an unbounded frame
count. Publish output only after successful complete import using an atomic
replacement in the output directory, and refuse source/output path aliases.
Pin the optional dependency and test it separately from the standard-library
compiler and C++ core. Use only generated project-owned fixtures in tests.

## Verification and limits

Compare imported pixels/durations with independently constructed expectations
through the native decoder, including palette changes, partial GIF frames and
disposal modes. Verify alpha, metadata, bounds, malformed/truncated inputs,
determinism and failed-import output preservation. Existing compiler golden
bytes and capacity reports must remain unchanged. This prepares real artwork
but does not establish representative five-minute capacity, target playback,
phone transfer, physical display behavior or fabrication approval.
