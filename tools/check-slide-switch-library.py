#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Check the provisional exact-MPN DPDT switch symbol and six local lands."""

from decimal import Decimal
from pathlib import Path
import runpy
import hashlib
import copy


ROOT = Path(__file__).resolve().parents[1]
PARSER = runpy.run_path(str(ROOT / 'tools/check-led-libraries.py'))
parse = PARSER['parse_sexpr']
children = PARSER['children']
one = PARSER['only_child']
properties = PARSER['property_map']
PART = 'JS202011JCQN'
FOOTPRINT = 'SW_CK_JS202011JCQN_ManufacturerPins'


def check(project=ROOT/'hardware/coupon/rev-a'):
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
                    '5': 'A2', '6': 'COM2', '7': 'B2'}

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
        '5': (Decimal('-2.5'), Decimal('1.2')),
        '6': (Decimal('0'), Decimal('1.2')),
        '7': (Decimal('2.5'), Decimal('1.2')),
    }
    legacy_path=project/'footprints/rgb-badge-coupon.pretty/SW_CK_JS202011JCQN.kicad_mod'
    assert hashlib.sha256(legacy_path.read_bytes()).hexdigest()=='fa050c2fa9f8d6741d5d91dcae2fe0a58829d9fbc71d70fc6a76b73a80c1344b', 'Historical switch land changed'
    legacy=parse(legacy_path);normalized=copy.deepcopy(footprint);normalized[1]=legacy[1]
    for pad in children(normalized,'pad'):
        if pad[1] in ('5','6','7'):pad[1]=str(int(pad[1])-1)
    strip_description=lambda fp:[q for q in fp if not(isinstance(q,list) and q and q[0]=='descr')]
    assert strip_description(normalized)==strip_description(legacy), 'Switch correction changed geometry or layer data'
    print('Provisional JS202011JCQN library check passed: exact MPN, six unique printed pins/pads (1/2/3, 5/6/7). Manufacturer visual pin-direction audit remains open.')


if __name__ == '__main__':
    check()
