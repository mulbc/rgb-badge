#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Coarse XY screen of the captured interlock's actual project-local courtyards."""

import argparse
import hashlib
import importlib.util
import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("current_fit", ROOT / "tools/screen-current-lp452845-xy.py")
fit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fit)


def edge_gap_mm(first, second):
    dx = max(first[0] - second[2], second[0] - first[2], 0)
    dy = max(first[1] - second[3], second[1] - first[3], 0)
    return round(math.hypot(dx, dy), 2)


def screen(xml):
    parts, counts = fit.space.component_inventory(xml)
    expected = {*(f"U{n}" for n in range(47, 56)), *(f"C{n}" for n in range(66, 75)),
                *(f"R{n}" for n in range(103, 114)), "TP13", "TP14"}
    present = {part["ref"] for part in parts}
    if sum(counts.values()) != 497 or len(parts) != 238 or not expected <= present:
        raise ValueError("Captured coupon inventory changed; re-audit the screen")
    pack = fit.box(31.0, 2.0, 47.0, 28.5)
    sensor = fit.box(49.5, 12.25, 10.0, 8.0)
    cases = []
    for variant in ("canonical 32 separate row FETs", "dual-package candidate"):
        for width in (106.0, 108.0, 110.0):
            fixed = fit.fixed_boxes(parts, right_shift=width - fit.BOARD_W)
            placed = fit.place(parts, variant, "area first", fixed,
                               pack, sensor, board_width=width)
            boxes = placed["boxes_mm"]
            bypass_gaps = {f"U{47 + index}/C{66 + index}":
                           edge_gap_mm(boxes[f"U{47 + index}"], boxes[f"C{66 + index}"])
                           for index in range(9)
                           if f"U{47 + index}" in boxes and f"C{66 + index}" in boxes}
            cases.append({"row_topology": variant, "board_width_mm": width,
                          "unplaced_count": placed["unplaced_count"],
                          "unplaced_refs": placed["unplaced_refs"],
                          "bypass_to_ic_edge_gap_mm": bypass_gaps,
                          "interlock_unplaced_refs": sorted(expected & set(placed["unplaced_refs"]))})
    grouped_cases = []
    bypass_pairs = {f"C{66 + index}": f"U{47 + index}" for index in range(9)}
    for width in (108.0, 110.0):
        fixed = fit.fixed_boxes(parts, right_shift=width - fit.BOARD_W)
        placed = fit.place(parts, "dual-package candidate", "area first", fixed,
                           pack, sensor, board_width=width, nearby=bypass_pairs,
                           near_gap_mm=3.0)
        boxes = placed["boxes_mm"]
        placed_gaps = {f"{anchor_ref}/{cap_ref}": edge_gap_mm(boxes[anchor_ref], boxes[cap_ref])
                       for cap_ref, anchor_ref in bypass_pairs.items()
                       if anchor_ref in boxes and cap_ref in boxes}
        if any(gap > 3.0 for gap in placed_gaps.values()):
            raise ValueError("Bypass-locality placement exceeded its trial gap")
        grouped_cases.append({"board_width_mm": width, "trial_bypass_edge_gap_mm": 3.0,
                              "unplaced_count": placed["unplaced_count"],
                              "unplaced_refs": placed["unplaced_refs"],
                              "placed_bypass_edge_gaps_mm": placed_gaps,
                              "bypass_unplaced_refs": sorted(set(bypass_pairs) & set(placed["unplaced_refs"]))})
    return {"SPDX-License-Identifier": "CERN-OHL-S-2.0",
            "status": "COARSE_COURTYARD_SCREEN_NOT_PLACEMENT_OR_CASE_APPROVAL",
            "native_xml_sha256": hashlib.sha256(xml.read_bytes()).hexdigest(),
            "coupon_pcb_items": sum(counts.values()),
            "rear_screened_parts": len(parts),
            "captured_interlock_refs": sorted(expected),
            "cases": cases,
            "local_bypass_trial_cases": grouped_cases,
            "limitations": [
                "Dual row package substitution remains proposed, not source-captured",
                "Free first-fit cases have no circuit-local routing or bypass proximity constraints",
                "3 mm bypass trial constrains only IC/cap courtyard gaps and remains placement-order dependent",
                "Reported bypass edge gaps diagnose dispersal; no electrical distance limit is implied",
                "No traces, vias, thermal copper, antenna exclusion or assembly access",
                "110 mm case walls, USB opening and mechanical tolerances are absent",
            ]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("native_xml", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = screen(args.native_xml)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    for case in result["cases"]:
        print(f'{case["row_topology"]}, {case["board_width_mm"]:.0f} mm: '
              f'{case["unplaced_count"]} unplaced; '
              f'interlock misses: {case["interlock_unplaced_refs"]}')
    for case in result["local_bypass_trial_cases"]:
        print(f'3 mm bypass trial, {case["board_width_mm"]:.0f} mm: '
              f'{case["unplaced_count"]} unplaced; bypass misses: {case["bypass_unplaced_refs"]}')


if __name__ == "__main__":
    main()
