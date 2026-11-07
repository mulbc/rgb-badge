# SPDX-License-Identifier: Apache-2.0
"""ADR0099 exact permission lead and ADR0098 isolated TP14 relocation guards."""
from collections import Counter
import math
from routing_track_replacements import contacts

COHORT = [
 ('track','USB_RAW_LOGIC_READY',93500000,18950000,92900000,18350000,'B.Cu',200000),
 ('track','USB_RAW_LOGIC_READY',93500000,19600000,93500000,18950000,'B.Cu',200000),
 ('track','USB_RAW_LOGIC_READY',92500000,20600000,93500000,19600000,'B.Cu',200000),
]
ENDPOINTS = [[92900000,18350000],[92500000,20600000]]


def validate_plan(plan):
    entry = plan.get('permission_lead_replacement')
    if entry is None:
        return Counter()
    assert entry['original_copper'] == list(map(list,COHORT)), 'Unreviewed permission replacement cohort'
    assert entry['endpoints_iu'] == ENDPOINTS and entry['boundary_contacts'], 'Permission boundary data missing'
    assert entry['replacement'] and sum(math.dist(row[2:4],row[4:6]) for row in entry['replacement']) <= 4000000
    for row in entry['replacement']:
        assert row[:2] == ['track','USB_RAW_LOGIC_READY'] and row[6:] == ['B.Cu',200000]
        assert all(92400000 <= row[i] <= 93600000 for i in (2,4)) and all(18300000 <= row[i] <= 20700000 for i in (3,5)), 'Permission detour outside local bounds'
    test = entry['testpad']
    assert test['reference'] == 'TP14' and test['net'] == 'ROW_ENABLE_N_CANDIDATE' and test['joined_pad'] == ['U54','3']
    assert test['connection'] and sum(math.dist(row[2:4],row[4:6]) for row in test['connection']) <= 5000000, 'TP14 lead exceeds 5 mm'
    for row in test['connection']:
        assert row[:2] == ['track',test['net']] and row[6:] == ['B.Cu',200000]
    assert not Counter(map(tuple,entry['replacement']+test['connection']))-Counter(map(tuple,plan['added_copper'])), 'Permission or probe lead missing'
    return Counter(COHORT)


def verify_native(old,new,plan,signature,physical_identity):
    import pcbnew as p
    entry = plan.get('permission_lead_replacement')
    if entry is None:
        return None
    validate_plan(plan)
    removed_ids = {t.m_Uuid.AsString() for t in old.GetTracks() if signature(old,t) in COHORT}
    boundary = {}
    for row in COHORT:
        t = next(t for t in old.GetTracks() if signature(old,t) == row)
        for key,item in contacts(old,t,signature,physical_identity):
            if item.m_Uuid.AsString() not in removed_ids:
                boundary[item.m_Uuid.AsString()] = (key,item)
    assert sorted((key for key,item in boundary.values()),key=repr) == sorted(entry['boundary_contacts'],key=repr), 'Permission boundary inventory differs'
    items = {item.m_Uuid.AsString():item for item in list(new.GetTracks())+[q for f in new.GetFootprints() for q in f.Pads()]}
    wanted = Counter(map(tuple,entry['replacement'])); replacement = []
    for t in new.GetTracks():
        key = signature(new,t)
        if wanted[key]:
            replacement.append(t); wanted[key] -= 1
    assert not +wanted and replacement, 'Permission replacement missing'
    for point in ENDPOINTS:
        assert any(t.GetEffectiveShape(p.B_Cu).Collide(p.SHAPE_CIRCLE(p.VECTOR2I(*point),1),0) for t in replacement), 'Permission outer endpoint lost'
    for uid,(key,item) in boundary.items():
        assert uid in items, 'Permission boundary copper missing'
        actual = items[uid]
        now = ['pad',*physical_identity(actual)] if isinstance(actual,p.PAD) else ['copper',*signature(new,actual)]
        assert now == key and actual.IsOnLayer(p.B_Cu), 'Permission boundary identity/layer changed'
        assert any(t.GetEffectiveShape(p.B_Cu).Collide(actual.GetEffectiveShape(p.B_Cu),0) for t in replacement), 'Permission original contact lost'
    before = old.FindFootprintByReference('TP14'); after = new.FindFootprintByReference('TP14')
    a,z = list(before.Pads()),list(after.Pads()); assert len(a) == len(z) == 1
    a,z = a[0],z[0]
    assert before.GetFPIDAsString() == after.GetFPIDAsString() == 'rgb-badge-coupon:TestPoint_Pad_D1.0mm'
    assert before.GetLayer() == after.GetLayer() == p.B_Cu and before.GetOrientationDegrees() == after.GetOrientationDegrees()
    assert a.GetNumber() == z.GetNumber() == '1' and a.GetNetname() == z.GetNetname() == 'ROW_ENABLE_N_CANDIDATE'
    assert a.GetSize() == z.GetSize() == p.VECTOR2I(1000000,1000000) and a.GetShape() == z.GetShape() == p.PAD_SHAPE_CIRCLE
    cluster = lambda board,q:frozenset(t.m_Uuid.AsString() for t in board.GetConnectivity().GetConnectedItems(q) if isinstance(t,p.PAD))
    assert len(cluster(old,a)) == 1, 'TP14 previously connected'
    previous = plan['previous_checkpoint']['pad_groups']
    assert next(group for group in previous if a.m_Uuid.AsString() in group) == [a.m_Uuid.AsString()], 'TP14 previous checkpoint not isolated'
    # Parent copper plus the selected successor is a superset of all preceding
    # 39-open copper. This also tests the previous additions, not only the parent.
    shape,box = a.GetEffectiveShape(p.B_Cu),a.GetBoundingBox()
    for board in (old,new):
        for t in board.GetTracks():
            if isinstance(t,p.PCB_TRACK) and not isinstance(t,p.PCB_VIA) and t.GetStart() == t.GetEnd():
                continue
            if t.IsOnLayer(p.B_Cu) and box.Intersects(t.GetBoundingBox()):
                assert not shape.Collide(t.GetEffectiveShape(p.B_Cu),0), 'TP14 prior copper-contact proof failed'
    target = next(q for q in new.FindFootprintByReference('U54').Pads() if q.GetNumber() == '3')
    assert cluster(new,z) == cluster(new,target) and len(cluster(new,z)) > 1, 'TP14 numbered output join missing'
    return {'boundary_contact_count':len(boundary), 'both_outer_endpoints_retained':True,
        'all_original_bcu_contacts_retained':True, 'tp14_previous_isolation_and_no_copper_contact':True,
        'tp14_joined_pad':['U54','3'], 'tp14_lead_length_mm':sum(math.dist(row[2:4],row[4:6]) for row in entry['testpad']['connection'])/1e6}
