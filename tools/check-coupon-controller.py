#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Validate the Coupon Rev A controller capture and complete XML netlist.

The source checker traces the deliberately constrained generated KiCad sheet.
The XML checker validates the complete matrix/driver/row/controller population.
Neither replaces native ERC, PCB DRC, RF review or bench measurements.
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
ROWS = runpy.run_path(str(TOOLS / "check-coupon-rows.py"))
LIB = runpy.run_path(str(TOOLS / "check-controller-libraries.py"))
A = MATRIX["AUDIT"]
parse, children, one, props = A["parse_sexpr"], A["children"], A["only_child"], A["property_map"]
PROJECT = A["PROJECT_DIR"]


PARTS = {
    "U3": ("ESP32-S3-WROOM-1U-N16R8", "ESP32-S3-WROOM-1U-N16R8", "rgb-badge-coupon:ESP32-S3-WROOM-1U"),
    "C3": ("GRM188R60J106ME47D", "10u 6.3V X5R", "rgb-badge-coupon:C_Murata_GRM18_0603"),
    "C4": ("GRM155R71C104KA88D", "100n 16V X7R", "rgb-badge-coupon:C_Murata_GRM15_0402"),
    "C5": ("GRM155C71A105KE11D", "1u 10V X7S", "rgb-badge-coupon:C_Murata_GRM15_0402"),
    "R43": ("ERJ-2RKF1002X", "10k 1%", "rgb-badge-coupon:R_Panasonic_ERJ2_0402"),
    "R44": ("ERJ-2RKF1002X", "10k 1%", "rgb-badge-coupon:R_Panasonic_ERJ2_0402"),
    "R45": ("ERJ-2RKF22R0X", "22R 1%", "rgb-badge-coupon:R_Panasonic_ERJ2_0402"),
    "R46": ("ERJ-2RKF22R0X", "22R 1%", "rgb-badge-coupon:R_Panasonic_ERJ2_0402"),
    "R47": ("ERJ-2RKF4990X", "499R 1%", "rgb-badge-coupon:R_Panasonic_ERJ2_0402"),
    "SW1": ("EVQP7J01P", "EVQP7J01P", "rgb-badge-coupon:SW_Panasonic_EVQP7J01P"),
}
PARTS.update({f"TP{i}": ("TestPoint_Pad", "TestPoint_Pad", "rgb-badge-coupon:TestPoint_Pad_D1.0mm") for i in range(2, 13)})

MODULE_NETS = {
    "1": "GND", "2": "+3V3_APP", "3": "ESP_EN", "4": "ROW_A0", "5": "ROW_A1",
    "6": "ROW_A2", "7": "ROW_A3", "10": "SYS_I2C_SDA", "11": "SYS_I2C_SCL",
    "12": "ROW_ENABLE_N", "13": "USB_DN_MCU", "14": "USB_DP_MCU",
    "17": "DISPLAY_ENABLE", "18": "LED_LAT", "19": "LED_SIN", "20": "LED_SCLK",
    "21": "LED_GCLK", "22": "LED_SOUT", "27": "MODE_BOOT_N", "36": "UART0_RX",
    "37": "UART0_TX_RAW", "40": "GND", "41": "GND",
}
MODULE_NC = set(map(str, range(1, 42))) - set(MODULE_NETS)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def library_pins(symbol):
    result = {}
    for unit in children(symbol, "symbol"):
        for pin in children(unit, "pin"):
            MATRIX["put_unique"](result, one(pin, "number", "pin")[1], pin, "library pin")
    return result


def expected_connections():
    result = {("U3", pin): net for pin, net in MODULE_NETS.items()}
    result.update({
        ("C3", "1"): "+3V3_APP", ("C3", "2"): "GND",
        ("C4", "1"): "+3V3_APP", ("C4", "2"): "GND",
        ("C5", "1"): "ESP_EN", ("C5", "2"): "GND",
        ("R43", "1"): "+3V3_APP", ("R43", "2"): "ESP_EN",
        ("R44", "1"): "+3V3_APP", ("R44", "2"): "MODE_BOOT_N",
        ("R45", "1"): "USB_DN_MCU", ("R45", "2"): "USB_D-",
        ("R46", "1"): "USB_DP_MCU", ("R46", "2"): "USB_D+",
        ("R47", "1"): "UART0_TX_RAW", ("R47", "2"): "UART0_TX",
        ("SW1", "1"): "MODE_BOOT_N", ("SW1", "2"): "GND",
    })
    for i, net in enumerate(("ESP_EN", "MODE_BOOT_N", "UART0_TX", "UART0_RX", "LED_GCLK",
                             "ROW_ENABLE_N", "+3V3_APP", "GND", "DISPLAY_ENABLE",
                             "SYS_I2C_SDA", "SYS_I2C_SCL"), 2):
        result[(f"TP{i}", "1")] = net
    return result


def expected_native_no_connects():
    """Return KiCad XML's one-node nets for explicit U3 no-connect markers."""
    pin_names = LIB["MODULE_PINS"]
    return {
        ("U3", pin): f"unconnected-(U3-{pin_names[int(pin)]}-Pad{pin})"
        for pin in MODULE_NC
    }


def mapping_difference(actual, expected):
    changed = []
    for key in sorted(set(actual) | set(expected)):
        if actual.get(key) != expected.get(key):
            changed.append(f"{key}: expected {expected.get(key)!r}, got {actual.get(key)!r}")
    return "; ".join(changed[:8]) + (f"; ... {len(changed) - 8} more" if len(changed) > 8 else "")


def check_sources(project=PROJECT):
    LIB["check_libraries"](project)
    root = parse(project / "rgb-badge-coupon.kicad_sch")
    sheets = children(root, "sheet")
    require(len(sheets) == 7, "Expected four matrix, driver, row and controller sheets")
    targets = [s for s in sheets if props(s)["Sheetfile"] == "controller.kicad_sch"]
    require(len(targets) == 1 and not children(root, "symbol"), "Controller sheet missing/duplicated or root contains components")
    sheet_uuid = one(targets[0], "uuid", "controller sheet")[1]
    instance_path = f'/{one(root, "uuid", "root")[1]}/{sheet_uuid}'
    source = parse(project / "controller.kicad_sch")
    require(one(source, "uuid", "controller")[1] == "8c76aba2-3e70-5442-9e12-3838cdcea085",
            "Unexpected controller-sheet file UUID")
    for forbidden in ("sheet", "bus", "label", "junction"):
        require(not children(source, forbidden), f"Controller source subset does not support {forbidden}")

    controlled = {s[1]: s for s in children(parse(project / "symbols" / "rgb-badge-coupon.kicad_sym"), "symbol")}
    cached = {}
    for symbol in children(one(source, "lib_symbols", "controller"), "symbol"):
        name = symbol[1].removeprefix("rgb-badge-coupon:")
        require(name in controlled and symbol == [symbol[0], "rgb-badge-coupon:" + name, *controlled[name][2:]],
                f"Embedded controller symbol differs from controlled library: {name}")
        cached[symbol[1]] = symbol

    graph, labels = defaultdict(set), defaultdict(set)
    for wire in children(source, "wire"):
        points = children(one(wire, "pts", "wire"), "xy")
        require(len(points) == 2, "Controller wire must have two endpoints")
        a, b = [tuple(map(D, point[1:])) for point in points]
        require(a != b and (a[0] == b[0] or a[1] == b[1]), "Controller wires must be nonzero and axis-aligned")
        graph[a].add(b); graph[b].add(a)
    for label in children(source, "global_label"):
        position = MATRIX["position"](label)
        labels[position].add(label[1])
        angle = one(label, "at", "label")[3]
        justification = one(one(label, "effects", "label"), "justify", "label")[1:]
        valid = {"0": ("left", -1), "180": ("right", 1)}
        require(angle in valid and justification == [valid[angle][0]], f"Unsupported controller label orientation: {label[1]}")
        require(len(graph[position]) == 1 and all((p[0] - position[0]) * valid[angle][1] > 0 for p in graph[position]),
                f"Wire crosses controller label text: {label[1]}")

    nc_positions = {MATRIX["position"](item) for item in children(source, "no_connect")}
    require(len(nc_positions) == len(children(source, "no_connect")), "Duplicate no-connect marker position")
    seen, connections, module_pin_positions = set(), {}, {}
    for symbol in children(source, "symbol"):
        p = props(symbol); ref = p["Reference"]
        require(ref not in seen and ref in PARTS, f"Unexpected/duplicate controller component: {ref}")
        seen.add(ref)
        mpn, value, footprint_name = PARTS[ref]
        is_tp = ref.startswith("TP")
        require((p["MPN"], p["Value"], p["Footprint"]) == (("" if is_tp else mpn), value, footprint_name),
                f"{ref}: wrong MPN/value/footprint")
        require(one(symbol, "lib_id", ref)[1] == "rgb-badge-coupon:" + mpn, f"{ref}: wrong library ID")
        require(one(symbol, "at", ref)[3] == "0" and one(symbol, "unit", ref)[1] == "1" and not children(symbol, "mirror"),
                f"{ref}: unsupported transform")
        require(one(symbol, "dnp", ref)[1] == "no", f"{ref}: unexpectedly DNP")
        require(one(symbol, "in_bom", ref)[1] == ("no" if is_tp else "yes") and one(symbol, "on_board", ref)[1] == "yes",
                f"{ref}: unintended BOM/board state")
        path = one(one(one(symbol, "instances", ref), "project", ref), "path", ref)
        require(path[1] == instance_path and one(path, "reference", ref)[1] == ref, f"{ref}: incorrect hierarchy path")
        x, y = MATRIX["position"](symbol)
        for number, pin in library_pins(cached[one(symbol, "lib_id", ref)[1]]).items():
            px, py = MATRIX["position"](pin); start = (x + px, y - py)
            if ref == "U3": module_pin_positions[number] = start
            pending, visited, names = [start], set(), set()
            while pending:
                point = pending.pop()
                if point in visited: continue
                visited.add(point); names.update(labels[point]); pending.extend(graph[point] - visited)
            if ref == "U3" and number in MODULE_NC:
                require(start in nc_positions and not names, f"U3.{number}: expected isolated no-connect")
            else:
                require(start not in nc_positions and len(names) == 1,
                        f"{ref}.{number}: expected one connected global net, found {sorted(names)}")
                connections[ref, number] = names.pop()
    require(seen == set(PARTS), "Controller population incomplete")
    require(nc_positions == {module_pin_positions[n] for n in MODULE_NC}, "No-connect markers differ from unused module pins")
    require(connections == expected_connections(), "Controller source pin-to-net mismatch")


def check_netlist(path):
    root = ET.parse(path).getroot()
    require(root.tag == "export", "Expected KiCad XML export")
    components, connections = {}, {}
    for comp in root.findall("./components/comp"):
        ref = comp.get("ref")
        if ref and ref.startswith("#FLG"): continue
        MATRIX["put_unique"](components, ref, (comp.findtext("value"), comp.findtext("footprint") or ""), "XML component")
    for net in root.findall("./nets/net"):
        for node in net.findall("node"):
            if node.get("ref", "").startswith("#FLG"): continue
            MATRIX["put_unique"](connections, (node.get("ref"), node.get("pin")), net.get("name"), "XML node")
    expected_components, expected_nets = MATRIX["expected_matrix"]()
    expected_components.update({ref: (value, footprint) for ref, (_, value, footprint) in DRIVER["PARTS"].items()})
    expected_components.update({ref: (value, footprint) for ref, (_, value, footprint) in ROWS["PARTS"].items()})
    expected_components.update({ref: (value, footprint) for ref, (_, value, footprint) in PARTS.items()})
    expected_nets.update(DRIVER["expected_connections"]())
    expected_nets.update(ROWS["expected_connections"]())
    expected_nets.update(expected_connections())
    expected_nets.update(expected_native_no_connects())
    require(components == expected_components, "Complete coupon XML population/value/footprint mismatch")
    require(connections == expected_nets,
            "Complete coupon XML pin-to-net mismatch: " + mapping_difference(connections, expected_nets))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-dir", type=Path, default=PROJECT)
    parser.add_argument("--netlist", type=Path)
    args = parser.parse_args()
    try:
        if args.netlist:
            check_netlist(args.netlist)
            print("KiCad XML complete coupon check passed: 356 PCB items, 1360 logical pins; matrix + driver + rows + controller.")
        else:
            check_sources(args.project_dir)
            print("Controller source connectivity check passed: N16R8 module, safe boot/reset, USB/UART boundaries and 11 test pads (not KiCad ERC).")
    except (OSError, ValueError, KeyError, IndexError, ET.ParseError) as error:
        print(f"Controller check failed: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
