#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Audit exact Coupon Rev A controller symbols and land patterns.

The checks compare the project-local library against manufacturer pin tables
and package drawings. They do not replace KiCad ERC/DRC, RF review, assembly
DFM or measurements on a populated coupon.
"""

from collections import Counter
from decimal import Decimal as D
from pathlib import Path
import argparse
import runpy
import sys


LED = runpy.run_path(str(Path(__file__).with_name("check-led-libraries.py")))
parse, children, one = LED["parse_sexpr"], LED["children"], LED["only_child"]
props = LED["property_map"]
PROJECT = Path(__file__).resolve().parents[1] / "hardware" / "coupon" / "rev-a"
FP_PREFIX = "rgb-badge-coupon:"

MODULE_PINS = {
    1: "GND", 2: "3V3", 3: "EN", 4: "GPIO4", 5: "GPIO5", 6: "GPIO6",
    7: "GPIO7", 8: "GPIO15", 9: "GPIO16", 10: "GPIO17", 11: "GPIO18",
    12: "GPIO8", 13: "GPIO19/USB_D-", 14: "GPIO20/USB_D+", 15: "GPIO3",
    16: "GPIO46", 17: "GPIO9", 18: "GPIO10", 19: "GPIO11", 20: "GPIO12",
    21: "GPIO13", 22: "GPIO14", 23: "GPIO21", 24: "GPIO47", 25: "GPIO48",
    26: "GPIO45", 27: "GPIO0/BOOT", 28: "GPIO35/PSRAM",
    29: "GPIO36/PSRAM", 30: "GPIO37/PSRAM", 31: "GPIO38", 32: "GPIO39",
    33: "GPIO40", 34: "GPIO41", 35: "GPIO42", 36: "GPIO44/U0RXD",
    37: "GPIO43/U0TXD", 38: "GPIO2", 39: "GPIO1", 40: "GND", 41: "GND_EP",
}

PARTS = {
    "ESP32-S3-WROOM-1U-N16R8": ("ESP32-S3-WROOM-1U", MODULE_PINS),
    "ERJ-2RKF1002X": ("R_Panasonic_ERJ2_0402", {1: "~", 2: "~"}),
    "ERJ-2RKF22R0X": ("R_Panasonic_ERJ2_0402", {1: "~", 2: "~"}),
    "ERJ-2RKF4990X": ("R_Panasonic_ERJ2_0402", {1: "~", 2: "~"}),
    "GRM155C71A105KE11D": ("C_Murata_GRM15_0402", {1: "~", 2: "~"}),
    "GRM188R60J106ME47D": ("C_Murata_GRM18_0603", {1: "~", 2: "~"}),
    "EVQP7J01P": ("SW_Panasonic_EVQP7J01P", {1: "1", 2: "2"}),
}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def library_pins(symbol):
    result = {}
    for unit in children(symbol, "symbol"):
        for pin in children(unit, "pin"):
            number = one(pin, "number", "pin")[1]
            require(number not in result, f"duplicate symbol pin {number}")
            result[number] = pin
    return result


def dec(values):
    return tuple(map(D, values))


def pad_position(pad):
    at = one(pad, "at", "pad")
    return dec(at[1:3])


def pad_size(pad):
    return dec(one(pad, "size", "pad")[1:])


def footprint(project, name):
    return parse(project / "footprints" / "rgb-badge-coupon.pretty" / f"{name}.kicad_mod")


def check_module_footprint(project):
    pads = children(footprint(project, "ESP32-S3-WROOM-1U"), "pad")
    counts = Counter(pad[1] for pad in pads)
    require(counts == Counter({**{str(i): 1 for i in range(1, 41)}, "41": 9}),
            "ESP32 module pad count/number mismatch")
    by_number = {str(i): [p for p in pads if p[1] == str(i)] for i in range(1, 42)}
    for number in range(1, 15):
        expected = (D("-8.75"), D("-8.26") + D("1.27") * (number - 1))
        require(pad_position(by_number[str(number)][0]) == expected, f"module pad {number} position mismatch")
    for number in range(15, 27):
        expected = (D("-6.985") + D("1.27") * (number - 15), D("9.5"))
        require(pad_position(by_number[str(number)][0]) == expected, f"module pad {number} position mismatch")
    for number in range(27, 41):
        expected = (D("8.75"), D("8.25") - D("1.27") * (number - 27))
        require(pad_position(by_number[str(number)][0]) == expected, f"module pad {number} position mismatch")
    for number in range(1, 41):
        pad = by_number[str(number)][0]
        require(pad_size(pad) == (D("1.5"), D("0.9")), f"module pad {number} size mismatch")
        require(one(pad, "layers", "module pad")[1:] == ["F.Cu", "F.Paste", "F.Mask"],
                f"module pad {number} layer mismatch")
    expected_ep = {(D(x), D(y)) for x in ("-2.9", "-1.5", "-0.1") for y in ("-1.94", "-0.54", "0.86")}
    require({pad_position(p) for p in by_number["41"]} == expected_ep,
            "module central-ground array position mismatch")
    require(all(pad_size(p) == (D("0.9"), D("0.9")) for p in by_number["41"]),
            "module central-ground array pad size mismatch")


def check_small_footprints(project):
    cap = children(footprint(project, "C_Murata_GRM18_0603"), "pad")
    require([(p[1], pad_position(p), pad_size(p)) for p in cap] == [
        ("1", (D("-0.8"), D("0")), (D("0.9"), D("0.9"))),
        ("2", (D("0.8"), D("0")), (D("0.9"), D("0.9"))),
    ], "GRM18 selected land geometry mismatch")
    switch = children(footprint(project, "SW_Panasonic_EVQP7J01P"), "pad")
    require(Counter(p[1] for p in switch) == Counter({"1": 2, "2": 2}),
            "EVQP7J01P duplicate contact pads mismatch")
    expected = {
        ("1", D("-2.05"), D("-1.25")), ("1", D("-2.05"), D("1.25")),
        ("2", D("2.05"), D("-1.25")), ("2", D("2.05"), D("1.25")),
    }
    require({(p[1], *pad_position(p)) for p in switch} == expected,
            "EVQP7J01P pad position mismatch")
    require(all(pad_size(p) == (D("0.9"), D("0.4")) for p in switch),
            "EVQP7J01P pad size mismatch")


def check_libraries(project=PROJECT):
    symbols = {s[1]: s for s in children(parse(project / "symbols" / "rgb-badge-coupon.kicad_sym"), "symbol")}
    for mpn, (fp_name, pin_map) in PARTS.items():
        require(mpn in symbols, f"missing exact controller symbol {mpn}")
        symbol = symbols[mpn]
        properties = props(symbol)
        require(properties.get("MPN") == mpn, f"{mpn}: MPN property mismatch")
        require(properties.get("Footprint") == FP_PREFIX + fp_name, f"{mpn}: footprint property mismatch")
        pins = library_pins(symbol)
        require(set(pins) == set(map(str, pin_map)), f"{mpn}: pin number mismatch")
        for number, name in pin_map.items():
            require(one(pins[str(number)], "name", f"{mpn}.{number}")[1] == name,
                    f"{mpn}.{number}: pin name mismatch")
    module = library_pins(symbols["ESP32-S3-WROOM-1U-N16R8"])
    require(all(module[str(n)][1] == "power_in" for n in (1, 2, 40, 41)),
            "module power-pin electrical types mismatch")
    require(module["3"][1] == "input" and all(module[str(n)][1] == "bidirectional" for n in range(4, 40)),
            "module EN/GPIO electrical types mismatch")
    check_module_footprint(project)
    check_small_footprints(project)
    return symbols


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-dir", type=Path, default=PROJECT)
    args = parser.parse_args()
    try:
        check_libraries(args.project_dir)
        print("Controller library checks passed:")
        print("- 41 module pins match the Espressif ESP32-S3-WROOM-1U pin table")
        print("- N16R8 module land pattern matches the Espressif 1U geometry")
        print("- reset/USB/UART passives and the EVQP7J01P mode switch match their audits")
        print("- the central module ground uses nine same-numbered copper/paste lands")
    except (OSError, ValueError, KeyError, IndexError) as error:
        print(f"Controller library check failed: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
