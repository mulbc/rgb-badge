#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Generate the provisional charger core, with explicit unbuilt power boundaries."""

import argparse
import importlib.util
from pathlib import Path
import uuid

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / 'hardware/coupon/rev-a'
ROOT_UUID = '207fb68e-2ddb-46bb-8712-eba2f8c5eef6'
SHEET_UUID = '2f612542-2757-57f3-9ea0-8a9efdc1592b'
SCOPE = uuid.UUID(SHEET_UUID)
FILE_UUID = str(uuid.uuid5(SCOPE, 'file'))
spec = importlib.util.spec_from_file_location('coupon_3v3_generator', ROOT / 'tools/generate-coupon-3v3.py')
h = importlib.util.module_from_spec(spec)
spec.loader.exec_module(h)
h.SCOPE = SCOPE
h.FILE_UUID = FILE_UUID
h.PARTS = {
    'U41': ('BQ24074RGTR', 'BQ24074RGTR', 'VQFN_TI_RGT0016C_3x3mm_P0.5mm_EP1.68mm', 'Texas Instruments', 'https://www.ti.com/lit/ds/symlink/bq24074.pdf', 17),
    'R92': ('ERA2AEB2491X', '2.49k 0.1%', 'R_Panasonic_ERA2_0402', 'Panasonic', 'https://industrial.panasonic.com/ww/products/pt/high-precision-chip-resistors/models/ERA2AEB2491X', 2),
    'R93': ('ERA2AEB3651X', '3.65k 0.1%', 'R_Panasonic_ERA2_0402', 'Panasonic', 'https://industrial.panasonic.com/ww/products/pt/high-precision-chip-resistors/models/ERA2AEB3651X', 2),
    'C52': ('GRM155C71A105KE11D', '1u 10V X7S', 'C_Murata_GRM15_0402', 'Murata', 'https://pim.murata.com/en-global/pim/details/?partNum=GRM155C71A105KE11D', 2),
    'C53': ('GRM188R60J106ME47D', '10u 6.3V X5R', 'C_Murata_GRM18_0603', 'Murata', 'https://pim.murata.com/en-global/pim/details/?partNum=GRM188R60J106ME47D', 2),
    'C54': ('GRM188R60J106ME47D', '10u 6.3V X5R', 'C_Murata_GRM18_0603', 'Murata', 'https://pim.murata.com/en-global/pim/details/?partNum=GRM188R60J106ME47D', 2),
}


def part(ref, x, y):
    return [line.replace(f'(path "/{FILE_UUID}"', f'(path "/{ROOT_UUID}/{SHEET_UUID}"')
            for line in h.component(ref, x, y)]


def terminal(net, x, y, end_x, end_y, key):
    points = [(x, y)]
    if x != end_x and y != end_y:
        bend_x = x + (10.16 if end_x > x else -10.16)
        points.extend([(bend_x, y), (bend_x, end_y)])
    points.append((end_x, end_y))
    lines = [h.wire(*a, *b, f'{key}/{i}') for i, (a, b) in enumerate(zip(points, points[1:]))]
    angle, justify = (180, 'right') if end_x < x else (0, 'left')
    lines.append(f'(global_label {h.q(net)} (shape passive) (at {end_x:.3f} {end_y:.3f} {angle}) {h.effects(justify=justify)} (uuid {h.q(h.uid(key + "/label"))}) {h.prop("Intersheetrefs", "${INTERSHEET_REFS}", end_x, end_y, True)})')
    return lines


def nc(x, y, key):
    return f'(no_connect (at {x:.3f} {y:.3f}) (uuid {h.q(h.uid(key))}))'


def source_boundary(ref, x, y, net):
    """Mark an unresolved external supply only for draft ERC, never as a part."""
    lines = [f'(symbol (lib_id "rgb-badge-coupon:PWR_FLAG") (at {x:.3f} {y:.3f} 0) (unit 1)',
             '(exclude_from_sim no) (in_bom no) (on_board no) (dnp no)',
             f'(uuid {h.q(h.uid(ref))})',
             h.prop('Reference', ref, x, y - 5.08),
             h.prop('Value', 'PWR_FLAG', x, y - 2.54),
             h.prop('Footprint', '', x, y, True), h.prop('Datasheet', '', x, y, True),
             h.prop('Manufacturer', '', x, y, True), h.prop('MPN', '', x, y, True),
             f'(pin "1" (uuid {h.q(h.uid(ref + "/1"))}))',
             f'(instances (project "rgb-badge-coupon" (path "/{ROOT_UUID}/{SHEET_UUID}" (reference "{ref}") (unit 1)))))']
    lines.extend(terminal(net, x, y, x + 25.40, y, ref + '/net'))
    return lines


def generate():
    symbols = dict.fromkeys(row[0] for row in h.PARTS.values())
    lines = [
        '(kicad_sch', '(version 20260306)', '(generator "rgb_badge_charger_core")', '(generator_version "1.0")',
        f'(uuid {h.q(FILE_UUID)})', '(paper "A3")',
        '(title_block (title "Coupon Rev A - provisional BQ24074 charger core") (rev "A-draft") (comment 1 "SPDX-License-Identifier: CERN-OHL-S-2.0") (comment 2 "IN and BAT are unbuilt boundary nets; EN2 temporarily grounded"))',
        '(lib_symbols\n' + '\n'.join(h.cached_symbol(mpn) for mpn in symbols) + '\n' + h.cached_symbol('PWR_FLAG') + '\n)',
        f'(text "CHARGER_TS physically joins TH1 via global net. IN and BAT await E1 and pack connector." (at 20.320 20.320 0) {h.effects(justify="left")} (uuid {h.q(h.uid("note/1"))}))',
        f'(text "EN2=0, EN1=0 gives 100 mA fallback; R93 ILIM setting is inactive until EN2 drive is captured." (at 20.320 27.940 0) {h.effects(justify="left")} (uuid {h.q(h.uid("note/2"))}))',
        f'(text "ITERM open selects 10% default termination; TMR open selects live 30 min/5 h safety timers." (at 20.320 35.560 0) {h.effects(justify="left")} (uuid {h.q(h.uid("note/3"))}))',
    ]
    for ref, x, y in [('U41', 152.40, 116.84), ('R92', 254.00, 175.26), ('R93', 76.20, 175.26),
                      ('C52', 76.20, 76.20), ('C53', 254.00, 76.20), ('C54', 254.00, 96.52)]:
        lines.extend(part(ref, x, y))
    left = 138.43
    right = 166.37
    for pin, net, y, ex, ey in [
        ('13', 'CHARGER_IN_DRAFT', 106.68, 101.60, 106.68),
        ('1', 'CHARGER_TS', 111.76, 101.60, 111.76),
        ('4', 'GND', 114.30, 101.60, 114.30),
        ('5', 'GND', 116.84, 101.60, 116.84),
        ('6', 'GND', 119.38, 101.60, 119.38),
        ('12', 'CHARGER_ILIM', 121.92, 101.60, 121.92),
    ]:
        lines.extend(terminal(net, left, y, ex, ey, 'U41/' + pin))
    for pin, net, y, ex, ey in [
        ('2', '+BAT_PROTECTED_DRAFT', 106.68, 203.20, 106.68),
        ('3', '+BAT_PROTECTED_DRAFT', 109.22, 203.20, 109.22),
        ('10', '+SYS_APP_IN_DRAFT', 111.76, 203.20, 111.76),
        ('11', '+SYS_APP_IN_DRAFT', 114.30, 203.20, 114.30),
        ('16', 'CHARGER_ISET', 127.00, 203.20, 127.00),
    ]:
        lines.extend(terminal(net, right, y, ex, ey, 'U41/' + pin))
    for pin, x in [('8', 149.86), ('17', 154.94)]:
        lines.extend(terminal('GND', x, 132.08, x + (-20.32 if pin == '8' else 20.32), 154.94, 'U41/' + pin))
    for pin, x, y in [('7', right, 119.38), ('9', right, 121.92), ('14', left, 124.46), ('15', left, 127.00)]:
        lines.append(nc(x, y, 'U41/' + pin + '/nc'))
    for ref, x, y, net in [
        ('R92', 254.00, 175.26, 'CHARGER_ISET'), ('R93', 76.20, 175.26, 'CHARGER_ILIM'),
        ('C52', 76.20, 76.20, 'CHARGER_IN_DRAFT'), ('C53', 254.00, 76.20, '+BAT_PROTECTED_DRAFT'),
        ('C54', 254.00, 96.52, '+SYS_APP_IN_DRAFT'),
    ]:
        lines.extend(terminal(net, x - 5.08, y, x - 25.40, y, ref + '/1'))
        lines.extend(terminal('GND', x + 5.08, y, x + 25.40, y, ref + '/2'))
    lines.extend(source_boundary('#FLG08', 76.20, 208.28, 'CHARGER_IN_DRAFT'))
    lines.extend(source_boundary('#FLG09', 254.00, 208.28, '+BAT_PROTECTED_DRAFT'))
    return '\n'.join(lines + ['(embedded_fonts no)', ')']) + '\n'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=PROJECT / 'charger-core.kicad_sch')
    args = parser.parse_args()
    args.output.write_text(generate(), encoding='utf-8')


if __name__ == '__main__':
    main()
