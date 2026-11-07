#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Compile lossless RGBB v1/v2 assets using only the Python standard library."""
import argparse
import json
from pathlib import Path
import struct
import zlib

MAX_ASSET_BYTES = 16 * 1024 * 1024
MAX_DECODED_PIXELS = 16_000_000
KEYFRAME_INTERVAL = 60


def integer(value, label, minimum, maximum):
    if type(value) is not int or not minimum <= value <= maximum:
        raise ValueError(f'{label} must be an integer in {minimum}..{maximum}')
    return value


def runs(pixels):
    start = 0
    while start < len(pixels):
        end = start + 1
        while end < len(pixels) and end - start < 256 and pixels[end] == pixels[start]:
            end += 1
        yield end - start, pixels[start]
        start = end


def encode_frame(rgb, pixel_count):
    if not isinstance(rgb, bytes) or len(rgb) != pixel_count * 3:
        raise ValueError(f'each frame must contain exactly {pixel_count * 3} packed RGB bytes')
    pixels = [rgb[i:i+3] for i in range(0, len(rgb), 3)]
    repeated = list(runs(pixels))
    rgb_runs = b''.join(bytes([count-1]) + color for count, color in repeated)
    candidates = [(len(rgb), 0, 0, rgb), (len(rgb_runs), 1, 0, rgb_runs)]
    palette = dict.fromkeys(pixels)
    if len(palette) <= 256:
        indices = {color: i for i, color in enumerate(palette)}
        payload = b''.join(palette) + b''.join(bytes([count-1, indices[color]])
                                              for count, color in repeated)
        candidates.append((len(payload), 2, len(palette), payload))
    _, codec, count, payload = min(candidates, key=lambda item: (item[0], item[1]))
    return codec, count, payload


def encode_asset(width, height, frames, *, version=1):
    """frames is a finite iterable of (duration_us, packed_rgb_bytes) pairs."""
    integer(width, 'width', 16, 48)
    integer(height, 'height', 16, 16)
    integer(version, 'version', 1, 2)
    if width not in (16, 48):
        raise ValueError('supported dimensions are 16x16 and 48x16')
    pixels = width * height
    body = bytearray()
    frame_count = total_duration = 0
    previous = None
    for duration, rgb in frames:
        integer(duration, 'duration_us', 1, 0xffffffff)
        frame_count += 1
        if frame_count > MAX_DECODED_PIXELS // pixels:
            raise ValueError('asset exceeds the decoded-pixel work limit')
        codec, palette_count, payload = encode_frame(rgb, pixels)
        if version == 2 and previous is not None and (frame_count-1) % KEYFRAME_INTERVAL:
            residual = bytes(a ^ b for a, b in zip(rgb, previous))
            delta_codec, delta_palette, delta_payload = encode_frame(residual, pixels)
            # A raw delta cannot beat raw/full storage; ties prefer full frames.
            if delta_codec and len(delta_payload) < len(payload):
                codec, palette_count, payload = delta_codec+2, delta_palette, delta_payload
        body += struct.pack('<IBBHII', duration, codec, 0, palette_count,
                            len(payload), zlib.crc32(rgb))
        body += payload
        total_duration += duration
        previous = rgb
        if len(body) + 32 > MAX_ASSET_BYTES:
            raise ValueError('asset exceeds the encoded-size limit')
    if not frame_count:
        raise ValueError('asset must contain at least one frame')
    header = struct.pack('<4sHHHHIQII', b'RGBB', version, 32, width, height,
                         frame_count, total_duration, len(body), zlib.crc32(body))
    return header + body


def from_manifest(document):
    if type(document) is not dict or set(document) != {'version', 'width', 'height', 'frames'}:
        raise ValueError('manifest requires exactly version, width, height and frames')
    integer(document['version'], 'version', 1, 2)
    frames = document['frames']
    if type(frames) is not list:
        raise ValueError('frames must be a list')

    def source_frames():
        for frame in frames:
            if type(frame) is not dict or set(frame) != {'duration_us', 'rgb888'}:
                raise ValueError('each frame requires exactly duration_us and rgb888')
            if type(frame['rgb888']) is not str:
                raise ValueError('rgb888 must be a hex string')
            try:
                pixels = bytes.fromhex(frame['rgb888'])
            except ValueError as error:
                raise ValueError('rgb888 contains invalid hex') from error
            yield frame['duration_us'], pixels
    return encode_asset(document['width'], document['height'], source_frames(), version=document['version'])


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f'duplicate JSON field: {key}')
        result[key] = value
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('manifest', type=Path)
    parser.add_argument('output', type=Path)
    args = parser.parse_args()
    try:
        if args.manifest.resolve() == args.output.resolve():
            raise ValueError('input and output paths must differ')
        encoded = from_manifest(json.loads(args.manifest.read_text(), object_pairs_hook=unique_object))
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_bytes(encoded)
    except (ValueError, OSError, TypeError) as error:
        parser.error(str(error))
    print(json.dumps({'format': 'RGBB'+str(struct.unpack_from('<H', encoded, 4)[0]), 'encoded_bytes': len(encoded),
                      'frame_count': struct.unpack_from('<I', encoded, 12)[0]}))


if __name__ == '__main__':
    main()
