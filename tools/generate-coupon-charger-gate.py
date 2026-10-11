#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Generate provisional E1 charge-admission switch and independent EN sinks."""

import argparse
import importlib.util
from pathlib import Path
import uuid

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / 'hardware/coupon/rev-a'
ROOT_UUID = '207fb68e-2ddb-46bb-8712-eba2f8c5eef6'
SHEET_UUID = 'd8d1f8f8-44be-5ad4-a193-9dc90529f25a'
SCOPE = uuid.UUID(SHEET_UUID)
FILE_UUID = str(uuid.uuid5(SCOPE, 'file'))
spec = importlib.util.spec_from_file_location('coupon_3v3_generator', ROOT / 'tools/generate-coupon-3v3.py')
h = importlib.util.module_from_spec(spec)
spec.loader.exec_module(h)
h.SCOPE, h.FILE_UUID = SCOPE, FILE_UUID
h.PARTS = {
    'U44': ('TPS259474ARPWR','TPS259474ARPWR','VQFN_TI_RPW0010A_2x2mm_HotRod','Texas Instruments','https://www.ti.com/lit/ds/symlink/tps25947.pdf',10),
    'U42': ('SN74AUP1G125DBVR','SN74AUP1G125DBVR','SOT23_TI_DBV0005A','Texas Instruments','https://www.ti.com/lit/ds/symlink/sn74aup1g125.pdf',5),
    'U43': ('SN74AUP1G125DBVR','SN74AUP1G125DBVR','SOT23_TI_DBV0005A','Texas Instruments','https://www.ti.com/lit/ds/symlink/sn74aup1g125.pdf',5),
    'R94': ('ERJ2RKF2203X','220k 1%','R_Panasonic_ERJ2_0402','Panasonic','https://industrial.panasonic.com/ww/products/pt/general-purpose-chip-resistors/models/ERJ2RKF2203X',2),
    'R95': ('ERJ2RKF2703X','270k 1%','R_Panasonic_ERJ2_0402','Panasonic','https://industrial.panasonic.com/ww/products/pt/general-purpose-chip-resistors/models/ERJ2RKF2703X',2),
    'R96': ('ERJ2RKF3321X','3.32k 1%','R_Panasonic_ERJ2_0402','Panasonic','https://industrial.panasonic.com/ww/products/pt/general-purpose-chip-resistors/models/ERJ2RKF3321X',2),
    'C55': ('GRM155R71C104KA88D','100n 16V X7R','C_Murata_GRM15_0402','Murata','https://pim.murata.com/asset/pim4/ceramicCapacitorSMD/GRM155R71C104KA88-01A-EN_PDF_CERAMICCAPACITORSMD',2),
    'C56': ('GRM187R61A226ME15','22u 10V X5R','C_Murata_GRM18_0603','Murata','https://pim.murata.com/en-global/pim/details/?partNum=GRM187R61A226ME15',2),
    'C57': ('GRM1555C1H222GA01D','2.2n 50V C0G','C_Murata_GRM15_0402','Murata','https://www.murata.com/en-us/products/productdetail?partno=GRM1555C1H222GA01%23',2),
    'C58': ('GRM155R71C104KA88D','100n 16V X7R','C_Murata_GRM15_0402','Murata','https://pim.murata.com/asset/pim4/ceramicCapacitorSMD/GRM155R71C104KA88-01A-EN_PDF_CERAMICCAPACITORSMD',2),
    'C59': ('GRM155R71C104KA88D','100n 16V X7R','C_Murata_GRM15_0402','Murata','https://pim.murata.com/asset/pim4/ceramicCapacitorSMD/GRM155R71C104KA88-01A-EN_PDF_CERAMICCAPACITORSMD',2),
}


def part(ref,x,y):
    return [line.replace(f'(path "/{FILE_UUID}"', f'(path "/{ROOT_UUID}/{SHEET_UUID}"') for line in h.component(ref,x,y)]


def terminal(net,x,y,end_x,end_y,key):
    points=[(x,y)]
    if x != end_x and y != end_y:
        points.extend([(x,end_y)])
    points.append((end_x,end_y))
    lines=[h.wire(*a,*b,f'{key}/{i}') for i,(a,b) in enumerate(zip(points,points[1:]))]
    angle,justify=(180,'right') if end_x<x else (0,'left')
    lines.append(f'(global_label {h.q(net)} (shape passive) (at {end_x:.3f} {end_y:.3f} {angle}) {h.effects(justify=justify)} (uuid {h.q(h.uid(key + "/label"))}) {h.prop("Intersheetrefs", "${INTERSHEET_REFS}", end_x, end_y, True)})')
    return lines


def nc(x,y,key):
    return f'(no_connect (at {x:.3f} {y:.3f}) (uuid {h.q(h.uid(key))}))'


def source_flag(x,y):
    ref='#FLG08'
    lines=[f'(symbol (lib_id "rgb-badge-coupon:PWR_FLAG") (at {x:.3f} {y:.3f} 0) (unit 1)',
           '(exclude_from_sim no) (in_bom no) (on_board no) (dnp no)',
           f'(uuid {h.q(h.uid(ref))})',h.prop('Reference',ref,x,y-5.08),
           h.prop('Value','PWR_FLAG',x,y-2.54),h.prop('Footprint','',x,y,True),
           h.prop('Datasheet','',x,y,True),h.prop('Manufacturer','',x,y,True),h.prop('MPN','',x,y,True),
           f'(pin "1" (uuid {h.q(h.uid(ref + "/1"))}))',
           f'(instances (project "rgb-badge-coupon" (path "/{ROOT_UUID}/{SHEET_UUID}" (reference "{ref}") (unit 1)))))']
    lines.extend(terminal('USB_PROTECTED_DRAFT',x,y,x+20.32,y,ref+'/net'))
    return lines


def generate():
    symbols=dict.fromkeys(row[0] for row in h.PARTS.values())
    lines=['(kicad_sch','(version 20260306)','(generator "rgb_badge_charger_gate")','(generator_version "1.0")',
           f'(uuid {h.q(FILE_UUID)})','(paper "A3")',
           '(title_block (title "Coupon Rev A - provisional E1 charger gate") (rev "A-draft") (comment 1 "SPDX-License-Identifier: CERN-OHL-S-2.0") (comment 2 "E0 upstream source still absent; gate operating behavior unqualified"))',
           '(lib_symbols\n'+'\n'.join(h.cached_symbol(mpn) for mpn in symbols)+'\n'+h.cached_symbol('PWR_FLAG')+'\n)',
           f'(text "E1 IN is a draft protected-USB boundary. E1 OUT joins BQ IN and EN2 clamp." (at 20.320 20.320 0) {h.effects(justify="left")} (uuid {h.q(h.uid("note/1"))}))',
           f'(text "Three AUP sinks: source request, supervisor RESET, and temperature on the other sheet." (at 20.320 27.940 0) {h.effects(justify="left")} (uuid {h.q(h.uid("note/2"))}))',
           f'(text "Static divider screen assumes 1.6uA leakage; no startup, inrush or E0 fault qualification." (at 20.320 35.560 0) {h.effects(justify="left")} (uuid {h.q(h.uid("note/3"))}))']
    for ref,x,y in [('U44',170.18,106.68),('U42',91.44,182.88),('U43',223.52,182.88),
                    ('R94',76.20,71.12),('R95',76.20,91.44),('R96',254.00,132.08),
                    ('C55',76.20,111.76),('C56',254.00,71.12),('C57',254.00,91.44),
                    ('C58',76.20,223.52),('C59',254.00,223.52)]:
        lines.extend(part(ref,x,y))
    for pin,net,x,y,ex,ey in [
        ('5','USB_PROTECTED_DRAFT',154.94,96.52,124.46,96.52),
        ('1','CHARGER_GATE_EN',154.94,101.60,124.46,101.60),
        ('2','GND',154.94,106.68,124.46,106.68),
        ('6','CHARGER_IN_DRAFT',185.42,96.52,215.90,96.52),
        ('7','E1_DVDT',185.42,106.68,215.90,106.68),
        ('9','E1_ILM',185.42,111.76,215.90,111.76),
        ('8','GND',170.18,124.46,170.18,144.78)]:
        lines.extend(terminal(net,x,y,ex,ey,'U44/'+pin))
    for pin,x,y in [('3',185.42,101.60),('4',154.94,111.76),('10',185.42,116.84)]:
        lines.append(nc(x,y,'U44/'+pin+'/nc'))
    for ref,x,y,oe in [('U42',91.44,182.88,'USB_CHARGE_REQ'),('U43',223.52,182.88,'USB_RAW_LOGIC_READY')]:
        lines.extend(terminal(oe,x-12.70,y-2.54,x-38.10,y-2.54,ref+'/1'))
        lines.extend(terminal('GND',x-12.70,y+2.54,x-38.10,y+2.54,ref+'/2'))
        lines.extend(terminal('GND',x,y+10.16,x+20.32,y+20.32,ref+'/3'))
        lines.extend(terminal('CHARGER_GATE_EN',x+12.70,y,x+38.10,y,ref+'/4'))
        lines.extend(terminal('+3V3_USB',x,y-10.16,x+20.32,y-20.32,ref+'/5'))
    for ref,x,y,net in [('R94',76.20,71.12,'+3V3_USB'),('R95',76.20,91.44,'CHARGER_GATE_EN'),
                         ('R96',254.00,132.08,'E1_ILM'),('C55',76.20,111.76,'USB_PROTECTED_DRAFT'),
                         ('C56',254.00,71.12,'CHARGER_IN_DRAFT'),('C57',254.00,91.44,'E1_DVDT'),
                         ('C58',76.20,223.52,'+3V3_USB'),('C59',254.00,223.52,'+3V3_USB')]:
        if ref=='R94':
            lines.extend(terminal('+3V3_USB',x-5.08,y,x-25.40,y,ref+'/1'))
            lines.extend(terminal('CHARGER_GATE_EN',x+5.08,y,x+25.40,y,ref+'/2'))
        else:
            lines.extend(terminal(net,x-5.08,y,x-25.40,y,ref+'/1'))
            lines.extend(terminal('GND',x+5.08,y,x+25.40,y,ref+'/2'))
    lines.extend(source_flag(76.20,157.48))
    return '\n'.join(lines+['(embedded_fonts no)',')'])+'\n'


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,default=PROJECT/'charger-gate.kicad_sch')
    args=parser.parse_args()
    args.output.write_text(generate(),encoding='utf-8')


if __name__=='__main__':
    main()
