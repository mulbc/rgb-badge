#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Join both LED families' anode rows on a provisional inner layer."""

from pathlib import Path
import uuid

import pcbnew as pcb


ROOT = Path(__file__).resolve().parents[1]
STAGING = ROOT / 'hardware/coupon/rev-a/staging'
SOURCE = STAGING / 'led-1010-front-row-rgb-hdi-trial-114mm.kicad_pcb'
OUTPUT = STAGING / 'led-all-row-1010-rgb-hdi-trial-114mm.kicad_pcb'
SCOPE = uuid.UUID('74013f66-2534-48d2-9dda-0e2280cc9f38')


def stable_id(item, name):
    item.SetUuid(pcb.KIID(str(uuid.uuid5(SCOPE, name))))


def add_via_stack(board, position, net, name):
    for index, (top, bottom) in enumerate((
            (pcb.F_Cu, pcb.In1_Cu),
            (pcb.In1_Cu, pcb.In2_Cu),
            (pcb.In2_Cu, pcb.In3_Cu))):
        via = pcb.PCB_VIA(board)
        via.SetPosition(position)
        via.SetViaType(pcb.VIATYPE_MICROVIA)
        via.SetLayerPair(top, bottom)
        via.SetWidth(pcb.FromMM(0.3))
        via.SetDrill(pcb.FromMM(0.1))
        via.SetNet(net)
        stable_id(via, f'{name}-via-{index}')
        board.Add(via)


def add_track(board, start, end, layer, net, name):
    track = pcb.PCB_TRACK(board)
    track.SetStart(start)
    track.SetEnd(end)
    track.SetWidth(pcb.FromMM(0.2))
    track.SetLayer(layer)
    track.SetNet(net)
    stable_id(track, name)
    board.Add(track)


def generate():
    board = pcb.LoadBoard(str(SOURCE))
    assert board.GetCopperLayerCount() == 6
    parts = {part.GetReference(): part for part in board.GetFootprints()}
    assert len(parts) == 483
    assert len(list(board.GetTracks())) == 1144
    for row in range(16):
        net = board.FindNet(f'ROW_{row:02d}_A')
        pads = []
        positions = []
        for column in range(8, 16):
            ref = f'D{16*row+column+1}'
            assert parts[ref].GetValue() == 'QBLP1515A-RGB2A'
            pad = next(pad for pad in parts[ref].Pads()
                       if pad.GetNumber() == '1')
            assert pad.GetNetname() == f'ROW_{row:02d}_A'
            pads.append(pad)
            # Move within the same anode land to leave clearance for a
            # sloping red-column trunk on In1.Cu.
            via_position = pcb.VECTOR2I(
                pad.GetPosition().x+pcb.FromMM(0.05),
                pad.GetPosition().y)
            positions.append(via_position)
            add_via_stack(board, via_position, net,
                          f'row-{row:02d}-qt-{column:02d}')
        first_1010 = next(pad for pad in parts[f'D{16*row+1}'].Pads()
                          if pad.GetNumber() == '1')
        bus_y = first_1010.GetPosition().y-pcb.FromMM(0.55)
        left = pcb.VECTOR2I(pcb.FromMM(40.6), bus_y)
        bus_start = pcb.VECTOR2I(first_1010.GetPosition().x, bus_y)
        add_track(board, left, bus_start, pcb.F_Cu, net,
                  f'row-{row:02d}-front-left-extension')
        add_via_stack(board, left, net, f'row-{row:02d}-left-stack')
        add_track(board, left, positions[0], pcb.In3_Cu, net,
                  f'row-{row:02d}-inner-join')
        for column, (start, end) in enumerate(zip(positions, positions[1:])):
            add_track(board, start, end,
                      pcb.In3_Cu, net, f'row-{row:02d}-qt-{column:02d}')
    assert len(list(board.GetTracks())) == 1720
    assert pcb.SaveBoard(str(OUTPUT), board)
    loaded = pcb.LoadBoard(str(OUTPUT))
    assert loaded.GetConnectivity().GetUnconnectedCount(False) == 894
    print(f'{OUTPUT}: 894 open edges, 432 additional microvias and '
          '144 additional segments')


if __name__ == '__main__':
    generate()
