# SPDX-License-Identifier: Apache-2.0
"""Exact ordinary-width additive successor; no fabrication qualification."""
from collections import Counter
import hashlib
import json
from pathlib import Path
import runpy
ROOT=Path(__file__).resolve().parents[1]
PARENT=ROOT/'hardware/coupon/rev-a/staging/led-control-cluster-routing-trial-114mm.kicad_pcb'
PARENT_SHA='1d34fd1e29c8f65d22e7626cc0d2f0307be26b8d5255a0f6e16eb0eac46ceb6b'
OUTPUT=PARENT.with_name('led-ordinary-routing-trial-114mm.kicad_pcb')
PLAN=ROOT/'mechanical/review/ordinary-routing-plan.json'
PLAN_SHA='bff8addd38f04f3763afe8e5e135e364d2918ca82fe3fcd3ab89f3d1f5e587ec'
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def helper():return runpy.run_path(str(ROOT/'tools/check-routing-progress-trial.py'))
def load_plan():
    assert sha(PARENT)==PARENT_SHA and sha(PLAN)==PLAN_SHA,'Frozen ordinary source/plan changed'
    plan=json.loads(PLAN.read_text());assert plan['source_sha256']==PARENT_SHA and plan['fabrication_release_allowed'] is False
    return plan

def connectivity(old,new):
    import pcbnew as p
    def pads(b):return {q.m_Uuid.AsString():q for f in b.GetFootprints() for q in f.Pads() if q.GetNetname()}
    def group(b,q):return frozenset(z.m_Uuid.AsString() for z in b.GetConnectivity().GetConnectedItems(q) if isinstance(z,p.PAD))
    aa,bb=pads(old),pads(new);assert aa.keys()==bb.keys()
    original={group(old,q):key for key,q in aa.items()};assert len(original)==220
    for members,key in original.items():assert members<=group(new,bb[key]),'Original group split: '+aa[key].GetNetname()
    plan=load_plan()
    for name,expected in plan['expected_terminal_groups'].items():
        actual={tuple(sorted((bb[uid].GetParentFootprint().GetReference(),bb[uid].GetNumber()) for uid in group(new,q))) for q in bb.values() if q.GetNetname()==name}
        assert actual=={tuple(tuple(x) for x in g) for g in expected},'Expected terminal join differs: '+name
    current={group(new,q) for q in bb.values()};nets={q.GetNetname() for q in bb.values()}
    native=new.GetConnectivity().GetUnconnectedCount(False);physical=len(current)-len(nets)
    assert native==physical==plan['native_opens']==plan['physical_opens'] and len(nets)==188
    return dict(native_opens=native,physical_opens=physical,prior_groups_preserved=220,physical_groups=len(current),net_count=188)

def contacts(old,new,added):
    import pcbnew as p
    before=list(old.GetTracks())+[q for f in old.GetFootprints() for q in f.Pads()]
    after={t.m_Uuid.AsString():t for t in new.GetTracks()};result=[]
    for uid in sorted(added):
        t=after[uid];box=t.GetBoundingBox()
        for o in before:
            if o.GetNetCode()!=t.GetNetCode() or not box.Intersects(o.GetBoundingBox()):continue
            for l in old.GetEnabledLayers().CuStack():
                if t.IsOnLayer(l) and o.IsOnLayer(l) and t.GetEffectiveShape(l).Collide(o.GetEffectiveShape(l),0):
                    result.append(dict(added_uuid=uid,source_uuid=o.m_Uuid.AsString(),layer=old.GetLayerName(l),pad=[o.GetParentFootprint().GetReference(),o.GetNumber()] if isinstance(o,p.PAD) else None))
    return sorted(result,key=lambda r:(r['added_uuid'],r['source_uuid'],r['layer']))

def audit(path,plan=None):
    import pcbnew as p
    plan=load_plan() if plan is None else plan;assert plan==load_plan() and sha(PARENT)==PARENT_SHA
    h=helper();old,new=(p.LoadBoard(str(q)) for q in (PARENT,path))
    def parts(b):
        return {f.GetReference():(f.m_Uuid.AsString(),f.GetFPIDAsString(),f.GetValue(),tuple(f.GetPosition()),f.GetOrientation().AsDegrees()%360,f.GetLayer(),tuple(sorted((v.GetName(),v.GetText()) for v in f.GetFields())),tuple(sorted(h['local_pad_signature'](q) for q in f.Pads()))) for f in b.GetFootprints()}
    assert parts(old)==parts(new) and len(parts(new))==483,'Part, pad, field, pose or net differs'
    structure=runpy.run_path(str(ROOT/'tools/check-routing-progress-plan.py'))['immutable_board_structure']
    assert structure(PARENT)==structure(path),'Board/net/rule/zone/outline structure differs'
    for ext in ['.kicad_pro','.kicad_dru']:assert PARENT.with_suffix(ext).read_bytes()==path.with_suffix(ext).read_bytes(),'Profile differs'
    before={t.m_Uuid.AsString():t for t in old.GetTracks()};after={t.m_Uuid.AsString():t for t in new.GetTracks()}
    assert before.keys()<=after.keys(),'Original source copper retired'
    for uid,t in before.items():
        assert h['signature'](old,t)==h['signature'](new,after[uid]),'Original source copper changed'
        if isinstance(t,p.PCB_VIA):assert t.GetViaType()==after[uid].GetViaType(),'Original via type changed'
    rows=[];length=0;via_counts=Counter()
    for uid in sorted(after.keys()-before.keys()):
        t=after[uid];s=list(h['signature'](new,t));assert t.GetNetname() in plan['allowed_nets'],'New net outside frozen scope'
        kind=None
        if isinstance(t,p.PCB_VIA):
            kind=int(t.GetViaType());span={new.GetLayerName(t.TopLayer()),new.GetLayerName(t.BottomLayer())}
            if span=={'In2.Cu','In3.Cu'}:assert kind==int(p.VIATYPE_BURIED) and s[-2:]==[500000,300000]
            else:
                stack=['F.Cu','In1.Cu','In2.Cu','In3.Cu','In4.Cu','B.Cu'];assert abs(stack.index(s[4])-stack.index(s[5]))==1
                assert kind==int(p.VIATYPE_MICROVIA) and s[-2:]==[300000,100000]
            via_counts[tuple(sorted(span))]+=1
        else:
            assert t.GetWidth()==200000 and t.GetStart()!=t.GetEnd(),'New track width/geometry differs'
            length+=t.GetLength()/1e6
        rows.append(dict(uuid=uid,signature=s,via_type=kind))
    assert rows==plan['added_copper'] and len(rows)==len(plan['added_copper']),'Exact additive ledger differs'
    assert contacts(old,new,after.keys()-before.keys())==plan['original_contacts'],'Original contact proof differs'
    result=connectivity(old,new);result.update(additions=len(rows),new_vias=sum(via_counts.values()),added_track_length_mm=length,source_copper_items_preserved=len(before))
    return result

def check_drc(path,board=PARENT):
    from routing_control_cluster import check_drc as check
    return check(path,board)
