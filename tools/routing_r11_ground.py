# SPDX-License-Identifier: Apache-2.0
"""ADR0115 exact R11 leaf retirement and native shunt-ground endpoint proof."""
from collections import Counter
import math
from routing_track_replacements import contacts

ORIGINAL=('track','ROW_GATE_05',71750000,4250000,72150000,4250000,'B.Cu',200000)
ENDPOINTS=[([70995000,1150000],'B.Cu'),([69295346,4349500],'In4.Cu')]


def validate_plan(plan):
    entry=plan.get('r11_ground_replacement')
    assert ('R11' in plan['poses'])==(entry is not None),'R11 relocation guard missing'
    if entry is None:return Counter()
    assert entry['original_copper']==list(ORIGINAL),'Unreviewed R11 retirement'
    assert entry['reference']=='R11' and entry['original_junction_contacts'],'R11 original contacts missing'
    pose=plan['poses']['R11']
    assert pose=={'old_position_iu':[72250000,4250000],'old_angle_deg':180,'position_iu':[72750000,4250000],'angle_deg':180},'R11 relocation pose differs'
    gate=entry['gate_replacement']
    assert gate and sum(math.dist(row[2:4],row[4:6]) for row in gate)<=1000000,'R11 gate lead exceeds bound'
    for row in gate:
        assert row[:2]==['track','ROW_GATE_05'] and row[6:]==['B.Cu',200000],'R11 gate geometry differs'
        assert all(71900000<=row[i]<=72700000 for i in (2,4)) and all(3950000<=row[i]<=4550000 for i in (3,5)),'R11 gate lead outside bounds'
    ground=entry['ground_copper'];vias=[row for row in ground if row[0]=='via']
    assert len(vias)==1 and vias[0][4:]==['In4.Cu','B.Cu',300000,100000,1],'Ground-route adjacent capture missing'
    for row in ground:
        assert row[1]=='GND' and all(69000000<=row[i]<=71700000 for i in (2,)) and 1100000<=row[3]<=4500000,'Ground route outside bounds'
        if row[0]=='track':
            assert row[6] in ['B.Cu','In4.Cu'] and row[7]==200000 and 69000000<=row[4]<=71700000 and 1100000<=row[5]<=4500000,'Ground route geometry differs'
    assert not Counter(map(tuple,gate+ground))-Counter(map(tuple,plan['added_copper'])),'R11 or ground replacement missing'
    assert [(q['point_iu'],q['layer']) for q in entry['ground_endpoint_contacts']]==ENDPOINTS,'Ground endpoint moved'
    return Counter([ORIGINAL])


def verify_native(old,new,plan,signature,physical_identity):
    import pcbnew as p
    entry=plan.get('r11_ground_replacement');validate_plan(plan)
    if entry is None:return None
    a=old.FindFootprintByReference('R11');z=new.FindFootprintByReference('R11')
    for f in (a,z):
        assert f.GetValue()=='1k 1%' and f.GetFPIDAsString()=='rgb-badge-coupon:R_Panasonic_ERJ2_0402'
        assert next(q.GetText() for q in f.GetFields() if q.GetName()=='MPN')=='ERJ2RKF1001X'
    leaf=next(t for t in old.GetTracks() if signature(old,t)==ORIGINAL)
    for pad in a.Pads():
        external=[signature(old,t) for t in old.GetTracks() if t.GetNetCode()==pad.GetNetCode() and t.IsOnLayer(p.B_Cu) and t.GetEffectiveShape(p.B_Cu).Collide(pad.GetEffectiveShape(p.B_Cu),0)]
        assert external==([ORIGINAL] if pad.GetNumber()=='2' else []),'R11 source land contact scope differs'
    boundary=contacts(old,leaf,signature,physical_identity)
    assert [key for key,item in boundary]==entry['original_junction_contacts'],'R11 original leaf contacts differ'
    def key(item):return ['pad',*physical_identity(item)] if isinstance(item,p.PAD) else ['copper',*signature(new,item)]
    actual={q.m_Uuid.AsString():q for q in list(new.GetTracks())+[q for f in new.GetFootprints() for q in f.Pads()]}
    selected=lambda rows:[t for t in new.GetTracks() if list(signature(new,t)) in rows]
    gate=selected(entry['gate_replacement']);ground=selected(entry['ground_copper'])
    pin=lambda board,ref,n:next(q for q in board.FindFootprintByReference(ref).Pads() if q.GetNumber()==n)
    moved=pin(new,'R11','2')
    assert any(t.GetEffectiveShape(p.B_Cu).Collide(moved.GetEffectiveShape(p.B_Cu),0) for t in gate),'R11 moved gate contact lost'
    for expected,item in boundary:
        if isinstance(item,p.PAD):
            assert physical_identity(item)[:2]==('R11','2') or list(physical_identity(item)[:2])==['R11','2']
            continue
        assert item.m_Uuid.AsString() in actual and key(actual[item.m_Uuid.AsString()])==expected,'R11 retained boundary identity differs'
        assert any(t.GetEffectiveShape(p.B_Cu).Collide(actual[item.m_Uuid.AsString()].GetEffectiveShape(p.B_Cu),0) for t in gate),'R11 retained far-end contact lost'
    olditems=list(old.GetTracks())+[q for f in old.GetFootprints() for q in f.Pads()]
    for ep in entry['ground_endpoint_contacts']:
        layer=old.GetLayerID(ep['layer']);shape=p.SHAPE_CIRCLE(p.VECTOR2I(*ep['point_iu']),100000);expected=[]
        for item in olditems:
            if item.GetNetname()=='GND' and item.IsOnLayer(layer) and item.GetEffectiveShape(layer).Collide(shape,0):
                k=['pad',*physical_identity(item)] if isinstance(item,p.PAD) else ['copper',*signature(old,item)]
                expected.append({'uuid':item.m_Uuid.AsString(),'key':k})
        assert sorted(expected,key=repr)==ep['contacts'] and expected,'Ground source endpoint contact inventory differs'
        for row in expected:
            assert row['uuid'] in actual and key(actual[row['uuid']])==row['key'],'Ground endpoint source copper lost'
            assert any(t.IsOnLayer(layer) and t.GetEffectiveShape(layer).Collide(actual[row['uuid']].GetEffectiveShape(layer),0) for t in ground),'Ground actual endpoint contact lost'
            if isinstance(actual[row['uuid']],p.PCB_VIA):
                centre=actual[row['uuid']].GetPosition()
                assert any(not isinstance(t,p.PCB_VIA) and t.IsOnLayer(layer) and (t.GetStart()==centre or t.GetEnd()==centre) for t in ground),'Ground retained via centre not reached'
    group=lambda board,q:frozenset(t.m_Uuid.AsString() for t in board.GetConnectivity().GetConnectedItems(q) if isinstance(t,p.PAD))|{q.m_Uuid.AsString()}
    assert group(old,pin(old,'U38','3'))!=group(old,pin(old,'U35','9')),'Shunt source not isolated'
    assert group(new,pin(new,'U38','3'))==group(new,pin(new,'U52','3'))==group(new,pin(new,'U35','9')),'Actual shunt ground join missing'
    assert group(new,moved)==group(new,pin(new,'PAIR06','5')),'Actual R11 gate continuity missing'
    return {'reference':'R11','displacement_iu':[500000,0],'exact_original_leaf_retired':True,'all_original_land_contacts_accounted_for':True,'original_contact_count':len(boundary),'far_end_contacts_retained':True,'actual_old_ground_endpoints_retained':True,'retained_ground_via_centres_reached':True,'main_ground_pad_count':len(group(new,pin(new,'U35','9'))),'shunt_ground_joined':True,'gate_lead_length_mm':sum(math.dist(row[2:4],row[4:6]) for row in entry['gate_replacement'])/1e6}
