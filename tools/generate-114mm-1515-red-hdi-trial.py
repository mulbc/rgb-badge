#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Add red QT Brightek column trunks to the separate all-row trial."""

from pathlib import Path
import uuid

import pcbnew as pcb


ROOT = Path(__file__).resolve().parents[1]
STAGING = ROOT / 'hardware/coupon/rev-a/staging'
SOURCE = STAGING / 'led-all-row-1010-rgb-hdi-trial-114mm.kicad_pcb'
OUTPUT = STAGING / 'led-all-row-1010-rgb-1515-red-hdi-trial-114mm.kicad_pcb'
SCOPE = uuid.UUID('5dd85011-4595-4dd0-88ef-6628a74cdcf0')


def stable_id(item, name):
    item.SetUuid(pcb.KIID(str(uuid.uuid5(SCOPE, name))))


def generate():
    board = pcb.LoadBoard(str(SOURCE))
    assert board.GetCopperLayerCount() == 6
    parts = {part.GetReference(): part for part in board.GetFootprints()}
    assert len(parts) == 483
    assert len(list(board.GetTracks())) == 1720
    for column in range(8, 16):
        pads = []
        for row in range(16):
            ref = f'D{16*row+column+1}'
            pad = next(pad for pad in parts[ref].Pads()
                       if pad.GetNumber() == '4')
            assert pad.GetNetname() == f'COL_{column:02d}_R'
            pads.append(pad)
            via = pcb.PCB_VIA(board)
            via.SetPosition(pad.GetPosition())
            via.SetViaType(pcb.VIATYPE_MICROVIA)
            via.SetLayerPair(pcb.F_Cu, pcb.In1_Cu)
            via.SetWidth(pcb.FromMM(0.3))
            via.SetDrill(pcb.FromMM(0.1))
            via.SetNet(pad.GetNet())
            stable_id(via, f'qt-red-{column:02d}-{row:02d}-via')
            board.Add(via)
        for row, (start, end) in enumerate(zip(pads, pads[1:])):
            segment = pcb.PCB_TRACK(board)
            segment.SetStart(start.GetPosition())
            segment.SetEnd(end.GetPosition())
            segment.SetWidth(pcb.FromMM(0.2))
            segment.SetLayer(pcb.In1_Cu)
            segment.SetNet(start.GetNet())
            stable_id(segment, f'qt-red-{column:02d}-{row:02d}-segment')
            board.Add(segment)
    assert len(list(board.GetTracks())) == 1968
    assert pcb.SaveBoard(str(OUTPUT), board)
    loaded = pcb.LoadBoard(str(OUTPUT))
    assert loaded.GetConnectivity().GetUnconnectedCount(False) == 774
    print(f'{OUTPUT}: 128 red microvias, 120 red segments, 774 open edges')


if __name__ == '__main__':
    generate()
