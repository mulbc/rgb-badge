#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Relocate row-14 pullup beside its pair and join both local bias terminals.

Unbuilt geometry study only; canonical schematic/BOM and current limits stay fixed.
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
SOURCE = STAGING / 'led-ground-return-trial-114mm.kicad_pcb'
OUTPUT = STAGING / 'led-row14-bias-trial-114mm.kicad_pcb'
REPORT = ROOT / 'mechanical/review/row14-bias-trial.json'
SCOPE = uuid.UUID('e21b3125-9980-490a-9559-b8aab7565740')


def module(name, filename):
    spec = importlib.util.spec_from_file_location(name, ROOT / 'tools' / filename)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


def main():
    board = p.LoadBoard(str(SOURCE))
    parts = {f.GetReference(): f for f in board.GetFootprints()}
    resistor, pair = parts['R20'], parts['PAIR15']
    connected = board.GetConnectivity()
    # Both resistor terminals must be isolated in the input, so relocating it
    # cannot abandon any source route. A changed input must be reviewed anew.
    for pad in resistor.Pads():
        assert len(list(connected.GetConnectedItems(pad))) == 1
    old_position = [p.ToMM(resistor.GetPosition().x), p.ToMM(resistor.GetPosition().y)]
    resistor.SetOrientationDegrees(90)
    resistor.SetPosition(p.VECTOR2I(p.FromMM(73.5), p.FromMM(30)))
    for name, number in [('ROW_GATE_14', '5'), ('VLED', '4')]:
        start = next(pad for pad in resistor.Pads() if pad.GetNetname() == name)
        end = next(pad for pad in pair.Pads() if pad.GetNumber() == number)
        assert end.GetNetname() == name
        track = p.PCB_TRACK(board)
        track.SetStart(start.GetPosition())
        track.SetEnd(end.GetPosition())
        track.SetLayer(p.B_Cu)
        track.SetWidth(p.FromMM(.2))
        track.SetNet(start.GetNet())
        board.Add(track)
    p.ZONE_FILLER(board).Fill(board.Zones())
    p.SaveBoard(str(OUTPUT), board)
    helper = module('save', 'generate-paired-charger-114mm-routing.py')
    data = helper.sorted_native_tracks(OUTPUT.read_text(), expected=len(list(board.GetTracks())))
    sequence = iter(range(data.count('(uuid "')))
    data = re.sub(r'\(uuid "[0-9a-f-]{36}"\)',
                  lambda _: '(uuid "'+str(uuid.uuid5(SCOPE, str(next(sequence))))+'")', data)
    OUTPUT.write_text(data)
    loaded = p.LoadBoard(str(OUTPUT))
    report = dict(status='UNQUALIFIED_LOCAL_ROW_BIAS_STUDY',
                  source_sha256=hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
                  board_sha256=hashlib.sha256(OUTPUT.read_bytes()).hexdigest(),
                  kicad_version=p.GetBuildVersion(), moved_resistor='R20',
                  old_center_mm=old_position, new_center_mm=[73.5, 30],
                  new_rotation_degrees=90, added_tracks=2, width_mm=.2,
                  tracks_and_vias=len(list(loaded.GetTracks())),
                  open_edges=loaded.GetConnectivity().GetUnconnectedCount(False))
    report['SPDX-License-Identifier'] = 'CERN-OHL-S-2.0'
    REPORT.write_text(json.dumps(report, indent=2, sort_keys=True)+'\n')
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
