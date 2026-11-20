# SPDX-License-Identifier: Apache-2.0
"""Exact gate/bypass migration ledger; CAD continuity, never fabrication approval."""
from collections import Counter
import copy
import hashlib
import json
from pathlib import Path
import runpy
ROOT=Path(__file__).resolve().parents[1]
PARENT=ROOT/'hardware/coupon/rev-a/staging/led-gauge-routing-trial-114mm.kicad_pcb'
PARENT_SHA='14f0c49582063bab84ea685a8cec798011eb4cd66389b085a3a47777180a13ce'
OUTPUT=ROOT/'hardware/coupon/rev-a/staging/led-control-cluster-routing-trial-114mm.kicad_pcb'
PLAN=ROOT/'mechanical/review/control-cluster-routing-plan.json'
PLAN_SHA='da1e14ec6a8f878954434e2bcfa9f1490aaf7e953110e613b53f09309efc75e0'
BOARD_SHA='1d34fd1e29c8f65d22e7626cc0d2f0307be26b8d5255a0f6e16eb0eac46ceb6b'
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def helper():return runpy.run_path(str(ROOT/'tools/check-routing-progress-trial.py'))
def load_plan():
 assert sha(PARENT)==PARENT_SHA and sha(PLAN)==PLAN_SHA,'Frozen source/plan changed'
 plan=json.loads(PLAN.read_text());assert plan['source_sha256']==PARENT_SHA and plan['expected_board_sha256']==BOARD_SHA and plan['fabrication_release_allowed'] is False
 return plan

def connectivity(old,new):
 import pcbnew as p
 def pads(b):return {q.m_Uuid.AsString():q for f in b.GetFootprints() for q in f.Pads() if q.GetNetname()}
 def group(b,q):return frozenset(z.m_Uuid.AsString() for z in b.GetConnectivity().GetConnectedItems(q) if isinstance(z,p.PAD))
 aa,bb=pads(old),pads(new);assert aa.keys()==bb.keys(),'Live pad inventory changed';groups={group(old,q):uid for uid,q in aa.items()};assert len(groups)==221
 for g,uid in groups.items():assert g<=group(new,bb[uid]),'Original group split: '+aa[uid].GetNetname()
 target=[next(q for q in new.FindFootprintByReference(ref).Pads() if q.GetNumber()==number) for ref,number in [('U51','4'),('U52','1')]]
 assert group(new,target[0])==group(new,target[1])==frozenset(q.m_Uuid.AsString() for q in target),'Exact CLEAR3 terminals disconnected'
 native=new.GetConnectivity().GetUnconnectedCount(False);physical=len({group(new,q) for q in bb.values()})-len({q.GetNetname() for q in bb.values()});assert native==physical==32
 return dict(native_opens=native,physical_opens=physical,prior_groups_preserved=221,physical_groups=220,net_count=188)

def contact_catalog(board,retired):
 import pcbnew as p
 signature=helper()['signature'];items={t.m_Uuid.AsString():t for t in board.GetTracks()};allitems=list(items.values())+[q for f in board.GetFootprints() for q in f.Pads()];result={}
 for uid in sorted(retired):
  original=items[uid];layers={}
  for layer in board.GetEnabledLayers().CuStack():
   if not original.IsOnLayer(layer):continue
   shape=original.GetEffectiveShape(layer);contacts=[]
   for item in allitems:
    if item.m_Uuid.AsString()==uid or item.GetNetCode()!=original.GetNetCode() or not item.IsOnLayer(layer) or not shape.Collide(item.GetEffectiveShape(layer),0):continue
    row=dict(uuid=item.m_Uuid.AsString())
    if isinstance(item,p.PAD):row['pad']=[item.GetParentFootprint().GetReference(),item.GetNumber()]
    else:row['signature']=list(signature(board,item))
    contacts.append(row)
   zones=[]
   for zone in board.Zones():
    if zone.GetNetCode()!=original.GetNetCode() or zone.GetLayer()!=layer:continue
    filled=zone.GetFilledPolysList(layer)
    for i in range(filled.OutlineCount()):
     if filled.UnitSet(i).Collide(shape,0):zones.append(dict(uuid=zone.m_Uuid.AsString(),polygon=i))
   layers[board.GetLayerName(layer)]=dict(copper_and_pads=sorted(contacts,key=lambda r:r['uuid']),filled_polygons=zones)
  result[uid]=layers
 return result

def audit(path,plan=None):
 import pcbnew as p
 plan=load_plan() if plan is None else plan
 assert plan==load_plan(),'Plan fields changed'
 old,new=(p.LoadBoard(str(q)) for q in (PARENT,path));h=helper();aa={f.GetReference():f for f in old.GetFootprints()};bb={f.GetReference():f for f in new.GetFootprints()};assert aa.keys()==bb.keys() and len(aa)==483
 assert set(plan['poses'])=={'U52','C71'}
 for ref,a in aa.items():
  b=bb[ref];assert (a.m_Uuid.AsString(),a.GetFPIDAsString(),a.GetValue(),a.GetLayer(),sorted((x.GetName(),x.GetText()) for x in a.GetFields()))==(b.m_Uuid.AsString(),b.GetFPIDAsString(),b.GetValue(),b.GetLayer(),sorted((x.GetName(),x.GetText()) for x in b.GetFields())),'Part identity/fields changed: '+ref
  assert sorted(h['local_pad_signature'](x) for x in a.Pads())==sorted(h['local_pad_signature'](x) for x in b.Pads()),'Local pads changed: '+ref
  pose=plan['poses'].get(ref,dict(position_iu=list(a.GetPosition()),orientation_degrees=a.GetOrientation().AsDegrees()%360));assert (list(b.GetPosition()),b.GetOrientation().AsDegrees()%360)==(pose['position_iu'],pose['orientation_degrees']),'Part pose changed: '+ref
  ap={x.m_Uuid.AsString():x for x in a.Pads()};bp={x.m_Uuid.AsString():x for x in b.Pads()};assert ap.keys()==bp.keys()
  for uid,q in ap.items():
   x,y=q.GetPosition();expected=[103200000-(y-1000000),5275000+(x-69250000)] if ref=='U52' else [103000000+(y-3295000),6750000-(x-68100000)] if ref=='C71' else [x,y];assert list(bp[uid].GetPosition())==expected,'Independent pad transform failed'
 assert runpy.run_path(str(ROOT/'tools/check-routing-progress-plan.py'))['immutable_board_structure'](PARENT)==runpy.run_path(str(ROOT/'tools/check-routing-progress-plan.py'))['immutable_board_structure'](path),'Board/net/zone/setup structure changed'
 for ext in ['.kicad_pro','.kicad_dru']:assert PARENT.with_suffix(ext).read_bytes()==Path(path).with_suffix(ext).read_bytes(),'Profile/rules changed'
 ot={t.m_Uuid.AsString():t for t in old.GetTracks()};nt={t.m_Uuid.AsString():t for t in new.GetTracks()};retired={r['uuid'] for r in plan['retired_copper']};assert ot.keys()-nt.keys()==retired and len(retired)==11,'Source retirement differs'
 for row in plan['retired_copper']:assert list(h['signature'](old,ot[row['uuid']]))==row['signature']
 for uid,t in ot.items():
  if uid in retired:continue
  assert h['signature'](old,t)==h['signature'](new,nt[uid]),'Retained source copper changed: '+uid
  if isinstance(t,p.PCB_VIA):assert t.GetViaType()==nt[uid].GetViaType(),'Original via type changed'
 added={r['uuid']:r for r in plan['added_copper']};assert nt.keys()-ot.keys()==added.keys() and len(added)==59,'Added inventory differs'
 for uid,row in added.items():
  t=nt[uid];assert list(h['signature'](new,t))==row['signature'],'Added copper geometry changed'
  assert (int(t.GetViaType()) if isinstance(t,p.PCB_VIA) else None)==row['via_type'],'Added via type changed'
 assert contact_catalog(old,retired)==plan['source_retirement_contacts'],'Original native contact catalog differs'
 result=connectivity(old,new);result.update(unchanged_source_copper=19167,added_copper=59,retired_copper=11,exact_part_inventory=483,unchanged_rules_profiles_structure=True)
 return result

def check_drc(path,board):
 import pcbnew as p
 baseline=json.loads((ROOT/'docs/development/remaining-routing-drc-2026-11-07.json').read_text());actual=json.loads(Path(path).read_text());normalized=copy.deepcopy(actual);old=p.LoadBoard(str(PARENT));new=p.LoadBoard(str(board));oldpads={q.m_Uuid.AsString():q for q in old.FindFootprintByReference('U52').Pads()};newpads={q.m_Uuid.AsString():q for q in new.FindFootprintByReference('U52').Pads()};count=0
 for v in normalized['violations']:
  for item in v['items']:
   uid=item['uuid']
   if uid in oldpads:
    x,y=oldpads[uid].GetPosition();expected=[103200000-(y-1000000),5275000+(x-69250000)];assert list(newpads[uid].GetPosition())==expected
    assert item['pos']==dict(zip(['x','y'],[n/1e6 for n in expected])),'Moved finding coordinate differs'
    item['pos']=dict(zip(['x','y'],[n/1e6 for n in oldpads[uid].GetPosition()]));count+=1
 key=lambda v:json.dumps(dict(v,items=sorted(v['items'],key=lambda x:x['uuid'])),sort_keys=True)
 assert len(actual['violations'])==len(baseline['violations'])==104 and count==8
 assert Counter(map(key,normalized['violations']))==Counter(map(key,baseline['violations'])),'Exact intrinsic finding payload differs'
 assert actual['ignored_checks']==baseline['ignored_checks'] and actual['included_severities']==baseline['included_severities'] and actual['schematic_parity']==baseline['schematic_parity'],'DRC check policy differs'
