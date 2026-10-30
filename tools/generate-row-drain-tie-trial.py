#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Join each candidate row pair's two physical P-drain lands on B.Cu.

Unbuilt geometry study only. Pin map, footprints, source limits and placements
are unchanged; the two lands already have the same schematic pin/net.
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
SOURCE = STAGING / 'led-vled-distribution-trial-114mm.kicad_pcb'
OUTPUT = STAGING / 'led-row-drain-tie-trial-114mm.kicad_pcb'
REPORT = ROOT / 'mechanical/review/row-drain-tie-trial.json'
SCOPE = uuid.UUID('f6e1f9a6-6ea0-4cf4-9785-bc9f49eb2d81')


def main():
    board = p.LoadBoard(str(SOURCE))
    parts = {f.GetReference(): f for f in board.GetFootprints()}
    routes = []
    for row in range(16):
        part = parts[f'PAIR{row+1:02d}']
        assert part.GetValue() == 'NTLJD3119CTBG_TRIAL_ONLY'
        pads = [pad for pad in part.Pads() if pad.GetNumber() == '3']
        assert len(pads) == 2
        assert all(pad.GetNetname() == f'ROW_{row:02d}_A' for pad in pads)
        pads.sort(key=lambda q: (q.GetPosition().x, q.GetPosition().y))
        trace = p.PCB_TRACK(board)
        trace.SetStart(pads[0].GetPosition())
        trace.SetEnd(pads[1].GetPosition())
        trace.SetLayer(p.B_Cu)
        trace.SetWidth(p.FromMM(.2))
        trace.SetNet(pads[0].GetNet())
        board.Add(trace)
        routes.append(dict(pair=part.GetReference(), net=pads[0].GetNetname(),
                           start_mm=[p.ToMM(pads[0].GetPosition().x), p.ToMM(pads[0].GetPosition().y)],
                           end_mm=[p.ToMM(pads[1].GetPosition().x), p.ToMM(pads[1].GetPosition().y)]))
    p.ZONE_FILLER(board).Fill(board.Zones())
    p.SaveBoard(str(OUTPUT), board)
    spec = importlib.util.spec_from_file_location('save', ROOT / 'tools/generate-paired-charger-114mm-routing.py')
    helper = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(helper)
    data = helper.sorted_native_tracks(OUTPUT.read_text(), expected=len(list(board.GetTracks())))
    sequence = iter(range(data.count('(uuid "')))
    data = re.sub(r'\(uuid "[0-9a-f-]{36}"\)',
                  lambda _: '(uuid "'+str(uuid.uuid5(SCOPE, str(next(sequence))))+'")', data)
    OUTPUT.write_text(data)
    loaded = p.LoadBoard(str(OUTPUT))
    report = dict(status='UNQUALIFIED_PHYSICAL_DRAIN_TIE_STUDY',
                  source_sha256=hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
                  board_sha256=hashlib.sha256(OUTPUT.read_bytes()).hexdigest(),
                  kicad_version=p.GetBuildVersion(), width_mm=.2, routes=routes,
                  added_tracks=16, tracks_and_vias=len(list(loaded.GetTracks())),
                  open_edges=loaded.GetConnectivity().GetUnconnectedCount(False))
    report['SPDX-License-Identifier'] = 'CERN-OHL-S-2.0'
    REPORT.write_text(json.dumps(report, indent=2, sort_keys=True)+'\n')
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
