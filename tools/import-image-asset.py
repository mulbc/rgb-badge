#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Import exact-size static PNG or one GIF cycle into lossless RGBB assets."""
import argparse
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import struct
import tempfile

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('compile_assets', ROOT / 'tools/compile-assets.py')
compiler = importlib.util.module_from_spec(spec)
spec.loader.exec_module(compiler)
MAX_INPUT_BYTES = 16 * 1024 * 1024


def background_rgb(value):
    if len(value) != 6 or any(c not in '0123456789abcdefABCDEF' for c in value):
        raise argparse.ArgumentTypeError('background must be six RGB hex digits, e.g. 000000')
    return tuple(bytes.fromhex(value))


def read_source(path):
    with path.open('rb') as stream:
        data = stream.read(MAX_INPUT_BYTES + 1)
    if len(data) > MAX_INPUT_BYTES:
        raise ValueError('source exceeds the 16 MiB input limit')
    return data


def gif_delays(data):
    """Validate block framing so decoder EOF cannot hide a truncated last frame.

    This checks the GIF envelope, not LZW pixels (Pillow decodes those). Graphic
    control applies to one following image; plain-text rendering is unsupported.
    """
    if len(data) < 13:
        raise ValueError('truncated GIF header')
    width, height = struct.unpack_from('<HH', data, 6)
    if (width, height) not in ((16, 16), (48, 16)):
        raise ValueError('source canvas must be exactly 16x16 or 48x16')
    position = 13
    flags = data[10]

    def take(count):
        nonlocal position
        end = position + count
        if end > len(data):
            raise ValueError('truncated GIF block')
        part = data[position:end]
        position = end
        return part

    def subblocks():
        while True:
            count = take(1)[0]
            if not count:
                return
            take(count)

    if flags & 128:
        take(3 * (2 << (flags & 7)))
    delays, pending_delay = [], None
    max_frames = compiler.MAX_DECODED_PIXELS // (width * height)
    while True:
        marker = take(1)[0]
        if marker == 0x3b:
            if position != len(data) or not delays or pending_delay is not None:
                raise ValueError('invalid GIF trailer or unfinished graphic control')
            return delays
        if marker == 0x21:
            label = take(1)[0]
            if label == 0xf9:
                if take(1) != b'\x04' or pending_delay is not None:
                    raise ValueError('invalid GIF graphic control block')
                control = take(4)
                if control[0] & 0xe2 or ((control[0] >> 2) & 7) > 3 or take(1) != b'\0':
                    raise ValueError('unsupported GIF graphic control')
                pending_delay = struct.unpack_from('<H', control, 1)[0] * 10000
            elif label in (0xfe, 0xff):
                subblocks()
            else:
                raise ValueError('unsupported GIF extension (including plain-text rendering)')
        elif marker == 0x2c:
            if len(delays) >= max_frames:
                raise ValueError('asset exceeds the decoded-pixel work limit')
            compiler.integer(pending_delay, f'GIF frame {len(delays)} duration_us', 1, 0xffffffff)
            left, top, w, h, packed = struct.unpack('<HHHHB', take(9))
            if not w or not h or left+w > width or top+h > height or packed & 0x18:
                raise ValueError('invalid GIF frame rectangle or reserved bits')
            if packed & 128:
                take(3 * (2 << (packed & 7)))
            if not 2 <= take(1)[0] <= 8:
                raise ValueError('invalid GIF LZW code size')
            subblocks()
            delays.append(pending_delay)
            pending_delay = None
        else:
            raise ValueError('invalid GIF block marker')


def import_image(data, *, version=1, still_duration_us=None, background=None):
    """Return (encoded bytes, summary), preserving decoded samples and GIF delays.

    Caller supplies an immutable, bounded snapshot. Pillow is optional and is
    imported here so the existing compiler/build remain dependency-free.
    """
    from PIL import Image, __version__ as pillow_version

    if not isinstance(data, bytes) or len(data) > MAX_INPUT_BYTES:
        raise ValueError('source must be bytes within the 16 MiB input limit')
    compiler.integer(version, 'version', 1, 2)
    if still_duration_us is not None:
        compiler.integer(still_duration_us, 'still_duration_us', 1, 0xffffffff)
    if background is not None:
        if type(background) is not tuple or len(background) != 3:
            raise ValueError('background must be an RGB tuple')
        for channel in background:
            compiler.integer(channel, 'background channel', 0, 255)
    # Pillow converts true-colour 16-bit PNG to 8-bit internally. Inspect IHDR
    # before any decode so that reduction can never happen silently.
    expected_delays = None
    if data.startswith(b'\x89PNG\r\n\x1a\n'):
        if len(data) < 33 or data[12:16] != b'IHDR' or data[24] != 8:
            raise ValueError('only 8-bit PNG samples are supported')
        if struct.unpack_from('>II', data, 16) not in ((16, 16), (48, 16)):
            raise ValueError('source canvas must be exactly 16x16 or 48x16')
        # Inspect actual chunk names, not byte substrings inside compressed
        # data. Pillow can intentionally fall back to static PNG for a broken
        # animation control chunk; that fallback would discard source intent.
        offset = 8
        while offset + 12 <= len(data):
            length = struct.unpack_from('>I', data, offset)[0]
            name = data[offset+4:offset+8]
            if name in (b'acTL', b'fcTL', b'fdAT'):
                raise ValueError('APNG is not supported; no animation frames were imported')
            if name in (b'iCCP', b'eXIf'):
                raise ValueError('ICC/EXIF metadata is unsupported; export untagged source art explicitly')
            offset += length + 12
        with Image.open(io.BytesIO(data), formats=['PNG']) as verification:
            verification.verify()
    elif data.startswith((b'GIF87a', b'GIF89a')):
        expected_delays = gif_delays(data)

    with Image.open(io.BytesIO(data), formats=['PNG', 'GIF']) as image:
        width, height = image.size
        if (width, height) not in ((16, 16), (48, 16)):
            raise ValueError('source canvas must be exactly 16x16 or 48x16; resize explicitly before import')
        source_format = image.format
        if source_format == 'PNG':
            if getattr(image, 'is_animated', False):
                raise ValueError('APNG is not supported; no animation frames were imported')
            if still_duration_us is None:
                raise ValueError('static PNG requires --still-duration-us')
        elif still_duration_us is not None:
            raise ValueError('--still-duration-us is only for static PNG; GIF uses its own delays')
        loop = image.info.get('loop') if source_format == 'GIF' else None
        frame_count = total_duration = 0
        alpha_composited = False
        max_frames = compiler.MAX_DECODED_PIXELS // (width * height)

        def frames():
            nonlocal frame_count, total_duration, alpha_composited
            index = 0
            while True:
                try:
                    image.seek(index)
                except EOFError:
                    break
                if index >= max_frames:
                    raise ValueError('asset exceeds the decoded-pixel work limit')
                if image.size != (width, height):
                    raise ValueError(f'frame {index} changes the source canvas')
                if 'icc_profile' in image.info or 'exif' in image.info:
                    raise ValueError('ICC/EXIF metadata is unsupported; export untagged source art explicitly')
                if source_format == 'GIF':
                    delay = image.info.get('duration')
                    compiler.integer(delay, f'GIF frame {index} duration_ms', 1, 0xffffffff // 1000)
                    duration = delay * 1000
                    if index >= len(expected_delays) or duration != expected_delays[index]:
                        raise ValueError('GIF decoded timing disagrees with source blocks')
                else:
                    duration = still_duration_us
                # GIF seek/load applies local palettes, offsets and disposal.
                # Never crop to a GIF's local changed rectangle.
                rgba = image.convert('RGBA').tobytes()
                # PNG metadata may follow IDAT and only become visible on load.
                if 'icc_profile' in image.info or 'exif' in image.info:
                    raise ValueError('ICC/EXIF metadata is unsupported; export untagged source art explicitly')
                rgb = bytearray()
                for offset in range(0, len(rgba), 4):
                    red, green, blue, alpha = rgba[offset:offset+4]
                    if alpha != 255:
                        if background is None:
                            raise ValueError(f'frame {index} has transparency; supply --background RRGGBB')
                        alpha_composited = True
                        rgb.extend((channel * alpha + base * (255-alpha) + 127) // 255
                                   for channel, base in zip((red, green, blue), background))
                    else:
                        rgb.extend((red, green, blue))
                frame_count += 1
                total_duration += duration
                yield duration, bytes(rgb)
                index += 1

        encoded = compiler.encode_asset(width, height, frames(), version=version)
        if expected_delays is not None and frame_count != len(expected_delays):
            raise ValueError('GIF decoder did not return every source frame')
    summary = dict(format='RGBB', version=version, source_format=source_format,
                   source_sha256=hashlib.sha256(data).hexdigest(),
                   asset_sha256=hashlib.sha256(encoded).hexdigest(),
                   width=width, height=height, frame_count=frame_count,
                   duration_us=total_duration, encoded_bytes=len(encoded),
                   imported_cycles=1, source_loop=loop, pillow_version=pillow_version,
                   background_rgb=list(background) if background is not None else None,
                   alpha_composited=alpha_composited)
    return encoded, summary


def atomic_write(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(dir=path.parent, prefix='.rgbb-', delete=False) as stream:
            temporary = Path(stream.name)
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path)
    parser.add_argument('output', type=Path)
    parser.add_argument('--version', type=int, choices=(1, 2), default=1)
    parser.add_argument('--still-duration-us', type=int)
    parser.add_argument('--background', type=background_rgb)
    args = parser.parse_args()
    try:
        if args.source.resolve() == args.output.resolve() or (
                args.output.exists() and args.source.samefile(args.output)):
            raise ValueError('input and output paths must differ, including aliases')
        encoded, summary = import_image(read_source(args.source), version=args.version,
                                       still_duration_us=args.still_duration_us, background=args.background)
        atomic_write(args.output, encoded)
    except ImportError:
        parser.error('image import requires Pillow; install tools/image-import-requirements.txt in a virtual environment')
    except (ValueError, OSError, EOFError, SyntaxError, struct.error) as error:
        parser.error(str(error))
    print(json.dumps(summary, sort_keys=True))


if __name__ == '__main__':
    main()
