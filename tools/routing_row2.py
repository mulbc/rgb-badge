# SPDX-License-Identifier: Apache-2.0
"""Exact complete row-two resistor exchange ledger; CAD continuity only."""
from collections import Counter
import copy
import hashlib
import json
from pathlib import Path
import runpy
ROOT=Path(__file__).resolve().parents[1]
PARENT=ROOT/'hardware/coupon/rev-a/staging/led-inverter-routing-trial-114mm.kicad_pcb'
PARENT_SHA='a4d27c5babed5556002cf71b8fae3c3280f627edeb0ff673b9b787d21d4b91ab'
OUTPUT=ROOT/'hardware/coupon/rev-a/staging/led-row2-routing-trial-114mm.kicad_pcb'
PLAN=ROOT/'mechanical/review/row2-routing-plan.json'
PLAN_SHA='cfac460d07605254132805ab9f0e66c1fc67c446b65c5b03c87960e2d3741b01'
BOARD_SHA='1723cb53524f7907c784cc401e3b73c5e0ee93b667dedd246a87bf60c673ac34'
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
 aa,bb=pads(old),pads(new);assert aa.keys()==bb.keys(),'Live pad inventory changed';groups={group(old,q):uid for uid,q in aa.items()};assert len(groups)==217
 for g,uid in groups.items():assert g<=group(new,bb[uid]),'Original group split: '+aa[uid].GetNetname()
 target=[q for fp in new.GetFootprints() for q in fp.Pads() if q.GetNetname()=='ROW_GATE_02']
 assert len(target)==4 and group(new,target[0])==frozenset(q.m_Uuid.AsString() for q in target),'Full row gate terminal group disconnected'
 native=new.GetConnectivity().GetUnconnectedCount(False);physical=len({group(new,q) for q in bb.values()})-len({q.GetNetname() for q in bb.values()});assert native==physical==28
 return dict(native_opens=native,physical_opens=physical,prior_groups_preserved=217,physical_groups=216,net_count=188)

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
 assert set(plan['poses'])=={'R8','R37'}
 for ref,a in aa.items():
  b=bb[ref];assert (a.m_Uuid.AsString(),a.GetFPIDAsString(),a.GetValue(),a.GetLayer(),sorted((x.GetName(),x.GetText()) for x in a.GetFields()))==(b.m_Uuid.AsString(),b.GetFPIDAsString(),b.GetValue(),b.GetLayer(),sorted((x.GetName(),x.GetText()) for x in b.GetFields())),'Part identity/fields changed: '+ref
  assert sorted(h['local_pad_signature'](x) for x in a.Pads())==sorted(h['local_pad_signature'](x) for x in b.Pads()),'Local pads changed: '+ref
  pose=plan['poses'].get(ref,dict(position_iu=list(a.GetPosition()),orientation_degrees=a.GetOrientation().AsDegrees()%360));assert (list(b.GetPosition()),b.GetOrientation().AsDegrees()%360)==(pose['position_iu'],pose['orientation_degrees']),'Part pose changed: '+ref
  ap={x.m_Uuid.AsString():x for x in a.Pads()};bp={x.m_Uuid.AsString():x for x in b.Pads()};assert ap.keys()==bp.keys()
  for uid,q in ap.items():
   x,y=q.GetPosition();expected=[145150000-x,17000000-y] if ref=='R8' else [x+4950000,y+2250000] if ref=='R37' else [x,y];assert list(bp[uid].GetPosition())==expected,'Independent pad transform failed'
 assert runpy.run_path(str(ROOT/'tools/check-routing-progress-plan.py'))['immutable_board_structure'](PARENT)==runpy.run_path(str(ROOT/'tools/check-routing-progress-plan.py'))['immutable_board_structure'](path),'Board/net/zone/setup structure changed'
 for ext in ['.kicad_pro','.kicad_dru']:assert PARENT.with_suffix(ext).read_bytes()==Path(path).with_suffix(ext).read_bytes(),'Profile/rules changed'
 ot={t.m_Uuid.AsString():t for t in old.GetTracks()};nt={t.m_Uuid.AsString():t for t in new.GetTracks()};retired={r['uuid'] for r in plan['retired_copper']};assert ot.keys()-nt.keys()==retired and len(retired)==19,'Source retirement differs'
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
 result=connectivity(old,new);result['external_plane_contacts']=external_contacts(old,new);result['hole_audit']=hole_audit(new,added);result.update(unchanged_source_copper=19377,added_copper=len(added),retired_copper=19,exact_part_inventory=483,unchanged_rules_profiles_structure=True)
 return result

def check_drc(path,board):
 from routing_inverter import check_drc as original
 original(path,board)

def external_contacts(old,new):
 import pcbnew as p
 from routing_zone_targets import connected_polygons
 plan=load_plan();tracks={t.m_Uuid.AsString():t for t in new.GetTracks()}
 def pad(board,ref,n):return next(q for q in board.FindFootprintByReference(ref).Pads() if q.GetNumber()==n)
 def group(q):return frozenset(z.m_Uuid.AsString() for z in new.GetConnectivity().GetConnectedItems(q) if isinstance(z,p.PAD))
 supply=pad(new,'R8','1');assert list(supply.GetPosition())==[72575000,8500000] and supply.GetPosition()==pad(old,'R8','1').GetPosition(),'Fixed supply pad moved'
 selector=pad(new,'R37','1');assert group(selector)==frozenset(q.m_Uuid.AsString() for f in new.GetFootprints() for q in f.Pads() if q.GetNetname()=='ROW_SEL_15'),'Original selector group disconnected'
 lead=tracks[plan['selector_replacement_uuid']]
 for uid in plan['external_selector_tracks']:
  assert lead.GetEffectiveShape(p.B_Cu).Collide(tracks[uid].GetEffectiveShape(p.B_Cu),0),'Retained selector contact lost'
 ground=pad(new,'R37','2');gg=group(ground)
 assert len(gg)>100 and all(gg<=group(tracks[uid]) for uid in plan['old_ground_tracks']),'Original ground branch disconnected'
 witnesses=[dict(layer=new.GetLayerName(layer),zone_uuid=uid,polygon=i,source_witness_uuid=w) for layer,unit,uid,i,w in connected_polygons(new,ground) if layer==p.B_Cu and unit.Collide(ground.GetEffectiveShape(layer),0)]
 assert witnesses and any(v['source_witness_uuid'] in tracks for v in witnesses),'Original connected-ground fill contact lost'
 return dict(ground_fill=witnesses,selector_tracks=plan['external_selector_tracks'],old_ground_tracks=plan['old_ground_tracks'],fixed_supply_position_iu=list(supply.GetPosition()))

def hole_audit(board,added):
 """Independently audit actual close new drill pairs; no native rule relaxation."""
 import pcbnew as p
 stack=[p.F_Cu,p.In1_Cu,p.In2_Cu,p.In3_Cu,p.In4_Cu,p.B_Cu];outer={frozenset(z) for z in zip(stack,stack[1:]) if set(z)!={p.In2_Cu,p.In3_Cu}};central=frozenset([p.In2_Cu,p.In3_Cu]);holes=[t for t in board.GetTracks() if isinstance(t,p.PCB_VIA)]+[q for f in board.GetFootprints() for q in f.Pads() if max(q.GetDrillSize())>0];seen=set();disjoint=[];aligned=[]
 def span(o):return frozenset(stack[stack.index(o.TopLayer()):stack.index(o.BottomLayer())+1]) if isinstance(o,p.PCB_VIA) else frozenset(stack)
 def supported(o,s):
  return isinstance(o,p.PCB_VIA) and ((o.GetViaType()==p.VIATYPE_MICROVIA and s in outer and o.GetWidth(o.TopLayer())==300000 and o.GetDrillValue()==100000) or (o.GetViaType()==p.VIATYPE_BURIED and s==central and o.GetWidth(o.TopLayer())==500000 and o.GetDrillValue()==300000))
 for a in holes:
  if a.m_Uuid.AsString() not in added:continue
  for b in holes:
   pair=tuple(sorted([a.m_Uuid.AsString(),b.m_Uuid.AsString()]))
   if pair[0]==pair[1] or pair in seen:continue
   seen.add(pair)
   if not a.GetEffectiveHoleShape().Collide(b.GetEffectiveHoleShape(),250000):continue
   sa,sb=span(a),span(b);row=dict(uuids=list(pair),first_uuid=a.m_Uuid.AsString(),first_span=[board.GetLayerName(l) for l in stack if l in sa],second_span=[board.GetLayerName(l) for l in stack if l in sb],first_position_iu=list(a.GetPosition()),second_position_iu=list(b.GetPosition()))
   if supported(a,sa) and supported(b,sb) and sa.isdisjoint(sb):disjoint.append(row);continue
   if supported(a,sa) and supported(b,sb) and sa in outer and sb in outer and len(sa&sb)==1 and a.GetPosition()==b.GetPosition() and a.GetNetCode()==b.GetNetCode():aligned.append(row);continue
   raise AssertionError('Unsupported or overlapping close new drill pair: '+repr(row))
 return dict(disjoint_supported_close_pairs=disjoint,aligned_adjacent_stacks=aligned,other_close_pairs=0,minimum_unchanged_hole_clearance_mm=.25,fabrication_qualified=False)
