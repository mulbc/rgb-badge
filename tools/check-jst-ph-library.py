#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Audit the staged exact S2B-PH-SM4-TB connector land and pad numbering."""

from pathlib import Path
import runpy

ROOT = Path(__file__).resolve().parents[1]
LIB = runpy.run_path(str(ROOT / 'tools/check-led-libraries.py'))
parse = LIB['parse_sexpr']
children = LIB['children']
one = LIB['only_child']
SOURCE = ROOT / 'hardware/coupon/rev-a/footprints/rgb-badge-coupon.pretty/JST_PH_S2B-PH-SM4-TB.kicad_mod'


def check():
    footprint = parse(SOURCE)
    if footprint[1] != 'JST_PH_S2B-PH-SM4-TB' or children(footprint, 'model'):
        raise ValueError('Exact JST footprint name or project-local model rule changed')
    pads = {}
    for pad in children(footprint, 'pad'):
        number = pad[1]
        at = one(pad, 'at', 'pad')
        size = one(pad, 'size', 'pad')
        layers = one(pad, 'layers', 'pad')
        pads.setdefault(number, []).append((tuple(at[1:3]), tuple(size[1:3]), tuple(layers[1:])))
    expected = {
        '1': [(('-1', '-2.85'), ('1', '3.5'), ('F.Cu', 'F.Mask', 'F.Paste'))],
        '2': [(('1', '-2.85'), ('1', '3.5'), ('F.Cu', 'F.Mask', 'F.Paste'))],
        'MP': [(('-3.35', '2.9'), ('1.5', '3.4'), ('F.Cu', 'F.Mask', 'F.Paste')),
               (('3.35', '2.9'), ('1.5', '3.4'), ('F.Cu', 'F.Mask', 'F.Paste'))],
    }
    if pads != expected:
        raise ValueError(f'JST signal/retention pad map changed: {pads}')
    courtyard = [rect for rect in children(footprint, 'fp_rect')
                 if one(rect, 'layer', 'rectangle')[1] == 'F.CrtYd']
    if len(courtyard) != 1 or (tuple(one(courtyard[0], 'start', 'courtyard')[1:3]),
                               tuple(one(courtyard[0], 'end', 'courtyard')[1:3])) != (('-4.6', '-5.1'), ('4.6', '5.1')):
        raise ValueError('JST courtyard extent changed')
    return True


if __name__ == '__main__':
    check()
    print('Staged JST S2B-PH-SM4-TB land check passed: two 2 mm-pitch contacts, two retention lands, 9.2 × 10.2 mm courtyard.')
