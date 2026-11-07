<!-- SPDX-License-Identifier: Apache-2.0 -->

# RGBB version 2: bounded XOR deltas

Host-development extension under [ADR 0036](../docs/decisions/0036-bounded-xor-asset-deltas.md). The [version 1 specification](asset-format.md) still defines the byte order, dimensions, file/frame headers, reserved fields, CRC polynomial and resource limits. Version 2 changes the file version field to 2 and adds these codecs:

| Codec | Payload | Reconstruction |
|---:|---|---|
| 0/1/2 | Existing full-frame raw/RGB-run/palette-run data | Independent RGB888 frame |
| 3 | RGB-run data with palette count zero | Decode residual triplets, then XOR each channel with the previous validated frame |
| 4 | Palette-run data with 1…256 residual colours | Decode residual triplets, then XOR each channel with the previous validated frame |

Residual packets obey the same exact-pixel-count, palette-index and payload-boundary rules as their corresponding full-frame codecs. Decoded CRC-32 always covers the reconstructed RGB888 frame, not residual bytes. There is no raw-delta codec because it cannot save space over an independent raw frame.

The first frame must be independent. A chain may contain at most 59 consecutive deltas. The compiler forces independent frames at zero-based indices 0, 60, 120, …, and may choose additional full frames whenever they are no larger. Cadence is measured in frames, not elapsed time. This bounds dependencies without implementing random seeking or automatic error recovery.

The Python API defaults to version 1; use `encode_asset(..., version=2)` or JSON `"version": 2` to opt in. It chooses the smallest exact payload; ties prefer the lower numbered codec, so a full frame wins a tie with a delta. Every version 2 frame is therefore no larger than the corresponding version 1 choice. No pixels, durations, frame rate or brightness are degraded. A version 1 reader must reject a version 2 file; the updated reader supports both.

The reader owns one 768-pixel reference array, containing 2,304 RGB channel bytes, plus metadata/padding. This enlarges the reader object; it is not a heap allocation. Output buffers can be changed/reused between calls without modifying the reference. Target stack/object placement and decode throughput remain unqualified.

Only a frame with a valid reconstructed CRC becomes a reference. On structural or decoded-CRC failure, invalidate the reference and keep the cursor fixed. A decoded-CRC failure clears the expected destination pixels to black. A subsequent delta without a valid base returns `MissingReference` without writing. Argument errors (null, short or overlapping output) permit retry without discarding a valid reference. `rewind()` discards reference validity and restarts at the independent first frame. Callers must handle errors and actual display blanking.

Container CRC is corruption detection, not upload authentication. Synthetic storage improvements do not establish STO-001 or target 60 Hz playback. Hardware interlocks, current limits, partitions and fabrication gates remain unchanged.
