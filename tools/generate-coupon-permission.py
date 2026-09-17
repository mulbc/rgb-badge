#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Generate two staged USB permission sheets into a NEW directory.

Canonical KiCad files are reviewed copies of this deterministic output. The detector inputs now connect to the USB interface sheet; supervisors and
application controls remain explicit test boundaries.
"""

import argparse
import json
from pathlib import Path
import re
import runpy
import uuid

TOOLS = Path(__file__).resolve().parent
LIB = runpy.run_path(str(TOOLS / 'check-power-libraries.py'))
PROJECT_DIR = TOOLS.parent / 'hardware/coupon/rev-a'
ROOT_UUID = '207fb68e-2ddb-46bb-8712-eba2f8c5eef6'
NAMESPACE = uuid.UUID(ROOT_UUID)
PROJECT = 'rgb-badge-coupon'


def uid(name):
    return str(uuid.uuid5(NAMESPACE, 'usb-permission-rev-a/' + name))


def q(s):
    return json.dumps(str(s))


def field(name, value, x, y, hidden=False):
    return f'(property {q(name)} {q(value)} (at {x:.3f} {y:.3f} 0) (effects (font (size 1.27 1.27)){" (hide yes)" if hidden else ""}))'


def extract_symbol(source, mpn):
    """Extract a balanced source expression without depending on indentation."""
    matches = list(re.finditer(r'\(symbol "' + re.escape(mpn) + r'"\s', source))
    if len(matches) != 1:
        raise ValueError(f'Expected one top-level library symbol: {mpn}')
    start = matches[0].start()
    depth, quoted, escape = 0, False, False
    for i in range(start, len(source)):
        c = source[i]
        if quoted:
            if escape: escape = False
            elif c == '\\': escape = True
            elif c == '"': quoted = False
        elif c == '"': quoted = True
        elif c == '(': depth += 1
        elif c == ')':
            depth -= 1
            if depth == 0:
                return source[start:i+1].replace(f'(symbol "{mpn}"', f'(symbol "rgb-badge-coupon:{mpn}"', 1)
    raise ValueError('Unterminated symbol')


class Sheet:
    def __init__(self, name, title):
        self.name = name
        self.sheet_uuid = uid(name + '/sheet')
        self.file_uuid = uid(name + '/file')
        self.source = (PROJECT_DIR / 'symbols/rgb-badge-coupon.kicad_sym').read_text()
        root = LIB['parse'](PROJECT_DIR / 'symbols/rgb-badge-coupon.kicad_sym')
        self.symbols = {s[1]: s for s in LIB['children'](root, 'symbol')}
        self.used, self.body = set(), []
        self.title = title

    def note(self, text, x, y, tag, size=1.27):
        self.body.append(f'(text {q(text)} (at {x:.3f} {y:.3f} 0) (effects (font (size {size} {size})) (justify left)) (uuid {q(uid(self.name+tag))}))')

    def label(self, net, px, py, end_x, tag):
        angle, just = (180, 'right') if end_x < px else (0, 'left')
        self.body += [
            f'(wire (pts (xy {px:.3f} {py:.3f}) (xy {end_x:.3f} {py:.3f})) (stroke (width 0) (type default)) (uuid {q(uid(tag+"/wire"))}))',
            f'(global_label {q(net)} (shape passive) (at {end_x:.3f} {py:.3f} {angle}) (effects (font (size 1.016 1.016)) (justify {just})) (uuid {q(uid(tag+"/label"))}) {field("Intersheetrefs", "${INTERSHEET_REFS}", end_x, py, True)})',
        ]

    def component(self, ref, mpn, x, y, nets, value=None):
        self.used.add(mpn)
        lib = self.symbols[mpn]
        props = LIB['property_map'](lib)
        pins = LIB['library_pins'](lib)
        virtual = mpn == 'PWR_FLAG'
        purchased = mpn not in ('PWR_FLAG', 'TestPoint_Pad')
        top = max(float(LIB['one'](p, 'at', 'pin')[2]) for p in pins.values())
        header = max(12.70 if ref.startswith('U') else 6.35, top + 5.08)
        ry, vy = y-header, y-header+2.54
        items = [f'(symbol (lib_id "rgb-badge-coupon:{mpn}") (at {x:.3f} {y:.3f} 0) (unit 1)',
                 f'(exclude_from_sim no) (in_bom {"yes" if purchased else "no"}) (on_board {"no" if virtual else "yes"}) (dnp no)',
                 f'(uuid {q(uid(ref))})', field('Reference',ref,x,ry,virtual), field('Value', value or mpn,x,vy)]
        for k in ('Footprint', 'Datasheet', 'Manufacturer', 'MPN'):
            items.append(field(k, (mpn if purchased else '') if k=='MPN' else props.get(k,''),x,y,True))
        items.extend(f'(pin {q(n)} (uuid {q(uid(ref+"/pin/"+n))}))' for n in pins)
        items.append(f'(instances (project {q(PROJECT)} (path "/{ROOT_UUID}/{self.sheet_uuid}" (reference {q(ref)}) (unit 1)))))')
        self.body += items
        for n,pin in pins.items():
            at = LIB['one'](pin,'at','pin')
            px,py = x+float(at[1]),y-float(at[2])
            if n not in nets:
                self.body.append(f'(no_connect (at {px:.3f} {py:.3f}) (uuid {q(uid(ref+"/nc/"+n))}))')
            else:
                # Top/bottom power pins have horizontal stubs clear of headings.
                left = float(at[1]) < 0 or (float(at[1])==0 and float(at[2])<0)
                self.label(nets[n],px,py,px+(-10.16 if left else 10.16),ref+'/'+n)

    def capacitor(self, ref, x, y):
        self.component(ref,'GRM155R71C104KA88D',x,y,{'1':'+3V3_USB','2':'GND'},'100n 16V X7R')

    def output(self):
        return '\n'.join(['(kicad_sch (version 20260306) (generator "rgb_badge_permission") (generator_version "1.0")',
                          f'(uuid {q(self.file_uuid)}) (paper "A2")',
                          f'(title_block (title {q(self.title)}) (rev "A-draft") (comment 1 "SPDX-License-Identifier: CERN-OHL-S-2.0") (comment 2 "Staged logic; supervisors, startup inhibit and charger actuation remain open"))',
                          '(lib_symbols\n'+'\n'.join(extract_symbol(self.source,n) for n in sorted(self.used))+'\n)',
                          *self.body,'(embedded_fonts no)',')',''])


RAW = ('OUT1','OUT2','CHG_AL_N','CHG_DET','SW_OPEN','VBUS_VALID','LOGIC_READY','SWITCH_ON','ESP_RUNNING','USB_REQUEST')


def conditioning():
    s = Sheet('usb-conditioning','Coupon Rev A - USB input conditioning (staged)')
    s.note('USB input conditioning: detector outputs connected; five supervisor/application inputs remain staged',20.32,20.32,'title',2)
    s.note('OUT1/OUT2 and BC outputs come from usb-interface. Supervisors, switch and MCU inputs remain test boundaries.',20.32,30.48,'boundary')
    s.note('CHG_DET uses the staged 4.80-5.25 V USB supply boundary; protection is pending. ESP_RUNNING is not tied to ESP_EN.',20.32,38.10,'domains')
    for i in range(5):
        x,y = 83.82+(i%3)*180.34,76.20+(i//3)*119.38
        a,b=RAW[2*i:2*i+2]
        s.note(f'{a} / {b}: conditioned before ordinary LVC gates',x-60.96,y-20.32,f'group{i}',1.016)
        s.component(f'U{24+i}','SN74LVC2G17DBVR',x,y,{'1':'USB_RAW_'+a,'2':'GND','3':'USB_RAW_'+b,'4':'USB_'+b,'5':'+3V3_USB','6':'USB_'+a})
        s.capacitor(f'C{24+i}',x,y+22.86)
        for j,name in enumerate((a,b)):
            n=2*i+j
            up=name in ('OUT1','OUT2','CHG_AL_N','SW_OPEN')
            s.component(f'R{60+n}','ERJ-2RKF1002X' if up else 'ERJ-2RKF1003X',x,y+45.72+j*20.32,
                        {'1':'USB_RAW_'+name,'2':'+3V3_USB' if up else 'GND'},'10k 1%' if up else '100k 1%')
    for i,name in enumerate(RAW):
        x,y=83.82+(i%5)*106.68,325.12+(i//5)*25.4
        s.component(f'TP{20+i}','TestPoint_Pad',x,y,{'1':'USB_RAW_'+name},name)
    s.note('+3V3_USB is supplied by U29 on usb-interface; its protected 5 V input is still a draft boundary.',378.46,241.30,'power',1.016)
    s.note('Default pull-ups: 10 kohm. Default pull-downs: 100 kohm. Source/leakage/suspend budgets remain to be qualified.',20.32,375.92,'pulls')
    return s


def permission():
    s=Sheet('usb-permission','Coupon Rev A - USB charging permission gates (staged)')
    s.note('ADR 0011 permission gates: physical pin connectivity is checked against all 1,024 input combinations',20.32,20.32,'title',2)
    s.note('USB_HIGH_REQ and USB_EN1_RAW_N are test outputs, NOT connections to ILIM or charger EN1.',20.32,30.48,'actuator')
    s.note('Supply supervision, ramp/brownout inhibition and the parallel ILIM switch are still outside this captured boundary.',20.32,38.10,'startup')
    # MPNS and pin assignments are explicit rather than generated from the oracle.
    gates = [
        ('U10','00',{'1':'USB_OUT1','2':'USB_OUT2','4':'USB_ATTACHED'},'Attached = NOT (OUT1 AND OUT2)'),
        ('U11','04',{'2':'USB_OUT1','4':'USB_CC_HIGH'},'CC high-current advertisement'),
        ('U12','04',{'2':'USB_CHG_AL_N','4':'USB_BC_ALLOWED'},'Positive BC classification'),
        ('U13','04',{'2':'USB_CHG_DET','4':'USB_NOT_CHG_DET'},'No charging-source flag'),
        ('U14','04',{'2':'USB_SW_OPEN','4':'USB_DATA_CLOSED'},'BC data switch closed'),
        ('U15','08',{'1':'USB_BC_ALLOWED','2':'USB_CHG_DET','4':'USB_BC_HIGH'},'Qualified BC high-current source'),
        ('U16','32',{'1':'USB_CC_HIGH','2':'USB_BC_HIGH','4':'USB_SOURCE_HIGH'},'Hardware source permission'),
        ('U17','11',{'1':'USB_VBUS_VALID','3':'USB_LOGIC_READY','6':'USB_ATTACHED','4':'USB_READY_ATTACHED'},'Both supplies valid AND attached'),
        ('U18','08',{'1':'USB_READY_ATTACHED','2':'USB_SOURCE_HIGH','4':'USB_HIGH_REQ'},'Hardware-only high-current request'),
        ('U19','11',{'1':'USB_BC_ALLOWED','3':'USB_NOT_CHG_DET','6':'USB_DATA_CLOSED','4':'USB_SDP'},'SDP data-source qualification'),
        ('U20','11',{'1':'USB_SWITCH_ON','3':'USB_ESP_RUNNING','6':'USB_USB_REQUEST','4':'USB_APP_GRANT'},'ON AND running AND USB-stack grant'),
        ('U21','11',{'1':'USB_READY_ATTACHED','3':'USB_SDP','6':'USB_APP_GRANT','4':'USB_LOW_REQ'},'Low-current-only application route'),
        ('U22','32',{'1':'USB_HIGH_REQ','2':'USB_LOW_REQ','4':'USB_RUN_REQ'},'Either qualified route can request run'),
        ('U23','06',{'2':'USB_RUN_REQ','4':'USB_EN1_RAW_N'},'Open-drain request output; not charger pin'),
    ]
    for i,(ref,code,nets,description) in enumerate(gates):
        x,y=78.74+(i%4)*139.70,76.20+(i//4)*76.20
        nets |= {'2' if code=='11' else '3':'GND','5':'+3V3_USB'}
        s.note(description,x-58.42,y-22.86,ref+'-title',1.016)
        s.component(ref,f'SN74LVC1G{code}DBVR',x,y,nets)
        s.capacitor('C'+ref[1:],x,y+27.94)
    s.component('R70','ERJ-2RKF1002X',358.14,325.12,{'1':'+3V3_USB','2':'USB_EN1_RAW_N'},'10k 1%')
    s.component('TP30','TestPoint_Pad',487.68,325.12,{'1':'USB_HIGH_REQ'},'HIGH_REQ')
    s.component('TP31','TestPoint_Pad',487.68,350.52,{'1':'USB_EN1_RAW_N'},'EN1_RAW_N')
    s.note('The 3.3 V pull-up on the RAW output is for this logic boundary only; it does not meet charger startup requirements.',20.32,375.92,'raw-pullup')
    return s


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output',type=Path,required=True)
    args=p.parse_args()
    LIB['check_libraries'](PROJECT_DIR)
    args.output.mkdir(parents=True,exist_ok=False)
    for sheet in (conditioning(),permission()):
        path=args.output/(sheet.name+'.kicad_sch')
        path.write_text(sheet.output(),encoding='utf-8')
        print(f'{path}: sheet UUID {sheet.sheet_uuid}, file UUID {sheet.file_uuid}')


if __name__=='__main__':
    main()
