#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Generate provisional autonomous connector-to-protected-USB E0 sheet."""

import argparse
import importlib.util
from pathlib import Path
import uuid

ROOT=Path(__file__).resolve().parents[1]
PROJECT=ROOT/'hardware/coupon/rev-a'
ROOT_UUID='207fb68e-2ddb-46bb-8712-eba2f8c5eef6'
SHEET_UUID='3d2d377d-95a1-5768-ad3e-aacb83e8c36d'
SCOPE=uuid.UUID(SHEET_UUID)
FILE_UUID=str(uuid.uuid5(SCOPE,'file'))
spec=importlib.util.spec_from_file_location('coupon_3v3_generator',ROOT/'tools/generate-coupon-3v3.py')
h=importlib.util.module_from_spec(spec)
spec.loader.exec_module(h)
h.SCOPE,h.FILE_UUID=SCOPE,FILE_UUID
TI='https://www.ti.com/lit/ds/symlink/tps25947.pdf'
PAN='https://industrial.panasonic.com/ww/products/pt/general-purpose-chip-resistors/models/'
h.PARTS={
 'U45':('TPS259474ARPWR','TPS259474ARPWR','VQFN_TI_RPW0010A_2x2mm_HotRod','Texas Instruments',TI,10),
 'R97':('ERJ2RKF3832X','38.3k 1%','R_Panasonic_ERJ2_0402','Panasonic',PAN+'ERJ2RKF3832X',2),
 'R98':('ERJ2RKF1002X','10k 1%','R_Panasonic_ERJ2_0402','Panasonic',PAN+'ERJ2RKF1002X',2),
 'R99':('ERJ2RKF3903X','390k 1%','R_Panasonic_ERJ2_0402','Panasonic',PAN+'ERJ2RKF3903X',2),
 'R100':('ERJ2RKF3321X','3.32k 1%','R_Panasonic_ERJ2_0402','Panasonic',PAN+'ERJ2RKF3321X',2),
 'C60':('C1608X7R1H105K080AB','1u 50V X7R','C_TDK_C1608_0603','TDK','https://product.tdk.com/en/search/capacitor/ceramic/mlcc/info?part_no=C1608X7R1H105K080AB',2),
 'C61':('GRM187R61A226ME15','22u 10V X5R','C_Murata_GRM18_0603','Murata','https://pim.murata.com/en-global/pim/details/?partNum=GRM187R61A226ME15',2),
 'C62':('GRM1555C1H222GA01D','2.2n 50V C0G','C_Murata_GRM15_0402','Murata','https://www.murata.com/en-us/products/productdetail?partno=GRM1555C1H222GA01%23',2),
}


def part(ref,x,y):
    return [line.replace(f'(path "/{FILE_UUID}"',f'(path "/{ROOT_UUID}/{SHEET_UUID}"') for line in h.component(ref,x,y)]


def terminal(net,x,y,end_x,end_y,key):
    points=[(x,y)]
    if x!=end_x and y!=end_y:points.append((x,end_y))
    points.append((end_x,end_y))
    lines=[h.wire(*a,*b,f'{key}/{i}') for i,(a,b) in enumerate(zip(points,points[1:]))]
    angle,justify=(180,'right') if end_x<x else (0,'left')
    lines.append(f'(global_label {h.q(net)} (shape passive) (at {end_x:.3f} {end_y:.3f} {angle}) {h.effects(justify=justify)} (uuid {h.q(h.uid(key+"/label"))}) {h.prop("Intersheetrefs", "${INTERSHEET_REFS}", end_x, end_y, True)})')
    return lines


def nc(x,y,key):
    return f'(no_connect (at {x:.3f} {y:.3f}) (uuid {h.q(h.uid(key))}))'


def generate():
    mpns=dict.fromkeys(row[0] for row in h.PARTS.values())
    lines=['(kicad_sch','(version 20260306)','(generator "rgb_badge_e0")','(generator_version "1.0")',
           f'(uuid {h.q(FILE_UUID)})','(paper "A3")',
           '(title_block (title "Coupon Rev A - provisional E0 USB input protection") (rev "A-draft") (comment 1 "SPDX-License-Identifier: CERN-OHL-S-2.0") (comment 2 "Electrical source capture only; connector faults and inrush unqualified"))',
           '(lib_symbols\n'+'\n'.join(h.cached_symbol(mpn) for mpn in mpns)+'\n)',
           f'(text "E0 joins connector VBUS to USB logic and E1 input. No firmware or charge request controls E0." (at 20.320 20.320 0) {h.effects(justify="left")} (uuid {h.q(h.uid("note/1"))}))',
           f'(text "OVLO is disconnect, not surge clamp. CIN bias, cable inductance and fault waveforms open." (at 20.320 27.940 0) {h.effects(justify="left")} (uuid {h.q(h.uid("note/2"))}))']
    for ref,x,y in [('U45',170.18,106.68),('R97',76.20,71.12),('R98',76.20,91.44),
                    ('R99',76.20,111.76),('R100',254.00,132.08),('C60',76.20,132.08),
                    ('C61',254.00,71.12),('C62',254.00,91.44)]:
        lines.extend(part(ref,x,y))
    for pin,net,x,y,ex,ey in [
        ('5','VBUS_CONNECTOR',154.94,96.52,124.46,96.52),
        ('1','E0_EN',154.94,101.60,124.46,101.60),
        ('2','E0_OVLO',154.94,106.68,124.46,106.68),
        ('6','+5V_USB',185.42,96.52,215.90,96.52),
        ('7','E0_DVDT',185.42,106.68,215.90,106.68),
        ('9','E0_ILM',185.42,111.76,215.90,111.76),
        ('8','GND',170.18,124.46,170.18,144.78)]:
        lines.extend(terminal(net,x,y,ex,ey,'U45/'+pin))
    for pin,x,y in [('3',185.42,101.60),('4',154.94,111.76),('10',185.42,116.84)]:
        lines.append(nc(x,y,'U45/'+pin+'/nc'))
    for ref,x,y,left,right in [
        ('R97',76.20,71.12,'VBUS_CONNECTOR','E0_OVLO'),
        ('R98',76.20,91.44,'E0_OVLO','GND'),
        ('R99',76.20,111.76,'VBUS_CONNECTOR','E0_EN'),
        ('R100',254.00,132.08,'E0_ILM','GND'),
        ('C60',76.20,132.08,'VBUS_CONNECTOR','GND'),
        ('C61',254.00,71.12,'+5V_USB','GND'),
        ('C62',254.00,91.44,'E0_DVDT','GND')]:
        lines.extend(terminal(left,x-5.08,y,x-25.40,y,ref+'/1'))
        lines.extend(terminal(right,x+5.08,y,x+25.40,y,ref+'/2'))
    return '\n'.join(lines+['(embedded_fonts no)',')'])+'\n'


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output',type=Path,default=PROJECT/'usb-protection.kicad_sch')
    p.parse_args().output.write_text(generate(),encoding='utf-8')


if __name__=='__main__':main()
