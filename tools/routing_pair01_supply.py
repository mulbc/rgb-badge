# SPDX-License-Identifier: Apache-2.0
"""Exact PAIR01 supply continuation. CAD continuity only."""
import json,runpy,copy,tempfile
from pathlib import Path
from collections import Counter
from decimal import Decimal
from routing_r6_direct_bottom import sha,serialized_copper,components,contact_catalog,hole_audit,helper,PROFILES
ROOT=Path(__file__).resolve().parents[1]
PARENT=ROOT/'hardware/coupon/rev-a/staging/led-r6-direct-bottom-trial-114mm.kicad_pcb'
PARENT_SHA='230b0c9f456837a0dd1b5e432497aa5223da95334ac2909ff8cd39d2edea804a'
OUTPUT=ROOT/'hardware/coupon/rev-a/staging/led-pair01-supply-routing-trial-114mm.kicad_pcb'
PLAN=ROOT/'mechanical/review/pair01-supply-routing-plan.json'
BOARD_SHA='9574949d6bd56caa6f79b9db78af3531b0150cfba1f110d727c829effcaf62b3'
PLAN_SHA='006db8ac73da1ba34baf5ce8b70be341489c5f90eee1a9ff6635e04a884d068d'
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
 plan=load_plan() if plan is None else plan;aa,original,oa=components(old);bb,current,na=components(new);assert aa.keys()==bb.keys() and len(original)==212
 retired={r['uuid'] for r in plan['retired_copper']};added={r['uuid'] for r in plan['added_copper']};lookup={uid:(g,cu) for g,(_,cu) in current.items() for uid in g}
 for g,(uid,cu) in original.items():
  ng,nc=lookup[uid];assert g<=ng,'Original group split: '+aa[uid].GetNetname();assert cu-retired<=nc,'Retained attached Cu lost'
 assert retired<=oa and added<=na and len(list(new.GetTracks()))==len(na),'Orphan Cu'
 def group(ref,n):
  q=next(q for q in new.FindFootprintByReference(ref).Pads() if q.GetNumber()==n);return lookup[q.m_Uuid.AsString()][0]
 assert len(group('C71','2'))==197 and next(q for q in new.FindFootprintByReference('PAIR01').Pads() if q.GetNumber()=='1').m_Uuid.AsString() in group('C71','2')
 assert len(group('R18','1'))==38 and next(q for q in new.FindFootprintByReference('R6').Pads() if q.GetNumber()=='1').m_Uuid.AsString() in group('R18','1')
 for ref,n,count in [('PAIR01','3',18),('PAIR01','2',3),('PAIR01','5',4),('PAIR01','4',38),('R6','2',4)]:assert len(group(ref,n))==count,(ref,n,count)
 nets=len({q.GetNetname() for q in bb.values()});native=new.GetConnectivity().GetUnconnectedCount(False);assert native==len(current)-nets==23 and nets==188 and len(current)==211
 return dict(native_opens=native,physical_opens=23,physical_groups=211,prior_groups_preserved=212,net_count=188,main_ground_pads=197,main_vled_pads=38,orphan_copper=0,retained_attached_source_copper=len(oa-retired))

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
 assert plan['poses']=={'PAIR01':dict(position_iu=[80000000,5200000],orientation_degrees=180,layer='F.Cu')};held=[]
 for ref,a in aa.items():
  z=bb[ref];assert (a.m_Uuid.AsString(),a.GetFPIDAsString(),a.GetValue(),sorted((v.GetName(),v.GetText(),v.m_Uuid.AsString()) for v in a.GetFields()))==(z.m_Uuid.AsString(),z.GetFPIDAsString(),z.GetValue(),sorted((v.GetName(),v.GetText(),v.m_Uuid.AsString()) for v in z.GetFields())),'Part identity changed: '+ref
  expected=a
  if ref=='PAIR01':
   expected=p.FOOTPRINT(a);held.append(expected);expected.SetOrientationDegrees(180);expected.SetPosition(p.VECTOR2I(80000000,5200000));assert a.GetLayer()==z.GetLayer()==p.F_Cu
  assert (expected.GetLayer(),list(expected.GetPosition()),expected.GetOrientationDegrees()%360)==(z.GetLayer(),list(z.GetPosition()),z.GetOrientationDegrees()%360),'Part pose changed: '+ref
  assert sorted(h['local_pad_signature'](q) for q in expected.Pads())==sorted(h['local_pad_signature'](q) for q in z.Pads()),'Package/pin changed: '+ref
  ap={q.m_Uuid.AsString():q for q in a.Pads()};zp={q.m_Uuid.AsString():q for q in z.Pads()};assert ap.keys()==zp.keys()
  for uid,q in ap.items():
   x,y=q.GetPosition();assert list(zp[uid].GetPosition())==([84300000-y,x-70900000] if ref=='PAIR01' else [x,y]),'Independent absolute pin transform failed'
 structure=runpy.run_path(str(ROOT/'tools/check-routing-progress-plan.py'))['immutable_board_structure'];assert structure(PARENT)==structure(path),'Board structure changed'
 for ext,digest in PROFILES.items():assert sha(Path(path).with_suffix(ext))==digest and PARENT.with_suffix(ext).read_bytes()==Path(path).with_suffix(ext).read_bytes()
 ot={t.m_Uuid.AsString():t for t in old.GetTracks()};nt={t.m_Uuid.AsString():t for t in new.GetTracks()};retired={r['uuid'] for r in plan['retired_copper']};added={r['uuid']:r for r in plan['added_copper']};assert len(ot)==19384 and len(nt)==19349 and len(retired)==62 and len(added)==27 and ot.keys()-nt.keys()==retired and nt.keys()-ot.keys()==added.keys()
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
 result=connectivity(old,new,plan);result.update(external_contacts=external_contacts(old,new,plan),front_courtyards=front_courtyards(new),hole_audit=hole_audit(new,added),exact_part_inventory=483,retired_copper=62,added_copper=27,unchanged_source_copper=19322,fabrication_release_allowed=False);return result

def check_drc(path,board):
 import pcbnew as p
 from routing_r6_direct_bottom import check_drc as previous
 old=p.LoadBoard(str(PARENT));new=p.LoadBoard(str(board));a=old.FindFootprintByReference('PAIR01');z=new.FindFootprintByReference('PAIR01')
 if (a.GetLayer(),list(a.GetPosition()),a.GetOrientationDegrees()%360)==(z.GetLayer(),list(z.GetPosition()),z.GetOrientationDegrees()%360):return previous(path,board)
 assert z.GetLayer()==p.F_Cu and list(z.GetPosition())==[80000000,5200000] and z.GetOrientationDegrees()%360==180
 op={q.m_Uuid.AsString():q for q in a.Pads()};np={q.m_Uuid.AsString():q for q in z.Pads()};actual=json.loads(Path(path).read_text());normalized=copy.deepcopy(actual);count=0
 for finding in normalized['violations']:
  touched=[item for item in finding['items'] if item['uuid'] in op]
  if not touched:continue
  assert finding['type']=='clearance' and len(finding['items'])==len(touched)==2,'External finding cannot normalize'
  for item in touched:
   uid=item['uuid'];x,y=op[uid].GetPosition();expected=[84300000-y,x-70900000];assert list(np[uid].GetPosition())==expected and item['pos']==dict(zip(['x','y'],[v/1e6 for v in expected]))
   assert item['description'].endswith('of PAIR01 on F.Cu');item['pos']=dict(zip(['x','y'],[v/1e6 for v in op[uid].GetPosition()]));count+=1
 assert count==12 and len(actual['violations'])==104,'New or missing DRC finding'
 # Only the six package-intrinsic pairs have been mapped. The source board
 # supplies the inherited pose proxy to the exact previous comparison.
 with tempfile.TemporaryDirectory(prefix='rgb-pair-supply-drc-') as tmp:
  target=Path(tmp)/'normalized.json';target.write_text(json.dumps(normalized));previous(target,PARENT)

def external_contacts(old,new,plan):
 import pcbnew as p
 old.BuildConnectivity();new.BuildConnectivity();nt={t.m_Uuid.AsString():t for t in new.GetTracks()};ot={t.m_Uuid.AsString():t for t in old.GetTracks()}
 def group(board,ref,pin):
  q=next(q for q in board.FindFootprintByReference(ref).Pads() if q.GetNumber()==pin);return {o.m_Uuid.AsString() for o in board.GetConnectivity().GetConnectedItems(q) if isinstance(o,p.PAD)}
 witnesses=[('9e97b5ce-a21b-5767-80bb-e30b1564a12d','R18','1',37),('93a70658-ba40-56ea-8f25-87c61eb44337','C71','2',197),('4409883b-837d-5302-90d8-af9d735403e5','PAIR01','3',18),('4986b5dd-44f3-5c5c-a3c1-540ce3bd5a05','R6','2',4),(plan['selector_route']['goal_witness_uuid'],'R22','1',3)]
 for uid,ref,pin,count in witnesses:
  assert uid in ot and uid in nt
  pads={o.m_Uuid.AsString() for o in old.GetConnectivity().GetConnectedItems(ot[uid]) if isinstance(o,p.PAD)};assert pads==group(old,ref,pin) and len(pads)==count
 assert group(old,'R18','1')<group(new,'R18','1') and len(group(new,'R18','1'))==38
 # Actual conductor intersection with each frozen retained source port.
 for net,uid in [('VLED',witnesses[0][0]),('GND',witnesses[1][0]),('ROW_00_A',witnesses[2][0]),('ROW_GATE_00',witnesses[3][0]),('ROW_SEL_00',witnesses[4][0])]:
  port=nt[uid];assert any(any(t.IsOnLayer(l) and port.IsOnLayer(l) and t.GetEffectiveShape(l).Collide(port.GetEffectiveShape(l),0) for l in new.GetEnabledLayers().CuStack()) for t in [nt[r['uuid']] for r in plan['added_copper'] if r['signature'][1]==net]),'Lost source port: '+net
 lengths={net:sum(nt[r['uuid']].GetLength() for r in plan['added_copper'] if r['signature'][0]=='track' and r['signature'][1]==net)/1e6 for net in ['VLED','ROW_SEL_00']};assert abs(lengths['VLED']-4.625)<1e-10 and abs(lengths['ROW_SEL_00']-plan['selector_route']['total_selector_conductor_mm'])<1e-10
 row=next(nt[r['uuid']] for r in plan['added_copper'] if r['signature'][:2]==['track','ROW_00_A'] and r['signature'][6]=='In1.Cu');assert row.GetLength()<6000000
 return dict(source_ports=5,power_length_mm=lengths['VLED'],selector_length_mm=lengths['ROW_SEL_00'],row_lead_mm=row.GetLength()/1e6)
