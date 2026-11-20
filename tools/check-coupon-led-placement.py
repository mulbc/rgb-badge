#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Inspect saved KiCad coupon trials against the accepted LED placement contract."""

import sys
from pathlib import Path

import pcbnew as pcb


def check(board_path: Path) -> None:
    board = pcb.LoadBoard(str(board_path))
    parts = {part.GetReference(): part for part in board.GetFootprints()}
    assert all(f'D{index}' in parts for index in range(1, 257))
    origin = parts['D1'].GetPosition()
    expected_qt_origin_x = origin.x + pcb.FromMM(8 * 1.95)
    for row in range(16):
        for col in range(16):
            part = parts[f'D{16 * row + col + 1}']
            position = part.GetPosition()
            x = (origin.x + pcb.FromMM(col * 1.95) if col < 8
                 else expected_qt_origin_x + pcb.FromMM((col - 8) * 2.2))
            y = origin.y + pcb.FromMM(row * 1.95)
            assert (position.x, position.y) == (x, y), (part.GetReference(), position)
            assert part.GetOrientationDegrees() == 0, part.GetReference()
            pads = {pad.GetNumber(): pad for pad in part.Pads()}
            assert set(pads) == {'1', '2', '3', '4'}, part.GetReference()
            if col < 8:
                assert part.GetFPID().GetLibItemName() == 'LED_Everlight_EAST10105RGBA0'
                cathode_map = [('2', 'R'), ('3', 'B'), ('4', 'G')]
            else:
                assert part.GetFPID().GetLibItemName() == 'LED_QTBrightek_QBLP1515A-RGB2A'
                assert all((pad.GetSize().x, pad.GetSize().y) ==
                           (pcb.FromMM(0.6), pcb.FromMM(0.4))
                           for pad in pads.values()), part.GetReference()
                cathode_map = [('2', 'B'), ('3', 'G'), ('4', 'R')]
            assert pads['1'].GetNetname() == f'ROW_{row:02d}_A'
            for number, colour in cathode_map:
                assert pads[number].GetNetname() == f'COL_{col:02d}_{colour}'
    print(f'{board_path}: 256 exact LED placements, rotations, pad maps and nets passed')


if __name__ == '__main__':
    assert len(sys.argv) > 1, 'Pass at least one saved KiCad PCB'
    for name in sys.argv[1:]:
        check(Path(name))
