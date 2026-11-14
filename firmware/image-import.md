<!-- SPDX-License-Identifier: Apache-2.0 -->

# Prepare PNG and GIF artwork

[ADR 0042](../docs/decisions/0042-exact-image-import.md) adds an optional host
importer that feeds the existing lossless RGBB compiler. Start with a static
8-bit PNG or a GIF whose complete canvas is exactly **16 × 16** (coupon) or
**48 × 16** (final). Dimensions are pixels. Export at the intended size before
import; there is no implicit resizing, cropping, colour reduction or dimming.

Create the optional environment once, from the repository root:

```sh
python3 -m venv firmware/build/image-import-venv
firmware/build/image-import-venv/bin/python -m pip install --only-binary=:all: -r tools/image-import-requirements.txt
```

Python 3.11 or newer is required by the pinned Pillow 13.0.0 dependency. The
existing JSON compiler, native library and default host checks still work
without Pillow. No third-party artwork is included in this repository.
Dependency references: [Pillow release](https://pypi.org/project/pillow/13.0.0/)
and [official image-format documentation](https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html).

For a static picture, supply the intended display duration in microseconds:

```sh
firmware/build/image-import-venv/bin/python tools/import-image-asset.py artwork.png firmware/build/artwork.rgbb --still-duration-us 2000000
```

For an animation, import one complete cycle with original GIF frame delays:

```sh
firmware/build/image-import-venv/bin/python tools/import-image-asset.py animation.gif firmware/build/animation.rgbb --version 2
```

Version 1 is the default; `--version 2` enables the existing lossless deltas.
Each GIF delay must be positive and present. GIF milliseconds are multiplied
by 1,000 exactly; no browser delay minimum, rounding, merging or frame dropping
is applied. Partial rectangles, local palettes and disposal are composited by
Pillow before RGB extraction. GIF loop metadata is reported as `source_loop`
(`null` when absent, `0` for infinite); it never expands repeated cycles into
stored frames. RGBB remains a one-shot timeline; this tool adds no loop policy
to the playback core. Even a single-frame GIF uses its encoded delay.
GIF block framing is checked independently before decoding; unfinished image
blocks cannot silently shorten a clip. Plain-text extensions, interactive
user-input controls, reserved disposal methods and trailing data are rejected.

Nonopaque decoded frames require `--background RRGGBB`, for example
`--background 000000` for black. Opaque RGB samples pass through unchanged.
Alpha blending rounds each channel as
`(source × alpha + background × (255 − alpha) + 127) // 255`.
The background fills remaining alpha after GIF disposal/composition; it does
not replace an opaque GIF global background. This is an explicit sample-value
operation, with no colour-space conversion, gamma or brightness correction.

Supported PNG modes are 8-bit RGB/RGBA, grayscale/grayscale-alpha and indexed
colour, including `tRNS` transparency. Other sample depths (including packed
1/2/4-bit indexed images), APNG and embedded ICC/EXIF metadata are rejected.
Export untagged 8-bit art explicitly; profile conversion and orientation must
be resolved in the source editor. PNG gamma/sRGB metadata does not change stored
sample values. Other formats such as JPEG/WebP are outside this importer.

Successful import prints one JSON summary containing dimensions, frame count,
exact duration, encoded size, source/output SHA-256, loop/background information
and Pillow version. Failure emits an error and no success JSON. The input read
is bounded at 16 MiB; the compiler's 16-million-decoded-pixel and 16-MiB-encoded
limits also apply. Output is replaced atomically only after complete encoding;
a failed import preserves an existing output. Source/output aliases are refused.
Use the ignored build directory for generated assets; never commit artwork you
do not have permission to distribute.

After building the [host tools](host/README.md), validate every decoded frame:

```sh
firmware/build/cmake-host/rgbb-inspect firmware/build/animation.rgbb
```

Run optional integration verification (including the native decoder):

```sh
cmake -S firmware/host -B firmware/build/cmake-image-import -DCMAKE_BUILD_TYPE=Debug -DBUILD_TESTING=ON -DRGB_BADGE_IMAGE_IMPORT_TESTS=ON -DPython3_EXECUTABLE="$PWD/firmware/build/image-import-venv/bin/python"
cmake --build firmware/build/cmake-image-import --target asset_decode --parallel 2
ctest --test-dir firmware/build/cmake-image-import --output-on-failure -R '^image_import$'
```

Independent stdlib-authored PNG/GIF fixtures cover pixels, delays, disposal,
palettes, alpha and rejected inputs. The optional CI job runs these checks with
native sanitizers. [Retained host evidence](review/image-import-check-2026-10-21.json)
records versions, source hashes and results. These generated fixtures are not
representative badge art. Representative capacity, target timing, phone upload,
hardware operation and independent Gate A remain open.
