#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Run a current-inventory LP452845 rear-courtyard first-fit stress screen.

The result is neither a KiCad PCB nor electrical, routing, height or assembly proof.
"""

import argparse
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("component_space", ROOT / "tools/screen-final-component-space.py")
space = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = space
SPEC.loader.exec_module(space)
layout = space.layout
GRID = 0.25
BOARD_W, BOARD_H = 106.0, 32.5
EXTRA_BOX_MM = 0.5
LOW_FOOTPRINTS = {"R_Panasonic_ERJ2_0402", "R_Panasonic_ERA2_0402",
                  "C_Murata_GRM15_0402", "NTC_Murata_NCU15_0402"}
PAIR_FOOTPRINT = "U-DFN2020-6_TypeB_Diodes_DMC1229UFDB"


def box(x, y, w, h):
    return (round(x, 3), round(y, 3), round(x + w, 3), round(y + h, 3))


def overlap(a, b):
    return a[0] < b[2] and a[2] > b[0] and a[1] < b[3] and a[3] > b[1]


def fixed_boxes(parts, right_shift=0):
    by_ref = {p["ref"]: p for p in parts}
    fixed_xy = {"J2": (20.25, 0.25), "SW2": (0.5, 0.3),
                "SW1": (91.1, 0.3), "U2": (97.0, 0.5)}
    fixed = {ref: box(x, y, by_ref[ref]["width_mm"], by_ref[ref]["height_mm"])
             for ref, (x, y) in fixed_xy.items()}
    mcu = layout.courtyard(layout.FOOTPRINTS / layout.PARTS["mcu"])
    fixed["U3"] = box(0.5, 9.25, mcu.x1 - mcu.x0, mcu.y1 - mcu.y0)
    usb = layout.usb_courtyard(layout.courtyard(layout.FOOTPRINTS / layout.PARTS["usb"]))
    fixed["J1"] = (usb.x0, usb.y0, usb.x1, usb.y1)
    driver = layout.analyze()["rear_trial"]["drivers"]
    for index, item in enumerate(driver, 1):
        fixed[f"U1-project-{index}"] = tuple(item[key] for key in ("x0", "y0", "x1", "y1"))
    for ref in ("J1", "U2", "SW1"):
        x0, y0, x1, y1 = fixed[ref]
        fixed[ref] = (x0 + right_shift, y0, x1 + right_shift, y1)
    return fixed


def place(parts, variant, order, fixed, pack, sensor_reserve, board_width=BOARD_W,
          nearby=None, near_gap_mm=3.0, priority_refs=()):
    used = dict(fixed)
    remaining = [p for p in parts if p["ref"] not in set(fixed) | {"J2", "SW1", "SW2", "U2"}]
    if variant == "dual-package candidate":
        remaining = [p for p in remaining if not (p["ref"].startswith("Q") and p["ref"][1:].isdigit())]
        pair = layout.courtyard(layout.FOOTPRINTS / f"{PAIR_FOOTPRINT}.kicad_mod")
        width, height = pair.x1 - pair.x0, pair.y1 - pair.y0
        remaining.extend({"ref": f"PAIR{n + 1:02d}", "footprint": PAIR_FOOTPRINT,
                          "width_mm": width, "height_mm": height, "area_mm2": width * height}
                         for n in range(16))
    large = [p for p in remaining if p["footprint"] not in LOW_FOOTPRINTS]
    small = [p for p in remaining if p["footprint"] in LOW_FOOTPRINTS]
    if order == "area first":
        priority = set(priority_refs)
        large.sort(key=lambda p: (0 if p["ref"] in priority else 1,
                                  -p["area_mm2"], p["ref"]))
    else:
        large.sort(key=lambda p: (0 if p["ref"].startswith(("Q", "PAIR")) else 1,
                                  -p["area_mm2"], p["ref"]))
    small.sort(key=lambda p: p["ref"])

    def find(part, under_pack):
        w = math.ceil((part["width_mm"] + EXTRA_BOX_MM) / GRID) * GRID
        h = math.ceil((part["height_mm"] + EXTRA_BOX_MM) / GRID) * GRID
        x_start = math.ceil(pack[0] / GRID) if under_pack else 0
        x_end = math.floor((pack[2] - w) / GRID) if under_pack else math.floor((board_width - w) / GRID)
        y_start = math.ceil(pack[1] / GRID) if under_pack else 0
        y_end = math.floor((pack[3] - h) / GRID) if under_pack else math.floor((BOARD_H - h) / GRID)
        for yi in range(y_start, y_end + 1):
            for xi in range(x_start, x_end + 1):
                candidate = box(xi * GRID, yi * GRID, w, h)
                if (not under_pack and overlap(candidate, pack)) or overlap(candidate, sensor_reserve):
                    continue
                if any(overlap(candidate, other) for other in used.values()):
                    continue
                return candidate
        return None

    def find_near(part, anchor_ref):
        if anchor_ref not in used:
            return None
        anchor = used[anchor_ref]
        w = math.ceil((part["width_mm"] + EXTRA_BOX_MM) / GRID) * GRID
        h = math.ceil((part["height_mm"] + EXTRA_BOX_MM) / GRID) * GRID
        xlo = max(0, math.floor((anchor[0] - near_gap_mm - w) / GRID))
        xhi = min(math.floor((board_width - w) / GRID),
                  math.ceil((anchor[2] + near_gap_mm) / GRID))
        ylo = max(0, math.floor((anchor[1] - near_gap_mm - h) / GRID))
        yhi = min(math.floor((BOARD_H - h) / GRID),
                  math.ceil((anchor[3] + near_gap_mm) / GRID))
        candidates = []
        for yi in range(ylo, yhi + 1):
            for xi in range(xlo, xhi + 1):
                candidate = box(xi * GRID, yi * GRID, w, h)
                dx = max(anchor[0] - candidate[2], candidate[0] - anchor[2], 0)
                dy = max(anchor[1] - candidate[3], candidate[1] - anchor[3], 0)
                gap = math.hypot(dx, dy)
                if gap > near_gap_mm or overlap(candidate, pack) or overlap(candidate, sensor_reserve):
                    continue
                if any(overlap(candidate, other) for other in used.values()):
                    continue
                candidates.append((gap, yi, xi, candidate))
        return min(candidates)[3] if candidates else None

    unplaced = []
    under_count = 0
    nearby = nearby or {}
    nearby_parts = {part["ref"]: part for part in small if part["ref"] in nearby}
    near_by_anchor = {}
    for near_ref, anchor_ref in nearby.items():
        if near_ref not in nearby_parts:
            raise ValueError(f"{near_ref} is not a screened small part")
        near_by_anchor.setdefault(anchor_ref, []).append(near_ref)
    for part in large:
        found = find(part, False)
        if found is None:
            unplaced.append(part["ref"])
        else:
            used[part["ref"]] = found
        for near_ref in near_by_anchor.get(part["ref"], []):
            near_found = find_near(nearby_parts[near_ref], part["ref"])
            if near_found is None:
                unplaced.append(near_ref)
            else:
                used[near_ref] = near_found
    for part in small:
        if part["ref"] in nearby:
            continue
        found = find(part, True)
        if found is not None:
            under_count += 1
        else:
            found = find(part, False)
        if found is None:
            unplaced.append(part["ref"])
        else:
            used[part["ref"]] = found
    for index, (ref, rect) in enumerate(used.items()):
        if ref != "J1" and (rect[0] < 0 or rect[1] < 0 or rect[2] > board_width or rect[3] > BOARD_H):
            raise ValueError(f"{ref} outside trial board")
        if any(overlap(rect, other) for other in list(used.values())[index + 1:]):
            raise ValueError(f"{ref} overlaps another courtyard box")
    if len(used) + len(unplaced) != len(remaining) + len(fixed):
        raise ValueError("Current inventory was not accounted for")
    return {"variant": variant, "order": order, "placed_boxes": len(used),
            "small_parts_placed_under_pack": under_count, "unplaced_count": len(unplaced),
            "unplaced_refs": unplaced, "boxes_mm": {ref: list(rect) for ref, rect in sorted(used.items())}}


def report(xml):
    parts, counts = space.component_inventory(xml)
    if sum(counts.values()) != 466 or len(parts) != 207:
        raise ValueError("Schematic inventory has changed; re-audit this screen before use")
    pack = box(31.0, 2.0, 47.0, 28.5)  # LP452845 max body, October 9 swap origin.
    sensor = box(49.5, 12.25, 10.0, 8.0)
    fixed = fixed_boxes(parts)
    for index, rect in enumerate(fixed.values()):
        if overlap(rect, pack) or any(overlap(rect, other) for other in list(fixed.values())[index + 1:]):
            raise ValueError("Fixed envelope collision")
    results = [place(parts, variant, order, fixed, pack, sensor)
               for variant in ("canonical 32 separate row FETs", "dual-package candidate")
               for order in ("area first", "rows first")]
    reserve_sensitivity = []
    for name, pocket in (("10x10 left of pack", box(20.25, 11.0, 10.0, 10.0)),
                         ("7x12 beside decoder", box(91.0, 10.0, 7.0, 12.0))):
        if overlap(pocket, pack) or any(overlap(pocket, item) for item in fixed.values()):
            raise ValueError(f"Interlock reservation overlaps a fixed envelope: {name}")
        for order in ("area first", "rows first"):
            screened = place(parts, "dual-package candidate", order,
                             {**fixed, "INTERLOCK_RESERVE": pocket}, pack, sensor)
            reserve_sensitivity.append({"reservation": name, "box_mm": list(pocket),
                                        "order": order, "unplaced_count": screened["unplaced_count"],
                                        "unplaced_refs": screened["unplaced_refs"]})
    retained_test_pads = {"TP2", "TP3", "TP7", "TP8", "TP9", "TP10", "TP34", "TP35"}
    reduced_pad_parts = [p for p in parts if not p["ref"].startswith("TP") or p["ref"] in retained_test_pads]
    reduced_pad_sensitivity = []
    narrow_pocket = box(91.0, 10.0, 7.0, 12.0)
    for order in ("area first", "rows first"):
        screened = place(reduced_pad_parts, "dual-package candidate", order,
                         {**fixed, "INTERLOCK_RESERVE": narrow_pocket}, pack, sensor)
        reduced_pad_sensitivity.append({"order": order, "unplaced_count": screened["unplaced_count"],
                                        "unplaced_refs": screened["unplaced_refs"]})
    width_sensitivity = []
    for width in (106.0, 108.0, 110.0):
        shifted_fixed = fixed_boxes(parts, right_shift=width - BOARD_W)
        screened = place(parts, "dual-package candidate", "area first",
                         {**shifted_fixed, "INTERLOCK_RESERVE": narrow_pocket}, pack, sensor,
                         board_width=width)
        width_sensitivity.append({"board_width_mm": width, "order": "area first",
                                  "unplaced_count": screened["unplaced_count"],
                                  "unplaced_refs": screened["unplaced_refs"]})
    return {"SPDX-License-Identifier": "CERN-OHL-S-2.0",
            "status": "GEOMETRIC_FIRST_FIT_STRESS_SCREEN_NOT_A_PCB_OR_FIT_APPROVAL",
            "native_xml_sha256": hashlib.sha256(xml.read_bytes()).hexdigest(),
            "board_mm": [BOARD_W, BOARD_H], "source_coupon_pcb_items": sum(counts.values()),
            "pack_body_box_mm": list(pack), "sensor_cluster_reserved_box_mm": list(sensor),
            "additional_box_width_and_height_mm": EXTRA_BOX_MM,
            "fixed_envelopes_mm": {ref: list(rect) for ref, rect in fixed.items()},
            "variants": results, "interlock_reservation_sensitivity": reserve_sensitivity,
            "test_pad_omission_sensitivity": {
                "status": "trial only; not an approved final-board test-access plan",
                "retained_test_pad_refs": sorted(retained_test_pads),
                "omitted_test_pad_count": 22 - len(retained_test_pads),
                "interlock_reserve_box_mm": list(narrow_pocket),
                "dual_package_results": reduced_pad_sensitivity,
            },
            "board_width_sensitivity": {
                "status": "geometric option only; PCB and 110mm case mechanical fit unverified",
                "assumptions": ["Board is lengthened at the right edge", "USB J1, decoder U2 and switch SW1 shift right with the edge",
                                "Pack, sensor, three driver projections and 7x12mm interlock reservation stay at their 106mm-trial positions"],
                "dual_package_results": width_sensitivity,
            },
            "limitations": ["Only the selected pack's maximum body rectangle is modeled; no wires, PCM protrusion, swell or support",
                            "Three final driver bodies are projected from the one-driver coupon",
                            "Under-pack placement is conditional on insulation, height and sensor coupling",
                            "Sensor reservation does not force the actual NTC/TMP390 components into that region",
                            "The dual package is not accepted electrically or in the canonical schematic",
                            "No display interlock components, routes, copper, RF cable, mounting or case tolerance are modeled"]}


def svg(result):
    variant = next(item for item in result["variants"]
                   if item["variant"] == "dual-package candidate" and item["order"] == "area first")
    scale = 10
    out = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="-12 -35 1084 410">',
           '<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->',
           '<title>LP452845 current-inventory dual-package XY screen; no routing or fit approval</title>',
           '<rect x="-12" y="-35" width="1084" height="410" fill="white"/>',
           '<text x="0" y="-12" font-family="sans-serif" font-size="15">Dual-package candidate · geometric first fit only</text>',
           f'<rect x="0" y="0" width="{BOARD_W * scale}" height="{BOARD_H * scale}" fill="#f3f6f8" stroke="#182a3a"/>']
    def draw(rect, color, opacity=1.0, stroke="#35424e"):
        x0, y0, x1, y1 = rect
        out.append(f'<rect x="{x0 * scale:.2f}" y="{y0 * scale:.2f}" '
                   f'width="{(x1 - x0) * scale:.2f}" height="{(y1 - y0) * scale:.2f}" '
                   f'fill="{color}" fill-opacity="{opacity}" stroke="{stroke}" stroke-width=".8"/>')
    draw(result["pack_body_box_mm"], "#efd89b", 0.7, "#b1812a")
    draw(result["sensor_cluster_reserved_box_mm"], "#e9b5b0", 0.7, "#b14a43")
    fixed = set(result["fixed_envelopes_mm"])
    for ref, rect in variant["boxes_mm"].items():
        if ref in fixed:
            color = "#604d9b"
        elif ref.startswith("PAIR"):
            color = "#25a574"
        else:
            color = "#438db8"
        draw(rect, color, 0.75)
    out.append('<text x="0" y="354" font-family="sans-serif" font-size="12">Purple: fixed envelopes · green: unapproved row-package substitution · blue: other captured items · gold: pack body · red: sensor reservation</text>')
    out.append('<text x="0" y="374" font-family="sans-serif" font-size="12">Conditional under-pack parts, no circuit-locality constraint, no interlock, routing, height, support or DRC.</text>')
    out.append('</svg>')
    return "\n".join(out) + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("native_xml", type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--svg", type=Path)
    args = parser.parse_args()
    result = report(args.native_xml)
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    if args.svg:
        args.svg.write_text(svg(result), encoding="utf-8")
    for item in result["variants"]:
        print(f"{item['variant']}, {item['order']}: {item['unplaced_count']} unplaced")
    for item in result["interlock_reservation_sensitivity"]:
        print(f"dual-package candidate with {item['reservation']}, {item['order']}: "
              f"{item['unplaced_count']} unplaced")
    for item in result["test_pad_omission_sensitivity"]["dual_package_results"]:
        print(f"dual-package candidate with 14 coupon test pads omitted and 7x12 reserve, "
              f"{item['order']}: {item['unplaced_count']} unplaced")
    for item in result["board_width_sensitivity"]["dual_package_results"]:
        print(f"dual-package candidate with 7x12 reserve on {item['board_width_mm']:.0f}mm board: "
              f"{item['unplaced_count']} unplaced")


if __name__ == "__main__":
    main()
