#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""ADR0094 bounded R90 locality; ignored output, fixed sensor and exact parts."""
import argparse,hashlib,json,math,runpy,shutil,uuid
from collections import Counter,defaultdict
from pathlib import Path
import pcbnew as p
import routing_remaining as policy
ROOT=policy.ROOT;BUILD=ROOT/'hardware/coupon/rev-a/build'
def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--source',type=Path,required=True);ap.add_argument('--return-detour',action='store_true');ap.add_argument('--output',type=Path,required=True);a=ap.parse_args();src,out=a.source.resolve(),a.output.resolve();assert BUILD.resolve() in out.parents and out!=src
 before=policy.sha(src);b=p.LoadBoard(str(src));f=b.FindFootprintByReference('R90');ic=b.FindFootprintByReference('U39');pin=lambda fp,n:next(q for q in fp.Pads() if q.GetNumber()==n)
 assert next(q.GetText() for q in f.GetFields() if q.GetName()=='MPN')=='ERJ2RKF1402X' and f.GetValue()=='14k 1%'
 original_pose=[f.GetPosition().x,f.GetPosition().y,f.GetOrientationDegrees()];original=Counter(policy.signature(b,t) for t in b.GetTracks());cluster=lambda q:frozenset(z.m_Uuid.AsString() for z in b.GetConnectivity().GetConnectedItems(q) if isinstance(z,p.PAD));groups={q.m_Uuid.AsString():cluster(q) for fp in b.GetFootprints() for q in fp.Pads() if q.GetNetname()};old_count=b.GetConnectivity().GetUnconnectedCount(False)
 retired=[];replacement=[];junctions=[]
 if a.return_detour:
  wanted=('track','GND',59865000,16000000,58365000,16000000,'B.Cu',200000)
  old=next((t for t in b.GetTracks() if policy.signature(b,t)==wanted),None);assert old is not None,'Input must contain the exact original local return'
  junction_helper=runpy.run_path(str(ROOT/'tools/routing_track_replacements.py'));identity_helper=runpy.run_path(str(ROOT/'tools/check-routing-progress-trial.py'))
  junctions=junction_helper['contacts'](b,old,policy.signature,identity_helper['physical_identity']);retired=[wanted];b.Remove(old)
  points=[(59865000,16000000),(60250000,16000000),(60250000,17750000),(58450000,17750000),(58450000,16000000),(58365000,16000000)]
  for aa,zz in zip(points,points[1:]):
   t=p.PCB_TRACK(b);t.SetStart(p.VECTOR2I(*aa));t.SetEnd(p.VECTOR2I(*zz));t.SetLayer(p.B_Cu);t.SetWidth(200000);t.SetNetCode(b.FindNet('GND').GetNetCode());replacement.append(t);b.Add(t)
  for point in [old.GetStart(),old.GetEnd()]:assert any(t.GetEffectiveShape(p.B_Cu).Collide(p.SHAPE_CIRCLE(point,1),0) for t in replacement)
  assert all(any(t.GetEffectiveShape(p.B_Cu).Collide(o.GetEffectiveShape(p.B_Cu),0) for t in replacement) for _,o in junctions)
 helper=runpy.run_path(str(ROOT/'tools/screen-converter-inductor-locality.py'));g,courts=helper['geometry'],helper['courtyards'];external=[poly for fp in b.GetFootprints() if fp.GetReference()!='R90' and fp.GetLayer()==p.B_Cu for poly in courts(fp)]
 copper=[t for t in b.GetTracks() if t.IsOnLayer(p.B_Cu)]+[q for fp in b.GetFootprints() if fp.GetReference()!='R90' for q in fp.Pads() if q.IsOnLayer(p.B_Cu)]
 def clear(t):
  box=t.GetBoundingBox();box.Inflate(200000)
  return not any(o.GetNetCode()!=t.GetNetCode() and box.Intersects(o.GetBoundingBox()) and t.GetEffectiveShape(p.B_Cu).Collide(o.GetEffectiveShape(p.B_Cu),199990) for o in copper+list(f.Pads()))
 def distance(a,z):return math.hypot(a.GetPosition().x-z.GetPosition().x,a.GetPosition().y-z.GetPosition().y)/1e6
 if not all(clear(t) for t in replacement):raise AssertionError('Proposed local return collides with original copper')
 poses=[]
 for angle in (0,90,180,270):
  for x in range(54500000,62750001,250000):
   for y in range(12250000,18750001,250000):
    f.SetOrientationDegrees(angle);f.SetPosition(p.VECTOR2I(x,y));q1,q2=pin(f,'1'),pin(f,'2');d1,d2=distance(q1,pin(ic,'2')),distance(q2,pin(ic,'3'))
    if max(d1,d2)>3:continue
    if any(g.intersects(c,e) for c in courts(f) for e in external):continue
    if not all(clear(q) for q in [q1,q2]):continue
    poses.append((d1+d2,d1,d2,x,y,angle))
 poses.sort();print('Eligible R90 poses',len(poses),poses[:12],flush=True);fail=Counter()
 for _,d1,d2,x,y,angle in poses:
  f.SetOrientationDegrees(angle);f.SetPosition(p.VECTOR2I(x,y));q1,q2=pin(f,'1'),pin(f,'2');dest=pin(ic,'2');bb=dest.GetBoundingBox();end=(q1.GetPosition().x,q1.GetPosition().y);centre=(dest.GetPosition().x,dest.GetPosition().y);starts=[centre,(bb.GetRight(),centre[1]),(bb.GetX(),centre[1]),(centre[0],bb.GetY()),(centre[0],bb.GetBottom())]
  for start in starts:
   paths=[(start,end),(start,(end[0],start[1]),end),(start,(start[0],end[1]),end)]
   paths += [(start,(xx,start[1]),(xx,end[1]),end) for xx in list(range(59000000,59300001,50000))+list(range(max(start[0],end[0])+400000,max(start[0],end[0])+2400001,200000))]
   paths += [(start,(xx,start[1]),(xx,yy),(end[0],yy),end) for xx in [max(start[0],end[0])+400000,max(start[0],end[0])+800000] for yy in [end[1]-500000,end[1]+500000,end[1]-1000000,end[1]+1000000]]
   for points in paths:
    new=[]
    for aa,zz in zip(points,points[1:]):
     if aa==zz:continue
     t=p.PCB_TRACK(b);t.SetStart(p.VECTOR2I(*aa));t.SetEnd(p.VECTOR2I(*zz));t.SetLayer(p.B_Cu);t.SetWidth(200000);t.SetNetCode(q1.GetNetCode());new.append(t)
    if not all(clear(t) for t in new):continue
    for t in new:b.Add(t)
    p.ZONE_FILLER(b).Fill(b.Zones());b.BuildConnectivity();pads={q.m_Uuid.AsString():q for fp in b.GetFootprints() for q in fp.Pads()};actual=Counter(policy.signature(b,t) for t in b.GetTracks());expected=original-Counter(retired)+Counter(policy.signature(b,t) for t in new+replacement)
    good=(actual==expected and b.GetConnectivity().GetUnconnectedCount(False)==old_count-1 and all(old<=cluster(pads[k]) for k,old in groups.items()) and cluster(q1)==cluster(dest))
    local_ground=False
    if good:
     for zone in b.Zones():
      if zone.GetNetCode()!=q2.GetNetCode() or zone.GetLayer()!=p.B_Cu:continue
      filled=zone.GetFilledPolysList(p.B_Cu)
      for i in range(filled.OutlineCount()):
       unit=filled.UnitSet(i)
       if unit.Collide(q2.GetEffectiveShape(p.B_Cu),0) and unit.Collide(pin(ic,'3').GetEffectiveShape(p.B_Cu),0):local_ground=True;break
    if good and local_ground:
     nets=defaultdict(set)
     for q in pads.values():
      if q.GetNetname():nets[q.GetNetname()].add(cluster(q))
     good=sum(len(v)-1 for v in nets.values())==old_count-1
    if good and local_ground:
     assert policy.sha(src)==before
     for t in new+replacement:t.SetUuid(p.KIID(str(uuid.uuid5(uuid.NAMESPACE_URL,'rgb-badge:ADR0094:R90:'+repr(policy.signature(b,t))))))
     out.parent.mkdir(parents=True,exist_ok=True);p.SaveBoard(str(out),b)
     for ext in ('.kicad_pro','.kicad_dru'):shutil.copyfile(src.with_suffix(ext),out.with_suffix(ext))
     report={'SPDX-License-Identifier':'CERN-OHL-S-2.0','status':'IGNORED_TMP390_LOCALITY_REQUIRES_FULL_DRC','source_sha256':before,'old_pose':original_pose,'pose':{'reference':'R90','position_iu':[x,y],'angle_deg':angle},'cold_pad_distance_mm':d1,'ground_pad_distance_mm':d2,'same_local_bcu_ground_polygon':True,'all_source_groups_and_other_copper_preserved':True,'removed_copper':[list(row) for row in retired],'replacement_copper':[list(policy.signature(b,t)) for t in replacement],'source_junctions':[key for key,_ in junctions],'native_opens':old_count-1,'physical_opens':old_count-1,'added_copper':[list(policy.signature(b,t)) for t in new+replacement],'fabrication_release_allowed':False};out.with_suffix('.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n');print(report,flush=True);return
    fail['ground_or_group_rejected']+=1
    for t in new:b.Remove(t)
 print('No preserving local pose',dict(fail),flush=True);assert policy.sha(src)==before
if __name__=='__main__':main()
