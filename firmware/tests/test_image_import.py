#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Independent PNG/GIF fixtures compared with the native RGBB decoder."""
import argparse
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import struct
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
import zlib

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / 'tools/import-image-asset.py'
spec = importlib.util.spec_from_file_location('image_import', SCRIPT)
importer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(importer)
DECODER = None


def chunk(name, data):
    return struct.pack('>I', len(data)) + name + data + struct.pack('>I', zlib.crc32(name + data))


def png(width, height, pixels, *, color=2, depth=8, before=(), after=()):
    channels = {0: 1, 2: 3, 3: 1, 4: 2, 6: 4}[color]
    stride = width * channels * (2 if depth == 16 else 1)
    raw = b''.join(b'\0' + pixels[y*stride:(y+1)*stride] for y in range(height))
    return (b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', struct.pack('>IIBBBBB', width, height, depth, color, 0, 0, 0))
            + b''.join(chunk(*pair) for pair in before) + chunk(b'IDAT', zlib.compress(raw))
            + b''.join(chunk(*pair) for pair in after) + chunk(b'IEND', b''))


COLORS = ((0, 0, 0), (255, 0, 0), (0, 255, 0), (0, 0, 255))


def gif(frames, *, width=16, height=16, loop=None):
    """Literal GIF89a: independent of Pillow's encoder and optimizer.

    Frame dict: rectangle, indices, delay_cs, disposal, transparent, palette.
    Clear before each literal keeps LZW code width at three bits.
    """
    result = bytearray(b'GIF89a' + struct.pack('<HHBBB', width, height, 0x81, 0, 0))
    result.extend(channel for color in COLORS for channel in color)
    if loop is not None:
        result += b'!\xff\x0bNETSCAPE2.0\x03\x01' + struct.pack('<H', loop) + b'\0'
    for frame in frames:
        if frame.get('delay_cs') is not None:
            flags = frame.get('disposal', 1) << 2
            transparent = frame.get('transparent')
            if transparent is not None:
                flags |= 1
            result += b'!\xf9\x04' + bytes([flags]) + struct.pack('<H', frame['delay_cs'])
            result += bytes([transparent or 0, 0])
        left, top, w, h = frame.get('rectangle', (0, 0, width, height))
        palette = frame.get('palette')
        result += b',' + struct.pack('<HHHHB', left, top, w, h, 0x81 if palette else 0)
        if palette:
            result.extend(channel for color in palette for channel in color)
        indices = frame.get('indices', [1] * (w * h))
        assert len(indices) == w * h
        codes = [code for index in indices for code in (4, index)] + [5]
        bits = sum(code << (3 * i) for i, code in enumerate(codes))
        packed = bits.to_bytes((len(codes)*3+7)//8, 'little')
        result += b'\x02'
        for start in range(0, len(packed), 255):
            block = packed[start:start+255]
            result += bytes([len(block)]) + block
        result += b'\0'
    return bytes(result + b';')


class ImageImportTests(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory(prefix='rgb-image-test-')
        self.addCleanup(directory.cleanup)
        self.path = Path(directory.name)

    def cli(self, source, *options, output=None):
        path = self.path / 'source with spaces ☃.image'
        path.write_bytes(source)
        output = output or self.path / 'output.rgbb'
        result = subprocess.run([sys.executable, str(SCRIPT), str(path), str(output), *options],
                                capture_output=True, text=True, timeout=30)
        return result, output

    def check_frames(self, source, width, frames, **options):
        for version in (1, 2):
            encoded, summary = importer.import_image(source, version=version, **options)
            self.assertEqual(encoded, importer.import_image(source, version=version, **options)[0])
            self.assertEqual(encoded, importer.compiler.encode_asset(width, 16, frames, version=version))
            path = self.path / 'native.rgbb'
            path.write_bytes(encoded)
            result = subprocess.run([str(DECODER), str(path)], capture_output=True, timeout=30)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(result.stdout, b''.join(rgb for _, rgb in frames))
            self.assertEqual(json.loads(result.stderr), dict(version=version, width=width, height=16,
                duration_us=sum(d for d, _ in frames), durations_us=[d for d, _ in frames]))
            self.assertEqual(summary['frame_count'], len(frames))
            self.assertEqual(summary['source_sha256'], hashlib.sha256(source).hexdigest())
            self.assertEqual(summary['asset_sha256'], hashlib.sha256(encoded).hexdigest())
            self.assertEqual(summary['duration_us'], sum(d for d, _ in frames))
        return summary

    def test_truecolor_png_exact_order_and_768_colours(self):
        for width in (16, 48):
            rgb = bytes(channel for i in range(width*16) for channel in (i & 255, i >> 8, (i*17) & 255))
            self.check_frames(png(width, 16, rgb), width, [(0xffffffff, rgb)], still_duration_us=0xffffffff)

    def test_palette_grayscale_and_gray_alpha_png(self):
        indices = bytes(i % 4 for i in range(256))
        palette = bytes(channel for color in COLORS for channel in color)
        expected = bytes(channel for index in indices for channel in COLORS[index])
        self.check_frames(png(16, 16, indices, color=3, before=[(b'PLTE', palette)]),
                          16, [(10, expected)], still_duration_us=10)
        gray = bytes(range(256))
        self.check_frames(png(16, 16, gray, color=0), 16,
                          [(1, bytes(value for value in gray for _ in range(3)))], still_duration_us=1)
        gray_alpha = bytes(channel for value in gray for channel in (value, 255))
        self.check_frames(png(16, 16, gray_alpha, color=4), 16,
                          [(1, bytes(value for value in gray for _ in range(3)))], still_duration_us=1)

    def test_all_alpha_values_explicit_compositing(self):
        rgba = bytes(channel for alpha in range(256) for channel in (231, 19, 91, alpha))
        background = (17, 203, 8)
        expected = bytes((value*alpha+base*(255-alpha)+127)//255
                         for alpha in range(256) for value, base in zip((231, 19, 91), background))
        source = png(16, 16, rgba, color=6)
        with self.assertRaisesRegex(ValueError, 'transparency'):
            importer.import_image(source, still_duration_us=5)
        summary = self.check_frames(source, 16, [(5, expected)], still_duration_us=5, background=background)
        self.assertTrue(summary['alpha_composited'])

    def test_transparent_palette_and_rgb_png(self):
        # tRNS transparency on palette and on an RGB colour must not be lost.
        palette = bytes(channel for color in COLORS for channel in color)
        source = png(16, 16, bytes([1, 2])*128, color=3,
                     before=[(b'PLTE', palette), (b'tRNS', bytes([255, 0, 255, 255]))])
        expected = bytes([11, 22, 33, 0, 255, 0])*128
        self.check_frames(source, 16, [(1, expected)], still_duration_us=1, background=(11, 22, 33))
        source = png(16, 16, bytes([255, 0, 0])*256, before=[(b'tRNS', struct.pack('>HHH', 255, 0, 0))])
        self.check_frames(source, 16, [(1, bytes([11, 22, 33])*256)], still_duration_us=1, background=(11, 22, 33))

    def test_gif_partial_rectangles_local_palette_and_exact_delays(self):
        custom = ((0, 0, 0), (17, 18, 19), (91, 92, 93), (255, 255, 255))
        source = gif([dict(delay_cs=1), dict(delay_cs=7, rectangle=(2, 3, 2, 1),
                     indices=[1, 2], palette=custom), dict(delay_cs=65535, rectangle=(15, 15, 1, 1), indices=[3])], loop=0)
        frame = bytearray(bytes([255, 0, 0])*256)
        frame[(3*16+2)*3:(3*16+4)*3] = bytes([17, 18, 19, 91, 92, 93])
        third = bytearray(frame)
        third[-3:] = bytes([0, 0, 255])
        summary = self.check_frames(source, 16, [(10000, bytes([255, 0, 0])*256),
                          (70000, bytes(frame)), (655350000, bytes(third))])
        self.assertEqual(summary['source_loop'], 0)
        self.assertEqual(summary['imported_cycles'], 1)

    def test_gif_dispose_background_previous_and_transparent_overlays(self):
        for disposal in (1, 2, 3):
            source = gif([dict(delay_cs=2), dict(delay_cs=3, disposal=disposal,
                          rectangle=(0, 0, 2, 1), indices=[2, 0], transparent=0),
                          dict(delay_cs=4, rectangle=(15, 15, 1, 1), indices=[3])], loop=4)
            first = bytes([255, 0, 0])*256
            second = bytearray(first)
            second[:3] = bytes([0, 255, 0])
            third = bytearray(second if disposal == 1 else first)
            if disposal == 2:
                # The initial canvas is opaque; restore its global background
                # (index zero), rather than replacing it with our alpha matte.
                third[:6] = bytes(6)
            third[-3:] = bytes([0, 0, 255])
            self.check_frames(source, 16, [(20000, first), (30000, bytes(second)), (40000, bytes(third))],
                              background=(11, 22, 33))

    def test_gif_transparent_initial_canvas_requires_background(self):
        source = gif([dict(delay_cs=1, transparent=0, indices=[0, 1]*128)])
        with self.assertRaisesRegex(ValueError, 'transparency'):
            importer.import_image(source)
        self.check_frames(source, 16, [(10000, bytes([9, 8, 7, 255, 0, 0])*128)], background=(9, 8, 7))

    def test_gif_missing_zero_delay_and_static_timing_rejected(self):
        for delay in (None, 0):
            for bad in (0, 1):
                frames = [dict(delay_cs=1), dict(delay_cs=1)]
                frames[bad]['delay_cs'] = delay
                with self.assertRaisesRegex(ValueError, 'duration_us'):
                    importer.import_image(gif(frames))
        with self.assertRaisesRegex(ValueError, 'only for static PNG'):
            importer.import_image(gif([dict(delay_cs=1)]), still_duration_us=10)
        source = png(16, 16, bytes(768))
        with self.assertRaisesRegex(ValueError, 'requires --still-duration-us'):
            importer.import_image(source)
        for duration in (True, 0, -1, 2**32):
            with self.assertRaises(ValueError):
                importer.import_image(source, still_duration_us=duration)

    def test_wrong_dimensions_depth_metadata_and_apng_rejected(self):
        for width, height in ((48, 15), (17, 16), (1, 1)):
            with self.assertRaisesRegex(ValueError, 'canvas'):
                importer.import_image(png(width, height, bytes(width*height*3)), still_duration_us=1)
        with self.assertRaisesRegex(ValueError, '8-bit PNG'):
            importer.import_image(png(16, 16, bytes(1536), depth=16), still_duration_us=1)
        for name, content in ((b'iCCP', b'profile\0\0'+zlib.compress(b'ICC data')),
                              (b'eXIf', b'II*\0\x08\0\0\0\0\0\0\0\0\0')):
            for location in ('before', 'after'):
                with self.subTest(name=name, location=location):
                    with self.assertRaisesRegex(ValueError, 'ICC/EXIF'):
                        importer.import_image(png(16, 16, bytes(768), **{location: [(name, content)]}), still_duration_us=1)
        from PIL import Image
        stream = io.BytesIO()
        Image.new('RGB', (16, 16), 'red').save(stream, format='PNG', save_all=True,
            append_images=[Image.new('RGB', (16, 16), 'blue')], duration=[10, 20])
        with self.assertRaisesRegex(ValueError, 'APNG'):
            importer.import_image(stream.getvalue(), still_duration_us=1)
        # acTL with one animation frame still identifies APNG, even though
        # Pillow's is_animated property is false for a single-frame animation.
        one_frame_apng = png(16, 16, bytes(768), before=[
            (b'acTL', struct.pack('>II', 1, 0)),
            (b'fcTL', struct.pack('>IIIIIHHBB', 0, 16, 16, 0, 0, 1, 100, 0, 0))])
        with self.assertRaisesRegex(ValueError, 'APNG'):
            importer.import_image(one_frame_apng, still_duration_us=1)
        invalid_apng = png(16, 16, bytes(768), before=[(b'acTL', struct.pack('>II', 0, 0))])
        with self.assertRaisesRegex(ValueError, 'APNG'):
            importer.import_image(invalid_apng, still_duration_us=1)

    def test_malformed_and_corrupt_sources_preserve_existing_output(self):
        source = png(16, 16, bytes(768))
        corrupt = bytearray(source)
        corrupt[-20] ^= 1
        valid_gif = gif([dict(delay_cs=1)])
        broken_second = valid_gif[:-1] + b'!\xf9\x04\x04\x01\0\0\0,\0\0;'
        for data in (b'', b'not an image', source[:30], source[:-12], bytes(corrupt), valid_gif[:-1],
                     valid_gif[:40]+b';', broken_second):
            output = self.path / 'output.rgbb'
            output.write_bytes(b'keep existing output')
            options = () if data.startswith(b'GIF') else ('--still-duration-us', '1')
            result, _ = self.cli(data, *options, output=output)
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(result.stdout, '')
            self.assertEqual(output.read_bytes(), b'keep existing output')
            self.assertEqual(list(self.path.glob('.rgbb-*')), [])

    def test_gif_unsupported_extensions_controls_and_extra_data_rejected(self):
        original = gif([dict(delay_cs=1)])
        for bad in (original + b'extra', gif([dict(delay_cs=1, disposal=4)]),
                    gif([dict(delay_cs=1, rectangle=(16, 0, 1, 1), indices=[1])]),
                    original[:25] + b'!\x01\0' + original[25:]):
            with self.assertRaises(ValueError):
                importer.import_image(bad)
        # A user-input flag requests interactive timing, unsupported here.
        control = original.index(b'!\xf9') + 3
        altered = bytearray(original)
        altered[control] |= 2
        with self.assertRaisesRegex(ValueError, 'graphic control'):
            importer.import_image(bytes(altered))

    def test_work_and_encoded_limits_fail_without_output(self):
        source = gif([dict(delay_cs=1), dict(delay_cs=1)])
        with patch.object(importer.compiler, 'MAX_DECODED_PIXELS', 256):
            with self.assertRaisesRegex(ValueError, 'decoded-pixel'):
                importer.import_image(source)
        with patch.object(importer.compiler, 'MAX_ASSET_BYTES', 40):
            with self.assertRaisesRegex(ValueError, 'encoded-size'):
                importer.import_image(source)
        path = self.path / 'oversize.image'
        with path.open('wb') as stream:
            stream.seek(importer.MAX_INPUT_BYTES)
            stream.write(b'\0')
        with self.assertRaisesRegex(ValueError, '16 MiB'):
            importer.read_source(path)

    def test_atomic_write_failure_keeps_existing_file_and_cleans_temporary(self):
        path = self.path / 'asset.rgbb'
        path.write_bytes(b'old')
        with patch.object(importer.os, 'replace', side_effect=OSError('injected replace failure')):
            with self.assertRaisesRegex(OSError, 'injected'):
                importer.atomic_write(path, b'new')
        self.assertEqual(path.read_bytes(), b'old')
        self.assertEqual(list(self.path.glob('.rgbb-*')), [])
        importer.atomic_write(path, b'new')
        self.assertEqual(path.read_bytes(), b'new')

    def test_cli_summary_determinism_options_and_aliases(self):
        source = png(16, 16, bytes([91, 92, 93])*256)
        result, output = self.cli(source, '--version', '2', '--still-duration-us', '16667', '--background', '010203')
        self.assertEqual(result.returncode, 0, result.stderr)
        summary = json.loads(result.stdout)
        self.assertEqual(summary['version'], 2)
        self.assertEqual(summary['frame_count'], 1)
        self.assertEqual(summary['background_rgb'], [1, 2, 3])
        self.assertFalse(summary['alpha_composited'])
        self.assertEqual(summary['asset_sha256'], hashlib.sha256(output.read_bytes()).hexdigest())
        again, _ = self.cli(source, '--version', '2', '--still-duration-us', '16667', '--background', '010203')
        self.assertEqual(result.stdout, again.stdout)
        path = self.path / 'source with spaces ☃.image'
        for alias_type in ('same', 'symlink', 'hardlink'):
            alias = self.path / alias_type
            if alias_type == 'symlink':
                alias.symlink_to(path)
            elif alias_type == 'hardlink':
                os.link(path, alias)
            else:
                alias = path
            rejected, _ = self.cli(source, '--still-duration-us', '1', output=alias)
            self.assertNotEqual(rejected.returncode, 0)
            self.assertEqual(path.read_bytes(), source)
            self.assertIn('aliases', rejected.stderr)
        for value in ('#000000', 'abc', 'zzzzzz'):
            result, _ = self.cli(source, '--background', value, '--still-duration-us', '1')
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(result.stdout, '')

    def test_missing_dependency_has_actionable_error_and_help_still_works(self):
        source = self.path / 'source.png'
        source.write_bytes(png(16, 16, bytes(768)))
        result = subprocess.run([sys.executable, '-S', str(SCRIPT), str(source), str(self.path / 'out'),
                                 '--still-duration-us', '1'], capture_output=True, text=True, timeout=30)
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, '')
        self.assertIn('image-import-requirements.txt', result.stderr)
        result = subprocess.run([sys.executable, '-S', str(SCRIPT), '--help'], capture_output=True, text=True, timeout=30)
        self.assertEqual(result.returncode, 0)
        self.assertIn('--background', result.stdout)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--decoder', required=True, type=Path)
    args, remaining = parser.parse_known_args()
    DECODER = args.decoder.resolve()
    unittest.main(argv=[__file__, *remaining])
