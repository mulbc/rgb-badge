#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Give the unselected complete-matrix trial numbered onsemi row-pair pads."""

from pathlib import Path
import re
import uuid

import pcbnew as pcb


ROOT = Path(__file__).resolve().parents[1]
STAGING = ROOT / 'hardware/coupon/rev-a/staging'
SOURCE = STAGING / 'led-qt-uniform-2p2-matrix-trial-114mm.kicad_pcb'
OUTPUT = STAGING / 'led-qt-uniform-2p2-onsemi-row-trial-114mm.kicad_pcb'
LIBRARY = ROOT / 'hardware/coupon/rev-a/footprints/rgb-badge-coupon.pretty'
NAME = 'WDFN6_2x2_onsemi_NTLJD3119C'
SCOPE = uuid.UUID('96803346-b8ef-4bcd-99bd-788501988ac6')


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
    assert len(list(board.GetTracks())) == 2416
    row_pad = next(pad for pad in board.FindFootprintByReference('PAIR01').Pads()
                   if pad.GetNumber() == '3' and
                   abs(pcb.ToMM(pad.GetPosition().x)-104.175) < 0.001)
    assert row_pad.GetNetname() == 'ROW_00_A'
    row_net = row_pad.GetNet()
    escape = pcb.VECTOR2I(pcb.FromMM(104.5), pcb.FromMM(7.1))
    rear = pcb.PCB_TRACK(board)
    rear.SetStart(row_pad.GetPosition())
    rear.SetEnd(escape)
    rear.SetWidth(pcb.FromMM(0.2))
    rear.SetLayer(pcb.B_Cu)
    rear.SetNet(row_net)
    rear.SetUuid(pcb.KIID(str(uuid.uuid5(SCOPE, 'ROW_00_A/rear'))))
    board.Add(rear)
    via = pcb.PCB_VIA(board)
    via.SetPosition(escape)
    via.SetViaType(pcb.VIATYPE_THROUGH)
    via.SetLayerPair(pcb.F_Cu, pcb.B_Cu)
    via.SetWidth(pcb.FromMM(0.5))
    via.SetDrill(pcb.FromMM(0.3))
    via.SetNet(row_net)
    via.SetUuid(pcb.KIID(str(uuid.uuid5(SCOPE, 'ROW_00_A/via'))))
    board.Add(via)
    inner = pcb.PCB_TRACK(board)
    inner.SetStart(pcb.VECTOR2I(pcb.FromMM(74.7), pcb.FromMM(2.6)))
    inner.SetEnd(escape)
    inner.SetWidth(pcb.FromMM(0.2))
    inner.SetLayer(pcb.In3_Cu)
    inner.SetNet(row_net)
    inner.SetUuid(pcb.KIID(str(uuid.uuid5(SCOPE, 'ROW_00_A/inner'))))
    board.Add(inner)
    assert len(list(board.GetTracks())) == 2419
    pcb.SaveBoard(str(OUTPUT), board)
    contents = OUTPUT.read_text()
    serial = iter(range(contents.count('(uuid "')))
    contents = re.sub(r'\(uuid "[0-9a-f-]{36}"\)',
                      lambda _: '(uuid "' + str(uuid.uuid5(SCOPE, str(next(serial)))) + '")',
                      contents)
    OUTPUT.write_text(contents)
    loaded = pcb.LoadBoard(str(OUTPUT))
    assert loaded.GetConnectivity().GetUnconnectedCount(False) == 661
    print(f'{OUTPUT}: 16 onsemi pairs with assigned pads; '
          'ROW_00_A joins the matrix; 661 open edges; root schematic unchanged')


if __name__ == '__main__':
    generate()
