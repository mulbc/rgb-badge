#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Audit exact row-decoder, MOSFET and gate-pull-up KiCad libraries.

This is an independent transcription check against the manufacturer package and
pin tables. It does not validate the not-yet-captured row schematic or replace
native KiCad ERC/DRC.
"""
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
    "74HC4514PW,118": {
        "footprint": "TSSOP_Nexperia_SOT355-1_24",
        "datasheet": "https://assets.nexperia.com/documents/data-sheet/74HC_HCT4514.pdf",
        "pins": {
            1: ("LE", "input"), 2: ("A0", "input"), 3: ("A1", "input"),
            4: ("Q7", "output"), 5: ("Q6", "output"), 6: ("Q5", "output"),
            7: ("Q4", "output"), 8: ("Q3", "output"), 9: ("Q1", "output"),
            10: ("Q2", "output"), 11: ("Q0", "output"), 12: ("GND", "power_in"),
            13: ("Q13", "output"), 14: ("Q12", "output"), 15: ("Q15", "output"),
            16: ("Q14", "output"), 17: ("Q9", "output"), 18: ("Q8", "output"),
            19: ("Q11", "output"), 20: ("Q10", "output"), 21: ("A2", "input"),
            22: ("A3", "input"), 23: ("E", "input"), 24: ("VCC", "power_in"),
        },
    },
    "DMP2066LSN-7": {
        "footprint": "SC59_Diodes_DMP2066LSN",
        "datasheet": "https://www.diodes.com/datasheet/download/DMP2066LSN.pdf",
        "pins": {1: ("G", "input"), 2: ("S", "passive"), 3: ("D", "passive")},
    },
    "2N7002K-7": {
        "footprint": "SOT23_Diodes_2N7002K",
        "datasheet": "https://www.diodes.com/assets/Datasheets/2N7002K.pdf",
        "pins": {1: ("G", "input"), 2: ("S", "passive"), 3: ("D", "passive")},
    },
    "ERJ-2RKF1001X": {
        "footprint": "R_Panasonic_ERJ2_0402",
        "datasheet": "https://industrial.panasonic.com/cdbs/www-data/pdf/RDA0000/AOA0000C304.pdf",
        "pins": {1: ("~", "passive"), 2: ("~", "passive")},
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


def decimal_list(values):
    return list(map(D, values))


def footprint_pads(project, footprint):
    path = project / "footprints" / "rgb-badge-coupon.pretty" / f"{footprint}.kicad_mod"
    root = parse(path)
    pads = children(root, "pad")
    result = {}
    for pad in pads:
        require(pad[1] not in result, f"{footprint}: duplicate pad {pad[1]}")
        result[pad[1]] = pad
    return root, result


def check_pad(pad, position, size, context):
    require(pad[2] == "smd", f"{context}: expected SMD pad")
    require(one(pad, "layers", context)[1:] == ["F.Cu", "F.Paste", "F.Mask"],
            f"{context}: copper/paste/mask layers differ from audit")
    require(decimal_list(one(pad, "at", context)[1:3]) == decimal_list(position),
            f"{context}: position differs from audit")
    require(decimal_list(one(pad, "size", context)[1:]) == decimal_list(size),
            f"{context}: size differs from audit")


def check_libraries(project=PROJECT):
    library_path = project / "symbols" / "rgb-badge-coupon.kicad_sym"
    symbols = {s[1]: s for s in children(parse(library_path), "symbol")}
    for mpn, audit in PARTS.items():
        require(mpn in symbols, f"missing exact row symbol {mpn}")
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
            require(pin[1] == electrical_type, f"{mpn}.{number}: electrical type mismatch")
            require(one(pin, "name", f"{mpn}.{number}")[1] == name,
                    f"{mpn}.{number}: pin name mismatch")
        if mpn == "74HC4514PW,118":
            require(pins["23"][2] == "inverted", "74HC4514 E pin must show active-low inversion")

    _, tssop = footprint_pads(project, "TSSOP_Nexperia_SOT355-1_24")
    require(set(tssop) == set(map(str, range(1, 25))), "SOT355-1 pad numbers mismatch")
    for number in range(1, 25):
        if number <= 12:
            position = ("-2.8625", str(D("-3.575") + D("0.65") * (number - 1)))
        else:
            position = ("2.8625", str(D("3.575") - D("0.65") * (number - 13)))
        check_pad(tssop[str(number)], position, ("1.475", "0.4"), f"SOT355-1 pad {number}")

    sc59_root, sc59 = footprint_pads(project, "SC59_Diodes_DMP2066LSN")
    require(set(sc59) == {"1", "2", "3"}, "SC-59 pad numbers mismatch")
    for number, position in {"1": ("-0.675", "1.2"), "2": ("0.675", "1.2"), "3": ("0", "-1.2")}.items():
        check_pad(sc59[number], position, ("0.8", "1.0"), f"SC-59 pad {number}")

    sot23_root, sot23 = footprint_pads(project, "SOT23_Diodes_2N7002K")
    require(set(sot23) == {"1", "2", "3"}, "SOT23 pad numbers mismatch")
    for number, position in {"1": ("-0.675", "1.0"), "2": ("0.675", "1.0"), "3": ("0", "-1.0")}.items():
        check_pad(sot23[number], position, ("0.8", "0.9"), f"SOT23 pad {number}")

    for root, name, expected in (
        (sc59_root, "SC-59", ("-1.25", "1.72")),
        (sot23_root, "SOT23", ("-1.25", "1.48")),
    ):
        marker = one(root, "fp_circle", f"{name} pin-1 marker")
        require(one(marker, "center", f"{name} pin-1 marker")[1:] == list(expected),
                f"{name}: pin-1 marker mismatch")

    # The exact 1 kΩ part intentionally reuses the already audited 0402 land pattern.
    _, resistor = footprint_pads(project, "R_Panasonic_ERJ2_0402")
    require(set(resistor) == {"1", "2"}, "row pull-up resistor pad numbers mismatch")
    return symbols


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-dir", type=Path, default=PROJECT)
    args = parser.parse_args()
    try:
        check_libraries(args.project_dir)
        print("Row-selection library checks passed:")
        print("- 24 decoder pins match the Nexperia SOT355-1 pin table")
        print("- P/N MOSFET gate, source and drain pins match Diodes top views")
        print("- three package land patterns and polarity marks match the audit")
        print("- exact 1 kOhm gate pull-up reuses the audited 0402 footprint")
    except (OSError, ValueError, KeyError, IndexError) as error:
        print(f"Row library check failed: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
