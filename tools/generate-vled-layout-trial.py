#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Create an unconnected, local KiCad PCB placement for the VLED candidate.

Run with KiCad's bundled Python 3.9 so pcbnew is available. This is a layout
study, not the coupon or final-board PCB, and must never be exported for fab.
"""

import json
from pathlib import Path
import re
import subprocess
import tempfile
import uuid
import xml.etree.ElementTree as ET

import pcbnew as pcb


ROOT = Path(__file__).resolve().parents[1]
STAGING = ROOT / "hardware/coupon/rev-a/staging"
SHEET = STAGING / "vled-converter.kicad_sch"
BOARD = STAGING / "vled-layout-trial.kicad_pcb"
FOOTPRINTS = ROOT / "hardware/coupon/rev-a/footprints/rgb-badge-coupon.pretty"
FIT = ROOT / "mechanical/review/fit-trial.json"
CLI = Path("/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli")
UUID_SCOPE = uuid.UUID("a195d24f-1e19-5e1f-97ae-90e9ca90a027")
REFS = {"U37", "L2", *("C" + str(n) for n in range(44, 51)),
        *("R" + str(n) for n in range(84, 88))}


def source_nets():
    with tempfile.TemporaryDirectory(prefix="rgb-vled-layout-") as dirname:
        path = Path(dirname) / "vled.xml"
        subprocess.run([str(CLI), "sch", "export", "netlist", "--format", "kicadxml",
                        "--output", str(path), str(SHEET)], check=True,
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        tree = ET.parse(path).getroot()
    values = {part.attrib["ref"]: part.findtext("value")
              for part in tree.find("components")}
    pins = {}
    for net in tree.find("nets"):
        for node in net.findall("node"):
            pins[(node.attrib["ref"], node.attrib["pin"])] = net.attrib["name"]
    assert set(values) == REFS
    return values, pins


def add_outline(board):
    # Local study window at the same coordinates as the final-board XY screen.
    corners = [(90.5, 22.0), (105.5, 22.0), (105.5, 32.5), (90.5, 32.5)]
    for start, end in zip(corners, corners[1:] + corners[:1]):
        edge = pcb.PCB_SHAPE(board)
        edge.SetShape(pcb.S_SEGMENT)
        edge.SetStart(pcb.VECTOR2I(pcb.FromMM(start[0]), pcb.FromMM(start[1])))
        edge.SetEnd(pcb.VECTOR2I(pcb.FromMM(end[0]), pcb.FromMM(end[1])))
        edge.SetLayer(pcb.Edge_Cuts)
        edge.SetWidth(pcb.FromMM(0.05))
        board.Add(edge)


def normalize_board_text(contents):
    """Sort pcbnew's unordered footprint container before assigning stable IDs."""
    starts = [match.start() for match in re.finditer(r'\n\t\(footprint ', contents)]
    assert len(starts) == len(REFS)
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
    assert {reference(block) for block in ordered} == REFS
    contents = contents[:blocks[0][0]] + ''.join(ordered) + contents[blocks[-1][1]:]
    count = iter(range(contents.count('(uuid "')))
    return re.sub(r'\(uuid "[0-9a-f-]{36}"\)',
                  lambda _: '(uuid "' + str(uuid.uuid5(UUID_SCOPE, str(next(count)))) + '")',
                  contents)


def generate():
    project_file = BOARD.with_suffix(".kicad_pro")
    project_existed = project_file.exists()
    report = json.loads(FIT.read_text())
    trial = report["dual_row_package_screen"]
    placements = [p for p in trial["fixed_and_reservations"]
                  if p["ref"] == "VLED" or p["category"] == "VLED candidate passive"]
    assert len(placements) == len(REFS) == 13
    assert trial["vled_cluster_envelope_mm"] == {"x0": 91.0, "y0": 22.8,
                                                   "x1": 102.0, "y1": 32.1}
    values, source = source_nets()
    board = pcb.BOARD()
    add_outline(board)
    nets = {}
    for name in sorted(set(source.values())):
        if name.startswith("unconnected-"):
            continue
        item = pcb.NETINFO_ITEM(board, name)
        board.Add(item)
        nets[name] = item
    physical_pins = set()
    for placement in placements:
        ref = "U37" if placement["ref"] == "VLED" else placement["ref"]
        part = pcb.FootprintLoad(str(FOOTPRINTS), placement["footprint"])
        assert part is not None, ref
        part.SetFPID(pcb.LIB_ID("rgb-badge-coupon", placement["footprint"]))
        part.SetReference(ref)
        part.SetValue(values[ref])
        rect = placement["box"]
        x, y = (rect["x0"] + rect["x1"]) / 2, (rect["y0"] + rect["y1"]) / 2
        part.SetPosition(pcb.VECTOR2I(pcb.FromMM(x), pcb.FromMM(y)))
        part.SetOrientationDegrees(placement.get("orientation_deg", 0))
        part.Value().SetVisible(False)
        board.Add(part)
        for pad in part.Pads():
            number = pad.GetNumber()
            if not number:
                continue  # manufacturer's unnumbered paste apertures
            key = (ref, number)
            assert key in source, key
            name = source[key]
            if not name.startswith("unconnected-"):
                pad.SetNet(nets[name])
            physical_pins.add(key)
    assert physical_pins == set(source), sorted(set(source) - physical_pins)
    BOARD.parent.mkdir(parents=True, exist_ok=True)
    assert pcb.SaveBoard(str(BOARD), board)
    BOARD.write_text(normalize_board_text(BOARD.read_text()))
    saved = pcb.LoadBoard(str(BOARD))
    actual = {part.GetReference(): part for part in saved.GetFootprints()}
    assert set(actual) == REFS
    assert not list(saved.GetTracks()), "Local trial unexpectedly contains routing"
    for placement in placements:
        ref = "U37" if placement["ref"] == "VLED" else placement["ref"]
        part = actual[ref]
        assert part.GetFPIDAsString() == "rgb-badge-coupon:" + placement["footprint"]
        rect = placement["box"]
        expected_xy = ((rect["x0"] + rect["x1"]) / 2,
                       (rect["y0"] + rect["y1"]) / 2)
        assert abs(pcb.ToMM(part.GetPosition().x) - expected_xy[0]) < 0.001
        assert abs(pcb.ToMM(part.GetPosition().y) - expected_xy[1]) < 0.001
        assert abs(part.GetOrientationDegrees() - placement.get("orientation_deg", 0)) < 0.001
        for pad in part.Pads():
            number = pad.GetNumber()
            if not number:
                continue
            net = source[(ref, number)]
            assert pad.GetNetname() == ("" if net.startswith("unconnected-") else net), (ref, number, net)
    if not project_existed and project_file.is_file():
        project_file.unlink()
    print(f"Staged {len(placements)} actual footprints and {len(physical_pins)} unique pin numbers in {BOARD}")


if __name__ == "__main__":
    generate()
