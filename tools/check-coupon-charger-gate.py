#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Check deterministic provisional E1 gate and exact native XML pin nets."""

from pathlib import Path
import runpy
import sys
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]
PROJECT=ROOT/'hardware/coupon/rev-a'
GEN=runpy.run_path(str(ROOT/'tools/generate-coupon-charger-gate.py'))
PARTS=GEN['h'].PARTS
EXPECTED={
 ('U44','1'):'CHARGER_GATE_EN',('U44','2'):'GND',
 ('U44','3'):'unconnected-(U44-PG-Pad3)',('U44','4'):'unconnected-(U44-PGTH-Pad4)',
 ('U44','5'):'+5V_USB',('U44','6'):'CHARGER_IN_DRAFT',
 ('U44','7'):'E1_DVDT',('U44','8'):'GND',('U44','9'):'E1_ILM',
 ('U44','10'):'unconnected-(U44-ITIMER-Pad10)',
 ('U42','1'):'USB_CHARGE_REQ',('U42','2'):'GND',('U42','3'):'GND',
 ('U42','4'):'CHARGER_GATE_EN',('U42','5'):'+3V3_USB',
 ('U43','1'):'USB_RAW_LOGIC_READY',('U43','2'):'GND',('U43','3'):'GND',
 ('U43','4'):'CHARGER_GATE_EN',('U43','5'):'+3V3_USB',
 ('R94','1'):'+3V3_USB',('R94','2'):'CHARGER_GATE_EN',
 ('R95','1'):'CHARGER_GATE_EN',('R95','2'):'GND',
 ('R96','1'):'E1_ILM',('R96','2'):'GND',
 ('C55','1'):'+5V_USB',('C55','2'):'GND',
 ('C56','1'):'CHARGER_IN_DRAFT',('C56','2'):'GND',
 ('C57','1'):'E1_DVDT',('C57','2'):'GND',
 ('C58','1'):'+3V3_USB',('C58','2'):'GND',
 ('C59','1'):'+3V3_USB',('C59','2'):'GND',
}


def check_source():
    actual=(PROJECT/'charger-gate.kicad_sch').read_text()
    if actual!=GEN['generate']():
        raise ValueError('E1 gate differs from deterministic generator')
    root=(PROJECT/'rgb-badge-coupon.kicad_sch').read_text()
    if root.count('(property "Sheetfile" "charger-gate.kicad_sch"')!=1:
        raise ValueError('E1 gate must be root-linked exactly once')
    if len(PARTS)!=11 or sum(row[5] for row in PARTS.values())!=len(EXPECTED):
        raise ValueError('E1 gate component/pin inventory mismatch')
    if '(property "Reference" "#FLG08"' in actual:
        raise ValueError('Old provisional E0 source marker remains in parallel with physical E0 output')
    if '(property "Reference" "#FLG08"' in (PROJECT/'charger-core.kicad_sch').read_text():
        raise ValueError('Old BQ input source marker remains in parallel with E1 output')


def check_netlist(xml_path):
    root=ET.parse(xml_path).getroot()
    components={}
    connected={}
    nets={}
    for comp in root.findall('./components/comp'):
        ref=comp.get('ref')
        if ref in PARTS:
            components[ref]=(comp.findtext('value'),comp.findtext('footprint'))
    for net in root.findall('./nets/net'):
        name=net.get('name')
        nets[name]={(node.get('ref'),node.get('pin')) for node in net.findall('node')}
        for node in net.findall('node'):
            key=node.get('ref'),node.get('pin')
            if key[0] in PARTS:
                if key in connected: raise ValueError(f'Duplicate E1 pin {key}')
                connected[key]=name
    expected_parts={ref:(row[1],'rgb-badge-coupon:'+row[2]) for ref,row in PARTS.items()}
    if components!=expected_parts:
        raise ValueError(f'E1 population mismatch: {components}')
    if connected!=EXPECTED:
        differences={key:(EXPECTED.get(key),connected.get(key)) for key in set(EXPECTED)|set(connected)
                     if EXPECTED.get(key)!=connected.get(key)}
        raise ValueError(f'E1 pin-to-net mismatch: {differences}')
    for net,pin in [('CHARGER_GATE_EN',('U40','4')),
                    ('CHARGER_IN_DRAFT',('U41','13')),
                    ('USB_CHARGE_REQ',('U17','4')),
                    ('USB_RAW_LOGIC_READY',('U34','1')),
                    ('+5V_USB',('U45','6'))]:
        if pin not in nets.get(net,set()):
            raise ValueError(f'E1 boundary lacks {pin} on {net}')


def main():
    check_source()
    if len(sys.argv)==3 and sys.argv[1]=='--netlist':
        check_netlist(Path(sys.argv[2]))
        print('E1 KiCad XML: 11 items, 36 exact pins; source, supervisor, temperature and BQ nets joined.')
    elif len(sys.argv)==1:
        print('E1 gate sheet matches deterministic source: 11 items, 36 pins.')
    else:
        raise SystemExit('Usage: check-coupon-charger-gate.py [--netlist PATH]')


if __name__=='__main__':main()
