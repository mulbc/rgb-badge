#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Replace netless Diodes pair boxes with separately netted onsemi trial pads."""

from pathlib import Path
import re
import uuid

import pcbnew as pcb


ROOT = Path(__file__).resolve().parents[1]
STAGING = ROOT / 'hardware/coupon/rev-a/staging'
SOURCE = STAGING / 'paired-charger-local-routing-trial-114mm.kicad_pcb'
OUTPUT = STAGING / 'onsemi-row-placement-trial-114mm.kicad_pcb'
LIBRARY = ROOT / 'hardware/coupon/rev-a/footprints/rgb-badge-coupon.pretty'
NAME = 'WDFN6_2x2_onsemi_NTLJD3119C'
SCOPE = uuid.UUID('25bdbcc6-9fd8-4b5a-8400-d895a67e02e2')


def generate():
    board = pcb.LoadBoard(str(SOURCE))
    originals = {part.GetReference(): part for part in board.GetFootprints()}
    assert len(originals) == 483
    for index in range(1, 17):
        ref = f'PAIR{index:02d}'
        old = originals[ref]
        assert old.GetValue() == 'DMC1229UFDB-7_GEOMETRY_ONLY'
        assert all(not pad.GetNetname() for pad in old.Pads())
        position, angle, flipped = old.GetPosition(), old.GetOrientationDegrees(), old.IsFlipped()
        board.Delete(old)
        part = pcb.FootprintLoad(str(LIBRARY), NAME)
        part.SetFPID(pcb.LIB_ID('rgb-badge-coupon', NAME))
        part.SetReference(ref)
        part.SetValue('NTLJD3119CTBG_TRIAL_ONLY')
        part.Reference().SetVisible(False)
        part.Value().SetVisible(False)
        board.Add(part)
        part.SetPosition(position)
        if flipped:
            part.Flip(position, False)
        part.SetOrientationDegrees(angle)
        part.SetUuid(pcb.KIID(str(uuid.uuid5(SCOPE, ref))))
        # N drain (pin 6) sinks P gate (pin 5) through the external row node.
        nets = {'1': 'GND', '2': f'ROW_SEL_{index-1:02d}',
                '3': f'ROW_{index-1:02d}_A', '4': 'VLED',
                '5': f'ROW_GATE_{index-1:02d}',
                '6': f'ROW_GATE_{index-1:02d}'}
        seen = {}
        for pad in part.Pads():
            number = pad.GetNumber()
            ordinal = seen.get(number, 0)
            seen[number] = ordinal + 1
            pad.SetNet(board.FindNet(nets[number]))
            pad.SetUuid(pcb.KIID(str(uuid.uuid5(SCOPE, f'{ref}/pad/{number}/{ordinal}'))))
        assert seen == {'1': 1, '2': 1, '3': 2, '4': 1, '5': 1, '6': 2}, (ref, seen)
    assert len(list(board.GetFootprints())) == 483
    assert len(list(board.GetTracks())) == 162
    pcb.SaveBoard(str(OUTPUT), board)
    contents = OUTPUT.read_text()
    serial = iter(range(contents.count('(uuid "')))
    contents = re.sub(r'\(uuid "[0-9a-f-]{36}"\)',
                      lambda _: '(uuid "' + str(uuid.uuid5(SCOPE, str(next(serial)))) + '")',
                      contents)
    OUTPUT.write_text(contents)
    print(f'{OUTPUT}: 16 onsemi pairs with assigned pads; root schematic is unchanged')


if __name__ == '__main__':
    generate()
