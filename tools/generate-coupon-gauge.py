#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Generate a staged MAX17048 sheet into a new directory, never in place.

The switched battery input is an explicit draft boundary. Neither a switch nor
a charger/battery path exists in this sheet; a power flag is an ERC assumption.
"""

import argparse
import json
from pathlib import Path
import re
import uuid


PROJECT = Path(__file__).resolve().parents[1] / "hardware/coupon/rev-a"
ROOT_UUID = "207fb68e-2ddb-46bb-8712-eba2f8c5eef6"
SHEET_UUID = "a3481745-5e2e-5d38-a0e5-19e861e87d30"
FILE_UUID = "0e9b0552-544c-5c4e-83ac-90b44a40a47a"
SCOPE = uuid.UUID(SHEET_UUID)
LIBRARY = PROJECT / "symbols/rgb-badge-coupon.kicad_sym"
SOURCE = {
    "MAX17048G+T10": ("Analog Devices (Maxim Integrated)", "https://www.analog.com/media/en/technical-documentation/data-sheets/MAX17048-MAX17049.pdf", "TDFN_Maxim_T822-3_2x2mm_P0.5mm_EP0.7x1.38mm", list(map(str, range(1, 10)))),
    "ERJ2RKF2201X": ("Panasonic", "https://industrial.panasonic.com/cdbs/www-data/pdf/RDA0000/AOA0000C304.pdf", "R_Panasonic_ERJ2_0402", ["1", "2"]),
    "GRM155R71C104KA88D": ("Murata", "https://pim.murata.com/asset/pim4/ceramicCapacitorSMD/GRM155R71C104KA88-01A-EN_PDF_CERAMICCAPACITORSMD", "C_Murata_GRM15_0402", ["1", "2"]),
    "PWR_FLAG": ("", "", "", ["1"]),
}


def uid(name):
    return str(uuid.uuid5(SCOPE, name))


def q(value):
    return json.dumps(str(value), ensure_ascii=False)


def effects(hidden=False, justify=""):
    return f'(effects (font (size 1.27 1.27))' + (f' (justify {justify})' if justify else '') + (' (hide yes)' if hidden else '') + ')'


def property_line(key, value, x, y, hidden=False):
    return f'(property {q(key)} {q(value)} (at {x:.3f} {y:.3f} 0) {effects(hidden)})'


def controlled_symbol(mpn):
    text = LIBRARY.read_text(encoding="utf-8")
    matches = re.findall(r'^\t\(symbol "' + re.escape(mpn) + r'"\n.*?^\t\)', text, re.M | re.S)
    if len(matches) != 1:
        raise ValueError(f"Expected exactly one project-local symbol for {mpn}")
    return matches[0].replace(f'(symbol "{mpn}"', f'(symbol "rgb-badge-coupon:{mpn}"', 1)


def component(ref, mpn, value, x, y):
    manufacturer, datasheet, fp, pins = SOURCE[mpn]
    if ref.startswith("#"):
        fp = ""
    lines = [f'(symbol (lib_id "rgb-badge-coupon:{mpn}") (at {x:.3f} {y:.3f} 0) (unit 1)',
             f'(exclude_from_sim no) (in_bom {"no" if ref.startswith("#") else "yes"}) (on_board {"no" if ref.startswith("#") else "yes"}) (dnp no)',
             f'(uuid {q(uid(ref))})',
             property_line("Reference", ref, x, y - (15.24 if ref.startswith("U") else 5.08)),
             property_line("Value", value, x, y - (12.70 if ref.startswith("U") else 2.54)),
             property_line("Footprint", "rgb-badge-coupon:" + fp if fp else "", x, y, True),
             property_line("Datasheet", datasheet, x, y, True),
             property_line("Manufacturer", manufacturer, x, y, True),
             property_line("MPN", mpn if not ref.startswith("#") else "", x, y, True)]
    lines += [f'(pin {q(pin)} (uuid {q(uid(ref + "/" + pin))}))' for pin in pins]
    lines.append(f'(instances (project "rgb-badge-coupon" (path "/{ROOT_UUID}/{SHEET_UUID}" (reference {q(ref)}) (unit 1)))))')
    return lines


def wire_label(net, x, y, end_x, end_y, name):
    points = [(x, y)]
    if x != end_x and y != end_y:
        points.append((x, end_y))
    points.append((end_x, end_y))
    if len(set(points)) != len(points):
        raise ValueError("Zero length wire")
    lines = [f'(wire (pts (xy {a:.3f} {b:.3f}) (xy {c:.3f} {d:.3f})) (stroke (width 0) (type default)) (uuid {q(uid(name + "/wire/" + str(i)))}))'
             for i, ((a, b), (c, d)) in enumerate(zip(points, points[1:]))]
    angle, justify = (180, "right") if end_x < x else (0, "left")
    lines.append(f'(global_label {q(net)} (shape passive) (at {end_x:.3f} {end_y:.3f} {angle}) {effects(justify=justify)} (uuid {q(uid(name + "/label"))}) {property_line("Intersheetrefs", "${INTERSHEET_REFS}", end_x, end_y, True)})')
    return lines


def generate():
    lines = ['(kicad_sch', '(version 20260306)', '(generator "rgb_badge_gauge")', '(generator_version "1.0")',
             f'(uuid {q(FILE_UUID)})', '(paper "A4")',
             '(title_block (title "Coupon Rev A - staged switched fuel gauge") (rev "A-draft") (comment 1 "SPDX-License-Identifier: CERN-OHL-S-2.0") (comment 2 "Switched BAT source and actual DPDT switch are NOT captured"))',
             '(lib_symbols\n' + '\n'.join(controlled_symbol(mpn) for mpn in SOURCE) + '\n)',
             f'(text "MAX17048: switched gauge domain; no charger, pack, or mechanical switch here" (at 20.320 20.320 0) {effects(justify="left")} (uuid {q(uid("note/title"))}))',
             f'(text "PWR_FLAG is a temporary switched-BAT source assumption, NOT a physical connection." (at 20.320 30.480 0) {effects(justify="left")} (uuid {q(uid("note/boundary"))}))']
    gx, gy = 99.06, 83.82
    lines += component("U35", "MAX17048G+T10", "MAX17048G+T10", gx, gy)
    lines += wire_label("+BAT_GAUGE_SW", gx - 12.70, gy - 7.62, 63.50, gy - 7.62, "U35/VDD")
    lines += wire_label("+BAT_GAUGE_SW", gx - 12.70, gy - 5.08, 63.50, gy - 5.08, "U35/CELL")
    lines += wire_label("GND", gx - 12.70, gy, 63.50, gy, "U35/QSTRT")
    for index, (pin, x) in enumerate((("CTG", gx - 2.54), ("GND", gx), ("EP", gx + 2.54))):
        # Native rendering showed all three GND labels overlapping at one Y.
        lines += wire_label("GND", x, gy + 12.70, x + 17.78, gy + 25.40 + index * 7.62, "U35/" + pin)
    lines += wire_label("SYS_I2C_SDA", gx + 12.70, gy - 2.54, 134.62, gy - 2.54, "U35/SDA")
    lines += wire_label("SYS_I2C_SCL", gx + 12.70, gy, 134.62, gy, "U35/SCL")
    lines.append(f'(no_connect (at {gx + 12.70:.3f} {gy - 7.62:.3f}) (uuid {q(uid("U35/ALRT/nc"))}))')
    for ref, y, net in (("R79", 71.12, "SYS_I2C_SDA"), ("R80", 91.44, "SYS_I2C_SCL")):
        x = 198.12
        lines += component(ref, "ERJ2RKF2201X", "2.2k 1%", x, y)
        lines += wire_label("+3V3_APP", x - 5.08, y, x - 20.32, y, ref + "/1")
        lines += wire_label(net, x + 5.08, y, x + 20.32, y, ref + "/2")
    x, y = 198.12, 116.84
    lines += component("C39", "GRM155R71C104KA88D", "100n 16V X7R", x, y)
    lines += wire_label("+BAT_GAUGE_SW", x - 5.08, y, x - 20.32, y, "C39/1")
    lines += wire_label("GND", x + 5.08, y, x + 20.32, y, "C39/2")
    lines += component("#FLG06", "PWR_FLAG", "PWR_FLAG", 198.12, 144.78)
    lines += wire_label("+BAT_GAUGE_SW", 198.12, 144.78, 177.80, 144.78, "#FLG06/1")
    lines += ['(embedded_fonts no)', ')']
    return '\n'.join(lines) + '\n'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=False)
    (args.output / "gauge.kicad_sch").write_text(generate(), encoding="utf-8")


if __name__ == "__main__":
    main()
