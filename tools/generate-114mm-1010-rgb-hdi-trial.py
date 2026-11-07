#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Add 1010 red cathode trunks to the separate 114 mm front-row study."""

from pathlib import Path
import uuid

import pcbnew as pcb


ROOT = Path(__file__).resolve().parents[1]
STAGING = ROOT / 'hardware/coupon/rev-a/staging'
SOURCE = STAGING / 'led-1010-front-row-bus-trial-114mm.kicad_pcb'
RGB_OUTPUT = STAGING / 'led-1010-front-row-rgb-hdi-trial-114mm.kicad_pcb'
SCOPE = uuid.UUID('e097cda7-7f6e-49c2-ad31-fbfdd79301e0')


def set_id(item, name):
    item.SetUuid(pcb.KIID(str(uuid.uuid5(SCOPE, name))))


def add_colour(board, parts, colour, pad_number):
    for column in range(8):
        pads = []
        for row in range(16):
            ref = f'D{16*row+column+1}'
            assert parts[ref].GetValue() == 'EAST10105RGBA0'
            pad = next(pad for pad in parts[ref].Pads()
                       if pad.GetNumber() == pad_number)
            assert pad.GetNetname() == f'COL_{column:02d}_{colour}'
            pads.append(pad)
            via = pcb.PCB_VIA(board)
            via.SetPosition(pad.GetPosition())
            via.SetViaType(pcb.VIATYPE_MICROVIA)
            via.SetLayerPair(pcb.F_Cu, pcb.In1_Cu)
            via.SetWidth(pcb.FromMM(0.3))
            via.SetDrill(pcb.FromMM(0.1))
            via.SetNet(pad.GetNet())
            set_id(via, f'{colour}-{column:02d}-{row:02d}-via')
            board.Add(via)
        for row, (start, end) in enumerate(zip(pads, pads[1:])):
            segment = pcb.PCB_TRACK(board)
            segment.SetStart(start.GetPosition())
            segment.SetEnd(end.GetPosition())
            segment.SetWidth(pcb.FromMM(0.2))
            segment.SetLayer(pcb.In1_Cu)
            segment.SetNet(start.GetNet())
            set_id(segment, f'{colour}-{column:02d}-{row:02d}-segment')
            board.Add(segment)


def add_green(board, parts):
    """Use an offset stacked microvia to avoid red/blue on In1.Cu."""
    for column in range(8):
        ends = []
        for row in range(16):
            ref = f'D{16*row+column+1}'
            pad = next(pad for pad in parts[ref].Pads() if pad.GetNumber() == '4')
            assert pad.GetNetname() == f'COL_{column:02d}_G'
            pos = pad.GetPosition()
            end = pcb.VECTOR2I(pos.x-pcb.FromMM(0.55),
                               pos.y+pcb.FromMM(0.40))
            ends.append(end)
            stub = pcb.PCB_TRACK(board)
            stub.SetStart(pos)
            stub.SetEnd(end)
            stub.SetWidth(pcb.FromMM(0.2))
            stub.SetLayer(pcb.F_Cu)
            stub.SetNet(pad.GetNet())
            set_id(stub, f'green-{column:02d}-{row:02d}-stub')
            board.Add(stub)
            for start_layer, end_layer, suffix in (
                    (pcb.F_Cu, pcb.In1_Cu, 'top'),
                    (pcb.In1_Cu, pcb.In2_Cu, 'lower')):
                via = pcb.PCB_VIA(board)
                via.SetPosition(end)
                via.SetViaType(pcb.VIATYPE_MICROVIA)
                via.SetLayerPair(start_layer, end_layer)
                via.SetWidth(pcb.FromMM(0.3))
                via.SetDrill(pcb.FromMM(0.1))
                via.SetNet(pad.GetNet())
                set_id(via, f'green-{column:02d}-{row:02d}-{suffix}-via')
                board.Add(via)
        for row, (start, end) in enumerate(zip(ends, ends[1:])):
            segment = pcb.PCB_TRACK(board)
            segment.SetStart(start)
            segment.SetEnd(end)
            segment.SetWidth(pcb.FromMM(0.2))
            segment.SetLayer(pcb.In2_Cu)
            segment.SetNet(board.FindNet(f'COL_{column:02d}_G'))
            set_id(segment, f'green-{column:02d}-{row:02d}-segment')
            board.Add(segment)


def generate():
    board = pcb.LoadBoard(str(SOURCE))
    assert board.GetCopperLayerCount() == 6
    parts = {part.GetReference(): part for part in board.GetFootprints()}
    assert len(parts) == 483
    assert len(list(board.GetTracks())) == 144
    add_colour(board, parts, 'R', '2')
    assert len(list(board.GetTracks())) == 392
    add_colour(board, parts, 'B', '3')
    assert len(list(board.GetTracks())) == 640
    add_green(board, parts)
    assert len(list(board.GetTracks())) == 1144
    assert pcb.SaveBoard(str(RGB_OUTPUT), board)
    loaded = pcb.LoadBoard(str(RGB_OUTPUT))
    assert loaded.GetConnectivity().GetUnconnectedCount(False) == 1022
    print(f'{RGB_OUTPUT}: 144 row segments, 512 colour microvias, '
          '488 colour segments; 1022 open edges')


if __name__ == '__main__':
    generate()
