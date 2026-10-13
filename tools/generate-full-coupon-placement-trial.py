#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Stage every captured coupon footprint on a 120 mm unrouted study board.

This deliberately exceeds the final 110 mm case target. It is a wiring and
clearance discovery artifact, not the canonical PCB or a fabrication release.
"""

import importlib.util
from pathlib import Path
import re
import subprocess
import tempfile
import uuid
import xml.etree.ElementTree as ET

import pcbnew as pcb


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / "hardware/coupon/rev-a"
BOARD = PROJECT / "staging/full-coupon-placement-trial-120mm.kicad_pcb"
FOOTPRINTS = PROJECT / "footprints/rgb-badge-coupon.pretty"
CLI = Path("/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli")
SCOPE = uuid.UUID("c3161b5a-c243-51ed-b55b-511cd465a6ca")
WIDTH, HEIGHT, PITCH = 120.0, 32.5, 1.95


def current_fit_module():
    path = ROOT / "tools/screen-current-lp452845-xy.py"
    spec = importlib.util.spec_from_file_location("current_coupon_fit", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def source():
    with tempfile.TemporaryDirectory(prefix="rgb-full-placement-") as dirname:
        xml = Path(dirname) / "coupon.xml"
        subprocess.run([str(CLI), "sch", "export", "netlist", "--format", "kicadxml",
                        "--output", str(xml), str(PROJECT / "rgb-badge-coupon.kicad_sch")],
                       check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        root = ET.parse(xml).getroot()
        fit = current_fit_module()
        rear, counts = fit.space.component_inventory(xml)
        pack = fit.box(31.0, 2.0, 47.0, 28.5)
        sensor = fit.box(49.5, 12.25, 10.0, 8.0)
        fixed = fit.fixed_boxes(rear, right_shift=WIDTH - fit.BOARD_W)
        placement = fit.place(rear, "canonical 32 separate row FETs", "area first",
                              fixed, pack, sensor, board_width=WIDTH)
    components = {part.get("ref"): part for part in root.findall("./components/comp")}
    pins = {(node.get("ref"), node.get("pin")): net.get("name")
            for net in root.findall("./nets/net") for node in net.findall("node")}
    assert len(components) == 497 and sum(counts.values()) == 497
    assert placement["unplaced_count"] == 0
    return components, pins, placement["boxes_mm"]


def add_outline(board):
    corners = [(0, 0), (WIDTH, 0), (WIDTH, HEIGHT), (0, HEIGHT)]
    for start, end in zip(corners, corners[1:] + corners[:1]):
        edge = pcb.PCB_SHAPE(board)
        edge.SetShape(pcb.S_SEGMENT)
        edge.SetStart(pcb.VECTOR2I(pcb.FromMM(start[0]), pcb.FromMM(start[1])))
        edge.SetEnd(pcb.VECTOR2I(pcb.FromMM(end[0]), pcb.FromMM(end[1])))
        edge.SetLayer(pcb.Edge_Cuts)
        edge.SetWidth(pcb.FromMM(0.05))
        board.Add(edge)


def target(ref, boxes):
    if ref.startswith("D") and ref[1:].isdigit():
        index = int(ref[1:]) - 1
        assert 0 <= index < 256
        row, col = divmod(index, 16)
        return ((WIDTH - 15 * PITCH) / 2 + col * PITCH,
                (HEIGHT - 15 * PITCH) / 2 + row * PITCH), None
    box = boxes["U1-project-1" if ref == "U1" else ref]
    x, y = (box[0] + box[2]) / 2, (box[1] + box[3]) / 2
    # Small native-DRC corrections to the first-fit courtyard coordinates.
    if ref == "Q1":
        y += 0.15
    elif ref == "TP4":
        x -= 0.15
    return (x, y), box


def align_courtyard(part, xy):
    layer = pcb.F_CrtYd if part.GetLayer() == pcb.F_Cu else pcb.B_CrtYd
    bbox = part.GetCourtyard(layer).BBox()
    assert bbox.GetWidth() and bbox.GetHeight(), part.GetReference()
    current_x = bbox.GetX() + bbox.GetWidth() // 2
    current_y = bbox.GetY() + bbox.GetHeight() // 2
    part.SetPosition(pcb.VECTOR2I(pcb.FromMM(xy[0]) - current_x,
                                  pcb.FromMM(xy[1]) - current_y))


def normalize(contents):
    starts = [match.start() for match in re.finditer(r'\n\t\(footprint ', contents)]
    assert len(starts) == 497
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
    contents = contents[:blocks[0][0]] + ''.join(ordered) + contents[blocks[-1][1]:]
    count = iter(range(contents.count('(uuid "')))
    updated = re.sub(r'\(uuid "[0-9a-f-]{36}"\)',
                     lambda _: '(uuid "' + str(uuid.uuid5(SCOPE, str(next(count)))) + '")',
                     contents)
    assert updated != contents
    return updated


def generate():
    components, pins, boxes = source()
    project_file = BOARD.with_suffix(".kicad_pro")
    project_existed = project_file.exists()
    board = pcb.BOARD()
    add_outline(board)
    nets = {}
    for name in sorted(set(pins.values())):
        if not name.startswith("unconnected-"):
            item = pcb.NETINFO_ITEM(board, name)
            board.Add(item)
            nets[name] = item
    assigned = set()
    for ref in sorted(components):
        component = components[ref]
        library, footprint = component.findtext("footprint").split(":", 1)
        assert library == "rgb-badge-coupon"
        part = pcb.FootprintLoad(str(FOOTPRINTS), footprint)
        assert part is not None, ref
        part.SetFPID(pcb.LIB_ID(library, footprint))
        part.SetReference(ref)
        part.SetValue(component.findtext("value"))
        board.Add(part)
        if not ref.startswith("D") and ref != "J1":
            part.Flip(pcb.VECTOR2I(0, 0), False)
        if ref == "J1":
            part.SetOrientationDegrees(90)
        elif ref.startswith("D") and component.findtext("value") == "QBLP1515A-RGB2A":
            index = int(ref[1:]) - 1
            row, col = divmod(index, 16)
            if (row + col) % 2:
                part.SetOrientationDegrees(90)
        xy, _ = target(ref, boxes)
        align_courtyard(part, xy)
        part.Reference().SetVisible(False)
        part.Value().SetVisible(False)
        for pad in part.Pads():
            number = pad.GetNumber()
            if not number:
                continue
            key = ref, number
            if key == ("J2", "MP"):
                # Non-electrical SMT mounting tabs in the exact JST land.
                continue
            assert key in pins, key
            name = pins[key]
            if not name.startswith("unconnected-"):
                pad.SetNet(nets[name])
            assigned.add(key)
    assert assigned == set(pins)
    assert pcb.SaveBoard(str(BOARD), board)
    BOARD.write_text(normalize(BOARD.read_text()))
    loaded = pcb.LoadBoard(str(BOARD))
    assert len(loaded.GetFootprints()) == len(components)
    assert not list(loaded.GetTracks())
    if not project_existed and project_file.is_file():
        project_file.unlink()
    print(f"Staged {len(components)} exact footprints and {len(assigned)} unique numbered pad nets")
    print("120 mm study outline, no routing, no USB cutout or fabrication status")


if __name__ == "__main__":
    generate()
