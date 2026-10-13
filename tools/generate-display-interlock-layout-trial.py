#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Create an unrouted, exact-footprint KiCad placement study of the interlock."""

from pathlib import Path
import re
import subprocess
import tempfile
import uuid
import xml.etree.ElementTree as ET

import pcbnew as pcb


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / "hardware/coupon/rev-a"
BOARD = PROJECT / "staging/display-interlock-layout-trial.kicad_pcb"
FOOTPRINTS = PROJECT / "footprints/rgb-badge-coupon.pretty"
CLI = Path("/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli")
UUID_SCOPE = uuid.UUID("5c13e327-6a3d-5885-9cb4-d897ad9c6587")
EXPECTED = {*(f"U{n}" for n in range(47, 56)), *(f"C{n}" for n in range(66, 75)),
            *(f"R{n}" for n in range(103, 114)), "TP13", "TP14"}

# Centres in a 35 x 24 mm local study. These are not final-board coordinates.
POSITIONS = {
    "U47": (4, 4.5), "U48": (11, 4.5), "U49": (17, 4.5), "U50": (23, 4.5),
    "C66": (4, 8), "C67": (11, 8), "C68": (17, 8), "C69": (23, 8),
    "U51": (4, 13), "U52": (10, 13), "U53": (17, 13), "U54": (24, 13), "U55": (31, 13),
    "C70": (4, 17), "C71": (10, 17), "C72": (17, 17), "C73": (24, 17), "C74": (31, 17),
    "R103": (3, 22), "R104": (8, 22), "R105": (13, 22),
    "R106": (18, 22), "R107": (23, 22), "R108": (28, 22),
    "R109": (13, 19.5), "R110": (16, 19.5), "R111": (19, 19.5),
    "R112": (22, 19.5), "R113": (25, 19.5),
    "TP13": (30, 19.5), "TP14": (33, 19.5),
}
assert set(POSITIONS) == EXPECTED


def source_nets():
    with tempfile.TemporaryDirectory(prefix="rgb-interlock-layout-") as dirname:
        path = Path(dirname) / "coupon.xml"
        subprocess.run([str(CLI), "sch", "export", "netlist", "--format", "kicadxml",
                        "--output", str(path), str(PROJECT / "rgb-badge-coupon.kicad_sch")],
                       check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        root = ET.parse(path).getroot()
    components = {part.get("ref"): part for part in root.findall("./components/comp")}
    pins = {(node.get("ref"), node.get("pin")): net.get("name")
            for net in root.findall("./nets/net") for node in net.findall("node")}
    assert EXPECTED <= set(components)
    return components, pins


def outline(board):
    corners = [(0, 0), (35, 0), (35, 24), (0, 24)]
    for start, end in zip(corners, corners[1:] + corners[:1]):
        edge = pcb.PCB_SHAPE(board)
        edge.SetShape(pcb.S_SEGMENT)
        edge.SetStart(pcb.VECTOR2I(pcb.FromMM(start[0]), pcb.FromMM(start[1])))
        edge.SetEnd(pcb.VECTOR2I(pcb.FromMM(end[0]), pcb.FromMM(end[1])))
        edge.SetLayer(pcb.Edge_Cuts)
        edge.SetWidth(pcb.FromMM(0.05))
        board.Add(edge)


def normalize_board_text(contents):
    starts = [match.start() for match in re.finditer(r'\n\t\(footprint ', contents)]
    assert len(starts) == len(EXPECTED)
    blocks = []
    for start in starts:
        depth = 0
        quoted = escaped = False
        for pos in range(start + 2, len(contents)):
            char = contents[pos]
            if quoted:
                if escaped:
                    escaped = False
                elif char == "\\":
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
                    blocks.append((start, pos + 1, contents[start:pos + 1]))
                    break
        else:
            raise ValueError("Unclosed footprint in native board export")
    assert all(not contents[a[1]:b[0]].strip() for a, b in zip(blocks, blocks[1:]))
    def reference(block):
        match = re.search(r'\(property "Reference" "([^"]+)"', block)
        assert match
        return match.group(1)
    ordered = sorted((block[2] for block in blocks), key=reference)
    assert {reference(block) for block in ordered} == EXPECTED
    contents = contents[:blocks[0][0]] + ''.join(ordered) + contents[blocks[-1][1]:]
    count = iter(range(contents.count('(uuid "')))
    return re.sub(r'\(uuid "[0-9a-f-]{36}"\)',
                  lambda _: '(uuid "' + str(uuid.uuid5(UUID_SCOPE, str(next(count)))) + '")',
                  contents)


def generate():
    project_file = BOARD.with_suffix(".kicad_pro")
    project_existed = project_file.exists()
    components, source = source_nets()
    board = pcb.BOARD()
    outline(board)
    nets = {}
    for name in sorted(set(source.values())):
        if name.startswith("unconnected-"):
            continue
        item = pcb.NETINFO_ITEM(board, name)
        board.Add(item)
        nets[name] = item
    actual_pins = set()
    for ref in sorted(EXPECTED):
        component = components[ref]
        full_footprint = component.findtext("footprint")
        library, footprint = full_footprint.split(":", 1)
        assert library == "rgb-badge-coupon"
        part = pcb.FootprintLoad(str(FOOTPRINTS), footprint)
        assert part is not None, ref
        part.SetFPID(pcb.LIB_ID(library, footprint))
        part.SetReference(ref)
        part.SetValue(component.findtext("value"))
        x, y = POSITIONS[ref]
        part.SetPosition(pcb.VECTOR2I(pcb.FromMM(x), pcb.FromMM(y)))
        part.Reference().SetVisible(False)
        part.Value().SetVisible(False)
        board.Add(part)
        for pad in part.Pads():
            pin = pad.GetNumber()
            if not pin:
                continue
            key = (ref, pin)
            assert key in source, key
            name = source[key]
            if not name.startswith("unconnected-"):
                pad.SetNet(nets[name])
            actual_pins.add(key)
    assert actual_pins == {key for key in source if key[0] in EXPECTED}
    assert pcb.SaveBoard(str(BOARD), board)
    BOARD.write_text(normalize_board_text(BOARD.read_text()))
    saved = pcb.LoadBoard(str(BOARD))
    parts = {part.GetReference(): part for part in saved.GetFootprints()}
    assert set(parts) == EXPECTED
    assert not list(saved.GetTracks())
    for ref, part in parts.items():
        assert part.GetFPIDAsString() == components[ref].findtext("footprint")
        assert (pcb.ToMM(part.GetPosition().x), pcb.ToMM(part.GetPosition().y)) == POSITIONS[ref]
        for pad in part.Pads():
            pin = pad.GetNumber()
            if not pin:
                continue
            name = source[(ref, pin)]
            assert pad.GetNetname() == ("" if name.startswith("unconnected-") else name)
    if not project_existed and project_file.is_file():
        project_file.unlink()
    print(f"Staged {len(parts)} interlock footprints with {len(actual_pins)} unique numbered pads")


if __name__ == "__main__":
    generate()
