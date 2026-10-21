#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Encode synthetic five-minute sets; report actual sizes, not target performance."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import struct
import sys

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('compiler', ROOT / 'tools/compile-assets.py')
compiler = importlib.util.module_from_spec(spec)
spec.loader.exec_module(compiler)


def source_frames(profile, clip):
    for frame in range(750):
        duration = (16667, 16667, 16666)[frame % 3]
        if profile == 'solid_colour_frames':
            rgb = bytes(((clip*11+frame) % 256, (clip*7+frame*3) % 256,
                         (clip*17+frame*5) % 256)) * 768
        elif profile == 'moving_two_colour_bar':
            phase = (clip*7+frame) % 48
            color = bytes((255, (clip*11) % 256, (clip*23) % 256))
            row = b''.join(color if (x-phase) % 48 < 6 else b'\0\0\0' for x in range(48))
            rgb = row * 16
        elif profile == 'high_colour_no_runs':
            rgb = b''.join(bytes((i % 256, i // 256, (clip*13+frame) % 256)) for i in range(768))
        else:
            raise ValueError('unknown synthetic profile')
        yield duration, rgb


def screen():
    cases = {}
    for profile in ('solid_colour_frames', 'moving_two_colour_bar', 'high_colour_no_runs'):
        clips = []
        for clip in range(24):
            encoded = compiler.encode_asset(48, 16, source_frames(profile, clip))
            count = struct.unpack_from('<I', encoded, 12)[0]
            duration = struct.unpack_from('<Q', encoded, 16)[0]
            assert count == 750 and duration == 12_500_000
            clips.append(dict(clip=clip, encoded_bytes=len(encoded), frames=count,
                              duration_us=duration, sha256=hashlib.sha256(encoded).hexdigest()))
        total = sum(c['encoded_bytes'] for c in clips)
        cases[profile] = dict(assets=clips, total_encoded_bytes=total,
                              total_duration_us=sum(c['duration_us'] for c in clips),
                              total_frames=sum(c['frames'] for c in clips),
                              within_planning_8_MiB=total <= 8*1024*1024,
                              within_planning_10_MiB=total <= 10*1024*1024)
        print(f'{profile}: {total} bytes for 24 synthetic clips / 300 seconds', file=sys.stderr, flush=True)
    return {'SPDX-License-Identifier':'Apache-2.0', 'status':'SYNTHETIC_HOST_ENCODING_SCREEN',
            'format':'RGBB1', 'dimensions':[48,16], 'source_content_rate_fps':60,
            'cases':cases,
            'source_sha256':{name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest()
                             for name in ('tools/screen-asset-capacity.py','tools/compile-assets.py')},
            'limits':['Synthetic patterns are not representative user content or STO-001 acceptance.',
                      '8/10 MiB are planning budgets, not allocated flash partitions.',
                      'No target throughput, display operation or physical storage measurement.']}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report', type=Path, required=True)
    args = parser.parse_args()
    result = screen()
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(result, indent=2, sort_keys=True)+'\n')


if __name__ == '__main__':
    main()
