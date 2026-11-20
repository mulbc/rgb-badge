#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Verify saved copper connectivity and unchanged intrinsic DRC findings."""

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path

import pcbnew as p

ROOT=Path(__file__).resolve().parents[1]
STAGING=ROOT/'hardware/coupon/rev-a/staging'
PIN_MAP=[(8,9,10),(11,12,13),(14,15,16),(17,18,19),
         (20,21,22),(23,24,25),(30,31,32),(33,34,35),
         (36,37,38),(39,40,41),(44,45,46),(47,48,49),
         (50,51,52),(53,54,55),(2,3,4),(5,6,7)]


def findings(path):
    report=json.loads(path.read_text())
    return Counter(json.dumps({
        'type':finding['type'],'description':finding['description'],
        'severity':finding['severity'],
        'items':sorted(({'description':item['description'],'pos':item['pos']}
                        for item in finding['items']),
                       key=lambda item:json.dumps(item,sort_keys=True))},sort_keys=True)
                   for finding in report['violations'])


def pads_in_cluster(connectivity,pad):
    return {(item.GetParentFootprint().GetReference(),item.GetNumber())
            for item in connectivity.GetConnectedItems(pad)
            if isinstance(item,p.PAD)}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--board',type=Path,default=STAGING/'led-colour-fanout-grid-trial-114mm.kicad_pcb')
    parser.add_argument('--manifest',type=Path,default=ROOT/'mechanical/review/colour-fanout-grid-trial.json')
    parser.add_argument('--drc',type=Path,required=True)
    args=parser.parse_args()
    board=p.LoadBoard(str(args.board));connectivity=board.GetConnectivity()
    parts={part.GetReference():part for part in board.GetFootprints()}
    assert len(parts)==483
    driver={pad.GetNumber():pad for pad in parts['U1'].Pads()}
    report=json.loads(args.manifest.read_text())
    assert hashlib.sha256(args.board.read_bytes()).hexdigest()==report['board_sha256']
    assert len(list(board.GetTracks()))==report['tracks_and_vias']
    routes={route['net']:route for route in report['routes']}
    completed=0
    for col,pins in enumerate(PIN_MAP):
        for colour,pin in zip('RGB',pins):
            name=f'COL_{col:02d}_{colour}';pad=driver[str(pin)]
            assert pad.GetNetname()==name
            expected={('U1',str(pin))}
            cathode=({'R':'2','B':'3','G':'4'} if col<8
                     else {'B':'2','G':'3','R':'4'})[colour]
            if routes[name]['connected']:
                expected.update((f'D{16*row+col+1}',cathode) for row in range(16))
                completed+=1
            actual=pads_in_cluster(connectivity,pad)
            assert actual==expected,(name,sorted(actual^expected))
    for row in range(16):
        pair=parts[f'PAIR{row+1:02d}']
        output=next(pad for pad in pair.Pads() if pad.GetNumber()=='3')
        assert output.GetNetname()==f'ROW_{row:02d}_A'
        expected={(f'D{16*row+col+1}','1') for col in range(16)}
        expected.add((pair.GetReference(),'3'))
        assert pads_in_cluster(connectivity,output)==expected,row
    baseline=ROOT/'docs/development/led-qt-uniform-2p2-row-bank-onsemi-drc-2026-10-16.json'
    assert findings(args.drc)==findings(baseline),'Native DRC findings changed'
    assert completed==report['connected_colours']
    assert completed==48,'The saved trial does not complete all 48 colour outputs'
    assert connectivity.GetUnconnectedCount(False)==report['open_edges']
    print(f'{completed}/48 colour drivers reach every one of their 16 LED cathodes; '
          'all 16 complete anode rows retained; exact 104 intrinsic DRC findings retained.')


if __name__=='__main__':
    main()
