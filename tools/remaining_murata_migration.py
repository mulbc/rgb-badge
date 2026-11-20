#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Exact ADR 0084 pad-only policy; historical shared libraries stay unchanged."""
PARTS = {
 'GRM187R61A226ME15': dict(refs=('C40','C41','C46','C47','C48','C49','C56','C61'),
    old='C_Murata_GRM18_0603',name='C_Murata_GRM187R61A226ME15_0603',
    offset=775000,old_offset=800000,size=(750000,900000),old_size=(900000,900000),value='22u 10V X5R'),
 'GRM219R60J476ME44': dict(refs=('C42','C43'),
    old='C_Murata_GRM21_0805',name='C_Murata_GRM219R60J476ME44_0805',
    offset=950000,old_offset=950000,size=(700000,1300000),old_size=(1200000,1300000),value='47u 6.3V X5R')}
REFS=tuple(sorted(ref for spec in PARTS.values() for ref in spec['refs']))
NETS={'C40':'+SYS_APP_IN_DRAFT','C41':'+SYS_APP_IN_DRAFT','C42':'+3V3_APP','C43':'+3V3_APP',
      'C46':'VLED','C47':'VLED','C48':'VLED','C49':'VLED','C56':'CHARGER_IN_DRAFT','C61':'+5V_USB'}


def spec_for(ref):
    return next((mpn,spec) for mpn,spec in PARTS.items() if ref in spec['refs'])


def verify_part(f,corrected):
    import pcbnew as p
    ref=f.GetReference();assert ref in REFS, 'Unreviewed capacitor reference'
    mpn,spec=spec_for(ref)
    assert f.GetField('MPN').GetText()==mpn and f.GetField('Manufacturer').GetText()=='Murata'
    assert f.GetValue()==spec['value']
    assert f.GetFPIDAsString()=='rgb-badge-coupon:'+spec['name' if corrected else 'old'], 'Exact capacitor footprint differs'
    pads=list(f.Pads());assert len(pads)==2 and {q.GetNumber() for q in pads}=={'1','2'}
    for q in pads:
        x=spec['offset' if corrected else 'old_offset']*(-1 if q.GetNumber()=='1' else 1)
        assert q.GetFPRelativePosition()==p.VECTOR2I(x,0), 'Exact capacitor pad position differs'
        assert q.GetSize()==p.VECTOR2I(*spec['size' if corrected else 'old_size']), 'Exact capacitor pad size differs'
        assert q.GetShape()==p.PAD_SHAPE_RECT and q.GetAttribute()==p.PAD_ATTRIB_SMD
        assert q.GetNetname()==(NETS[ref] if q.GetNumber()=='1' else 'GND'), 'Capacitor numbered net differs'
        assert set(q.GetLayerSet().Seq())==({p.B_Cu,p.B_Paste,p.B_Mask} if f.IsFlipped() else {p.F_Cu,p.F_Paste,p.F_Mask})


def apply(board):
    import pcbnew as p
    parts={f.GetReference():f for f in board.GetFootprints()}
    for mpn,spec in PARTS.items():
        assert {ref for ref,f in parts.items() if f.GetField('MPN') and f.GetField('MPN').GetText()==mpn}==set(spec['refs'])
        for ref in spec['refs']:
            f=parts[ref];verify_part(f,False)
            for q in f.Pads():
                q.SetSize(p.VECTOR2I(*spec['size']))
                q.SetFPRelativePosition(p.VECTOR2I(spec['offset']*(-1 if q.GetNumber()=='1' else 1),0))
            f.SetFPIDAsString('rgb-badge-coupon:'+spec['name']);verify_part(f,True)


def historical_identity(pad,identity):
    f=pad.GetParentFootprint();ref=f.GetReference()
    if ref in REFS and f.GetFPIDAsString()=='rgb-badge-coupon:'+spec_for(ref)[1]['name']:
        verify_part(f,True)
        return (ref,pad.GetNumber(),spec_for(ref)[1]['old_offset']*(-1 if pad.GetNumber()=='1' else 1),0)
    return identity


def normalized_signature(pad,signature):
    f=pad.GetParentFootprint();ref=f.GetReference();result=list(signature)
    if ref in REFS and f.GetFPIDAsString()=='rgb-badge-coupon:'+spec_for(ref)[1]['name']:
        verify_part(f,True);spec=spec_for(ref)[1]
        result[2:6]=[spec['old_offset']*(-1 if pad.GetNumber()=='1' else 1),0,*spec['old_size']]
    return tuple(result)
