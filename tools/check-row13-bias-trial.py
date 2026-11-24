#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Check the saved row-13 study, physical cluster preservation and native DRC."""
import argparse
from collections import Counter
import hashlib
import importlib.util
import json
from pathlib import Path
import pcbnew as p

ROOT = Path(__file__).resolve().parents[1]
STAGING = ROOT / 'hardware/coupon/rev-a/staging'
SOURCE = STAGING / 'led-control-continuation-trial-114mm.kicad_pcb'
OUTPUT = STAGING / 'led-row13-bias-trial-114mm.kicad_pcb'


def module(name, filename):
    spec = importlib.util.spec_from_file_location(name, ROOT / 'tools' / filename)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


def identity(pad):
    ref, number = pad.GetParentFootprint().GetReference(), pad.GetNumber()
    # Only this two-pad footprint moves. All duplicate drain lands retain
    # their physical coordinates, so removing a second pad-3 tie cannot hide.
    return (ref, number, 0, 0) if ref == 'R19' else (
        ref, number, pad.GetPosition().x, pad.GetPosition().y)


def cluster(board, pad):
    return frozenset(identity(q) for q in board.GetConnectivity().GetConnectedItems(pad)
                     if isinstance(q, p.PAD))


def validate_geometry(old, new):
    escape = module('escape', 'check-ground-escape-trial.py')
    grid = module('grid', 'generate-colour-fanout-grid-trial.py')
    before = {part.GetReference(): part for part in old.GetFootprints()}
    after = {part.GetReference(): part for part in new.GetFootprints()}
    assert before.keys() == after.keys() and len(after) == 483
    new_pads = {}
    for ref, part in before.items():
        other = after[ref]
        assert (part.GetValue(), part.GetFPIDAsString(), part.GetLayer()) == (
            other.GetValue(), other.GetFPIDAsString(), other.GetLayer()), ref
        expected = part
        if ref == 'R19':
            assert (part.GetPosition().x, part.GetPosition().y) == (59750000, 5750000)
            assert part.GetOrientation().AsDegrees() == 180
            assert all(len(old.GetConnectivity().GetConnectedItems(q)) == 1 for q in part.Pads())
            assert (other.GetPosition().x, other.GetPosition().y) == (72950000, 27450000)
            assert other.GetOrientation().AsDegrees() == 0
            expected = p.FOOTPRINT(part)
            expected.SetOrientationDegrees(0)
            expected.SetPosition(p.VECTOR2I(72950000, 27450000))
        else:
            assert (part.GetPosition(), part.GetOrientation().AsDegrees()) == (
                other.GetPosition(), other.GetOrientation().AsDegrees()), ref
        assert Counter(map(escape.pad_signature, expected.Pads())) == Counter(
            map(escape.pad_signature, other.Pads())), ('Physical pad geometry changed', ref)
        for pad in other.Pads():
            assert identity(pad) not in new_pads, ('Duplicate physical pad identity', ref)
            new_pads[identity(pad)] = pad

    originals = Counter(grid.signature(item) for item in old.GetTracks())
    added = []
    for item in new.GetTracks():
        signature = grid.signature(item)
        if originals[signature]:
            originals[signature] -= 1
        else:
            added.append(item)
    assert not +originals, 'Source copper removed'
    assert len(added) == 11, 'Expected nine added tracks and two microvias'
    vias = [item for item in added if isinstance(item, p.PCB_VIA)]
    tracks = [item for item in added if not isinstance(item, p.PCB_VIA)]
    assert len(vias) == 2 and len(tracks) == 9
    assert Counter(t.GetNetname() for t in tracks) == Counter({'ROW_GATE_13': 5, 'VLED': 4})
    for item in tracks:
        assert item.GetWidth() == p.FromMM(.2)
        assert item.GetStart() != item.GetEnd()
        assert item.GetLayer() in ((p.B_Cu, p.In4_Cu) if item.GetNetname() == 'ROW_GATE_13' else (p.B_Cu,))
    stack = list(new.GetEnabledLayers().CuStack())
    for item in vias:
        assert item.GetNetname() == 'ROW_GATE_13'
        assert item.GetViaType() == p.VIATYPE_MICROVIA
        assert item.GetWidth(item.TopLayer()) == p.FromMM(.3)
        assert item.GetDrillValue() == p.FromMM(.1)
        assert {item.TopLayer(), item.BottomLayer()} == {p.B_Cu, p.In4_Cu}
        assert abs(stack.index(item.TopLayer())-stack.index(item.BottomLayer())) == 1
    changed = set()
    for part in before.values():
        for pad in part.Pads():
            if not pad.GetNetname():
                continue
            a, b = cluster(old, pad), cluster(new, new_pads[identity(pad)])
            assert a <= b, ('Existing physical pad cluster split', identity(pad))
            if a != b:
                changed.add(pad.GetNetname())
    assert changed == {'ROW_GATE_13', 'VLED'}
    for name, anchor_ref, anchor_number, terminal in (
            ('ROW_GATE_13', 'PAIR14', '5', '2'), ('VLED', 'PAIR13', '4', '1')):
        anchor = next(q for q in before[anchor_ref].Pads() if q.GetNumber() == anchor_number)
        resistor_pad = next(q for q in after['R19'].Pads() if q.GetNumber() == terminal)
        assert resistor_pad.GetNetname() == name
        assert cluster(new, resistor_pad) == cluster(old, anchor) | {('R19', terminal, 0, 0)}
    physical = module('physical', 'check-row-drain-tie-trial.py')
    physical.check_physical_rows(new)
    return dict(unchanged_footprints=482, moved_resistor='R19', added_tracks=9,
                added_microvias=2, source_tracks_and_vias_preserved=True,
                existing_physical_pad_clusters_preserved=True,
                exactly_two_terminal_merges=True, physical_anode_pads_per_row=18)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--drc', type=Path, required=True)
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    manifest = json.loads((ROOT / 'mechanical/review/row13-bias-trial.json').read_text())
    assert hashlib.sha256(SOURCE.read_bytes()).hexdigest() == manifest['source_sha256']
    assert hashlib.sha256(OUTPUT.read_bytes()).hexdigest() == manifest['board_sha256']
    assert hashlib.sha256((ROOT / 'tools/generate-row13-bias-trial.py').read_bytes()).hexdigest() == manifest['generator_sha256']
    old, new = p.LoadBoard(str(SOURCE)), p.LoadBoard(str(OUTPUT))
    result = validate_geometry(old, new)
    colour = module('colour', 'check-colour-fanout-trial.py')
    assert colour.findings(args.drc) == colour.findings(ROOT / 'docs/development/led-control-continuation-drc-2026-10-21.json')
    assert len(colour.findings(args.drc)) == 104
    reporter = module('connectivity', 'report-coupon-board-connectivity.py')
    opens = reporter.open_edges_by_net(OUTPUT)
    assert opens['native_open_edges'] == opens['pad_cluster_open_edges'] == manifest['open_edges'] == 234
    assert opens['by_net']['GND'] == 27 and opens['by_net']['VLED'] == 14
    assert 'ROW_GATE_13' not in opens['by_net']
    remaining = {int(name.removeprefix('ROW_GATE_')) for name in opens['by_net'] if name.startswith('ROW_GATE_')}
    assert remaining == {0, 2, 3, 4, 5, 6, 7}
    assert len(list(new.GetTracks())) == manifest['tracks_and_vias'] == 14494
    result.update(board_sha256=manifest['board_sha256'], kicad_version=p.GetBuildVersion(),
                  tracks_and_vias=14494, native_open_edges=234, ground_open_edges=27,
                  vled_open_edges=14, connected_gate_terminals=9, remaining_gate_rows=sorted(remaining),
                  full_drc='104_UNCHANGED_INTRINSIC_FINDINGS',
                  drc_sha256=hashlib.sha256(args.drc.read_bytes()).hexdigest())
    result['SPDX-License-Identifier'] = 'CERN-OHL-S-2.0'
    if args.report:
        args.report.write_text(json.dumps(result, indent=2, sort_keys=True)+'\n')
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
