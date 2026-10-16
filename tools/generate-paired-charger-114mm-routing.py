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
    assert len(starts) == 339
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
    battery = pad('J2', 1, '+BAT_PROTECTED_DRAFT').GetNet()
    battery_header_via = point(27.0, 3.0)
    battery_charger_via = point(105.5, 24.75)
    for position in (battery_header_via, battery_charger_via):
        add_through_via(board, position, battery)
    add_segment(board, pad('J2', 1, '+BAT_PROTECTED_DRAFT').GetPosition(),
                battery_header_via, pcb.B_Cu, battery)
    add_segment(board, battery_header_via, battery_charger_via, pcb.In1_Cu, battery,
                width=0.5)
    battery_switch_via = point(6.5, 4.8)
    add_through_via(board, battery_switch_via, battery)
    add_segment(board, pad('SW2', 5, '+BAT_PROTECTED_DRAFT').GetPosition(),
                battery_switch_via, pcb.B_Cu, battery)
    add_segment(board, battery_switch_via, battery_header_via, pcb.In1_Cu, battery,
                width=0.5)
    battery_ground_via = point(22.5, 1.8)
    add_through_via(board, battery_ground_via, ground)
    ground_path(pad('J2', 2, 'GND').GetPosition(), battery_ground_via, pcb.B_Cu)
    add_segment(board, battery_ground_via, point(30.0, 1.8), pcb.In2_Cu,
                ground, width=0.5)
    add_segment(board, point(30.0, 1.8), resistor_ground_via, pcb.In2_Cu,
                ground, width=0.5)
    connect(pad('U41', 17, 'GND'), pad('U41', 6, 'GND'), [])
    connect(pad('U41', 3, '+BAT_PROTECTED_DRAFT'),
            pad('U41', 2, '+BAT_PROTECTED_DRAFT'), [])
    connect(pad('U41', 11, '+SYS_APP_IN_DRAFT'),
            pad('U41', 10, '+SYS_APP_IN_DRAFT'), [])
    sys_rail = pad('SW2', 2, '+SYS_APP_IN_DRAFT').GetNet()
    sys_switch_via = point(6.5, 1.4)
    add_through_via(board, sys_switch_via, sys_rail)
    add_segment(board, pad('SW2', 2, '+SYS_APP_IN_DRAFT').GetPosition(),
                sys_switch_via, pcb.B_Cu, sys_rail)
    add_segment(board, sys_switch_via, point(105.3, 26.0), pcb.In3_Cu, sys_rail,
                width=0.5)
    shell_pads = sorted((item for item in parts['J1'].Pads()
                         if item.GetNumber() == 'S1' and item.GetNetname() == 'GND'),
                        key=lambda item: (item.GetPosition().y, item.GetPosition().x))
    assert len(shell_pads) == 4
    ground_path(shell_pads[0].GetPosition(), shell_pads[1].GetPosition(), pcb.In3_Cu)
    ground_path(shell_pads[0].GetPosition(), ground_jack_via, pcb.In3_Cu)
    ground_path(shell_pads[2].GetPosition(), shell_pads[3].GetPosition(), pcb.In2_Cu)
    ground_path(shell_pads[2].GetPosition(), charger_ground_via, pcb.In2_Cu)
    e1_ilm = pad('R96', 1, 'E1_ILM').GetNet()
    ilm_resistor_via, ilm_ic_via = point(98.5, 25.5), point(98.5, 18.4)
    for position in (ilm_resistor_via, ilm_ic_via):
        add_through_via(board, position, e1_ilm)
    ilm_waypoints = [(98.5, 25.5), (99.0, 24.5), (99.0, 22.5),
                     (97.7, 21.6), (97.7, 19.5), (98.5, 18.4)]
    for start, end, layer in (
        (pad('R96', 1, 'E1_ILM').GetPosition(), point(98.5, 22.5), pcb.B_Cu),
        (point(98.5, 22.5), ilm_resistor_via, pcb.B_Cu),
        *[(point(*a), point(*b), pcb.In4_Cu)
          for a, b in zip(ilm_waypoints, ilm_waypoints[1:])],
        (ilm_ic_via, point(99.2, 18.4), pcb.B_Cu),
        (point(99.2, 18.4), point(99.4, 18.775), pcb.B_Cu),
        (point(99.4, 18.775), pad('U44', 9, 'E1_ILM').GetPosition(), pcb.B_Cu),
    ):
        add_segment(board, start, end, layer, e1_ilm)
    charger_gate = pad('U42', 4, 'CHARGER_GATE_EN').GetNet()
    gate_logic_via, gate_efuse_via = point(91.2, 16.075), point(102.3, 17.9)
    for position in (gate_logic_via, gate_efuse_via):
        add_through_via(board, position, charger_gate)
    for start, end, layer in (
        (pad('U42', 4, 'CHARGER_GATE_EN').GetPosition(), gate_logic_via, pcb.B_Cu),
        (gate_logic_via, point(93.0, 14.3), pcb.In1_Cu),
        (point(93.0, 14.3), point(101.0, 14.3), pcb.In1_Cu),
        (point(101.0, 14.3), gate_efuse_via, pcb.In1_Cu),
        (gate_efuse_via, side_pad('U44', 1, 'CHARGER_GATE_EN').GetPosition(), pcb.B_Cu),
    ):
        add_segment(board, start, end, layer, charger_gate)
    gate_bias_via = point(76.25, 10.25)
    add_through_via(board, gate_bias_via, charger_gate)
    for start, end, layer in (
        (pad('R94', 2, 'CHARGER_GATE_EN').GetPosition(), point(71.75, 9.5), pcb.B_Cu),
        (point(71.75, 9.5), point(75.25, 9.5), pcb.B_Cu),
        (point(75.25, 9.5), pad('R95', 1, 'CHARGER_GATE_EN').GetPosition(), pcb.B_Cu),
        (pad('R95', 1, 'CHARGER_GATE_EN').GetPosition(), gate_bias_via, pcb.B_Cu),
        (gate_bias_via, gate_logic_via, pcb.In1_Cu),
    ):
        add_segment(board, start, end, layer, charger_gate)
    sink_a_via, sink_b_via = point(25.45, 14.4), point(20.35, 18.75)
    test_via = point(100, 29)
    for position in (sink_a_via, sink_b_via, test_via):
        add_through_via(board, position, charger_gate)
    for start, end, layer in (
        (pad('U40', 4, 'CHARGER_GATE_EN').GetPosition(), sink_a_via, pcb.B_Cu),
        (pad('U43', 4, 'CHARGER_GATE_EN').GetPosition(), sink_b_via, pcb.B_Cu),
        (sink_b_via, sink_a_via, pcb.In4_Cu),
        (sink_a_via, point(30, 14.4), pcb.In4_Cu),
        (point(30, 14.4), point(75, 14.4), pcb.In4_Cu),
        (point(75, 14.4), gate_bias_via, pcb.In4_Cu),
        (pad('TP35', 1, 'CHARGER_GATE_EN').GetPosition(), test_via, pcb.B_Cu),
        (test_via, point(90, 29), pcb.In4_Cu),
        (point(90, 29), point(90, 16.075), pcb.In4_Cu),
        (point(90, 16.075), gate_logic_via, pcb.In4_Cu),
    ):
        add_segment(board, start, end, layer, charger_gate)
    usb_logic = pad('R94', 1, '+3V3_USB').GetNet()
    ground = pad('R95', 2, 'GND').GetNet()
    bias_supply_via, logic_supply_via = point(73.2, 11.2), point(76.25, 8.75)
    bias_ground_via = point(74.25, 11.25)
    for position in (bias_supply_via, logic_supply_via):
        add_through_via(board, position, usb_logic)
    add_through_via(board, bias_ground_via, ground)
    for start, end, layer, net in (
        (pad('R94', 1, '+3V3_USB').GetPosition(), bias_supply_via, pcb.B_Cu, usb_logic),
        (pad('R77', 1, '+3V3_USB').GetPosition(), logic_supply_via, pcb.B_Cu, usb_logic),
        (bias_supply_via, logic_supply_via, pcb.In2_Cu, usb_logic),
        (pad('R95', 2, 'GND').GetPosition(), bias_ground_via, pcb.B_Cu, ground),
        (bias_ground_via, point(74.25, 18), pcb.In2_Cu, ground),
    ):
        add_segment(board, start, end, layer, net)
    usb_ready = pad('U34', 1, 'USB_RAW_LOGIC_READY').GetNet()
    ready_supervisor_via, ready_sink_via = point(24.55, 11.675), point(25.05, 15.925)
    for position in (ready_supervisor_via, ready_sink_via):
        add_through_via(board, position, usb_ready)
    for start, end, layer in (
        (pad('U34', 1, 'USB_RAW_LOGIC_READY').GetPosition(), ready_supervisor_via, pcb.B_Cu),
        (pad('U43', 1, 'USB_RAW_LOGIC_READY').GetPosition(), ready_sink_via, pcb.B_Cu),
        (ready_supervisor_via, point(24.55, 15.425), pcb.In2_Cu),
        (point(24.55, 15.425), ready_sink_via, pcb.In2_Cu),
    ):
        add_segment(board, start, end, layer, usb_ready)
    supervisor_supply_via, sink_supply_via = point(20.45, 11.675), point(20.45, 15.925)
    for position in (supervisor_supply_via, sink_supply_via):
        add_through_via(board, position, usb_logic)
    for start, end, layer in (
        (pad('U34', 6, '+3V3_USB').GetPosition(), supervisor_supply_via, pcb.B_Cu),
        (pad('U43', 5, '+3V3_USB').GetPosition(), sink_supply_via, pcb.B_Cu),
        (supervisor_supply_via, sink_supply_via, pcb.In2_Cu),
    ):
        add_segment(board, start, end, layer, usb_logic)
    for ref in ('U40', 'U43'):
        add_segment(board, pad(ref, 2, 'GND').GetPosition(),
                    pad(ref, 3, 'GND').GetPosition(), pcb.B_Cu, ground)
    charge_request = pad('U17', 4, 'USB_CHARGE_REQ').GetNet()
    request_source_via, request_sink_via = point(91.3, 7.575), point(94.8, 13.2)
    for position in (request_source_via, request_sink_via):
        add_through_via(board, position, charge_request)
    for start, end, layer in (
        (pad('U17', 4, 'USB_CHARGE_REQ').GetPosition(), request_source_via, pcb.B_Cu),
        (pad('U42', 1, 'USB_CHARGE_REQ').GetPosition(), request_sink_via, pcb.B_Cu),
        (request_source_via, point(93.5, 9.775), pcb.In4_Cu),
        (point(93.5, 9.775), point(93.5, 13.175), pcb.In4_Cu),
        (point(93.5, 13.175), request_sink_via, pcb.In4_Cu),
    ):
        add_segment(board, start, end, layer, charge_request)
    source_supply_via, request_supply_via = point(91.2, 6.625), point(91.2, 14.175)
    for position in (source_supply_via, request_supply_via):
        add_through_via(board, position, usb_logic)
    for start, end, layer in (
        (pad('U17', 5, '+3V3_USB').GetPosition(), source_supply_via, pcb.B_Cu),
        (pad('U42', 5, '+3V3_USB').GetPosition(), request_supply_via, pcb.B_Cu),
        (source_supply_via, point(90, 6.625), pcb.In2_Cu),
        (point(90, 6.625), point(90, 14.175), pcb.In2_Cu),
        (point(90, 14.175), request_supply_via, pcb.In2_Cu),
    ):
        add_segment(board, start, end, layer, usb_logic)
    add_segment(board, pad('U42', 2, 'GND').GetPosition(),
                pad('U42', 3, 'GND').GetPosition(), pcb.B_Cu, ground)
    add_segment(board, pad('U42', 2, 'GND').GetPosition(),
                point(96, 15.22), pcb.B_Cu, ground)
    source_ground_via = point(95.8, 6.625)
    add_through_via(board, source_ground_via, ground)
    for start, end, layer in (
        (pad('U17', 2, 'GND').GetPosition(), source_ground_via, pcb.B_Cu),
        (source_ground_via, point(94, 6.625), pcb.In2_Cu),
        (point(94, 6.625), point(94, 14.7), pcb.In2_Cu),
        (point(94, 14.7), point(96, 15.22), pcb.In2_Cu),
    ):
        add_segment(board, start, end, layer, ground)
    temp_ok = pad('U39', 6, 'TEMP_OK').GetNet()
    temp_sink_via, temp_edge_via = point(29.9, 11.675), point(77.5, 12.5)
    for position in (temp_sink_via, temp_edge_via):
        add_through_via(board, position, temp_ok)
    for start, end, layer in (
        (pad('U40', 1, 'TEMP_OK').GetPosition(), temp_sink_via, pcb.B_Cu),
        (pad('U39', 6, 'TEMP_OK').GetPosition(), point(56, 15), pcb.B_Cu),
        (point(56, 15), point(56, 16), pcb.B_Cu),
        (point(56, 16), pad('U39', 4, 'TEMP_OK').GetPosition(), pcb.B_Cu),
        (point(56, 15), point(56, 13.5), pcb.B_Cu),
        (point(56, 13.5), point(67.5, 13.5), pcb.B_Cu),
        (point(67.5, 13.5), point(69.25, 11.75), pcb.B_Cu),
        (point(69.25, 11.75), pad('R91', 2, 'TEMP_OK').GetPosition(), pcb.B_Cu),
        (point(69.25, 11.75), point(69.25, 12.1), pcb.B_Cu),
        (point(69.25, 12.1), point(77.5, 12.1), pcb.B_Cu),
        (point(77.5, 12.1), temp_edge_via, pcb.B_Cu),
        (temp_sink_via, point(30, 9.5), pcb.In4_Cu),
        (point(30, 9.5), point(77.5, 9.5), pcb.In4_Cu),
        (point(77.5, 9.5), temp_edge_via, pcb.In4_Cu),
    ):
        add_segment(board, start, end, layer, temp_ok)
    left_ground_via, supervisor_ground_via = point(31, 13.575), point(25, 18.5)
    for position in (left_ground_via, supervisor_ground_via):
        add_through_via(board, position, ground)
    for start, end, layer in (
        (pad('U40', 3, 'GND').GetPosition(), left_ground_via, pcb.B_Cu),
        (pad('U43', 3, 'GND').GetPosition(), supervisor_ground_via, pcb.B_Cu),
        (supervisor_ground_via, left_ground_via, pcb.In2_Cu),
        (left_ground_via, point(31, 2.166), pcb.In2_Cu),
    ):
        add_segment(board, start, end, layer, ground)
    for start, end, layer in (
        (logic_supply_via, source_supply_via, pcb.In2_Cu),
        (pad('R91', 1, '+3V3_USB').GetPosition(), point(70.25, 11.4), pcb.B_Cu),
        (point(70.25, 11.4), point(72.8, 11.4), pcb.B_Cu),
        (point(72.8, 11.4), bias_supply_via, pcb.B_Cu),
        (pad('U40', 5, '+3V3_USB').GetPosition(), point(26.45, 11), pcb.B_Cu),
        (point(26.45, 11), point(32.75, 11), pcb.B_Cu),
        (point(32.75, 11), pad('R78', 1, '+3V3_USB').GetPosition(), pcb.B_Cu),
        (pad('R78', 1, '+3V3_USB').GetPosition(), point(32.75, 9.5), pcb.B_Cu),
        (point(32.75, 9.5), point(70.25, 9.5), pcb.B_Cu),
        (point(70.25, 9.5), pad('R91', 1, '+3V3_USB').GetPosition(), pcb.B_Cu),
        (pad('U40', 5, '+3V3_USB').GetPosition(), point(26.45, 10.5), pcb.B_Cu),
        (point(26.45, 10.5), point(21.45, 10.5), pcb.B_Cu),
        (point(21.45, 10.5), pad('U34', 6, '+3V3_USB').GetPosition(), pcb.B_Cu),
    ):
        add_segment(board, start, end, layer, usb_logic)
    sensor_supply_via, sensor_ground_via = point(77.5, 16), point(76.3, 15.7)
    add_through_via(board, sensor_supply_via, usb_logic)
    for start, end, layer in (
        (pad('U39', 5, '+3V3_USB').GetPosition(), point(57.625, 15.5), pcb.B_Cu),
        (point(57.625, 15.5), point(57.625, 16.7), pcb.B_Cu),
        (point(57.625, 16.7), point(77.5, 16.7), pcb.B_Cu),
        (point(77.5, 16.7), sensor_supply_via, pcb.B_Cu),
        (sensor_supply_via, point(78.5, 16), pcb.In2_Cu),
        (point(78.5, 16), point(78.5, 8.75), pcb.In2_Cu),
        (point(78.5, 8.75), logic_supply_via, pcb.In2_Cu),
    ):
        add_segment(board, start, end, layer, usb_logic)
    add_through_via(board, sensor_ground_via, ground)
    for start, end, layer in (
        (pad('U39', 3, 'GND').GetPosition(), point(59.2, 16), pcb.B_Cu),
        (point(59.2, 16), point(76.3, 16), pcb.B_Cu),
        (point(76.3, 16), sensor_ground_via, pcb.B_Cu),
        (sensor_ground_via, point(76.3, 18.73), pcb.In2_Cu),
    ):
        add_segment(board, start, end, layer, ground)
    ldo_output_via, ldo_ground_via = point(91.2, 9.925), point(95.8, 10.875)
    add_through_via(board, ldo_output_via, usb_logic)
    add_through_via(board, ldo_ground_via, ground)
    for start, end, layer, net in (
        (pad('U29', 5, '+3V3_USB').GetPosition(), ldo_output_via, pcb.B_Cu, usb_logic),
        (ldo_output_via, point(90, 9.925), pcb.In2_Cu, usb_logic),
        (pad('U29', 2, 'GND').GetPosition(), ldo_ground_via, pcb.B_Cu, ground),
        (ldo_ground_via, point(94, 10.875), pcb.In2_Cu, ground),
    ):
        add_segment(board, start, end, layer, net)
    usb_five_volt = pad('U29', 1, '+5V_USB').GetNet()
    ldo_input_via = point(95.8, 9.925)
    add_through_via(board, ldo_input_via, usb_five_volt)
    for start, end, layer in (
        (pad('U29', 1, '+5V_USB').GetPosition(), ldo_input_via, pcb.B_Cu),
        (ldo_input_via, point(97, 9.925), pcb.F_Cu),
        (point(97, 9.925), point(100.5, 17), pcb.F_Cu),
    ):
        add_segment(board, start, end, layer, usb_five_volt)
    add_segment(board, pad('C32', 1, '+3V3_USB').GetPosition(),
                ldo_output_via, pcb.B_Cu, usb_logic)
    output_cap_ground_via = point(88.45, 11.4)
    add_through_via(board, output_cap_ground_via, ground)
    add_segment(board, pad('C32', 2, 'GND').GetPosition(),
                output_cap_ground_via, pcb.B_Cu, ground)
    add_segment(board, output_cap_ground_via, ldo_ground_via, pcb.In3_Cu, ground)
    for start, end in (
        (pad('C30', 1, '+5V_USB').GetPosition(), point(97.65, 8.3)),
        (point(97.65, 8.3), point(94, 8.3)),
        (point(94, 8.3), point(94, 9.925)),
        (point(94, 9.925), pad('U29', 1, '+5V_USB').GetPosition()),
    ):
        add_segment(board, start, end, pcb.B_Cu, usb_five_volt)
    input_cap_ground_via = point(96.2, 9.15)
    add_through_via(board, input_cap_ground_via, ground)
    for start, end, layer in (
        (pad('C30', 2, 'GND').GetPosition(), input_cap_ground_via, pcb.B_Cu),
        (input_cap_ground_via, point(94, 9.15), pcb.In3_Cu),
        (point(94, 9.15), point(94, 10.875), pcb.In3_Cu),
        (point(94, 10.875), ldo_ground_via, pcb.In3_Cu),
    ):
        add_segment(board, start, end, layer, ground)
    logic_ready = pad('U17', 3, 'USB_LOGIC_READY').GetNet()
    for start, end in (
        (pad('U17', 3, 'USB_LOGIC_READY').GetPosition(), point(95.8, 7.575)),
        (point(95.8, 7.575), point(95.8, 7.75)),
        (point(95.8, 7.75), point(98.3, 7.75)),
        (point(98.3, 7.75), point(98.3, 11.325)),
        (point(98.3, 11.325), pad('U25', 4, 'USB_LOGIC_READY').GetPosition()),
    ):
        add_segment(board, start, end, pcb.B_Cu, logic_ready)
    vbus_valid = pad('U17', 1, 'USB_VBUS_VALID').GetNet()
    valid_source_via, valid_sink_via = point(96.0, 5.675), point(100.9, 9.425)
    for position in (valid_source_via, valid_sink_via):
        add_through_via(board, position, vbus_valid)
    for start, end, layer in (
        (pad('U17', 1, 'USB_VBUS_VALID').GetPosition(), valid_source_via, pcb.B_Cu),
        (valid_source_via, point(100.9, 5.675), pcb.In3_Cu),
        (point(100.9, 5.675), valid_sink_via, pcb.In3_Cu),
        (valid_sink_via, pad('U25', 6, 'USB_VBUS_VALID').GetPosition(), pcb.B_Cu),
    ):
        add_segment(board, start, end, layer, vbus_valid)
    cc_high = pad('U17', 6, 'USB_CC_HIGH').GetNet()
    cc_source_via, cc_sink_via = point(91.2, 5.675), point(97.7, 6.5)
    for position in (cc_source_via, cc_sink_via):
        add_through_via(board, position, cc_high)
    for start, end, layer in (
        (pad('U17', 6, 'USB_CC_HIGH').GetPosition(), cc_source_via, pcb.B_Cu),
        (cc_source_via, point(91.2, 4.0), pcb.In1_Cu),
        (point(91.2, 4.0), point(98.3, 4.0), pcb.In1_Cu),
        (point(98.3, 4.0), point(98.3, 6.5), pcb.In1_Cu),
        (point(98.3, 6.5), cc_sink_via, pcb.In1_Cu),
        (cc_sink_via, pad('U11', 4, 'USB_CC_HIGH').GetPosition(), pcb.B_Cu),
    ):
        add_segment(board, start, end, layer, cc_high)
    cc_supply_via, qualifier_supply_via = point(96.8, 4.85), point(100.8, 10.375)
    for position in (cc_supply_via, qualifier_supply_via):
        add_through_via(board, position, usb_logic)
    for start, end, layer in (
        (source_supply_via, point(90, 6.625), pcb.In1_Cu),
        (point(90, 6.625), point(90, 8.3), pcb.In1_Cu),
        (point(90, 8.3), point(96.8, 8.3), pcb.In1_Cu),
        (point(96.8, 8.3), cc_supply_via, pcb.In1_Cu),
        (cc_supply_via, pad('U11', 5, '+3V3_USB').GetPosition(), pcb.B_Cu),
        (point(96.8, 8.3), point(99.0, 8.3), pcb.In1_Cu),
        (point(99.0, 8.3), point(99.0, 10.375), pcb.In1_Cu),
        (point(99.0, 10.375), qualifier_supply_via, pcb.In1_Cu),
        (qualifier_supply_via, pad('U25', 5, '+3V3_USB').GetPosition(), pcb.B_Cu),
    ):
        add_segment(board, start, end, layer, usb_logic)
    qualifier_ground_via = point(103.3, 10.375)
    add_through_via(board, qualifier_ground_via, ground)
    for start, end, layer in (
        (pad('U25', 2, 'GND').GetPosition(), qualifier_ground_via, pcb.B_Cu),
        (pad('U11', 3, 'GND').GetPosition(), point(101.2, 7.075), pcb.B_Cu),
        (point(101.2, 7.075), point(101.2, 8.2), pcb.B_Cu),
        (point(101.2, 8.2), point(103.3, 8.2), pcb.B_Cu),
        (point(103.3, 8.2), qualifier_ground_via, pcb.B_Cu),
        (qualifier_ground_via, point(103.8, 11.0), pcb.In3_Cu),
        (point(103.8, 11.0), ground_cap_via, pcb.In3_Cu),
    ):
        add_segment(board, start, end, layer, ground)
    assert len(list(board.GetTracks())) == 339
    pcb.SaveBoard(str(OUTPUT), board)
    contents = sorted_native_tracks(OUTPUT.read_text())
    serial = iter(range(contents.count('(uuid "')))
    contents = re.sub(r'\(uuid "[0-9a-f-]{36}"\)',
                      lambda _: '(uuid "' + str(uuid.uuid5(SCOPE, str(next(serial)))) + '")',
                      contents)
    OUTPUT.write_text(contents)
    print(f'{OUTPUT}: 265 trace segments, 74 through vias; staged USB, shell, charger and battery links')


if __name__ == '__main__':
    generate()
