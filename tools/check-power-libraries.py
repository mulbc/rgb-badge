#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Audit the controlled Coupon Rev A power/input component libraries.

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
    "TLV75533PDBVR": {
        "footprint": "SOT23_TI_DBV0005A",
        "datasheet": "https://www.ti.com/lit/ds/symlink/tlv755p.pdf",
        "pins": {
            1: ("IN", "power_in"), 2: ("GND", "power_in"),
            3: ("EN", "input"), 4: ("NC", "passive"),
            5: ("OUT", "power_out"),
        },
    },
    "SN74LVC1G04DBVR": {
        "footprint": "SOT23_TI_DBV0005A",
        "datasheet": "https://www.ti.com/lit/ds/symlink/sn74lvc1g04.pdf",
        "pins": {
            1: ("NC", "passive"), 2: ("A", "input"),
            3: ("GND", "power_in"), 4: ("Y", "output"),
            5: ("VCC", "power_in"),
        },
    },
    "INA232AIDDFR": {
        "footprint": "SOT23_THIN_TI_DDF0008A",
        "datasheet": "https://www.ti.com/lit/ds/symlink/ina232.pdf",
        "pins": {
            1: ("IN+", "input"), 2: ("IN-", "input"),
            3: ("GND", "power_in"), 4: ("VS", "power_in"),
            5: ("SCL", "input"), 6: ("SDA", "bidirectional"),
            7: ("A0", "input"), 8: ("ALERT", "open_collector"),
        },
    },
    "TPD4E05U06DQAR": {
        "footprint": "USON_TI_DQA0010A",
        "datasheet": "https://www.ti.com/lit/ds/symlink/tpd4e05u06.pdf",
        "pins": {
            1: ("D1+", "passive"), 2: ("D1-", "passive"),
            3: ("GND", "power_in"), 4: ("D2+", "passive"),
            5: ("D2-", "passive"), 6: ("NC", "passive"),
            7: ("NC", "passive"), 8: ("GND", "power_in"),
            9: ("NC", "passive"), 10: ("NC", "passive"),
        },
    },
    "TUSB320LAIRWBR": {
        "footprint": "X2QFN_TI_RWB0012A_1.6x1.6mm_P0.4mm",
        "datasheet": "https://www.ti.com/lit/ds/symlink/tusb320lai.pdf",
        "pins": {
            1: ("CC1", "bidirectional"), 2: ("CC2", "bidirectional"),
            3: ("PORT", "input"), 4: ("VBUS_DET", "input"),
            5: ("ADDR", "input"), 6: ("INT_N/OUT3", "open_collector"),
            7: ("SDA/OUT1", "bidirectional"), 8: ("SCL/OUT2", "bidirectional"),
            9: ("ID", "open_collector"), 10: ("GND", "power_in"),
            11: ("EN_N", "input"), 12: ("VDD", "power_in"),
        },
    },
    "TPS63020DSJT": {
        "footprint": "VSON_TI_DSJ0014_4x3mm_P0.5mm_EP2.85x1.58mm",
        "datasheet": "https://www.ti.com/lit/ds/symlink/tps63020.pdf",
        "pins": {
            1: ("VINA", "power_in"), 2: ("GND", "power_in"),
            3: ("FB", "input"), 4: ("VOUT", "power_out"),
            5: ("VOUT", "power_out"), 6: ("L2", "passive"),
            7: ("L2", "passive"), 8: ("L1", "passive"),
            9: ("L1", "passive"), 10: ("VIN", "power_in"),
            11: ("VIN", "power_in"), 12: ("EN", "input"),
            13: ("PS/SYNC", "input"), 14: ("PG", "open_collector"),
            15: ("PGND_EP", "power_in"),
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
    require(library_pins(symbols["SN74LVC1G04DBVR"])["4"][2] == "inverted",
            "SN74LVC1G04 output must show inversion")
    require(library_pins(symbols["TUSB320LAIRWBR"])["11"][2] == "inverted",
            "TUSB320LAI EN_N must show active-low inversion")
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


def check_simple_gullwing(project, name, expected_positions, expected_size, marker_position):
    root = footprint(project, name)
    pads = children(root, "pad")
    require(Counter(pad[1] for pad in pads) == Counter(expected_positions.keys()),
            f"{name} pad numbers mismatch")
    by_number = {pad[1]: pad for pad in pads}
    for number, position in expected_positions.items():
        pad = by_number[number]
        require(pad_position(pad) == dec(position), f"{name} pad {number} position mismatch")
        require(pad_size(pad) == dec(expected_size), f"{name} pad {number} size mismatch")
        require(pad_layers(pad) == ["F.Cu", "F.Paste", "F.Mask"],
                f"{name} pad {number} layer mismatch")
    marker = one(root, "fp_circle", f"{name} pin-1 marker")
    require(dec(one(marker, "center", f"{name} pin-1 marker")[1:]) == dec(marker_position),
            f"{name} pin-1 marker mismatch")


def check_phase_two_footprints(project):
    check_simple_gullwing(project, "SOT23_TI_DBV0005A", {
        "1": ("-1.3", "-0.95"), "2": ("-1.3", "0"), "3": ("-1.3", "0.95"),
        "4": ("1.3", "0.95"), "5": ("1.3", "-0.95"),
    }, ("1.1", "0.6"), ("-2.05", "-1.45"))
    check_simple_gullwing(project, "SOT23_THIN_TI_DDF0008A", {
        "1": ("-1.3", "-0.975"), "2": ("-1.3", "-0.325"),
        "3": ("-1.3", "0.325"), "4": ("-1.3", "0.975"),
        "5": ("1.3", "0.975"), "6": ("1.3", "0.325"),
        "7": ("1.3", "-0.325"), "8": ("1.3", "-0.975"),
    }, ("1.05", "0.45"), ("-2.05", "-1.45"))

    root = footprint(project, "USON_TI_DQA0010A")
    pads = children(root, "pad")
    require(Counter(pad[1] for pad in pads) == Counter(map(str, range(1, 11))),
            "DQA0010A pad numbers mismatch")
    by_number = {pad[1]: pad for pad in pads}
    for number in range(1, 11):
        if number <= 5:
            position = (D("-0.4175"), D("-1.0") + D("0.5") * (number - 1))
        else:
            position = (D("0.4175"), D("1.0") - D("0.5") * (number - 6))
        pad = by_number[str(number)]
        size = (D("0.565"), D("0.4") if number in (3, 8) else D("0.2"))
        require(pad_position(pad) == position, f"DQA0010A pad {number} position mismatch")
        require(pad_size(pad) == size, f"DQA0010A pad {number} size mismatch")
        require(pad_layers(pad) == ["F.Cu", "F.Paste", "F.Mask"],
                f"DQA0010A pad {number} layer mismatch")
    marker = one(root, "fp_circle", "DQA0010A pin-1 marker")
    require(dec(one(marker, "center", "DQA0010A pin-1 marker")[1:]) ==
            (D("-0.95"), D("-1.35")), "DQA0010A pin-1 marker mismatch")


def check_rwb_footprint(project):
    root = footprint(project, "X2QFN_TI_RWB0012A_1.6x1.6mm_P0.4mm")
    pads = children(root, "pad")
    numbered = {pad[1]: pad for pad in pads if pad[1]}
    require(set(numbered) == set(map(str, range(1, 13))), "RWB0012A pad numbers mismatch")
    positions = {
        "1": ("-0.65", "-0.20"), "2": ("-0.65", "0.20"),
        "3": ("-0.60", "0.75"), "4": ("-0.20", "0.75"),
        "5": ("0.20", "0.75"), "6": ("0.60", "0.75"),
        "7": ("0.65", "0.20"), "8": ("0.65", "-0.20"),
        "9": ("0.60", "-0.75"), "10": ("0.20", "-0.75"),
        "11": ("-0.20", "-0.75"), "12": ("-0.60", "-0.75"),
    }
    side_numbers = {"1", "2", "7", "8"}
    for number, position in positions.items():
        pad = numbered[number]
        require(pad_position(pad) == dec(position), f"RWB0012A pad {number} position mismatch")
        size = (D("0.70"), D("0.20")) if number in side_numbers else (D("0.20"), D("0.50"))
        require(pad_size(pad) == size, f"RWB0012A pad {number} size mismatch")
        layers = ["F.Cu", "F.Mask"] if number in side_numbers else ["F.Cu", "F.Paste", "F.Mask"]
        require(pad_layers(pad) == layers, f"RWB0012A pad {number} layer mismatch")
    paste = [pad for pad in pads if not pad[1]]
    require(len(paste) == 4, "RWB0012A side stencil aperture count mismatch")
    require({pad_position(pad) for pad in paste} == {
        (D("-0.65"), D("-0.20")), (D("-0.65"), D("0.20")),
        (D("0.65"), D("0.20")), (D("0.65"), D("-0.20")),
    }, "RWB0012A side stencil aperture positions mismatch")
    require(all(pad_size(pad) == (D("0.67"), D("0.20")) for pad in paste),
            "RWB0012A side stencil aperture size mismatch")
    require(all(pad_layers(pad) == ["F.Paste"] for pad in paste),
            "RWB0012A side stencil aperture layers mismatch")
    marker = one(root, "fp_circle", "RWB0012A pin-1 marker")
    require(dec(one(marker, "center", "RWB0012A pin-1 marker")[1:]) ==
            (D("-1.25"), D("-0.75")), "RWB0012A pin-1 marker mismatch")


def check_dsj_footprint(project):
    root = footprint(project, "VSON_TI_DSJ0014_4x3mm_P0.5mm_EP2.85x1.58mm")
    pads = children(root, "pad")
    signal = {pad[1]: pad for pad in pads if pad[1] and pad[1] != "15"}
    require(set(signal) == set(map(str, range(1, 15))), "DSJ0014 signal pad numbers mismatch")
    for number in range(1, 15):
        if number <= 7:
            position = (D("-1.50") + D("0.50") * (number - 1), D("-1.40"))
        else:
            position = (D("1.50") - D("0.50") * (number - 8), D("1.40"))
        pad = signal[str(number)]
        require(pad_position(pad) == position, f"DSJ0014 pad {number} position mismatch")
        require(pad_size(pad) == (D("0.24"), D("0.60")),
                f"DSJ0014 pad {number} size mismatch")
        require(pad_layers(pad) == ["F.Cu", "F.Paste", "F.Mask"],
                f"DSJ0014 pad {number} layer mismatch")
        mask_margin = one(pad, "solder_mask_margin", f"DSJ0014 pad {number}")
        require(D(mask_margin[1]) == D("0.07"),
                f"DSJ0014 pad {number} solder-mask margin mismatch")

    thermal = [pad for pad in pads if pad[1] == "15"]
    require(len(thermal) == 9, "DSJ0014 exposed copper piece count mismatch")
    central = [pad for pad in thermal if pad_position(pad) == (D("0"), D("0"))]
    require(len(central) == 1, "DSJ0014 central exposed pad mismatch")
    require(pad_size(central[0]) == (D("2.85"), D("1.58")),
            "DSJ0014 central exposed pad size mismatch")
    fingers = [pad for pad in thermal if pad is not central[0]]
    require({pad_position(pad) for pad in fingers} == {
        (x, y) for x in (D("-1.8125"), D("1.8125"))
        for y in (D("-0.69"), D("-0.23"), D("0.23"), D("0.69"))
    }, "DSJ0014 thermal-finger positions mismatch")
    require(all(pad_size(pad) == (D("0.775"), D("0.20")) for pad in fingers),
            "DSJ0014 thermal-finger size mismatch")
    require(all(pad_layers(pad) == ["F.Cu", "F.Mask"] for pad in thermal),
            "DSJ0014 exposed copper layers mismatch")

    paste = [pad for pad in pads if not pad[1]]
    require(len(paste) == 12, "DSJ0014 thermal stencil aperture count mismatch")
    central_paste = [pad for pad in paste if pad_size(pad) == (D("1.25"), D("0.46"))]
    require({pad_position(pad) for pad in central_paste} == {
        (D("-0.725"), D("-0.33")), (D("0.725"), D("-0.33")),
        (D("-0.725"), D("0.33")), (D("0.725"), D("0.33")),
    }, "DSJ0014 central stencil positions mismatch")
    side_paste = [pad for pad in paste if pad_size(pad) == (D("0.85"), D("0.20"))]
    require({pad_position(pad) for pad in side_paste} == {
        (x, y) for x in (D("-1.775"), D("1.775"))
        for y in (D("-0.69"), D("-0.23"), D("0.23"), D("0.69"))
    }, "DSJ0014 side stencil positions mismatch")
    require(len(central_paste) == 4 and len(side_paste) == 8,
            "DSJ0014 thermal stencil aperture sizes mismatch")
    require(all(pad_layers(pad) == ["F.Paste"] for pad in paste),
            "DSJ0014 thermal stencil aperture layers mismatch")
    marker = one(root, "fp_circle", "DSJ0014 pin-1 marker")
    require(dec(one(marker, "center", "DSJ0014 pin-1 marker")[1:]) ==
            (D("-2.50"), D("-1.75")), "DSJ0014 pin-1 marker mismatch")


def check_libraries(project=PROJECT):
    symbols = check_symbol_libraries(project)
    check_rtw_footprint(project)
    check_drl_footprint(project)
    check_phase_two_footprints(project)
    check_rwb_footprint(project)
    check_dsj_footprint(project)
    return symbols


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-dir", type=Path, default=PROJECT)
    args = parser.parse_args()
    try:
        check_libraries(args.project_dir)
        print("Power library checks passed:")
        print("- 25 BQ25616J pins match the TI RTW pin table and exposed-pad map")
        print("- RTW signal lands and four-way stencil segmentation match TI drawing 4211120-3/D")
        print("- 8 TPS631000 pins and DRL lands match the current TI pin/package drawings")
        print("- DBV, DDF and base-suffix DQA0010A land patterns match current TI drawings")
        print("- 12 TUSB320LAI pins and asymmetric RWB X2QFN copper/stencil maps match TI drawings")
        print("- 15 TPS63020 logical pins and DSJ signal/thermal/stencil maps match TI drawings")
        print("- blocked USB-C and fuel-gauge footprints were not guessed")
    except (OSError, ValueError, KeyError, IndexError) as error:
        print(f"Power library check failed: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
