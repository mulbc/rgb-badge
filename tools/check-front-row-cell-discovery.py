#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Replay the unselected three-part front cell in memory; never write a PCB."""
import pcbnew as p,sys,json,math,runpy,uuid,hashlib
from pathlib import Path
from collections import defaultdict
import routing_pair03_supply as policy
from routing_pair01_supply import contact_catalog
record=policy.ROOT/'mechanical/review/front-row-cell-discovery.json'
data=json.loads(record.read_text());g=data['geometry']
assert hashlib.sha256(json.dumps(g,sort_keys=True,separators=(',',':')).encode()).hexdigest()==data['geometry_sha256']=='db91c5495a3b62cc592347452859dfab5c469b1775f04fb16396e9562b361ee8'
assert data['selected'] is False and data['fabrication_release_allowed'] is False
assert policy.sha(policy.OUTPUT)==g['source_sha256']==policy.BOARD_SHA
cell={'pair_pose':g['poses']['PAIR05'],'resistor_option':{'resistor_pose':g['poses']['R10']},'pulldown_pose':g['poses']['R26'],'new_copper':g['added_copper']}
catalog={'retired_copper':g['retired_copper'],'source_retirement_contacts':g['source_retirement_external_contacts']}
f=policy.ROOT/'hardware/coupon/rev-a/build/pair03-supply-routing/front-pair05';f.mkdir(parents=True,exist_ok=True)
def external(data,drop):
 return {uid:{layer:dict(copper_and_pads=[o for o in value['copper_and_pads'] if o['uuid'] not in drop],filled_polygons=value['filled_polygons']) for layer,value in layers.items()} for uid,layers in data.items()}
old=p.LoadBoard(str(policy.OUTPUT));b=p.LoadBoard(str(policy.OUTPUT));sig=policy.helper()['signature'];drop={r['uuid'] for r in catalog['retired_copper']};assert len(drop)==111 and external(contact_catalog(old,drop),drop)==catalog['source_retirement_contacts'];held=[]
for o in list(b.GetTracks()):
 if o.m_Uuid.AsString() in drop:
  r=next(r for r in catalog['retired_copper'] if r['uuid']==o.m_Uuid.AsString());assert list(sig(b,o))==r['signature'] and (int(o.GetViaType()) if isinstance(o,p.PCB_VIA) else None)==r['via_type'];b.Remove(o);held.append(o)
poses={'PAIR05':cell['pair_pose'],'R10':cell['resistor_option']['resistor_pose'],'R26':cell['pulldown_pose']}
for ref,pose in poses.items():
 fp=b.FindFootprintByReference(ref);assert fp.GetLayer()==p.B_Cu;fp.Flip(fp.GetPosition(),p.FLIP_DIRECTION_TOP_BOTTOM);fp.SetOrientationDegrees(pose['orientation_degrees']);fp.SetPosition(p.VECTOR2I(*pose['position_iu']))
fields=lambda fp:sorted((v.GetName(),v.GetText(),v.m_Uuid.AsString()) for v in fp.GetFields())
for a in old.GetFootprints():
 z=b.FindFootprintByReference(a.GetReference());assert a.m_Uuid==z.m_Uuid and a.GetValue()==z.GetValue() and a.GetFPIDAsString()==z.GetFPIDAsString() and fields(a)==fields(z);ap={q.m_Uuid.AsString():q for q in a.Pads()};zp={q.m_Uuid.AsString():q for q in z.Pads()};assert ap.keys()==zp.keys()
 for u,q in ap.items():
  x,y=q.GetPosition();expected=[94650000-y,88850000-x] if a.GetReference()=='PAIR05' else [130350000-x,10850000+y] if a.GetReference()=='R10' else [120950000-x,3650000+y] if a.GetReference()=='R26' else [x,y];assert list(zp[u].GetPosition())==expected;assert zp[u].GetNumber()==q.GetNumber() and zp[u].GetNetname()==q.GetNetname() and zp[u].GetSize()==q.GetSize()
add=runpy.run_path(str(policy.ROOT/'tools/generate-gauge-supply-routing.py'))['add'];fixedids=set()
for i,row in enumerate(cell['new_copper']):
 uid=str(uuid.uuid5(uuid.NAMESPACE_URL,'rgb-badge:ADR0279:fixed:'+str(i)+':'+json.dumps(row,sort_keys=True)));add(b,dict(row,uuid=uid));fixedids.add(uid)
geometry=runpy.run_path(str(policy.ROOT/'tools/screen-converter-inductor-locality.py'))['geometry']
def polygon(fp):
 fp.BuildCourtyardCaches();poly=fp.GetCourtyard(p.F_CrtYd);assert poly.OutlineCount()==1 and poly.HoleCount(0)==0;ch=poly.COutline(0);return [tuple(ch.CPoint(i)) for i in range(ch.PointCount())]
front=[fp for fp in b.GetFootprints() if fp.GetLayer()==p.F_Cu]
for ref in poses:
 fp=b.FindFootprintByReference(ref)
 for other in front:
  if other.GetReference()!=ref:assert not geometry.intersects(polygon(fp),polygon(other)),('Courtyard',ref,other.GetReference())
layers=list(b.GetEnabledLayers().CuStack());objects=list(b.GetTracks())+[q for fp in b.GetFootprints() for q in fp.Pads()];bins=defaultdict(dict)
def cells(box):return [(x,y) for x in range(box.GetX()//1000000,box.GetRight()//1000000+1) for y in range(box.GetY()//1000000,box.GetBottom()//1000000+1)]
for o in objects:
 box=o.GetBoundingBox();box.Inflate(200000)
 for l in layers:
  if o.IsOnLayer(l):
   for c in cells(box):bins[(l,*c)][o.m_Uuid.AsString()]=o
for o in [o for o in b.GetTracks() if o.m_Uuid.AsString() in fixedids]+[q for fp in front if fp.GetReference() in poses for q in fp.Pads()]:
 others={u:z for l in layers if o.IsOnLayer(l) for c in cells(o.GetBoundingBox()) for u,z in bins[(l,*c)].items()}
 for z in others.values():
  if o.m_Uuid==z.m_Uuid or o.GetNetCode()==z.GetNetCode():continue
  if isinstance(o,p.PAD) and isinstance(z,p.PAD) and o.GetParentFootprint().m_Uuid==z.GetParentFootprint().m_Uuid:continue
  assert all(not o.IsOnLayer(l) or not z.IsOnLayer(l) or not o.GetEffectiveShape(l).Collide(z.GetEffectiveShape(l),199990) for l in layers),('New external Cu',o.m_Uuid.AsString(),z.m_Uuid.AsString())
fixedvias={o.m_Uuid.AsString() for o in b.GetTracks() if isinstance(o,p.PCB_VIA) and o.m_Uuid.AsString() in fixedids};holes=policy.hole_audit(b,fixedvias);aa,original_groups,original_attached=policy.components(old)
def verify(opens,lost):
 bb,current,attached=policy.components(b);assert aa.keys()==bb.keys() and len(original_groups)==210;lookup={u:(g,cu) for g,(_,cu) in current.items() for u in g};actual_lost=[]
 for g,(uid,cu) in original_groups.items():
  ng,nc=lookup[uid]
  if not g<=ng:actual_lost.append(aa[uid].GetNetname())
  union=set().union(*(lookup[u][1] for u in g));assert cu-drop<=union,('Retained source Cu lost',aa[uid].GetNetname())
 assert sorted(actual_lost)==sorted(lost),('Prior group splits',actual_lost)
 assert len(attached)==len(list(b.GetTracks())),'Orphan Cu';assert len(original_attached-drop)==19256
 nets=len({q.GetNetname() for q in bb.values()});native=b.GetConnectivity().GetUnconnectedCount(False);assert native==len(current)-nets==opens and nets==188
 def size(ref,pin):
  q=next(q for q in b.FindFootprintByReference(ref).Pads() if q.GetNumber()==pin);return len(lookup[q.m_Uuid.AsString()][0])
 assert size('C71','2')==size('PAIR05','1')==size('R26','2')==197
 assert size('R18','1')==size('PAIR05','4')==size('R10','1')==40
 assert size('PAIR05','5')==size('R10','2')==4
 assert size('PAIR05','3')==(2 if 'ROW_04_A' in lost else 18)
 assert size('PAIR05','2')==size('R26','1')==(2 if 'ROW_SEL_04' in lost else 3)
 return dict(native_opens=native,physical_opens=opens,original_groups=210,prior_groups_preserved=210-len(actual_lost),temporarily_split_original_groups=actual_lost,retained_attached_source_copper=19256,main_ground_pads=197,main_vled_pads=40,gate_pads=4,row_pads=size('PAIR05','3'),selector_pads=size('PAIR05','2'),orphan_copper=0)
p.ZONE_FILLER(b).Fill(b.Zones());b.BuildConnectivity();base=verify(22,['ROW_04_A','ROW_SEL_04']);print('CELL_BASE',base,flush=True)
if __name__=='__main__':
 (f/'public-replay.json').write_text(json.dumps(dict(source_sha256=policy.BOARD_SHA,geometry_sha256=data['geometry_sha256'],base=base,hole_audit=holes,selected=False,read_only=True,pcb_written=False,fabrication_release_allowed=False),indent=2)+'\n')

# Optional independently frozen selector-only replay. This still leaves ROW04 open.
if __name__=='__main__' and '--restore-selector' in sys.argv[1:]:
 route=data['selector_only_restoration']['supply_bridge'];rows=route['new_copper']
 assert hashlib.sha256(json.dumps(rows,sort_keys=True,separators=(',',':')).encode()).hexdigest()==data['selector_route_sha256']=='a251ec65094ca128045753ce7b11c0d169ca0373406d8f54cc0e32930f02cc52'
 assert route['goal_witness_uuid']=='7c230c90-28aa-5a4c-a462-1ff328f288fd'
 added=set();vias=set()
 for i,row in enumerate(rows):
  s=row['signature'];assert s[1]=='ROW_SEL_04'
  if s[0]=='track':assert s[6] in ['F.Cu','In1.Cu'] and s[7]==200000 and row['via_type'] is None
  else:assert s==['via','ROW_SEL_04',83425000,12200000,'F.Cu','In1.Cu',300000,100000] and row['via_type']==1
  uid=str(uuid.uuid5(uuid.NAMESPACE_URL,'rgb-badge:ADR0290:'+str(i)+':'+json.dumps(s)));add(b,dict(row,uuid=uid));added.add(uid)
  if s[0]=='via':vias.add(uid)
 assert len(vias)==1
 for o in b.GetTracks():
  if o.m_Uuid.AsString() not in added:continue
  for l in [p.F_Cu,p.In1_Cu]:
   if not o.IsOnLayer(l):continue
   for z in {u:z for c in cells(o.GetBoundingBox()) for u,z in bins[(l,*c)].items()}.values():
    if o.GetNetCode()!=z.GetNetCode():assert not o.GetEffectiveShape(l).Collide(z.GetEffectiveShape(l),199990),('Selector Cu',o.m_Uuid.AsString(),z.m_Uuid.AsString())
 selector_holes=policy.hole_audit(b,fixedvias|vias)
 p.ZONE_FILLER(b).Fill(b.Zones());b.BuildConnectivity();restored=verify(21,['ROW_04_A'])
 assert policy.sha(policy.OUTPUT)==policy.BOARD_SHA
 (f/'public-selector-replay.json').write_text(json.dumps(dict(source_sha256=policy.BOARD_SHA,geometry_sha256=data['geometry_sha256'],selector_route_sha256=data['selector_route_sha256'],selector=restored,hole_audit=selector_holes,selected=False,read_only=True,pcb_written=False,fabrication_release_allowed=False),indent=2)+'\n')
 print('SELECTOR_ONLY_REPLAY',restored,flush=True)
