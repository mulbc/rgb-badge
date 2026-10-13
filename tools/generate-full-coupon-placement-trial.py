#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Stage every coupon footprint and four local USB links on a 120 mm study board.

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
        # Keep the protected USB input stages close to the physical connector
        # before the area-first pass consumes this routing corridor.
        fixed["U45"] = fit.box(104.0, 13.25, 3.5, 3.5)
        fixed["U44"] = fit.box(104.0, 17.25, 3.5, 3.5)
        fixed["C60"] = fit.box(108.0, 13.25, 3.0, 1.5)
        fixed["C61"] = fit.box(108.0, 15.25, 3.5, 1.5)
        fixed["C62"] = fit.box(101.0, 15.25, 2.5, 1.5)
        fixed["C52"] = fit.box(108.0, 18.25, 2.5, 1.5)
        fixed["C57"] = fit.box(101.0, 18.25, 2.5, 1.5)
        fixed["R99"] = fit.box(101.0, 11.25, 2.5, 1.5)
        fixed["R100"] = fit.box(101.0, 13.25, 2.5, 1.5)
        fixed["R97"] = fit.box(98.0, 13.25, 2.5, 1.5)
        fixed["R98"] = fit.box(98.0, 15.25, 2.5, 1.5)
        fixed["R96"] = fit.box(101.0, 16.75, 2.5, 1.5)
        fixed["U50"] = fit.box(94.25, 29.5, 2.5, 2.5)
        placement = fit.place(rear, "canonical 32 separate row FETs", "area first",
                              fixed, pack, sensor, board_width=WIDTH)
    components = {part.get("ref"): part for part in root.findall("./components/comp")}
    pins = {(node.get("ref"), node.get("pin")): net.get("name")
            for net in root.findall("./nets/net") for node in net.findall("node")}
    assert len(components) == 497 and sum(counts.values()) == 497
    assert placement["unplaced_count"] == 0, placement["unplaced_refs"]
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
        x += 0.15 if box[0] < 0.5 else -0.15
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


def verify_saved_board(board, components, pins):
    footprints = {part.GetReference(): part for part in board.GetFootprints()}
    assert len(footprints) == len(components)
    assert set(footprints) == set(components)
    seen = set()
    for ref, part in footprints.items():
        library, name = components[ref].findtext("footprint").split(":", 1)
        assert part.GetFPID().GetLibNickname() == library, ref
        assert part.GetFPID().GetLibItemName() == name, ref
        for pad in part.Pads():
            number = pad.GetNumber()
            if not number or (ref, number) == ("J2", "MP"):
                continue
            key = ref, number
            assert key in pins, key
            expected = pins[key]
            actual = pad.GetNetname()
            assert actual == ("" if expected.startswith("unconnected-") else expected), (key, expected, actual)
            seen.add(key)
    assert seen == set(pins), (len(seen), len(pins))


def route_local_efuse_support(board):
    """Capture four short, native-DRC-screened support links in the USB cluster."""
    parts = {part.GetReference(): part for part in board.GetFootprints()}
    routes = (
        ("C62", "1", "U45", "7", 0, ()),
        ("C57", "1", "U44", "7", 1, ()),
        ("R100", "1", "U45", "9", 0, ((103.75, 14.0), (103.75, 14.78))),
        ("R96", "1", "U44", "9", 0, ((103.75, 17.5), (103.75, 18.77))),
    )
    for start_ref, start_pin, end_ref, end_pin, end_index, waypoints in routes:
        start_pad = next(pad for pad in parts[start_ref].Pads() if pad.GetNumber() == start_pin)
        end_pad = [pad for pad in parts[end_ref].Pads() if pad.GetNumber() == end_pin][end_index]
        assert start_pad.GetNetname() and start_pad.GetNetname() == end_pad.GetNetname()
        points = [start_pad.GetPosition()]
        points.extend(pcb.VECTOR2I(pcb.FromMM(x), pcb.FromMM(y)) for x, y in waypoints)
        points.append(end_pad.GetPosition())
        for start, end in zip(points, points[1:]):
            track = pcb.PCB_TRACK(board)
            track.SetStart(start)
            track.SetEnd(end)
            track.SetWidth(pcb.FromMM(0.2))
            track.SetLayer(pcb.B_Cu)
            track.SetNet(start_pad.GetNet())
            board.Add(track)


def generate():
    components, pins, boxes = source()
    project_file = BOARD.with_suffix(".kicad_pro")
    project_existed = project_file.exists()
    board = pcb.BOARD()
    board.SetCopperLayerCount(6)
    board.GetDesignSettings().SetBoardThickness(pcb.FromMM(1.0))
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
    route_local_efuse_support(board)
    assert pcb.SaveBoard(str(BOARD), board)
    BOARD.write_text(normalize(BOARD.read_text()))
    loaded = pcb.LoadBoard(str(BOARD))
    assert loaded.GetCopperLayerCount() == 6
    assert loaded.GetDesignSettings().GetBoardThickness() == pcb.FromMM(1.0)
    verify_saved_board(loaded, components, pins)
    tracks = list(loaded.GetTracks())
    assert len(tracks) == 8
    assert {track.GetNetname() for track in tracks} == {"E0_DVDT", "E1_DVDT", "E0_ILM", "E1_ILM"}
    assert all(track.GetLayer() == pcb.B_Cu and track.GetWidth() == pcb.FromMM(0.2)
               for track in tracks)
    if not project_existed and project_file.is_file():
        project_file.unlink()
    print(f"Staged and round-trip-checked {len(components)} exact footprints and {len(assigned)} unique numbered pad nets")
    print("120 mm study outline, four local eFuse support nets; other routing and USB cutout remain open")


if __name__ == "__main__":
    generate()
