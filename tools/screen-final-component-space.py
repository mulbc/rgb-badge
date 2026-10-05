#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Screen captured coupon parts against a hypothetical 48x16 rear floorplan.

This is a coarse 2D packing/area test, not PCB placement, routing or DRC.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import math
import os
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / "hardware/coupon/rev-a"
LAYOUT_SCRIPT = ROOT / "tools/screen-preliminary-placement.py"
spec = importlib.util.spec_from_file_location("preliminary_placement", LAYOUT_SCRIPT)
layout = importlib.util.module_from_spec(spec)
assert spec.loader is not None
sys.modules[spec.name] = layout
spec.loader.exec_module(layout)

GRID_MM = 0.25
TRIAL_COMPONENT_GAP_MM = 0.25  # Each side; not a routing or assembly clearance rule.
TEST_PAD_RESERVATION_MM = 1.5  # 1.0 mm pad plus a provisional 0.25 mm each side.
DRIVER_FP = layout.PARTS["driver"].removesuffix(".kicad_mod")
LARGE_FPS = {layout.PARTS[k].removesuffix(".kicad_mod") for k in ("mcu", "usb", "driver")}


def kicad_cli() -> str:
    candidate = os.environ.get("RGB_BADGE_KICAD_CLI")
    if candidate:
        return candidate
    app = Path("/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli")
    if app.is_file():
        return str(app)
    from shutil import which
    found = which("kicad-cli")
    if found:
        return found
    raise RuntimeError("KiCad CLI is needed to export the current schematic netlist")


def component_inventory(netlist: Path) -> tuple[list[dict], dict]:
    root = ET.parse(netlist).getroot()
    parts = []
    counts = Counter()
    for comp in root.findall("./components/comp"):
        ref = comp.attrib["ref"]
        fp = (comp.findtext("footprint") or "").split(":")[-1]
        if not fp:
            raise ValueError(f"{ref} has no footprint")
        counts[fp] += 1
        if fp.startswith("LED_") or fp in LARGE_FPS:
            continue
        if fp == "TestPoint_Pad_D1.0mm":
            width = height = TEST_PAD_RESERVATION_MM
            source = "1.0 mm pad with trial 1.5 mm square reservation"
        else:
            rect = layout.courtyard(layout.FOOTPRINTS / f"{fp}.kicad_mod")
            width, height = rect.x1 - rect.x0, rect.y1 - rect.y0
            source = "project-local F.CrtYd"
        parts.append({"ref": ref, "footprint": fp, "width_mm": width,
                      "height_mm": height, "area_mm2": round(width * height, 4), "source": source})
    return parts, dict(sorted(counts.items()))


def screen(parts: list[dict], counts: dict) -> dict:
    trial = layout.analyze()
    back = trial["rear_trial"]
    pack = trial["battery_sensor_trial"]["lp503055_finished_body_max"]
    usb = layout.usb_courtyard(layout.courtyard(layout.FOOTPRINTS / layout.PARTS["usb"]))
    fixed = {"lp503055_body": pack, "mcu": back["controller"],
             "drivers": back["drivers"], "usb_connector_courtyard": vars(usb)}
    board_area = layout.BOARD_W * layout.BOARD_H
    def area(box: dict) -> float:
        return (box["x1"] - box["x0"]) * (box["y1"] - box["y0"])
    pack_area = area(pack)
    usb_on_board = {"x0": max(0, usb.x0), "y0": max(0, usb.y0),
                    "x1": min(layout.BOARD_W, usb.x1), "y1": min(layout.BOARD_H, usb.y1)}
    fixed_area = area(back["controller"]) + sum(area(r) for r in back["drivers"]) + area(usb_on_board)
    free_area = board_area - pack_area - fixed_area
    small_area = sum(p["area_mm2"] for p in parts)

    # First-fit stress test with fixed large reservations and a small perimeter
    # around each remaining part. It ignores nets, thermal placement and routing.
    nx, ny = int(layout.BOARD_W / GRID_MM), int(layout.BOARD_H / GRID_MM)
    cells = [bytearray(nx) for _ in range(ny)]
    def occupy(x: int, y: int, w: int, h: int) -> None:
        for yy in range(y, min(y + h, ny)):
            cells[yy][x:min(x + w, nx)] = b"\x01" * max(0, min(x + w, nx) - x)
    for box in [pack, back["controller"], *back["drivers"], vars(usb)]:
        x0 = math.floor(box["x0"] / GRID_MM)
        y0 = math.floor(max(0, box["y0"]) / GRID_MM)
        x1 = math.ceil(min(layout.BOARD_W, box["x1"]) / GRID_MM)
        y1 = math.ceil(min(layout.BOARD_H, box["y1"]) / GRID_MM)
        occupy(x0, y0, x1 - x0, y1 - y0)
    placed, unplaced = [], []
    for part in sorted(parts, key=lambda p: (-p["area_mm2"], p["ref"])):
        w = math.ceil((part["width_mm"] + 2 * TRIAL_COMPONENT_GAP_MM) / GRID_MM)
        h = math.ceil((part["height_mm"] + 2 * TRIAL_COMPONENT_GAP_MM) / GRID_MM)
        chosen = None
        for y in range(ny - h + 1):
            for x in range(nx - w + 1):
                if all(not any(cells[yy][x:x + w]) for yy in range(y, y + h)):
                    chosen = (x, y)
                    break
            if chosen is not None:
                break
        if chosen is None:
            unplaced.append(part["ref"])
            continue
        x, y = chosen
        occupy(x, y, w, h)
        placed.append({"ref": part["ref"], "footprint": part["footprint"],
                       "x0": x * GRID_MM, "y0": y * GRID_MM,
                       "x1": (x + w) * GRID_MM, "y1": (y + h) * GRID_MM})
    return {
        "method": "2D courtyard-area lower bound and first-fit 0.25 mm grid stress test; not a PCB",
        "board_mm": [layout.BOARD_W, layout.BOARD_H],
        "assumptions": ["48x16 front LED array replaces the coupon's 256 mixed LEDs",
                        "three driver bodies replace the coupon's one driver body",
                        "all 151 other captured footprints are trialed on the rear outside the pack",
                        "only the LP503055 finished body is reserved; leads, PCM protrusion, connector and swelling are omitted",
                        "uncaptured charger, VLED, input protection and other final support parts are omitted"],
        "schematic_footprint_counts": counts,
        "fixed_boxes": fixed,
        "area_mm2": {"board": round(board_area, 2), "lp503055_body": round(pack_area, 2),
                     "mcu_three_drivers_usb": round(fixed_area, 2),
                     "free_after_fixed_boxes": round(free_area, 2),
                     "other_captured_courtyards_and_testpad_reservations": round(small_area, 2),
                     "remaining_before_clearance_routing_or_missing_parts": round(free_area - small_area, 2)},
        "packing_trial": {"component_gap_each_side_mm": TRIAL_COMPONENT_GAP_MM,
                          "placed_count": len(placed), "unplaced_count": len(unplaced),
                          "unplaced_refs": unplaced, "placed": placed},
        "inventory": parts,
    }


def svg(report: dict) -> str:
    scale = 8
    def rect(box: dict, color: str, opacity: float = 1) -> str:
        return (f'<rect x="{box["x0"] * scale:.2f}" y="{box["y0"] * scale:.2f}" '
                f'width="{(box["x1"] - box["x0"]) * scale:.2f}" '
                f'height="{(box["y1"] - box["y0"]) * scale:.2f}" '
                f'fill="{color}" opacity="{opacity}" stroke="#263238" stroke-width="0.5"/>')
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="-10 -35 {layout.BOARD_W * scale + 20} {layout.BOARD_H * scale + 100}">',
           '<title>Rear component-space stress test; unplaced components remain</title>',
           '<style>text{font:14px sans-serif;fill:#18242e}</style>',
           f'<rect x="-10" y="-35" width="{layout.BOARD_W * scale + 20}" height="{layout.BOARD_H * scale + 100}" fill="#ffffff"/>',
           '<text x="0" y="-12">REAR SPACE SCREEN · captured coupon parts projected onto final board</text>',
           f'<rect x="0" y="0" width="{layout.BOARD_W * scale}" height="{layout.BOARD_H * scale}" fill="#f4f6f8" stroke="#263238"/>']
    fixed = report["fixed_boxes"]
    out.append(rect(fixed["lp503055_body"], "#f2d59e"))
    out.append(rect(fixed["mcu"], "#8cc79b"))
    for box in fixed["drivers"]:
        out.append(rect(box, "#8982c6"))
    out.append(rect(fixed["usb_connector_courtyard"], "#f1a6a6"))
    for box in report["packing_trial"]["placed"]:
        out.append(rect(box, "#3d8fba", 0.8))
    out.append(f'<text x="0" y="{layout.BOARD_H * scale + 22:.0f}">First-fit only: {report["packing_trial"]["placed_count"]} placed, {report["packing_trial"]["unplaced_count"]} unplaced.</text>')
    out.append(f'<text x="0" y="{layout.BOARD_H * scale + 42:.0f}">No routing, thermal spacing, leads or unfinished power circuit included.</text>')
    out.append('</svg>')
    return '\n'.join(out) + '\n'


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    with tempfile.TemporaryDirectory() as tmp:
        netlist = Path(tmp) / "coupon.xml"
        subprocess.run([kicad_cli(), "sch", "export", "netlist", "--format", "kicadxml",
                        "--output", str(netlist), str(PROJECT / "rgb-badge-coupon.kicad_sch")],
                       check=True, stdout=subprocess.DEVNULL)
        parts, counts = component_inventory(netlist)
    report = screen(parts, counts)
    args.output.mkdir(parents=True, exist_ok=True)
    (args.output / "component-space.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    (args.output / "component-space.svg").write_text(svg(report), encoding="utf-8")
    print(json.dumps({"area_mm2": report["area_mm2"],
                      "packing_trial": {k: v for k, v in report["packing_trial"].items()
                                        if k in ("placed_count", "unplaced_count")}}, indent=2))


if __name__ == "__main__":
    main()
