#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Check the row-14 pullup relocation, both joins and native DRC equivalence."""
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


def pad_id(pad):
    return (pad.GetParentFootprint().GetReference(), pad.GetNumber(),
            pad.GetPosition().x, pad.GetPosition().y)


def cluster_ids(board, pad):
    return {(q.GetParentFootprint().GetReference(), q.GetNumber())
            for q in board.GetConnectivity().GetConnectedItems(pad) if isinstance(q, p.PAD)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--drc', type=Path, required=True)
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    source = escape.STAGING / 'led-ground-return-trial-114mm.kicad_pcb'
    output = escape.STAGING / 'led-row14-bias-trial-114mm.kicad_pcb'
    manifest = json.loads((ROOT / 'mechanical/review/row14-bias-trial.json').read_text())
    assert hashlib.sha256(source.read_bytes()).hexdigest() == manifest['source_sha256']
    assert hashlib.sha256(output.read_bytes()).hexdigest() == manifest['board_sha256']
    old, new = p.LoadBoard(str(source)), p.LoadBoard(str(output))
    old_parts = {f.GetReference(): f for f in old.GetFootprints()}
    new_parts = {f.GetReference(): f for f in new.GetFootprints()}
    assert old_parts.keys() == new_parts.keys() and len(new_parts) == 483
    for ref, part in old_parts.items():
        other = new_parts[ref]
        assert (part.GetValue(), part.GetFPIDAsString(), part.GetLayer()) == (
            other.GetValue(), other.GetFPIDAsString(), other.GetLayer()), ref
        if ref == 'R20':
            assert [p.ToMM(other.GetPosition().x), p.ToMM(other.GetPosition().y)] == [73.5, 30]
            assert other.GetOrientation().AsDegrees() == 90
            # Check the actual rotated pad geometry against an independently
            # transformed input footprint, rather than ignoring all its pads.
            part.SetOrientationDegrees(90)
            part.SetPosition(p.VECTOR2I(p.FromMM(73.5), p.FromMM(30)))
        else:
            assert (part.GetPosition(), part.GetOrientation().AsDegrees()) == (
                other.GetPosition(), other.GetOrientation().AsDegrees()), ref
        assert Counter(map(escape.pad_signature, part.Pads())) == Counter(map(escape.pad_signature, other.Pads())), ref
    grid = escape.load_module('grid', 'generate-colour-fanout-grid-trial.py')
    originals = Counter(grid.signature(item) for item in old.GetTracks())
    added = []
    for item in new.GetTracks():
        signature = grid.signature(item)
        if originals[signature]:
            originals[signature] -= 1
        else:
            added.append(item)
    assert not +originals and len(added) == 2
    assert Counter(t.GetNetname() for t in added) == Counter({'VLED': 1, 'ROW_GATE_14': 1})
    assert all(not isinstance(t, p.PCB_VIA) and t.GetLayer() == p.B_Cu and t.GetWidth() == p.FromMM(.2) for t in added)
    # Reload the input after the temporary geometry transform above.
    old = p.LoadBoard(str(source))
    old_parts = {f.GetReference(): f for f in old.GetFootprints()}
    # Includes ground: a refilled zone must not split any existing pad cluster.
    for ref, part in old_parts.items():
        for pad in part.Pads():
            if not pad.GetNetname() or pad.GetNetname() in ('ROW_GATE_14', 'VLED'):
                continue
            other = next(q for q in new_parts[ref].Pads() if pad_id(q) == pad_id(pad))
            assert cluster_ids(old, pad) == cluster_ids(new, other), (ref, pad.GetNumber())
    for name, number in [('ROW_GATE_14', '5'), ('VLED', '4')]:
        before = next(q for q in old_parts['PAIR15'].Pads() if q.GetNumber() == number)
        after = next(q for q in new_parts['PAIR15'].Pads() if q.GetNumber() == number)
        terminal = '2' if name == 'ROW_GATE_14' else '1'
        assert cluster_ids(new, after) == cluster_ids(old, before) | {('R20', terminal)}
    colour = escape.load_module('colour', 'check-colour-fanout-trial.py')
    baseline = ROOT / 'docs/development/led-ground-return-drc-2026-10-20.json'
    assert colour.findings(args.drc) == colour.findings(baseline)
    assert len(colour.findings(args.drc)) == 104
    reporter = escape.load_module('connectivity', 'report-coupon-board-connectivity.py')
    opens = reporter.open_edges_by_net(output)
    assert opens['native_open_edges'] == opens['pad_cluster_open_edges'] == manifest['open_edges'] == 364
    assert opens['by_net']['GND'] == 27 and opens['by_net']['VLED'] == 40
    assert 'ROW_GATE_14' not in opens['by_net']
    assert len(list(new.GetTracks())) == manifest['tracks_and_vias'] == 13286
    result = dict(board_sha256=manifest['board_sha256'], kicad_version=p.GetBuildVersion(),
                  moved_footprints=['R20'], unchanged_footprints=482, added_tracks=2,
                  existing_copper_and_other_clusters_preserved=True,
                  connected_gate_pullups=8, native_open_edges=364, ground_open_edges=27,
                  full_drc='104_UNCHANGED_INTRINSIC_FINDINGS',
                  drc_sha256=hashlib.sha256(args.drc.read_bytes()).hexdigest())
    result['SPDX-License-Identifier'] = 'CERN-OHL-S-2.0'
    if args.report:
        args.report.write_text(json.dumps(result, indent=2, sort_keys=True)+'\n')
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
