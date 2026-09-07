#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Generate the initial matrix-only KiCad draft in a NEW output directory.

Canonical files remain editable KiCad sources. This one-time capture helper
never overwrites an existing project or treats regenerated text as validation.
"""

import argparse
import json
from pathlib import Path
import re
import runpy
import uuid


TOOLS = Path(__file__).resolve().parent
AUDIT = runpy.run_path(str(TOOLS / "check-led-libraries.py"))
ROOT_UUID = "207fb68e-2ddb-46bb-8712-eba2f8c5eef6"
NAMESPACE = uuid.UUID(ROOT_UUID)
PROJECT = "rgb-badge-coupon"


def uid(name):
    return str(uuid.uuid5(NAMESPACE, "matrix-rev-a/" + name))


def quote(value):
    return json.dumps(str(value), ensure_ascii=False)


def effects(size=1.27, justify="", hidden=False):
    return f'(effects (font (size {size} {size}))' + (f' (justify {justify})' if justify else '') + (' (hide yes)' if hidden else '') + ')'


def prop(name, value, x, y, *, hidden=False, size=1.27, justify=""):
    return f'(property {quote(name)} {quote(value)} (at {x:.2f} {y:.2f} 0) {effects(size, justify, hidden)})'


def note(text, x, y, name, size=1.27):
    return f'(text {quote(text)} (at {x:.2f} {y:.2f} 0) {effects(size, "left")} (uuid {quote(uid(name))}))'


def header(identifier, title, paper):
    return [
        '(kicad_sch', '(version 20260306)', '(generator "rgb_badge_matrix")',
        '(generator_version "1.0")', f'(uuid {quote(identifier)})', f'(paper {quote(paper)})',
        f'(title_block (title {quote(title)}) (rev "A - matrix draft") '
        '(comment 1 "SPDX-License-Identifier: CERN-OHL-S-2.0") '
        '(comment 2 "Matrix only: driver, row stages and power circuits pending"))',
    ]


def cached_symbol(mpn):
    source = AUDIT["SYMBOL_LIBRARY"].read_text()
    matches = re.findall(r'^\t\(symbol "' + re.escape(mpn) + r'"\n.*?^\t\)', source, re.M | re.S)
    if len(matches) != 1:
        raise ValueError(f"Cannot extract the controlled symbol {mpn}")
    return matches[0].replace(f'(symbol "{mpn}"', f'(symbol "rgb-badge-coupon:{mpn}"', 1)


def pixel(row, column, x, y, sheet_id):
    mpn = "EAST10105RGBA0" if column < 8 else "QBLP1515A-RGB2A"
    part = AUDIT["PARTS"][mpn]
    ref = f'D{row * 16 + column + 1}'
    items = [
        f'(symbol (lib_id "rgb-badge-coupon:{mpn}") (at {x:.2f} {y:.2f} 0) (unit 1)',
        '(exclude_from_sim no) (in_bom yes) (on_board yes) (dnp no)',
        f'(uuid {quote(uid(ref))})',
        prop('Reference', ref, x, y - 6.35),
        prop('Value', mpn, x, y + 6.35, size=1.016),
        prop('Footprint', part['footprint_property'], x, y, hidden=True),
        prop('Datasheet', part['datasheet'], x, y, hidden=True),
        prop('Manufacturer', part['manufacturer'], x, y, hidden=True),
        prop('MPN', mpn, x, y, hidden=True),
        prop('Matrix Row', row, x, y, hidden=True),
        prop('Matrix Column', column, x, y, hidden=True),
    ]
    for number in sorted(part['pins'].values()):
        items.append(f'(pin {quote(number)} (uuid {quote(uid(ref + "/pin/" + number))}))')
    items.append(
        f'(instances (project {quote(PROJECT)} (path "/{ROOT_UUID}/{sheet_id}" '
        f'(reference {quote(ref)}) (unit 1)))))'
    )
    # Explicit short wires attach each pin to a global row/colour-column net.
    # Y is inverted relative to the library symbol's Cartesian coordinates.
    terminals = [
        ('A', f'ROW_{row:02d}_A', x + 7.62, y, x + 17.78, 180),
        ('R_K', f'COL_{column:02d}_R', x - 7.62, y - 2.54, x - 17.78, 0),
        ('G_K', f'COL_{column:02d}_G', x - 7.62, y, x - 17.78, 0),
        ('B_K', f'COL_{column:02d}_B', x - 7.62, y + 2.54, x - 17.78, 0),
    ]
    for function, net, pin_x, pin_y, end_x, angle in terminals:
        items.append(
            f'(wire (pts (xy {pin_x:.2f} {pin_y:.2f}) (xy {end_x:.2f} {pin_y:.2f})) '
            f'(stroke (width 0) (type default)) (uuid {quote(uid(ref + "/wire/" + function))}))'
        )
        items.append(
            f'(global_label {quote(net)} (shape passive) (at {end_x:.2f} {pin_y:.2f} {angle}) '
            f'{effects(1.016, "right" if angle == 180 else "left")} '
            f'(uuid {quote(uid(ref + "/net/" + function))}) '
            f'{prop("Intersheetrefs", "${INTERSHEET_REFS}", end_x, pin_y, hidden=True)})'
        )
    return items


def generate():
    AUDIT['check_symbols']()
    files = {}
    root = header(ROOT_UUID, 'Coupon Rev A - matrix capture', 'A4')
    root.append('(lib_symbols)')
    root.extend([
        note('16 x 16 RGB matrix - initial circuit capture', 20.32, 20.32, 'root/title', 2.0),
        note('Four sheets use global nets: ROW_00_A..ROW_15_A and COL_00_R/G/B..COL_15_R/G/B.', 20.32, 30.48, 'root/nets'),
        note('These are 16 switched anodes and 48 cathode sinks. They are not logic control signals.', 20.32, 38.10, 'root/meaning'),
        note('TLC59581, row stages, controller, USB and power circuits are not captured yet.', 20.32, 45.72, 'root/pending'),
        note('No PCB placement exists. QBLP1515 rotation belongs to the later PCB, per ADR 0008.', 20.32, 157.48, 'root/pcb'),
    ])
    for index, (first_row, first_column) in enumerate(((0, 0), (0, 8), (8, 0), (8, 8))):
        stem = f'matrix-r{first_row:02d}-c{first_column:02d}'
        sheet_id = uid(stem + '/sheet')
        name = f'Rows {first_row:02d}-{first_row+7:02d}, columns {first_column:02d}-{first_column+7:02d}'
        mpn = 'EAST10105RGBA0' if first_column == 0 else 'QBLP1515A-RGB2A'
        x, y = 20.32 + (index % 2) * 132.08, 63.50 + (index // 2) * 45.72
        root.append('\n'.join([
            f'(sheet (at {x:.2f} {y:.2f}) (size 116.84 27.94)',
            '(exclude_from_sim no) (in_bom yes) (on_board yes) (dnp no)',
            '(stroke (width 0.1524) (type solid)) (fill (color 0 0 0 0))',
            f'(uuid {quote(sheet_id)})',
            prop('Sheetname', name, x, y-1.27, justify='left bottom'),
            prop('Sheetfile', stem + '.kicad_sch', x, y+29.21, justify='left top'),
            f'(instances (project {quote(PROJECT)} (path "/{ROOT_UUID}" (page "{index+2}")))))',
        ]))
        root.append(note(mpn + ' - 64 LEDs', x+5.08, y+12.70, stem+'/root-note'))
        sheet = header(uid(stem + '/file'), name + ' - ' + mpn, 'A2')
        sheet.append('(lib_symbols\n' + cached_symbol(mpn) + '\n)')
        sheet.extend([
            note(name + ' / ' + mpn, 20.32, 20.32, stem+'/title', 2.0),
            note('Global labels join matching row/colour-column nets across all four matrix sheets.', 20.32, 30.48, stem+'/nets'),
            note('Reference = D(16 x row + column + 1); row and column numbers are zero-based.', 20.32, 38.10, stem+'/refs'),
        ])
        for row in range(first_row, first_row+8):
            for column in range(first_column, first_column+8):
                sheet.extend(pixel(row, column, 40.64+(column-first_column)*71.12, 60.96+(row-first_row)*40.64, sheet_id))
        sheet.append('(embedded_fonts no)\n)')
        files[stem + '.kicad_sch'] = '\n'.join(sheet) + '\n'
    root.extend(['(sheet_instances (path "/" (page "1")))', '(embedded_fonts no)\n)'])
    files[PROJECT + '.kicad_sch'] = '\n'.join(root) + '\n'
    return files


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True, type=Path, help='New directory; existing paths are rejected')
    args = parser.parse_args()
    files = generate()
    args.output.mkdir(parents=True, exist_ok=False)
    for name, content in files.items():
        (args.output / name).write_text(content, encoding='utf-8')
    print(f'Generated matrix-only draft: 256 LEDs, four matrix sheets and root in {args.output}')


if __name__ == '__main__':
    main()
