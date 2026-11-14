#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Finite ADR0097 sensor pad/courtyard/adjacent-via feasibility; no routed output.

Require the exact 39-open source. In-memory exclusions enumerate only the
recorded local study cohort; no copper is retired from a saved board. Zero
candidates proves nothing between samples or with wider coordinated rework.
"""
from pathlib import Path
from collections import defaultdict,Counter
import pcbnew as p,sys,json,runpy,math,argparse,hashlib
sys.path.insert(0,'tools');import routing_remaining as policy
ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--source',type=Path,default=policy.OUTPUT);ap.add_argument('--output',type=Path,default=policy.ROOT/'hardware/coupon/rev-a/build/zero-open-routing/temp-cluster-screen.json');args=ap.parse_args();src=args.source.resolve();out=args.output.resolve();assert (policy.ROOT/'hardware/coupon/rev-a/build').resolve() in out.parents and out.suffix=='.json' and out!=src;source_sha=policy.sha(src);assert source_sha=='aab8f44a9ec3ae65aed4ee2500d52d57d4d3872c8428b8f50c765bfedd205a1e','Recorded 39-open source required';b=p.LoadBoard(str(src));h=runpy.run_path('tools/screen-converter-inductor-locality.py');courts=h['courtyards'];g=h['geometry'];moving={'U39','R89','R90'};f=b.FindFootprintByReference('U39');pin=lambda fp,n:next(q for q in fp.Pads() if q.GetNumber()==n);q5=pin(f,'5');original=p.VECTOR2I(f.GetPosition());c50=pin(b.FindFootprintByReference('C50'),'1').GetPosition();oldcap=math.hypot(q5.GetPosition().x-c50.x,q5.GetPosition().y-c50.y)
# Exact local rows enumerated in the read-only source inventory, not a general deletion policy.
rows = [('track', 'TEMP_OK', 56885000, 15000000, 56935000, 14750000, 'B.Cu', 200000),
 ('track', 'TEMP_OK', 56885000, 16000000, 57550000, 16000000, 'B.Cu', 200000),
 ('track', 'TEMP_OK', 57550000, 15000000, 56885000, 15000000, 'B.Cu', 200000),
 ('track', 'TEMP_OK', 57550000, 16000000, 57550000, 15000000, 'B.Cu', 200000),
 ('track', 'GND', 58350000, 16000000, 58450000, 16000000, 'B.Cu', 200000),
 ('track', 'TMP_COLD_SET', 58365000, 15500000, 59000000, 15500000, 'B.Cu', 200000),
 ('track', 'GND', 58365000, 16000000, 58350000, 16000000, 'B.Cu', 200000),
 ('track', 'GND', 58450000, 16000000, 58365000, 16000000, 'B.Cu', 200000),
 ('track', 'GND', 58450000, 16000000, 58450000, 17650000, 'B.Cu', 200000),
 ('track', 'GND', 58450000, 17750000, 58450000, 16000000, 'B.Cu', 200000),
 ('track', 'TMP_COLD_SET', 59000000, 15500000, 59000000, 16750000, 'B.Cu', 200000),
 ('track', 'TMP_COLD_SET', 59000000, 16750000, 59500000, 16750000, 'B.Cu', 200000),
 ('track', 'TMP_HOT_SET', 59865000, 14500000, 58365000, 15000000, 'B.Cu', 200000),
 ('track', 'GND', 59865000, 15500000, 59865000, 16000000, 'B.Cu', 200000),
 ('track', 'GND', 59865000, 16000000, 60250000, 16000000, 'B.Cu', 200000),
 ('track', 'GND', 60250000, 16000000, 60250000, 17750000, 'B.Cu', 200000),
 ('track', 'GND', 60250000, 17750000, 58450000, 17750000, 'B.Cu', 200000)]
assert all(sum(policy.signature(b,t)==row for t in b.GetTracks())==1 for row in rows),'Exact study cohort missing'
held=[]
for t in list(b.GetTracks()):
 if policy.signature(b,t) in rows:b.Remove(t);held.append(t)
items=list(b.GetTracks())+[q for fp in b.GetFootprints() if fp.GetReference() not in moving for q in fp.Pads()];bins=defaultdict(list)
def cells(bb):return [(x,y) for x in range(bb.GetX()//1000000,bb.GetRight()//1000000+1) for y in range(bb.GetY()//1000000,bb.GetBottom()//1000000+1)]
for o in items:
 box=o.GetBoundingBox();box.Inflate(400000)
 for l in (p.B_Cu,p.In4_Cu):
  if o.IsOnLayer(l):
   for cell in cells(box):bins[(l,*cell)].append(o)
def clear(q,l):
 box=q.GetBoundingBox();obs={o.m_Uuid.AsString():o for cell in cells(box) for o in bins[(l,*cell)]}
 return not any(o.GetNetCode()!=q.GetNetCode() and q.GetEffectiveShape(l).Collide(o.GetEffectiveShape(l),199990) for o in obs.values())
external=[(fp.GetReference(),poly) for fp in b.GetFootprints() if fp.GetReference() not in moving and fp.GetLayer()==p.B_Cu for poly in courts(fp)];fail=Counter();result=[]
for angle in (0,90,180,270):
 f.SetOrientationDegrees(angle)
 for x in range(54000000,59000001,100000):
  for y in range(13000000,19000001,100000):
   f.SetPosition(p.VECTOR2I(x,y));v=q5.GetPosition()
   if math.hypot(x-original.x,y-original.y)>3000000:continue
   own=courts(f)
   if any(min(pt[0] for pt in poly)<49500000 or max(pt[0] for pt in poly)>59500000 or min(pt[1] for pt in poly)<12250000 or max(pt[1] for pt in poly)>20250000 for poly in own):fail['outside_sensor_reservation']+=1;continue
   if math.hypot(v.x-c50.x,v.y-c50.y)>oldcap:fail['bypass_distance_increased']+=1;continue
   if any(g.intersects(poly,other) for poly in own for ref,other in external):fail['courtyard']+=1;continue
   if not all(clear(q,p.B_Cu) for q in f.Pads()):fail['pad_copper']+=1;continue
   via=p.PCB_VIA(b);via.SetPosition(v);via.SetViaType(p.VIATYPE_MICROVIA);via.SetLayerPair(p.In4_Cu,p.B_Cu);via.SetWidth(300000);via.SetDrill(100000);via.SetNetCode(q5.GetNetCode())
   if not all(clear(via,l) for l in (p.B_Cu,p.In4_Cu)):fail['via_copper']+=1;continue
   result.append({'sensor_centre_iu':[x,y],'angle_deg':angle,'vdd_capture_iu':[v.x,v.y],'movement_mm':math.hypot(x-original.x,y-original.y)/1e6,'bypass_pad_distance_mm':math.hypot(v.x-c50.x,v.y-c50.y)/1e6})
result.sort(key=lambda q:q['movement_mm']);assert policy.sha(src)==source_sha
out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps({'SPDX-License-Identifier':'CERN-OHL-S-2.0','source_sha256':source_sha,'tool_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'grid_step_iu':100000,'orthogonal_orientations_deg':[0,90,180,270],'sensor_centre_bounds_iu':[[54000000,13000000],[59000000,19000000]],'sensor_reservation_iu':[[49500000,12250000],[59500000,20250000]],'sensor_movement_bound_iu':3000000,'fixed_bypass_reference':'C50','previous_bypass_pad_distance_mm':oldcap/1e6,'exact_unselected_study_copper_cohort':rows,'candidate_count':len(result),'failures':dict(fail),'candidates':result,'status':'READ_ONLY_SENSOR_PAD_VIA_SCREEN_RESISTOR_RESTORATION_NOT_ESTABLISHED','source_unchanged':True,'fabrication_release_allowed':False},indent=2,sort_keys=True)+'\n');print('sensor pad/via candidates',len(result),'failures',dict(fail));print(result[:20])
