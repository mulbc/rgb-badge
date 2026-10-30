# SPDX-License-Identifier: Apache-2.0
"""ADR 0071 printed terminal mapping, preserving every physical land and net."""
OLD='rgb-badge-coupon:SW_CK_JS202011JCQN'
NEW='rgb-badge-coupon:SW_CK_JS202011JCQN_ManufacturerPins'
FORWARD={'1':'1','2':'2','3':'3','4':'5','5':'6','6':'7'}
REVERSE={new:old for old,new in FORWARD.items()}
LEGACY_PADS={'1':(-2500000,1200000,''),'2':(0,1200000,'+SYS_APP_IN_DRAFT'),
             '3':(2500000,1200000,'APP_ON_SW_DRAFT'),'4':(-2500000,-1200000,''),
             '5':(0,-1200000,'+BAT_PROTECTED_DRAFT'),'6':(2500000,-1200000,'+BAT_GAUGE_SW')}


def verify_part(part,corrected):
    import pcbnew as p
    assert part.GetReference()=='SW2' and part.GetField('MPN').GetText()=='JS202011JCQN'
    assert part.GetFPIDAsString()==(NEW if corrected else OLD)
    assert part.GetLayer()==p.B_Cu, 'Unreviewed switch side'
    expected={FORWARD[k] if corrected else k:v for k,v in LEGACY_PADS.items()}
    pads=list(part.Pads());assert len(pads)==6 and {q.GetNumber() for q in pads}==set(expected)
    for q in pads:
        x,y,net=expected[q.GetNumber()];pos=q.GetFPRelativePosition()
        assert (pos.x,pos.y,q.GetNetname())==(x,y,net), 'Switch physical pin/net mapping differs'
        assert q.GetSize()==p.VECTOR2I(1000000,1600000) and q.GetShape()==p.PAD_SHAPE_RECT


def apply(board):
    part=board.FindFootprintByReference('SW2');verify_part(part,False)
    for pad in list(part.Pads()):pad.SetNumber(FORWARD[pad.GetNumber()])
    part.SetFPIDAsString(NEW);verify_part(part,True)


def historical_identity(pad,identity):
    part=pad.GetParentFootprint()
    if part.GetReference()=='SW2' and part.GetFPIDAsString()==NEW:
        number=pad.GetNumber();assert number in REVERSE
        old=REVERSE[number];x,y,net=LEGACY_PADS[old];pos=pad.GetFPRelativePosition()
        assert (pos.x,pos.y,pad.GetNetname())==(x,y,net), 'Switch identity cannot hide changed physical contact'
        return ('SW2',old,pos.x,pos.y)
    return identity


def normalized_signature(pad,signature):
    if pad.GetParentFootprint().GetReference()=='SW2' and pad.GetParentFootprint().GetFPIDAsString()==NEW:
        signature=list(signature);signature[0]=historical_identity(pad,None)[1];return tuple(signature)
    return signature
