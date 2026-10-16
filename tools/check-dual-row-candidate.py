#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Check the unpopulated Diodes Type B dual-MOSFET land candidate."""

from collections import Counter
from decimal import Decimal
from pathlib import Path
import runpy


ROOT = Path(__file__).resolve().parents[1]
NAME = "U-DFN2020-6_TypeB_Diodes_DMC1229UFDB"
PATH = ROOT / "hardware/coupon/rev-a/footprints/rgb-badge-coupon.pretty" / f"{NAME}.kicad_mod"
PARSER = runpy.run_path(str(Path(__file__).with_name("check-led-libraries.py")))
parse = PARSER["parse_sexpr"]
children = PARSER["children"]
one = PARSER["only_child"]
D = Decimal


def check(path=PATH):
    root = parse(path)
    assert root[0] == "footprint" and root[1] == NAME
    expected = {
        ("1", "-0.65", "-0.9", "0.35", "0.5"),
        ("2", "0", "-0.9", "0.35", "0.5"),
        ("3", "0.65", "-0.9", "0.35", "0.5"),
        ("3", "0.525", "0", "0.6", "1.0"),
        ("4", "0.65", "0.9", "0.35", "0.5"),
        ("5", "0", "0.9", "0.35", "0.5"),
        ("6", "-0.65", "0.9", "0.35", "0.5"),
        ("6", "-0.525", "0", "0.6", "1.0"),
    }
    actual = set()
    numbers = Counter()
    for pad in children(root, "pad"):
        assert pad[2:4] == ["smd", "rect"], f"pad {pad[1]} type/shape"
        assert one(pad, "layers", "pad")[1:] == ["F.Cu", "F.Paste", "F.Mask"]
        at = one(pad, "at", "pad")[1:3]
        size = one(pad, "size", "pad")[1:]
        actual.add((pad[1], *map(str, map(D, at)), *map(str, map(D, size))))
        numbers[pad[1]] += 1
    assert actual == {(n, *map(str, map(D, (x, y, w, h)))) for n, x, y, w, h in expected}
    assert numbers == Counter({"1": 1, "2": 1, "3": 2, "4": 1, "5": 1, "6": 2})
    markers = children(root, "fp_circle")
    assert len(markers) == 1
    assert one(markers[0], "center", "pin-one marker")[1:] == ["-1.25", "-1.25"]
    courtyards = [x for x in children(root, "fp_rect") if one(x, "layer", "courtyard")[1] == "F.CrtYd"]
    assert len(courtyards) == 1
    assert one(courtyards[0], "start", "courtyard")[1:] == ["-1.5", "-1.5"]
    assert one(courtyards[0], "end", "courtyard")[1:] == ["1.5", "1.5"]
    rows = (ROOT / "hardware/coupon/rev-a/rows.kicad_sch").read_text()
    assert "DMC1229UFDB" not in rows, "candidate was silently connected to canonical rows"
    return len(actual)


if __name__ == "__main__":
    print(f"Dual-row candidate footprint: {check()} lands checked; canonical rows unchanged.")
