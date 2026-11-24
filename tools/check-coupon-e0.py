#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Check the deterministic E0 source bridge and native XML pin map."""

from pathlib import Path
import runpy
import sys
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]
PROJECT=ROOT/'hardware/coupon/rev-a'
GEN=runpy.run_path(str(ROOT/'tools/generate-coupon-e0.py'))
PARTS=GEN['h'].PARTS
EXPECTED={
 ('U45','1'):'E0_EN',('U45','2'):'E0_OVLO',
 ('U45','3'):'unconnected-(U45-PG-Pad3)',
 ('U45','4'):'unconnected-(U45-PGTH-Pad4)',
 ('U45','5'):'VBUS_CONNECTOR',('U45','6'):'+5V_USB',
 ('U45','7'):'E0_DVDT',('U45','8'):'GND',('U45','9'):'E0_ILM',
 ('U45','10'):'unconnected-(U45-ITIMER-Pad10)',
 ('R97','1'):'VBUS_CONNECTOR',('R97','2'):'E0_OVLO',
 ('R98','1'):'E0_OVLO',('R98','2'):'GND',
 ('R99','1'):'VBUS_CONNECTOR',('R99','2'):'E0_EN',
 ('R100','1'):'E0_ILM',('R100','2'):'GND',
 ('C60','1'):'VBUS_CONNECTOR',('C60','2'):'GND',
 ('C61','1'):'+5V_USB',('C61','2'):'GND',
 ('C62','1'):'E0_DVDT',('C62','2'):'GND',
}


def check_source():
    if (PROJECT/'usb-protection.kicad_sch').read_text()!=GEN['generate']():
        raise ValueError('E0 sheet differs from deterministic generator')
    root=(PROJECT/'rgb-badge-coupon.kicad_sch').read_text()
    if root.count('(property "Sheetfile" "usb-protection.kicad_sch"')!=1:
        raise ValueError('E0 sheet not root-linked exactly once')
    if len(PARTS)!=8 or sum(row[5] for row in PARTS.values())!=len(EXPECTED):
        raise ValueError('E0 component/pin inventory mismatch')
    interface=(PROJECT/'usb-interface.kicad_sch').read_text()
    if interface.count('(property "Reference" "#FLG05"')!=1:
        raise ValueError('Missing external connector VBUS source marker')
    if '(global_label "VBUS_CONNECTOR" (shape passive) (at 299.720 355.600 0)' not in interface:
        raise ValueError('External source marker is not on connector VBUS')
    if '(property "Reference" "#FLG08"' in (PROJECT/'charger-gate.kicad_sch').read_text():
        raise ValueError('Parallel fictitious E1 input source marker remains')


def check_netlist(xml_path):
    root=ET.parse(xml_path).getroot()
    components={}
    connected={}
    nets={}
    for comp in root.findall('./components/comp'):
        ref=comp.get('ref')
        if ref in PARTS:components[ref]=(comp.findtext('value'),comp.findtext('footprint'))
    for net in root.findall('./nets/net'):
        name=net.get('name')
        nets[name]={(node.get('ref'),node.get('pin')) for node in net.findall('node')}
        for node in net.findall('node'):
            key=node.get('ref'),node.get('pin')
            if key[0] in PARTS:
                if key in connected:raise ValueError(f'Duplicate E0 pin {key}')
                connected[key]=name
    expected_parts={ref:(row[1],'rgb-badge-coupon:'+row[2]) for ref,row in PARTS.items()}
    if components!=expected_parts:raise ValueError(f'E0 population mismatch: {components}')
    if connected!=EXPECTED:
        differences={key:(EXPECTED.get(key),connected.get(key)) for key in set(EXPECTED)|set(connected)
                     if EXPECTED.get(key)!=connected.get(key)}
        raise ValueError(f'E0 pin-to-net mismatch: {differences}')
    for net,pin in [('VBUS_CONNECTOR',('J1','A4_B9')),
                    ('+5V_USB',('U29','1')),
                    ('+5V_USB',('U44','5'))]:
        if pin not in nets.get(net,set()):raise ValueError(f'E0 boundary lacks {pin} on {net}')


def main():
    check_source()
    if len(sys.argv)==3 and sys.argv[1]=='--netlist':
        check_netlist(Path(sys.argv[2]))
        print('E0 KiCad XML: eight exact parts, 24 pins; connector, USB logic and E1 input joined.')
    elif len(sys.argv)==1:
        print('E0 source sheet matches deterministic 8-part, 24-pin capture.')
    else:raise SystemExit('Usage: check-coupon-e0.py [--netlist PATH]')


if __name__=='__main__':main()
