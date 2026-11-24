#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Require both physical drain lands and every LED anode in each row cluster."""
import argparse
from collections import Counter
import hashlib
import importlib.util
import json
from pathlib import Path
import pcbnew as p

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('escape', ROOT / 'tools/check-ground-escape-trial.py')
escape = importlib.util.module_from_spec(spec)
spec.loader.exec_module(escape)


def cluster(board, pad):
    return frozenset((q.GetParentFootprint().GetReference(), q.GetNumber(),
                      q.GetPosition().x, q.GetPosition().y)
                     for q in board.GetConnectivity().GetConnectedItems(pad)
                     if isinstance(q, p.PAD))


def check_physical_rows(board):
    parts = {f.GetReference(): f for f in board.GetFootprints()}
    for row in range(16):
        ref = f'PAIR{row+1:02d}'
        drains = [q for q in parts[ref].Pads() if q.GetNumber() == '3']
        assert len(drains) == 2
        expected = {(ref, '3', q.GetPosition().x, q.GetPosition().y) for q in drains}
        for col in range(16):
            led = parts[f'D{16*row+col+1}']
            pad = next(q for q in led.Pads() if q.GetNumber() == '1')
            expected.add((led.GetReference(), '1', pad.GetPosition().x, pad.GetPosition().y))
        assert len(expected) == 18
        assert all(cluster(board, q) == expected for q in drains), ('Physical row drain not joined', row)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--drc', type=Path, required=True)
    parser.add_argument('--report', type=Path)
    parser.add_argument('--self-test', action='store_true', help='require rejection after removing one new tie in memory')
    args = parser.parse_args()
    source = escape.STAGING / 'led-vled-distribution-trial-114mm.kicad_pcb'
    output = escape.STAGING / 'led-row-drain-tie-trial-114mm.kicad_pcb'
    manifest = json.loads((ROOT / 'mechanical/review/row-drain-tie-trial.json').read_text())
    assert hashlib.sha256(source.read_bytes()).hexdigest() == manifest['source_sha256']
    assert hashlib.sha256(output.read_bytes()).hexdigest() == manifest['board_sha256']
    old, new = p.LoadBoard(str(source)), p.LoadBoard(str(output))
    before, after = ({f.GetReference(): f for f in b.GetFootprints()} for b in (old, new))
    assert before.keys() == after.keys() and len(after) == 483
    new_pads = {}
    for ref, part in before.items():
        other = after[ref]
        assert (part.GetValue(), part.GetFPIDAsString(), part.GetPosition(), part.GetOrientation().AsDegrees(), part.GetLayer()) == (
            other.GetValue(), other.GetFPIDAsString(), other.GetPosition(), other.GetOrientation().AsDegrees(), other.GetLayer()), ref
        assert Counter(map(escape.pad_signature, part.Pads())) == Counter(map(escape.pad_signature, other.Pads())), ref
        for q in other.Pads():
            new_pads[(ref, q.GetNumber(), q.GetPosition().x, q.GetPosition().y)] = q
    grid = escape.load_module('grid', 'generate-colour-fanout-grid-trial.py')
    originals = Counter(grid.signature(t) for t in old.GetTracks())
    added = []
    for t in new.GetTracks():
        signature = grid.signature(t)
        if originals[signature]:
            originals[signature] -= 1
        else:
            added.append(t)
    assert not +originals and len(added) == manifest['added_tracks'] == 16
    assert Counter(t.GetNetname() for t in added) == Counter({f'ROW_{row:02d}_A': 1 for row in range(16)})
    assert all(not isinstance(t, p.PCB_VIA) and t.GetLayer() == p.B_Cu and t.GetWidth() == p.FromMM(.2) for t in added)
    for ref, part in before.items():
        for pad in part.Pads():
            name = pad.GetNetname()
            if not name:
                continue
            other = new_pads[(ref, pad.GetNumber(), pad.GetPosition().x, pad.GetPosition().y)]
            a, b = cluster(old, pad), cluster(new, other)
            if name.startswith('ROW_') and name.endswith('_A'):
                assert a <= b
            else:
                assert a == b, ('Other cluster changed', ref, pad.GetNumber())
    check_physical_rows(new)
    colour = escape.load_module('colour', 'check-colour-fanout-trial.py')
    assert colour.findings(args.drc) == colour.findings(ROOT / 'docs/development/led-vled-distribution-drc-2026-10-20.json')
    assert len(colour.findings(args.drc)) == 104
    reporter = escape.load_module('connectivity', 'report-coupon-board-connectivity.py')
    opens = reporter.open_edges_by_net(output)
    assert opens['native_open_edges'] == opens['pad_cluster_open_edges'] == manifest['open_edges'] == 246
    assert not any(f'ROW_{row:02d}_A' in opens['by_net'] for row in range(16))
    assert opens['by_net']['GND'] == 27
    assert len(list(new.GetTracks())) == manifest['tracks_and_vias'] == 14195
    mutation_rejected = None
    if args.self_test:
        # A copied board only: never edit the checked source artifact. Ref/pin
        # sets alone would miss the lost exposed land, since both pads are "3".
        probe = p.LoadBoard(str(output))
        target = grid.signature(next(t for t in added if t.GetNetname() == 'ROW_00_A'))
        item = next(t for t in probe.GetTracks() if grid.signature(t) == target)
        probe.Remove(item)
        probe.BuildConnectivity()
        try:
            check_physical_rows(probe)
        except AssertionError:
            mutation_rejected = True
        assert mutation_rejected is True, 'Missing physical drain tie was not rejected'
    result = dict(board_sha256=manifest['board_sha256'], kicad_version=p.GetBuildVersion(),
                  unchanged_footprints=483, added_tracks=16, joined_rows=16,
                  physical_anode_pads_per_row=18, other_pad_clusters_unchanged=True,
                  source_tracks_and_vias_preserved=True, native_open_edges=246, ground_open_edges=27,
                  removed_drain_tie_mutation_rejected=mutation_rejected,
                  full_drc='104_UNCHANGED_INTRINSIC_FINDINGS',
                  drc_sha256=hashlib.sha256(args.drc.read_bytes()).hexdigest())
    result['SPDX-License-Identifier'] = 'CERN-OHL-S-2.0'
    if args.report:
        args.report.write_text(json.dumps(result, indent=2, sort_keys=True)+'\n')
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
