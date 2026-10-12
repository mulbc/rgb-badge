#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Stress-screen proposed display-interlock IC bodies against the current rear XY trial.

This deliberately omits all support passives and routing. It is a lower-bound
geometric screen, not a footprint, PCB, enclosure, or electrical approval.
"""

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location(
    "current_fit", ROOT / "tools/screen-current-lp452845-xy.py"
)
fit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fit)

# Nominal package bodies from TI product pages; these are NOT pad courtyards.
# Width and height are deliberately kept axis-aligned and may rotate in a PCB.
IC_BODIES = (
    ("TPS3823A-33DBVR", 2.9, 1.6),
    ("SN74LVC1G74DCUR-A", 2.0, 3.1),
    ("SN74LVC1G74DCUR-B", 2.0, 3.1),
    ("TLV6700DSER", 1.5, 1.5),
    ("SN74LVC1G04DRLR", 1.6, 1.6),
    ("SN74LVC1G11DCKR", 2.0, 2.1),
    ("SN74LVC1G08DRLR", 1.6, 1.6),
    ("SN74LVC2G00DCUR", 2.0, 3.1),
    ("SN74LVC2G08DCUR", 2.0, 3.1),
)


def screen(xml: Path) -> dict:
    parts, counts = fit.space.component_inventory(xml)
    if sum(counts.values()) != 466 or len(parts) != 207:
        raise ValueError("Current coupon inventory changed; re-audit the screen")
    pack = fit.box(31.0, 2.0, 47.0, 28.5)
    sensor = fit.box(49.5, 12.25, 10.0, 8.0)
    cases = []
    for body_margin in (0.5, 1.0):
        candidate_parts = list(parts)
        for name, width, height in IC_BODIES:
            w, h = width + body_margin, height + body_margin
            candidate_parts.append({"ref": "INT_" + name, "footprint": "ESTIMATED_IC_BODY",
                                    "width_mm": w, "height_mm": h, "area_mm2": w * h})
        for board_width in (106.0, 108.0, 110.0):
            fixed = fit.fixed_boxes(parts, right_shift=board_width - fit.BOARD_W)
            placed = fit.place(candidate_parts, "dual-package candidate", "area first",
                               fixed, pack, sensor, board_width=board_width)
            cases.append({"body_margin_each_dimension_mm": body_margin,
                          "board_width_mm": board_width,
                          "unplaced_count": placed["unplaced_count"],
                          "unplaced_refs": placed["unplaced_refs"],
                          "interlock_unplaced_refs": [ref for ref in placed["unplaced_refs"]
                                                      if ref.startswith("INT_")]})
    return {"SPDX-License-Identifier": "CERN-OHL-S-2.0",
            "status": "IC_BODY_ONLY_GEOMETRIC_LOWER_BOUND_NOT_A_PCB_OR_FIT_APPROVAL",
            "native_xml_sha256": hashlib.sha256(xml.read_bytes()).hexdigest(),
            "source_coupon_pcb_items": sum(counts.values()),
            "source_coupon_rear_parts": len(parts),
            "assumed_ic_bodies_mm": [{"mpn": name, "width_mm": w, "height_mm": h}
                                  for name, w, h in IC_BODIES],
            "inherited_grid_mm": fit.GRID,
            "inherited_extra_box_each_dimension_mm": fit.EXTRA_BOX_MM,
            "cases": cases,
            "limitations": [
                "No interlock resistors, capacitors, test pads, traces or via/thermal/RF clearance",
                "Body dimensions are not footprint courtyards or manufacturer land patterns",
                "The dual row package substitution is still proposed, not captured",
                "Under-pack 0402 placement is conditional and not circuit-local",
                "110mm case wall, USB opening, mounting and routing tolerances are absent",
            ]}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("native_xml", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = screen(args.native_xml)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    for case in result["cases"]:
        print(f"margin {case['body_margin_each_dimension_mm']:.1f} mm, "
              f"board {case['board_width_mm']:.0f} mm: "
              f"{case['unplaced_count']} unplaced")


if __name__ == "__main__":
    main()
