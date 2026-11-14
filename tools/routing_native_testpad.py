# SPDX-License-Identifier: Apache-2.0
"""ADR0101 exact native capture and bounded TP13 connection; no grid rounding."""
from collections import Counter
import math

ISOLATION_SHA = '01fb2e8a1ac781172797d369df99ff3c834016453ffeaa3d76c224b525355031'


def verify_native(old,new,plan,signature):
    import pcbnew as p
    entry = plan.get('native_testpad_escape')
    if entry is None:
        return None
    assert entry['reference'] == 'TP13' and entry['net'] == 'VLED_ENABLE_CANDIDATE' and entry['source_pad'] == ['U55','7']
    assert entry['isolation_source_sha256'] == ISOLATION_SHA, 'TP13 isolation basis differs'
    rows = entry['copper']; vias = [row for row in rows if row[0]=='via']; tracks = [row for row in rows if row[0]=='track']
    assert len(vias)==2 and tracks
    for row in vias:
        assert row[1]==entry['net'] and row[4:]==['In4.Cu','B.Cu',300000,100000,int(p.VIATYPE_MICROVIA)]
    for row in tracks:
        assert row[:2]==['track',entry['net']] and row[6:]==['In4.Cu',200000]
    length = sum(math.dist(row[2:4],row[4:6]) for row in tracks)
    assert length <= 5000000, 'TP13 lead exceeds 5 mm'
    assert not Counter(map(tuple,rows))-Counter(map(tuple,plan['added_copper'])), 'TP13 escape copper missing'
    before,after = [board.FindFootprintByReference('TP13') for board in (old,new)]
    a,z = list(before.Pads()),list(after.Pads()); assert len(a)==len(z)==1; a,z=a[0],z[0]
    assert before.GetFPIDAsString()==after.GetFPIDAsString()=='rgb-badge-coupon:TestPoint_Pad_D1.0mm'
    assert before.GetLayer()==after.GetLayer()==p.B_Cu and before.GetOrientationDegrees()==after.GetOrientationDegrees()
    assert a.GetNumber()==z.GetNumber()=='1' and a.GetNetname()==z.GetNetname()==entry['net']
    assert a.GetSize()==z.GetSize()==p.VECTOR2I(1000000,1000000) and a.GetShape()==z.GetShape()==p.PAD_SHAPE_CIRCLE
    cluster=lambda board,q:frozenset(t.m_Uuid.AsString() for t in board.GetConnectivity().GetConnectedItems(q) if isinstance(t,p.PAD))
    assert len(cluster(old,a))==1
    assert entry['isolation_pad_group']==[a.m_Uuid.AsString()], 'Test-land historical isolation group differs'
    source=next(q for q in new.FindFootprintByReference('U55').Pads() if q.GetNumber()=='7')
    prior=next(group for group in plan['previous_checkpoint']['pad_groups'] if a.m_Uuid.AsString() in group)
    if plan['previous_checkpoint']['source_sha256']==ISOLATION_SHA:
        assert prior==[a.m_Uuid.AsString()], 'TP13 first-adoption source not isolated'
    else:
        assert source.m_Uuid.AsString() in prior, 'TP13 previous join missing'
    shape,box=a.GetEffectiveShape(p.B_Cu),a.GetBoundingBox()
    for board in (old,new):
        for t in board.GetTracks():
            if isinstance(t,p.PCB_TRACK) and not isinstance(t,p.PCB_VIA) and t.GetStart()==t.GetEnd():continue
            if t.IsOnLayer(p.B_Cu) and box.Intersects(t.GetBoundingBox()):
                assert not shape.Collide(t.GetEffectiveShape(p.B_Cu),0), 'TP13 prior copper-contact proof failed'
    wanted=Counter(map(tuple,rows)); selected=[]
    for t in new.GetTracks():
        key=signature(new,t)
        if wanted[key]:selected.append(t);wanted[key]-=1
    assert not +wanted
    vv=[t for t in selected if isinstance(t,p.PCB_VIA)]
    captures=[]
    for pad,message in [(source,'Native source capture moved'),(z,'Native target capture moved')]:
        matching=[v for v in vv if v.GetPosition()==pad.GetPosition()]
        assert len(matching)==1,message
        v=matching[0];assert v.GetEffectiveShape(p.B_Cu).Collide(pad.GetEffectiveShape(p.B_Cu),0)
        assert any(t.GetLayer()==p.In4_Cu and t.GetEffectiveShape(p.In4_Cu).Collide(v.GetEffectiveShape(p.In4_Cu),0) for t in selected if not isinstance(t,p.PCB_VIA)), 'Native capture lacks inner trace'
        captures.append([v.GetPosition().x,v.GetPosition().y])
    assert captures[0]==[26250000,20875000], 'Native source capture moved'
    assert cluster(new,z)==cluster(new,source) and len(cluster(new,z))>1, 'TP13 numbered output join missing'
    return {'source_capture_iu':captures[0],'target_capture_iu':captures[1],
        'historical_isolation_source_sha256':ISOLATION_SHA,'prior_isolation_and_no_copper_contact':True,
        'joined_pad':['U55','7'],'trace_length_mm':length/1e6,'new_vias':2,'source_copper_retired':False}
