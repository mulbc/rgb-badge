#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Visual, deterministic bounding-box screen; NOT a KiCad board or DRC."""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[1]
FOOTPRINTS = ROOT / "hardware/coupon/rev-a/footprints/rgb-badge-coupon.pretty"
PARTS = {
    "led": "LED_QTBrightek_QBLP1515A-RGB2A.kicad_mod",
    "usb": "USB_C_GCT_USB4505-03-0-A_MidMount.kicad_mod",
    "mcu": "ESP32-S3-WROOM-1U.kicad_mod",
    "driver": "QFN_TI_RTQ0056E_8x8mm_P0.5mm_EP5.7mm.kicad_mod",
}
BOARD_W, BOARD_H, PITCH = 106.0, 32.5, 1.95
USB_CUTOUT_DATUM = 6.75  # Audit of GCT A2; guides also checked below.
USB_REAR_DATUM = 0.55
PACK_W, PACK_H = 50.5, 30.5  # Coupon-only GlobTek BL0750F5030481S1PCTC bounding size.


@dataclass(frozen=True)
class Rect:
    x0: float
    y0: float
    x1: float
    y1: float

    def shifted(self, x: float, y: float) -> Rect:
        return Rect(self.x0 + x, self.y0 + y, self.x1 + x, self.y1 + y)

    def rotated90(self) -> Rect:
        return Rect(-self.y1, self.x0, -self.y0, self.x1)

    def gap_x(self, other: Rect) -> float:
        return other.x0 - self.x1

    def overlap(self, other: Rect) -> bool:
        return self.x0 < other.x1 and self.x1 > other.x0 and self.y0 < other.y1 and self.y1 > other.y0


def courtyard(path: Path) -> Rect:
    text = path.read_text(encoding="utf-8")
    # Stop at the next rectangle, so a F.Fab outline cannot borrow a later F.CrtYd layer.
    rects = re.findall(r"\(fp_rect\b(?:(?!\(fp_rect\b).)*?\(layer\s+\"F.CrtYd\"\)", text, re.S)
    if len(rects) != 1:
        raise ValueError(f"expected one front courtyard rectangle in {path}: found {len(rects)}")
    match = re.search(r"\(start\s+([-.\d]+)\s+([-.\d]+)\).*?\(end\s+([-.\d]+)\s+([-.\d]+)\)", rects[0], re.S)
    if match is None:
        raise ValueError(f"missing courtyard coordinates in {path}")
    x0, y0, x1, y1 = map(float, match.groups())
    if not x0 < x1 or not y0 < y1:
        raise ValueError(f"invalid courtyard in {path}")
    return Rect(x0, y0, x1, y1)


def usb_courtyard(footprint: Rect) -> Rect:
    # 90-degree clockwise to point the connector through the right short edge.
    # Local +Y faces toward the right board edge; local Y=6.75 is the edge datum.
    return Rect(BOARD_W + footprint.y0 - USB_CUTOUT_DATUM,
                BOARD_H / 2 + footprint.x0,
                BOARD_W + footprint.y1 - USB_CUTOUT_DATUM,
                BOARD_H / 2 + footprint.x1)


def validate_usb_guide(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    for needle in ('(start -4.62 6.75) (end -4.62 0.55)',
                   '(start -4.62 0.55) (end 4.62 0.55)',
                   '(start 4.62 0.55) (end 4.62 6.75)'):
        if needle not in text:
            raise ValueError(f"USB cutout guide changed in {path}; re-audit drawing")


def analyze() -> dict:
    led, usb, mcu, driver = (courtyard(FOOTPRINTS / PARTS[name]) for name in PARTS)
    validate_usb_guide(FOOTPRINTS / PARTS["usb"])
    connector = usb_courtyard(usb)
    grid_x0 = (BOARD_W - PITCH * 47) / 2
    grid_y0 = (BOARD_H - PITCH * 15) / 2

    def grid(shift: float) -> list[Rect]:
        return [(led if (row + col) % 2 == 0 else led.rotated90()).shifted(
            grid_x0 + col * PITCH - shift, grid_y0 + row * PITCH)
            for row in range(16) for col in range(48)]

    centered = grid(0)
    # A margin to the USB courtyard; 0.25 mm is illustrative, not a clearance rule.
    nearest = max((r.x1 for r in centered if r.y0 < connector.y1 and r.y1 > connector.y0))
    shift = round(nearest - connector.x0 + 0.25, 3)
    moved = grid(shift)
    pack = Rect((BOARD_W - PACK_W) / 2, (BOARD_H - PACK_H) / 2,
                (BOARD_W + PACK_W) / 2, (BOARD_H + PACK_H) / 2)
    # Trial rear reservations; NOT placed components or a complete packing solution.
    controller = mcu.shifted(14.5, BOARD_H / 2)
    drivers = [driver.shifted(83.0, y) for y in (5.0, BOARD_H / 2, 27.5)]
    rear = [controller, *drivers]
    bbox = Rect(0, 0, BOARD_W, BOARD_H)
    return {
        "inputs": {"board_mm": [BOARD_W, BOARD_H], "pitch_mm": PITCH,
                   "led_courtyard_mm": vars(led), "usb_courtyard_local_mm": vars(usb),
                   "pack_coupon_only_mm": [PACK_W, PACK_H]},
        "centered": {"usb_courtyard_overlaps": sum(r.overlap(connector) for r in centered),
                     "worst_horizontal_courtyard_gap_mm": round(connector.x0 - nearest, 3),
                     "straight_cutout_inner_x_mm": BOARD_W - (USB_CUTOUT_DATUM - USB_REAR_DATUM)},
        "shifted_trial": {"shift_left_mm": shift,
                          "usb_courtyard_overlaps": sum(r.overlap(connector) for r in moved),
                          "worst_horizontal_courtyard_gap_mm": round(connector.x0 - max(r.x1 for r in moved if r.y0 < connector.y1 and r.y1 > connector.y0), 3),
                          "smallest_left_courtyard_edge_mm": round(min(r.x0 for r in moved), 3)},
        "rear_trial": {"pack": vars(pack), "controller": vars(controller),
                       "drivers": [vars(r) for r in drivers],
                       "any_rear_box_overlap": any(a.overlap(b) for i, a in enumerate(rear + [pack]) for b in (rear + [pack])[i + 1:]),
                       "all_rear_boxes_inside_board": all(r.x0 >= bbox.x0 and r.y0 >= bbox.y0 and r.x1 <= bbox.x1 and r.y1 <= bbox.y1 for r in rear + [pack])},
    }


def svg(report: dict) -> str:
    width, height, scale = BOARD_W, BOARD_H, 8
    gap = 22
    y_offset = height + gap
    def rect(box: dict | Rect, fill: str, stroke: str, yshift: float = 0, opacity: float = 1) -> str:
        r = box if isinstance(box, Rect) else Rect(**box)
        return f'<rect x="{r.x0*scale:.2f}" y="{(r.y0+yshift)*scale:.2f}" width="{(r.x1-r.x0)*scale:.2f}" height="{(r.y1-r.y0)*scale:.2f}" fill="{fill}" stroke="{stroke}" opacity="{opacity}"/>'
    shift = report["shifted_trial"]["shift_left_mm"]
    led = Rect(**report["inputs"]["led_courtyard_mm"])
    gx = (width - 47 * PITCH) / 2
    gy = (height - 15 * PITCH) / 2
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="-20 -28 {width*scale+40} {(height*2+gap)*scale+90}">',
           '<title>Preliminary RGB badge two-face bounding-box study; not a PCB</title>',
           '<style>text{font:14px sans-serif;fill:#192535} .small{font:11px sans-serif}</style>',
           '<text x="0" y="-8">FRONT · 48 × 16 QT LED courtyards, left shift ' + escape(str(shift)) + ' mm</text>',
           rect(Rect(0, 0, width, height), '#f2f5f8', '#27313b'),
           rect(Rect(width - 6.2, height/2 - 4.62, width, height/2 + 4.62), '#ffd6d6', '#db3030'),
           rect(usb_courtyard(Rect(**report["inputs"]["usb_courtyard_local_mm"])), 'none', '#d22a30')]
    for row in range(16):
        for col in range(48):
            r = (led if (row+col)%2==0 else led.rotated90()).shifted(gx+col*PITCH-shift, gy+row*PITCH)
            out.append(rect(r, '#48a4d0', 'none', opacity=0.65))
    out.extend(['<text x="0" y="' + str((y_offset-5)*scale) + '">REAR · coupon-only pack envelope and selected large footprints</text>',
                rect(Rect(0, 0, width, height), '#f2f5f8', '#27313b', y_offset)])
    back = report["rear_trial"]
    out.append(rect(back["pack"], '#f1dbab', '#9c6e00', y_offset))
    out.append(rect(back["controller"], '#aad7ae', '#217b38', y_offset))
    for item in back["drivers"]:
        out.append(rect(item, '#b8b3e4', '#5a49b1', y_offset))
    out.extend([f'<text class="small" x="{(back["pack"]["x0"]+2)*scale:.0f}" y="{(y_offset+height/2)*scale:.0f}">700 mAh coupon pack*</text>',
                f'<text class="small" x="0" y="{(y_offset+height+4)*scale:.0f}">*Volume, wires and height unmodelled; rear boxes are reservations, not a routed layout.</text>',
                '</svg>'])
    return '\n'.join(out) + '\n'


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True, help="output directory for JSON and SVG (build/ is gitignored)")
    args = parser.parse_args()
    report = analyze()
    args.output.mkdir(parents=True, exist_ok=True)
    (args.output / "placement.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    (args.output / "placement.svg").write_text(svg(report), encoding="utf-8")
    print(json.dumps({"centered": report["centered"], "shifted_trial": report["shifted_trial"],
                      "rear_trial": {k: v for k, v in report["rear_trial"].items() if k.startswith("any_") or k.startswith("all_")}}, indent=2))


if __name__ == "__main__":
    main()
