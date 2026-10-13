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

# Alternative package-only sensitivity. Logic functions and chip count are unchanged.
# Leadless lands, solder process and sourcing are NOT qualified by this screen.
COMPACT_IC_BODIES = (
    ("TPS3823A-33DBVR", 2.9, 1.6),
    ("SN74LVC1G74RSER-A", 1.5, 1.5),
    ("SN74LVC1G74RSER-B", 1.5, 1.5),
    ("TLV6700DSER", 1.5, 1.5),
    ("SN74LVC1G04DSFR", 1.0, 1.0),
    ("SN74LVC1G11DRYR", 1.45, 1.0),
    ("SN74LVC1G08DSFR", 1.0, 1.0),
    ("SN74LVC2G00DCUR", 2.0, 3.1),
    ("SN74LVC2G08DCUR", 2.0, 3.1),
)

# Existing project-local courtyards are stronger evidence than a generic body
# allowance. The placement engine adds 0.5 mm, so subtract that before passing
# these floors to it. Other interlock ICs still use estimated body allowances.
LOCAL_COURTYARD_FLOORS_MM = {
    "TPS3823A-33DBVR": (4.3, 3.6),  # SOT23_TI_DBV0005A
    "SN74LVC1G74RSER-A": (2.4, 2.4),  # UQFN_TI_RSE0008A
    "SN74LVC1G74RSER-B": (2.4, 2.4),
    "SN74LVC1G04DSFR": (1.9, 1.5),  # X2SON_TI_DSF0006A
    "SN74LVC1G08DSFR": (1.9, 1.5),
    "TLV6700DSER": (2.5, 2.1),  # WSON_TI_DSE0006A
    "SN74LVC1G11DRYR": (1.6, 2.0),  # USON_TI_DRY0006A
    "SN74LVC2G00DCUR": (3.7, 3.7),  # VSSOP_TI_DCU0008A
    "SN74LVC2G08DCUR": (3.7, 3.7),
}


def estimated_box(name, body_width, body_height, body_margin):
    floor_w, floor_h = LOCAL_COURTYARD_FLOORS_MM.get(name, (0.0, 0.0))
    width = max(body_width + body_margin, floor_w - fit.EXTRA_BOX_MM)
    height = max(body_height + body_margin, floor_h - fit.EXTRA_BOX_MM)
    return {"ref": "INT_" + name, "footprint": "ESTIMATED_IC_BODY",
            "width_mm": width, "height_mm": height, "area_mm2": width * height}


def screen(xml: Path) -> dict:
    parts, counts = fit.space.component_inventory(xml)
    if sum(counts.values()) != 466 or len(parts) != 207:
        raise ValueError("Current coupon inventory changed; re-audit the screen")
    pack = fit.box(31.0, 2.0, 47.0, 28.5)
    sensor = fit.box(49.5, 12.25, 10.0, 8.0)
    def cases_for(bodies):
        cases = []
        for body_margin in (0.5, 1.0):
            candidate_parts = list(parts)
            for name, width, height in bodies:
                candidate_parts.append(estimated_box(name, width, height, body_margin))
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
        return cases
    support_cases = []
    support_parts = list(parts)
    for name, width, height in COMPACT_IC_BODIES:
        support_parts.append(estimated_box(name, width, height, 1.0))
    # Sensitivity only: twenty proposed 0402 courtyard boxes, all forced
    # outside the pack. These do not represent a captured support-circuit BOM.
    for index in range(20):
        support_parts.append({"ref": f"INT_SUPPORT_{index + 1:02d}",
                              "footprint": "ESTIMATED_INTERLOCK_SUPPORT_0402",
                              "width_mm": 2.0, "height_mm": 1.0, "area_mm2": 2.0})
    for board_width in (106.0, 108.0, 110.0):
        fixed = fit.fixed_boxes(parts, right_shift=board_width - fit.BOARD_W)
        placed = fit.place(support_parts, "dual-package candidate", "area first",
                           fixed, pack, sensor, board_width=board_width)
        support_cases.append({"board_width_mm": board_width,
                              "unplaced_count": placed["unplaced_count"],
                              "unplaced_refs": placed["unplaced_refs"]})
    return {"SPDX-License-Identifier": "CERN-OHL-S-2.0",
            "status": "IC_BODY_ONLY_GEOMETRIC_LOWER_BOUND_NOT_A_PCB_OR_FIT_APPROVAL",
            "native_xml_sha256": hashlib.sha256(xml.read_bytes()).hexdigest(),
            "source_coupon_pcb_items": sum(counts.values()),
            "source_coupon_rear_parts": len(parts),
            "assumed_ic_bodies_mm": [{"mpn": name, "width_mm": w, "height_mm": h}
                                  for name, w, h in IC_BODIES],
            "compact_assumed_ic_bodies_mm": [{"mpn": name, "width_mm": w, "height_mm": h}
                                          for name, w, h in COMPACT_IC_BODIES],
            "local_courtyard_floors_mm": LOCAL_COURTYARD_FLOORS_MM,
            "inherited_grid_mm": fit.GRID,
            "inherited_extra_box_each_dimension_mm": fit.EXTRA_BOX_MM,
            "cases": cases_for(IC_BODIES),
            "compact_cases": cases_for(COMPACT_IC_BODIES),
            "compact_plus_20_support_0402_cases": support_cases,
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
    for case in result["compact_cases"]:
        print(f"compact margin {case['body_margin_each_dimension_mm']:.1f} mm, "
              f"board {case['board_width_mm']:.0f} mm: "
              f"{case['unplaced_count']} unplaced")
    for case in result["compact_plus_20_support_0402_cases"]:
        print(f"compact + 20 outside-pack 0402, board {case['board_width_mm']:.0f} mm: "
              f"{case['unplaced_count']} unplaced")


if __name__ == "__main__":
    main()
