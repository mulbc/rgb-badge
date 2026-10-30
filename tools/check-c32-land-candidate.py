#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Check the unselected exact C32 reflow candidate against the supplied drawing."""
from decimal import Decimal as D
from pathlib import Path
import runpy

ROOT=Path(__file__).resolve().parents[1]
FOOTPRINT=ROOT/'hardware/coupon/rev-a/staging/library-candidates.pretty/C_Murata_GRM188R60J106ME47_0603.kicad_mod'
A=runpy.run_path(str(ROOT/'tools/check-led-libraries.py'))


def one(node,tag):
    rows=A['children'](node,tag)
    assert len(rows)==1, 'Expected one '+tag
    return rows[0]


def validate(fp):
    assert fp[:2]==['footprint','C_Murata_GRM188R60J106ME47_0603']
    pads=A['children'](fp,'pad')
    assert len(pads)==2 and [p[1] for p in pads]==['1','2']
    for pad,x in zip(pads,[D('-.675'),D('.675')]):
        assert pad[2:4]==['smd','rect']
        assert list(map(D,one(pad,'at')[1:3]))==[x,D(0)], 'Exact part land centre differs'
        assert list(map(D,one(pad,'size')[1:3]))==[D('.65'),D('.70')], 'Exact reflow land b/c differs'
        assert one(pad,'layers')[1:]==['F.Cu','F.Paste','F.Mask']
    # a is the inner gap, b the length of ONE copper land, c its width.
    # The legacy implementation's oversized b must not be accepted by
    # relabelling a/b or selecting the larger dimensional-tolerance row.
    a=2*D('.675')-D('.65');b=D('.65');c=D('.70')
    assert D('.6')<=a<=D('.8') and D('.6')<=b<=D('.7') and D('.6')<=c<=D('.8')
    rects={one(q,'layer')[1]:q for q in A['children'](fp,'fp_rect')}
    for layer,expected in [('F.Fab',['-.8','-.4','.8','.4']),('F.CrtYd',['-1.25','-.65','1.25','.65'])]:
        q=rects[layer]
        assert list(map(D,one(q,'start')[1:3]+one(q,'end')[1:3]))==list(map(D,expected))
    return {'status':'EXACT_PART_LAND_CANDIDATE_NOT_SELECTED_FOR_CANONICAL_PCB',
            'mpn':'GRM188R60J106ME47D','gap_a_mm':str(a),'pad_b_mm':str(b),'pad_c_mm':str(c),
            'fabrication_release_allowed':False}


if __name__=='__main__':
    print(validate(A['parse_sexpr'](FOOTPRINT)))
