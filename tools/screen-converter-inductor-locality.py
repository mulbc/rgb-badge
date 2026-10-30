#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Finite native copper/courtyard screen; never moves accepted PCB source.

Run with KiCad Python. Results are unselected geometry observations, not power,
assembly, thermal or fabrication qualification. Zero results do not prove
impossibility between sampled poses or with a different floorplan.
"""
import argparse
from collections import defaultdict,Counter
import hashlib
import json
from pathlib import Path
import sys
import pcbnew as p

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
import convex_geometry as geometry
SOURCE=ROOT/'hardware/coupon/rev-a/staging/led-routing-progress-trial-114mm.kicad_pcb'
SOURCE_SHA256='95d7b7679319cdd64f8e22d428bd2a78454b91298ca17432d34ede0c824ab214'
BUILD=ROOT/'hardware/coupon/rev-a/build'


def native_box(box):return (box.GetX(),box.GetY(),box.GetRight(),box.GetBottom())
def overlap(a,b):return not(a[2]<b[0] or b[2]<a[0] or a[3]<b[1] or b[3]<a[1])
def cells(box):
    return ((x,y) for x in range(box[0]//1000000,box[2]//1000000+1)
            for y in range(box[1]//1000000,box[3]//1000000+1))
def courtyards(fp):
    fp.BuildCourtyardCaches();poly=fp.GetCourtyard(p.B_CrtYd);result=[]
    for i in range(poly.OutlineCount()):
        assert poly.HoleCount(i)==0, 'Courtyard holes need explicit screening'
        chain=poly.COutline(i)
        points=[(chain.CPoint(j).x,chain.CPoint(j).y) for j in range(chain.PointCount())]
        assert geometry.convex(points), 'Nonconvex courtyard requires another exact screen'
        result.append(points)
    return result


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--source',type=Path,default=SOURCE,help='Exact corrected 59-edge board, including an archived copy')
    ap.add_argument('--output',type=Path,default=BUILD/'converter-locality-59/angled-poses.json')
    ap.add_argument('--step-iu',type=int,default=200000)
    ap.add_argument('--angle-step',type=int,default=15)
    args=ap.parse_args();out=args.output.resolve();source=args.source.resolve()
    assert BUILD.resolve() in out.parents and out.suffix=='.json'
    assert args.step_iu in (100000,200000) and args.angle_step in (15,45,90)
    assert hashlib.sha256(source.read_bytes()).hexdigest()==SOURCE_SHA256
    b=p.LoadBoard(str(source));parts={f.GetReference():f for f in b.GetFootprints()}
    footprint_parts={}
    for ref,mpn in [('L1','DFE252012P-1R0M=P2'),('L2','DFE252012P-1R5M=P2')]:
        f=parts[ref];assert f.GetField('MPN').GetText()==mpn
        assert f.GetFPIDAsString()=='rgb-badge-coupon:L_Murata_DFE252012P' and f.GetLayer()==p.B_Cu
        assert sorted((q.GetNumber(),q.GetFPRelativePosition().x,q.GetFPRelativePosition().y,q.GetSize().x,q.GetSize().y) for q in f.Pads())==[('1',-1000000,0,800000,2000000),('2',1000000,0,800000,2000000)]
        footprint_parts[ref]=dict(mpn=mpn,old_position_iu=[f.GetPosition().x,f.GetPosition().y],old_angle_deg=f.GetOrientation().AsDegrees())
    copper_bins=defaultdict(list);copper=[]
    for item in list(b.GetTracks())+[q for f in b.GetFootprints() if f.GetReference() not in ('L1','L2') for q in f.Pads()]:
        if not item.IsOnLayer(p.B_Cu):continue
        box=native_box(item.GetBoundingBox());index=len(copper)
        copper.append((item.GetNetCode(),item.GetEffectiveShape(p.B_Cu)))
        for cell in cells(box):copper_bins[cell].append(index)
    courtyard_bins=defaultdict(list);courtyard_data=[]
    for f in b.GetFootprints():
        if f.GetReference() in ('L1','L2') or f.GetLayer()!=p.B_Cu:continue
        for poly in courtyards(f):
            box=geometry.bounds(poly);index=len(courtyard_data)
            courtyard_data.append((f.GetReference(),box,poly))
            for cell in cells(box):courtyard_bins[cell].append(index)
    results={}
    for ref,ic in [('L1','U36'),('L2','U37')]:
        f=parts[ref];centre=parts[ic].GetPosition();old=f.GetPosition();old_angle=f.GetOrientation().AsDegrees()
        counts=Counter();blockers=Counter();success=[]
        for rot in range(0,360,args.angle_step):
            f.SetPosition(old);f.SetOrientationDegrees(rot)
            base=courtyards(f);assert len(base)==1
            offsets=[(x-old.x,y-old.y) for x,y in base[0]]
            for dx in range(-8000000,8000001,args.step_iu):
                for dy in range(-8000000,8000001,args.step_iu):
                    if dx*dx+dy*dy>8000000**2:continue
                    x,y=centre.x+dx,centre.y+dy;counts['sampled_poses']+=1
                    poly=[(x+a,y+b) for a,b in offsets];box=geometry.bounds(poly)
                    if box[0]<0 or box[1]<0 or box[2]>114000000 or box[3]>32500000:
                        counts['courtyard_outside_board']+=1;continue
                    indices={i for cell in cells(box) for i in courtyard_bins[cell]}
                    hit={courtyard_data[i][0] for i in indices if overlap(box,courtyard_data[i][1]) and geometry.intersects(poly,courtyard_data[i][2])}
                    if hit:
                        counts['courtyard_obstructed']+=1;blockers.update(hit);continue
                    counts['courtyard_clear']+=1;f.SetPosition(p.VECTOR2I(x,y));clear=True
                    for q in f.Pads():
                        qb=q.GetBoundingBox()
                        if qb.GetX()<500000 or qb.GetY()<500000 or qb.GetRight()>113500000 or qb.GetBottom()>32000000:
                            clear=False;break
                        qb.Inflate(200000);candidates={i for cell in cells(native_box(qb)) for i in copper_bins[cell]}
                        shape=q.GetEffectiveShape(p.B_Cu)
                        if any(net!=q.GetNetCode() and shape.Collide(other,200000) for net,other in (copper[i] for i in candidates)):
                            clear=False;break
                    if not clear:counts['pad_copper_or_edge_obstructed']+=1;continue
                    counts['pad_and_courtyard_clear']+=1
                    distances=[]
                    for q in f.Pads():
                        targets=[z for z in parts[ic].Pads() if z.GetNetname()==q.GetNetname()]
                        distances.append(min(((q.GetPosition().x-z.GetPosition().x)**2+(q.GetPosition().y-z.GetPosition().y)**2)**.5/1e6 for z in targets))
                    success.append(dict(position_iu=[x,y],angle_deg=rot,pad_centre_distances_mm=distances))
        f.SetPosition(old);f.SetOrientationDegrees(old_angle)
        results[ref]=dict(counts=dict(counts),courtyard_blockers=dict(sorted(blockers.items())),clear_poses=success)
        print(ref,dict(counts),'clear poses',len(success),flush=True)
    report=dict(status='UNSELECTED_FINITE_INDUCTOR_LOCALITY_SCREEN_NOT_HARDWARE_MEASUREMENTS',
                source_sha256=SOURCE_SHA256,kicad_version=p.GetBuildVersion(),step_iu=args.step_iu,
                angle_step_deg=args.angle_step,radius_iu=8000000,clearance_iu=200000,
                copper_edge_clearance_iu=500000,footprint_parts=footprint_parts,results=results,
                source_unchanged=hashlib.sha256(source.read_bytes()).hexdigest()==SOURCE_SHA256,
                fabrication_release_allowed=False,limitations=['Finite sampled positions/angles only',
                    'No route, refill, current, bypass, return or thermal acceptance implied',
                    'Centre distances are planning observations, not pad-edge routing lower bounds'])
    report['SPDX-License-Identifier']='CERN-OHL-S-2.0'
    report['tool_sha256']={str(path.relative_to(ROOT)):hashlib.sha256(path.read_bytes()).hexdigest()
        for path in [Path(__file__),ROOT/'tools/convex_geometry.py']}
    out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')

if __name__=='__main__':main()
