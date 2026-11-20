#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Report actual open pad groups and nearest pad pairs, without routing claims."""
import argparse
from collections import defaultdict
import hashlib
import itertools
import json
import math
from pathlib import Path
import pcbnew as p

ROOT = Path(__file__).resolve().parents[1]
DEFAULT = ROOT/'hardware/coupon/rev-a/staging/led-remaining-routing-trial-114mm.kicad_pcb'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def report(path):
    before = sha(path)
    board = p.LoadBoard(str(path))
    board.BuildConnectivity()
    partitions = defaultdict(lambda: defaultdict(list))
    for footprint in board.GetFootprints():
        for pad in footprint.Pads():
            if not pad.GetNetname():
                continue
            group = frozenset(item.m_Uuid.AsString()
                for item in board.GetConnectivity().GetConnectedItems(pad)
                if isinstance(item, p.PAD)) | {pad.m_Uuid.AsString()}
            partitions[pad.GetNetname()][group].append({
                'reference': footprint.GetReference(), 'pin': pad.GetNumber(),
                'uuid': pad.m_Uuid.AsString(),
                'position_iu': [pad.GetPosition().x, pad.GetPosition().y]})
    nets = []
    for net, groups in sorted(partitions.items()):
        if len(groups) < 2:
            continue
        rows = sorted((sorted(group, key=lambda row: (row['reference'], row['pin'], row['uuid']))
            for group in groups.values()), key=lambda group: (-len(group), repr(group)))
        pairs = []
        for i, j in itertools.combinations(range(len(rows)), 2):
            distance, a, b = min(((math.dist(a['position_iu'], b['position_iu']), a, b)
                for a in rows[i] for b in rows[j]),
                key=lambda item: (item[0], item[1]['uuid'], item[2]['uuid']))
            pairs.append({'groups': [i, j], 'pad_centre_distance_mm': distance/1e6,
                'pads': [[a['reference'], a['pin']], [b['reference'], b['pin']]]})
        pairs.sort(key=lambda row: (row['pad_centre_distance_mm'], row['groups']))
        nets.append({'net': net, 'open_edges': len(rows)-1,
            'groups': rows, 'nearest_pad_pairs': pairs})
    physical = sum(row['open_edges'] for row in nets)
    native = board.GetConnectivity().GetUnconnectedCount(False)
    assert physical == native, 'Native/pad-group counts disagree; inspect pad-free copper'
    assert sha(path) == before, 'Read-only report changed source'
    return {'SPDX-License-Identifier': 'CERN-OHL-S-2.0', 'source_sha256': before,
        'tool_sha256': sha(Path(__file__)), 'native_opens': native,
        'physical_opens': physical, 'all_named_pad_group_count': sum(map(len, partitions.values())),
        'named_net_count': len(partitions), 'nets': nets, 'source_unchanged': True,
        'interpretation': 'Actual native pad groups; distances are pad-centre geometry, not routes or electrical qualification',
        'fabrication_release_allowed': False}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--board', type=Path, default=DEFAULT)
    ap.add_argument('--output', type=Path)
    args = ap.parse_args()
    result = report(args.board.resolve())
    data = json.dumps(result, indent=2, sort_keys=True)+'\n'
    if args.output:
        assert args.output.suffix == ".json", "Report output must be JSON"
        assert args.output.resolve() != args.board.resolve()
        args.output.write_text(data)
        print(result['native_opens'], 'native/physical opens;', len(result['nets']), 'nets with opens')
    else:
        print(data, end='')


if __name__ == '__main__':
    main()
