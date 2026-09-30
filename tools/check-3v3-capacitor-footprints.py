#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Check provisional TPS631000 capacitor lands against exact Murata reflow tables."""

from decimal import Decimal as D
from pathlib import Path
import runpy
import sys


LED = runpy.run_path(str(Path(__file__).with_name("check-led-libraries.py")))
parse, children = LED["parse_sexpr"], LED["children"]
ROOT = Path(__file__).resolve().parents[1] / "hardware/coupon/rev-a/footprints/rgb-badge-coupon.pretty"
SYMBOL_LIBRARY = ROOT.parents[1] / "symbols/rgb-badge-coupon.kicad_sym"


def atom(node, tag):
    matches = children(node, tag)
    if len(matches) != 1:
        raise ValueError(f"expected one {tag}: {node[0]}")
    return matches[0]


def check(name, pad_x, pad_length, gap, pad_width, fab, courtyard):
    fp = parse(ROOT / (name + ".kicad_mod"))
    pads = children(fp, "pad")
    if len(pads) != 2 or [p[1] for p in pads] != ["1", "2"]:
        raise ValueError(f"{name}: exactly two numbered lands required")
    for pad, x in zip(pads, (-pad_x, pad_x)):
        if pad[2:4] != ["smd", "rect"]:
            raise ValueError(f"{name}: wrong pad type/shape")
        if atom(pad, "at")[1:3] != [str(x), "0"]:
            raise ValueError(f"{name}: pad position mismatch")
        if list(map(D, atom(pad, "size")[1:3])) != [pad_length, pad_width]:
            raise ValueError(f"{name}: pad dimensions mismatch")
        if atom(pad, "layers")[1:] != ["F.Cu", "F.Paste", "F.Mask"]:
            raise ValueError(f"{name}: pad layers mismatch")
    if 2 * pad_x - pad_length != gap:
        raise ValueError(f"{name}: wrong inner land gap")
    rectangles = {atom(r, "layer")[1]: r for r in children(fp, "fp_rect")}
    for layer, expected in (("F.Fab", fab), ("F.CrtYd", courtyard)):
        rect = rectangles.get(layer)
        if rect is None:
            raise ValueError(f"{name}: missing {layer} rectangle")
        coords = [*atom(rect, "start")[1:3], *atom(rect, "end")[1:3]]
        if list(map(D, coords)) != list(expected):
            raise ValueError(f"{name}: {layer} dimensions mismatch")


def check_symbols():
    symbols = {s[1]: s for s in children(parse(SYMBOL_LIBRARY), "symbol")}
    reference = "GRM188R60J106ME47D"
    template = symbols[reference]

    def replace(node, old, new):
        if isinstance(node, list):
            return [replace(x, old, new) for x in node]
        return node.replace(old, new) if isinstance(node, str) else node

    for mpn, footprint in (("GRM187R61A226ME15", "C_Murata_GRM18_0603"),
                           ("GRM219R60J476ME44", "C_Murata_GRM21_0805")):
        expected = replace(template, reference, mpn)
        expected = replace(expected, "rgb-badge-coupon:C_Murata_GRM18_0603",
                           "rgb-badge-coupon:" + footprint)
        if symbols.get(mpn) != expected:
            raise ValueError(f"{mpn}: exact MPN, passive pins, datasheet or footprint differs from template")


def main():
    try:
        # GRM187R61A226ME15: 1.6 ±0.2 × 0.8 ±0.2 mm body;
        # reflow a=0.7–0.9, b=0.7–0.8, c=0.8–1.0 mm.
        check("C_Murata_GRM18_0603", D("0.8"), D("0.9"), D("0.7"), D("0.9"),
              (D("-0.8"), D("-0.4"), D("0.8"), D("0.4")),
              (D("-1.5"), D("-0.65"), D("1.5"), D("0.65")))
        # GRM219R60J476ME44: 2.0 ±0.2 × 1.25 ±0.2 mm body;
        # reflow a=1.0–1.4, b=0.6–0.8, c=1.2–1.4 mm.
        check("C_Murata_GRM21_0805", D("0.95"), D("1.2"), D("0.7"), D("1.3"),
              (D("-1"), D("-0.625"), D("1"), D("0.625")),
              (D("-1.8"), D("-1"), D("1.8"), D("1")))
        check_symbols()
    except (OSError, ValueError, KeyError, IndexError) as error:
        print(f"3V3 capacitor land check failed: {error}", file=sys.stderr)
        return 1
    print("3V3 capacitor libraries passed: two exact passive MPNs, GRM18 reuse and GRM21 land")
    return 0


if __name__ == "__main__":
    sys.exit(main())
