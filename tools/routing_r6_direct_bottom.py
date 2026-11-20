# SPDX-License-Identifier: Apache-2.0
"""Exact R6 direct bottom continuation. CAD continuity only."""
import json,runpy,copy,tempfile
from pathlib import Path
from collections import Counter
from decimal import Decimal
from routing_pair01_front_ground import sha,serialized_copper,components,contact_catalog,hole_audit,helper,PROFILES
ROOT=Path(__file__).resolve().parents[1]
PARENT=ROOT/'hardware/coupon/rev-a/staging/led-pair01-front-ground-trial-114mm.kicad_pcb'
PARENT_SHA='ec0bf7fc842f3dd4f9210e7667925cffc388d3d82906e44c5bde4e10f428ee88'
OUTPUT=ROOT/'hardware/coupon/rev-a/staging/led-r6-direct-bottom-trial-114mm.kicad_pcb'
PLAN=ROOT/'mechanical/review/r6-direct-bottom-plan.json'
BOARD_SHA='230b0c9f456837a0dd1b5e432497aa5223da95334ac2909ff8cd39d2edea804a'
PLAN_SHA='20576fa6cb0bf253c34cc17a86c1b8d521b01a7762c2c550358fd7e6cb72277b'
def load_plan():
 assert sha(PARENT)==PARENT_SHA and sha(PLAN)==PLAN_SHA,'Frozen source/plan changed'
 plan=json.loads(PLAN.read_text());assert plan['source_sha256']==PARENT_SHA and plan['expected_board_sha256']==BOARD_SHA and plan['fabrication_release_allowed'] is False and plan['selected'] is False
 return plan

def serialized_ledger(path,plan):
 old,new=serialized_copper(PARENT),serialized_copper(path);retired={r['uuid'] for r in plan['retired_copper']};added={r['uuid']:r for r in plan['added_copper']}
 assert old.keys()-new.keys()==retired and new.keys()-old.keys()==added.keys(),'Serialized Cu inventory differs'
 for uid in old.keys()&new.keys():assert old[uid]==new[uid],'Serialized source Cu changed: '+uid
 def iu(v):
  n=Decimal(v)*1000000;assert n==n.to_integral_value();return int(n)
 for uid,row in added.items():
  node=new[uid];attrs={v[0]:v[1:] for v in node[1:] if isinstance(v,list)};s=row['signature']
  if s[0]=='track':
   assert node[0]=='segment' and len(node)==7 and set(attrs)=={'start','end','width','layer','net','uuid'}
   actual=['track',attrs['net'][0],*map(iu,attrs['start']),*map(iu,attrs['end']),attrs['layer'][0],iu(attrs['width'][0])]
  else:
   assert node[:2]==['via','micro' if row['via_type']==1 else 'buried'] and len(node)==8 and set(attrs)=={'at','size','drill','layers','net','uuid'}
   actual=['via',attrs['net'][0],*map(iu,attrs['at']),*attrs['layers'],iu(attrs['size'][0]),iu(attrs['drill'][0])]
  assert actual==s,'Serialized new Cu differs: '+uid

def connectivity(old,new,plan=None):
 import pcbnew as p
 plan=load_plan() if plan is None else plan;aa,original,oa=components(old);bb,current,na=components(new);assert aa.keys()==bb.keys() and len(original)==213
 retired={r['uuid'] for r in plan['retired_copper']};added={r['uuid'] for r in plan['added_copper']};lookup={uid:(g,cu) for g,(_,cu) in current.items() for uid in g}
 for g,(uid,cu) in original.items():
  ng,nc=lookup[uid];assert g<=ng,'Original group split: '+aa[uid].GetNetname();assert cu-retired<=nc,'Retained attached Cu lost'
 assert retired<=oa and added<=na and len(list(new.GetTracks()))==len(na),'Orphan Cu'
 def group(ref,n):
  q=next(q for q in new.FindFootprintByReference(ref).Pads() if q.GetNumber()==n);return lookup[q.m_Uuid.AsString()][0]
 assert len(group('C71','2'))==197 and next(q for q in new.FindFootprintByReference('PAIR01').Pads() if q.GetNumber()=='1').m_Uuid.AsString() in group('C71','2')
 assert len(group('R18','1'))==37 and next(q for q in new.FindFootprintByReference('R6').Pads() if q.GetNumber()=='1').m_Uuid.AsString() in group('R18','1')
 for ref,n,count in [('PAIR01','3',18),('PAIR01','2',3),('PAIR01','5',4),('PAIR01','4',1),('R6','2',4)]:assert len(group(ref,n))==count,(ref,n,count)
 nets=len({q.GetNetname() for q in bb.values()});native=new.GetConnectivity().GetUnconnectedCount(False);assert native==len(current)-nets==24 and nets==188 and len(current)==212
 return dict(native_opens=native,physical_opens=24,physical_groups=212,prior_groups_preserved=213,net_count=188,main_ground_pads=197,main_vled_pads=37,orphan_copper=0,retained_attached_source_copper=len(oa-retired))

def bottom_courtyards(board):
 import pcbnew as p
 geometry=runpy.run_path(str(ROOT/'tools/screen-converter-inductor-locality.py'))['geometry']
 def polygons(fp):
  fp.BuildCourtyardCaches();poly=fp.GetCourtyard(p.B_CrtYd);assert poly.OutlineCount()==1 and poly.HoleCount(0)==0,'Missing bottom courtyard: '+fp.GetReference();ch=poly.COutline(0);points=[tuple(ch.CPoint(i)) for i in range(ch.PointCount())];assert geometry.convex(points);return points
 target=board.FindFootprintByReference('R6');assert target.GetLayer()==p.B_Cu;own=polygons(target);others=[fp for fp in board.GetFootprints() if fp.GetLayer()==p.B_Cu and fp.GetReference()!='R6'];assert len(others)==223
 for fp in others:assert not geometry.intersects(own,polygons(fp)),'Bottom courtyard collision: '+fp.GetReference()
 return dict(checked_bottom_courtyards=224,overlaps=0,missing=0)

def audit(path,plan=None):
 import pcbnew as p
 plan=load_plan() if plan is None else plan;assert plan==load_plan();serialized_ledger(path,plan);old,new=(p.LoadBoard(str(x)) for x in (PARENT,path));h=helper();aa={fp.GetReference():fp for fp in old.GetFootprints()};bb={fp.GetReference():fp for fp in new.GetFootprints()};assert aa.keys()==bb.keys() and len(aa)==len(list(old.GetFootprints()))==len(list(new.GetFootprints()))==483
 assert plan['poses']=={'R6':dict(position_iu=[77750000,5600000],orientation_degrees=90,layer='B.Cu')};held=[]
 for ref,a in aa.items():
  z=bb[ref];assert (a.m_Uuid.AsString(),a.GetFPIDAsString(),a.GetValue(),sorted((v.GetName(),v.GetText(),v.m_Uuid.AsString()) for v in a.GetFields()))==(z.m_Uuid.AsString(),z.GetFPIDAsString(),z.GetValue(),sorted((v.GetName(),v.GetText(),v.m_Uuid.AsString()) for v in z.GetFields())),'Part identity changed: '+ref
  expected=a
  if ref=='R6':
   expected=p.FOOTPRINT(a);held.append(expected);expected.SetOrientationDegrees(90);expected.SetPosition(p.VECTOR2I(77750000,5600000));assert a.GetLayer()==z.GetLayer()==p.B_Cu
  assert (expected.GetLayer(),list(expected.GetPosition()),expected.GetOrientationDegrees()%360)==(z.GetLayer(),list(z.GetPosition()),z.GetOrientationDegrees()%360),'Part pose changed: '+ref
  assert sorted(h['local_pad_signature'](q) for q in expected.Pads())==sorted(h['local_pad_signature'](q) for q in z.Pads()),'Package/pin changed: '+ref
  ap={q.m_Uuid.AsString():q for q in a.Pads()};zp={q.m_Uuid.AsString():q for q in z.Pads()};assert ap.keys()==zp.keys()
  for uid,q in ap.items():
   x,y=q.GetPosition();assert list(zp[uid].GetPosition())==([86500000-y,x-51650000] if ref=='R6' else [x,y]),'Independent absolute pin transform failed'
 structure=runpy.run_path(str(ROOT/'tools/check-routing-progress-plan.py'))['immutable_board_structure'];assert structure(PARENT)==structure(path),'Board structure changed'
 for ext,digest in PROFILES.items():assert sha(Path(path).with_suffix(ext))==digest and PARENT.with_suffix(ext).read_bytes()==Path(path).with_suffix(ext).read_bytes()
 ot={t.m_Uuid.AsString():t for t in old.GetTracks()};nt={t.m_Uuid.AsString():t for t in new.GetTracks()};retired={r['uuid'] for r in plan['retired_copper']};added={r['uuid']:r for r in plan['added_copper']};assert len(ot)==19380 and len(nt)==19384 and len(retired)==6 and len(added)==10 and ot.keys()-nt.keys()==retired and nt.keys()-ot.keys()==added.keys()
 for row in plan['retired_copper']:
  t=ot[row['uuid']];assert list(h['signature'](old,t))==row['signature'] and (int(t.GetViaType()) if isinstance(t,p.PCB_VIA) else None)==row['via_type']
 for uid in ot.keys()&nt.keys():
  assert h['signature'](old,ot[uid])==h['signature'](new,nt[uid])
  if isinstance(ot[uid],p.PCB_VIA):assert ot[uid].GetViaType()==nt[uid].GetViaType()
 for uid,row in added.items():
  t=nt[uid];assert list(h['signature'](new,t))==row['signature'] and (int(t.GetViaType()) if isinstance(t,p.PCB_VIA) else None)==row['via_type']
  if isinstance(t,p.PCB_VIA):
   span=(t.TopLayer(),t.BottomLayer())
   if span==(p.In2_Cu,p.In3_Cu):assert t.GetViaType()==p.VIATYPE_BURIED and t.GetWidth(t.TopLayer())==500000 and t.GetDrillValue()==300000
   else:assert span in [(p.F_Cu,p.In1_Cu),(p.In1_Cu,p.In2_Cu),(p.In3_Cu,p.In4_Cu),(p.In4_Cu,p.B_Cu)] and t.GetViaType()==p.VIATYPE_MICROVIA and t.GetWidth(t.TopLayer())==300000 and t.GetDrillValue()==100000
  else:assert t.GetWidth()==200000 and t.GetLayer() in [p.B_Cu,p.In2_Cu,p.In3_Cu]
 assert contact_catalog(old,retired)==plan['source_retirement_contacts'],'Source contact catalog changed'
 assert next(v.GetText() for v in bb['R6'].GetFields() if v.GetName()=='MPN')=='ERJ2RKF1001X'
 result=connectivity(old,new,plan);result.update(external_contacts=external_contacts(old,new,plan),bottom_courtyards=bottom_courtyards(new),hole_audit=hole_audit(new,added),exact_part_inventory=483,retired_copper=6,added_copper=10,unchanged_source_copper=19374,fabrication_release_allowed=False);return result

from routing_pair01_front_ground import check_drc

def external_contacts(old,new,plan):
 import pcbnew as p
 nt={t.m_Uuid.AsString():t for t in new.GetTracks()}
 def pad(board,ref,n):return next(q for q in board.FindFootprintByReference(ref).Pads() if q.GetNumber()==n)
 original=pad(old,'PAIR02','4');assert original.m_Uuid.AsString()==plan['supply_source_pad_uuid'] and list(original.GetPosition())==[78825000,6650000]
 originalgroup=frozenset(q.m_Uuid.AsString() for q in old.GetConnectivity().GetConnectedItems(original) if isinstance(q,p.PAD));assert len(originalgroup)==37 and pad(old,'R6','1').m_Uuid.AsString() in originalgroup
 power=next(nt[r['uuid']] for r in plan['added_copper'] if r['signature'][0]=='track' and r['signature'][1]=='VLED' and r['signature'][6]=='B.Cu');gate=next(nt[r['uuid']] for r in plan['added_copper'] if r['signature'][0]=='track' and r['signature'][1]=='ROW_GATE_00' and r['signature'][6]=='B.Cu')
 for q in [pad(new,'R6','1'),pad(new,'PAIR02','4')]:assert power.GetEffectiveShape(p.B_Cu).Collide(q.GetEffectiveShape(p.B_Cu),0),'Power endpoint lost'
 lower=next(nt[r['uuid']] for r in plan['added_copper'] if r['signature'][:4]==['via','ROW_GATE_00',76650000,4550000] and r['signature'][5]=='B.Cu');assert gate.GetEffectiveShape(p.B_Cu).Collide(lower.GetEffectiveShape(p.B_Cu),0) and gate.GetEffectiveShape(p.B_Cu).Collide(pad(new,'R6','2').GetEffectiveShape(p.B_Cu),0)
 powerlen=power.GetLength()/1e6;gatelen=sum(nt[r['uuid']].GetLength() for r in plan['added_copper'] if r['signature'][:2]==['track','ROW_GATE_00'])/1e6;assert abs(powerlen-plan['new_supply_length_mm'])<1e-10 and abs(gatelen-plan['new_gate_length_mm'])<1e-10
 stem=next(nt[r['uuid']] for r in plan['added_copper'] if r['signature'][:2]==['track','VLED'] and r['signature'][6]=='In2.Cu');assert stem.GetEffectiveShape(p.In2_Cu).Collide(nt['607bd79b-bb37-5fc4-8a76-ed1e127f247c'].GetEffectiveShape(p.In2_Cu),0),'Mandatory original stem junction lost'
 return dict(supply_source_pad_uuid=original.m_Uuid.AsString(),new_supply_length_mm=powerlen,new_gate_length_mm=gatelen,mandatory_stem_junction_preserved=True)
