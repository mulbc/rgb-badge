#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Check the saved, provisional In2 ground study against its source and DRC."""

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path

import pcbnew as pcb


ROOT = Path(__file__).resolve().parents[1]
STAGING = ROOT / 'hardware/coupon/rev-a/staging'


def signature(track):
    if isinstance(track, pcb.PCB_VIA):
        return ('via', track.GetNetname(), track.GetPosition().x,
                track.GetPosition().y, track.GetViaType(), track.GetWidth(pcb.F_Cu),
                track.GetDrillValue(), tuple(sorted(track.GetLayerSet().CuStack())))
    return ('segment', track.GetNetname(), track.GetLayer(),
            track.GetStart().x, track.GetStart().y,
            track.GetEnd().x, track.GetEnd().y, track.GetWidth())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--drc', required=True, type=Path)
    args = parser.parse_args()
    source = STAGING / 'led-row-pulldown-complete-trial-114mm.kicad_pcb'
    output = STAGING / 'led-in2-ground-plane-trial-114mm.kicad_pcb'
    report = json.loads((ROOT / 'mechanical/review/in2-ground-plane-trial.json').read_text())
    assert report['status'] == 'UNQUALIFIED_GROUND_PLANE_STUDY'
    assert hashlib.sha256(source.read_bytes()).hexdigest() == report['source_sha256']
    assert hashlib.sha256(output.read_bytes()).hexdigest() == report['board_sha256']
    old = pcb.LoadBoard(str(source))
    new = pcb.LoadBoard(str(output))
    from collections import Counter
    removed = Counter(map(signature, old.GetTracks())) - Counter(map(signature, new.GetTracks()))
    added = Counter(map(signature, new.GetTracks())) - Counter(map(signature, old.GetTracks()))
    assert not removed, removed
    assert sum(added.values()) == 3, added
    assert len(list(new.GetTracks())) == report['tracks_and_vias'] == 11484
    assert all(item[0] == 'via' and item[1] == 'GND' and
               [pcb.ToMM(item[2]), pcb.ToMM(item[3])] == report['ground_anchor_mm']
               for item in added), added
    parts = {part.GetReference(): part for part in new.GetFootprints()}
    assert len(parts) == 483
    anchor = next(pad for pad in parts['R25'].Pads() if pad.GetNumber() == '2')
    assert anchor.GetNetname() == 'GND'
    assert all(via in new.GetConnectivity().GetConnectedItems(anchor)
               for via in new.GetTracks() if signature(via) in added)
    zones = list(new.Zones())
    assert len(zones) == 1
    zone = zones[0]
    assert zone.GetNetname() == 'GND' and zone.GetLayer() == pcb.In2_Cu
    assert zone.GetIslandRemovalMode() == pcb.ISLAND_REMOVAL_MODE_ALWAYS
    fill = zone.GetFilledPolysList(pcb.In2_Cu)
    assert fill.OutlineCount() == report['zone_outlines'] == 1
    assert round(fill.Area() / 1e12, 3) == report['zone_area_mm2']
    assert new.GetConnectivity().GetUnconnectedCount(False) == report['open_edges'] == 534
    spec = importlib.util.spec_from_file_location(
        'colour_check', ROOT / 'tools/check-colour-fanout-trial.py')
    colour = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(colour)
    baseline = ROOT / 'docs/development/led-colour-fanout-grid-drc-2026-10-19.json'
    assert colour.findings(args.drc) == colour.findings(baseline)
    assert len(colour.findings(args.drc)) == 104
    print('One anchored In2 GND polygon; three added GND microvias; '
          '534 open edges and 104 unchanged DRC findings.')


if __name__ == '__main__':
    main()
