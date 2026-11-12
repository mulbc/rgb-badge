#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""ADR 0118 finite read-only U49 proximity screen; no PCB is saved."""
from collections import Counter,defaultdict
import argparse
import hashlib
import json
from pathlib import Path
import runpy
import pcbnew as p

ROOT=Path(__file__).resolve().parents[1]
HELPERS=runpy.run_path(str(ROOT/'tools/screen-converter-inductor-locality.py'))
g=HELPERS['geometry']
courtyards,cells,overlap,native_box=(HELPERS[n] for n in ('courtyards','cells','overlap','native_box'))
SOURCE=ROOT/'hardware/coupon/rev-a/staging/led-rse-corrected-routing-trial-114mm.kicad_pcb'
SOURCE_SHA='3967bb66e89e0005f6859ce78a766b4536d06883b76fce130e75a6fdeefaf96e'


def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--output',type=Path,required=True)
    args=ap.parse_args();out=args.output.resolve();assert (ROOT/'hardware/coupon/rev-a/build').resolve() in out.parents
    assert out.suffix=='.json' and sha(SOURCE)==SOURCE_SHA
    b=p.LoadBoard(str(SOURCE));parts={f.GetReference():f for f in b.GetFootprints()}
    f=parts['U49'];centre=parts['U48'].GetPosition();old=p.VECTOR2I(f.GetPosition());angle=f.GetOrientation().AsDegrees()
    assert f.GetValue()=='SN74LVC1G74RSER' and f.GetField('MPN').GetText()==f.GetValue()
    assert f.GetLayer()==p.B_Cu
    assert {q.GetNumber():q.GetNetname() for q in f.Pads()}=={
        '1':'+3V3_APP','2':'DISPLAY_CLEAR_OK','3':'HEARTBEAT_SEEN','4':'GND',
        '5':'','6':'+3V3_APP','7':'HEARTBEAT_FALL_CLK','8':'+3V3_APP'}
    fixed=[];fixed_bins=defaultdict(list)
    for part in b.GetFootprints():
        if part.GetReference()=='U49' or part.GetLayer()!=p.B_Cu:continue
        for poly in courtyards(part):
            box=g.bounds(poly);i=len(fixed);fixed.append((part.GetReference(),box,poly))
            for cell in cells(box):fixed_bins[cell].append(i)
    copper=[];copper_bins=defaultdict(list)
    for item in list(b.GetTracks())+[q for part in b.GetFootprints() if part.GetReference()!='U49' for q in part.Pads()]:
        if not item.IsOnLayer(p.B_Cu):continue
        i=len(copper);copper.append((item.GetNetCode(),item.GetEffectiveShape(p.B_Cu),item.m_Uuid.AsString()))
        for cell in cells(native_box(item.GetBoundingBox())):copper_bins[cell].append(i)
    counts=Counter();blockers=Counter();clear=[];witnesses=[];best=[];best_count=None
    for rotation in (0,90,180,270):
        f.SetPosition(old);f.SetOrientationDegrees(rotation);polys=courtyards(f);assert len(polys)==1
        offsets=[(x-old.x,y-old.y) for x,y in polys[0]]
        for dx in range(-8000000,8000001,100000):
            for dy in range(-8000000,8000001,100000):
                if dx*dx+dy*dy>8000000**2:continue
                x,y=centre.x+dx,centre.y+dy;counts['sampled']+=1
                poly=[(x+a,y+c) for a,c in offsets];box=g.bounds(poly)
                if box[0]<0 or box[1]<0 or box[2]>114000000 or box[3]>32500000:
                    counts['courtyard_outside_board']+=1;continue
                indices={i for cell in cells(box) for i in fixed_bins[cell]}
                hit=sorted({fixed[i][0] for i in indices if overlap(box,fixed[i][1]) and g.intersects(poly,fixed[i][2])})
                blockers.update(hit)
                if best_count is None or len(hit)<best_count:best_count=len(hit);best=[]
                if len(hit)==best_count and len(best)<20:best.append(dict(position_iu=[x,y],angle_deg=rotation,blockers=hit))
                if hit:counts['courtyard_obstructed']+=1;continue
                counts['courtyard_clear']+=1;f.SetPosition(p.VECTOR2I(x,y));reason=None
                for q in f.Pads():
                    qb=q.GetBoundingBox()
                    if qb.GetX()<500000 or qb.GetY()<500000 or qb.GetRight()>113500000 or qb.GetBottom()>32000000:
                        reason=dict(pad=q.GetNumber(),reason='COPPER_EDGE');break
                    qb.Inflate(200000);indices={i for cell in cells(native_box(qb)) for i in copper_bins[cell]}
                    shape=q.GetEffectiveShape(p.B_Cu)
                    hits=[copper[i][2] for i in indices if copper[i][0]!=q.GetNetCode() and shape.Collide(copper[i][1],200000)]
                    if hits:reason=dict(pad=q.GetNumber(),reason='FOREIGN_COPPER',items=hits);break
                if reason:
                    counts['pad_or_edge_obstructed']+=1
                    if len(witnesses)<512:witnesses.append(dict(position_iu=[x,y],angle_deg=rotation,**reason))
                    continue
                clock=next(q for q in f.Pads() if q.GetNumber()=='7').GetPosition()
                target=next(q for q in parts['U48'].Pads() if q.GetNumber()=='4').GetPosition()
                distance=((clock.x-target.x)**2+(clock.y-target.y)**2)**.5/1e6
                clear.append(dict(position_iu=[x,y],angle_deg=rotation,clock_pad_distance_mm=distance))
                counts['pad_and_courtyard_clear']+=1
        print(rotation,dict(counts),flush=True)
    f.SetPosition(old);f.SetOrientationDegrees(angle)
    result={'SPDX-License-Identifier':'CERN-OHL-S-2.0','status':'READ_ONLY_FINITE_SCREEN_NOT_LAYOUT_ACCEPTANCE',
        'source_sha256':SOURCE_SHA,'source_unchanged':sha(SOURCE)==SOURCE_SHA,'kicad_version':p.GetBuildVersion(),
        'step_iu':100000,'radius_iu':8000000,'clearance_iu':200000,'copper_edge_iu':500000,
        'counts':dict(counts),'fixed_courtyard_blockers':dict(blockers),'minimum_courtyard_blocker_count':best_count,
        'minimum_blocker_examples':best,'clear_poses':sorted(clear,key=lambda q:q['clock_pad_distance_mm']),
        'copper_rejection_witnesses':witnesses,'fabrication_release_allowed':False,
        'tool_sha256':{str(Path(__file__).relative_to(ROOT)):sha(Path(__file__))},
        'limitations':['Finite samples only, not proof of impossibility','Filled zones excluded; native refills still required',
                       'No support/bypass relocation, contact restoration, routing or DRC acceptance','No PCB saved or source modified']}
    out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')


if __name__=='__main__':main()
