#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Validate the captured Coupon Rev A row selectors and complete XML netlist.

The source checker independently traces the deliberately simple symbols,
axis-aligned wires and global labels. The XML checker validates the complete
matrix + driver + row population exported by KiCad. Neither is ERC, DRC,
simulation, assembler DFM or bench measurement.
"""

import argparse
from collections import defaultdict
from decimal import Decimal as D
from pathlib import Path
import runpy
import sys
import xml.etree.ElementTree as ET


TOOLS = Path(__file__).resolve().parent
MATRIX = runpy.run_path(str(TOOLS / "check-coupon-matrix.py"))
DRIVER = runpy.run_path(str(TOOLS / "check-coupon-driver.py"))
ROW_LIB = runpy.run_path(str(TOOLS / "check-row-libraries.py"))
A = MATRIX["AUDIT"]
parse, children, one, props = A["parse_sexpr"], A["children"], A["only_child"], A["property_map"]
PROJECT = A["PROJECT_DIR"]


PARTS = {
    "U2": ("74HC4514PW,118", "74HC4514PW,118", "rgb-badge-coupon:TSSOP_Nexperia_SOT355-1_24"),
    "C2": ("GRM155R71C104KA88D", "100n 16V X7R", "rgb-badge-coupon:C_Murata_GRM15_0402"),
}
PARTS.update({f"Q{i + 1}": ("DMP2066LSN-7", "DMP2066LSN-7", "rgb-badge-coupon:SC59_Diodes_DMP2066LSN") for i in range(16)})
PARTS.update({f"Q{i + 17}": ("2N7002K-7", "2N7002K-7", "rgb-badge-coupon:SOT23_Diodes_2N7002K") for i in range(16)})
PARTS.update({f"R{i + 6}": ("ERJ-2RKF1001X", "1k 1%", "rgb-badge-coupon:R_Panasonic_ERJ2_0402") for i in range(16)})
PARTS.update({f"R{i + 22}": ("ERJ-2RKF1003X", "100k 1%", "rgb-badge-coupon:R_Panasonic_ERJ2_0402") for i in range(16)})
PARTS.update({f"R{i + 38}": ("ERJ-2RKF1003X", "100k 1%", "rgb-badge-coupon:R_Panasonic_ERJ2_0402") for i in range(4)})
PARTS["R42"] = ("ERJ-2RKF1003X", "100k 1%", "rgb-badge-coupon:R_Panasonic_ERJ2_0402")
FLAGS = {"#FLG03": "VLED"}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def library_pins(symbol):
    result = {}
    for unit in children(symbol, "symbol"):
        for pin in children(unit, "pin"):
            number = one(pin, "number", "pin")[1]
            MATRIX["put_unique"](result, number, pin, "library pin")
    return result


def expected_connections():
    result = {}
    decoder = {"VCC": "+3V3_APP", "GND": "GND", "LE": "+3V3_APP", "E": "ROW_ENABLE_N"}
    decoder.update({f"A{i}": f"ROW_A{i}" for i in range(4)})
    decoder.update({f"Q{i}": f"ROW_SEL_{i:02d}" for i in range(16)})
    for number, (name, _) in ROW_LIB["PARTS"]["74HC4514PW,118"]["pins"].items():
        result["U2", str(number)] = decoder[name]
    result.update({("C2", "1"): "+3V3_APP", ("C2", "2"): "GND"})
    for i in range(16):
        row = f"{i:02d}"
        result.update({
            (f"Q{i + 1}", "1"): f"ROW_GATE_{row}",
            (f"Q{i + 1}", "2"): "VLED",
            (f"Q{i + 1}", "3"): f"ROW_{row}_A",
            (f"Q{i + 17}", "1"): f"ROW_SEL_{row}",
            (f"Q{i + 17}", "2"): "GND",
            (f"Q{i + 17}", "3"): f"ROW_GATE_{row}",
            (f"R{i + 6}", "1"): "VLED",
            (f"R{i + 6}", "2"): f"ROW_GATE_{row}",
            (f"R{i + 22}", "1"): f"ROW_SEL_{row}",
            (f"R{i + 22}", "2"): "GND",
        })
    for i in range(4):
        result[f"R{i + 38}", "1"] = f"ROW_A{i}"
        result[f"R{i + 38}", "2"] = "GND"
    result.update({("R42", "1"): "+3V3_APP", ("R42", "2"): "ROW_ENABLE_N"})
    return result


def check_sources(project=PROJECT):
    ROW_LIB["check_libraries"](project)
    root = parse(project / "rgb-badge-coupon.kicad_sch")
    sheets = children(root, "sheet")
    require(len(sheets) == 6, "Expected four matrix, one driver and one row sheet")
    row_sheets = [sheet for sheet in sheets if props(sheet)["Sheetfile"] == "rows.kicad_sch"]
    require(len(row_sheets) == 1 and not children(root, "symbol"), "Row sheet missing/duplicated or root contains components")
    sheet_uuid = one(row_sheets[0], "uuid", "row sheet")[1]
    instance_path = f'/{one(root, "uuid", "root")[1]}/{sheet_uuid}'
    source = parse(project / "rows.kicad_sch")
    require(one(source, "uuid", "rows")[1] == "2a21bafc-2155-5152-9b8f-db9a5063a2ae", "Unexpected row-sheet file UUID")
    for forbidden in ("no_connect", "sheet", "bus", "label", "junction"):
        require(not children(source, forbidden), f"Row source subset does not support {forbidden}")

    controlled = {s[1]: s for s in children(parse(project / "symbols/rgb-badge-coupon.kicad_sym"), "symbol")}
    cached = {}
    for symbol in children(one(source, "lib_symbols", "rows"), "symbol"):
        name = symbol[1].removeprefix("rgb-badge-coupon:")
        require(name in controlled and symbol == [symbol[0], "rgb-badge-coupon:" + name, *controlled[name][2:]],
                f"Embedded row symbol differs from controlled library: {name}")
        cached[symbol[1]] = symbol

    graph, labels = defaultdict(set), defaultdict(set)
    for wire in children(source, "wire"):
        points = children(one(wire, "pts", "wire"), "xy")
        require(len(points) == 2, "Row wire must have two endpoints")
        a, b = [tuple(map(D, point[1:])) for point in points]
        require(a != b and (a[0] == b[0] or a[1] == b[1]), "Row wires must be nonzero and axis-aligned")
        graph[a].add(b)
        graph[b].add(a)
    for label in children(source, "global_label"):
        position = MATRIX["position"](label)
        labels[position].add(label[1])
        angle = one(label, "at", "label")[3]
        justification = one(one(label, "effects", "label"), "justify", "label")[1:]
        valid = {"0": ("left", -1), "180": ("right", 1)}
        require(angle in valid and justification == [valid[angle][0]], f"Unsupported row label orientation: {label[1]}")
        neighbours = graph[position]
        require(len(neighbours) == 1 and all((p[0] - position[0]) * valid[angle][1] > 0 for p in neighbours),
                f"Wire crosses row label text: {label[1]}")

    seen, connections = set(), {}
    for symbol in children(source, "symbol"):
        p = props(symbol)
        ref = p["Reference"]
        require(ref not in seen, f"Duplicate row reference: {ref}")
        seen.add(ref)
        virtual = ref in FLAGS
        require(ref in PARTS or virtual, f"Unexpected row component: {ref}")
        mpn, value, footprint = ("PWR_FLAG", "PWR_FLAG", "") if virtual else PARTS[ref]
        require((p["MPN"], p["Value"], p["Footprint"]) == (("" if virtual else mpn), value, footprint),
                f"{ref}: wrong MPN/value/footprint")
        require(one(symbol, "lib_id", ref)[1] == "rgb-badge-coupon:" + mpn, f"{ref}: wrong library ID")
        require(one(symbol, "at", ref)[3] == "0" and one(symbol, "unit", ref)[1] == "1" and not children(symbol, "mirror"),
                f"{ref}: unsupported transform")
        require(one(symbol, "dnp", ref)[1] == "no", f"{ref}: unexpectedly DNP")
        require(one(symbol, "in_bom", ref)[1] == ("no" if virtual else "yes") and
                one(symbol, "on_board", ref)[1] == ("no" if virtual else "yes"), f"{ref}: unintended BOM/board state")
        path = one(one(one(symbol, "instances", ref), "project", ref), "path", ref)
        require(path[1] == instance_path and one(path, "reference", ref)[1] == ref, f"{ref}: incorrect hierarchy path")
        x, y = MATRIX["position"](symbol)
        for number, pin in library_pins(cached[one(symbol, "lib_id", ref)[1]]).items():
            px, py = MATRIX["position"](pin)
            pending, visited, names = [(x + px, y - py)], set(), set()
            while pending:
                point = pending.pop()
                if point in visited:
                    continue
                visited.add(point)
                names.update(labels[point])
                pending.extend(graph[point] - visited)
            require(len(names) == 1, f"{ref}.{number}: expected one connected global net, found {sorted(names)}")
            connections[ref, number] = names.pop()
    require(seen == set(PARTS) | set(FLAGS), "Row population incomplete")
    expected = expected_connections() | {(ref, "1"): net for ref, net in FLAGS.items()}
    require(connections == expected, "Row source pin-to-net mismatch")


def check_netlist(path):
    root = ET.parse(path).getroot()
    require(root.tag == "export", "Expected KiCad XML export")
    components, connections = {}, {}
    for comp in root.findall("./components/comp"):
        ref = comp.get("ref")
        if ref and ref.startswith("#FLG"):
            continue
        MATRIX["put_unique"](components, ref, (comp.findtext("value"), comp.findtext("footprint") or ""), "XML component")
    for net in root.findall("./nets/net"):
        for node in net.findall("node"):
            if node.get("ref", "").startswith("#FLG"):
                continue
            MATRIX["put_unique"](connections, (node.get("ref"), node.get("pin")), net.get("name"), "XML node")
    expected_components, expected_nets = MATRIX["expected_matrix"]()
    expected_components.update({ref: (value, footprint) for ref, (_, value, footprint) in DRIVER["PARTS"].items()})
    expected_components.update({ref: (value, footprint) for ref, (_, value, footprint) in PARTS.items()})
    expected_nets.update(DRIVER["expected_connections"]())
    expected_nets.update(expected_connections())
    require(components == expected_components, "Complete coupon XML population/value/footprint mismatch")
    require(connections == expected_nets, "Complete coupon XML pin-to-net mismatch")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-dir", type=Path, default=PROJECT)
    parser.add_argument("--netlist", type=Path)
    args = parser.parse_args()
    try:
        if args.netlist:
            check_netlist(args.netlist)
            print("KiCad XML complete coupon check passed: 335 PCB items, 1290 physical pins; matrix + driver + row selectors.")
        else:
            check_sources(args.project_dir)
            print("Row source connectivity check passed: decoder, 16 P/N-MOSFET stages, 37 resistors, C2 and VLED boundary flag (not KiCad ERC).")
    except (OSError, ValueError, KeyError, IndexError, ET.ParseError) as error:
        print(f"Row check failed: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
