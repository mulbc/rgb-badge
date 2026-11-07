#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Check the generated temperature sheet and its exact native XML nets."""

from pathlib import Path
import runpy
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / 'hardware/coupon/rev-a'
GEN = runpy.run_path(str(ROOT / 'tools/generate-coupon-temperature.py'))
PARTS = GEN['h'].PARTS
EXPECTED = {
    ('TH1', '1'): 'CHARGER_TS', ('TH1', '2'): 'GND',
    ('TP34', '1'): 'CHARGER_TS', ('TP35', '1'): 'CHARGER_GATE_EN',
    ('U39', '1'): 'TMP_HOT_SET', ('U39', '2'): 'TMP_COLD_SET',
    ('U39', '3'): 'GND', ('U39', '4'): 'TEMP_OK',
    ('U39', '5'): '+3V3_USB', ('U39', '6'): 'TEMP_OK',
    ('U40', '1'): 'TEMP_OK', ('U40', '2'): 'GND',
    ('U40', '3'): 'GND', ('U40', '4'): 'CHARGER_GATE_EN',
    ('U40', '5'): '+3V3_USB',
    ('R89', '1'): 'TMP_HOT_SET', ('R89', '2'): 'GND',
    ('R90', '1'): 'TMP_COLD_SET', ('R90', '2'): 'GND',
    ('R91', '1'): '+3V3_USB', ('R91', '2'): 'TEMP_OK',
    ('C50', '1'): '+3V3_USB', ('C50', '2'): 'GND',
    ('C51', '1'): '+3V3_USB', ('C51', '2'): 'GND',
}


def check_source():
    actual = (PROJECT / 'charger-temperature.kicad_sch').read_text(encoding='utf-8')
    if actual != GEN['generate']():
        raise ValueError('Temperature sheet differs from deterministic generator')
    if len(PARTS) != 10 or sum(row[5] for row in PARTS.values()) != len(EXPECTED):
        raise ValueError('Temperature component/pin inventory mismatch')


def check_netlist(xml_path):
    root = ET.parse(xml_path).getroot()
    components = {}
    connected = {}
    for comp in root.findall('./components/comp'):
        ref = comp.get('ref')
        if ref in PARTS:
            components[ref] = (comp.findtext('value'), comp.findtext('footprint'))
    for net in root.findall('./nets/net'):
        for node in net.findall('node'):
            key = node.get('ref'), node.get('pin')
            if key[0] in PARTS:
                if key in connected:
                    raise ValueError(f'Duplicate temperature pin: {key}')
                connected[key] = net.get('name')
    expected_components = {ref: (row[1], 'rgb-badge-coupon:' + row[2]) for ref, row in PARTS.items()}
    if components != expected_components:
        raise ValueError(f'Temperature component population mismatch: {components}')
    if connected != EXPECTED:
        differences = {key: (EXPECTED.get(key), connected.get(key)) for key in set(EXPECTED) | set(connected)
                       if EXPECTED.get(key) != connected.get(key)}
        raise ValueError(f'Temperature pin-to-net mismatch: {differences}')


def main():
    check_source()
    if len(sys.argv) == 3 and sys.argv[1] == '--netlist':
        check_netlist(Path(sys.argv[2]))
        print('Temperature KiCad XML: 10 items, 25 exact pins connected.')
    elif len(sys.argv) == 1:
        print('Temperature sheet matches deterministic source: 10 items, 25 pins.')
    else:
        raise SystemExit('Usage: check-coupon-temperature.py [--netlist PATH]')


if __name__ == '__main__':
    main()
