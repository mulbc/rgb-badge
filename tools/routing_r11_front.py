# SPDX-License-Identifier: Apache-2.0
"""Exact front-side R11 local gate replacement; CAD continuity only."""
import json,runpy
from pathlib import Path
from routing_r21 import sha,serialized_copper,components,contact_catalog,hole_audit,check_drc,helper,PROFILES
ROOT=Path(__file__).resolve().parents[1]
PARENT=ROOT/'hardware/coupon/rev-a/staging/led-r21-routing-trial-114mm.kicad_pcb'
PARENT_SHA='e7748bee49f33b3b5c021c9215d441a047718b284e3a1ee27975e3832ddfb5d2'
OUTPUT=ROOT/'hardware/coupon/rev-a/staging/led-r11-front-routing-trial-114mm.kicad_pcb'
PLAN=ROOT/'mechanical/review/r11-front-routing-plan.json'
PLAN_SHA='a98428bc804458696a56c58145af0bf8b9b1e9563d7e453fe89c8f8167723c62'
BOARD_SHA='fb862c0a548599b7acf328ad8bb5006ce5f78d8b98ceec12bb4af9ace21f1d0f'
def load_plan():
 assert sha(PARENT)==PARENT_SHA and sha(PLAN)==PLAN_SHA,'Frozen source/plan changed'
 plan=json.loads(PLAN.read_text());assert plan['source_sha256']==PARENT_SHA and plan['expected_board_sha256']==BOARD_SHA and plan['fabrication_release_allowed'] is False
 for ext,digest in PROFILES.items():assert sha(PARENT.with_suffix(ext))==digest
 return plan
from decimal import Decimal
def serialized_ledger(path,plan):
 old,new=serialized_copper(PARENT),serialized_copper(path);retired={r['uuid'] for r in plan['retired_copper']};added={r['uuid']:r for r in plan['added_copper']}
 assert old.keys()-new.keys()==retired and new.keys()-old.keys()==added.keys(),'Serialized copper inventory differs'
 for uid in old.keys()&new.keys():assert old[uid]==new[uid],'Serialized source copper changed: '+uid
 def iu(value):
  v=Decimal(value)*1000000;assert v==v.to_integral_value(),'Sub-nanometre serialized coordinate';return int(v)
 for uid,row in added.items():
  node=new[uid];assert node[0]=='segment';attrs={v[0]:v[1:] for v in node[1:] if isinstance(v,list)}
  assert set(attrs)=={'start','end','width','layer','net','uuid'} and len(attrs)==len(node)-1,'Unexpected added copper attributes'
  signature=['track',attrs['net'][0],*map(iu,attrs['start']),*map(iu,attrs['end']),attrs['layer'][0],iu(attrs['width'][0])]
  assert signature==row['signature'],'Serialized added copper differs: '+uid


def connectivity(old,new):
 import pcbnew as p
 aa,original,oldattached=components(old);bb,current,newattached=components(new);assert aa.keys()==bb.keys() and len(original)==215
 plan=load_plan();retired={r['uuid'] for r in plan['retired_copper']};added={r['uuid'] for r in plan['added_copper']};lookup={uid:(g,cu) for g,(_,cu) in current.items() for uid in g}
 for g,(uid,cu) in original.items():
  now,newcu=lookup[uid];assert g<=now,'Original pad group split: '+aa[uid].GetNetname();assert cu-retired<=newcu,'Retained attached source copper orphaned'
 assert retired<=oldattached and added<=newattached and len(list(new.GetTracks()))==len(newattached),'Orphan copper or retirement'
 gate=[uid for uid,q in bb.items() if q.GetNetname()=='ROW_GATE_05'];assert len(gate)==4 and lookup[gate[0]][0]==frozenset(gate)
 def pad(ref,n):return next(q for q in new.FindFootprintByReference(ref).Pads() if q.GetNumber()==n)
 supply=lookup[pad('R18','1').m_Uuid.AsString()][0];ground=lookup[pad('C71','2').m_Uuid.AsString()][0]
 assert pad('R11','1').m_Uuid.AsString() in supply and len(supply)==37 and len(ground)==196
 native=new.GetConnectivity().GetUnconnectedCount(False);nets=len({q.GetNetname() for q in bb.values()});assert native==len(current)-nets==26 and len(current)==214 and nets==188
 return dict(native_opens=native,physical_opens=26,prior_groups_preserved=215,physical_groups=214,net_count=188,main_vled_pads=37,main_ground_pads=196,retained_attached_source_copper=len(oldattached-retired),original_orphan_copper=19381-len(oldattached),new_orphan_copper=19357-len(newattached))

def external_contacts(old,new,plan):
 import pcbnew as p
 ot={t.m_Uuid.AsString():t for t in old.GetTracks()};nt={t.m_Uuid.AsString():t for t in new.GetTracks()}
 def pad(board,ref,n):return next(q for q in board.FindFootprintByReference(ref).Pads() if q.GetNumber()==n)
 lead=nt[plan['added_copper'][0]['uuid']];outside={r['uuid']:r for ls in plan['source_retirement_contacts'].values() for v in ls.values() for r in v['copper_and_pads'] if r['uuid'] not in {r['uuid'] for r in plan['retired_copper']}}
 assert outside==plan['source_outside_interfaces'];assert {tuple(r['pad']) for r in outside.values() if 'pad' in r}=={('R11','2')}
 assert {uid for uid,r in outside.items() if 'signature' in r}=={'bdf3e2be-ec90-5848-83cf-76e3dfb7171f','88ac0e8a-2225-5b70-a89a-b8a5aac76824','af1c44e0-5935-5c37-8c11-ac9c67fce62b','1dd5131b-4d4a-52d1-b368-7b86a71a4244'}
 for uid,row in outside.items():
  target=pad(new,'R11','2') if 'pad' in row else nt[uid];assert lead.GetEffectiveShape(p.F_Cu).Collide(target.GetEffectiveShape(p.F_Cu),0),'Gate endpoint contact lost'
 assert all(not v['filled_polygons'] for ls in plan['source_retirement_contacts'].values() for v in ls.values())
 supply=pad(new,'R11','1');uid=plan['supply_source_uuid'];oldanchor=pad(old,'R18','1');oldmain=frozenset(o.m_Uuid.AsString() for o in old.GetConnectivity().GetConnectedItems(oldanchor) if isinstance(o,p.PAD));assert len(oldmain)==36
 assert frozenset(o.m_Uuid.AsString() for o in old.GetConnectivity().GetConnectedItems(ot[uid]) if isinstance(o,p.PAD))==oldmain
 assert supply.GetEffectiveShape(p.F_Cu).Collide(nt[uid].GetEffectiveShape(p.F_Cu),0) and plan['new_supply_copper_mm']==0
 assert abs(lead.GetLength()/1e6-plan['new_gate_length_mm'])<1e-10
 return dict(gate_outside_contacts=sorted(outside),retained_main_supply_contact=uid,new_supply_copper_mm=0,new_gate_length_mm=lead.GetLength()/1e6)

def front_courtyards(board):
 """Check the actual front side; the historical discovery helper is B-only."""
 import pcbnew as p
 geometry=runpy.run_path(str(ROOT/'tools/screen-converter-inductor-locality.py'))['geometry']
 def polygons(fp):
  fp.BuildCourtyardCaches();native=fp.GetCourtyard(p.F_CrtYd);result=[]
  for i in range(native.OutlineCount()):
   assert native.HoleCount(i)==0,'Unsupported front courtyard hole';chain=native.COutline(i);points=[(chain.CPoint(j).x,chain.CPoint(j).y) for j in range(chain.PointCount())];assert geometry.convex(points),'Unsupported front courtyard shape';result.append(points)
  return result
 target=board.FindFootprintByReference('R11');assert target.GetLayer()==p.F_Cu;own=polygons(target);assert len(own)==1,'R11 front courtyard missing'
 others=[fp for fp in board.GetFootprints() if fp.GetReference()!='R11' and fp.GetLayer()==p.F_Cu];assert len(others)==257
 count=0
 for fp in others:
  theirs=polygons(fp);assert len(theirs)==1,'Original front courtyard missing: '+fp.GetReference();count+=len(theirs)
  assert not any(geometry.intersects(a,z) for a in own for z in theirs),'Front courtyard overlap: '+fp.GetReference()
 return dict(r11_front_courtyards=1,other_front_footprints=257,other_front_courtyards=count,missing_front_courtyards=0,overlaps=0)

def audit(path,plan=None):
 import pcbnew as p
 plan=load_plan() if plan is None else plan;assert plan==load_plan(),'Plan changed';serialized_ledger(path,plan)
 old,new=(p.LoadBoard(str(q)) for q in (PARENT,path));h=helper();aa={f.GetReference():f for f in old.GetFootprints()};bb={f.GetReference():f for f in new.GetFootprints()};assert aa.keys()==bb.keys() and len(aa)==len(list(old.GetFootprints()))==len(list(new.GetFootprints()))==483
 assert plan['poses']=={'R11':{'position_iu':[78850000,9100000],'orientation_degrees':180,'layer':'F.Cu','flip':'top-bottom'}}
 assert next(v.GetText() for v in bb['R11'].GetFields() if v.GetName()=='MPN')=='ERJ2RKF1001X'
 references=[]
 for ref,a in aa.items():
  z=bb[ref];assert (a.m_Uuid.AsString(),a.GetFPIDAsString(),a.GetValue(),sorted((v.GetName(),v.GetText(),v.m_Uuid.AsString()) for v in a.GetFields()))==(z.m_Uuid.AsString(),z.GetFPIDAsString(),z.GetValue(),sorted((v.GetName(),v.GetText(),v.m_Uuid.AsString()) for v in z.GetFields())),'Part identity/fields changed: '+ref
  if ref=='R11':
   mirror=p.FOOTPRINT(a);mirror.Flip(mirror.GetPosition(),p.FLIP_DIRECTION_TOP_BOTTOM);references.append(mirror);assert z.GetLayer()==p.F_Cu and a.GetLayer()==p.B_Cu
   assert sorted(h['local_pad_signature'](q) for q in mirror.Pads())==sorted(h['local_pad_signature'](q) for q in z.Pads()),'Mirrored local package changed'
   assert list(z.GetPosition())==[78850000,9100000] and z.GetOrientationDegrees()%360==180
  else:
   assert (a.GetLayer(),list(a.GetPosition()),a.GetOrientationDegrees()%360)==(z.GetLayer(),list(z.GetPosition()),z.GetOrientationDegrees()%360),'Fixed pose changed: '+ref
   assert sorted(h['local_pad_signature'](q) for q in a.Pads())==sorted(h['local_pad_signature'](q) for q in z.Pads())
  ap={q.m_Uuid.AsString():q for q in a.Pads()};zp={q.m_Uuid.AsString():q for q in z.Pads()};assert ap.keys()==zp.keys() and len(ap)==len(list(a.Pads())) and len(zp)==len(list(z.Pads()))
  for uid,q in ap.items():
   x,y=q.GetPosition();assert list(zp[uid].GetPosition())==([x+6100000,13350000-y] if ref=='R11' else [x,y]),'Independent absolute pad transform failed'
 structure=runpy.run_path(str(ROOT/'tools/check-routing-progress-plan.py'))['immutable_board_structure'];assert structure(PARENT)==structure(path)
 for ext,digest in PROFILES.items():assert sha(Path(path).with_suffix(ext))==digest and PARENT.with_suffix(ext).read_bytes()==Path(path).with_suffix(ext).read_bytes()
 ot={t.m_Uuid.AsString():t for t in old.GetTracks()};nt={t.m_Uuid.AsString():t for t in new.GetTracks()};assert len(ot)==19381 and len(nt)==len(list(new.GetTracks()))==19357
 retired={r['uuid'] for r in plan['retired_copper']};added={r['uuid']:r for r in plan['added_copper']};assert ot.keys()-nt.keys()==retired and len(retired)==25 and nt.keys()-ot.keys()==added.keys() and len(added)==1
 for row in plan['retired_copper']:
  o=ot[row['uuid']];assert list(h['signature'](old,o))==row['signature'] and (int(o.GetViaType()) if isinstance(o,p.PCB_VIA) else None)==row['via_type']
 for uid in ot.keys()&nt.keys():
  assert h['signature'](old,ot[uid])==h['signature'](new,nt[uid])
  if isinstance(ot[uid],p.PCB_VIA):assert ot[uid].GetViaType()==nt[uid].GetViaType()
 for uid,row in added.items():assert list(h['signature'](new,nt[uid]))==row['signature'] and not isinstance(nt[uid],p.PCB_VIA) and row['via_type'] is None and nt[uid].GetWidth()==200000 and nt[uid].GetLayer()==p.F_Cu
 assert contact_catalog(old,retired)==plan['source_retirement_contacts']
 result=connectivity(old,new);result.update(front_courtyards=front_courtyards(new),external_contacts=external_contacts(old,new,plan),hole_audit=hole_audit(new,added),unchanged_source_copper=19356,retired_copper=25,added_copper=1,exact_part_inventory=483,unchanged_profiles_rules_structure=True);return result
