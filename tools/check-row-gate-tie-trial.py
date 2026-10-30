#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Check saved colour, anode and gate copper against native KiCad DRC."""

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path

import pcbnew as pcb


ROOT = Path(__file__).resolve().parents[1]
STAGING = ROOT / 'hardware/coupon/rev-a/staging'
SPEC = importlib.util.spec_from_file_location(
    'colour_check', ROOT / 'tools/check-colour-fanout-trial.py')
colour = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(colour)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--drc', required=True, type=Path)
    args = parser.parse_args()
    board_path = STAGING / 'led-row-gate-tie-trial-114mm.kicad_pcb'
    report = json.loads((ROOT / 'mechanical/review/row-gate-tie-trial.json').read_text())
    assert hashlib.sha256(board_path.read_bytes()).hexdigest() == report['board_sha256']
    board = pcb.LoadBoard(str(board_path))
    connected = board.GetConnectivity()
    parts = {part.GetReference(): part for part in board.GetFootprints()}
    assert len(parts) == 483
    assert len(list(board.GetTracks())) == report['tracks_and_vias'] == 6656
    driver_pads = {pad.GetNumber(): pad for pad in parts['U1'].Pads()}
    for column, pins in enumerate(colour.PIN_MAP):
        for name, pin in zip('RGB', pins):
            net = f'COL_{column:02d}_{name}'
            pad = driver_pads[str(pin)]
            assert pad.GetNetname() == net
            cathode = ({'R': '2', 'B': '3', 'G': '4'} if column < 8
                       else {'B': '2', 'G': '3', 'R': '4'})[name]
            expected = {('U1', str(pin))}
            expected.update((f'D{16*row+column+1}', cathode)
                            for row in range(16))
            assert colour.pads_in_cluster(connected, pad) == expected, net
    for row in range(16):
        ref = f'PAIR{row+1:02d}'
        pair = parts[ref]
        assert pair.GetValue() == 'NTLJD3119CTBG_TRIAL_ONLY'
        output = next(pad for pad in pair.Pads() if pad.GetNumber() == '3')
        expected = {(f'D{16*row+column+1}', '1') for column in range(16)}
        expected.add((ref, '3'))
        assert colour.pads_in_cluster(connected, output) == expected, row
        gates = [pad for pad in pair.Pads()
                 if pad.GetNetname() == f'ROW_GATE_{row:02d}']
        assert sorted(pad.GetNumber() for pad in gates) == ['5', '6', '6']
        cluster = connected.GetConnectedItems(gates[0])
        assert all(pad in cluster for pad in gates), row
    baseline = ROOT / 'docs/development/led-colour-fanout-grid-drc-2026-10-19.json'
    assert colour.findings(args.drc) == colour.findings(baseline)
    assert len(colour.findings(args.drc)) == 104
    assert connected.GetUnconnectedCount(False) == report['open_edges'] == 566
    print('48 complete colour channels, 16 complete anode rows, '
          '16 local gate ties; 104 unchanged intrinsic DRC findings.')


if __name__ == '__main__':
    main()
