#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Probe a USB-to-charger copper path on the 114 mm placement-only board."""

import importlib.util
from pathlib import Path
import re
import uuid

import pcbnew as pcb


ROOT = Path(__file__).resolve().parents[1]
STAGING = ROOT / 'hardware/coupon/rev-a/staging'
SOURCE = STAGING / 'paired-charger-placement-only-114mm.kicad_pcb'
OUTPUT = STAGING / 'paired-charger-local-routing-trial-114mm.kicad_pcb'
SCOPE = uuid.UUID('4e64503b-3ef7-5a2c-8ea4-e8b770154d44')


def point(x, y):
    return pcb.VECTOR2I(pcb.FromMM(x), pcb.FromMM(y))


def add_segment(board, start, end, layer, net, width=0.2):
    track = pcb.PCB_TRACK(board)
    track.SetStart(start)
    track.SetEnd(end)
    track.SetWidth(pcb.FromMM(width))
    track.SetLayer(layer)
    track.SetNet(net)
    board.Add(track)


def add_through_via(board, position, net):
    via = pcb.PCB_VIA(board)
    via.SetPosition(position)
    via.SetViaType(pcb.VIATYPE_THROUGH)
    via.SetLayerPair(pcb.F_Cu, pcb.B_Cu)
    via.SetWidth(pcb.FromMM(0.6))
    via.SetDrill(pcb.FromMM(0.3))
    via.SetNet(net)
    board.Add(via)


def sorted_native_tracks(contents):
    pattern = r'\n\t\((?:segment|via)(?=\s)'
    starts = [match.start() for match in re.finditer(pattern, contents)]
    assert len(starts) == 129
    blocks = []
    for start in starts:
        depth = 0
        quoted = escaped = False
        for pos in range(start + 2, len(contents)):
            char = contents[pos]
            if quoted:
                if escaped:
                    escaped = False
                elif char == '\\':
                    escaped = True
                elif char == '"':
                    quoted = False
            elif char == '"':
                quoted = True
            elif char == '(':
                depth += 1
            elif char == ')':
                depth -= 1
                if depth == 0:
                    blocks.append((start, pos+1, contents[start:pos+1]))
                    break
        else:
            raise ValueError('Unclosed track/via in native board export')
    ordered = sorted((block[2] for block in blocks),
                     key=lambda block: re.sub(r'\(uuid "[0-9a-f-]{36}"\)', '', block))
    return contents[:blocks[0][0]] + ''.join(ordered) + contents[blocks[-1][1]:]


def generate():
    board = pcb.LoadBoard(str(SOURCE))
    assert not list(board.GetTracks())
    parts = {part.GetReference(): part for part in board.GetFootprints()}
    def pad(ref, number, net):
        matches = [item for item in parts[ref].Pads()
                   if item.GetNumber() == str(number) and item.GetNetname() == net]
        assert len(matches) == 1, (ref, number, net)
        return matches[0]
    def connect(start, end, bends):
        assert start.GetNetname() == end.GetNetname()
        positions = [start.GetPosition()] + [point(*xy) for xy in bends] + [end.GetPosition()]
        for first, second in zip(positions, positions[1:]):
            add_segment(board, first, second, pcb.B_Cu, start.GetNet())

    connect(pad('C53', 1, '+BAT_PROTECTED_DRAFT'),
            pad('U41', 2, '+BAT_PROTECTED_DRAFT'),
            [(105.5, 24.75), (106.25, 25.5)])
    connect(pad('R92', 1, 'CHARGER_ISET'), pad('U41', 16, 'CHARGER_ISET'),
            [(105.4, 28.5), (105.4, 27.6), (106.0, 27.0)])
    connect(pad('C56', 1, 'CHARGER_IN_DRAFT'), pad('U41', 13, 'CHARGER_IN_DRAFT'),
            [(109.0, 28.3)])
    connect(pad('R93', 1, 'CHARGER_ILIM'), pad('U41', 12, 'CHARGER_ILIM'),
            [(111.9, 27.9), (111.9, 26.0)])

    cap = pad('C54', 1, '+SYS_APP_IN_DRAFT')
    charger = pad('U41', 10, '+SYS_APP_IN_DRAFT')
    first, second = point(105.3, 26.0), point(110.5, 25.0)
    for position in (first, second):
        add_through_via(board, position, cap.GetNet())
    for start, end, layer in ((cap.GetPosition(), first, pcb.B_Cu),
                              (first, point(110.0, 25.5), pcb.In3_Cu),
                              (point(110.0, 25.5), second, pcb.In3_Cu),
                              (second, charger.GetPosition(), pcb.B_Cu)):
        add_segment(board, start, end, layer, cap.GetNet())

    gate = pad('U44', 6, 'CHARGER_IN_DRAFT')
    input_cap = pad('C52', 1, 'CHARGER_IN_DRAFT')
    assert gate.GetNetname() == input_cap.GetNetname() == pad('U41', 13, 'CHARGER_IN_DRAFT').GetNetname()
    gate_via = point(100.7, 20.8)
    cap_via = point(105.5, 19.0)
    input_via = point(109.5, 27.5)
    for position in (gate_via, cap_via, input_via):
        add_through_via(board, position, gate.GetNet())
    for start, end, layer in ((gate.GetPosition(), point(100.5, 20.5), pcb.B_Cu),
                              (point(100.5, 20.5), gate_via, pcb.B_Cu),
                              (gate_via, point(103.7, 20.8), pcb.In4_Cu),
                              (point(103.7, 20.8), cap_via, pcb.In4_Cu),
                              (cap_via, input_cap.GetPosition(), pcb.B_Cu),
                              (cap_via, point(105.5, 23.5), pcb.In4_Cu),
                              (point(105.5, 23.5), input_via, pcb.In4_Cu),
                              (input_via, point(109.0, 27.5), pcb.B_Cu)):
        add_segment(board, start, end, layer, gate.GetNet())

    e0_out = pad('U45', 6, '+5V_USB')
    e1_in = pad('U44', 5, '+5V_USB')
    usb_cap = pad('C61', 1, '+5V_USB')
    usb_first, usb_second = point(100.5, 17.0), point(105.55, 16.8)
    for position in (usb_first, usb_second):
        add_through_via(board, position, e0_out.GetNet())
    for start, end, layer in ((e0_out.GetPosition(), usb_first, pcb.B_Cu),
                              (usb_first, point(105.35, 17.0), pcb.In4_Cu),
                              (point(105.35, 17.0), usb_second, pcb.In4_Cu),
                              (usb_second, usb_cap.GetPosition(), pcb.B_Cu),
                              (e1_in.GetPosition(), point(101.0, 17.5), pcb.B_Cu),
                              (point(101.0, 17.5), usb_first, pcb.B_Cu)):
        add_segment(board, start, end, layer, e0_out.GetNet())

    e0_in = pad('U45', 5, 'VBUS_CONNECTOR')
    connector_a = pad('J1', 'B4_A9', 'VBUS_CONNECTOR')
    connector_b = pad('J1', 'A4_B9', 'VBUS_CONNECTOR')
    connector_cap = pad('C60', 1, 'VBUS_CONNECTOR')
    vbus_first, vbus_second = point(101.0, 12.5), point(105.2, 13.2)
    vbus_third = point(107.2, 18.65)
    for position in (vbus_first, vbus_second, vbus_third):
        add_through_via(board, position, e0_in.GetNet())
    for start, end, layer in ((e0_in.GetPosition(), vbus_first, pcb.B_Cu),
                              (vbus_first, point(104.5, 12.5), pcb.In4_Cu),
                              (point(104.5, 12.5), vbus_second, pcb.In4_Cu),
                              (vbus_second, connector_cap.GetPosition(), pcb.B_Cu),
                              (vbus_second, point(105.85, 13.85), pcb.F_Cu),
                              (point(105.85, 13.85), connector_a.GetPosition(), pcb.F_Cu),
                              (connector_b.GetPosition(), vbus_third, pcb.F_Cu),
                              (vbus_third, point(107.2, 15.2), pcb.In4_Cu),
                              (point(107.2, 15.2), vbus_second, pcb.In4_Cu)):
        add_segment(board, start, end, layer, e0_in.GetNet())

    ground = pad('C60', 2, 'GND').GetNet()
    def ground_path(start, end, layer):
        add_segment(board, start, end, layer, ground)
    input_ground = pad('C60', 2, 'GND')
    connector_ground = pad('J1', 'B1_A12', 'GND')
    ground_cap_via, ground_jack_via = point(103.8, 13.5), point(107.5, 12.3)
    for position in (ground_cap_via, ground_jack_via):
        add_through_via(board, position, ground)
    for start, end, layer in ((input_ground.GetPosition(), ground_cap_via, pcb.B_Cu),
                              (ground_cap_via, point(105.2, 15.0), pcb.In3_Cu),
                              (point(105.2, 15.0), ground_jack_via, pcb.In3_Cu),
                              (ground_jack_via, connector_ground.GetPosition(), pcb.F_Cu)):
        ground_path(start, end, layer)
    gate_ground = pad('C52', 2, 'GND')
    gate_ground_via = point(103.1, 19.0)
    add_through_via(board, gate_ground_via, ground)
    ground_path(gate_ground.GetPosition(), gate_ground_via, pcb.B_Cu)
    ground_path(gate_ground_via, ground_cap_via, pcb.In3_Cu)
    charger_ground = pad('U41', 4, 'GND')
    charger_ground_via = point(106.8, 23.1)
    add_through_via(board, charger_ground_via, ground)
    ground_path(charger_ground.GetPosition(), charger_ground_via, pcb.B_Cu)
    ground_path(charger_ground_via, gate_ground_via, pcb.In3_Cu)

    for first, second in ((pad('C53', 2, 'GND'), pad('C54', 2, 'GND')),
                          (pad('C54', 2, 'GND'), pad('R92', 2, 'GND'))):
        ground_path(first.GetPosition(), second.GetPosition(), pcb.B_Cu)
    resistor_ground = pad('R92', 2, 'GND')
    resistor_ground_via = point(103.0, 28.5)
    add_through_via(board, resistor_ground_via, ground)
    ground_path(resistor_ground.GetPosition(), resistor_ground_via, pcb.B_Cu)
    ground_path(resistor_ground_via, point(103.0, 23.1), pcb.In2_Cu)
    ground_path(point(103.0, 23.1), charger_ground_via, pcb.In2_Cu)
    input_bulk_ground = pad('C56', 2, 'GND')
    input_bulk_via = point(106.25, 29.5)
    add_through_via(board, input_bulk_via, ground)
    ground_path(input_bulk_ground.GetPosition(), input_bulk_via, pcb.B_Cu)
    ground_path(input_bulk_via, resistor_ground_via, pcb.In2_Cu)
    ilim_ground = pad('R93', 2, 'GND')
    ilim_ground_via = point(110.75, 28.25)
    add_through_via(board, ilim_ground_via, ground)
    ground_path(ilim_ground.GetPosition(), ilim_ground_via, pcb.B_Cu)
    ground_path(ilim_ground_via, input_bulk_via, pcb.In2_Cu)

    other_connector_ground = pad('J1', 'A1_B12', 'GND')
    other_ground_via = point(106.2, 20.0)
    add_through_via(board, other_ground_via, ground)
    for start, end, layer in ((other_connector_ground.GetPosition(), point(107.2, 19.45), pcb.F_Cu),
                              (point(107.2, 19.45), other_ground_via, pcb.F_Cu),
                              (other_ground_via, point(104.0, 20.0), pcb.In3_Cu),
                              (point(104.0, 20.0), gate_ground_via, pcb.In3_Cu)):
        ground_path(start, end, layer)
    efuse_ground = pad('U44', 2, 'GND')
    ground_path(efuse_ground.GetPosition(), point(102.2, 18.775), pcb.B_Cu)
    ground_path(point(102.2, 18.775), gate_ground_via, pcb.B_Cu)

    # Continue the local return network on the trial board. Each branch is
    # checked against the native DRC before being retained in this study.
    c61_ground = pad('C61', 2, 'GND')
    c61_via = point(103.7, 15.45)
    add_through_via(board, c61_via, ground)
    ground_path(c61_ground.GetPosition(), c61_via, pcb.B_Cu)
    ground_path(c61_via, ground_cap_via, pcb.In3_Cu)

    e0_ground = pad('U45', 8, 'GND')
    e0_ground_via = point(96.0, 15.225)
    add_through_via(board, e0_ground_via, ground)
    ground_path(e0_ground.GetPosition(), e0_ground_via, pcb.B_Cu)
    ground_path(e0_ground_via, c61_via, pcb.In3_Cu)

    e1_ground = pad('U44', 8, 'GND')
    e1_ground_via = point(99.0, 19.225)
    add_through_via(board, e1_ground_via, ground)
    ground_path(e1_ground.GetPosition(), e1_ground_via, pcb.B_Cu)
    ground_path(e1_ground_via, gate_ground_via, pcb.In3_Cu)

    c62_ground = pad('C62', 2, 'GND')
    c62_via = point(96.85, 15.3)
    add_through_via(board, c62_via, ground)
    ground_path(c62_ground.GetPosition(), c62_via, pcb.B_Cu)
    ground_path(c62_via, e0_ground_via, pcb.In3_Cu)

    c57_ground = pad('C57', 2, 'GND')
    c57_via = point(96.85, 19.6)
    add_through_via(board, c57_via, ground)
    ground_path(c57_ground.GetPosition(), c57_via, pcb.B_Cu)
    ground_path(c57_via, e1_ground_via, pcb.In3_Cu)

    for number, via_x in ((6, 108.0), (8, 109.0)):
        charger_pad = pad('U41', number, 'GND')
        local_via = point(via_x, 23.1)
        add_through_via(board, local_via, ground)
        ground_path(charger_pad.GetPosition(), local_via, pcb.B_Cu)
        ground_path(local_via, charger_ground_via, pcb.In2_Cu)

    def side_pad(ref, number, net):
        matches = [item for item in parts[ref].Pads()
                   if item.GetNumber() == str(number) and item.GetNetname() == net]
        assert len(matches) == 2, (ref, number, net)
        return max(matches, key=lambda item: item.GetPosition().x)

    connect(pad('C62', 1, 'E0_DVDT'), side_pad('U45', 7, 'E0_DVDT'), [])
    connect(pad('C57', 1, 'E1_DVDT'), side_pad('U44', 7, 'E1_DVDT'),
            [(97.65, 20.0), (100.025, 20.0)])
    connect(pad('R100', 1, 'E0_ILM'), pad('U45', 9, 'E0_ILM'),
            [(97.75, 14.775)])
    ground_path(pad('R100', 2, 'GND').GetPosition(), e0_ground_via, pcb.B_Cu)
    ground_path(pad('R96', 2, 'GND').GetPosition(),
                pad('R98', 2, 'GND').GetPosition(), pcb.B_Cu)
    ground_path(pad('R98', 2, 'GND').GetPosition(), c57_via, pcb.B_Cu)
    ovlo = pad('R97', 2, 'E0_OVLO').GetNet()
    ovlo_divider_via = point(95.9, 17.5)
    ovlo_low_via = point(98.6, 20.75)
    ovlo_ic_via = point(102.5, 14.775)
    for position in (ovlo_divider_via, ovlo_low_via, ovlo_ic_via):
        add_through_via(board, position, ovlo)
    for start, end, layer in (
        (pad('R97', 2, 'E0_OVLO').GetPosition(), ovlo_divider_via, pcb.B_Cu),
        (pad('R98', 1, 'E0_OVLO').GetPosition(), ovlo_low_via, pcb.B_Cu),
        (pad('U45', 2, 'E0_OVLO').GetPosition(), ovlo_ic_via, pcb.B_Cu),
        (ovlo_low_via, ovlo_divider_via, pcb.In2_Cu),
        (ovlo_divider_via, ovlo_ic_via, pcb.In2_Cu),
    ):
        add_segment(board, start, end, layer, ovlo)
    e0_enable = pad('R99', 2, 'E0_EN').GetNet()
    enable_resistor_via = point(95.9, 12.0)
    enable_ic_via = point(102.5, 13.4)
    for position in (enable_resistor_via, enable_ic_via):
        add_through_via(board, position, e0_enable)
    for start, end, layer in (
        (pad('R99', 2, 'E0_EN').GetPosition(), enable_resistor_via, pcb.B_Cu),
        (enable_resistor_via, point(100.0, 11.5), pcb.In2_Cu),
        (point(100.0, 11.5), point(102.5, 11.5), pcb.In2_Cu),
        (point(102.5, 11.5), enable_ic_via, pcb.In2_Cu),
        (enable_ic_via, side_pad('U45', 1, 'E0_EN').GetPosition(), pcb.B_Cu),
    ):
        add_segment(board, start, end, layer, e0_enable)
    vbus = pad('R99', 1, 'VBUS_CONNECTOR').GetNet()
    ovlo_supply_via = point(98.5, 17.5)
    add_through_via(board, ovlo_supply_via, vbus)
    for start, end, layer in (
        (pad('R99', 1, 'VBUS_CONNECTOR').GetPosition(), vbus_first, pcb.B_Cu),
        (pad('R97', 1, 'VBUS_CONNECTOR').GetPosition(), ovlo_supply_via, pcb.B_Cu),
        (ovlo_supply_via, vbus_first, pcb.In4_Cu),
    ):
        add_segment(board, start, end, layer, vbus)
    assert len(list(board.GetTracks())) == 129
    pcb.SaveBoard(str(OUTPUT), board)
    contents = sorted_native_tracks(OUTPUT.read_text())
    serial = iter(range(contents.count('(uuid "')))
    contents = re.sub(r'\(uuid "[0-9a-f-]{36}"\)',
                      lambda _: '(uuid "' + str(uuid.uuid5(SCOPE, str(next(serial)))) + '")',
                      contents)
    OUTPUT.write_text(contents)
    print(f'{OUTPUT}: 98 trace segments, 31 through vias; staged USB rails and local ground returns')


if __name__ == '__main__':
    generate()
