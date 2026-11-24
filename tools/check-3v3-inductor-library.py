#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Compare staged Murata DFE252012P library with its published land sketch.

Source geometry only: this does not qualify current derating, assembly or layout.
"""

from pathlib import Path
import runpy


PROJECT = Path(__file__).resolve().parents[1] / "hardware/coupon/rev-a"
LED = runpy.run_path(str(Path(__file__).with_name("check-led-libraries.py")))
parse, children = LED["parse_sexpr"], LED["children"]
MPN = "DFE252012P-1R0M=P2"
FOOTPRINT = "L_Murata_DFE252012P"
SOURCE = "https://www.murata.com/~/media/webrenewal/products/inductor/chip/tokoproducts/wirewoundmetalalloychiptype/m_dfe252012p.ashx"


def only(node, tag):
    found = children(node, tag)
    if len(found) != 1:
        raise ValueError(f"expected one {tag}")
    return found[0]


def check(project=PROJECT):
    symbols = [s for s in children(parse(project / "symbols/rgb-badge-coupon.kicad_sym"), "symbol") if s[1] == MPN]
    if len(symbols) != 1:
        raise ValueError("exact-MPN inductor symbol missing or duplicated")
    symbol = symbols[0]
    properties = {p[1]: p[2] for p in children(symbol, "property")}
    expected = {"Reference": "L", "Value": MPN, "MPN": MPN, "Manufacturer": "Murata",
                "Footprint": "rgb-badge-coupon:" + FOOTPRINT, "Datasheet": SOURCE}
    if any(properties.get(k) != v for k, v in expected.items()):
        raise ValueError("inductor symbol identity, footprint or source mismatch")
    units = children(symbol, "symbol")
    pins = [p for unit in units for p in children(unit, "pin")]
    if len(pins) != 2 or sorted(only(p, "number")[1] for p in pins) != ["1", "2"]:
        raise ValueError("inductor requires exactly two numbered pins")
    if any(p[1:3] != ["passive", "line"] for p in pins):
        raise ValueError("inductor pins must be passive")

    fp = parse(project / "footprints/rgb-badge-coupon.pretty" / (FOOTPRINT + ".kicad_mod"))
    pads = children(fp, "pad")
    if len(pads) != 2 or [p[1] for p in pads] != ["1", "2"]:
        raise ValueError("inductor requires two numbered lands")
    for pad, x in zip(pads, ("-1", "1")):
        if pad[2:4] != ["smd", "rect"] or only(pad, "at")[1:3] != [x, "0"]:
            raise ValueError("land type or position mismatch")
        if only(pad, "size")[1:3] != ["0.8", "2"]:
            raise ValueError("land dimensions differ from Murata 2.8/1.2/2.0 pattern")
        if only(pad, "layers")[1:] != ["F.Cu", "F.Paste", "F.Mask"]:
            raise ValueError("land layer mismatch")
    rectangles = {only(r, "layer")[1]: r for r in children(fp, "fp_rect")}
    for layer, coordinates in {"F.Fab": ["-1.25", "-1", "1.25", "1"],
                               "F.CrtYd": ["-1.65", "-1.35", "1.65", "1.35"]}.items():
        rect = rectangles.get(layer)
        if rect is None or only(rect, "start")[1:3] + only(rect, "end")[1:3] != coordinates:
            raise ValueError(f"{layer} body/courtyard mismatch")
    return True


if __name__ == "__main__":
    check()
    print("3V3 inductor library passed: exact Murata MPN, two passive pins, 2.8 mm span / 1.2 mm gap / 2.0 mm land width.")
    print("Inductor is on the root-linked provisional converter; thermal/DC-bias, assembly and Gate A remain open.")
