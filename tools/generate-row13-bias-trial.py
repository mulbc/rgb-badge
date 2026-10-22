#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Replay the selected row-13 placement/escape on the checked control study.

Unbuilt, noncanonical geometry only. No package, net or current-setting change.
"""
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import uuid
import pcbnew as p

ROOT = Path(__file__).resolve().parents[1]
STAGING = ROOT / 'hardware/coupon/rev-a/staging'
SOURCE = STAGING / 'led-control-continuation-trial-114mm.kicad_pcb'
OUTPUT = STAGING / 'led-row13-bias-trial-114mm.kicad_pcb'
REPORT = ROOT / 'mechanical/review/row13-bias-trial.json'
SOURCE_SHA256 = 'f945becb2b685e14bc08a3402e07bf1c2fc56af6b940e12b3470f6fad3e16851'
SCOPE = uuid.UUID('b3c838ba-12ae-4d21-9de7-c20b9c639b16')

# Compact replay of the selected 0.05 mm search path. The first gate lead
# contacts the interior of existing vertical gate copper at its exact x.
SEGMENTS = [
    ('ROW_GATE_13', p.B_Cu, (78.825, 26.721428), (78.2, 27.45)),
    ('ROW_GATE_13', p.B_Cu, (78.2, 27.45), (78.2, 27.5)),
    ('ROW_GATE_13', p.In4_Cu, (78.2, 27.5), (77.1, 27.5)),
    ('ROW_GATE_13', p.In4_Cu, (77.1, 27.5), (77.1, 27.45)),
    ('ROW_GATE_13', p.In4_Cu, (77.1, 27.45), (73.45, 27.45)),
    ('VLED', p.B_Cu, (72.45, 27.45), (72.45, 26.85)),
    ('VLED', p.B_Cu, (72.45, 26.85), (74.8, 26.85)),
    ('VLED', p.B_Cu, (74.8, 26.85), (74.8, 26.9)),
    ('VLED', p.B_Cu, (74.8, 26.9), (74.825, 26.9)),
]
VIA_POSITIONS = [(78.2, 27.5), (73.45, 27.45)]


def point(xy):
    return p.VECTOR2I(*(p.FromMM(value) for value in xy))


def main():
    assert hashlib.sha256(SOURCE.read_bytes()).hexdigest() == SOURCE_SHA256, 'Source changed; review the escape again'
    board = p.LoadBoard(str(SOURCE))
    parts = {part.GetReference(): part for part in board.GetFootprints()}
    resistor = parts['R19']
    assert resistor.GetValue() == '1k 1%'
    assert resistor.GetFPIDAsString() == 'rgb-badge-coupon:R_Panasonic_ERJ2_0402'
    assert resistor.GetPosition() == point((59.75, 5.75))
    assert resistor.GetOrientation().AsDegrees() == 180
    assert {pad.GetNumber(): pad.GetNetname() for pad in resistor.Pads()} == {'1': 'VLED', '2': 'ROW_GATE_13'}
    assert all(len(board.GetConnectivity().GetConnectedItems(pad)) == 1 for pad in resistor.Pads()), 'R19 must have two isolated source pads'
    initial_tracks = len(list(board.GetTracks()))
    resistor.SetOrientationDegrees(0)
    resistor.SetPosition(point((72.95, 27.45)))
    for name, layer, start, end in SEGMENTS:
        track = p.PCB_TRACK(board)
        track.SetStart(point(start))
        track.SetEnd(point(end))
        track.SetLayer(layer)
        track.SetWidth(p.FromMM(.2))
        track.SetNet(board.FindNet(name))
        board.Add(track)
    for position in VIA_POSITIONS:
        via = p.PCB_VIA(board)
        via.SetPosition(point(position))
        via.SetViaType(p.VIATYPE_MICROVIA)
        via.SetLayerPair(p.In4_Cu, p.B_Cu)
        via.SetWidth(p.FromMM(.3))
        via.SetDrill(p.FromMM(.1))
        via.SetNet(board.FindNet('ROW_GATE_13'))
        board.Add(via)
    p.ZONE_FILLER(board).Fill(board.Zones())
    p.SaveBoard(str(OUTPUT), board)
    spec = importlib.util.spec_from_file_location('save', ROOT / 'tools/generate-paired-charger-114mm-routing.py')
    helper = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(helper)
    data = helper.sorted_native_tracks(OUTPUT.read_text(), expected=initial_tracks+11)
    sequence = iter(range(data.count('(uuid "')))
    data = re.sub(r'\(uuid "[0-9a-f-]{36}"\)',
                  lambda _: '(uuid "'+str(uuid.uuid5(SCOPE, str(next(sequence))))+'")', data)
    OUTPUT.write_text(data)
    loaded = p.LoadBoard(str(OUTPUT))
    report = dict(status='UNQUALIFIED_ROW13_BIAS_GEOMETRY_STUDY',
                  source_sha256=SOURCE_SHA256,
                  board_sha256=hashlib.sha256(OUTPUT.read_bytes()).hexdigest(),
                  generator_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                  kicad_version=p.GetBuildVersion(), moved_resistor='R19',
                  old_center_mm=[59.75, 5.75], old_rotation_degrees=180,
                  new_center_mm=[72.95, 27.45], new_rotation_degrees=0,
                  track_width_mm=.2, microvia_diameter_drill_mm=[.3, .1],
                  source_tracks_and_vias=initial_tracks, added_tracks=9, added_microvias=2,
                  tracks_and_vias=len(list(loaded.GetTracks())),
                  open_edges=loaded.GetConnectivity().GetUnconnectedCount(False),
                  search_result_replayed_as_fixed_geometry=True)
    report['SPDX-License-Identifier'] = 'CERN-OHL-S-2.0'
    REPORT.write_text(json.dumps(report, indent=2, sort_keys=True)+'\n')
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
