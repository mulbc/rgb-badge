#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Check the control continuation against physical-drain source and full native DRC."""
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


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--drc', required=True, type=Path)
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    source = escape.STAGING / 'led-row-drain-tie-trial-114mm.kicad_pcb'
    output = escape.STAGING / 'led-control-continuation-trial-114mm.kicad_pcb'
    manifest = json.loads((ROOT / 'mechanical/review/control-continuation-trial.json').read_text())
    assert manifest['connected_copper_endpoints'] and manifest['preserve_clusters_after_each_join']
    assert hashlib.sha256(source.read_bytes()).hexdigest() == manifest['source_sha256']
    assert hashlib.sha256(output.read_bytes()).hexdigest() == manifest['board_sha256']
    old, new = p.LoadBoard(str(source)), p.LoadBoard(str(output))
    before = {f.GetReference(): f for f in old.GetFootprints()}
    after = {f.GetReference(): f for f in new.GetFootprints()}
    assert before.keys() == after.keys() and len(after) == 483
    new_pads = {}
    for ref, part in before.items():
        other = after[ref]
        assert (part.GetValue(), part.GetFPIDAsString(), part.GetPosition(),
                part.GetOrientation().AsDegrees(), part.GetLayer()) == (
                    other.GetValue(), other.GetFPIDAsString(), other.GetPosition(),
                    other.GetOrientation().AsDegrees(), other.GetLayer()), ref
        assert Counter(map(escape.pad_signature, part.Pads())) == Counter(map(escape.pad_signature, other.Pads())), ref
        for pad in other.Pads():
            new_pads[(ref, pad.GetNumber(), pad.GetPosition().x, pad.GetPosition().y)] = pad
    grid = escape.load_module('grid', 'generate-colour-fanout-grid-trial.py')
    originals = Counter(grid.signature(item) for item in old.GetTracks())
    added = []
    for item in new.GetTracks():
        signature = grid.signature(item)
        if originals[signature]:
            originals[signature] -= 1
        else:
            added.append(item)
    assert not +originals, 'Source copper removed'
    assert len(added) == manifest['added_tracks_and_vias'] == 288
    assert all(t.GetNetname() in manifest['allowed_nets'] for t in added)
    stack = list(new.GetEnabledLayers().CuStack())
    for item in added:
        if isinstance(item, p.PCB_VIA):
            assert item.GetViaType() == p.VIATYPE_MICROVIA
            assert item.GetWidth(item.TopLayer()) == p.FromMM(.3) and item.GetDrillValue() == p.FromMM(.1)
            assert abs(stack.index(item.TopLayer())-stack.index(item.BottomLayer())) == 1
        else:
            assert item.GetWidth() == p.FromMM(.2)
    changed_nets = set()
    for ref, part in before.items():
        for pad in part.Pads():
            if not pad.GetNetname():
                continue
            other = new_pads[(ref, pad.GetNumber(), pad.GetPosition().x, pad.GetPosition().y)]
            a, b = cluster(old, pad), cluster(new, other)
            assert a <= b, ('Existing cluster split', ref, pad.GetNumber())
            if a != b:
                assert pad.GetNetname() in manifest['allowed_nets']
                changed_nets.add(pad.GetNetname())
    completed_routes = [r for r in manifest['routes'] if r['routed']]
    assert changed_nets == {r['net'] for r in completed_routes}
    assert changed_nets == {'CHARGER_GATE_EN', 'ROW_A2', 'ROW_A3',
                            'SYS_I2C_SDA', 'USB_CC_HIGH', 'USB_CHARGE_REQ',
                            'USB_LOGIC_SENSE'}
    assert len(completed_routes) == 10
    rejected = [r for r in manifest['routes'] if r.get('rejected_reason')]
    assert {r['net'] for r in rejected} == {'GAUGE_I2C_SDA', 'GAUGE_I2C_SCL'}
    assert all(not r['routed'] and r['rejected_reason'] ==
               'existing_pad_cluster_split_after_zone_refill' for r in rejected)
    # Native evidence for each claimed source-to-anchor join, including the
    # multiple-pad ARM_LATCH and VLED_WINDOW_OK networks.
    for route in completed_routes:
        pads = sorted((q for f in after.values() for q in f.Pads() if q.GetNetname() == route['net']),
                      key=lambda q: (q.GetParentFootprint().GetReference(), q.GetNumber()))
        pad = next(q for q in pads if [q.GetParentFootprint().GetReference(), q.GetNumber()] == route['source'])
        assert cluster(new, pad) == cluster(new, pads[0]), route
    colour = escape.load_module('colour', 'check-colour-fanout-trial.py')
    baseline = ROOT / 'docs/development/led-row-drain-tie-drc-2026-10-20.json'
    assert colour.findings(args.drc) == colour.findings(baseline)
    assert len(colour.findings(args.drc)) == 104
    reporter = escape.load_module('connectivity', 'report-coupon-board-connectivity.py')
    opens = reporter.open_edges_by_net(output)
    assert opens['native_open_edges'] == opens['pad_cluster_open_edges'] == manifest['open_edges'] == 236
    assert opens['by_net']['GND'] == 27
    assert 246-opens['native_open_edges'] >= len(completed_routes) > 0
    assert len(list(new.GetTracks())) == manifest['tracks_and_vias'] == 14483
    physical = escape.load_module('physical', 'check-row-drain-tie-trial.py')
    physical.check_physical_rows(new)
    assert sum(opens['by_net'].get(n, 0) for n in ('GND', 'VLED', '+3V3_APP', '+3V3_USB')) == 53
    result = dict(board_sha256=manifest['board_sha256'], kicad_version=p.GetBuildVersion(),
                  unchanged_footprints=483, physical_anode_pads_per_row=18, added_tracks_and_vias=len(added),
                  plane_splitting_route_rejections=len(rejected),
                  source_tracks_and_vias_preserved=True, existing_pad_clusters_preserved=True,
                  changed_nets=sorted(changed_nets), control_joins=246-opens['native_open_edges'],
                  native_open_edges=opens['native_open_edges'], ground_open_edges=27,
                  full_drc='104_UNCHANGED_INTRINSIC_FINDINGS',
                  drc_sha256=hashlib.sha256(args.drc.read_bytes()).hexdigest())
    result['SPDX-License-Identifier'] = 'CERN-OHL-S-2.0'
    if args.report:
        args.report.write_text(json.dumps(result, indent=2, sort_keys=True)+'\n')
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
