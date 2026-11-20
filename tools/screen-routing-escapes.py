#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Read-only native obstacle witnesses for ADR0091 trapped-pad escapes.

This identifies bounded replacement candidates, never permission to delete their
copper. Actual replacements require exact direct-contact and all-pad-group proofs,
refill, completed net joins and full native DRC before checkpoint selection.
"""
import argparse,hashlib,json,math
from collections import defaultdict,Counter
from pathlib import Path
import pcbnew as p
import routing_closure as policy
ROOT=policy.ROOT
BUILD=ROOT/'hardware/coupon/rev-a/build'

def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--source',type=Path,default=policy.OUTPUT);ap.add_argument('--output',type=Path,required=True);ap.add_argument('--nets',nargs='*');ap.add_argument('--references',nargs='*');ap.add_argument('--step-um',type=int,default=100);args=ap.parse_args()
 source,out=args.source.resolve(),args.output.resolve();assert BUILD.resolve() in out.parents and out!=source;assert 25<=args.step_um<=200
 before=policy.sha(source);b=p.LoadBoard(str(source));items=list(b.GetTracks())+[q for f in b.GetFootprints() for q in f.Pads()];bins=defaultdict(list)
 def cells(box):return [(x,y) for x in range(box.GetX()//1000000,box.GetRight()//1000000+1) for y in range(box.GetY()//1000000,box.GetBottom()//1000000+1)]
 for o in items:
  bb=o.GetBoundingBox();bb.Inflate(400000)
  for l in (p.B_Cu,p.In4_Cu):
   if o.IsOnLayer(l):
    for cell in cells(bb):bins[(l,*cell)].append(o)
 def hits(t):
  result={}
  for l in (p.B_Cu,p.In4_Cu):
   if not t.IsOnLayer(l):continue
   obs={o.m_Uuid.AsString():o for cell in cells(t.GetBoundingBox()) for o in bins[(l,*cell)]}
   for uid,o in obs.items():
    if o.GetNetCode()==t.GetNetCode():continue
    if t.GetEffectiveShape(l).Collide(o.GetEffectiveShape(l),199990):result[uid]=o
  return result
 nets=defaultdict(list)
 for fp in b.GetFootprints():
  for q in fp.Pads():
   if q.GetNetname():nets[q.GetNetname()].append(q)
 cluster=lambda q:frozenset(z.m_Uuid.AsString() for z in b.GetConnectivity().GetConnectedItems(q) if isinstance(z,p.PAD))
 records=[]
 for net,pads in sorted(nets.items()):
  if args.nets and net not in args.nets:continue
  groups=defaultdict(list)
  for q in pads:groups[cluster(q)].append(q)
  if len(groups)<=1:continue
  anchor=max(groups,key=len)
  for group,qs in groups.items():
   if group==anchor and not args.references:continue
   qs.sort(key=lambda q:(q.GetParentFootprint().GetReference(),q.GetNumber()))
   for q in qs:
    if args.references and q.GetParentFootprint().GetReference() not in args.references:continue
    if not q.IsOnLayer(p.B_Cu):continue
    bb=q.GetBoundingBox();cx,cy=q.GetPosition().x,q.GetPosition().y
    starts=[(cx,cy),(bb.GetX(),cy),(bb.GetRight(),cy),(cx,bb.GetY()),(cx,bb.GetBottom())]
    best={};counts=Counter()
    for x in range(cx-1000000,cx+1000001,args.step_um*1000):
     for y in range(cy-1000000,cy+1000001,args.step_um*1000):
      if not(650000<=x<=113350000 and 650000<=y<=31850000):continue
      v=p.PCB_VIA(b);v.SetPosition(p.VECTOR2I(x,y));v.SetViaType(p.VIATYPE_MICROVIA);v.SetLayerPair(p.In4_Cu,p.B_Cu);v.SetWidth(300000);v.SetDrill(100000);v.SetNetCode(q.GetNetCode());vh=hits(v)
      if any(not isinstance(o,p.PCB_TRACK) or isinstance(o,p.PCB_VIA) for o in vh.values()):counts['immutable_via_site']+=1;continue
      lead_starts=[None] if v.GetEffectiveShape(p.B_Cu).Collide(q.GetEffectiveShape(p.B_Cu),0) else starts
      for start in lead_starts:
       t=p.PCB_TRACK(b);t.SetStart(p.VECTOR2I(*(start or (x,y))));t.SetEnd(p.VECTOR2I(x,y));t.SetWidth(200000);t.SetLayer(p.B_Cu);t.SetNetCode(q.GetNetCode());obstacles=dict(vh);obstacles.update(hits(t) if start else {})
       if any(not isinstance(o,p.PCB_TRACK) or isinstance(o,p.PCB_VIA) for o in obstacles.values()):counts['immutable_lead']+=1;continue
       if len(obstacles)>2:counts['more_than_two_tracks']+=1;continue
       if any(o.GetWidth()!=200000 or not o.GetNetname().startswith(('COL_','ROW_SEL_','ROW_GATE_')) for o in obstacles.values()):counts['outside_replacement_scope']+=1;continue
       key=tuple(sorted(obstacles));row={'via_position_iu':[x,y],'lead_start_iu':list(start) if start else None,'lead_end_iu':[x,y],'blockers':[{'uuid':uid,'signature':list(policy.signature(b,o))} for uid,o in sorted(obstacles.items())],'lead_length_mm':math.dist(start,(x,y))/1e6 if start else 0}
       score=(len(obstacles),row['lead_length_mm'],x,y)
       if key not in best or score<best[key][0]:best[key]=(score,row)
    rows=[row for _,row in sorted(best.values(),key=lambda r:r[0])[:8]]
    entry={'net':net,'reference':q.GetParentFootprint().GetReference(),'pin':q.GetNumber(),'group_pad_count':len(group),'candidates':rows,'rejected_counts':dict(counts)};records.append(entry)
    print(net,entry['reference'],entry['pin'],'candidate obstacle counts',[len(row['blockers']) for row in rows],flush=True)
 assert policy.sha(source)==before
 out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps({'SPDX-License-Identifier':'CERN-OHL-S-2.0','status':'READ_ONLY_ESCAPE_OBSTACLE_SCREEN','source_sha256':before,'tool_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'fabrication_release_allowed':False,'records':records},indent=2,sort_keys=True)+'\n')
if __name__=='__main__':main()
