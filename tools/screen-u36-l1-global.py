#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""ADR 0086 whole-coupon finite two-part native short-node screen."""
from pathlib import Path
from collections import Counter,defaultdict
import argparse,hashlib,json,math,runpy
import pcbnew as p

def main():
    root=Path(__file__).resolve().parents[1]
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--source',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);args=ap.parse_args();source=args.source.resolve();output=args.output.resolve();assert source!=output, 'Output must not overwrite input';assert (root/'hardware/coupon/rev-a/build').resolve() in output.parents and output.suffix=='.json', 'Output must be an ignored build JSON';base=output.parent;base.mkdir(parents=True,exist_ok=True);assert hashlib.sha256(source.read_bytes()).hexdigest()=='db9643801c165fb25c8078816b5cb0a4223c4ddaffa516aae1775392b3a65ded';h=runpy.run_path(str(root/'tools/screen-converter-inductor-locality.py'));g=h['geometry'];box=h['native_box'];cells=h['cells'];overlap=h['overlap'];courts=h['courtyards'];b=p.LoadBoard(str(source));parts={f.GetReference():f for f in b.GetFootprints()};ic,coil=parts['U36'],parts['L1'];assert ic.GetField('MPN').GetText()=='TPS631000DRLR' and coil.GetField('MPN').GetText()=='DFE252012P-1R0M=P2';old_ic=(ic.GetPosition(),ic.GetOrientation().AsDegrees());old_coil=(coil.GetPosition(),coil.GetOrientation().AsDegrees())
    def pad(f,n):return next(q for q in f.Pads() if q.GetNumber()==n)
    def xy(v):return(v.x,v.y)
    def identity(t):return ['pad',t.GetParentFootprint().GetReference(),t.GetNumber()] if isinstance(t,p.PAD) else ['copper',t.GetNetname(),*xy(t.GetStart()),*xy(t.GetEnd())]
    copper=[];cbins=defaultdict(list)
    for t in list(b.GetTracks())+[q for f in b.GetFootprints() if f.GetReference() not in ('U36','L1') for q in f.Pads()]:
     if not t.IsOnLayer(p.B_Cu):continue
     index=len(copper);copper.append((t.GetNetCode(),t.GetEffectiveShape(p.B_Cu),identity(t)))
     for cell in cells(box(t.GetBoundingBox())):cbins[cell].append(index)
    external=[];ebins=defaultdict(list)
    for f in b.GetFootprints():
     if f.GetReference() in ('U36','L1') or f.GetLayer()!=p.B_Cu:continue
     for poly in courts(f):
      q=g.bounds(poly);index=len(external);external.append((f.GetReference(),q,poly))
      for cell in cells(q):ebins[cell].append(index)
    def court_hits(poly):
     q=g.bounds(poly);indices={i for cell in cells(q) for i in ebins[cell]}
     return sorted({external[i][0] for i in indices if overlap(q,external[i][1]) and g.intersects(poly,external[i][2])})
    def hits(t):
     q=t.GetBoundingBox();q.Inflate(200000);indices={i for cell in cells(box(q)) for i in cbins[cell]};shape=t.GetEffectiveShape(p.B_Cu)
     return [copper[i][2] for i in indices if copper[i][0]!=t.GetNetCode() and shape.Collide(copper[i][1],200000)]
    def edges_clear(f):
     for q in f.Pads():
      v=q.GetBoundingBox()
      if v.GetX()<500000 or v.GetY()<500000 or v.GetRight()>113500000 or v.GetBottom()>32000000:return False
     return True
    # Cardinal orientation is selected from actual B-side numbered pad positions.
    coil_templates={}
    for angle in (0,90,180,270):
     coil.SetPosition(old_coil[0]);coil.SetOrientationDegrees(angle);poly=courts(coil);assert len(poly)==1
     coil_templates[angle]=dict(court=[(x-old_coil[0].x,y-old_coil[0].y) for x,y in poly[0]],pad1=(pad(coil,'1').GetPosition().x-old_coil[0].x,pad(coil,'1').GetPosition().y-old_coil[0].y))
    counts=Counter();blockers=Counter();coil_blockers=Counter();clear_IC_poses=[];coil_witnesses=[];best=[];distances=(2650000,2900000,3150000,3400000);tangents=(-250000,0,250000);variants=len(distances)*len(tangents)
    for angle in (0,90,180,270):
     ic.SetPosition(old_ic[0]);ic.SetOrientationDegrees(angle);poly=courts(ic);assert len(poly)==1;offsets=[(x-old_ic[0].x,y-old_ic[0].y) for x,y in poly[0]];q2,q3=pad(ic,'2').GetPosition(),pad(ic,'3').GetPosition();mid=((q2.x+q3.x)//2,(q2.y+q3.y)//2);out=(round((mid[0]-old_ic[0].x)/740000),round((mid[1]-old_ic[0].y)/740000));along=(round((q3.x-q2.x)/500000),round((q3.y-q2.y)/500000));assert sum(abs(x) for x in out)==sum(abs(x) for x in along)==1 and sum(a*z for a,z in zip(out,along))==0
     coil_angle=max(coil_templates,key=lambda a:sum(v*w for v,w in zip(coil_templates[a]['pad1'],along)));coil.SetOrientationDegrees(coil_angle)
     for x in range(1500000,112500001,250000):
      for y in range(1500000,31000001,250000):
       dx,dy=x-old_ic[0].x,y-old_ic[0].y;counts['sampled_templates']+=variants;ip=[(x+a,y+z) for a,z in offsets];ib=g.bounds(ip)
       if ib[0]<0 or ib[1]<0 or ib[2]>114000000 or ib[3]>32500000:counts['IC_courtyard_outside_board']+=variants;continue
       blocked=court_hits(ip)
       if blocked:counts['IC_external_courtyard_blocked']+=variants;blockers.update({ref:variants for ref in blocked});continue
       ic.SetPosition(p.VECTOR2I(x,y))
       if not edges_clear(ic) or any(hits(q) for q in ic.Pads()):counts['IC_pad_or_edge_blocked']+=variants;continue
       clear_IC_poses.append(dict(position_iu=[x,y],angle_deg=ic.GetOrientation().AsDegrees()))
       for distance in distances:
        for tangent in tangents:
         cx=x+out[0]*distance+along[0]*tangent;cy=y+out[1]*distance+along[1]*tangent;cp=[(cx+a,cy+z) for a,z in coil_templates[coil_angle]['court']];q=g.bounds(cp)
         if q[0]<0 or q[1]<0 or q[2]>114000000 or q[3]>32500000:counts['coil_courtyard_outside_board']+=1;continue
         if g.intersects(ip,cp):counts['mutual_courtyard_blocked']+=1;continue
         blocked=court_hits(cp)
         if blocked:
          counts['coil_external_courtyard_blocked']+=1;blockers.update(blocked);coil_blockers.update(blocked);coil_witnesses.append(dict(IC_position_iu=[x,y],IC_angle_deg=ic.GetOrientation().AsDegrees(),coil_position_iu=[cx,cy],coil_angle_deg=coil.GetOrientation().AsDegrees(),blockers=blocked));continue
         coil.SetPosition(p.VECTOR2I(cx,cy))
         if not edges_clear(coil) or any(hits(q) for q in coil.Pads()):counts['coil_pad_or_edge_blocked']+=1;continue
         if any(a.GetNetCode()!=z.GetNetCode() and a.GetEffectiveShape(p.B_Cu).Collide(z.GetEffectiveShape(p.B_Cu),200000) for a in ic.Pads() for z in coil.Pads()):counts['mutual_pad_blocked']+=1;continue
         tracks=[];routes=[];route_hits=[]
         for ic_pin,terminal in [('3','1'),('2','2')]:
          a,z=pad(ic,ic_pin),pad(coil,terminal);assert a.GetNetname()==z.GetNetname();start=xy(a.GetPosition());lead=(start[0]+out[0]*600000,start[1]+out[1]*600000);end=xy(z.GetPosition());points=[start,lead,end];length=sum(math.dist(a,z) for a,z in zip(points,points[1:]))/1e6
          if length>5:route_hits.append(['length_bound']);continue
          local=[]
          for a,z in zip(points,points[1:]):
           t=p.PCB_TRACK(b);t.SetStart(p.VECTOR2I(*a));t.SetEnd(p.VECTOR2I(*z));t.SetWidth(200000);t.SetLayer(p.B_Cu);t.SetNetCode(pad(ic,ic_pin).GetNetCode());bad=hits(t);bad.extend(['mutual_pad',q.GetNumber(),q.GetParentFootprint().GetReference()] for q in list(ic.Pads())+list(coil.Pads()) if q.GetNetCode()!=t.GetNetCode() and t.GetEffectiveShape(p.B_Cu).Collide(q.GetEffectiveShape(p.B_Cu),200000));route_hits.extend(bad);local.append(['track',t.GetNetname(),*a,*z,'B.Cu',200000]);tracks.append(t)
          routes.append(dict(net=pad(ic,ic_pin).GetNetname(),ic_pin=ic_pin,coil_pad=terminal,length_mm=length,tracks=local))
         if any(t.GetNetCode()!=z.GetNetCode() and t.GetEffectiveShape(p.B_Cu).Collide(z.GetEffectiveShape(p.B_Cu),200000) for i,t in enumerate(tracks) for z in tracks[i+1:]):route_hits.append(['mutual_track'])
         if route_hits:counts['local_switching_path_blocked']+=1;continue
         counts['clear_short_switching_templates']+=1;record=dict(U36_position_iu=[x,y],U36_angle_deg=ic.GetOrientation().AsDegrees(),L1_position_iu=[cx,cy],L1_angle_deg=coil.GetOrientation().AsDegrees(),IC_displacement_mm=math.hypot(dx,dy)/1e6,outward_distance_mm=distance/1e6,tangential_offset_mm=tangent/1e6,routes=routes)
         score=(record['IC_displacement_mm'],min((angle-180)%360,(180-angle)%360),sum(z['length_mm'] for z in routes),x,y,coil_angle,distance,tangent)
         best.append((score,record));best=sorted(best,key=lambda row:row[0])[:20]
     ic.SetPosition(old_ic[0]);print('ANGLE',angle,dict(counts),'retained',len(best),flush=True)
    ic.SetPosition(old_ic[0]);ic.SetOrientationDegrees(old_ic[1]);coil.SetPosition(old_coil[0]);coil.SetOrientationDegrees(old_coil[1])
    report=dict(search_region_mm={'x':[1.5,112.5],'y':[1.5,31.0],'grid':0.25},status='UNSELECTED_FINITE_U36_L1_PAIR_TEMPLATE_SCREEN_PENDING_FILLED_GROUP_AND_FULL_DRC_PROOF',source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),tool_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),counts=dict(counts),courtyard_blockers=dict(blockers),coil_only_courtyard_blockers=dict(coil_blockers),native_clear_IC_poses=clear_IC_poses,coil_courtyard_rejection_witnesses=coil_witnesses,retained_best_clear_templates=[record for score,record in best],maximum_retained_clear_templates=20,source_unchanged=hashlib.sha256(source.read_bytes()).hexdigest()=='db9643801c165fb25c8078816b5cb0a4223c4ddaffa516aae1775392b3a65ded',fabrication_release_allowed=False);report['SPDX-License-Identifier']='CERN-OHL-S-2.0';output.write_text(json.dumps(report,indent=2,sort_keys=True)+'\n');print('FINAL',dict(counts),'BEST',best[0][1] if best else None,flush=True)


if __name__=="__main__":main()
