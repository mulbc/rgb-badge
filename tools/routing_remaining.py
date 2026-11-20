# SPDX-License-Identifier: Apache-2.0
"""ADR0092 exact routing successor validation, separate from qualification."""
from collections import Counter
import hashlib,json,math,runpy
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PARENT=ROOT/'hardware/coupon/rev-a/staging/led-switch-routing-trial-114mm.kicad_pcb'
PARENT_SHA='b847f59f8a13a63d8db7a3c2ed2e7efc37239edc03c16fe12adc8b5758b4d524'
OUTPUT=ROOT/'hardware/coupon/rev-a/staging/led-remaining-routing-trial-114mm.kicad_pcb'
PLAN=ROOT/'mechanical/review/remaining-routing-plan.json'
PLAN_SHA='d3337ea9a71a1b646e2329d8271144d42a6a568e6eee3bd7ca3ee08e3c3433c3'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load_plan():
 assert sha(PARENT)==PARENT_SHA and sha(PLAN)==PLAN_SHA,'Frozen routing source/plan changed'
 plan=json.loads(PLAN.read_text());assert plan['parent_sha256']==PARENT_SHA
 assert plan['native_opens']==plan['physical_opens'] and 0<=plan['native_opens']<43
 assert not plan['fabrication_release_allowed']
 return plan

def signature(board,t):
 import pcbnew as p
 if isinstance(t,p.PCB_VIA):return ('via',t.GetNetname(),t.GetPosition().x,t.GetPosition().y,board.GetLayerName(t.TopLayer()),board.GetLayerName(t.BottomLayer()),t.GetWidth(t.TopLayer()),t.GetDrillValue(),int(t.GetViaType()))
 return ('track',t.GetNetname(),t.GetStart().x,t.GetStart().y,t.GetEnd().x,t.GetEnd().y,board.GetLayerName(t.GetLayer()),t.GetWidth())

def audit(path,plan=None,fill=True):
 import pcbnew as p
 plan=plan or load_plan();old,new=[p.LoadBoard(str(x)) for x in (PARENT,path)]
 inventory=lambda b:Counter(signature(b,t) for t in b.GetTracks())
 a,b=inventory(old),inventory(new)
 from routing_cap_microplacement import validate_plan as cap_plan,verify_native as cap_verify
 cap_plan(plan)
 assert a-b==Counter(map(tuple,plan['removed_copper'])),'Exact copper retirement differs'
 assert b-a==Counter(map(tuple,plan['added_copper'])),'Exact added copper differs'
 allowed=('track','GND',59865000,16000000,58365000,16000000,'B.Cu',200000)
 from routing_ground_plane import validate_plan as plane_plan,verify_native as plane_verify
 plane_retired=plane_plan(plan)
 from routing_permission_lead import validate_plan as permission_plan,verify_native as permission_verify
 permission_retired=permission_plan(plan)
 from routing_r11_ground import validate_plan as r11_plan,verify_native as r11_verify
 r11_retired=r11_plan(plan)
 entry=plan.get('ground_return_replacement')
 if entry:
  assert Counter(map(tuple,plan['removed_copper']))==Counter([allowed])+plane_retired+permission_retired+r11_retired and entry['original']==list(allowed),'Unreviewed retirement scope'
  originals=[t for t in old.GetTracks() if signature(old,t)==allowed];assert len(originals)==1
  h=runpy.run_path(str(ROOT/'tools/check-routing-progress-trial.py'))
  witnesses=runpy.run_path(str(ROOT/'tools/routing_track_replacements.py'))['contacts'](old,originals[0],signature,h['physical_identity'])
  assert [key for key,_ in witnesses]==entry['junction_contacts'],'Ground-return source contacts differ'
  wanted=Counter(map(tuple,entry['replacement']));replacement=[]
  for t in new.GetTracks():
   key=signature(new,t)
   if wanted[key]:replacement.append(t);wanted[key]-=1
  assert not +wanted and replacement,'Ground-return replacement missing'
  assert sum(math.dist(row[2:4],row[4:6]) for row in entry['replacement'])<8000000
  for row in entry['replacement']:
   assert row[:2]==['track','GND'] and row[6:]==['B.Cu',200000]
   assert all(58300000<=row[i]<=60750000 for i in (2,4)) and all(16000000<=row[i]<=18250000 for i in (3,5))
  for point in [originals[0].GetStart(),originals[0].GetEnd()]:
   assert any(t.GetEffectiveShape(p.B_Cu).Collide(p.SHAPE_CIRCLE(point,1),0) for t in replacement),'Original return endpoint lost'
  assert all(any(t.GetEffectiveShape(p.B_Cu).Collide(o.GetEffectiveShape(p.B_Cu),0) for t in replacement) for _,o in witnesses),'Original return junction lost'
 else:assert Counter(map(tuple,plan['removed_copper']))==plane_retired+permission_retired+r11_retired,'Unreviewed original copper retirement'

 layers=['F.Cu','In1.Cu','In2.Cu','In3.Cu','In4.Cu','B.Cu']
 for row in plan['added_copper']:
  if row[0]=='track':assert row[-1]==200000,'General narrowing forbidden'
  elif row[-1]==int(p.VIATYPE_MICROVIA):
   assert row[6:8]==[300000,100000] and abs(layers.index(row[4])-layers.index(row[5]))==1
   assert set(row[4:6])!={'In2.Cu','In3.Cu'},'New unsupported centre microvia'
  else:assert row[4:] in (['In2.Cu','In3.Cu',500000,300000,int(p.VIATYPE_BURIED)],['F.Cu','B.Cu',500000,300000,int(p.VIATYPE_THROUGH)]),'Unreviewed via type/geometry'
 helpers=runpy.run_path(str(ROOT/'tools/check-routing-progress-trial.py'));local=helpers['local_pad_signature']
 aa={f.GetReference():f for f in old.GetFootprints()};bb={f.GetReference():f for f in new.GetFootprints()};assert aa.keys()==bb.keys() and len(aa)==483
 for ref,f in aa.items():
  g=bb[ref];assert f.m_Uuid.AsString()==g.m_Uuid.AsString()
  assert f.GetFPIDAsString()==g.GetFPIDAsString() and f.GetLayer()==g.GetLayer()
  assert Counter(map(local,f.Pads()))==Counter(map(local,g.Pads())),'Local pad/net geometry changed: '+ref
  assert sorted((q.GetName(),q.GetText()) for q in f.GetFields())==sorted((q.GetName(),q.GetText()) for q in g.GetFields()),'Part fields changed'
  pose=plan['poses'].get(ref)
  expected=(*pose['position_iu'],pose['angle_deg']) if pose else (f.GetPosition().x,f.GetPosition().y,f.GetOrientation().AsDegrees())
  assert (g.GetPosition().x,g.GetPosition().y,g.GetOrientation().AsDegrees())==expected,'Pose differs: '+ref
 structure=runpy.run_path(str(ROOT/'tools/check-routing-progress-plan.py'))['immutable_board_structure'];assert structure(PARENT)==structure(path),'Board structure changed'
 for ext in ('.kicad_pro','.kicad_dru'):assert path.with_suffix(ext).read_bytes()==PARENT.with_suffix(ext).read_bytes(),'Rule/project profile changed'
 pads=lambda board:{q.m_Uuid.AsString():q for f in board.GetFootprints() for q in f.Pads()}
 cluster=lambda board,q:frozenset(z.m_Uuid.AsString() for z in board.GetConnectivity().GetConnectedItems(q) if isinstance(z,p.PAD))
 pa,pb=pads(old),pads(new);assert pa.keys()==pb.keys() and len(pa)==2092
 groups={cluster(old,q):key for key,q in pa.items() if q.GetNetname()};assert len(groups)==231
 for _ in range(3 if fill else 1):
  if fill:p.ZONE_FILLER(new).Fill(new.Zones());new.BuildConnectivity()
  assert inventory(new)==b,'Refill changed exact copper/net identity'
  plane_witness=plane_verify(old,new,plan,signature,helpers['physical_identity'])
  permission_witness=permission_verify(old,new,plan,signature,helpers['physical_identity'])
  from routing_native_testpad import verify_native as native_testpad_verify
  native_testpad_witness=native_testpad_verify(old,new,plan,signature)
  r11_witness=r11_verify(old,new,plan,signature,helpers['physical_identity'])
  cap_witness=cap_verify(new,plan,signature,helpers['physical_identity'])
  assert all(group<=cluster(new,pb[key]) for group,key in groups.items()),'Parent pad group split'
  assert new.GetConnectivity().GetUnconnectedCount(False)==plan['native_opens'],'Native open count differs'
  previous=plan.get('previous_checkpoint')
  if previous:
   assert not Counter(map(tuple,previous['added_copper_since_parent']))-(b-a),'Previous selected checkpoint copper retired'
   named={k:q for k,q in pb.items() if q.GetNetname()}
   assert previous['native_opens']==previous['physical_opens']
   assert len(previous['pad_groups'])==len({q.GetNetname() for q in named.values()})+previous['physical_opens']
   assert sorted(k for g in previous['pad_groups'] for k in g)==sorted(named),'Previous pad-group inventory incomplete or duplicated'
   assert all(g and set(g)<=cluster(new,pb[g[0]]) for g in previous['pad_groups']),'Previous selected checkpoint group split'
 def pin(ref,n):
  qs=[q for q in bb[ref].Pads() if q.GetNumber()==n];assert len(qs)==1
  return qs[0]
 for entries in plan['joined_pads']:
  assert len({cluster(new,pin(*entry)) for entry in entries})==1,'Selected pin witness missing'
 # Preserve intentional source boundaries as separate net names, irrespective of routing completeness.
 assert pin('U36','6').GetNetname()=='GND' and pin('U37','12').GetNetname()=='VLED_ENABLE_DRAFT'
 assert pin('SW2','3').GetNetname()=='APP_ON_SW_DRAFT'
 if 'R1' in plan['poses']:
  for x,y in [('1','1'),('2','56')]:
   assert math.dist((pin('R1',x).GetPosition().x,pin('R1',x).GetPosition().y),(pin('U1',y).GetPosition().x,pin('U1',y).GetPosition().y))<=3000000,'IREF resistor locality lost'
 if 'R90' in plan['poses']:
  for n,m in [('1','2'),('2','3')]:
   assert math.dist((pin('R90',n).GetPosition().x,pin('R90',n).GetPosition().y),(pin('U39',m).GetPosition().x,pin('U39',m).GetPosition().y))<=3000000,'TMP390 resistor locality lost'
  local_ground=False
  for zone in new.Zones():
   if zone.GetLayer()!=p.B_Cu or zone.GetNetCode()!=pin('R90','2').GetNetCode():continue
   filled=zone.GetFilledPolysList(p.B_Cu)
   for i in range(filled.OutlineCount()):
    unit=filled.UnitSet(i)
    if unit.Collide(pin('R90','2').GetEffectiveShape(p.B_Cu),0) and unit.Collide(pin('U39','3').GetEffectiveShape(p.B_Cu),0):local_ground=True;break
  assert local_ground,'TMP390 local ground polygon lost'
 result=runpy.run_path(str(ROOT/'tools/report-coupon-board-connectivity.py'))['open_edges_by_net'](path)
 assert result['native_open_edges']==result['pad_cluster_open_edges']==plan['native_opens']
 if r11_witness is not None:result['r11_ground_replacement_witness']=r11_witness
 if cap_witness is not None:result['capacitor_microplacement_witness']=cap_witness
 if plane_witness is not None:result['ground_plane_replacement_witness']=plane_witness
 if permission_witness is not None:result['permission_lead_replacement_witness']=permission_witness
 if native_testpad_witness is not None:result['native_testpad_escape_witness']=native_testpad_witness
 return old,new,result
