#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Check the generated provisional BQ24074 sheet and exact native XML pins."""

from pathlib import Path
import runpy
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / 'hardware/coupon/rev-a'
GEN = runpy.run_path(str(ROOT / 'tools/generate-coupon-charger-core.py'))
PARTS = GEN['h'].PARTS
EXPECTED = {
    ('U41', '1'): 'CHARGER_TS', ('U41', '2'): '+BAT_PROTECTED_DRAFT',
    ('U41', '3'): '+BAT_PROTECTED_DRAFT', ('U41', '4'): 'GND',
    ('U41', '5'): 'GND', ('U41', '6'): 'GND',
    ('U41', '7'): 'unconnected-(U41-PGOOD-Pad7)', ('U41', '8'): 'GND',
    ('U41', '9'): 'unconnected-(U41-CHG-Pad9)',
    ('U41', '10'): '+SYS_APP_IN_DRAFT', ('U41', '11'): '+SYS_APP_IN_DRAFT',
    ('U41', '12'): 'CHARGER_ILIM', ('U41', '13'): 'CHARGER_IN_DRAFT',
    ('U41', '14'): 'unconnected-(U41-TMR-Pad14)',
    ('U41', '15'): 'unconnected-(U41-ITERM-Pad15)',
    ('U41', '16'): 'CHARGER_ISET', ('U41', '17'): 'GND',
    ('R92', '1'): 'CHARGER_ISET', ('R92', '2'): 'GND',
    ('R93', '1'): 'CHARGER_ILIM', ('R93', '2'): 'GND',
    ('C52', '1'): 'CHARGER_IN_DRAFT', ('C52', '2'): 'GND',
    ('C53', '1'): '+BAT_PROTECTED_DRAFT', ('C53', '2'): 'GND',
    ('C54', '1'): '+SYS_APP_IN_DRAFT', ('C54', '2'): 'GND',
}


def check_source():
    actual = (PROJECT / 'charger-core.kicad_sch').read_text(encoding='utf-8')
    if actual != GEN['generate']():
        raise ValueError('Charger core differs from deterministic generator')
    root = (PROJECT / 'rgb-badge-coupon.kicad_sch').read_text(encoding='utf-8')
    if root.count('(property "Sheetfile" "charger-core.kicad_sch"') != 1:
        raise ValueError('Charger core must be root-linked exactly once')
    if len(PARTS) != 6 or sum(row[5] for row in PARTS.values()) != len(EXPECTED):
        raise ValueError('Charger core component/pin inventory mismatch')
    for ref in ('#FLG08', '#FLG09'):
        if f'(property "Reference" "{ref}"' not in actual:
            raise ValueError(f'Missing provisional external supply marker {ref}')


def check_netlist(xml_path):
    root = ET.parse(xml_path).getroot()
    components, connected = {}, {}
    for comp in root.findall('./components/comp'):
        ref = comp.get('ref')
        if ref in PARTS:
            components[ref] = (comp.findtext('value'), comp.findtext('footprint'))
    for net in root.findall('./nets/net'):
        for node in net.findall('node'):
            key = node.get('ref'), node.get('pin')
            if key[0] in PARTS:
                if key in connected:
                    raise ValueError(f'Duplicate charger pin: {key}')
                connected[key] = net.get('name')
    expected_components = {ref: (row[1], 'rgb-badge-coupon:' + row[2]) for ref, row in PARTS.items()}
    if components != expected_components:
        raise ValueError(f'Charger population mismatch: {components}')
    if connected != EXPECTED:
        differences = {key: (EXPECTED.get(key), connected.get(key)) for key in set(EXPECTED) | set(connected)
                       if EXPECTED.get(key) != connected.get(key)}
        raise ValueError(f'Charger pin-to-net mismatch: {differences}')
    if ('TH1', '1') not in [(node.get('ref'), node.get('pin'))
                           for net in root.findall('./nets/net') if net.get('name') == 'CHARGER_TS'
                           for node in net.findall('node')]:
        raise ValueError('Battery-facing NTC is not on charger TS net')


def main():
    check_source()
    if len(sys.argv) == 3 and sys.argv[1] == '--netlist':
        check_netlist(Path(sys.argv[2]))
        print('Charger KiCad XML: 6 items, 27 exact pins; NTC connected to TS.')
    elif len(sys.argv) == 1:
        print('Charger sheet matches deterministic source: 6 items, 27 pins.')
    else:
        raise SystemExit('Usage: check-coupon-charger-core.py [--netlist PATH]')


if __name__ == '__main__':
    main()
