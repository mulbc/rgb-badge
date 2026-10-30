#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Exact ADR 0069 geometry and historical identity mapping; no other MPNs."""
from pathlib import Path
import math

ROOT=Path(__file__).resolve().parents[1]
REFS=('C3','C32','C44','C45','C53','C54')
MPN='GRM188R60J106ME47D'
NAME='C_Murata_GRM188R60J106ME47_0603'
OLD='rgb-badge-coupon:C_Murata_GRM18_0603'
NEW='rgb-badge-coupon:'+NAME
NETS={'C3':'+3V3_APP','C32':'+3V3_USB','C44':'+SYS_APP_IN_DRAFT',
      'C45':'+SYS_APP_IN_DRAFT','C53':'+BAT_PROTECTED_DRAFT','C54':'+SYS_APP_IN_DRAFT'}


def verify_part(f, corrected):
    import pcbnew as p
    ref=f.GetReference()
    assert ref in REFS and f.GetField('MPN').GetText()==MPN, 'Unreviewed Murata identity'
    assert f.GetFPIDAsString()==(NEW if corrected else OLD), 'Murata assignment differs'
    assert f.GetValue()=='10u 6.3V X5R' and f.GetField('Manufacturer').GetText()=='Murata'
    pads=list(f.Pads())
    assert len(pads)==2 and {q.GetNumber() for q in pads}=={'1','2'}
    for q in pads:
        x=(675000 if corrected else 800000)*(-1 if q.GetNumber()=='1' else 1)
        assert q.GetFPRelativePosition()==p.VECTOR2I(x,0), 'Murata pad position differs'
        expected_size=p.VECTOR2I(650000,700000) if corrected else p.VECTOR2I(900000,900000)
        assert q.GetSize()==expected_size, 'Murata land size differs'
        assert q.GetShape()==p.PAD_SHAPE_RECT and q.GetAttribute()==p.PAD_ATTRIB_SMD
        assert q.GetNetname()==(NETS[ref] if q.GetNumber()=='1' else 'GND'), 'Murata pin/net differs'
        assert set(q.GetLayerSet().Seq())==({p.B_Cu,p.B_Paste,p.B_Mask} if f.IsFlipped() else {p.F_Cu,p.F_Paste,p.F_Mask})
    # Local courtyard coordinates, invariant under placement rotation and flipping.
    rects=[g for g in f.GraphicalItems() if g.GetLayer() in (p.F_CrtYd,p.B_CrtYd)]
    assert len(rects)==1 and rects[0].GetShape()==p.SHAPE_T_RECT, 'Murata courtyard differs'
    g=rects[0];centre=f.GetPosition();angle=f.GetOrientation().AsRadians()
    corners=[]
    for pos in (g.GetStart(),g.GetEnd()):
        dx,dy=pos.x-centre.x,pos.y-centre.y
        corners.append((abs(round(dx*math.cos(angle)+dy*math.sin(angle))),
                        abs(round(-dx*math.sin(angle)+dy*math.cos(angle)))))
    assert corners==[(1250000 if corrected else 1500000,650000)]*2, 'Murata courtyard size differs'


def apply(board):
    import pcbnew as p
    parts={f.GetReference():f for f in board.GetFootprints()}
    assert {f.GetReference() for f in parts.values() if f.GetField('MPN') and f.GetField('MPN').GetText()==MPN}==set(REFS)
    for ref in REFS:
        f=parts[ref];verify_part(f,False)
        for q in f.Pads():
            q.SetSize(p.VECTOR2I(650000,700000))
            q.SetFPRelativePosition(p.VECTOR2I(-675000 if q.GetNumber()=='1' else 675000,0))
        centre=f.GetPosition();angle=f.GetOrientation().AsRadians()
        def scaled(pos):
            dx,dy=pos.x-centre.x,pos.y-centre.y
            x=(dx*math.cos(angle)+dy*math.sin(angle))*1.25/1.5
            y=-dx*math.sin(angle)+dy*math.cos(angle)
            return p.VECTOR2I(centre.x+round(x*math.cos(angle)-y*math.sin(angle)),
                              centre.y+round(x*math.sin(angle)+y*math.cos(angle)))
        for g in f.GraphicalItems():
            if g.GetLayer() in (p.F_CrtYd,p.B_CrtYd):
                g.SetStart(scaled(g.GetStart()));g.SetEnd(scaled(g.GetEnd()))
        f.SetFPIDAsString(NEW);verify_part(f,True)


def historical_identity(pad):
    pos=pad.GetFPRelativePosition();ref=pad.GetParentFootprint().GetReference()
    if ref in REFS and pad.GetParentFootprint().GetFPIDAsString()==NEW:
        assert pad.GetNumber() in ('1','2')
        assert (pos.x,pos.y)==(-675000 if pad.GetNumber()=='1' else 675000,0)
        return (ref,pad.GetNumber(),-800000 if pad.GetNumber()=='1' else 800000,0)
    return (ref,pad.GetNumber(),pos.x,pos.y)


def normalized_signature(pad, signature):
    result=list(signature(pad))
    if pad.GetParentFootprint().GetReference() in REFS and pad.GetParentFootprint().GetFPIDAsString()==NEW:
        assert result[4:6]==[650000,700000], 'Murata land size differs'
        result[2:6]=[historical_identity(pad)[2],0,900000,900000]
    return tuple(result)
