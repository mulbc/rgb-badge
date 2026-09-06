#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0

"""Deterministically audit the Coupon Rev A LED symbols and footprints."""

from __future__ import annotations

import json
import math
import sys
from dataclasses import dataclass
from decimal import Decimal
from pathlib import Path
from typing import TypeAlias


Atom: TypeAlias = str
SExpr: TypeAlias = list["Atom | SExpr"]

REPO_ROOT = Path(__file__).resolve().parent.parent
PROJECT_DIR = REPO_ROOT / "hardware" / "coupon" / "rev-a"
SYMBOL_LIBRARY = PROJECT_DIR / "symbols" / "rgb-badge-coupon.kicad_sym"
FOOTPRINT_LIBRARY = PROJECT_DIR / "footprints" / "rgb-badge-coupon.pretty"
PIXEL_PITCH = Decimal("1.95")


@dataclass(frozen=True)
class Pad:
    x: Decimal
    y: Decimal
    width: Decimal
    height: Decimal


PARTS = {
    "EAST10105RGBA0": {
        "footprint_file": "LED_Everlight_EAST10105RGBA0.kicad_mod",
        "footprint_name": "LED_Everlight_EAST10105RGBA0",
        "footprint_property": "rgb-badge-coupon:LED_Everlight_EAST10105RGBA0",
        "datasheet": "https://www.mouser.com/datasheet/2/143/EAST10105RGBA0-1709851.pdf",
        "manufacturer": "Everlight Electronics",
        "revision": "DSE-0014497 Rev.1, 2015-12-24",
        "pins": {"A": "1", "R_K": "2", "G_K": "4", "B_K": "3"},
        "pads": {
            "1": Pad(Decimal("0.425"), Decimal("-0.425"), Decimal("0.45"), Decimal("0.45")),
            "2": Pad(Decimal("0.425"), Decimal("0.425"), Decimal("0.45"), Decimal("0.45")),
            "3": Pad(Decimal("-0.425"), Decimal("0.425"), Decimal("0.45"), Decimal("0.45")),
            "4": Pad(Decimal("-0.425"), Decimal("-0.425"), Decimal("0.45"), Decimal("0.45")),
        },
        "envelope": (Decimal("1.30"), Decimal("1.30")),
        "courtyard": (
            (Decimal("-0.85"), Decimal("-0.85")),
            (Decimal("0.85"), Decimal("0.85")),
        ),
        "fab_pin1_points": {
            (Decimal("0.3"), Decimal("-0.5")),
            (Decimal("0.5"), Decimal("-0.3")),
        },
    },
    "QBLP1515A-RGB2A": {
        "footprint_file": "LED_QTBrightek_QBLP1515A-RGB2A.kicad_mod",
        "footprint_name": "LED_QTBrightek_QBLP1515A-RGB2A",
        "footprint_property": "rgb-badge-coupon:LED_QTBrightek_QBLP1515A-RGB2A",
        "datasheet": "https://www.qt-brightek.com/datasheet/QBLP1515A-RGB2A.pdf",
        "manufacturer": "QT Brightek",
        "revision": "Version 1.0, 2025-12-16",
        "pins": {"A": "1", "R_K": "4", "G_K": "3", "B_K": "2"},
        "pads": {
            "1": Pad(Decimal("0.7"), Decimal("0.4"), Decimal("0.6"), Decimal("0.4")),
            "2": Pad(Decimal("-0.7"), Decimal("0.4"), Decimal("0.6"), Decimal("0.4")),
            "3": Pad(Decimal("-0.7"), Decimal("-0.4"), Decimal("0.6"), Decimal("0.4")),
            "4": Pad(Decimal("0.7"), Decimal("-0.4"), Decimal("0.6"), Decimal("0.4")),
        },
        "envelope": (Decimal("2.00"), Decimal("1.20")),
        "courtyard": (
            (Decimal("-1.1"), Decimal("-0.85")),
            (Decimal("1.1"), Decimal("0.85")),
        ),
        "fab_pin1_points": {
            (Decimal("0.775"), Decimal("0.5")),
            (Decimal("0.525"), Decimal("0.75")),
        },
    },
}


def abort(message: str) -> None:
    raise ValueError(message)


def parse_sexpr(path: Path) -> SExpr:
    """Parse the strict S-expression subset used by the controlled KiCad files."""

    source = path.read_text(encoding="utf-8")
    roots: list[SExpr] = []
    stack: list[SExpr] = []
    index = 0

    while index < len(source):
        character = source[index]
        if character.isspace():
            index += 1
            continue
        if character == "(":
            expression: SExpr = []
            if stack:
                stack[-1].append(expression)
            else:
                roots.append(expression)
            stack.append(expression)
            index += 1
            continue
        if character == ")":
            if not stack:
                abort(f"{path}: unexpected ')' at byte {index}")
            stack.pop()
            index += 1
            continue
        if not stack:
            abort(f"{path}: atom outside a root expression at byte {index}")

        if character == '"':
            end = index + 1
            escaped = False
            while end < len(source):
                if source[end] == '"' and not escaped:
                    break
                if source[end] == "\\" and not escaped:
                    escaped = True
                else:
                    escaped = False
                end += 1
            if end >= len(source):
                abort(f"{path}: unterminated string at byte {index}")
            try:
                atom = json.loads(source[index : end + 1])
            except json.JSONDecodeError as error:
                abort(f"{path}: invalid quoted string at byte {index}: {error}")
            stack[-1].append(atom)
            index = end + 1
            continue

        end = index
        while end < len(source) and not source[end].isspace() and source[end] not in "()":
            end += 1
        if end == index:
            abort(f"{path}: cannot parse byte {index}")
        stack[-1].append(source[index:end])
        index = end

    if stack:
        abort(f"{path}: {len(stack)} unclosed expression(s)")
    if len(roots) != 1:
        abort(f"{path}: expected one root expression, found {len(roots)}")
    return roots[0]


def children(expression: SExpr, name: str) -> list[SExpr]:
    return [
        item
        for item in expression[1:]
        if isinstance(item, list) and item and item[0] == name
    ]


def only_child(expression: SExpr, name: str, context: str) -> SExpr:
    matches = children(expression, name)
    if len(matches) != 1:
        abort(f"{context}: expected one '{name}' expression, found {len(matches)}")
    return matches[0]


def atom_at(expression: SExpr, position: int, context: str) -> str:
    try:
        value = expression[position]
    except IndexError:
        abort(f"{context}: missing item {position}")
    if not isinstance(value, str):
        abort(f"{context}: item {position} is not an atom")
    return value


def property_map(expression: SExpr) -> dict[str, str]:
    properties: dict[str, str] = {}
    for item in children(expression, "property"):
        name = atom_at(item, 1, "property name")
        value = atom_at(item, 2, f"property {name}")
        if name in properties:
            abort(f"duplicate property '{name}'")
        properties[name] = value
    return properties


def point_list(expression: SExpr, context: str) -> list[tuple[Decimal, Decimal]]:
    points_expression = only_child(expression, "pts", context)
    points: list[tuple[Decimal, Decimal]] = []
    for point in children(points_expression, "xy"):
        points.append(
            (
                Decimal(atom_at(point, 1, context)),
                Decimal(atom_at(point, 2, context)),
            )
        )
    if not points:
        abort(f"{context}: no points")
    return points


def layer_name(expression: SExpr, context: str) -> str:
    return atom_at(only_child(expression, "layer", context), 1, context)


def assert_equal(actual: object, expected: object, context: str) -> None:
    if actual != expected:
        abort(f"{context}: expected {expected!r}, found {actual!r}")


def check_symbols() -> None:
    root = parse_sexpr(SYMBOL_LIBRARY)
    assert_equal(atom_at(root, 0, str(SYMBOL_LIBRARY)), "kicad_symbol_lib", "symbol root")

    symbols = {
        atom_at(symbol, 1, "symbol name"): symbol
        for symbol in children(root, "symbol")
    }

    for mpn, expected in PARTS.items():
        symbol = symbols.get(mpn)
        if symbol is None:
            abort(f"symbol library: missing exact symbol '{mpn}'")
        properties = property_map(symbol)
        for property_name, property_value in {
            "Value": mpn,
            "Footprint": expected["footprint_property"],
            "Datasheet": expected["datasheet"],
            "Manufacturer": expected["manufacturer"],
            "MPN": mpn,
            "Datasheet Revision": expected["revision"],
        }.items():
            assert_equal(
                properties.get(property_name),
                property_value,
                f"{mpn} symbol property {property_name}",
            )

        pins: dict[str, str] = {}
        for unit in children(symbol, "symbol"):
            for pin in children(unit, "pin"):
                assert_equal(atom_at(pin, 1, f"{mpn} pin type"), "passive", f"{mpn} pin type")
                pin_name = atom_at(only_child(pin, "name", f"{mpn} pin"), 1, f"{mpn} pin name")
                pin_number = atom_at(only_child(pin, "number", f"{mpn} pin"), 1, f"{mpn} pin number")
                if pin_name in pins:
                    abort(f"{mpn}: duplicate pin name '{pin_name}'")
                pins[pin_name] = pin_number
        assert_equal(pins, expected["pins"], f"{mpn} symbol pin map")


def check_footprint(mpn: str, expected: dict[str, object]) -> dict[str, Pad]:
    path = FOOTPRINT_LIBRARY / str(expected["footprint_file"])
    root = parse_sexpr(path)
    assert_equal(atom_at(root, 0, str(path)), "footprint", f"{mpn} footprint root")
    assert_equal(atom_at(root, 1, str(path)), expected["footprint_name"], f"{mpn} footprint name")
    assert_equal(layer_name(root, f"{mpn} footprint"), "F.Cu", f"{mpn} footprint layer")

    properties = property_map(root)
    assert_equal(properties.get("Datasheet"), expected["datasheet"], f"{mpn} footprint datasheet")
    if mpn not in properties.get("Description", ""):
        abort(f"{mpn} footprint description does not contain the exact MPN")
    description = atom_at(only_child(root, "descr", f"{mpn} footprint"), 1, f"{mpn} description")
    if expected["datasheet"] not in description:
        abort(f"{mpn} footprint description does not contain the controlled datasheet URL")

    actual_pads: dict[str, Pad] = {}
    for pad_expression in children(root, "pad"):
        pad_number = atom_at(pad_expression, 1, f"{mpn} pad")
        assert_equal(atom_at(pad_expression, 2, f"{mpn} pad {pad_number}"), "smd", f"{mpn} pad {pad_number} type")
        assert_equal(atom_at(pad_expression, 3, f"{mpn} pad {pad_number}"), "rect", f"{mpn} pad {pad_number} shape")
        at = only_child(pad_expression, "at", f"{mpn} pad {pad_number}")
        size = only_child(pad_expression, "size", f"{mpn} pad {pad_number}")
        layers = only_child(pad_expression, "layers", f"{mpn} pad {pad_number}")
        assert_equal(
            [atom_at(layers, index, f"{mpn} pad {pad_number} layers") for index in range(1, len(layers))],
            ["F.Cu", "F.Mask", "F.Paste"],
            f"{mpn} pad {pad_number} layers",
        )
        if pad_number in actual_pads:
            abort(f"{mpn}: duplicate footprint pad '{pad_number}'")
        actual_pads[pad_number] = Pad(
            Decimal(atom_at(at, 1, f"{mpn} pad {pad_number} X")),
            Decimal(atom_at(at, 2, f"{mpn} pad {pad_number} Y")),
            Decimal(atom_at(size, 1, f"{mpn} pad {pad_number} width")),
            Decimal(atom_at(size, 2, f"{mpn} pad {pad_number} height")),
        )
    assert_equal(actual_pads, expected["pads"], f"{mpn} footprint pads")

    left = min(pad.x - pad.width / 2 for pad in actual_pads.values())
    right = max(pad.x + pad.width / 2 for pad in actual_pads.values())
    top = min(pad.y - pad.height / 2 for pad in actual_pads.values())
    bottom = max(pad.y + pad.height / 2 for pad in actual_pads.values())
    assert_equal((right - left, bottom - top), expected["envelope"], f"{mpn} copper envelope")

    courtyards = [item for item in children(root, "fp_rect") if layer_name(item, f"{mpn} rectangle") == "F.CrtYd"]
    if len(courtyards) != 1:
        abort(f"{mpn}: expected one F.CrtYd rectangle, found {len(courtyards)}")
    courtyard = courtyards[0]
    start = only_child(courtyard, "start", f"{mpn} courtyard")
    end = only_child(courtyard, "end", f"{mpn} courtyard")
    actual_courtyard = (
        (Decimal(atom_at(start, 1, f"{mpn} courtyard")), Decimal(atom_at(start, 2, f"{mpn} courtyard"))),
        (Decimal(atom_at(end, 1, f"{mpn} courtyard")), Decimal(atom_at(end, 2, f"{mpn} courtyard"))),
    )
    assert_equal(actual_courtyard, expected["courtyard"], f"{mpn} courtyard")

    silk_polygons = [item for item in children(root, "fp_poly") if layer_name(item, f"{mpn} polygon") == "F.SilkS"]
    fab_polygons = [item for item in children(root, "fp_poly") if layer_name(item, f"{mpn} polygon") == "F.Fab"]
    if len(silk_polygons) != 1 or len(fab_polygons) != 1:
        abort(f"{mpn}: expected one silk pin-1 marker and one fab body polygon")
    silk_points = point_list(silk_polygons[0], f"{mpn} silk pin-1 marker")
    pad_one = actual_pads["1"]
    silk_centroid = (
        sum(point[0] for point in silk_points) / len(silk_points),
        sum(point[1] for point in silk_points) / len(silk_points),
    )
    if (silk_centroid[0] * pad_one.x) <= 0 or (silk_centroid[1] * pad_one.y) <= 0:
        abort(f"{mpn}: silk polarity marker is not in the pad-1 quadrant")
    fab_points = set(point_list(fab_polygons[0], f"{mpn} fab body"))
    if not expected["fab_pin1_points"].issubset(fab_points):
        abort(f"{mpn}: fab pin-1 corner geometry changed")

    symbol_pins = expected["pins"]
    if set(symbol_pins.values()) != set(actual_pads):
        abort(f"{mpn}: symbol pin numbers do not match footprint pad numbers")
    return actual_pads


def rotate_pad_90(pad: Pad) -> Pad:
    return Pad(-pad.y, pad.x, pad.height, pad.width)


def translated_bounds(pad: Pad, x: Decimal, y: Decimal) -> tuple[Decimal, Decimal, Decimal, Decimal]:
    return (
        x + pad.x - pad.width / 2,
        y + pad.y - pad.height / 2,
        x + pad.x + pad.width / 2,
        y + pad.y + pad.height / 2,
    )


def checkerboard_clearance(pads: dict[str, Pad]) -> Decimal:
    rectangles: list[tuple[tuple[int, int], tuple[Decimal, Decimal, Decimal, Decimal]]] = []
    for row in range(4):
        for column in range(4):
            rotate = (row + column) % 2 == 1
            for pad in pads.values():
                placed_pad = rotate_pad_90(pad) if rotate else pad
                rectangles.append(
                    (
                        (row, column),
                        translated_bounds(
                            placed_pad,
                            Decimal(column) * PIXEL_PITCH,
                            Decimal(row) * PIXEL_PITCH,
                        ),
                    )
                )

    minimum_squared: Decimal | None = None
    for index, (cell_a, bounds_a) in enumerate(rectangles):
        for cell_b, bounds_b in rectangles[index + 1 :]:
            if cell_a == cell_b:
                continue
            left_a, top_a, right_a, bottom_a = bounds_a
            left_b, top_b, right_b, bottom_b = bounds_b
            gap_x = max(left_a - right_b, left_b - right_a, Decimal(0))
            gap_y = max(top_a - bottom_b, top_b - bottom_a, Decimal(0))
            squared = gap_x * gap_x + gap_y * gap_y
            if minimum_squared is None or squared < minimum_squared:
                minimum_squared = squared

    if minimum_squared is None:
        abort("checkerboard calculation did not compare any pads")
    return minimum_squared.sqrt()


def main() -> int:
    try:
        check_symbols()
        footprints = {
            mpn: check_footprint(mpn, expected)
            for mpn, expected in PARTS.items()
        }
        qtblp_envelope_width = PARTS["QBLP1515A-RGB2A"]["envelope"][0]
        uniform_overlap = qtblp_envelope_width - PIXEL_PITCH
        assert_equal(uniform_overlap, Decimal("0.05"), "uniform QBLP1515 overlap")
        minimum_clearance = checkerboard_clearance(footprints["QBLP1515A-RGB2A"])
        assert_equal(minimum_clearance, Decimal("0.35"), "QBLP1515 checkerboard clearance")
    except (OSError, ValueError) as error:
        print(f"LED library check failed: {error}", file=sys.stderr)
        return 1

    print("LED library checks passed:")
    print("- 2 exact-MPN symbol pin maps match 2 manufacturer pad maps")
    print("- footprint pad sizes, positions, layers, courtyards and polarity marks match the audit")
    print(f"- uniform QBLP1515 placement overlap: {uniform_overlap} mm")
    print(f"- 0/90-degree QBLP1515 checkerboard minimum copper clearance: {minimum_clearance} mm")
    return 0


if __name__ == "__main__":
    sys.exit(main())
