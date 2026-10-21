<!-- SPDX-License-Identifier: Apache-2.0 -->

# RGBB asset container, version 1

Development format under [ADR 0035](../docs/decisions/0035-host-asset-container.md). All integers are unsigned little-endian. Pixels are exact RGB888, top-to-bottom rows and left-to-right columns. Dimensions are either 16 × 16 or 48 × 16. No gamma, brightness or hardware register encoding is stored here.

## File header: 32 bytes

| Offset | Field | Bytes | Value |
|---:|---|---:|---|
| 0 | Magic | 4 | ASCII `RGBB` |
| 4 | Version | 2 | 1 |
| 6 | Header size | 2 | 32 |
| 8 | Width | 2 | 16 or 48 |
| 10 | Height | 2 | 16 |
| 12 | Frame count | 4 | positive |
| 16 | Total duration, microseconds | 8 | exact sum of frame durations |
| 24 | Body length | 4 | exact remaining file length |
| 28 | Body CRC-32 | 4 | IEEE reflected CRC-32 of all body bytes |

IEEE CRC-32 uses polynomial `0xedb88320`, initial state `0xffffffff` and final XOR `0xffffffff`; `123456789` gives `0xcbf43926`. CRC is corruption detection, not authentication. The body contains exactly the declared frames with no padding or trailing bytes. Encoded size is at most 16 MiB including the header; frame count × width × height is at most 16,000,000 pixels. These bounds do not reserve a flash partition.

## Frame header: 16 bytes followed by payload

| Offset | Field | Bytes | Value |
|---:|---|---:|---|
| 0 | Duration, microseconds | 4 | 1…4294967295 |
| 4 | Codec | 1 | 0, 1 or 2 |
| 5 | Reserved | 1 | zero |
| 6 | Palette count | 2 | zero for codecs 0/1, 1…256 for codec 2 |
| 8 | Payload length | 4 | exact bytes after this frame header |
| 12 | Decoded CRC-32 | 4 | CRC of exactly width × height RGB triplets |

- **0, raw RGB888:** exactly three bytes per pixel, no palette.
- **1, RGB runs:** four-byte records `[count_minus_one, red, green, blue]`. Each emits 1…256 identical pixels.
- **2, palette runs:** `palette_count` RGB triplets, then two-byte records `[count_minus_one, palette_index]`. Every index must be below the palette count; records emit 1…256 pixels. Duplicate palette colours are accepted, though the compiler emits a unique first-occurrence palette.

Run records must end exactly at the payload boundary and emit exactly the frame's pixel count. Underflow, overflow, unknown codecs and nonzero reserved fields are errors. Frames are independent, so losing a previous frame cannot change the next frame's decoded pixels.

## Compiler and decoder contract

`tools/compile-assets.py` consumes JSON with exactly `version`, `width`, `height` and `frames`. Version is 1. Each frame has exactly `duration_us` and `rgb888`, a hex string for all packed pixels. Integer fields reject booleans. The Python API accepts packed RGB bytes directly. Image import and phone transfer are future layers.

The compiler chooses the shortest payload among raw, RGB runs and (when there are at most 256 colours) palette runs. Ties use ascending codec number. Palette order is first occurrence; runs are split at 256 pixels. Compilation is deterministic and lossless, including frames with more than 256 colours. It reports actual encoded size; it never drops frames or quantizes colours.

The C++ reader borrows input that must remain alive and unchanged. Opening verifies body CRC, all frame structures/pixel counts, resource bounds and total duration. Sequential decode verifies each decoded CRC, writes at most the expected pixels and advances only on success. Insufficient/overlapping output is rejected before writing. Decoded-CRC failure clears the expected output pixels to black and leaves the cursor unchanged. The caller must handle errors and any actual display blanking. `rewind()` restarts iteration; end is distinct from failure.

These host contracts establish neither target throughput nor five-minute content capacity alongside dual application slots. There is no production asset filesystem, authenticated upload, target flash writer or hardware display driver yet.
