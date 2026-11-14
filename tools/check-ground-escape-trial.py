#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Check ground-only changes, native connectivity and copper shape clearance.

Without --drc this is a partial geometry check, never a full DRC pass.
"""
import argparse
from collections import Counter, defaultdict
import hashlib
import importlib.util
import json
from pathlib import Path
import pcbnew as p

ROOT = Path(__file__).resolve().parents[1]
STAGING = ROOT / 'hardware/coupon/rev-a/staging'


def load_module(name, filename):
    spec = importlib.util.spec_from_file_location(name, ROOT / 'tools' / filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def pad_signature(pad):
    return (pad.GetNumber(), pad.GetNetname(), pad.GetPosition().x,
            pad.GetPosition().y, pad.GetSize().x, pad.GetSize().y,
            pad.GetOrientation().AsDegrees(), pad.GetShape(),
            tuple(pad.GetLayerSet().Seq()))


def pad_clusters(board):
    connectivity = board.GetConnectivity()
    # UUIDs are normalized on save, so use physical pad identities instead.
    result = defaultdict(set)
    for part in board.GetFootprints():
        for pad in part.Pads():
            name = pad.GetNetname()
            if name and name != 'GND':
                result[name].add(tuple(sorted(
                    (item.GetParentFootprint().GetReference(), *pad_signature(item))
                    for item in connectivity.GetConnectedItems(pad)
                    if isinstance(item, p.PAD))))
    return dict(result)


def ground_shape_conflicts(board, added):
    """Native shape pair screen, excluding zones and full DRC rule evaluation."""
    ground = board.FindNet('GND').GetNetCode()
    bins = defaultdict(list)
    def cells(box, gap=0):
        return [(x, y)
                for x in range((box.GetX()-gap)//1000000,
                               (box.GetRight()+gap)//1000000+1)
                for y in range((box.GetY()-gap)//1000000,
                               (box.GetBottom()+gap)//1000000+1)]
    items = [item for item in board.GetTracks() if item.GetNetCode() != ground]
    items += [pad for part in board.GetFootprints() for pad in part.Pads()
              if pad.GetNetCode() != ground]
    layers = tuple(board.GetEnabledLayers().CuStack())
    for index, item in enumerate(items):
        for layer in layers:
            if item.IsOnLayer(layer):
                for cell in cells(item.GetBoundingBox(), p.FromMM(.2)):
                    bins[(layer, *cell)].append(index)
    conflicts = []
    for item in added:
        assert item.GetNetname() == 'GND'
        for layer in layers:
            if not item.IsOnLayer(layer):
                continue
            candidates = {index for cell in cells(item.GetBoundingBox())
                          for index in bins[(layer, *cell)]}
            shape = item.GetEffectiveShape(layer)
            for index in candidates:
                other = items[index]
                # Ten internal units (0.00001 mm) avoid equality-rounding noise.
                if shape.Collide(other.GetEffectiveShape(layer), p.FromMM(.2)-10):
                    conflicts.append((item.m_Uuid.AsString(), other.m_Uuid.AsString(), layer))
    return conflicts


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--drc', type=Path)
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    source = STAGING / 'led-row-combined-partial-trial-114mm.kicad_pcb'
    output = STAGING / 'led-ground-escape-trial-114mm.kicad_pcb'
    manifest = json.loads((ROOT / 'mechanical/review/ground-escape-trial.json').read_text())
    assert hashlib.sha256(source.read_bytes()).hexdigest() == manifest['source_sha256']
    assert hashlib.sha256(output.read_bytes()).hexdigest() == manifest['board_sha256']
    old, new = p.LoadBoard(str(source)), p.LoadBoard(str(output))
    old_parts = {part.GetReference(): part for part in old.GetFootprints()}
    new_parts = {part.GetReference(): part for part in new.GetFootprints()}
    assert old_parts.keys() == new_parts.keys() and len(new_parts) == 483
    for ref, part in old_parts.items():
        other = new_parts[ref]
        assert (part.GetValue(), part.GetFPIDAsString(), part.GetPosition(),
                part.GetOrientation().AsDegrees(), part.GetLayer()) == (
                    other.GetValue(), other.GetFPIDAsString(), other.GetPosition(),
                    other.GetOrientation().AsDegrees(), other.GetLayer()), ref
        assert Counter(map(pad_signature, part.Pads())) == Counter(map(pad_signature, other.Pads())), ref
    grid = load_module('grid', 'generate-colour-fanout-grid-trial.py')
    originals = Counter(grid.signature(item) for item in old.GetTracks())
    added = []
    for item in new.GetTracks():
        sig = grid.signature(item)
        if originals[sig]:
            originals[sig] -= 1
        else:
            added.append(item)
    assert not +originals, 'Existing copper removed'
    assert len(added) == 900
    assert all(item.GetNetname() == 'GND' for item in added)
    assert pad_clusters(old) == pad_clusters(new), 'Non-ground pad clusters changed'
    assert len(list(new.GetTracks())) == manifest['tracks_and_vias'] == 13262
    assert new.GetConnectivity().GetUnconnectedCount(False) == manifest['open_edges'] == 383
    zones = list(new.Zones())
    assert len(zones) == 1 and zones[0].GetNetname() == 'GND'
    assert zones[0].GetLayer() == p.In2_Cu
    fill = zones[0].GetFilledPolysList(p.In2_Cu)
    assert fill.OutlineCount() == manifest['zone_polygons'] == 6
    assert round(fill.Area()/1e12, 3) == manifest['zone_area_mm2']
    assert not ground_shape_conflicts(new, added), 'Added ground copper clearance conflict'
    connectivity = load_module('connectivity', 'report-coupon-board-connectivity.py')
    opens = connectivity.open_edges_by_net(output)
    assert opens['native_open_edges'] == opens['pad_cluster_open_edges'] == 383
    assert opens['by_net']['GND'] == 44
    result = dict(board_sha256=manifest['board_sha256'],
                  kicad_version=p.GetBuildVersion(),
                  added_ground_tracks_and_vias=len(added),
                  unchanged_footprints=483, non_ground_clusters_preserved=True,
                  native_shape_clearance_conflicts=0, native_open_edges=383,
                  ground_open_edges=44, zone_polygons=6,
                  full_drc='NOT_RUN',
                  limitations='Shape screen excludes zones, rule evaluation, mask, holes, RF, electrical and process qualification')
    result['SPDX-License-Identifier'] = 'CERN-OHL-S-2.0'
    if args.drc:
        colour = load_module('colour', 'check-colour-fanout-trial.py')
        baseline = ROOT / 'docs/development/led-colour-fanout-grid-drc-2026-10-19.json'
        assert colour.findings(args.drc) == colour.findings(baseline)
        assert len(colour.findings(args.drc)) == 104
        result['full_drc'] = '104_UNCHANGED_INTRINSIC_FINDINGS'
        result['drc_sha256'] = hashlib.sha256(args.drc.read_bytes()).hexdigest()
    if args.report:
        args.report.write_text(json.dumps(result, indent=2, sort_keys=True)+'\n')
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
