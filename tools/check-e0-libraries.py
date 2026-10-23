#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Audit exact provisional E0 resistor/capacitor symbols and the TDK land."""

from decimal import Decimal as D
from pathlib import Path
import runpy

ROOT=Path(__file__).resolve().parents[1]
PROJECT=ROOT/'hardware/coupon/rev-a'
CAP=runpy.run_path(str(ROOT/'tools/check-3v3-capacitor-footprints.py'))
LED=runpy.run_path(str(ROOT/'tools/check-led-libraries.py'))
parse,children=LED['parse_sexpr'],LED['children']


def properties(node):
    return {p[1]:p[2] for p in children(node,'property')}


def main():
    CAP['check']('C_TDK_C1608_0603',D('0.7'),D('0.7'),D('0.7'),D('0.7'),
                 (D('-0.8'),D('-0.4'),D('0.8'),D('0.4')),
                 (D('-1.3'),D('-0.6'),D('1.3'),D('0.6')))
    symbols={s[1]:s for s in children(parse(PROJECT/'symbols/rgb-badge-coupon.kicad_sym'),'symbol')}
    expected={
      'ERJ2RKF3832X':('R','Panasonic','rgb-badge-coupon:R_Panasonic_ERJ2_0402'),
      'ERJ2RKF3903X':('R','Panasonic','rgb-badge-coupon:R_Panasonic_ERJ2_0402'),
      'C1608X7R1H105K080AB':('C','TDK','rgb-badge-coupon:C_TDK_C1608_0603'),
    }
    for mpn,(ref,mfr,footprint) in expected.items():
        sym=symbols[mpn]
        props=properties(sym)
        if any(props.get(k)!=v for k,v in [('Reference',ref),('Value',mpn),
                                             ('MPN',mpn),('Manufacturer',mfr),
                                             ('Footprint',footprint)]):
            raise ValueError(f'{mpn}: exact metadata or footprint mismatch')
        pins=[p for unit in children(sym,'symbol') for p in children(unit,'pin')]
        if sorted(next(x[1] for x in children(p,'number')) for p in pins)!=['1','2'] or any(p[1]!='passive' for p in pins):
            raise ValueError(f'{mpn}: expected two passive numbered pins')
    print('E0 candidate libraries passed: exact 38.3k/390k and TDK 1u/50V symbols; TDK C1608 reflow lands.')


if __name__=='__main__':main()
