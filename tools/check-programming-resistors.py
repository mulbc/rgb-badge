#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Audit ADR 0012 precision resistor libraries and conditional error budget."""

from copy import deepcopy
from decimal import Decimal as D
import json
from pathlib import Path
import runpy

TOOLS=Path(__file__).resolve().parent
LIB=runpy.run_path(str(TOOLS/'check-power-libraries.py'))
PARTS={'ERA2AEB3651X':D('3650'),'ERA2AEB3481X':D('3480'),'ERA2AEB1131X':D('1130')}
TOTAL_ERROR=D('.01')
FOOTPRINT='R_Panasonic_ERA2_0402'


def resistance_factors(tolerance='.001',tcr='.000025',delta_t='65',drift='.005'):
    """Initial, temperature and allocated post-assembly/service errors multiply.

    Drift is a project allocation, not a manufacturer lifetime guarantee.
    """
    t,c,d,a=map(D,(tolerance,tcr,delta_t,drift))
    if not all(v.is_finite() and v>=0 for v in (t,c,d,a)) or max(t,c*d,a)>=1:
        raise ValueError('Invalid resistance error inputs')
    return (1-t)*(1-c*d)*(1-a),(1+t)*(1+c*d)*(1+a)


def check_budget(**kwargs):
    low,high=resistance_factors(**kwargs)
    if low<1-TOTAL_ERROR or high>1+TOTAL_ERROR:
        raise ValueError('Programming resistor exceeds the total ±1% design envelope')
    return low,high


def check_libraries(project=LIB['PROJECT']):
    parse,children,one=LIB['parse'],LIB['children'],LIB['one']
    symbols={s[1]:s for s in children(parse(project/'symbols/rgb-badge-coupon.kicad_sym'),'symbol')}
    for mpn in PARTS:
        expected=json.dumps(symbols['ERJ-2RKF1003X']).replace('ERJ-2RKF1003X',mpn).replace('R_Panasonic_ERJ2_0402',FOOTPRINT).replace('RDA0000/AOA0000C304.pdf','RDM0000/AOA0000C307.pdf')
        if json.dumps(symbols[mpn])!=expected:
            raise ValueError(f'{mpn}: exact identity, source, passive pins or symbol geometry mismatch')
    folder=project/'footprints/rgb-badge-coupon.pretty'
    actual=parse(folder/(FOOTPRINT+'.kicad_mod'))
    expected=deepcopy(parse(folder/'R_Panasonic_ERJ2_0402.kicad_mod'))
    expected[1]=FOOTPRINT
    for prop in children(expected,'property'):
        if prop[1]=='Value':prop[2]=FOOTPRINT
    courtyard=next(r for r in children(expected,'fp_rect') if one(r,'layer','rect')[1]=='F.CrtYd')
    one(courtyard,'start','courtyard')[2]='-0.55'
    one(courtyard,'end','courtyard')[2]='0.55'
    if actual!=expected:
        raise ValueError('ERA2 footprint differs from audited lands/body/expanded courtyard')
    # The ERA maximum body width is 0.60 mm; preserve 0.25 mm courtyard
    # clearance from it, not just from the 0.50-mm nominal drawing/pads.
    if D(one(courtyard,'end','courtyard')[2])-D('.60')/2<D('.25'):
        raise ValueError('ERA2 maximum-body courtyard clearance too small')
    return check_budget()


if __name__=='__main__':
    low,high=check_libraries()
    print(f'Programming resistor audit passed: 3 exact ERA2 parts, one land pattern; allocated resistance factors {low}..{high} fit ±1%.')
    print('Assembly/service drift allocation and whole-port current remain unqualified; no charger capture or native review claimed.')
