#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""ADR0091 finite R1 locality trial, exact ordinary-width routes, ignored output."""
import argparse,hashlib,itertools,json,math,runpy,shutil,uuid
from collections import Counter
from pathlib import Path
import pcbnew as p
ROOT=Path(__file__).resolve().parents[1]
BUILD=ROOT/'hardware/coupon/rev-a/build'
SOURCE=ROOT/'hardware/coupon/rev-a/staging/led-u36-stage-routing-trial-114mm.kicad_pcb'

def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--source',type=Path,default=SOURCE);ap.add_argument('--output',type=Path,required=True);a=ap.parse_args()
 source,out=a.source.resolve(),a.output.resolve();assert BUILD.resolve() in out.parents and out!=source
 b=p.LoadBoard(str(source));f=b.FindFootprintByReference('R1');u=b.FindFootprintByReference('U1')
 pin=lambda fp,n:next(q for q in fp.Pads() if q.GetNumber()==n)
 before={q.m_Uuid.AsString():frozenset(z.m_Uuid.AsString() for z in b.GetConnectivity().GetConnectedItems(q) if isinstance(z,p.PAD)) for fp in b.GetFootprints() for q in fp.Pads() if q.GetNetname()}
 h=runpy.run_path(str(ROOT/'tools/screen-converter-inductor-locality.py'));g,courts=h['geometry'],h['courtyards']
 external=[poly for fp in b.GetFootprints() if fp.GetReference()!='R1' and fp.GetLayer()==p.B_Cu for poly in courts(fp)]
 copper=[t for t in b.GetTracks() if t.IsOnLayer(p.B_Cu)]+[q for fp in b.GetFootprints() if fp.GetReference()!='R1' for q in fp.Pads() if q.IsOnLayer(p.B_Cu)]
 def clear(t):
  bb=t.GetBoundingBox();bb.Inflate(200000)
  return not any(o.GetNetCode()!=t.GetNetCode() and bb.Intersects(o.GetBoundingBox()) and t.GetEffectiveShape(p.B_Cu).Collide(o.GetEffectiveShape(p.B_Cu),199990) for o in copper+list(f.Pads()))
 def routes(q,dest,side):
  bb=dest.GetBoundingBox();start=(bb.GetRight(),dest.GetPosition().y) if side=='right' else (dest.GetPosition().x,bb.GetY())
  end=(q.GetPosition().x,q.GetPosition().y)
  for points in [(start,end),(start,(end[0],start[1]),end),(start,(start[0],end[1]),end)]+[(start,(start[0],yy),(end[0],yy),end) for yy in (600000,750000,1000000,1250000,1500000,1750000,2000000,2250000)]+[(start,(start[0],yy),(xx,yy),(xx,end[1]),end) for yy in (600000,750000,1000000) for xx in range(91000000,95000001,250000)]:
   items=[]
   for x,y in zip(points,points[1:]):
    if x==y:continue
    t=p.PCB_TRACK(b);t.SetStart(p.VECTOR2I(*x));t.SetEnd(p.VECTOR2I(*y));t.SetLayer(p.B_Cu);t.SetWidth(200000);t.SetNetCode(q.GetNetCode());items.append(t)
   if all(clear(t) for t in items):yield items
 poses=[]
 for angle in (90,0,180,270):
  for x in range(90750000,94500001,250000):
   for y in range(1000000,5500001,250000):
    f.SetOrientationDegrees(angle);f.SetPosition(p.VECTOR2I(x,y));q1,q2=pin(f,'1'),pin(f,'2')
    dist=lambda a,b:math.hypot(a.GetPosition().x-b.GetPosition().x,a.GetPosition().y-b.GetPosition().y)/1e6
    d1,d2=dist(q1,pin(u,'1')),dist(q2,pin(u,'56'))
    if max(d1,d2)>3:continue
    if any(q.GetBoundingBox().GetY()<500000 for q in (q1,q2)):continue
    if any(g.intersects(c,e) for c in courts(f) for e in external):continue
    if not all(clear(q) for q in (q1,q2)):continue
    poses.append((d1+d2,d1,d2,x,y,angle))
 poses.sort();print('Eligible poses',len(poses),poses[:12],flush=True)
 counts=Counter()
 for _,d1,d2,x,y,angle in poses:
  f.SetOrientationDegrees(angle);f.SetPosition(p.VECTOR2I(x,y))
  pairs=list(itertools.product(routes(pin(f,'1'),pin(u,'1'),'right'),routes(pin(f,'2'),pin(u,'56'),'top')))
  for signal,ground in pairs:
   items=signal+ground
   if any(t.GetEffectiveShape(p.B_Cu).Collide(v.GetEffectiveShape(p.B_Cu),199990) for t in signal for v in ground):continue
   for t in items:b.Add(t)
   p.ZONE_FILLER(b).Fill(b.Zones());b.BuildConnectivity()
   pads={q.m_Uuid.AsString():q for fp in b.GetFootprints() for q in fp.Pads()}
   cluster=lambda q:frozenset(z.m_Uuid.AsString() for z in b.GetConnectivity().GetConnectedItems(q) if isinstance(z,p.PAD))
   if all(group<=cluster(pads[key]) for key,group in before.items()) and cluster(pin(f,'1'))==cluster(pin(u,'1')):
    out.parent.mkdir(parents=True,exist_ok=True)
    for t in items:
     row=(t.GetNetname(),t.GetStart().x,t.GetStart().y,t.GetEnd().x,t.GetEnd().y)
     t.SetUuid(p.KIID(str(uuid.uuid5(uuid.NAMESPACE_URL,'rgb-badge:ADR0091:R1:'+repr(row)))))
    p.SaveBoard(str(out),b)
    for ext in ('.kicad_pro','.kicad_dru'):shutil.copyfile(source.with_suffix(ext),out.with_suffix(ext))
    report={'SPDX-License-Identifier':'CERN-OHL-S-2.0','status':'IGNORED_LOCALITY_TRIAL_REQUIRES_FULL_DRC','source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'pose':{'reference':'R1','position_iu':[x,y],'angle_deg':angle},'iref_distance_mm':d1,'return_distance_mm':d2,'new_track_count':len(items),'all_parent_groups_preserved':True,'native_opens':b.GetConnectivity().GetUnconnectedCount(False),'fabrication_release_allowed':False}
    out.with_suffix('.json').write_text(json.dumps(report,indent=2)+'\n');print(report,flush=True);return
   counts['pad_group_rejected']+=1
   for t in items:b.Remove(t)
 print('No valid local pose/routes',counts,flush=True);raise SystemExit(1)
if __name__=='__main__':main()
