#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""ADR0092 direct full-span plane joins; ignored output, no fabrication permission."""
import argparse,hashlib,json,math,runpy,shutil,uuid
from collections import defaultdict,Counter
from pathlib import Path
import pcbnew as p
import routing_closure as policy
from routing_zone_targets import connected_polygons
ROOT=policy.ROOT;BUILD=ROOT/'hardware/coupon/rev-a/build'
LAYERS=(p.F_Cu,p.In1_Cu,p.In2_Cu,p.In3_Cu,p.In4_Cu,p.B_Cu)

def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--source',type=Path,default=policy.OUTPUT);ap.add_argument('--output',type=Path,required=True);ap.add_argument('--nets',nargs='*');args=ap.parse_args()
 source,out=args.source.resolve(),args.output.resolve();assert BUILD.resolve() in out.parents and out!=source
 source_sha=policy.sha(source);b=p.LoadBoard(str(source));profile=json.loads(source.with_suffix('.kicad_pro').read_text());rules=profile['board']['design_settings']['rules'];assert rules['min_hole_to_hole']==rules['min_hole_clearance']==.25
 permitted=p.SHAPE_POLY_SET();assert b.GetBoardPolygonOutlines(permitted,False)
 permitted.Inflate(-751000,p.CORNER_STRATEGY_ROUND_ALL_CORNERS,1000)
 pads=[q for f in b.GetFootprints() for q in f.Pads()];by_net=defaultdict(list)
 for q in pads:
  if q.GetNetname():by_net[q.GetNetname()].append(q)
 cluster=lambda q:frozenset(z.m_Uuid.AsString() for z in b.GetConnectivity().GetConnectedItems(q) if isinstance(z,p.PAD))
 def all_groups():
  result={}
  for q in pads:
   if q.GetNetname():result.setdefault(cluster(q),q)
  return result
 def physical_opens():return sum(len({cluster(q) for q in qs})-1 for qs in by_net.values())
 def cells(box):return [(x,y) for x in range(box.GetX()//1000000,box.GetRight()//1000000+1) for y in range(box.GetY()//1000000,box.GetBottom()//1000000+1)]
 bins=defaultdict(list);holes=defaultdict(list)
 def rebuild():
  bins.clear();holes.clear()
  for item in list(b.GetTracks())+pads:
   box=item.GetBoundingBox();box.Inflate(501000)
   for l in LAYERS:
    if item.IsOnLayer(l):
     for cell in cells(box):bins[(l,*cell)].append(item)
   if isinstance(item,p.PCB_VIA) or (isinstance(item,p.PAD) and max(item.GetDrillSize().x,item.GetDrillSize().y)>0):
    for cell in cells(box):holes[cell].append(item)
 rebuild()
 def clear(v):
  box=v.GetBoundingBox()
  for l in LAYERS:
   obs={o.m_Uuid.AsString():o for cell in cells(box) for o in bins[(l,*cell)]}
   if any(o.GetNetCode()!=v.GetNetCode() and v.GetEffectiveShape(l).Collide(o.GetEffectiveShape(l),199990) for o in obs.values()):return False
  oldholes={o.m_Uuid.AsString():o for cell in cells(box) for o in holes[cell]}
  return not any(v.GetEffectiveHoleShape().Collide(o.GetEffectiveHoleShape(),250000) for o in oldholes.values())
 initial=b.GetConnectivity().GetUnconnectedCount(False);assert initial==physical_opens()
 routes=[];statistics=Counter();out.parent.mkdir(parents=True,exist_ok=True)
 names=sorted(by_net,key=lambda n:(n not in ('GND','VLED','+3V3_USB','+BAT_GAUGE_SW'),n))
 for name in names:
  if args.nets and name not in args.nets:continue
  qs=sorted(by_net[name],key=lambda q:(q.GetParentFootprint().GetReference(),q.GetNumber(),q.GetPosition().x,q.GetPosition().y))
  for q in qs:
   group=cluster(q);other_groups={cluster(x):x for x in qs if cluster(x)!=group}
   if not other_groups:break
   layer=q.GetLayer()
   if layer not in (p.B_Cu,p.F_Cu):continue
   reached=set();regions=[]
   for anchor in other_groups.values():
    reached.update(x.m_Uuid.AsString() for x in b.GetConnectivity().GetConnectedItems(anchor));regions.extend(connected_polygons(b,anchor))
   targets=[o for o in list(b.GetTracks())+pads if o.m_Uuid.AsString() in reached and o.GetNetCode()==q.GetNetCode()]
   bb=q.GetBoundingBox();cx,cy=q.GetPosition().x,q.GetPosition().y
   # Search actual land interiors. No assumed pad-centre/grid equivalence.
   coords={(cx,cy)}|{(x,y) for x in range(bb.GetX(),bb.GetRight()+1,50000) for y in range(bb.GetY(),bb.GetBottom()+1,50000)}
   coords=sorted(coords,key=lambda xy:(math.dist(xy,(cx,cy)),xy))
   accepted=False
   for x,y in coords:
    pos=p.VECTOR2I(x,y)
    if not permitted.Contains(pos) or not q.GetEffectiveShape(layer).Collide(p.SHAPE_CIRCLE(pos,1),0):continue
    v=p.PCB_VIA(b);v.SetPosition(pos);v.SetViaType(p.VIATYPE_THROUGH);v.SetLayerPair(p.F_Cu,p.B_Cu);v.SetWidth(500000);v.SetDrill(300000);v.SetNetCode(q.GetNetCode());v.SetUuid(p.KIID(str(uuid.uuid5(uuid.NAMESPACE_URL,'rgb-badge:ADR0092:'+source_sha+repr((name,x,y))))))
    if not clear(v):statistics['capture_or_hole_obstructed']+=1;continue
    vb=v.GetBoundingBox()
    # A geometrically plausible, separately copper-witnessed destination is
    # required before spending a refill on this candidate.
    touches=any(vb.Intersects(unit.BBox()) and unit.Collide(v.GetEffectiveShape(l),0) for l,unit,_,_,_ in regions)
    if not touches:
     touches=any(vb.Intersects(o.GetBoundingBox()) and any(o.IsOnLayer(l) and v.GetEffectiveShape(l).Collide(o.GetEffectiveShape(l),0) for l in LAYERS) for o in targets)
    if not touches:statistics['no_other_group_copper_contact']+=1;continue
    groups=all_groups();before=b.GetConnectivity().GetUnconnectedCount(False);b.Add(v);p.ZONE_FILLER(b).Fill(b.Zones());b.BuildConnectivity();after=b.GetConnectivity().GetUnconnectedCount(False)
    valid=after<before and group<cluster(q) and all(g<=cluster(anchor) for g,anchor in groups.items()) and physical_opens()==after
    if valid:
     row={'net':name,'source':[q.GetParentFootprint().GetReference(),q.GetNumber()],'position_iu':[x,y],'native_opens_before':before,'native_opens_after':after,'physical_opens_after':after,'all_prior_live_groups_preserved':True,'via':list(policy.signature(b,v))};routes.append(row);print(row,flush=True);accepted=True;rebuild();p.SaveBoard(str(out),b)
     for ext in ('.kicad_pro','.kicad_dru'):shutil.copyfile(source.with_suffix(ext),out.with_suffix(ext))
     break
    statistics['refill_or_join_guard_rejected']+=1;b.Remove(v);p.ZONE_FILLER(b).Fill(b.Zones());b.BuildConnectivity();assert b.GetConnectivity().GetUnconnectedCount(False)==before and all(g<=cluster(anchor) for g,anchor in groups.items())
   if not accepted:print('NO DIRECT THROUGH JOIN',name,q.GetParentFootprint().GetReference(),q.GetNumber(),flush=True)
 assert policy.sha(source)==source_sha
 p.SaveBoard(str(out),b)
 for ext in ('.kicad_pro','.kicad_dru'):shutil.copyfile(source.with_suffix(ext),out.with_suffix(ext))
 result={'SPDX-License-Identifier':'CERN-OHL-S-2.0','status':'UNSELECTED_FULL_SPAN_PLANE_JOIN_TRIAL','source_sha256':source_sha,'board_sha256':policy.sha(out),'native_opens_before':initial,'native_opens':b.GetConnectivity().GetUnconnectedCount(False),'physical_opens':physical_opens(),'full_span_pad_drill_iu':[500000,300000],'minimum_hole_gap_iu':250000,'routes':routes,'statistics':dict(statistics),'fabrication_release_allowed':False,'tool_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
 out.with_suffix('.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print('Saved direct-plane trial',result['native_opens'],'opens,',len(routes),'new through vias',flush=True)
if __name__=='__main__':main()
