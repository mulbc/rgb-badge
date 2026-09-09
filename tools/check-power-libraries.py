#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Audit the first exact Coupon Rev A charger and power-converter libraries.

This checks a controlled transcription of manufacturer pin tables and land
patterns. It does not approve the power architecture, schematic, PCB layout,
thermal design, assembly process or battery pack.
"""

from collections import Counter
from decimal import Decimal as D
from pathlib import Path
import argparse
import runpy
import sys


LED = runpy.run_path(str(Path(__file__).with_name("check-led-libraries.py")))
parse, children, one = LED["parse_sexpr"], LED["children"], LED["only_child"]
property_map = LED["property_map"]
PROJECT = Path(__file__).resolve().parents[1] / "hardware" / "coupon" / "rev-a"
FP_PREFIX = "rgb-badge-coupon:"

PARTS = {
    "BQ25616JRTWT": {
        "footprint": "QFN_TI_RTW0024A_4x4mm_P0.5mm_EP2.7mm",
        "datasheet": "https://www.ti.com/lit/ds/symlink/bq25616.pdf",
        "pins": {
            1: ("VAC", "power_in"), 2: ("ACDRV", "output"),
            3: ("D+", "bidirectional"), 4: ("D-", "bidirectional"),
            5: ("STAT", "open_collector"), 6: ("OTG", "input"),
            7: ("PG", "open_collector"), 8: ("ILIM", "input"),
            9: ("CE", "input"), 10: ("ICHG", "input"),
            11: ("TS", "input"), 12: ("VSET", "input"),
            13: ("BAT", "power_in"), 14: ("BAT", "power_in"),
            15: ("SYS", "power_out"), 16: ("SYS", "power_out"),
            17: ("GND", "power_in"), 18: ("GND", "power_in"),
            19: ("SW", "passive"), 20: ("SW", "passive"),
            21: ("BTST", "passive"), 22: ("REGN", "power_out"),
            23: ("PMID", "power_out"), 24: ("VBUS", "power_in"),
            25: ("GND_EP", "power_in"),
        },
    },
    "TPS631000DRLR": {
        "footprint": "SOT5X3_TI_DRL0008A",
        "datasheet": "https://www.ti.com/lit/ds/symlink/tps631000.pdf",
        "pins": {
            1: ("VOUT", "power_out"), 2: ("LX2", "passive"),
            3: ("LX1", "passive"), 4: ("VIN", "power_in"),
            5: ("EN", "input"), 6: ("MODE", "input"),
            7: ("GND", "power_in"), 8: ("FB", "input"),
        },
    },
}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def library_pins(symbol):
    result = {}
    for unit in children(symbol, "symbol"):
        for pin in children(unit, "pin"):
            number = one(pin, "number", "pin")[1]
            require(number not in result, f"duplicate library pin {number}")
            result[number] = pin
    return result


def footprint(project, name):
    path = project / "footprints" / "rgb-badge-coupon.pretty" / f"{name}.kicad_mod"
    return parse(path)


def dec(values):
    return tuple(map(D, values))


def pad_position(pad):
    return dec(one(pad, "at", "pad")[1:3])


def pad_size(pad):
    return dec(one(pad, "size", "pad")[1:])


def pad_layers(pad):
    return one(pad, "layers", "pad")[1:]


def check_symbol_libraries(project):
    library = parse(project / "symbols" / "rgb-badge-coupon.kicad_sym")
    symbols = {symbol[1]: symbol for symbol in children(library, "symbol")}
    for mpn, audit in PARTS.items():
        require(mpn in symbols, f"missing exact power symbol {mpn}")
        symbol = symbols[mpn]
        properties = property_map(symbol)
        require(properties.get("MPN") == mpn, f"{mpn}: MPN property mismatch")
        require(properties.get("Footprint") == FP_PREFIX + audit["footprint"],
                f"{mpn}: footprint property mismatch")
        require(properties.get("Datasheet") == audit["datasheet"],
                f"{mpn}: datasheet property mismatch")
        pins = library_pins(symbol)
        require(set(pins) == set(map(str, audit["pins"])), f"{mpn}: pin numbers mismatch")
        for number, (name, electrical_type) in audit["pins"].items():
            pin = pins[str(number)]
            require(one(pin, "name", f"{mpn}.{number}")[1] == name,
                    f"{mpn}.{number}: pin name mismatch")
            require(pin[1] == electrical_type, f"{mpn}.{number}: electrical type mismatch")
    require(library_pins(symbols["BQ25616JRTWT"])["9"][2] == "inverted",
            "BQ25616J CE must show active-low inversion")
    return symbols


def check_rtw_footprint(project):
    root = footprint(project, "QFN_TI_RTW0024A_4x4mm_P0.5mm_EP2.7mm")
    pads = children(root, "pad")
    numbered = {pad[1]: pad for pad in pads if pad[1]}
    require(set(numbered) == set(map(str, range(1, 26))), "RTW pad numbers mismatch")
    for number in range(1, 25):
        pad = numbered[str(number)]
        if number <= 6:
            position = (D("-1.975"), D("-1.25") + D("0.5") * (number - 1))
            size = (D("0.85"), D("0.28"))
        elif number <= 12:
            position = (D("-1.25") + D("0.5") * (number - 7), D("1.975"))
            size = (D("0.28"), D("0.85"))
        elif number <= 18:
            position = (D("1.975"), D("1.25") - D("0.5") * (number - 13))
            size = (D("0.85"), D("0.28"))
        else:
            position = (D("1.25") - D("0.5") * (number - 19), D("-1.975"))
            size = (D("0.28"), D("0.85"))
        require(pad_position(pad) == position, f"RTW pad {number} position mismatch")
        require(pad_size(pad) == size, f"RTW pad {number} size mismatch")
        require(pad_layers(pad) == ["F.Cu", "F.Paste", "F.Mask"],
                f"RTW pad {number} layer mismatch")
    ep = numbered["25"]
    require(pad_position(ep) == (D("0"), D("0")), "RTW exposed-pad position mismatch")
    require(pad_size(ep) == (D("3.1"), D("3.1")), "RTW exposed-pad size mismatch")
    require(pad_layers(ep) == ["F.Cu", "F.Mask"], "RTW exposed-pad layers mismatch")
    paste = [pad for pad in pads if not pad[1]]
    require(len(paste) == 4, "RTW stencil aperture count mismatch")
    require({pad_position(pad) for pad in paste} == {
        (D("-0.7"), D("-0.7")), (D("0.7"), D("-0.7")),
        (D("-0.7"), D("0.7")), (D("0.7"), D("0.7")),
    }, "RTW stencil aperture positions mismatch")
    require(all(pad_size(pad) == (D("1.1"), D("1.1")) for pad in paste),
            "RTW stencil aperture size mismatch")
    require(all(pad_layers(pad) == ["F.Paste"] for pad in paste),
            "RTW stencil aperture layers mismatch")
    marker = one(root, "fp_circle", "RTW pin-1 marker")
    require(dec(one(marker, "center", "RTW pin-1 marker")[1:]) == (D("-2.45"), D("-1.65")),
            "RTW pin-1 marker mismatch")


def check_drl_footprint(project):
    root = footprint(project, "SOT5X3_TI_DRL0008A")
    pads = children(root, "pad")
    require(Counter(pad[1] for pad in pads) == Counter(map(str, range(1, 9))),
            "DRL pad numbers mismatch")
    by_number = {pad[1]: pad for pad in pads}
    for number in range(1, 9):
        if number <= 4:
            position = (D("-0.74"), D("-0.75") + D("0.5") * (number - 1))
        else:
            position = (D("0.74"), D("0.75") - D("0.5") * (number - 5))
        pad = by_number[str(number)]
        require(pad_position(pad) == position, f"DRL pad {number} position mismatch")
        require(pad_size(pad) == (D("0.67"), D("0.3")), f"DRL pad {number} size mismatch")
        require(pad_layers(pad) == ["F.Cu", "F.Paste", "F.Mask"],
                f"DRL pad {number} layer mismatch")
    marker = one(root, "fp_circle", "DRL pin-1 marker")
    require(dec(one(marker, "center", "DRL pin-1 marker")[1:]) == (D("-1.25"), D("-1.20")),
            "DRL pin-1 marker mismatch")


def check_libraries(project=PROJECT):
    symbols = check_symbol_libraries(project)
    check_rtw_footprint(project)
    check_drl_footprint(project)
    return symbols


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-dir", type=Path, default=PROJECT)
    args = parser.parse_args()
    try:
        check_libraries(args.project_dir)
        print("Power library phase-one checks passed:")
        print("- 25 BQ25616J pins match the TI RTW pin table and exposed-pad map")
        print("- RTW signal lands and four-way stencil segmentation match TI drawing 4211120-3/D")
        print("- 8 TPS631000 pins and DRL lands match the current TI pin/package drawings")
        print("- blocked USB-C, tiny X2QFN, LED-rail and fuel-gauge footprints were not guessed")
    except (OSError, ValueError, KeyError, IndexError) as error:
        print(f"Power library check failed: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
