#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Connect the numbered candidate row-pair gate pads in the routing study."""

import hashlib
import importlib.util
import json
from pathlib import Path
import re
import uuid

import pcbnew as pcb


ROOT = Path(__file__).resolve().parents[1]
STAGING = ROOT / 'hardware/coupon/rev-a/staging'
SOURCE = STAGING / 'led-colour-fanout-grid-trial-114mm.kicad_pcb'
OUTPUT = STAGING / 'led-row-gate-tie-trial-114mm.kicad_pcb'
REPORT = ROOT / 'mechanical/review/row-gate-tie-trial.json'
SCOPE = uuid.UUID('36c3daa8-7b7b-4b68-9f2d-9bd10e221866')


def add_track(board, start, end, net, key):
    track = pcb.PCB_TRACK(board)
    track.SetStart(start)
    track.SetEnd(end)
    track.SetWidth(pcb.FromMM(0.2))
    track.SetLayer(pcb.B_Cu)
    track.SetNet(net)
    track.SetUuid(pcb.KIID(str(uuid.uuid5(SCOPE, key))))
    board.Add(track)


def main():
    board = pcb.LoadBoard(str(SOURCE))
    parts = {item.GetReference(): item for item in board.GetFootprints()}
    assert len(parts) == 483 and len(list(board.GetTracks())) == 6624
    for row in range(16):
        ref = f'PAIR{row+1:02d}'
        part = parts[ref]
        assert part.GetValue() == 'NTLJD3119CTBG_TRIAL_ONLY'
        gate = [pad for pad in part.Pads()
                if pad.GetNetname() == f'ROW_GATE_{row:02d}']
        assert sorted(pad.GetNumber() for pad in gate) == ['5', '6', '6']
        five = next(pad for pad in gate if pad.GetNumber() == '5')
        left_six = min((pad for pad in gate if pad.GetNumber() == '6'),
                       key=lambda pad: pad.GetPosition().x)
        island_six = max((pad for pad in gate if pad.GetNumber() == '6'),
                         key=lambda pad: pad.GetPosition().x)
        assert five.GetPosition().x == left_six.GetPosition().x
        add_track(board, five.GetPosition(), left_six.GetPosition(),
                  five.GetNet(), f'{ref}-5-to-6')
        add_track(board, left_six.GetPosition(), island_six.GetPosition(),
                  five.GetNet(), f'{ref}-6-to-island')
    pcb.SaveBoard(str(OUTPUT), board)
    spec = importlib.util.spec_from_file_location(
        'route_base', ROOT / 'tools/generate-paired-charger-114mm-routing.py')
    helper = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(helper)
    data = helper.sorted_native_tracks(
        OUTPUT.read_text(), expected=len(list(board.GetTracks())))
    sequence = iter(range(data.count('(uuid "')))
    data = re.sub(r'\(uuid "[0-9a-f-]{36}"\)',
                  lambda _: '(uuid "'+str(uuid.uuid5(SCOPE, str(next(sequence))))+'")',
                  data)
    OUTPUT.write_text(data)
    checked = pcb.LoadBoard(str(OUTPUT))
    connected = []
    for row in range(16):
        part = next(part for part in checked.GetFootprints()
                    if part.GetReference() == f'PAIR{row+1:02d}')
        pads = [pad for pad in part.Pads()
                if pad.GetNetname() == f'ROW_GATE_{row:02d}']
        cluster = checked.GetConnectivity().GetConnectedItems(pads[0])
        assert all(pad in cluster for pad in pads), row
        connected.append(row)
    report = {
        'SPDX-License-Identifier': 'CERN-OHL-S-2.0',
        'status': 'UNQUALIFIED_ROUTING_STUDY',
        'source_sha256': hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
        'board_sha256': hashlib.sha256(OUTPUT.read_bytes()).hexdigest(),
        'candidate_part': 'NTLJD3119CTBG_TRIAL_ONLY',
        'connected_local_gate_ties': len(connected),
        'tracks_and_vias': len(list(checked.GetTracks())),
        'open_edges': checked.GetConnectivity().GetUnconnectedCount(False),
    }
    REPORT.write_text(json.dumps(report, indent=2, sort_keys=True)+'\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
