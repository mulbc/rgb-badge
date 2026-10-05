#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Check the unplaced exact-MPN DPDT switch symbol and six local lands."""

from decimal import Decimal
from pathlib import Path
import runpy


ROOT = Path(__file__).resolve().parents[1]
PARSER = runpy.run_path(str(ROOT / 'tools/check-led-libraries.py'))
parse = PARSER['parse_sexpr']
children = PARSER['children']
one = PARSER['only_child']
properties = PARSER['property_map']
PART = 'JS202011JCQN'
FOOTPRINT = 'SW_CK_JS202011JCQN'


def check():
    project = ROOT / 'hardware/coupon/rev-a'
    symbols = parse(project / 'symbols/rgb-badge-coupon.kicad_sym')
    matches = [s for s in children(symbols, 'symbol') if s[1] == PART]
    assert len(matches) == 1, 'switch symbol missing or duplicated'
    symbol = matches[0]
    meta = properties(symbol)
    assert meta['MPN'] == PART
    assert meta['Footprint'] == 'rgb-badge-coupon:' + FOOTPRINT
    pins = {}
    for unit in children(symbol, 'symbol'):
        for pin in children(unit, 'pin'):
            number = one(pin, 'number', 'switch pin')[1]
            assert number not in pins
            pins[number] = one(pin, 'name', 'switch pin')[1]
    assert pins == {'1': 'A1', '2': 'COM1', '3': 'B1',
                    '4': 'A2', '5': 'COM2', '6': 'B2'}

    footprint = parse(project / 'footprints/rgb-badge-coupon.pretty' / (FOOTPRINT + '.kicad_mod'))
    assert footprint[1] == FOOTPRINT
    pads = {}
    for pad in children(footprint, 'pad'):
        number = pad[1]
        assert number not in pads
        at = one(pad, 'at', 'pad')
        size = one(pad, 'size', 'pad')
        layers = one(pad, 'layers', 'pad')
        assert pad[2:4] == ['smd', 'rect']
        assert [Decimal(size[1]), Decimal(size[2])] == [Decimal('1.0'), Decimal('1.6')]
        assert set(layers[1:]) == {'F.Cu', 'F.Paste', 'F.Mask'}
        pads[number] = (Decimal(at[1]), Decimal(at[2]))
    assert pads == {
        '1': (Decimal('-2.5'), Decimal('-1.2')),
        '2': (Decimal('0'), Decimal('-1.2')),
        '3': (Decimal('2.5'), Decimal('-1.2')),
        '4': (Decimal('-2.5'), Decimal('1.2')),
        '5': (Decimal('0'), Decimal('1.2')),
        '6': (Decimal('2.5'), Decimal('1.2')),
    }
    print('Unplaced JS202011JCQN library check passed: exact MPN, six unique pins and pads. Manufacturer visual pin-direction audit remains open.')


if __name__ == '__main__':
    check()
