#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Public inspection CLI must validate every decoded frame before success."""
import argparse
import importlib.util
import json
from pathlib import Path
import random
import struct
import subprocess
import tempfile
import unittest
import zlib

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("compile_assets", ROOT / "tools/compile-assets.py")
compiler = importlib.util.module_from_spec(spec)
spec.loader.exec_module(compiler)
INSPECTOR = None


class InspectionTests(unittest.TestCase):
    def inspect(self, encoded):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "clip with spaces ☃.rgbb"
            path.write_bytes(encoded)
            return subprocess.run([str(INSPECTOR), str(path)], text=True,
                                  capture_output=True, timeout=30)

    def test_exact_summary_versions_dimensions_and_encodings(self):
        rng = random.Random(40)
        for width in (16, 48):
            for version in (1, 2):
                with self.subTest(width=width, version=version):
                    frames = [(1, bytes([17, 34, 51]) * (width * 16)),
                              (16667, bytes(channel for i in range(width * 16)
                                            for channel in ((0, 255)[i % 2], 0, 0))),
                              (2**32 - 1, rng.randbytes(width * 16 * 3))]
                    encoded = compiler.encode_asset(width, 16, frames, version=version)
                    result = self.inspect(encoded)
                    self.assertEqual(result.returncode, 0, result.stderr)
                    self.assertEqual(result.stderr, "")
                    self.assertEqual(json.loads(result.stdout), {
                        "format": "RGBB", "version": version, "width": width, "height": 16,
                        "frame_count": 3, "duration_us": sum(d for d, _ in frames),
                        "encoded_bytes": len(encoded), "decoded_rgb888_bytes": width * 16 * 3 * 3,
                        "all_frame_checksums_valid": True})

    def test_v2_multiple_keyframes_and_all_decoded_checksums(self):
        frames = [(16667 if i % 3 != 2 else 16666,
                   bytes(channel for pixel in range(768)
                         for channel in (pixel & 255, pixel >> 8, i))) for i in range(125)]
        encoded = compiler.encode_asset(48, 16, frames, version=2)
        result = self.inspect(encoded)
        self.assertEqual(result.returncode, 0, result.stderr)
        summary = json.loads(result.stdout)
        self.assertEqual(summary["frame_count"], 125)
        self.assertEqual(summary["duration_us"], sum(d for d, _ in frames))
        self.assertTrue(summary["all_frame_checksums_valid"])

    def test_bad_decoded_crc_anywhere_has_no_success_output(self):
        frames = [(10, bytes([i + 1, 11, 22]) * 256) for i in range(64)]
        for version in (1, 2):
            for bad in (0, 1, 62, 63):
                with self.subTest(version=version, bad=bad):
                    encoded = bytearray(compiler.encode_asset(16, 16, frames, version=version))
                    offset = 32
                    for _ in range(bad):
                        offset += 16 + struct.unpack_from("<I", encoded, offset + 8)[0]
                    encoded[offset + 12] ^= 1
                    struct.pack_into("<I", encoded, 28, zlib.crc32(encoded[32:]))
                    result = self.inspect(encoded)
                    self.assertEqual(result.returncode, 1)
                    self.assertEqual(result.stdout, "")
                    self.assertIn(f"Invalid frame {bad}: bad_frame_checksum", result.stderr)

    def test_bad_container_never_emits_success(self):
        encoded = compiler.encode_asset(16, 16, [(10, bytes([1]) * 768)])
        body_corrupt = bytearray(encoded)
        body_corrupt[-1] ^= 1
        unsupported = bytearray(encoded)
        struct.pack_into("<H", unsupported, 4, 3)
        for invalid, message in ((body_corrupt, "bad_body_checksum"),
                                 (unsupported, "unsupported_version"),
                                 (encoded[:-1], "Invalid asset"), (b"", "Invalid asset"),
                                 (encoded + b"extra", "Invalid asset")):
            with self.subTest(message=message):
                result = self.inspect(invalid)
                self.assertEqual(result.returncode, 1)
                self.assertEqual(result.stdout, "")
                self.assertIn(message, result.stderr)

    def test_encoded_size_rejected_before_reading_payload(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "oversize.rgbb"
            with path.open("wb") as stream:
                stream.seek(16 * 1024 * 1024)
                stream.write(b"\0")
            result = subprocess.run([str(INSPECTOR), str(path)], text=True,
                                    capture_output=True, timeout=30)
        self.assertEqual(result.returncode, 1)
        self.assertEqual(result.stdout, "")
        self.assertIn("16 MiB", result.stderr)

    def test_missing_file_help_and_argument_errors(self):
        with tempfile.TemporaryDirectory() as directory:
            result = subprocess.run([str(INSPECTOR), str(Path(directory) / "absent.rgbb")],
                                    text=True, capture_output=True, timeout=30)
        self.assertEqual(result.returncode, 1)
        self.assertEqual(result.stdout, "")
        self.assertIn("Cannot read input file", result.stderr)
        result = subprocess.run([str(INSPECTOR), "--help"], text=True, capture_output=True, timeout=30)
        self.assertEqual(result.returncode, 0)
        self.assertIn("usage:", result.stdout)
        for arguments in ([], ["one", "two"]):
            result = subprocess.run([str(INSPECTOR), *arguments], text=True, capture_output=True, timeout=30)
            self.assertEqual(result.returncode, 2)
            self.assertEqual(result.stdout, "")
            self.assertIn("usage:", result.stderr)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--inspector", required=True, type=Path)
    args, remaining = parser.parse_known_args()
    INSPECTOR = args.inspector.resolve()
    unittest.main(argv=[__file__, *remaining])
