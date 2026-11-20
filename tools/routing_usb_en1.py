# SPDX-License-Identifier: Apache-2.0
"""Exact ADR 0121 USB-control placement/leaf policy, separate from qualification."""
from collections import Counter
import hashlib
import json
import math
from pathlib import Path
import runpy

ROOT=Path(__file__).resolve().parents[1]
PARENT=ROOT/'hardware/coupon/rev-a/staging/led-rse-corrected-routing-trial-114mm.kicad_pcb'
PARENT_SHA='3967bb66e89e0005f6859ce78a766b4536d06883b76fce130e75a6fdeefaf96e'
OUTPUT=ROOT/'hardware/coupon/rev-a/staging/led-usb-en1-routing-trial-114mm.kicad_pcb'
PLAN=ROOT/'mechanical/review/usb-en1-routing-plan.json'
PLAN_SHA='eabb8b1caa163d206ca93dfc3e6b5163709fd667e1a16421c905c06feda01ac6'
RETIRED={'8c491cd1-dd01-5b1a-9d4e-340b2b65fe19','9ced2287-042b-5ca1-9293-c90554a352a8','4e80acb9-3235-5100-af33-030e33569108'}


def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()


def helper():return runpy.run_path(str(ROOT/'tools/check-routing-progress-trial.py'))


def load_plan():
    assert sha(PARENT)==PARENT_SHA and sha(PLAN)==PLAN_SHA, 'Frozen USB-control source/plan changed'
    plan=json.loads(PLAN.read_text())
    assert plan['source_sha256']==PARENT_SHA and plan['fabrication_release_allowed'] is False
    return plan


def contact_catalog(board):
    """Re-derive contacts on every actual layer; never use only a via's pointer."""
    import pcbnew as p
    signature=helper()['signature']
    items={t.m_Uuid.AsString():t for t in board.GetTracks()}
    allitems=list(items.values())+[q for f in board.GetFootprints() for q in f.Pads()]
    result={}
    for uid in sorted(RETIRED):
        original=items[uid];by_layer={}
        for layer in board.GetEnabledLayers().CuStack():
            if not original.IsOnLayer(layer):continue
            shape=original.GetEffectiveShape(layer);contacts=[]
            for item in allitems:
                if item.m_Uuid.AsString()==uid or item.GetNetCode()!=original.GetNetCode() or not item.IsOnLayer(layer):continue
                if not shape.Collide(item.GetEffectiveShape(layer),0):continue
                row=dict(uuid=item.m_Uuid.AsString())
                if isinstance(item,p.PAD):row.update(pad=[item.GetParentFootprint().GetReference(),item.GetNumber()])
                else:row.update(signature=list(signature(board,item)))
                contacts.append(row)
            zones=[]
            for zone in board.Zones():
                if zone.GetNetCode()!=original.GetNetCode() or zone.GetLayer()!=layer:continue
                filled=zone.GetFilledPolysList(layer)
                for index in range(filled.OutlineCount()):
                    if filled.UnitSet(index).Collide(shape,0):zones.append(dict(uuid=zone.m_Uuid.AsString(),polygon=index))
            by_layer[board.GetLayerName(layer)]={'copper_and_pads':sorted(contacts,key=lambda r:r['uuid']),'filled_polygons':zones}
        result[uid]=by_layer
    return result


def connectivity(old,new):
    import pcbnew as p
    def pads(b):return {q.m_Uuid.AsString():q for f in b.GetFootprints() for q in f.Pads() if q.GetNetname()}
    def group(b,q):return frozenset(z.m_Uuid.AsString() for z in b.GetConnectivity().GetConnectedItems(q) if isinstance(z,p.PAD))
    aa,bb=pads(old),pads(new)
    assert aa.keys()==bb.keys(), 'Live pad inventory changed'
    source_groups={group(old,q):key for key,q in aa.items()}
    assert len(source_groups)==223
    for members,key in source_groups.items():
        assert members<=group(new,bb[key]), 'Prior live group lost: '+aa[key].GetNetname()
    def pad(b,ref,number):return next(q for q in b.FindFootprintByReference(ref).Pads() if q.GetNumber()==number)
    source_supply=group(old,pad(old,'R70','1'))
    assert len(source_supply)==32 and pad(old,'U23','5').m_Uuid.AsString() in source_supply
    assert group(new,pad(new,'R70','1'))==source_supply, 'Original complete USB supply group differs'
    target={pad(new,ref,number).m_Uuid.AsString() for ref,number in [('R70','2'),('TP31','1'),('U23','4')]}
    assert group(new,pad(new,'U23','4'))==frozenset(target), 'EN1 target node not fully joined'
    groups={group(new,q) for q in bb.values()}
    nets={q.GetNetname() for q in bb.values()}
    native=new.GetConnectivity().GetUnconnectedCount(False)
    physical=len(groups)-len(nets)
    assert native==physical==34 and len(groups)==222 and len(nets)==188
    return dict(native_opens=native,physical_opens=physical,prior_groups_preserved=223,
                physical_groups=222,net_count=188,complete_usb_supply_group_size=32)


def audit(path,plan=None):
    import pcbnew as p
    plan=load_plan() if plan is None else plan
    assert sha(PARENT)==PARENT_SHA
    c=helper();old,new=(p.LoadBoard(str(q)) for q in (PARENT,path))
    old.BuildConnectivity();new.BuildConnectivity()
    parts={f.GetReference():f for f in old.GetFootprints()}
    actual={f.GetReference():f for f in new.GetFootprints()}
    assert parts.keys()==actual.keys() and len(parts)==483
    assert set(plan['poses'])=={'R70','TP31'}
    for ref,f in parts.items():
        other=actual[ref]
        assert f.m_Uuid.AsString()==other.m_Uuid.AsString()
        assert (f.GetValue(),f.GetFPIDAsString(),f.GetLayer())==(other.GetValue(),other.GetFPIDAsString(),other.GetLayer()), 'Part identity changed: '+ref
        assert Counter(c['local_pad_signature'](q) for q in f.Pads())==Counter(c['local_pad_signature'](q) for q in other.Pads()), 'Local land/net changed: '+ref
        assert sorted((q.GetName(),q.GetText()) for q in f.GetFields())==sorted((q.GetName(),q.GetText()) for q in other.GetFields()), 'Part fields changed: '+ref
        pose=plan['poses'].get(ref)
        if pose:
            assert [f.GetPosition().x,f.GetPosition().y]==pose['old_position_iu'] and f.GetOrientation().AsDegrees()%360==pose['old_angle_deg']%360
            position,angle=pose['position_iu'],pose['angle_deg']
        else:position,angle=[f.GetPosition().x,f.GetPosition().y],f.GetOrientation().AsDegrees()
        assert [other.GetPosition().x,other.GetPosition().y]==position and other.GetOrientation().AsDegrees()%360==angle%360, 'Pose differs: '+ref
    assert actual['R70'].GetField('MPN').GetText()=='ERJ2RKF1002X'
    assert plan['poses']['R70']['position_iu']==[10550000,6500000] and plan['poses']['R70']['angle_deg']%360==270
    assert plan['poses']['TP31']['position_iu']==[11900000,7750000] and plan['poses']['TP31']['angle_deg']%360==180
    geometry=runpy.run_path(str(ROOT/'tools/screen-converter-inductor-locality.py'))
    for ref in ['R70','TP31']:
        for poly in geometry['courtyards'](actual[ref]):
            for other in actual.values():
                if other.GetReference()==ref or other.GetLayer()!=p.B_Cu:continue
                assert all(not geometry['geometry'].intersects(poly,q) for q in geometry['courtyards'](other)), 'Moved courtyard intersects '+other.GetReference()
    structure=runpy.run_path(str(ROOT/'tools/check-routing-progress-plan.py'))['immutable_board_structure']
    assert structure(PARENT)==structure(path), 'Board, net, rule or zone structure changed'
    for ext in ['.kicad_pro','.kicad_dru']:
        assert PARENT.with_suffix(ext).read_bytes()==path.with_suffix(ext).read_bytes(), 'Profile changed'
    before={t.m_Uuid.AsString():t for t in old.GetTracks()}
    after={t.m_Uuid.AsString():t for t in new.GetTracks()}
    assert before.keys()-after.keys()==RETIRED, 'Unreviewed source retirement'
    for uid,t in before.items():
        if uid not in RETIRED:assert c['signature'](old,t)==c['signature'](new,after[uid]), 'Retained copper changed'
    rse=json.loads((ROOT/'mechanical/review/rse-pin-migration-plan.json').read_text())
    assert not RETIRED&{r['uuid'] for r in rse['added_copper']}, 'Accepted RSE addition retired'
    retired=[dict(uuid=uid,signature=list(c['signature'](old,before[uid]))) for uid in sorted(RETIRED)]
    assert retired==plan['retired_copper']
    assert contact_catalog(old)==plan['original_contacts'], 'Original contact proof differs'
    added=[]
    for uid in sorted(after.keys()-before.keys()):
        t=after[uid]
        assert not isinstance(t,p.PCB_VIA), 'New via forbidden'
        assert t.GetLayer()==p.B_Cu and t.GetWidth()==200000 and t.GetStart()!=t.GetEnd(), 'Nonordinary added copper'
        assert t.GetNetname() in {'+3V3_USB','USB_EN1_RAW_N'}
        added.append(dict(uuid=uid,signature=list(c['signature'](new,t))))
    assert added==plan['added_copper'] and len(added)==11
    result=connectivity(old,new)
    assert {r['role'] for r in plan['branches']}=={'supply','output','test'} and len(plan['branches'])==3
    required={'supply':('R70','1','U23','5','+3V3_USB'),
              'output':('R70','2','U23','4','USB_EN1_RAW_N'),
              'test':('R70','2','TP31','1','USB_EN1_RAW_N')}
    branch_copper=Counter();lengths={}
    for row in plan['branches']:
        a,n,z,k,net=required[row['role']]
        assert row['start']==[a,n] and row['end']==[z,k] and row['net']==net
        first=next(q for q in actual[a].Pads() if q.GetNumber()==n)
        last=next(q for q in actual[z].Pads() if q.GetNumber()==k)
        points=row['points_iu']
        assert points[0]==[first.GetPosition().x,first.GetPosition().y] and points[-1]==[last.GetPosition().x,last.GetPosition().y], 'Branch misses actual native terminal'
        assert first.GetNetname()==last.GetNetname()==net
        length=sum(math.dist(a,z) for a,z in zip(points,points[1:]))/1e6
        assert length<=16 and all(type(v) is int for pt in points for v in pt)
        lengths[row['role']]=length
        for (x,y),(a,z) in zip(points,points[1:]):
            branch_copper[('track',net,x,y,a,z,'B.Cu',200000)]+=1
    assert branch_copper==Counter(tuple(r['signature']) for r in added), 'Branch/copper ledger differs'
    result.update(branch_lengths_mm=lengths,retirements=3,additions=11,new_vias=0,
                  all_other_copper_parts_and_structure_preserved=True,fabrication_release_allowed=False)
    return old,new,result


def check_drc(path):
    baseline=json.loads((ROOT/'docs/development/remaining-routing-drc-2026-11-07.json').read_text())
    actual=json.loads(path.read_text())
    def key(v):
        v=dict(v);v['items']=sorted(v['items'],key=lambda r:r['uuid'])
        return json.dumps(v,sort_keys=True)
    assert len(actual['violations'])==len(baseline['violations'])==104
    assert Counter(map(key,actual['violations']))==Counter(map(key,baseline['violations'])), 'Exact original DRC findings differ'
    assert actual['ignored_checks']==baseline['ignored_checks'] and actual['included_severities']==baseline['included_severities']
