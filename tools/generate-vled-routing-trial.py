#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Route only the first VLED switching and capacitor connections for geometry review.

This standalone local board is not a coupon/final board or a fabrication output.
Run with KiCad's bundled Python 3.9 after generate-vled-layout-trial.py.
"""

import importlib.util
from pathlib import Path
import re
import uuid

import pcbnew as pcb

ROOT = Path(__file__).resolve().parents[1]
STAGING = ROOT / "hardware/coupon/rev-a/staging"
SOURCE = STAGING / "vled-layout-trial.kicad_pcb"
TARGET = STAGING / "vled-routing-trial.kicad_pcb"

spec = importlib.util.spec_from_file_location(
    "vled_layout", ROOT / "tools/generate-vled-layout-trial.py")
layout = importlib.util.module_from_spec(spec)
spec.loader.exec_module(layout)

# Endpoints are native pad centres or intermediate points in millimetres.
# These are topology/clearance probes, not current-rated finished traces.
ROUTES = {
    "Net-(L2-~-Pad2)": [
        ((94.45, 26.05), (94.95, 26.05)),
        ((94.95, 26.05), (97.10, 26.05)),
        ((97.10, 26.05), (97.50, 26.45)),
    ],
    "Net-(L2-~-Pad1)": [
        ((94.45, 28.85), (94.95, 28.85)),
        ((94.95, 28.85), (97.10, 28.85)),
        ((97.10, 28.85), (97.50, 28.45)),
    ],
    "+SYS_APP_IN_DRAFT": [
        ((93.45, 28.85), (93.95, 28.85)),
        ((93.45, 28.85), (93.45, 30.30)),
        ((93.45, 30.30), (94.95, 30.30)),
    ],
    "VLED": [
        ((93.45, 26.05), (93.95, 26.05)),
        ((93.45, 26.05), (93.45, 24.60)),
        ((93.45, 24.60), (94.95, 24.60)),
    ],
}

ANCHORS = {
    ("U37", "4"): ("VLED", (93.45, 26.05)),
    ("U37", "5"): ("VLED", (93.95, 26.05)),
    ("U37", "6"): ("Net-(L2-~-Pad2)", (94.45, 26.05)),
    ("U37", "7"): ("Net-(L2-~-Pad2)", (94.95, 26.05)),
    ("U37", "8"): ("Net-(L2-~-Pad1)", (94.95, 28.85)),
    ("U37", "9"): ("Net-(L2-~-Pad1)", (94.45, 28.85)),
    ("U37", "10"): ("+SYS_APP_IN_DRAFT", (93.95, 28.85)),
    ("U37", "11"): ("+SYS_APP_IN_DRAFT", (93.45, 28.85)),
    ("L2", "1"): ("Net-(L2-~-Pad1)", (97.50, 28.45)),
    ("L2", "2"): ("Net-(L2-~-Pad2)", (97.50, 26.45)),
    ("C44", "1"): ("+SYS_APP_IN_DRAFT", (93.40, 30.30)),
    ("C45", "1"): ("+SYS_APP_IN_DRAFT", (94.95, 30.30)),
    ("C46", "1"): ("VLED", (93.40, 24.60)),
    ("C47", "1"): ("VLED", (94.95, 24.60)),
}


def point(xy):
    return pcb.VECTOR2I(pcb.FromMM(xy[0]), pcb.FromMM(xy[1]))


def normalize_routing_text(contents):
    contents = layout.normalize_board_text(contents)
    pattern = re.compile(r'\n\t\(segment\n.*?\n\t\)', re.DOTALL)
    blocks = list(pattern.finditer(contents))
    assert len(blocks) == 12
    assert all(not contents[a.end():b.start()].strip()
               for a, b in zip(blocks, blocks[1:]))
    def key(block):
        return (re.search(r'\(net "([^"]+)"\)', block).group(1),
                re.search(r'\(start ([^)]+)\)', block).group(1),
                re.search(r'\(end ([^)]+)\)', block).group(1))
    ordered = ''.join(sorted((block.group() for block in blocks), key=key))
    contents = contents[:blocks[0].start()] + ordered + contents[blocks[-1].end():]
    counter = iter(range(contents.count('(uuid "')))
    return re.sub(r'\(uuid "[0-9a-f-]{36}"\)',
                  lambda _: '(uuid "' + str(uuid.uuid5(layout.UUID_SCOPE,
                                             str(next(counter)))) + '")', contents)


def main():
    assert SOURCE.is_file(), "Generate the placement board first"
    project_file = TARGET.with_suffix(".kicad_pro")
    project_existed = project_file.exists()
    board = pcb.LoadBoard(str(SOURCE))
    assert not list(board.GetTracks())
    footprints = {item.GetReference(): item for item in board.GetFootprints()}
    for (ref, number), (net, xy) in ANCHORS.items():
        pad = next(p for p in footprints[ref].Pads() if p.GetNumber() == number)
        assert pad.GetNetname() == net, (ref, number)
        assert abs(pcb.ToMM(pad.GetPosition().x) - xy[0]) < 0.01, (ref, number)
        assert abs(pcb.ToMM(pad.GetPosition().y) - xy[1]) < 0.01, (ref, number)
    nets = {net.GetNetname(): net for net in board.GetNetInfo().NetsByNetcode().values()}
    assert set(ROUTES) <= set(nets)
    for name, segments in ROUTES.items():
        for start, end in segments:
            track = pcb.PCB_TRACK(board)
            track.SetStart(point(start))
            track.SetEnd(point(end))
            track.SetWidth(pcb.FromMM(0.20))
            track.SetLayer(pcb.F_Cu)
            track.SetNet(nets[name])
            board.Add(track)
    assert pcb.SaveBoard(str(TARGET), board)
    TARGET.write_text(normalize_routing_text(TARGET.read_text()))
    saved = pcb.LoadBoard(str(TARGET))
    assert len(list(saved.GetTracks())) == sum(map(len, ROUTES.values())) == 12
    assert len(list(saved.GetFootprints())) == 13
    if not project_existed and project_file.is_file():
        project_file.unlink()
    print(f"Staged {len(list(saved.GetTracks()))} F.Cu segments in {TARGET}")


if __name__ == "__main__":
    main()
