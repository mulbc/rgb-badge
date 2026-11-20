#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Compiler -> native session -> normalized colour, with mode/timing traces."""
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
SESSION = None
AWAIT, READY, PLAYING, INHIBITED, COMPLETE, PROGRAMMING, FAULT = range(7)


def converted(rgb, brightness):
    # Independent integer oracle for the trace adapter's synthetic quadratic
    # gamma and asymmetric white balance. This is not optical calibration.
    denominator = 65535**2
    balance = (65535, 32768, 16384)
    return [[(((value * value * 65535 + 32512) // 65025) * balance[channel] * brightness
              + denominator // 2) // denominator
             for channel, value in enumerate(rgb[pixel:pixel + 3])]
            for pixel in range(0, len(rgb), 3)]


class SessionTests(unittest.TestCase):
    def trace(self, width, frames, steps, *, version=1, brightness=32768, budget=0, corrupt_frame=None):
        encoded = compiler.encode_asset(width, 16, frames, version=version)
        if corrupt_frame is not None:
            encoded = bytearray(encoded)
            offset = 32
            for _ in range(corrupt_frame):
                offset += 16 + struct.unpack_from("<I", encoded, offset + 8)[0]
            encoded[offset + 12] ^= 1
            struct.pack_into("<I", encoded, 28, zlib.crc32(encoded[32:]))
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "session.rgbb"
            path.write_bytes(encoded)
            result = subprocess.run([str(SESSION), str(path), str(brightness), str(budget)],
                                    input="\n".join(f"{time} {int(pressed)} {command}" for time, pressed, command in steps),
                                    text=True, capture_output=True, check=True)
        return [json.loads(line) for line in result.stdout.splitlines()]

    def assert_black(self, event, width):
        self.assertEqual(event["rgb16"], [[0, 0, 0]] * (width * 16))
        self.assertTrue(event["display_inhibit"])
        self.assertFalse(event["frame_ready"])

    def test_exact_pipeline_both_versions_dimensions_and_brightness(self):
        rng = random.Random(39)
        for width in (16, 48):
            frames = [(40 + index * 10, rng.randbytes(width * 16 * 3)) for index in range(3)]
            for version in (1, 2):
                for brightness in (0, 16384, 65535):
                    with self.subTest(width=width, version=version, brightness=brightness):
                        steps = [(0, False, "start"), (10, False, "none"), (100, False, "start")]
                        boundary = 100
                        for duration, _ in frames:
                            steps.extend([(boundary + duration - 1, False, "none"),
                                          (boundary + duration, False, "none")])
                            boundary += duration
                        trace = self.trace(width, frames, steps, version=version, brightness=brightness)
                        self.assertEqual([e["state"] for e in trace[:2]], [AWAIT, READY])
                        for event in trace[:2] + trace[-1:]:
                            self.assert_black(event, width)
                        self.assertEqual(trace[-1]["state"], COMPLETE)
                        admitted = [e for e in trace if e["frame_ready"]]
                        self.assertEqual(len(admitted), len(frames))
                        boundary = 100
                        for index, (event, (duration, rgb)) in enumerate(zip(admitted, frames)):
                            self.assertEqual(event["rgb16"], converted(rgb, brightness))
                            self.assertEqual(event["frame_index"], index)
                            self.assertEqual(event["duration_us"], duration)
                            self.assertEqual(event["scheduled_start_us"], boundary)
                            self.assertEqual(event["scheduled_end_us"], boundary + duration)
                            boundary += duration
                        for event in trace:
                            self.assertEqual(event["brightness"], brightness)
                            self.assertFalse(event["ble_requested"])
                        for i in (3, 5, 7):
                            self.assertEqual(trace[i]["rgb16"], trace[i - 1]["rgb16"])
                            self.assertFalse(trace[i]["frame_ready"])

    def test_v2_delta_keys_and_converted_frames(self):
        frames = [(100, bytes(channel for pixel in range(768)
                              for channel in (pixel & 255, pixel >> 8, index)))
                  for index in range(125)]
        steps = [(0, False, "none"), (10, False, "none"), (100, False, "start")]
        steps.extend((100 + index * 100, False, "none") for index in range(1, 126))
        trace = self.trace(48, frames, steps, version=2, brightness=22222)
        for index, event in enumerate(trace[2:-1]):
            self.assertTrue(event["frame_ready"])
            self.assertEqual(event["frame_index"], index)
            self.assertEqual(event["rgb16"], converted(frames[index][1], 22222))
        self.assertEqual(trace[-1]["state"], COMPLETE)
        self.assert_black(trace[-1], 48)

    def test_interrupt_release_requires_explicit_resume_then_programming(self):
        frames = [(1000, bytes([51, 102, 153]) * 256)]
        steps = [(0, False, "none"), (10, False, "none"), (20, False, "start"),
                 (21, True, "start"), (22, False, "none"), (32, False, "none"),
                 (100, False, "none"), (101, False, "start"), (102, True, "none"),
                 (112, True, "none"), (142, True, "start"), (200, False, "stop"),
                 (0, False, "reset"), (10, False, "none"), (20, False, "start")]
        trace = self.trace(16, frames, steps, version=2)
        self.assertEqual([e["state"] for e in trace],
                         [AWAIT, READY, PLAYING, INHIBITED, INHIBITED, READY, READY, PLAYING,
                          INHIBITED, INHIBITED, PROGRAMMING, PROGRAMMING, AWAIT, READY, PLAYING])
        for index, event in enumerate(trace):
            if event["state"] != PLAYING:
                self.assert_black(event, 16)
            self.assertEqual(bool(event["ble_requested"]), event["state"] == PROGRAMMING)
            if index in (0, 3, 10, 11):
                self.assertFalse(event["command_accepted"])
        self.assertEqual(trace[10]["mode_event"], 2)
        self.assertEqual(trace[11]["mode_event"], 0)
        for index in (2, 7, 14):
            self.assertTrue(trace[index]["frame_ready"])
            self.assertEqual(trace[index]["frame_index"], 0)
            self.assertEqual(trace[index]["rgb16"], converted(frames[0][1], 32768))

    def test_deadline_fault_commands_cannot_clear(self):
        frames = [(10, bytes([1, 2, 3]) * 256), (20, bytes([4, 5, 6]) * 256)]
        steps = [(0, False, "none"), (10, False, "none"), (20, False, "start"),
                 (31, False, "start"), (32, False, "stop"), (33, True, "start"),
                 (100, True, "none"), (0, False, "reset"), (10, False, "none"), (20, False, "start")]
        trace = self.trace(16, frames, steps)
        for event in trace[3:7]:
            self.assertEqual(event["state"], FAULT)
            self.assertEqual(event["fault"], 2)
            self.assertEqual(event["playback_error"], 2)
            self.assertFalse(event["ble_requested"])
            self.assertFalse(event["command_accepted"])
            self.assert_black(event, 16)
        self.assertEqual(trace[-1]["state"], PLAYING)
        self.assertTrue(trace[-1]["frame_ready"])

    def test_decoded_corruption_clears_whole_output(self):
        frames = [(100, bytes([index + 1, 22, 33]) * 768) for index in range(3)]
        steps = [(0, False, "none"), (10, False, "none"), (20, False, "start"),
                 (120, False, "none"), (220, False, "none"), (320, False, "start")]
        for version in (1, 2):
            for bad in range(3):
                with self.subTest(version=version, bad=bad):
                    trace = self.trace(48, frames, steps, version=version, corrupt_frame=bad)
                    for event in trace[2 + bad:]:
                        self.assertEqual(event["state"], FAULT)
                        self.assertEqual(event["fault"], 2)
                        self.assertEqual(event["playback_error"], 4)
                        self.assertNotEqual(event["asset_error"], 0)
                        self.assert_black(event, 48)

    def test_clock_fault_revokes_programming_and_latches(self):
        frames = [(100, bytes([1]) * 768)]
        steps = [(0, False, "none"), (10, False, "none"), (20, True, "none"),
                 (30, True, "none"), (60, True, "none"), (59, True, "stop"), (100, False, "start")]
        trace = self.trace(16, frames, steps)
        self.assertTrue(trace[4]["ble_requested"])
        self.assertEqual(trace[4]["state"], PROGRAMMING)
        for event in trace[5:]:
            self.assertEqual(event["state"], FAULT)
            self.assertEqual(event["fault"], 1)
            self.assertFalse(event["ble_requested"])
            self.assert_black(event, 16)
        self.assertEqual(trace[5]["mode_event"], 3)
        self.assertEqual(trace[6]["mode_event"], 0)

    def test_lateness_and_expired_interval_policy(self):
        frames = [(10, bytes([1]) * 768), (20, bytes([2]) * 768)]
        base = [(0, False, "none"), (10, False, "none"), (20, False, "start")]
        trace = self.trace(16, frames, base + [(32, False, "none"), (50, False, "none")], budget=2)
        self.assertEqual(trace[3]["state"], PLAYING)
        self.assertEqual(trace[3]["lateness_us"], 2)
        self.assertEqual(trace[3]["scheduled_end_us"], 50)
        self.assertEqual(trace[4]["state"], COMPLETE)
        trace = self.trace(16, frames, base + [(50, False, "none")], budget=100)
        self.assertEqual(trace[-1]["state"], FAULT)
        self.assert_black(trace[-1], 16)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--session", required=True, type=Path)
    args, remaining = parser.parse_known_args()
    SESSION = args.session.resolve()
    unittest.main(argv=[__file__, *remaining])
