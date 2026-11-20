# SPDX-License-Identifier: Apache-2.0
"""Exact inverter/bypass migration ledger; CAD continuity only."""
from collections import Counter
import copy
import hashlib
import json
from pathlib import Path
import runpy
ROOT=Path(__file__).resolve().parents[1]
PARENT=ROOT/'hardware/coupon/rev-a/staging/led-enable-routing-trial-114mm.kicad_pcb'
PARENT_SHA='90db778d8e44b2c71ab5e1f5d8a1c586ee71c25d46892b1406c4792ac7720abd'
OUTPUT=ROOT/'hardware/coupon/rev-a/staging/led-inverter-routing-trial-114mm.kicad_pcb'
PLAN=ROOT/'mechanical/review/inverter-routing-plan.json'
PLAN_SHA='fd4135a4dd350664208a0956e4f5f5584dfbf774b333ecd8dad670621e9b3af8'
BOARD_SHA='a4d27c5babed5556002cf71b8fae3c3280f627edeb0ff673b9b787d21d4b91ab'
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
 aa,bb=pads(old),pads(new);assert aa.keys()==bb.keys(),'Live pad inventory changed';groups={group(old,q):uid for uid,q in aa.items()};assert len(groups)==218
 for g,uid in groups.items():assert g<=group(new,bb[uid]),'Original group split: '+aa[uid].GetNetname()
 target=[q for fp in new.GetFootprints() for q in fp.Pads() if q.GetNetname()=='HEARTBEAT_FALL_CLK']
 assert len(target)>1 and group(new,target[0])==frozenset(q.m_Uuid.AsString() for q in target),'Full clock terminal group disconnected'
 native=new.GetConnectivity().GetUnconnectedCount(False);physical=len({group(new,q) for q in bb.values()})-len({q.GetNetname() for q in bb.values()});assert native==physical==29
 return dict(native_opens=native,physical_opens=physical,prior_groups_preserved=218,physical_groups=217,net_count=188)

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
 assert set(plan['poses'])=={'U48','C67'}
 for ref,a in aa.items():
  b=bb[ref];assert (a.m_Uuid.AsString(),a.GetFPIDAsString(),a.GetValue(),a.GetLayer(),sorted((x.GetName(),x.GetText()) for x in a.GetFields()))==(b.m_Uuid.AsString(),b.GetFPIDAsString(),b.GetValue(),b.GetLayer(),sorted((x.GetName(),x.GetText()) for x in b.GetFields())),'Part identity/fields changed: '+ref
  assert sorted(h['local_pad_signature'](x) for x in a.Pads())==sorted(h['local_pad_signature'](x) for x in b.Pads()),'Local pads changed: '+ref
  pose=plan['poses'].get(ref,dict(position_iu=list(a.GetPosition()),orientation_degrees=a.GetOrientation().AsDegrees()%360));assert (list(b.GetPosition()),b.GetOrientation().AsDegrees()%360)==(pose['position_iu'],pose['orientation_degrees']),'Part pose changed: '+ref
  ap={x.m_Uuid.AsString():x for x in a.Pads()};bp={x.m_Uuid.AsString():x for x in b.Pads()};assert ap.keys()==bp.keys()
  for uid,q in ap.items():
   x,y=q.GetPosition();expected=[110000000+y-1000000,28150000-x+64250000] if ref=='U48' else [x+42700000,y+29200000] if ref=='C67' else [x,y];assert list(bp[uid].GetPosition())==expected,'Independent pad transform failed'
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
 result=connectivity(old,new);result['external_plane_contacts']=external_contacts(old,new);result['hole_audit']=hole_audit(new,added);result.update(unchanged_source_copper=19367,added_copper=len(added),retired_copper=2,exact_part_inventory=483,unchanged_rules_profiles_structure=True)
 return result

def check_drc(path,board):
 import pcbnew as p
 from routing_control_cluster import check_drc as original
 old=p.LoadBoard(str(PARENT));new=p.LoadBoard(str(board));a=old.FindFootprintByReference('U48');b=new.FindFootprintByReference('U48')
 if list(b.GetPosition())==list(a.GetPosition()) and b.GetOrientationDegrees()%360==a.GetOrientationDegrees()%360:return original(path,board)
 assert list(b.GetPosition())==[110000000,28150000] and b.GetOrientationDegrees()%360==270
 actual=json.loads(Path(path).read_text());normalized=copy.deepcopy(actual);op={q.m_Uuid.AsString():q for q in a.Pads()};np={q.m_Uuid.AsString():q for q in b.Pads()};count=0
 for v in normalized['violations']:
  for item in v['items']:
   uid=item['uuid']
   if uid in op:
    x,y=op[uid].GetPosition();expected=[110000000+y-1000000,28150000-x+64250000];assert list(np[uid].GetPosition())==expected
    assert item['pos']==dict(zip(['x','y'],[n/1e6 for n in expected])),'Moved U48 finding coordinate differs'
    item['pos']=dict(zip(['x','y'],[n/1e6 for n in op[uid].GetPosition()]));count+=1
 assert count==8 and len(actual['violations'])==104
 import tempfile
 with tempfile.TemporaryDirectory(prefix='rgb-inverter-drc-') as tmp:
  target=Path(tmp)/'normalized.json';target.write_text(json.dumps(normalized));original(target,board)

def external_contacts(old,new):
 import pcbnew as p
 from routing_zone_targets import connected_polygons
 tracks={t.m_Uuid.AsString():t for t in new.GetTracks()};oldtracks={t.m_Uuid.AsString():t for t in old.GetTracks()};anchor=next(q for q in new.FindFootprintByReference('U55').Pads() if q.GetNumber()=='8')
 def group(q):return frozenset(z.m_Uuid.AsString() for z in new.GetConnectivity().GetConnectedItems(q) if isinstance(z,p.PAD))
 external=['60e01f83-f71a-5075-a05f-7bb6b2aa0ac9','7ffffe04-6468-5761-a7bc-1fb7684213d0'];assert all(group(anchor)<=group(tracks[uid]) for uid in external),'Original external APP branch disconnected'
 shape=oldtracks['0f1184fa-3b7b-5bbc-9b14-39fb0d58d95c'].GetEffectiveShape(p.In4_Cu)
 witnesses=[dict(layer=new.GetLayerName(layer),zone_uuid=uid,polygon=i,source_witness_uuid=w) for layer,unit,uid,i,w in connected_polygons(new,anchor) if layer==p.In4_Cu and uid=='626b02a6-8846-59f7-b7df-a75c78241fe0' and unit.Collide(shape,0) and all(unit.Collide(tracks[u].GetEffectiveShape(layer),0) for u in external)]
 assert witnesses,'Original filled-plane contact lost'
 return witnesses

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
