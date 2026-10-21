#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Compare Python asset output with the native C++ reader, byte for byte."""
import argparse
import importlib.util
import json
from pathlib import Path
import random
import struct
import subprocess
import tempfile
import unittest
from unittest.mock import patch
import zlib

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('compiler', ROOT / 'tools/compile-assets.py')
compiler = importlib.util.module_from_spec(spec)
spec.loader.exec_module(compiler)
DECODER = None


def frame_headers(encoded):
    result, position = [], 32
    while position < len(encoded):
        duration, codec, reserved, palette, length, crc = struct.unpack_from('<IBBHII', encoded, position)
        result.append((duration, codec, palette, encoded[position+16:position+16+length], crc))
        position += 16 + length
    return result


class AssetPipeline(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory(prefix='rgb-asset-test-')
        self.addCleanup(self.directory.cleanup)
        self.path = Path(self.directory.name)

    def native(self, encoded):
        source = self.path / 'input.rgbb'
        source.write_bytes(encoded)
        return subprocess.run([str(DECODER), str(source)], capture_output=True)

    def check_frames(self, width, frames, codecs=None):
        encoded = compiler.encode_asset(width, 16, frames)
        self.assertEqual(encoded, compiler.encode_asset(width, 16, frames), 'deterministic bytes')
        self.assertEqual(zlib.crc32(encoded[32:]), struct.unpack_from('<I', encoded, 28)[0])
        if codecs is not None:
            self.assertEqual([f[1] for f in frame_headers(encoded)], codecs)
        result = self.native(encoded)
        self.assertEqual(result.returncode, 0, result.stderr.decode(errors='replace'))
        self.assertEqual(result.stdout, b''.join(rgb for duration, rgb in frames))
        info = json.loads(result.stderr)
        self.assertEqual(info, {'width': width, 'height': 16,
                               'duration_us': sum(d for d, _ in frames),
                               'durations_us': [d for d, _ in frames]})
        return encoded

    def test_three_codecs(self):
        self.check_frames(16, [(16667, b'\x12\x34\x56' * 256)], [1])
        self.check_frames(48, [(16667, b'\x12\x34\x56' * 768)], [2])
        self.check_frames(16, [(16667, bytes(range(256)) * 3)], [0])

    def test_palette_first_occurrence(self):
        rgb = b'\x80\x20\x10\x01\x02\x03' * 128
        encoded = self.check_frames(16, [(1, rgb)], [2])
        payload = frame_headers(encoded)[0][3]
        self.assertEqual(payload[:6], rgb[:6])

    def test_more_than_256_colours_remains_exact(self):
        rgb = b''.join(bytes((i%256, i//256, (i*17)%256)) for i in range(768))
        self.assertEqual(len({rgb[i:i+3] for i in range(0, len(rgb), 3)}), 768)
        self.check_frames(48, [(16666, rgb)], [0])

    def test_run_boundaries(self):
        encoded = self.check_frames(16, [(2, b'\x01\x02\x03'*255 + b'\x04\x05\x06')], [1])
        self.assertEqual(frame_headers(encoded)[0][3], bytes([254,1,2,3,0,4,5,6]))
        encoded = self.check_frames(48, [(2, b'\x01\x02\x03'*768)], [2])
        self.assertEqual(frame_headers(encoded)[0][3][3:], bytes([255,0])*3)

    def test_ties_choose_lower_codec(self):
        rgb = b''.join(bytes((i,0,0)) for i in range(191)) + bytes([191,0,0])*65
        self.check_frames(16, [(1, rgb)], [0])  # 192 RGB runs tie raw at 768 bytes.
        rgb = b'\x01\x02\x03'*85 + b'\x04\x05\x06'*85 + b'\x01\x02\x03'*86
        self.check_frames(16, [(1, rgb)], [1])  # RGB and palette runs tie at 12 bytes.

    def test_multiple_frames_and_64bit_duration(self):
        self.check_frames(16, [(0xffffffff, bytes([1,2,3])*256),
                               (0xffffffff, bytes([4,5,6])*256),
                               (16666, bytes(range(256))*3),
                               (16667, bytes([7,8,9])*256)])

    def test_seeded_cross_language_frames(self):
        rng = random.Random(20261021)
        for width in (16, 48):
            for colors in (1, 2, 8, 64, 256, 300):
                with self.subTest(width=width, colors=colors):
                    palette = [bytes(rng.randrange(256) for _ in range(3)) for _ in range(colors)]
                    frames = []
                    for _ in range(3):
                        rgb = b''.join(palette[rng.randrange(colors)] for _ in range(width*16))
                        frames.append((rng.randrange(1, 100000), rgb))
                    self.check_frames(width, frames)

    def test_corruption_and_decoded_crc(self):
        original = compiler.encode_asset(16, 16, [(1, b'\x01\x02\x03'*256)])
        damaged = bytearray(original); damaged[-1] ^= 1
        self.assertNotEqual(self.native(damaged).returncode, 0)
        damaged = bytearray(original); damaged[44] ^= 1
        struct.pack_into('<I', damaged, 28, zlib.crc32(damaged[32:]))
        result = self.native(damaged)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(result.stdout, b'', 'failed frame must not be emitted by adapter')

    def test_invalid_source(self):
        pixels = b'\0\0\0'*256
        for width, height, frames in [(17,16,[(1,pixels)]), (16,15,[(1,pixels)]),
                                      (True,16,[(1,pixels)]), (16,16,[]),
                                      (16,16,[(0,pixels)]), (16,16,[(True,pixels)]),
                                      (16,16,[(0x100000000,pixels)]), (16,16,[(1,pixels[:-1])])]:
            with self.subTest(width=width, height=height, frames=len(frames)):
                with self.assertRaises(ValueError): compiler.encode_asset(width, height, frames)

    def test_resource_bounds(self):
        pixels = b'\0\0\0'*256
        with patch.object(compiler, 'MAX_DECODED_PIXELS', 255):
            with self.assertRaises(ValueError): compiler.encode_asset(16, 16, [(1,pixels)])
        with patch.object(compiler, 'MAX_ASSET_BYTES', 51):
            with self.assertRaises(ValueError): compiler.encode_asset(16, 16, [(1,pixels)])

    def test_manifest_and_cli(self):
        document = {'version':1,'width':16,'height':16,
                    'frames':[{'duration_us':16667,'rgb888':(b'\x01\x02\x03'*256).hex()}]}
        expected = compiler.from_manifest(document)
        source, output = self.path/'source.json', self.path/'output.rgbb'
        source.write_text(json.dumps(document))
        command = ['python3', str(ROOT/'tools/compile-assets.py'), str(source), str(output)]
        result = subprocess.run(command, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(output.read_bytes(), expected)
        self.assertEqual(json.loads(result.stdout)['encoded_bytes'], len(expected))
        output.write_bytes(b'preserve')
        source.write_text('{}')
        self.assertNotEqual(subprocess.run(command, capture_output=True).returncode, 0)
        self.assertEqual(output.read_bytes(), b'preserve')
        source.write_text(json.dumps(document))
        result = subprocess.run(command[:-1]+[str(source)], capture_output=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(json.loads(source.read_text()), document)

    def test_manifest_rejects_typos_and_wrong_types(self):
        base = {'version':1,'width':16,'height':16,'frames':[{'duration_us':1,'rgb888':'00'*768}]}
        for document in [{}, dict(base, version=True), dict(base, typo=1), dict(base, frames={}),
                         dict(base, frames=[{'duration_ms':1,'rgb888':'00'*768}]),
                         dict(base, frames=[{'duration_us':1,'rgb888':[] }]),
                         dict(base, frames=[{'duration_us':1,'rgb888':'zz'}])]:
            with self.subTest(document=str(document)[:80]):
                with self.assertRaises(ValueError): compiler.from_manifest(document)

    def test_duplicate_json_fields_rejected(self):
        for source in ['{"version":1,"version":1}', '{"frames":[{"duration_us":1,"duration_us":2}]}']:
            with self.subTest(source=source):
                with self.assertRaises(ValueError):
                    json.loads(source, object_pairs_hook=compiler.unique_object)
        source = self.path/'duplicates.json'
        output = self.path/'preserved.rgbb'
        document = '{"version":1,"version":1,"width":16,"height":16,"frames":['
        document += '{"duration_us":1,"rgb888":"' + '00'*768 + '"}]}'
        source.write_text(document); output.write_bytes(b'preserve')
        result = subprocess.run(['python3', str(ROOT/'tools/compile-assets.py'), str(source), str(output)],
                                capture_output=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn(b'duplicate JSON field', result.stderr)
        self.assertEqual(output.read_bytes(), b'preserve')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--decoder', type=Path, required=True)
    args = parser.parse_args()
    DECODER = args.decoder.resolve()
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(AssetPipeline)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    raise SystemExit(0 if result.wasSuccessful() else 1)
