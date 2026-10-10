#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Generate the provisional root-linked switch and 3V3 application sheets.

The charger OUT now provides the provisional SYS source. The gauge pole stays
unwired until bus isolation and contact-order behavior have been reviewed.
"""

import argparse
import json
from pathlib import Path
import re
import uuid


PROJECT = Path(__file__).resolve().parents[1] / 'hardware/coupon/rev-a'
ROOT_UUID = '207fb68e-2ddb-46bb-8712-eba2f8c5eef6'
SW_SHEET_UUID = '6dbe5759-c45c-55eb-b787-20e70dd36eac'
APP_SHEET_UUID = 'bdc31b17-9749-5bfe-a9df-7b52b4cfb3e7'
SW_FILE_UUID = '0bb1413f-d6b1-5e08-b8ec-215d25d0e8b3'
APP_FILE_UUID = '4a0e948e-547b-5b41-a9fd-fd10c1f1b35e'
SCOPE = uuid.UUID(SW_FILE_UUID)
LIBRARY = PROJECT / 'symbols/rgb-badge-coupon.kicad_sym'


def uid(name):
    return str(uuid.uuid5(SCOPE, name))


def q(value):
    return json.dumps(str(value), ensure_ascii=False)


def effects(hidden=False, justify=''):
    return '(effects (font (size 1.27 1.27))' + (f' (justify {justify})' if justify else '') + (' (hide yes)' if hidden else '') + ')'


def prop(name, value, x, y, hidden=False):
    return f'(property {q(name)} {q(value)} (at {x:.3f} {y:.3f} 0) {effects(hidden)})'


def cached_symbol(mpn):
    match = re.findall(r'^[\t]*\(symbol "' + re.escape(mpn) + r'"(?:\n| ).*?^[\t]*\)',
                       LIBRARY.read_text(), re.M | re.S)
    if len(match) != 1:
        raise ValueError(f'Expected one local symbol: {mpn}')
    cached = match[0]
    if cached.count('(') - cached.count(')') == 1:
        cached += '\n)'
    if cached.count('(') != cached.count(')'):
        raise ValueError(f'Malformed local symbol: {mpn}')
    return cached.replace(f'(symbol "{mpn}"', f'(symbol "rgb-badge-coupon:{mpn}"', 1)


def wire_label(net, x1, y1, x2, y2, name):
    angle, justify = (180, 'right') if x2 < x1 else (0, 'left')
    return [f'(wire (pts (xy {x1:.3f} {y1:.3f}) (xy {x2:.3f} {y2:.3f})) (stroke (width 0) (type default)) (uuid {q(uid(name + "/wire"))}))',
            f'(global_label {q(net)} (shape passive) (at {x2:.3f} {y2:.3f} {angle}) {effects(justify=justify)} (uuid {q(uid(name + "/label"))}) {prop("Intersheetrefs", "${INTERSHEET_REFS}", x2, y2, True)})']


def component(ref, mpn, x, y, pins, value, footprint, manufacturer='', datasheet=''):
    virtual = ref.startswith('#')
    lines = [f'(symbol (lib_id "rgb-badge-coupon:{mpn}") (at {x:.3f} {y:.3f} 0) (unit 1)',
             f'(exclude_from_sim no) (in_bom {"no" if virtual else "yes"}) (on_board {"no" if virtual else "yes"}) (dnp no)',
             f'(uuid {q(uid(ref))})',
             prop('Reference', ref, x, y - (17.78 if not virtual else 5.08)),
             prop('Value', value, x, y - (15.24 if not virtual else 2.54)),
             prop('Footprint', footprint, x, y, True),
             prop('Datasheet', datasheet, x, y, True),
             prop('Manufacturer', manufacturer, x, y, True),
             prop('MPN', '' if virtual else mpn, x, y, True)]
    lines.extend(f'(pin {q(n)} (uuid {q(uid(ref + "/" + n))}))' for n in pins)
    lines.append(f'(instances (project "rgb-badge-coupon" (path "/{ROOT_UUID}/{SW_SHEET_UUID}" (reference {q(ref)}) (unit 1)))))')
    return lines


def generate_control():
    lines = ['(kicad_sch', '(version 20260306)', '(generator "rgb_badge_app_power")', '(generator_version "1.0")',
             f'(uuid {q(SW_FILE_UUID)})', '(paper "A4")',
             '(title_block (title "Coupon Rev A - provisional application control") (rev "A-draft") (comment 1 "SPDX-License-Identifier: CERN-OHL-S-2.0") (comment 2 "Charger OUT source staged; no fabrication"))',
             '(lib_symbols\n' + cached_symbol('JS202011JCQN') + '\n)',
             f'(text "Pole 1 drives TPS631000 EN with a separate 100k OFF pull-down on the converter page." (at 20.320 20.320 0) {effects(justify="left")} (uuid {q(uid("note/control"))}))',
             f'(text "Pole 2 is reserved for the gauge; leave it open until I2C isolation and contact order are reviewed." (at 20.320 27.940 0) {effects(justify="left")} (uuid {q(uid("note/gauge"))}))',
             f'(text "JCQN mechanical/throw-direction review remains open. Do not populate a board from this draft." (at 20.320 35.560 0) {effects(justify="left")} (uuid {q(uid("note/fit"))}))']
    lines += component('SW2', 'JS202011JCQN', 120.65, 86.36, [str(i) for i in range(1, 7)],
                       'JS202011JCQN', 'rgb-badge-coupon:SW_CK_JS202011JCQN',
                       'C&K / Littelfuse', 'https://www.ckswitches.com/media/1422/js.pdf')
    lines += wire_label('+SYS_APP_IN_DRAFT', 110.49, 78.74, 77.47, 78.74, 'SW2/2')
    lines += wire_label('APP_ON_SW_DRAFT', 130.81, 81.28, 163.83, 81.28, 'SW2/3')
    for pin, x, y in [(1,130.81,76.20),(4,130.81,91.44),(5,110.49,93.98),(6,130.81,96.52)]:
        lines.append(f'(no_connect (at {x:.3f} {y:.3f}) (uuid {q(uid("SW2/" + str(pin) + "/nc"))}))')
    lines += ['(embedded_fonts no)', ')']
    return '\n'.join(lines) + '\n'


def generate_converter():
    from runpy import run_path
    source = run_path(str(Path(__file__).with_name('generate-coupon-3v3.py')))
    text = source['generate']()
    text = text.replace(source['FILE_UUID'], APP_FILE_UUID)
    text = text.replace(f'path "/{APP_FILE_UUID}"', f'path "/{ROOT_UUID}/{APP_SHEET_UUID}"')
    text = text.replace('unlinked 3V3 converter candidate', 'provisional 3V3 application converter')
    text = text.replace('DO NOT LINK: SYS source and physical ON control pending', 'SYS source draft; physical switch control linked; no fabrication')
    text = text.replace('Unlinked candidate: protected SYS and switch ON drive are NOT captured.',
                        'SYS is a draft source boundary. SW2 control contact drives EN; gauge pole remains open.')
    return text


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=False)
    (args.output / 'app-control.kicad_sch').write_text(generate_control(), encoding='utf-8')
    (args.output / '3v3-converter.kicad_sch').write_text(generate_converter(), encoding='utf-8')


if __name__ == '__main__':
    main()
