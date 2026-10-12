#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Audit the first two TI display-interlock lands against published drawings."""

from decimal import Decimal as D
from pathlib import Path
import runpy


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / "hardware/coupon/rev-a"
LIB = runpy.run_path(str(ROOT / "tools/check-power-libraries.py"))
children = LIB["children"]
one = LIB["one"]
parse = LIB["parse"]


def check(name, expected, courtyard, body, mask_margin):
    path = PROJECT / "footprints/rgb-badge-coupon.pretty" / f"{name}.kicad_mod"
    footprint = parse(path)
    assert footprint[1] == name
    actual = {}
    for pad in children(footprint, "pad"):
        key = (pad[1], tuple(one(pad, "layers", "pad")[1:]))
        actual.setdefault(key, []).append((
            tuple(D(v) for v in one(pad, "at", "pad")[1:3]),
            tuple(D(v) for v in one(pad, "size", "pad")[1:]),
        ))
        assert pad[2:4] == ["smd", "roundrect"]
        radius = min(D(v) for v in one(pad, "size", "pad")[1:]) * D(one(pad, "roundrect_rratio", "pad")[1])
        assert abs(radius - D("0.05")) < D("0.00001"), (name, pad[1], radius)
    assert actual == expected, f"{name}: pad number, layer, position or size differs from TI drawing"
    assert D(one(footprint, "solder_mask_margin", name)[1]) == D(mask_margin)
    rectangles = {one(rect, "layer", "rect")[1]: (
        tuple(D(v) for v in one(rect, "start", "rect")[1:]),
        tuple(D(v) for v in one(rect, "end", "rect")[1:]),
    ) for rect in children(footprint, "fp_rect")}
    assert rectangles["F.CrtYd"] == courtyard
    assert rectangles["F.Fab"] == body
    assert len(children(footprint, "fp_circle")) == 1, f"{name}: pin-one mark missing"
    LIB["check_copper_separation"](footprint)


def main():
    dsf = {}
    left = ((D("-0.4"), D("-0.35")), (D("-0.4"), D("0")), (D("-0.4"), D("0.35")))
    right = ((D("0.4"), D("0.35")), (D("0.4"), D("0")), (D("0.4"), D("-0.35")))
    for number, position in enumerate(left + right, 1):
        dsf[(str(number), ("F.Cu", "F.Mask"))] = [(position, (D("0.6"), D("0.17")))]
    dsf[("", ("F.Paste",))] = [(position, (D("0.6"), D("0.15"))) for position in left + right]
    check("X2SON_TI_DSF0006A_1x1mm_P0.35mm", dsf,
          ((D("-0.95"), D("-0.75")), (D("0.95"), D("0.75"))),
          ((D("-0.5"), D("-0.5")), (D("0.5"), D("0.5"))), "0.05")

    dcu = {}
    positions = [(D("-1.125"), y) for y in map(D, ("-0.75", "-0.25", "0.25", "0.75"))]
    positions += [(D("1.125"), y) for y in map(D, ("0.75", "0.25", "-0.25", "-0.75"))]
    for number, position in enumerate(positions, 1):
        dcu[(str(number), ("F.Cu", "F.Paste", "F.Mask"))] = [(position, (D("0.85"), D("0.3")))]
    check("VSSOP_TI_DCU0008A", dcu,
          ((D("-1.85"), D("-1.85")), (D("1.85"), D("1.85"))),
          ((D("-1.2"), D("-1.6")), (D("1.2"), D("1.6"))), "0.05")
    print("TI DSF0006A and DCU0008A copper, paste, numbering and courtyard checks passed")


if __name__ == "__main__":
    main()
