# SPDX-License-Identifier: Apache-2.0
"""Exact bypass/enable migration ledger; CAD continuity only."""
from collections import Counter
import copy
import hashlib
import json
from pathlib import Path
import runpy
ROOT=Path(__file__).resolve().parents[1]
PARENT=ROOT/'hardware/coupon/rev-a/staging/led-ordinary-routing-trial-114mm.kicad_pcb'
PARENT_SHA='4b14dd289f0f9908d9c9f2339a37bb29896bec00ba805e2c6742a52eb241cb2c'
OUTPUT=ROOT/'hardware/coupon/rev-a/staging/led-enable-routing-trial-114mm.kicad_pcb'
PLAN=ROOT/'mechanical/review/enable-routing-plan.json'
PLAN_SHA='bf6e2c902e2cdb0d0a3dd6aedbe309200a01b22a6d6b9a7b45ff9ec81c0c433f'
BOARD_SHA='90db778d8e44b2c71ab5e1f5d8a1c586ee71c25d46892b1406c4792ac7720abd'
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
 aa,bb=pads(old),pads(new);assert aa.keys()==bb.keys(),'Live pad inventory changed';groups={group(old,q):uid for uid,q in aa.items()};assert len(groups)==219
 for g,uid in groups.items():assert g<=group(new,bb[uid]),'Original group split: '+aa[uid].GetNetname()
 target=[q for fp in new.GetFootprints() for q in fp.Pads() if q.GetNetname()=='DISPLAY_ENABLE']
 assert len(target)>1 and group(new,target[0])==frozenset(q.m_Uuid.AsString() for q in target),'Full enable terminal group disconnected'
 native=new.GetConnectivity().GetUnconnectedCount(False);physical=len({group(new,q) for q in bb.values()})-len({q.GetNetname() for q in bb.values()});assert native==physical==30
 return dict(native_opens=native,physical_opens=physical,prior_groups_preserved=219,physical_groups=218,net_count=188)

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
 assert set(plan['poses'])=={'C71'}
 for ref,a in aa.items():
  b=bb[ref];assert (a.m_Uuid.AsString(),a.GetFPIDAsString(),a.GetValue(),a.GetLayer(),sorted((x.GetName(),x.GetText()) for x in a.GetFields()))==(b.m_Uuid.AsString(),b.GetFPIDAsString(),b.GetValue(),b.GetLayer(),sorted((x.GetName(),x.GetText()) for x in b.GetFields())),'Part identity/fields changed: '+ref
  assert sorted(h['local_pad_signature'](x) for x in a.Pads())==sorted(h['local_pad_signature'](x) for x in b.Pads()),'Local pads changed: '+ref
  pose=plan['poses'].get(ref,dict(position_iu=list(a.GetPosition()),orientation_degrees=a.GetOrientation().AsDegrees()%360));assert (list(b.GetPosition()),b.GetOrientation().AsDegrees()%360)==(pose['position_iu'],pose['orientation_degrees']),'Part pose changed: '+ref
  ap={x.m_Uuid.AsString():x for x in a.Pads()};bp={x.m_Uuid.AsString():x for x in b.Pads()};assert ap.keys()==bp.keys()
  for uid,q in ap.items():
   x,y=q.GetPosition();expected=[x-500000,y] if ref=='C71' else [x,y];assert list(bp[uid].GetPosition())==expected,'Independent pad transform failed'
 assert runpy.run_path(str(ROOT/'tools/check-routing-progress-plan.py'))['immutable_board_structure'](PARENT)==runpy.run_path(str(ROOT/'tools/check-routing-progress-plan.py'))['immutable_board_structure'](path),'Board/net/zone/setup structure changed'
 for ext in ['.kicad_pro','.kicad_dru']:assert PARENT.with_suffix(ext).read_bytes()==Path(path).with_suffix(ext).read_bytes(),'Profile/rules changed'
 ot={t.m_Uuid.AsString():t for t in old.GetTracks()};nt={t.m_Uuid.AsString():t for t in new.GetTracks()};retired={r['uuid'] for r in plan['retired_copper']};assert ot.keys()-nt.keys()==retired and len(retired)==2,'Source retirement differs'
 for row in plan['retired_copper']:assert list(h['signature'](old,ot[row['uuid']]))==row['signature']
 for uid,t in ot.items():
  if uid in retired:continue
  assert h['signature'](old,t)==h['signature'](new,nt[uid]),'Retained source copper changed: '+uid
  if isinstance(t,p.PCB_VIA):assert t.GetViaType()==nt[uid].GetViaType(),'Original via type changed'
 added={r['uuid']:r for r in plan['added_copper']};assert nt.keys()-ot.keys()==added.keys() and len(added)==len(plan['added_copper']),'Added inventory differs'
 for uid,row in added.items():
  t=nt[uid];assert list(h['signature'](new,t))==row['signature'],'Added copper geometry changed'
  assert (int(t.GetViaType()) if isinstance(t,p.PCB_VIA) else None)==row['via_type'],'Added via type changed'
 assert contact_catalog(old,retired)==plan['source_retirement_contacts'],'Original native contact catalog differs'
 result=connectivity(old,new);result.update(unchanged_source_copper=19281,added_copper=len(added),retired_copper=2,exact_part_inventory=483,unchanged_rules_profiles_structure=True)
 return result

def check_drc(path,board):
 from routing_control_cluster import check_drc as original
 return original(path,board)
