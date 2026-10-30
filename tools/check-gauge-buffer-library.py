#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Check TCA9517ADGKR pin numbers and TI DGK0008A local land geometry."""

from pathlib import Path
import runpy

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / 'hardware/coupon/rev-a'
LIB = runpy.run_path(str(ROOT / 'tools/check-led-libraries.py'))
parse, children, one = LIB['parse_sexpr'], LIB['children'], LIB['only_child']
SYMBOL = 'TCA9517ADGKR'
LAND = 'VSSOP_TI_DGK0008A'


def check():
    library = parse(PROJECT / 'symbols/rgb-badge-coupon.kicad_sym')
    candidates = [s for s in children(library, 'symbol') if s[1] == SYMBOL]
    if len(candidates) != 1:
        raise ValueError('Exact gauge buffer symbol absent or duplicated')
    pins = {}
    for unit in children(candidates[0], 'symbol'):
        for pin in children(unit, 'pin'):
            number = one(pin, 'number', 'pin')[1]
            name = one(pin, 'name', 'pin')[1]
            if number in pins:
                raise ValueError('Duplicate buffer pin number')
            pins[number] = name
    expected_pins = {'1': 'VCCA', '2': 'SCLA', '3': 'SDAA', '4': 'GND',
                     '5': 'EN', '6': 'SDAB', '7': 'SCLB', '8': 'VCCB'}
    if pins != expected_pins:
        raise ValueError(f'TCA9517ADGKR pin map changed: {pins}')
    footprint = parse(PROJECT / f'footprints/rgb-badge-coupon.pretty/{LAND}.kicad_mod')
    if footprint[1] != LAND or children(footprint, 'model'):
        raise ValueError('Buffer land name or project-local model rule changed')
    pads = {}
    for pad in children(footprint, 'pad'):
        number = pad[1]
        if number in pads:
            raise ValueError('Duplicate buffer pad number')
        pads[number] = (tuple(one(pad, 'at', 'pad')[1:3]),
                        tuple(one(pad, 'size', 'pad')[1:3]),
                        tuple(one(pad, 'layers', 'pad')[1:]))
    expected_pads = {}
    for n, y in enumerate(('-0.975', '-0.325', '0.325', '0.975'), 1):
        expected_pads[str(n)] = (('-1.5', y), ('1.4', '0.45'), ('F.Cu', 'F.Paste', 'F.Mask'))
    for n, y in enumerate(('0.975', '0.325', '-0.325', '-0.975'), 5):
        expected_pads[str(n)] = (('1.5', y), ('1.4', '0.45'), ('F.Cu', 'F.Paste', 'F.Mask'))
    if pads != expected_pads:
        raise ValueError(f'TI DGK0008A pad geometry changed: {pads}')
    courtyard = [r for r in children(footprint, 'fp_rect') if one(r, 'layer', 'rect')[1] == 'F.CrtYd']
    if len(courtyard) != 1 or (tuple(one(courtyard[0], 'start', 'rect')[1:3]),
                               tuple(one(courtyard[0], 'end', 'rect')[1:3])) != (('-2.45', '-1.85'), ('2.45', '1.85')):
        raise ValueError('Buffer courtyard changed')
    return True


if __name__ == '__main__':
    check()
    print('Exact TCA9517ADGKR symbol and TI DGK0008A land: 8 pins/pads, 0.65 mm pitch, no external model.')
