#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Check supply-only additions, intact prior clusters and exact native DRC."""
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
EXPECT = {'app': dict(opens=315, supply=7, additions=86),
          'usb': dict(opens=287, supply=4, additions=113),
          'vled': dict(opens=262, supply=15, additions=297)}


def cluster(board, pad):
    return frozenset((q.GetParentFootprint().GetReference(), q.GetNumber(),
                      q.GetPosition().x, q.GetPosition().y)
                     for q in board.GetConnectivity().GetConnectedItems(pad)
                     if isinstance(q, p.PAD))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--rail', choices=EXPECT, default='app')
    parser.add_argument('--drc', type=Path, required=True)
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    generator = escape.load_module('supply_gen', 'generate-supply-distribution-trial.py')
    spec, expected = generator.SPECS[args.rail], EXPECT[args.rail]
    source = escape.STAGING / (spec['source']+'.kicad_pcb')
    output = escape.STAGING / ('led-'+args.rail+'-distribution-trial-114mm.kicad_pcb')
    manifest = json.loads((ROOT / ('mechanical/review/'+args.rail+'-distribution-trial.json')).read_text())
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
    assert not +originals, 'Existing tracks/vias removed'
    assert len(added) == expected['additions']
    assert all(t.GetNetname() == spec['net'] for t in added)
    assert len(list(new.GetTracks())) == manifest['tracks_and_vias']
    for ref, part in before.items():
        for pad in part.Pads():
            if not pad.GetNetname():
                continue
            other = new_pads[(ref, pad.GetNumber(), pad.GetPosition().x, pad.GetPosition().y)]
            a, b = cluster(old, pad), cluster(new, other)
            if pad.GetNetname() == spec['net']:
                assert a <= b, ('Supply cluster split', ref, pad.GetNumber())
            else:
                assert a == b, ('Other pad cluster changed', ref, pad.GetNumber())
    zones = list(new.Zones())
    assert len(zones) == len(list(old.Zones()))+1
    original_zones = Counter((z.GetNetname(), z.GetLayer(), z.GetLocalClearance(), z.GetPadConnection()) for z in old.Zones())
    current_zones = Counter((z.GetNetname(), z.GetLayer(), z.GetLocalClearance(), z.GetPadConnection()) for z in zones)
    assert current_zones-original_zones == Counter({(spec['net'], spec['plane'], p.FromMM(.2), p.ZONE_CONNECTION_FULL): 1})
    assert not original_zones-current_zones
    pads = [q for f in after.values() for q in f.Pads() if q.GetNetname() == spec['net']]
    main_group = max({cluster(new, q) for q in pads}, key=len)
    assert [list(node[:2]) for node in sorted(main_group)] == manifest['main_cluster_pads']
    assert any(node[0] == spec['source_ref'] for node in main_group), 'Converter/LDO output not joined'
    assert manifest['source_connected_to_main'] is True
    for route in manifest['escapes']:
        if route['routed']:
            pad = next(q for q in after[route['ref']].Pads() if q.GetNumber() == route['pad'])
            assert cluster(new, pad) == main_group, route
    colour = escape.load_module('colour', 'check-colour-fanout-trial.py')
    baseline = ROOT / 'docs/development/led-local-control-drc-2026-10-20.json'
    assert colour.findings(args.drc) == colour.findings(baseline)
    assert len(colour.findings(args.drc)) == 104
    reporter = escape.load_module('connectivity', 'report-coupon-board-connectivity.py')
    opens = reporter.open_edges_by_net(output)
    assert opens['native_open_edges'] == opens['pad_cluster_open_edges'] == manifest['open_edges'] == expected['opens']
    assert opens['by_net'][spec['net']] == manifest['supply_open_edges'] == expected['supply']
    assert opens['by_net']['GND'] == 27
    result = dict(board_sha256=manifest['board_sha256'], kicad_version=p.GetBuildVersion(),
                  unchanged_footprints=483, added_tracks_and_vias=len(added),
                  source_tracks_and_vias_preserved=True, other_pad_clusters_unchanged=True,
                  target_net=spec['net'], supply_open_edges=expected['supply'],
                  source_connected_to_main=True, native_open_edges=expected['opens'],
                  ground_open_edges=27, full_drc='104_UNCHANGED_INTRINSIC_FINDINGS',
                  drc_sha256=hashlib.sha256(args.drc.read_bytes()).hexdigest(),
                  limitations='No copper-current, transient, bypass-loop, RF, thermal, HDI or fabrication approval')
    result['SPDX-License-Identifier'] = 'CERN-OHL-S-2.0'
    if args.report:
        args.report.write_text(json.dumps(result, indent=2, sort_keys=True)+'\n')
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
