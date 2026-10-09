#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Compare the LP452845 finished-body drawing with the existing rear fit trial.

This uses the saved October 6 geometric trial, not a completed PCB or routing.
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "mechanical/review/fit-trial.json"
OUTPUT = ROOT / "mechanical/review/lp452845-swap.json"


def overlaps(a, b):
    return a["x0"] < b["x1"] and a["x1"] > b["x0"] and a["y0"] < b["y1"] and a["y1"] > b["y0"]


def inside(inner, outer):
    return all(inner[key] >= outer[key] for key in ("x0", "y0")) and all(
        inner[key] <= outer[key] for key in ("x1", "y1"))


def pocket_positions(board_w, board_h, obstacles, width, height):
    # Reuse the fit trial's 0.25 mm grid and illustrative PH pocket dimensions.
    count = 0
    for yi in range(round((board_h - height) / .25) + 1):
        for xi in range(round((board_w - width) / .25) + 1):
            x, y = xi * .25, yi * .25
            pocket = {"x0": x, "y0": y, "x1": x + width, "y1": y + height}
            count += all(not overlaps(pocket, item) for item in obstacles)
    return count


def report():
    source = json.loads(SOURCE.read_text())
    board_w, board_h = source["board_mm"]
    old_pack = source["pack_body_max_box_mm"]
    # LiPol drawing FD_6225_10, index 1: 46 ±1 × 28 ±0.5 × 4.5 ±0.3 mm.
    new_w, new_h, new_t = 47.0, 28.5, 4.8
    new_pack = {"x0": (board_w - new_w) / 2, "y0": (board_h - new_h) / 2,
                "x1": (board_w + new_w) / 2, "y1": (board_h + new_h) / 2}
    anchors = source["rear_trial"]["anchors"]
    under = source["rear_trial"]["under_pack_0402_candidates"]
    obstacles = [new_pack, *(item["box"] for item in anchors)]
    # Conditional dual-row-package layout already reserves 8 x 8 mm beside the
    # old pack. The shorter pack permits a 9.6 x 8 mm illustrative PH pocket.
    dual = source["dual_row_package_screen"]
    ph_pocket = {"x0": 16.5, "y0": 0.5, "x1": 26.1, "y1": 8.5}
    dual_fixed = [item for item in dual["fixed_and_reservations"] if item["ref"] != "BAT"]
    dual_other = dual["other_unrouted_first_fit"]
    ntc = source["ntc_xy_target_reservation_mm"]
    prior_under = dual["under_pack_0402_candidates"]
    retained = [item for item in prior_under if inside(item["box"], new_pack)
                and not overlaps(item["box"], ph_pocket)]
    repacked = []
    for item in prior_under:
        if item in retained:
            continue
        chosen = None
        for yi in range(9, 119, 5):
            for xi in range(119, 299, 9):
                x, y = xi * .25, yi * .25
                candidate = {"x0": x, "y0": y, "x1": x + 2.0, "y1": y + 1.0}
                if inside(candidate, new_pack) and not overlaps(candidate, ntc) and all(
                    not overlaps(candidate, other["box"]) for other in retained + repacked
                ):
                    chosen = candidate
                    break
            if chosen:
                break
        if chosen is None:
            raise ValueError(f"Cannot repack 0402 {item['ref']}")
        repacked.append({**item, "box": chosen})
    dual_collisions = [item["ref"] for item in dual_fixed + dual_other
                       if overlaps(item["box"], ph_pocket) or overlaps(item["box"], new_pack)]
    assert not dual_collisions and len(retained) + len(repacked) == 77
    assert not overlaps(ph_pocket, new_pack)
    for index, item in enumerate(retained + repacked):
        assert inside(item["box"], new_pack) and not overlaps(item["box"], ntc)
        assert not any(overlaps(item["box"], other["box"])
                       for other in (retained + repacked)[index + 1:])
    old_area = (old_pack["x1"] - old_pack["x0"]) * (old_pack["y1"] - old_pack["y0"])
    new_area = new_w * new_h
    old_section = source["section"]["trial_total_mm"]
    new_section = round(old_section - 5.3 + new_t, 3)
    return {
        "SPDX-License-Identifier": "CERN-OHL-S-2.0",
        "status": "GEOMETRIC_SWAP_SCREEN_NOT_PCB_FIT_OR_PACK_SELECTION",
        "source_trial": "mechanical/review/fit-trial.json",
        "pack_drawing": "LiPol FD_6225_10 index 1, LP452845 with PCM and JST PHR-2",
        "old_pack_max_box_mm": old_pack,
        "lp452845_max_body_box_mm": new_pack,
        "freed_projected_body_area_mm2": round(old_area - new_area, 2),
        "old_under_pack_0402_positions_retained_without_move": sum(inside(item["box"], new_pack) for item in under),
        "old_under_pack_0402_positions_needing_move": sum(not inside(item["box"], new_pack) for item in under),
        "anchored_courtyards_now_overlapping_pack": [item["ref"] for item in anchors if overlaps(item["box"], new_pack)],
        "illustrative_ph_pocket_free_positions_before_repacking": {
            "8x9.6_mm": pocket_positions(board_w, board_h, obstacles, 8.0, 9.6),
            "9.6x8_mm": pocket_positions(board_w, board_h, obstacles, 9.6, 8.0),
        },
        "illustrative_section_total_mm": new_section,
        "nominal_unused_in_11mm_case_mm": round(11.0 - new_section, 3),
        "dual_row_package_variant": {
            "status": "CONDITIONAL_XY_REPACK_ONLY_NO_ROUTING_OR_ASSEMBLY_CLEARANCE",
            "illustrative_ph_pocket_box_mm": ph_pocket,
            "fixed_or_other_courtyard_collisions_with_new_pack_or_pocket": dual_collisions,
            "old_0402_positions_retained": len(retained),
            "0402_positions_repacked": len(repacked),
            "0402_positions_total": len(retained) + len(repacked),
            "0402_positions": [*retained, *repacked],
        },
        "limitations": ["dual-row-package proposal is unapproved", "illustrative PH pocket is not a footprint",
                        "no PCB routes, support, wire bend, local PCM shape or swelling measurement"],
    }


if __name__ == "__main__":
    OUTPUT.write_text(json.dumps(report(), indent=2) + "\n")
