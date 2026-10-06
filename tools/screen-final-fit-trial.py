#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Build a to-scale, unconnected final-badge mechanical fit trial.

This deliberately does not produce a KiCad PCB or authorize fabrication.
"""

from __future__ import annotations

import importlib.util
import json
import math
import subprocess
import sys
import tempfile
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "mechanical/review"
for module_name, path in (
    ("preliminary_placement", ROOT / "tools/screen-preliminary-placement.py"),
    ("component_space", ROOT / "tools/screen-final-component-space.py"),
):
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
layout = sys.modules["preliminary_placement"]
space = sys.modules["component_space"]

BOARD_W, BOARD_H = layout.BOARD_W, layout.BOARD_H
GRID = 0.25
UNDER_PACK_FPS = {"R_Panasonic_ERJ2_0402", "C_Murata_GRM15_0402"}
NTC_TARGET = {"x0": 51.0, "y0": 14.25, "x1": 55.0, "y1": 18.25}


def overlap(a: dict, b: dict) -> bool:
    return a["x0"] < b["x1"] and a["x1"] > b["x0"] and a["y0"] < b["y1"] and a["y1"] > b["y0"]


def box(x: float, y: float, w: float, h: float) -> dict:
    return {"x0": round(x, 3), "y0": round(y, 3),
            "x1": round(x + w, 3), "y1": round(y + h, 3)}


def native_inventory() -> tuple[list[dict], dict]:
    with tempfile.TemporaryDirectory() as tmp:
        netlist = Path(tmp) / "coupon.xml"
        subprocess.run([space.kicad_cli(), "sch", "export", "netlist", "--format", "kicadxml",
                        "--output", str(netlist),
                        str(space.PROJECT / "rgb-badge-coupon.kicad_sch")],
                       check=True, stdout=subprocess.DEVNULL)
        return space.component_inventory(netlist)


def anchored_layout(inventory: list[dict]) -> tuple[list[dict], dict]:
    by_ref = {p["ref"]: p for p in inventory}
    base = layout.analyze()
    pack = base["battery_sensor_trial"]["lp503055_finished_body_max"]
    anchors: list[dict] = []

    def add(ref: str, category: str, x: float, y: float) -> None:
        p = by_ref[ref]
        anchors.append({"ref": ref, "category": category, "footprint": p["footprint"],
                        "box": box(x, y, p["width_mm"], p["height_mm"])})

    add("SW2", "top-edge control trial", 0.5, 0.3)
    add("SW1", "top-edge control trial", 10.5, 0.3)
    add("U2", "row decoder", 16.3, 0.45)
    # The external-antenna module is shifted left/down from the older rectangle
    # to expose a narrow strip for the row-stage bank. Its RF cable is unplaced.
    mcu_fp = layout.courtyard(layout.FOOTPRINTS / layout.PARTS["mcu"])
    anchors.append({"ref": "U3", "category": "MCU", "footprint": layout.PARTS["mcu"].removesuffix(".kicad_mod"),
                    "box": box(0.5, 9.25, mcu_fp.x1 - mcu_fp.x0, mcu_fp.y1 - mcu_fp.y0)})
    for i, rect in enumerate(base["rear_trial"]["drivers"], 1):
        anchors.append({"ref": f"U1-{i}", "category": "LED driver projection", "footprint": layout.PARTS["driver"].removesuffix(".kicad_mod"),
                        "box": rect})
    usb = layout.usb_courtyard(layout.courtyard(layout.FOOTPRINTS / layout.PARTS["usb"]))
    anchors.append({"ref": "J1", "category": "USB connector", "footprint": layout.PARTS["usb"].removesuffix(".kicad_mod"),
                    "box": vars(usb)})

    for n in range(16):
        add(f"Q{n+1}", "row P-MOS", 91.1 + (n % 2) * 3.55, 0.5 + (n // 2) * 3.8)
    nmos_xy = [(20.3, 9.3 + n * 3.4) for n in range(6)]
    nmos_xy += [(0.5, 5.1), (4.1, 5.1), (11.0, 4.2)]
    nmos_xy += [(x, y) for y in (0.5, 4.0, 23.0, 26.5) for x in (98.65, 102.2)]
    for n, (x, y) in enumerate(nmos_xy[:16]):
        add(f"Q{n+17}", "row N-MOS", x, y)

    for i, a in enumerate(anchors):
        for b in anchors[i+1:]:
            if overlap(a["box"], b["box"]):
                raise ValueError(f"Anchored courtyards overlap: {a['ref']} and {b['ref']}")
        r = a["box"]
        if r["x0"] < 0 or r["y0"] < 0 or r["x1"] > BOARD_W + 0.75 or r["y1"] > BOARD_H:
            raise ValueError(f"Anchor outside board/USB body guide: {a['ref']}")
        if a["ref"] != "J1" and overlap(r, pack):
            raise ValueError(f"Tall anchor intersects pack XY: {a['ref']}")
    return anchors, pack


def under_pack_trial(inventory: list[dict], pack: dict) -> list[dict]:
    by_ref = {p["ref"]: p for p in inventory}
    eligible = {p["ref"] for p in inventory if p["footprint"] in UNDER_PACK_FPS}
    placed: list[dict] = []
    def add(ref: str, x: float, y: float, category: str) -> None:
        p = by_ref[ref]
        r = box(x, y, p["width_mm"], p["height_mm"])
        if r["x0"] < pack["x0"] or r["y0"] < pack["y0"] or r["x1"] > pack["x1"] or r["y1"] > pack["y1"]:
            raise ValueError(f"Under-pack candidate outside pack: {ref}")
        if overlap(r, NTC_TARGET) or any(overlap(r, q["box"]) for q in placed):
            raise ValueError(f"Under-pack candidate collision: {ref}")
        placed.append({"ref": ref, "category": category, "footprint": p["footprint"], "box": r})
    # Keep the row-gate resistor pairs in two columns near the driver-side
    # edge. This is proximity intent, not a route-length qualification.
    for n in range(16):
        y = 1.2 + n * 1.875
        add(f"R{n+6}", 76.0, y, "row pull-up candidate")
        add(f"R{n+22}", 78.25, y, "row pull-down candidate")
    remaining = sorted(eligible - {p["ref"] for p in placed})
    for ref in remaining:
        candidate = by_ref[ref]
        found = False
        for yi in range(4, 116, 5):  # 1.0..28.75 mm, 1.25 mm pitch.
            for xi in range(104, 296, 9):  # 26..73.75 mm, 2.25 mm pitch.
                x, y = xi * GRID, yi * GRID
                r = box(x, y, candidate["width_mm"], candidate["height_mm"])
                if not overlap(r, NTC_TARGET) and all(not overlap(r, q["box"]) for q in placed):
                    add(ref, x, y, "other 0402 candidate")
                    found = True
                    break
            if found:
                break
        if not found:
            raise ValueError(f"Could not even place 0402 candidate in XY: {ref}")
    assert len(placed) == len(eligible) == 77
    return placed


def remaining_trial(inventory: list[dict], anchors: list[dict], under_pack: list[dict], pack: dict) -> tuple[list[dict], list[str]]:
    claimed = {p["ref"] for p in anchors + under_pack}
    parts = [p for p in inventory if p["ref"] not in claimed]
    nx, ny = int(BOARD_W / GRID), int(BOARD_H / GRID)
    occupied = [bytearray(nx) for _ in range(ny)]
    def mark(x: int, y: int, w: int, h: int) -> None:
        for yy in range(y, min(y + h, ny)):
            occupied[yy][x:min(x + w, nx)] = b"\x01" * max(0, min(x + w, nx) - x)
    for r in [pack, *[a["box"] for a in anchors]]:
        x0, y0 = math.floor(r["x0"] / GRID), math.floor(max(0, r["y0"]) / GRID)
        x1, y1 = math.ceil(min(BOARD_W, r["x1"]) / GRID), math.ceil(min(BOARD_H, r["y1"]) / GRID)
        mark(x0, y0, x1 - x0, y1 - y0)
    placed, unplaced = [], []
    for p in sorted(parts, key=lambda item: (-item["area_mm2"], item["ref"])):
        w, h = math.ceil(p["width_mm"] / GRID), math.ceil(p["height_mm"] / GRID)
        chosen = None
        for y in range(ny - h + 1):
            for x in range(nx - w + 1):
                if all(not any(occupied[yy][x:x+w]) for yy in range(y, y+h)):
                    chosen = x, y
                    break
            if chosen is not None:
                break
        if chosen is None:
            unplaced.append(p["ref"])
            continue
        x, y = chosen
        mark(x, y, w, h)
        placed.append({"ref": p["ref"], "category": "unrouted first-fit only", "footprint": p["footprint"],
                       "box": box(x * GRID, y * GRID, w * GRID, h * GRID)})
    return placed, unplaced


def candidate_package_minima() -> list[dict]:
    names = [
        ("BQ24074 charger IC", "VQFN_TI_RGT0016C_3x3mm_P0.5mm_EP1.68mm", 1),
        ("TPS63020 VLED IC", "VSON_TI_DSJ0014_4x3mm_P0.5mm_EP2.85x1.58mm", 1),
        ("TPS259474 input-switch candidate", "VQFN_TI_RPW0010A_2x2mm_HotRod", 2),
        ("INA232 current monitor candidate", "SOT23_THIN_TI_DDF0008A", 1),
    ]
    minima = []
    for label, fp, quantity in names:
        r = layout.courtyard(layout.FOOTPRINTS / f"{fp}.kicad_mod")
        minima.append({"label": label, "footprint": fp, "quantity": quantity,
                       "courtyard_mm": [round(r.x1-r.x0, 3), round(r.y1-r.y0, 3)]})
    return minima


def connector_envelope_screen(anchors: list[dict], placed: list[dict], pack: dict) -> dict:
    """Try an illustrative mated side-entry PH pocket, not a footprint/land audit."""
    sizes = [(8.0, 9.6), (9.6, 8.0)]
    grouped = [pack, *[p["box"] for p in anchors]]
    occupied = [*grouped, *[p["box"] for p in placed]]
    counts = []
    for w, h in sizes:
        fits_grouped = fits_all = 0
        for yi in range(round((BOARD_H - h) / GRID) + 1):
            for xi in range(round((BOARD_W - w) / GRID) + 1):
                candidate = box(xi * GRID, yi * GRID, w, h)
                if all(not overlap(candidate, other) for other in grouped):
                    fits_grouped += 1
                if all(not overlap(candidate, other) for other in occupied):
                    fits_all += 1
        counts.append({"envelope_mm": [w, h], "grid_mm": GRID,
                       "free_before_first_fit": fits_grouped, "free_after_first_fit": fits_all})
    return {
        "candidate_header": "JST S2B-PH-SM4-TB with PHR-2 housing; no pack termination selected",
        "status": "illustrative mated-connector pocket only; dimensions and direction are not an audited courtyard",
        "placements": counts,
        "omits": ["wire bend", "strain relief", "case wall", "routing", "mounting hardware"],
    }


def build() -> dict:
    inventory, counts = native_inventory()
    anchors, pack = anchored_layout(inventory)
    under = under_pack_trial(inventory, pack)
    placed, unplaced = remaining_trial(inventory, anchors, under, pack)
    captured_refs = {p["ref"] for p in inventory}
    accounted = {p["ref"] for p in anchors + under + placed} & captured_refs
    if accounted | set(unplaced) != captured_refs or accounted & set(unplaced):
        raise ValueError("Captured footprint accounting is incomplete or duplicated")
    section = [
        ("replaceable diffuser", 0.6), ("optical gap", 0.5),
        ("front LED maximum trial height", 1.2), ("PCB", 0.8),
        ("conditional 0402 height example", 0.55),
        ("electrical isolation", 0.3), ("swelling/installation allowance", 0.5),
        ("LP503055 maximum body", 5.3), ("rear shell", 1.0),
    ]
    total = round(sum(h for _, h in section), 3)
    return {
        "status": "mechanical feasibility trial only; no connected final PCB or physical fit approval",
        "board_mm": [BOARD_W, BOARD_H], "case_max_mm": [110, 35, 11],
        "pack_body_max_box_mm": pack, "battery_separate_and_wired": True,
        "ntc_xy_target_reservation_mm": NTC_TARGET,
        "front": {"trial_led_count": 768, "pitch_mm": 1.95,
                  "source": "mechanical/review/placement.svg; final LED choice pending"},
        "captured_footprint_count": sum(counts.values()),
        "rear_trial": {"anchors": anchors, "under_pack_0402_candidates": under,
                       "other_unrouted_first_fit": placed, "unplaced_captured_refs": unplaced},
        "unallocated_required_package_minima": candidate_package_minima(),
        "battery_connector_envelope_screen": connector_envelope_screen(anchors, placed, pack),
        "other_unallocated_needs": ["exact keyed battery connector and wire bend/strain relief",
                                    "antenna and coax route/case-edge zone",
                                    "mounting bosses and magnet clearance",
                                    "charger/VLED/input passives, inductors and thermal copper",
                                    "display interlock and gauge isolation",
                                    "two added driver support networks and all PCB routing"],
        "section": {"layers_front_to_rear_mm": section, "trial_total_mm": total,
                    "nominal_unused_with_11mm_case_mm": round(11-total, 3),
                    "note": "0.55 mm is an illustrative GRM155 0402 height; other candidate heights, support, solder, adhesive and tolerances are unqualified"},
    }


def plan_svg(report: dict) -> str:
    s = 8
    def draw(r: dict, fill: str, stroke: str = "#233", opacity: float = 1) -> str:
        return (f'<rect x="{r["x0"]*s:.2f}" y="{r["y0"]*s:.2f}" '
                f'width="{(r["x1"]-r["x0"])*s:.2f}" height="{(r["y1"]-r["y0"])*s:.2f}" '
                f'fill="{fill}" fill-opacity="{opacity}" stroke="{stroke}" stroke-width="0.7"/>')
    rear = report["rear_trial"]
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="-15 -40 {BOARD_W*s+30} {BOARD_H*s+260}">',
           '<title>RGB badge rear footprint and battery-over-board fit trial</title>',
           '<style>text{font:13px sans-serif;fill:#21313c}.small{font:11px sans-serif}</style>',
           f'<rect x="-15" y="-40" width="{BOARD_W*s+30}" height="{BOARD_H*s+260}" fill="white"/>',
           '<text x="0" y="-15">REAR · exact captured footprint courtyards; unconnected, incomplete final circuit</text>',
           draw(box(0, 0, BOARD_W, BOARD_H), "#f1f4f6"),
           draw(report["pack_body_max_box_mm"], "#f2d59e", "#9a6300", 0.55)]
    for p in rear["under_pack_0402_candidates"]:
        out.append(draw(p["box"], "#dcb95d", "#8b6b21", 0.9))
    out.append(draw(report["ntc_xy_target_reservation_mm"], "none", "#d2232a"))
    for p in rear["anchors"]:
        color = {"MCU":"#8fc69b", "LED driver projection":"#a8a2dc", "USB connector":"#f5aaac",
                 "row P-MOS":"#5079b6", "row N-MOS":"#64a0d4", "row decoder":"#a8cf96",
                 "top-edge control trial":"#c5a3cf"}[p["category"]]
        out.append(draw(p["box"], color))
        if p["category"] not in ("row P-MOS", "row N-MOS"):
            r=p["box"]
            out.append(f'<text class="small" x="{r["x0"]*s+2:.1f}" y="{r["y0"]*s+12:.1f}">{escape(p["ref"])}</text>')
    for p in rear["other_unrouted_first_fit"]:
        out.append(draw(p["box"], "#88bbc2", "#2f707c", 0.8))
    y0=BOARD_H*s+22
    out += [f'<text x="0" y="{y0}">Captured coupon parts: {report["captured_footprint_count"]}; 3 driver bodies projected for final board.</text>',
            f'<text x="0" y="{y0+20}">Under-pack 0402 positions: 77 conditional · captured parts still unplaced: {len(rear["unplaced_captured_refs"])}.</text>',
            f'<text x="0" y="{y0+40}">Charger, VLED, input protection, battery connector, RF and routing are not placed.</text>',
            f'<text x="0" y="{y0+60}">Battery needs case support above the board; height and circuit locality are unqualified.</text>',
            f'<text x="0" y="{y0+82}">UNALLOCATED PACKAGE MINIMA (shown to scale off-board; support parts need more space)</text>']
    labels = [("BQ", report["unallocated_required_package_minima"][0]["courtyard_mm"]),
              ("VLED", report["unallocated_required_package_minima"][1]["courtyard_mm"]),
              ("E0", report["unallocated_required_package_minima"][2]["courtyard_mm"]),
              ("E1", report["unallocated_required_package_minima"][2]["courtyard_mm"]),
              ("INA", report["unallocated_required_package_minima"][3]["courtyard_mm"])]
    x = 0.0
    for label, (w, h) in labels:
        out.append(f'<rect x="{x:.1f}" y="{y0+94:.1f}" width="{w*s:.1f}" height="{h*s:.1f}" fill="#d1d5d8" stroke="#596a72"/>')
        out.append(f'<text class="small" x="{x:.1f}" y="{y0+145:.1f}">{label}</text>')
        x += w*s + 25
    out.append('</svg>')
    return '\n'.join(out)+'\n'


def section_svg(report: dict) -> str:
    scale=32
    z=0.0
    colors=["#dfe4e8","#f4f4f4","#73b5d4","#447d92","#dcb95d","#b3d4bc","#f1f1f1","#f2d59e","#c5cdd3"]
    out=['<svg xmlns="http://www.w3.org/2000/svg" viewBox="-12 -35 780 460">',
         '<title>Illustrative 11 mm front-to-rear stack with a 0402 below the battery</title>',
         '<style>text{font:14px sans-serif;fill:#1e303a}</style>',
         '<rect x="-12" y="-35" width="780" height="460" fill="white"/>',
         '<text x="0" y="-10">SECTION · trial maximum stack at an under-pack 0402 location</text>']
    for (label,h),color in zip(report["section"]["layers_front_to_rear_mm"],colors):
        out.append(f'<rect x="0" y="{z*scale:.2f}" width="260" height="{h*scale:.2f}" fill="{color}" stroke="#2b3b42"/>')
        out.append(f'<text x="275" y="{(z+h/2)*scale+5:.2f}">{escape(label)} · {h:.2f} mm</text>')
        z+=h
    out.append(f'<rect x="0" y="{z*scale:.2f}" width="260" height="{(11-z)*scale:.2f}" fill="#ffffff" stroke="#d03c3c"/>')
    out.append(f'<text x="275" y="{(z+(11-z)/2)*scale+5:.2f}">Nominal unused allowance · {11-z:.2f} mm</text>')
    out += ['<text x="0" y="385">Pack is wired; a case support must hold it clear of the PCB.</text>',
            '<text x="0" y="406">Support, cover, solder, adhesive and tolerance are not verified by this arithmetic.</text>',
            '</svg>']
    return '\n'.join(out)+'\n'


def main() -> None:
    report=build()
    OUT.mkdir(parents=True,exist_ok=True)
    (OUT/'fit-trial.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    (OUT/'fit-trial-plan.svg').write_text(plan_svg(report),encoding='utf-8')
    (OUT/'fit-trial-section.svg').write_text(section_svg(report),encoding='utf-8')
    print(json.dumps({"captured":report["captured_footprint_count"],
                      "unplaced_captured":report["rear_trial"]["unplaced_captured_refs"],
                      "unallocated_package_minima":len(report["unallocated_required_package_minima"]),
                      "section":report["section"]},indent=2))


if __name__ == '__main__':
    main()
