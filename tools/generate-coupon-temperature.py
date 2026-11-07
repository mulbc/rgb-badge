#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Generate the root-linked Rev A charger temperature and TS boundary sheet."""

import argparse
import importlib.util
from pathlib import Path
import uuid

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / "hardware/coupon/rev-a"
ROOT_UUID = "207fb68e-2ddb-46bb-8712-eba2f8c5eef6"
SHEET_UUID = "d477891a-e380-5cf3-87c1-b3e0b1426b0a"
SCOPE = uuid.UUID(SHEET_UUID)
FILE_UUID = str(uuid.uuid5(SCOPE, "file"))
SPEC = importlib.util.spec_from_file_location("coupon_3v3_generator", ROOT / "tools/generate-coupon-3v3.py")
h = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(h)
h.SCOPE = SCOPE
h.FILE_UUID = FILE_UUID
h.PARTS = {
    "TH1": ("NCU15XH103F60RC", "10k NTC", "NTC_Murata_NCU15_0402", "Murata", "https://www.murata.com/en-us/products/productdetail?partno=NCU15XH103F60RC", 2),
    "U39": ("TMP390A2DRLR", "TMP390A2DRLR", "SOT563_TI_DRL0006A", "Texas Instruments", "https://www.ti.com/lit/ds/symlink/tmp390.pdf", 6),
    "U40": ("SN74AUP1G125DBVR", "SN74AUP1G125DBVR", "SOT23_TI_DBV0005A", "Texas Instruments", "https://www.ti.com/lit/ds/symlink/sn74aup1g125.pdf", 5),
    "R89": ("ERJ2RKF2151X", "2.15k 1%", "R_Panasonic_ERJ2_0402", "Panasonic", "https://industrial.panasonic.com/ww/products/pt/general-purpose-chip-resistors/models/ERJ2RKF2151X", 2),
    "R90": ("ERJ2RKF1402X", "14k 1%", "R_Panasonic_ERJ2_0402", "Panasonic", "https://industrial.panasonic.com/ww/products/pt/general-purpose-chip-resistors/models/ERJ2RKF1402X", 2),
    "R91": ("ERJ2RKF1002X", "10k 1%", "R_Panasonic_ERJ2_0402", "Panasonic", "https://industrial.panasonic.com/ww/products/pt/general-purpose-chip-resistors/models/ERJ2RKF1002X", 2),
    "C50": ("GRM155R71C104KA88D", "100n 16V X7R", "C_Murata_GRM15_0402", "Murata", "https://pim.murata.com/asset/pim4/ceramicCapacitorSMD/GRM155R71C104KA88-01A-EN_PDF_CERAMICCAPACITORSMD", 2),
    "C51": ("GRM155R71C104KA88D", "100n 16V X7R", "C_Murata_GRM15_0402", "Murata", "https://pim.murata.com/asset/pim4/ceramicCapacitorSMD/GRM155R71C104KA88-01A-EN_PDF_CERAMICCAPACITORSMD", 2),
    "TP34": ("TestPoint_Pad", "TestPoint_Pad", "TestPoint_Pad_D1.0mm", "", "", 1),
    "TP35": ("TestPoint_Pad", "TestPoint_Pad", "TestPoint_Pad_D1.0mm", "", "", 1),
}


def part(ref, x, y):
    old = f'(path "/{FILE_UUID}"'
    new = f'(path "/{ROOT_UUID}/{SHEET_UUID}"'
    lines = [line.replace(old, new) for line in h.component(ref, x, y)]
    if ref.startswith('TP'):
        lines = [line.replace('(in_bom yes)', '(in_bom no)').replace('(property "MPN" "TestPoint_Pad"', '(property "MPN" ""') for line in lines]
    return lines


def terminal(net, x, y, end_x, end_y, key):
    """Orthogonal wire from one pin to a clearly separated global label."""
    points = [(x, y)]
    if x != end_x and y != end_y:
        points.append((x, end_y))
    points.append((end_x, end_y))
    lines = [h.wire(*a, *b, f'{key}/{i}') for i, (a, b) in enumerate(zip(points, points[1:]))]
    angle, justify = (180, "right") if end_x < x else (0, "left")
    lines.append(f'(global_label {h.q(net)} (shape passive) (at {end_x:.3f} {end_y:.3f} {angle}) {h.effects(justify=justify)} (uuid {h.q(h.uid(key + "/label"))}) {h.prop("Intersheetrefs", "${INTERSHEET_REFS}", end_x, end_y, True)})')
    return lines


def generate():
    symbols = dict.fromkeys(row[0] for row in h.PARTS.values())
    lines = [
        '(kicad_sch', '(version 20260306)', '(generator "rgb_badge_temperature")',
        '(generator_version "1.0")', f'(uuid {h.q(FILE_UUID)})', '(paper "A3")',
        '(title_block (title "Coupon Rev A - battery-facing charge temperature") (rev "A-draft") (comment 1 "SPDX-License-Identifier: CERN-OHL-S-2.0") (comment 2 "BQ TS and E1 EN terminals pending connected charger capture"))',
        '(lib_symbols\n' + '\n'.join(h.cached_symbol(mpn) for mpn in symbols) + '\n)',
        f'(text "LP452845 Rev A: TH1 is BQ TS NTC; U39/U40 inhibit charger input at hot/cold faults." (at 20.320 20.320 0) {h.effects(justify="left")} (uuid {h.q(h.uid("note/title"))}))',
        f'(text "CHARGER_TS and CHARGER_GATE_EN are named boundaries; BQ24074 and E1 are not yet placed." (at 20.320 27.940 0) {h.effects(justify="left")} (uuid {h.q(h.uid("note/boundary"))}))',
    ]
    for ref, x, y in [
        ('TH1', 76.20, 91.44), ('U39', 152.40, 91.44),
        ('R89', 76.20, 129.54), ('R90', 76.20, 149.86),
        ('R91', 223.52, 81.28), ('C50', 223.52, 116.84),
        ('U40', 152.40, 190.50), ('C51', 223.52, 241.30),
        ('TP34', 76.20, 111.76), ('TP35', 223.52, 215.90),
    ]:
        lines.extend(part(ref, x, y))
    # Charger TS NTC directly to ground, with no fixed TS bypass.
    lines.extend(terminal('CHARGER_TS', 71.12, 91.44, 50.80, 91.44, 'TH1/1'))
    lines.extend(terminal('GND', 81.28, 91.44, 101.60, 91.44, 'TH1/2'))
    lines.extend(terminal('CHARGER_TS', 71.12, 111.76, 50.80, 111.76, 'TP34/1'))
    # TMP390 pin map: SETA 1, SETB 2, GND 3, OUTB 4, VDD 5, OUTA 6.
    lines.extend(terminal('TMP_HOT_SET', 139.70, 86.36, 114.30, 81.28, 'U39/1'))
    lines.extend(terminal('TMP_COLD_SET', 139.70, 88.90, 119.38, 101.60, 'U39/2'))
    lines.extend(terminal('GND', 152.40, 101.60, 172.72, 111.76, 'U39/3'))
    lines.extend(terminal('TEMP_OK', 165.10, 93.98, 187.96, 101.60, 'U39/4'))
    lines.extend(terminal('+3V3_USB', 152.40, 81.28, 177.80, 73.66, 'U39/5'))
    lines.extend(terminal('TEMP_OK', 165.10, 88.90, 187.96, 86.36, 'U39/6'))
    for ref, y, net in [('R89', 129.54, 'TMP_HOT_SET'), ('R90', 149.86, 'TMP_COLD_SET')]:
        lines.extend(terminal(net, 71.12, y, 48.26, y, ref + '/1'))
        lines.extend(terminal('GND', 81.28, y, 101.60, y, ref + '/2'))
    lines.extend(terminal('+3V3_USB', 218.44, 81.28, 198.12, 81.28, 'R91/1'))
    lines.extend(terminal('TEMP_OK', 228.60, 81.28, 248.92, 81.28, 'R91/2'))
    lines.extend(terminal('+3V3_USB', 218.44, 116.84, 198.12, 116.84, 'C50/1'))
    lines.extend(terminal('GND', 228.60, 116.84, 248.92, 116.84, 'C50/2'))
    # AUP pin map: active-low OE 1, A 2, GND 3, Y 4, VCC 5.
    lines.extend(terminal('TEMP_OK', 139.70, 187.96, 114.30, 182.88, 'U40/1'))
    lines.extend(terminal('GND', 139.70, 193.04, 119.38, 205.74, 'U40/2'))
    lines.extend(terminal('GND', 152.40, 200.66, 172.72, 215.90, 'U40/3'))
    lines.extend(terminal('CHARGER_GATE_EN', 165.10, 190.50, 200.66, 190.50, 'U40/4'))
    lines.extend(terminal('CHARGER_GATE_EN', 218.44, 215.90, 198.12, 215.90, 'TP35/1'))
    lines.extend(terminal('+3V3_USB', 152.40, 180.34, 177.80, 172.72, 'U40/5'))
    lines.extend(terminal('+3V3_USB', 218.44, 241.30, 198.12, 241.30, 'C51/1'))
    lines.extend(terminal('GND', 228.60, 241.30, 248.92, 241.30, 'C51/2'))
    return '\n'.join(lines + ['(embedded_fonts no)', ')']) + '\n'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=PROJECT / 'charger-temperature.kicad_sch')
    args = parser.parse_args()
    args.output.write_text(generate(), encoding='utf-8')


if __name__ == '__main__':
    main()
