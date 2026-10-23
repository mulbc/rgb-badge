#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Check USB4505 land transcription; not cutout, process or USB approval."""

from collections import Counter
from decimal import Decimal as D
from itertools import combinations
from pathlib import Path
import argparse
import runpy
import sys

HELP = runpy.run_path(str(Path(__file__).with_name("check-power-libraries.py")))
parse, children, one = HELP["parse"], HELP["children"], HELP["one"]
require, dec = HELP["require"], HELP["dec"]
PROJECT = HELP["PROJECT"]
MPN = "USB4505-03-0-A"
FOOTPRINT = "USB_C_GCT_USB4505-03-0-A_MidMount"
# Independently transcribed from the manufacturer contact table and top-view
# layout. Joined identifiers describe one physical solder land, not new pins.
LANDS = {
    "A1_B12": ("GND", "-3.2", "0.6"),
    "A4_B9": ("VBUS", "-2.4", "0.6"),
    "B8": ("SBU2", "-1.75", "0.3"),
    "A5": ("CC1", "-1.25", "0.3"),
    "B7": ("D-", "-0.75", "0.3"),
    "A6": ("D+", "-0.25", "0.3"),
    "A7": ("D-", "0.25", "0.3"),
    "B6": ("D+", "0.75", "0.3"),
    "A8": ("SBU1", "1.25", "0.3"),
    "B5": ("CC2", "1.75", "0.3"),
    "B4_A9": ("VBUS", "2.4", "0.6"),
    "B1_A12": ("GND", "3.2", "0.6"),
}


def check_symbol(symbol):
    props = HELP["property_map"](symbol)
    require(props.get("MPN") == MPN, "USB connector MPN mismatch")
    require(props.get("Footprint") == "rgb-badge-coupon:" + FOOTPRINT,
            "USB connector footprint assignment mismatch")
    require(props.get("Datasheet") == "https://gct.co/files/drawings/usb4505.pdf",
            "USB connector datasheet mismatch")
    pins = HELP["library_pins"](symbol)
    expected = {key: value[0] for key, value in LANDS.items()} | {"S1": "SHIELD"}
    require(set(pins) == set(expected), "USB connector shared-land pin set mismatch")
    for number, name in expected.items():
        require(one(pins[number], "name", number)[1] == name,
                f"USB contact function mismatch: {number}")
        require(pins[number][1] == "passive", f"USB contact type mismatch: {number}")


def check_footprint(root):
    pads = children(root, "pad")
    require(Counter(p[1] for p in pads) == Counter(list(LANDS) + ["S1"] * 4),
            "USB pad count/shared-land identifiers mismatch")
    by_number = {p[1]: p for p in pads if p[1] != "S1"}
    for number, (_, x, width) in LANDS.items():
        pad = by_number[number]
        require(pad[2:4] == ["smd", "rect"], f"USB signal shape mismatch: {number}")
        require(dec(one(pad, "at", number)[1:]) == (D(x), D(0)),
                f"USB land position/rotation mismatch: {number}")
        require(HELP["pad_size"](pad) == (D(width), D("1.1")),
                f"USB land size mismatch: {number}")
        require(HELP["pad_layers"](pad) == ["F.Cu", "F.Paste", "F.Mask"],
                f"USB signal layers mismatch: {number}")
    stakes = [p for p in pads if p[1] == "S1"]
    require({HELP["pad_position"](p) for p in stakes} == {
        (D(x), D(y)) for x in ("-5.62", "5.62") for y in ("1.15", "5.15")
    }, "USB shell-stake position mismatch")
    for pad in stakes:
        rear = HELP["pad_position"](pad)[1] == D("1.15")
        require(len(one(pad, "at", "stake")) == 3, "USB stake rotation unexpected")
        require(pad[2:4] == ["thru_hole", "oval"], "USB shell-stake type mismatch")
        require(HELP["pad_size"](pad) == dec(("1", "1.8" if rear else "2.2")),
                "USB shell-stake copper size mismatch")
        drill = one(pad, "drill", "stake")
        require(drill[1] == "oval" and dec(drill[2:]) ==
                dec(("0.6", "1.4" if rear else "1.8")), "USB shell slot mismatch")
        require(HELP["pad_layers"](pad) == ["*.Cu", "*.Mask"],
                "USB shell layers/provisional no-paste mismatch")
    require(D(one(root, "solder_mask_margin", "USB")[1]) == D("0.05"),
            "USB provisional mask expansion mismatch")
    # Independent geometry guard includes both signal lands and plated stakes.
    for a, b in combinations(pads, 2):
        if a[1] == b[1]:
            continue
        ap, bp = HELP["pad_position"](a), HELP["pad_position"](b)
        az, bz = HELP["pad_size"](a), HELP["pad_size"](b)
        gap = max(abs(ap[i] - bp[i]) - (az[i] + bz[i]) / 2 for i in (0, 1))
        require(gap >= D("0.20"), "USB copper clearance below 0.20 mm")
    require(not any(n[0] == "layer" and n[1] == "Edge.Cuts"
                    for item in root if isinstance(item, list)
                    for n in item if isinstance(n, list)),
            "Unqualified USB cutout must not become Edge.Cuts")
    guides = [item for item in children(root, "fp_line")
              if one(item, "layer", "guide")[1] == "Dwgs.User"]
    require({(dec(one(g, "start", "guide")[1:]), dec(one(g, "end", "guide")[1:]))
             for g in guides} == {
        (dec(a), dec(b)) for a, b in [
            (("-7", "6.75"), ("-4.62", "6.75")),
            (("-4.62", "6.75"), ("-4.62", "0.55")),
            (("-4.62", "0.55"), ("4.62", "0.55")),
            (("4.62", "0.55"), ("4.62", "6.75")),
            (("4.62", "6.75"), ("7", "6.75")),
        ]}, "USB mechanical datum guides mismatch")


def check_libraries(project=PROJECT):
    library = parse(project / "symbols" / "rgb-badge-coupon.kicad_sym")
    symbols = [s for s in children(library, "symbol") if s[1] == MPN]
    require(len(symbols) == 1, "USB connector symbol missing or duplicated")
    check_symbol(symbols[0])
    check_footprint(HELP["footprint"](project, FOOTPRINT))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-dir", type=Path, default=PROJECT)
    args = parser.parse_args()
    try:
        check_libraries(args.project_dir)
    except (OSError, ValueError, KeyError, IndexError) as error:
        print(f"USB connector audit failed: {error}", file=sys.stderr)
        return 1
    print("USB connector source audit passed: 16 contacts / 12 lands, four shell slots, 0.20 mm minimum copper gap.")
    print("USB4505 draft: 0.80 mm PCB; cutout reliefs and assembly process remain unqualified.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
