#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Verify ground-return additions and native DRC against the checked baseline."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import pcbnew as p

ROOT = Path(__file__).resolve().parents[1]
# Reuse the baseline's physical-pad and native-shape comparisons.
import importlib.util
spec = importlib.util.spec_from_file_location('escape', ROOT / 'tools/check-ground-escape-trial.py')
escape = importlib.util.module_from_spec(spec)
spec.loader.exec_module(escape)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--drc', type=Path, required=True)
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    source = escape.STAGING / 'led-ground-escape-trial-114mm.kicad_pcb'
    output = escape.STAGING / 'led-ground-return-trial-114mm.kicad_pcb'
    manifest = json.loads((ROOT / 'mechanical/review/ground-return-trial.json').read_text())
    assert hashlib.sha256(source.read_bytes()).hexdigest() == manifest['source_sha256']
    assert hashlib.sha256(output.read_bytes()).hexdigest() == manifest['board_sha256']
    old, new = p.LoadBoard(str(source)), p.LoadBoard(str(output))
    old_parts = {f.GetReference(): f for f in old.GetFootprints()}
    new_parts = {f.GetReference(): f for f in new.GetFootprints()}
    assert old_parts.keys() == new_parts.keys() and len(new_parts) == 483
    for ref, part in old_parts.items():
        other = new_parts[ref]
        assert (part.GetValue(), part.GetFPIDAsString(), part.GetPosition(),
                part.GetOrientation().AsDegrees(), part.GetLayer()) == (
                    other.GetValue(), other.GetFPIDAsString(), other.GetPosition(),
                    other.GetOrientation().AsDegrees(), other.GetLayer()), ref
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
    assert not +originals, 'Existing copper removed'
    assert len(added) == 22
    assert all(item.GetNetname() == 'GND' for item in added)
    assert escape.pad_clusters(old) == escape.pad_clusters(new), 'Non-ground pad clusters changed'
    assert len(list(new.GetTracks())) == manifest['tracks_and_vias'] == 13284
    assert new.GetConnectivity().GetUnconnectedCount(False) == manifest['open_edges'] == 366
    assert not escape.ground_shape_conflicts(new, added), 'Ground copper clearance conflict'
    zones = list(new.Zones())
    assert len(zones) == 2 and all(z.GetNetname() == 'GND' for z in zones)
    actual_zones = [dict(layer=new.GetLayerName(z.GetLayer()),
                         polygons=z.GetFilledPolysList(z.GetLayer()).OutlineCount(),
                         area_mm2=round(z.GetFilledPolysList(z.GetLayer()).Area()/1e12, 3))
                    for z in zones]
    assert sorted(actual_zones, key=lambda x: x['layer']) == sorted(manifest['zones'], key=lambda x: x['layer'])
    assert {z.GetLayer() for z in zones} == {p.B_Cu, p.In2_Cu}
    reporter = escape.load_module('connectivity', 'report-coupon-board-connectivity.py')
    opens = reporter.open_edges_by_net(output)
    assert opens['native_open_edges'] == opens['pad_cluster_open_edges'] == 366
    assert opens['by_net']['GND'] == manifest['ground_open_edges'] == 27
    # Check that every claimed island join reaches the real main network.
    connected = new.GetConnectivity()
    reference = next(q for q in new_parts['C1'].Pads() if q.GetNumber() == '2')
    main_cluster = {q.m_Uuid.AsString() for q in connected.GetConnectedItems(reference)
                    if isinstance(q, p.PAD)}
    for route in manifest['routes']:
        if route['routed']:
            for ref, number in route['pads']:
                pads = [q for q in new_parts[ref].Pads() if q.GetNumber() == number]
                assert pads and all(pad.m_Uuid.AsString() in main_cluster for pad in pads), (ref, number)
    colour = escape.load_module('colour', 'check-colour-fanout-trial.py')
    baseline = ROOT / 'docs/development/led-ground-escape-drc-2026-10-20.json'
    assert colour.findings(args.drc) == colour.findings(baseline)
    assert len(colour.findings(args.drc)) == 104
    result = dict(board_sha256=manifest['board_sha256'], kicad_version=p.GetBuildVersion(),
                  added_ground_tracks_and_vias=len(added), unchanged_footprints=483,
                  non_ground_clusters_preserved=True, native_shape_clearance_conflicts=0,
                  native_open_edges=366, ground_open_edges=27, zones=actual_zones,
                  full_drc='104_UNCHANGED_INTRINSIC_FINDINGS',
                  drc_sha256=hashlib.sha256(args.drc.read_bytes()).hexdigest(),
                  limitations='Unbuilt geometry study; current returns, RF, thermal, mask/paste, HDI and Gate A remain unqualified')
    result['SPDX-License-Identifier'] = 'CERN-OHL-S-2.0'
    if args.report:
        args.report.write_text(json.dumps(result, indent=2, sort_keys=True)+'\n')
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
