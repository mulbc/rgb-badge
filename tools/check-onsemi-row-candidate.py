#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Check the isolated onsemi row trial against KiCad XML and ERC output."""

import argparse
from collections import Counter, defaultdict
import hashlib
from pathlib import Path
import runpy
import xml.etree.ElementTree as ET
import json


ROOT = Path(__file__).resolve().parents[1]
CANDIDATE = ROOT / 'hardware/coupon/rev-a/staging/onsemi-row-candidate/rows.kicad_sch'
GENERATOR = ROOT / 'tools/generate-coupon-rows.py'
CANONICAL_SHA256 = 'e332b3a7d50a1e66fba1797a9481fff820d7df3dd5a5181797295764b742aa28'
PAIR_FOOTPRINT = 'rgb-badge-coupon:WDFN6_2x2_onsemi_NTLJD3119C'
DECODER_PINS = (11, 9, 10, 8, 7, 6, 5, 4, 18, 17, 20, 19, 14, 13, 16, 15)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def check_generated():
    generate = runpy.run_path(str(GENERATOR))['generate']
    canonical = generate().encode()
    require(hashlib.sha256(canonical).hexdigest() == CANONICAL_SHA256,
            'Default canonical row generation changed')
    require(CANDIDATE.read_text(encoding='utf-8') == generate('onsemi-candidate'),
            'Committed onsemi row sheet differs from deterministic generator')


def check_xml(path):
    root = ET.parse(path).getroot()
    components = {item.get('ref'): item for item in root.findall('./components/comp')}
    require(len(components) == 55, f'Expected 55 candidate components, got {len(components)}')
    require(Counter(item.findtext('value') for item in components.values()) ==
            {'NTLJD3119CTBG': 16, '74HC4514PW,118': 1,
             '1k 1%': 16, '100k 1%': 21, '100n 16V X7R': 1},
            'Candidate population differs from one pair and two gate resistors per row')
    by_net = defaultdict(set)
    for net in root.findall('./nets/net'):
        for node in net.findall('node'):
            by_net[net.get('name')].add((node.get('ref'), node.get('pin')))
    for index in range(16):
        row = f'{index:02d}'
        pair, pullup, pulldown = f'Q{index + 1}', f'R{index + 6}', f'R{index + 22}'
        item = components[pair]
        require(item.findtext('value') == 'NTLJD3119CTBG' and
                item.findtext('footprint') == PAIR_FOOTPRINT,
                f'{pair} exact package/footprint mismatch')
        expected = {
            f'ROW_{row}_A': {(pair, '3')},
            f'ROW_GATE_{row}': {(pair, '5'), (pair, '6'), (pullup, '2')},
            f'ROW_SEL_{row}': {(pair, '2'), (pulldown, '1'), ('U2', str(DECODER_PINS[index]))},
        }
        for net, nodes in expected.items():
            require(by_net[net] == nodes, f'{net}: expected {nodes}, got {by_net[net]}')
        for net, node in [('VLED', (pair, '4')), ('VLED', (pullup, '1')),
                          ('GND', (pair, '1')), ('GND', (pulldown, '2'))]:
            require(node in by_net[net], f'{pair}: missing {node} on {net}')
    print('Onsemi candidate XML: 16 exact numbered pairs, decoder selects and gate-bias nets passed')


def check_erc(path):
    data = json.loads(path.read_text())
    found = Counter((item['severity'], item['type'])
                    for sheet in data['sheets'] for item in sheet['violations'])
    expected = {('error', 'power_pin_not_driven'): 2,
                ('warning', 'isolated_pin_label'): 16}
    require(found == expected, f'Unexpected standalone candidate ERC findings: {found}')
    print('Onsemi candidate ERC: 18 expected standalone boundary findings only')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--netlist', type=Path, required=True)
    parser.add_argument('--erc', type=Path, required=True)
    args = parser.parse_args()
    check_generated()
    check_xml(args.netlist)
    check_erc(args.erc)


if __name__ == '__main__':
    main()
