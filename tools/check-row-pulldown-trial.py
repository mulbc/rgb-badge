#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Check the saved candidate row-select pulldowns and native DRC baseline."""

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
    board_path = STAGING / 'led-row-pulldown-trial-114mm.kicad_pcb'
    report = json.loads((ROOT / 'mechanical/review/row-pulldown-trial.json').read_text())
    assert hashlib.sha256(board_path.read_bytes()).hexdigest() == report['board_sha256']
    board = pcb.LoadBoard(str(board_path))
    connected = board.GetConnectivity()
    parts = {part.GetReference(): part for part in board.GetFootprints()}
    assert len(parts) == 483
    assert len(list(board.GetTracks())) == report['tracks_and_vias']
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
    route_status = {item['net']: item['connected'] for item in report['routes']}
    assert len(route_status) == 16
    completed = 0
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
        name = f'ROW_SEL_{row:02d}'
        select = next(pad for pad in pair.Pads() if pad.GetNetname() == name)
        decoder = next(pad for pad in parts['U2'].Pads()
                       if pad.GetNetname() == name)
        reached = decoder in connected.GetConnectedItems(select)
        assert reached, name
        completed += reached
    assert completed == 16
    pulldowns = 0
    for row in range(16):
        name = f'ROW_SEL_{row:02d}'
        ref = f'R{22+row}'
        resistor = next(pad for pad in parts[ref].Pads()
                        if pad.GetNetname() == name)
        decoder = next(pad for pad in parts['U2'].Pads()
                       if pad.GetNetname() == name)
        reached = decoder in connected.GetConnectedItems(resistor)
        assert reached == route_status[name], name
        pulldowns += reached
    assert pulldowns == report['connected_pulldowns'] == 15
    assert not route_status['ROW_SEL_02']
    baseline = ROOT / 'docs/development/led-colour-fanout-grid-drc-2026-10-19.json'
    assert colour.findings(args.drc) == colour.findings(baseline)
    assert len(colour.findings(args.drc)) == 104
    assert connected.GetUnconnectedCount(False) == report['open_edges'] == 535
    print('48 complete colour channels, 16 complete anode rows, '
          '16 gate ties, 16 decoder-to-pair selects, 15 select pulldowns; '
          '104 unchanged DRC findings.')


if __name__ == '__main__':
    main()
