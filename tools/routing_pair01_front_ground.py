# SPDX-License-Identifier: Apache-2.0
"""Exact PAIR01 front ground continuation. CAD continuity only."""
import json,runpy,copy,tempfile
from pathlib import Path
from collections import Counter
from decimal import Decimal
from routing_r11_front import sha,serialized_copper,components,contact_catalog,hole_audit,helper,PROFILES
ROOT=Path(__file__).resolve().parents[1]
PARENT=ROOT/'hardware/coupon/rev-a/staging/led-r11-front-routing-trial-114mm.kicad_pcb'
PARENT_SHA='fb862c0a548599b7acf328ad8bb5006ce5f78d8b98ceec12bb4af9ace21f1d0f'
OUTPUT=ROOT/'hardware/coupon/rev-a/staging/led-pair01-front-ground-trial-114mm.kicad_pcb'
PLAN=ROOT/'mechanical/review/pair01-front-ground-plan.json'
BOARD_SHA='ec0bf7fc842f3dd4f9210e7667925cffc388d3d82906e44c5bde4e10f428ee88'
PLAN_SHA='26c2759448f8ada3213dc5dfe23ae1c0cb3dcf88e21e8f4e3696fa1288e4a467'
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
   assert node[:2]==['via','micro'] and len(node)==8 and set(attrs)=={'at','size','drill','layers','net','uuid'}
   actual=['via',attrs['net'][0],*map(iu,attrs['at']),*attrs['layers'],iu(attrs['size'][0]),iu(attrs['drill'][0])]
  assert actual==s,'Serialized new Cu differs: '+uid

def connectivity(old,new,plan=None):
 import pcbnew as p
 plan=load_plan() if plan is None else plan;aa,original,oa=components(old);bb,current,na=components(new);assert aa.keys()==bb.keys() and len(original)==214
 retired={r['uuid'] for r in plan['retired_copper']};added={r['uuid'] for r in plan['added_copper']};lookup={uid:(g,cu) for g,(_,cu) in current.items() for uid in g}
 for g,(uid,cu) in original.items():
  ng,nc=lookup[uid];assert g<=ng,'Original group split: '+aa[uid].GetNetname();assert cu-retired<=nc,'Retained attached Cu lost'
 assert retired<=oa and added<=na and len(list(new.GetTracks()))==len(na),'Orphan Cu'
 def group(ref,n):
  q=next(q for q in new.FindFootprintByReference(ref).Pads() if q.GetNumber()==n);return lookup[q.m_Uuid.AsString()][0]
 assert len(group('C71','2'))==197 and next(q for q in new.FindFootprintByReference('PAIR01').Pads() if q.GetNumber()=='1').m_Uuid.AsString() in group('C71','2')
 assert len(group('R18','1'))==37 and next(q for q in new.FindFootprintByReference('R6').Pads() if q.GetNumber()=='1').m_Uuid.AsString() in group('R18','1')
 for ref,n,count in [('PAIR01','3',18),('PAIR01','2',3),('PAIR01','5',3),('PAIR01','4',1),('R6','2',1)]:assert len(group(ref,n))==count,(ref,n,count)
 nets=len({q.GetNetname() for q in bb.values()});native=new.GetConnectivity().GetUnconnectedCount(False);assert native==len(current)-nets==25 and nets==188 and len(current)==213
 return dict(native_opens=native,physical_opens=25,physical_groups=213,prior_groups_preserved=214,net_count=188,main_ground_pads=197,main_vled_pads=37,orphan_copper=0,retained_attached_source_copper=len(oa-retired))

def front_courtyards(board):
 import pcbnew as p
 geometry=runpy.run_path(str(ROOT/'tools/screen-converter-inductor-locality.py'))['geometry']
 def polygons(fp):
  fp.BuildCourtyardCaches();poly=fp.GetCourtyard(p.F_CrtYd);assert poly.OutlineCount()==1 and poly.HoleCount(0)==0,'Missing front courtyard: '+fp.GetReference();ch=poly.COutline(0);points=[tuple(ch.CPoint(i)) for i in range(ch.PointCount())];assert geometry.convex(points);return points
 target=board.FindFootprintByReference('PAIR01');own=polygons(target);others=[fp for fp in board.GetFootprints() if fp.GetLayer()==p.F_Cu and fp is not target and fp.GetReference()!='PAIR01'];assert len(others)==258
 for fp in others:assert not geometry.intersects(own,polygons(fp)),'Front courtyard collision: '+fp.GetReference()
 return dict(checked_front_courtyards=259,overlaps=0,missing=0)

def audit(path,plan=None):
 import pcbnew as p
 plan=load_plan() if plan is None else plan;assert plan==load_plan();serialized_ledger(path,plan);old,new=(p.LoadBoard(str(x)) for x in (PARENT,path));h=helper();aa={fp.GetReference():fp for fp in old.GetFootprints()};bb={fp.GetReference():fp for fp in new.GetFootprints()};assert aa.keys()==bb.keys() and len(aa)==len(list(old.GetFootprints()))==len(list(new.GetFootprints()))==483
 assert plan['poses']=={'PAIR01':dict(position_iu=[76100000,4300000],orientation_degrees=270,layer='F.Cu',flip='top-bottom')};held=[]
 for ref,a in aa.items():
  z=bb[ref];assert (a.m_Uuid.AsString(),a.GetFPIDAsString(),a.GetValue(),sorted((v.GetName(),v.GetText(),v.m_Uuid.AsString()) for v in a.GetFields()))==(z.m_Uuid.AsString(),z.GetFPIDAsString(),z.GetValue(),sorted((v.GetName(),v.GetText(),v.m_Uuid.AsString()) for v in z.GetFields())),'Part identity changed: '+ref
  expected=a
  if ref=='PAIR01':
   expected=p.FOOTPRINT(a);held.append(expected);expected.Flip(expected.GetPosition(),p.FLIP_DIRECTION_TOP_BOTTOM);expected.SetOrientationDegrees(270);expected.SetPosition(p.VECTOR2I(76100000,4300000));assert a.GetLayer()==p.B_Cu and z.GetLayer()==p.F_Cu
  assert (expected.GetLayer(),list(expected.GetPosition()),expected.GetOrientationDegrees()%360)==(z.GetLayer(),list(z.GetPosition()),z.GetOrientationDegrees()%360),'Part pose changed: '+ref
  assert sorted(h['local_pad_signature'](q) for q in expected.Pads())==sorted(h['local_pad_signature'](q) for q in z.Pads()),'Package/pin changed: '+ref
  ap={q.m_Uuid.AsString():q for q in a.Pads()};zp={q.m_Uuid.AsString():q for q in z.Pads()};assert ap.keys()==zp.keys()
  for uid,q in ap.items():
   x,y=q.GetPosition();assert list(zp[uid].GetPosition())==([79850000-y,80050000-x] if ref=='PAIR01' else [x,y]),'Independent absolute pin transform failed'
 structure=runpy.run_path(str(ROOT/'tools/check-routing-progress-plan.py'))['immutable_board_structure'];assert structure(PARENT)==structure(path),'Board structure changed'
 for ext,digest in PROFILES.items():assert sha(Path(path).with_suffix(ext))==digest and PARENT.with_suffix(ext).read_bytes()==Path(path).with_suffix(ext).read_bytes()
 ot={t.m_Uuid.AsString():t for t in old.GetTracks()};nt={t.m_Uuid.AsString():t for t in new.GetTracks()};retired={r['uuid'] for r in plan['retired_copper']};added={r['uuid']:r for r in plan['added_copper']};assert len(ot)==19357 and len(nt)==19380 and len(retired)==38 and len(added)==61 and ot.keys()-nt.keys()==retired and nt.keys()-ot.keys()==added.keys()
 for row in plan['retired_copper']:
  t=ot[row['uuid']];assert list(h['signature'](old,t))==row['signature'] and (int(t.GetViaType()) if isinstance(t,p.PCB_VIA) else None)==row['via_type']
 for uid in ot.keys()&nt.keys():
  assert h['signature'](old,ot[uid])==h['signature'](new,nt[uid])
  if isinstance(ot[uid],p.PCB_VIA):assert ot[uid].GetViaType()==nt[uid].GetViaType()
 for uid,row in added.items():
  t=nt[uid];assert list(h['signature'](new,t))==row['signature'] and (int(t.GetViaType()) if isinstance(t,p.PCB_VIA) else None)==row['via_type']
  if isinstance(t,p.PCB_VIA):assert t.GetViaType()==p.VIATYPE_MICROVIA and t.TopLayer()==p.F_Cu and t.BottomLayer()==p.In1_Cu and t.GetWidth(t.TopLayer())==300000 and t.GetDrillValue()==100000
  else:assert t.GetWidth()==200000 and t.GetLayer() in [p.F_Cu,p.In1_Cu]
 assert contact_catalog(old,retired)==plan['source_retirement_contacts'],'Source contact catalog changed'
 result=connectivity(old,new,plan);result.update(front_courtyards=front_courtyards(new),hole_audit=hole_audit(new,added),exact_part_inventory=483,retired_copper=38,added_copper=61,unchanged_source_copper=19319,fabrication_release_allowed=False);return result

def check_drc(path,board):
 import pcbnew as p
 from routing_r11_front import check_drc as previous
 old=p.LoadBoard(str(PARENT));new=p.LoadBoard(str(board));a=old.FindFootprintByReference('PAIR01');z=new.FindFootprintByReference('PAIR01')
 if (a.GetLayer(),list(a.GetPosition()),a.GetOrientationDegrees()%360)==(z.GetLayer(),list(z.GetPosition()),z.GetOrientationDegrees()%360):return previous(path,board)
 assert z.GetLayer()==p.F_Cu and list(z.GetPosition())==[76100000,4300000] and z.GetOrientationDegrees()%360==270
 op={q.m_Uuid.AsString():q for q in a.Pads()};np={q.m_Uuid.AsString():q for q in z.Pads()};actual=json.loads(Path(path).read_text());normalized=copy.deepcopy(actual);count=0
 for finding in normalized['violations']:
  touched=[item for item in finding['items'] if item['uuid'] in op]
  if not touched:continue
  assert finding['type']=='clearance' and len(finding['items'])==len(touched)==2,'External finding cannot normalize'
  for item in touched:
   uid=item['uuid'];x,y=op[uid].GetPosition();expected=[79850000-y,80050000-x];assert list(np[uid].GetPosition())==expected and item['pos']==dict(zip(['x','y'],[v/1e6 for v in expected]))
   assert item['description'].endswith('of PAIR01 on F.Cu');item['description']=item['description'][:-len('F.Cu')]+'B.Cu';item['pos']=dict(zip(['x','y'],[v/1e6 for v in op[uid].GetPosition()]));count+=1
 assert count==12 and len(actual['violations'])==104,'New or missing DRC finding'
 with tempfile.TemporaryDirectory(prefix='rgb-pair-ground-drc-') as tmp:
  target=Path(tmp)/'normalized.json';target.write_text(json.dumps(normalized));previous(target,board)
