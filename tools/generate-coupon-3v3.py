#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Generate the unlinked TPS631000 circuit candidate for source review.

Do not link it into the project while the existing +3V3_APP draft PWR_FLAG
still declares a source and the protected SYS / ON switch are unresolved.
"""

import argparse
import json
from pathlib import Path
import re
import uuid


PROJECT = Path(__file__).resolve().parents[1] / "hardware/coupon/rev-a"
SCOPE = uuid.UUID("a8893768-879f-5700-9390-326289fdc91a")
FILE_UUID = str(uuid.uuid5(SCOPE, "file"))
LIBRARY = PROJECT / "symbols/rgb-badge-coupon.kicad_sym"
PARTS = {
    "U36": ("TPS631000DRLR", "TPS631000DRLR", "SOT5X3_TI_DRL0008A", "Texas Instruments", "https://www.ti.com/lit/ds/symlink/tps631000.pdf", 8),
    "L1": ("DFE252012P-1R0M=P2", "1u 20%", "L_Murata_DFE252012P", "Murata", "https://www.murata.com/~/media/webrenewal/products/inductor/chip/tokoproducts/wirewoundmetalalloychiptype/m_dfe252012p.ashx", 2),
    "C40": ("GRM187R61A226ME15", "22u 10V X5R", "C_Murata_GRM18_0603", "Murata", "https://pim.murata.com/en-global/pim/details/?partNum=GRM187R61A226ME15", 2),
    "C41": ("GRM187R61A226ME15", "22u 10V X5R", "C_Murata_GRM18_0603", "Murata", "https://pim.murata.com/en-global/pim/details/?partNum=GRM187R61A226ME15", 2),
    "C42": ("GRM219R60J476ME44", "47u 6.3V X5R", "C_Murata_GRM21_0805", "Murata", "https://pim.murata.com/en-global/pim/details/?partNum=GRM219R60J476ME44", 2),
    "C43": ("GRM219R60J476ME44", "47u 6.3V X5R", "C_Murata_GRM21_0805", "Murata", "https://pim.murata.com/en-global/pim/details/?partNum=GRM219R60J476ME44", 2),
    "R81": ("ERJ2RKF5113X", "511k 1%", "R_Panasonic_ERJ2_0402", "Panasonic", "https://industrial.panasonic.com/ww/products/pt/general-purpose-chip-resistors/models/ERJ2RKF5113X", 2),
    "R82": ("ERJ2RKF9102X", "91k 1%", "R_Panasonic_ERJ2_0402", "Panasonic", "https://industrial.panasonic.com/ww/products/pt/general-purpose-chip-resistors/models/ERJ2RKF9102X", 2),
    "R83": ("ERJ2RKF1003X", "100k 1%", "R_Panasonic_ERJ2_0402", "Panasonic", "https://industrial.panasonic.com/ww/products/pt/general-purpose-chip-resistors/models/ERJ2RKF1003X", 2),
}


def uid(name):
    return str(uuid.uuid5(SCOPE, name))


def q(value):
    return json.dumps(str(value), ensure_ascii=False)


def effects(hidden=False, justify=""):
    return '(effects (font (size 1.27 1.27))' + (f' (justify {justify})' if justify else '') + (' (hide yes)' if hidden else '') + ')'


def prop(key, value, x, y, hidden=False):
    return f'(property {q(key)} {q(value)} (at {x:.3f} {y:.3f} 0) {effects(hidden)})'


def cached_symbol(mpn):
    matches = re.findall(r'^[\t]*\(symbol "' + re.escape(mpn) + r'"[^\n]*\n.*?^[\t]*\)', LIBRARY.read_text(), re.M | re.S)
    if len(matches) != 1:
        raise ValueError(f"Expected exactly one local symbol: {mpn}")
    cached = matches[0]
    # Multi-line IC symbols have a closing line for both unit and parent.
    if cached.count('(') - cached.count(')') == 1:
        cached += '\n\t)'
    if cached.count('(') != cached.count(')'):
        raise ValueError(f"Malformed cached symbol: {mpn}")
    return cached.replace(f'(symbol "{mpn}"', f'(symbol "rgb-badge-coupon:{mpn}"', 1)


def component(ref, x, y):
    mpn, value, footprint, manufacturer, datasheet, pin_count = PARTS[ref]
    lines = [f'(symbol (lib_id "rgb-badge-coupon:{mpn}") (at {x:.3f} {y:.3f} 0) (unit 1)',
             '(exclude_from_sim no) (in_bom yes) (on_board yes) (dnp no)',
             f'(uuid {q(uid(ref))})',
             prop('Reference', ref, x, y - (11.43 if ref.startswith('U') else 6.35)),
             prop('Value', value, x, y - (8.89 if ref.startswith('U') else 3.81)),
             prop('Footprint', 'rgb-badge-coupon:' + footprint, x, y, True),
             prop('Datasheet', datasheet, x, y, True),
             prop('Manufacturer', manufacturer, x, y, True),
             prop('MPN', mpn, x, y, True)]
    lines.extend(f'(pin "{n}" (uuid {q(uid(ref + "/" + str(n)))}))' for n in range(1, pin_count + 1))
    lines.append(f'(instances (project "rgb-badge-coupon" (path "/{FILE_UUID}" (reference "{ref}") (unit 1)))))')
    return lines


def wire(x1, y1, x2, y2, name):
    if (x1 == x2 and y1 == y2) or (x1 != x2 and y1 != y2):
        raise ValueError('Wire must be a nonzero straight segment')
    return f'(wire (pts (xy {x1:.3f} {y1:.3f}) (xy {x2:.3f} {y2:.3f})) (stroke (width 0) (type default)) (uuid {q(uid(name))}))'


def labelled(net, x1, y1, x2, y2, name):
    angle, justify = (180, 'right') if x2 < x1 else (0, 'left')
    return [wire(x1, y1, x2, y2, name + '/wire'),
            f'(global_label {q(net)} (shape passive) (at {x2:.3f} {y2:.3f} {angle}) {effects(justify=justify)} (uuid {q(uid(name + "/label"))}) {prop("Intersheetrefs", "${INTERSHEET_REFS}", x2, y2, True)})']


def generate():
    mpns = dict.fromkeys(p[0] for p in PARTS.values())
    lines = ['(kicad_sch', '(version 20260306)', '(generator "rgb_badge_3v3_candidate")', '(generator_version "1.0")',
             f'(uuid {q(FILE_UUID)})', '(paper "A3")',
             '(title_block (title "Coupon Rev A - unlinked 3V3 converter candidate") (rev "A-draft") (comment 1 "SPDX-License-Identifier: CERN-OHL-S-2.0") (comment 2 "DO NOT LINK: SYS source and physical ON control pending"))',
             '(lib_symbols\n' + '\n'.join(cached_symbol(mpn) for mpn in mpns) + '\n)',
             f'(text "Unlinked candidate: protected SYS and switch ON drive are NOT captured." (at 20.320 20.320 0) {effects(justify="left")} (uuid {q(uid("note/source"))}))',
             f'(text "LX1/LX2 wires are local switching nodes. No PCB, thermal or load validation." (at 20.320 27.940 0) {effects(justify="left")} (uuid {q(uid("note/lx"))}))']
    for ref, x, y in [('U36',147.32,96.52),('L1',147.32,137.16),('C40',50.80,66.04),('C41',50.80,83.82),
                      ('C42',254.00,66.04),('C43',254.00,83.82),('R81',254.00,116.84),
                      ('R82',254.00,137.16),('R83',50.80,116.84)]:
        lines.extend(component(ref, x, y))
    for pin, net, y, end in [('VIN','+SYS_APP_IN_DRAFT',91.44,99.06),('EN','APP_ON_SW_DRAFT',99.06,99.06),
                             ('MODE','GND',101.60,99.06)]:
        lines.extend(labelled(net,134.62,y,end,y,'U36/'+pin))
    lines.extend(labelled('+3V3_APP',160.02,91.44,193.04,91.44,'U36/VOUT'))
    lines.extend(labelled('APP_3V3_FB',160.02,101.60,193.04,101.60,'U36/FB'))
    lines.extend(labelled('GND',147.32,106.68,180.34,106.68,'U36/GND'))
    for ref,x,y,input_net,output_net in [
        ('C40',50.80,66.04,'+SYS_APP_IN_DRAFT','GND'),('C41',50.80,83.82,'+SYS_APP_IN_DRAFT','GND'),
        ('C42',254.00,66.04,'+3V3_APP','GND'),('C43',254.00,83.82,'+3V3_APP','GND'),
        ('R81',254.00,116.84,'+3V3_APP','APP_3V3_FB'),('R82',254.00,137.16,'APP_3V3_FB','GND'),
        ('R83',50.80,116.84,'APP_ON_SW_DRAFT','GND')]:
        lines.extend(labelled(input_net,x-5.08,y,x-20.32,y,ref+'/1'))
        lines.extend(labelled(output_net,x+5.08,y,x+20.32,y,ref+'/2'))
    for side, a, b, turn in [('LX1',134.62,142.24,127.00),('LX2',160.02,152.40,167.64)]:
        lines.append(wire(a,96.52,turn,96.52,side+'/top'))
        lines.append(wire(turn,96.52,turn,137.16,side+'/vertical'))
        lines.append(wire(turn,137.16,b,137.16,side+'/bottom'))
    lines += ['(embedded_fonts no)', ')']
    return '\n'.join(lines) + '\n'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=False)
    (args.output / '3v3-converter.kicad_sch').write_text(generate(), encoding='utf-8')


if __name__ == '__main__':
    main()
