#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Probe five local charger connections on the 114 mm placement-only board."""

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
    assert len(starts) == 18
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

    assert len(list(board.GetTracks())) == 18
    pcb.SaveBoard(str(OUTPUT), board)
    contents = sorted_native_tracks(OUTPUT.read_text())
    serial = iter(range(contents.count('(uuid "')))
    contents = re.sub(r'\(uuid "[0-9a-f-]{36}"\)',
                      lambda _: '(uuid "' + str(uuid.uuid5(SCOPE, str(next(serial)))) + '")',
                      contents)
    OUTPUT.write_text(contents)
    print(f'{OUTPUT}: 16 trace segments, 2 through vias, five local charger nets')


if __name__ == '__main__':
    generate()
