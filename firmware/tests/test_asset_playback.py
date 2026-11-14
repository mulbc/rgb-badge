#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Cross-language playback traces; source pixels/durations are the oracle."""
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
PLAYER = None
FRAME, WAITING, END, ERROR = 1, 2, 3, 4


class PlaybackTests(unittest.TestCase):
    def trace(self, width, frames, times, *, version=1, budget=0, start=0, corrupt_frame=None):
        encoded = compiler.encode_asset(width, 16, frames, version=version)
        if corrupt_frame is not None:
            encoded = bytearray(encoded)
            offset = 32
            for _ in range(corrupt_frame):
                offset += 16 + struct.unpack_from("<I", encoded, offset + 8)[0]
            encoded[offset + 12] ^= 1
            struct.pack_into("<I", encoded, 28, zlib.crc32(encoded[32:]))
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "test.rgbb"
            path.write_bytes(encoded)
            result = subprocess.run([str(PLAYER), str(path), str(budget), str(start)],
                                    input="\n".join(map(str, times)), text=True,
                                    capture_output=True, check=True)
        return [json.loads(line) for line in result.stdout.splitlines()]

    def test_both_versions_dimensions_and_variable_durations(self):
        rng = random.Random(37)
        for width in (16, 48):
            frames = [(rng.randrange(1, 100000), rng.randbytes(width * 16 * 3)) for _ in range(121)]
            for version in (1, 2):
                with self.subTest(width=width, version=version):
                    start, now, times = 123456789, 123456789, []
                    for duration, _ in frames:
                        times.extend([now, now + duration - 1, now + duration])
                        now += duration
                    trace = self.trace(width, frames, times, version=version, start=start)
                    self.assertEqual(len(trace), len(times) + 1)
                    emitted = [event for event in trace if event["status"] == FRAME]
                    self.assertEqual(len(emitted), len(frames))
                    boundary = start
                    for index, (event, (duration, rgb)) in enumerate(zip(emitted, frames)):
                        self.assertEqual(event["frame_index"], index)
                        self.assertEqual(event["duration_us"], duration)
                        self.assertEqual(event["scheduled_start_us"], boundary)
                        self.assertEqual(event["scheduled_end_us"], boundary + duration)
                        self.assertEqual(event["lateness_us"], 0)
                        self.assertEqual(bytes.fromhex(event["rgb888"]), rgb)
                        boundary += duration
                    self.assertEqual(trace[-1]["status"], END)
                    self.assertEqual(bytes.fromhex(trace[-1]["rgb888"]), bytes(width * 16 * 3))
                    self.assertFalse(any(e["status"] == ERROR for e in trace))

    def test_delta_chain_keyframes_and_waiting_pixels(self):
        frames = []
        for index in range(125):
            rgb = bytes(channel for pixel in range(768)
                        for channel in (pixel & 255, pixel >> 8, index))
            frames.append(((16667, 16667, 16666)[index % 3], rgb))
        now, times = 0, []
        for duration, _ in frames:
            times.extend([now + duration - 1, now + duration])
            now += duration
        trace = self.trace(48, frames, times, version=2)
        for index, (_, rgb) in enumerate(frames):
            ready, waiting = trace[2 * index:2 * index + 2]
            self.assertEqual(ready["status"], FRAME)
            self.assertEqual(waiting["status"], WAITING)
            self.assertEqual(ready["frame_index"], index)
            self.assertEqual(waiting["frame_index"], index)
            self.assertEqual(bytes.fromhex(ready["rgb888"]), rgb)
            self.assertEqual(waiting["rgb888"], ready["rgb888"])
        self.assertEqual(trace[-1]["status"], END)

    def test_explicit_lateness_without_drift(self):
        frames = [(10, bytes([index + 1]) * 768) for index in range(4)]
        trace = self.trace(16, frames, [12, 21, 30, 40], version=2, budget=2)
        self.assertEqual([e["status"] for e in trace], [FRAME] * 4 + [END])
        self.assertEqual([e["scheduled_end_us"] for e in trace[:-1]], [10, 20, 30, 40])
        self.assertEqual([e["lateness_us"] for e in trace], [0, 2, 1, 0, 0])
        self.assertEqual([e["duration_us"] for e in trace], [10] * 5)

    def test_deadline_fault_never_emits_catchup_frames(self):
        frames = [(10, bytes([index + 1]) * 768) for index in range(4)]
        for version in (1, 2):
            for budget, timestamp in ((0, 11), (1, 12), (1000, 20)):
                with self.subTest(version=version, budget=budget):
                    trace = self.trace(16, frames, [timestamp, timestamp, 40], version=version, budget=budget)
                    self.assertEqual([e["status"] for e in trace], [FRAME, ERROR, ERROR, ERROR])
                    for event in trace[1:]:
                        self.assertEqual(event["error"], 2)
                        self.assertEqual(bytes.fromhex(event["rgb888"]), bytes(768))
                    self.assertEqual(trace[1], trace[2])

    def test_decoded_crc_failure_clears_output_and_latches(self):
        frames = [(100, bytes([index + 1]) * 2304) for index in range(3)]
        for version in (1, 2):
            for bad in (0, 1, 2):
                with self.subTest(version=version, bad=bad):
                    trace = self.trace(48, frames, [100, 200, 300], version=version, corrupt_frame=bad)
                    self.assertEqual([e["status"] for e in trace[:bad]], [FRAME] * bad)
                    for event in trace[bad:]:
                        self.assertEqual(event["status"], ERROR)
                        self.assertEqual(event["error"], 4)
                        self.assertNotEqual(event["asset_error"], 0)
                        self.assertEqual(bytes.fromhex(event["rgb888"]), bytes(2304))

    def test_backward_clock_and_overflow(self):
        frames = [(100, bytes([1]) * 768)]
        trace = self.trace(16, frames, [99], start=100)
        self.assertEqual(trace[-1]["error"], 1)
        self.assertEqual(bytes.fromhex(trace[-1]["rgb888"]), bytes(768))
        maximum = 2**64 - 1
        trace = self.trace(16, frames, [maximum], start=maximum - 100)
        self.assertEqual(trace[-1]["status"], END)
        trace = self.trace(16, frames, [maximum], start=maximum - 99)
        self.assertTrue(all(event["status"] == ERROR and event["error"] == 3 for event in trace))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--player", required=True, type=Path)
    args, remaining = parser.parse_known_args()
    PLAYER = args.player.resolve()
    unittest.main(argv=[__file__, *remaining])
