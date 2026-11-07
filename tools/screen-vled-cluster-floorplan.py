#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""ADR 0072 finite rigid courtyard/copper screen; no PCB source is saved."""
import argparse
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path
import runpy
import pcbnew as p
import convex_geometry as g

ROOT = Path(__file__).resolve().parents[1]
helpers = runpy.run_path(str(ROOT/'tools/screen-converter-inductor-locality.py'))
courtyards, cells, overlap, native_box = (helpers[n] for n in ('courtyards','cells','overlap','native_box'))
SOURCE = ROOT/'hardware/coupon/rev-a/staging/led-routing-progress-trial-114mm.kicad_pcb'
SOURCE_SHA256 = '3451177253a021d8706ff818696212afabf539a108f15ef9e5d6921e46435acc'
TEMPLATE = ROOT/'hardware/coupon/rev-a/staging/vled-layout-trial.kicad_pcb'
TEMPLATE_SHA256 = '8907f5d51f93211c5d67e74254ece1e54f7e37bc4bd41e7e03c4ecb85d956cec'
BUILD = ROOT/'hardware/coupon/rev-a/build'
REFS = {'U37','L2','C63',*('C'+str(n) for n in range(44,50)),*('R'+str(n) for n in range(84,88))}


def xy(pt): return [pt.x,pt.y]
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--source',type=Path,default=SOURCE)
    ap.add_argument('--output',type=Path,default=BUILD/'converter-floorplan-58/vled-rigid-screen.json')
    args = ap.parse_args(); source=args.source.resolve(); output=args.output.resolve()
    assert BUILD.resolve() in output.parents and output.suffix=='.json'
    assert sha(source)==SOURCE_SHA256 and sha(TEMPLATE)==TEMPLATE_SHA256
    board=p.LoadBoard(str(source)); template=p.LoadBoard(str(TEMPLATE))
    parts={f.GetReference():f for f in board.GetFootprints()}
    old={('C63' if f.GetReference()=='C50' else f.GetReference()):f for f in template.GetFootprints()}
    assert set(old)==REFS
    assert parts['U37'].GetField('MPN').GetText()=='TPS63020DSJT'
    assert parts['L2'].GetField('MPN').GetText()=='DFE252012P-1R5M=P2'
    origin=p.VECTOR2I(old['U37'].GetPosition())
    initial={r:dict(position_iu=xy(parts[r].GetPosition()),angle_deg=parts[r].GetOrientation().AsDegrees(),
                    mpn=parts[r].GetField('MPN').GetText(),footprint=parts[r].GetFPIDAsString()) for r in sorted(REFS)}
    base={}
    for ref in sorted(REFS):
        old[ref].Flip(origin,p.FLIP_DIRECTION_TOP_BOTTOM)
        f=parts[ref]; assert f.GetLayer()==p.B_Cu and old[ref].GetLayer()==p.B_Cu
        base[ref]=(old[ref].GetPosition()-origin,old[ref].GetOrientation().AsDegrees())
    fixed=[]; fixed_bins=defaultdict(list)
    for f in board.GetFootprints():
        if f.GetReference() in REFS or f.GetLayer()!=p.B_Cu: continue
        for poly in courtyards(f):
            box=g.bounds(poly); index=len(fixed); fixed.append((f.GetReference(),box,poly))
            for cell in cells(box): fixed_bins[cell].append(index)
    copper=[]; copper_bins=defaultdict(list)
    for item in list(board.GetTracks())+[q for f in board.GetFootprints() if f.GetReference() not in REFS for q in f.Pads()]:
        if not item.IsOnLayer(p.B_Cu): continue
        index=len(copper); copper.append((item.GetNetCode(),item.GetEffectiveShape(p.B_Cu)))
        for cell in cells(native_box(item.GetBoundingBox())): copper_bins[cell].append(index)
    counts=Counter(); histogram=Counter(); common=Counter(); best=[]; best_n=None; clear=[]; rotations=[]
    for rotation in (0,90,180,270):
        cluster=[]
        for ref,(pos,angle) in base.items():
            f=parts[ref]; f.SetPosition(pos); f.SetOrientationDegrees(angle)
            f.Rotate(p.VECTOR2I(0,0),p.EDA_ANGLE(rotation,p.DEGREES_T))
            for poly in courtyards(f): cluster.append((ref,g.bounds(poly),poly))
        internal=[]
        for i,(ref,box,poly) in enumerate(cluster):
            for other,other_box,other_poly in cluster[i+1:]:
                if ref!=other and overlap(box,other_box) and g.intersects(poly,other_poly): internal.append([ref,other])
        assert not internal, ('Template internal courtyard obstruction',rotation,internal)
        bounds=g.bounds([v for _,_,poly in cluster for v in poly])
        poses={r:(p.VECTOR2I(parts[r].GetPosition()),parts[r].GetOrientation().AsDegrees()) for r in REFS}
        rotations.append(dict(rotation_deg=rotation,relative_courtyard_bounds_iu=list(bounds),internal_courtyard_obstructions=internal))
        for x in range(0,114000001,500000):
            for y in range(0,32500001,500000):
                counts['sampled_poses']+=1
                if bounds[0]+x<0 or bounds[1]+y<0 or bounds[2]+x>114000000 or bounds[3]+y>32500000:
                    counts['courtyard_outside_board']+=1; continue
                counts['courtyard_inside_board']+=1; hit=set()
                for ref,box,poly in cluster:
                    box=(box[0]+x,box[1]+y,box[2]+x,box[3]+y)
                    translated=[(a+x,b+y) for a,b in poly]
                    indices={i for cell in cells(box) for i in fixed_bins[cell]}
                    hit.update(fixed[i][0] for i in indices if overlap(box,fixed[i][1]) and g.intersects(translated,fixed[i][2]))
                histogram[len(hit)]+=1; common.update(hit)
                if best_n is None or len(hit)<best_n: best_n=len(hit); best=[]
                if len(hit)==best_n and len(best)<20:
                    best.append(dict(ic_position_iu=[x,y],rotation_deg=rotation,fixed_courtyard_blockers=sorted(hit)))
                if hit: counts['courtyard_obstructed']+=1; continue
                counts['courtyard_clear']+=1; pad_clear=True
                for ref,(pos,angle) in poses.items():
                    f=parts[ref]; f.SetPosition(p.VECTOR2I(pos.x+x,pos.y+y)); f.SetOrientationDegrees(angle)
                    for q in f.Pads():
                        if not q.IsOnLayer(p.B_Cu): continue
                        box=q.GetBoundingBox()
                        if box.GetX()<500000 or box.GetY()<500000 or box.GetRight()>113500000 or box.GetBottom()>32000000:
                            pad_clear=False; break
                        box.Inflate(200000)
                        indices={i for cell in cells(native_box(box)) for i in copper_bins[cell]}
                        shape=q.GetEffectiveShape(p.B_Cu)
                        if any(net!=q.GetNetCode() and shape.Collide(other,200000) for net,other in (copper[i] for i in indices)):
                            pad_clear=False; break
                    if not pad_clear: break
                if not pad_clear: counts['pad_copper_or_edge_obstructed']+=1; continue
                counts['pad_and_courtyard_clear']+=1
                clear.append(dict(ic_position_iu=[x,y],rotation_deg=rotation,
                    poses={r:dict(position_iu=[pos.x+x,pos.y+y],angle_deg=angle) for r,(pos,angle) in poses.items()}))
        print(rotation,dict(counts),'minimum fixed blockers',best_n,flush=True)
    report=dict(status='UNSELECTED_FINITE_RIGID_VLED_PACKING_SCREEN_NOT_LAYOUT_ACCEPTANCE',
        source_sha256=SOURCE_SHA256,template_sha256=TEMPLATE_SHA256,kicad_version=p.GetBuildVersion(),
        counts=dict(counts),fixed_courtyard_blocker_histogram=dict(sorted(histogram.items())),
        fixed_courtyard_observations=dict(sorted(common.items())),minimum_fixed_courtyard_blockers=best_n,
        minimum_blocker_examples=best,clear_poses=clear,initial_parts=initial,rotations=rotations,
        grid_step_iu=500000,clearance_iu=200000,copper_edge_clearance_iu=500000,
        source_unchanged=sha(source)==SOURCE_SHA256,template_unchanged=sha(TEMPLATE)==TEMPLATE_SHA256,
        fabrication_release_allowed=False,
        limitations=['Finite rigid historical template only; no proof against other arrangements or between samples',
                     'Historical poses only; current footprints/pads/nets/MPNs retained',
                     'Filled zones excluded from copper clearance screening',
                     'No old-contact reconnection, routing, refill, DRC, current, thermal, EMI or layout acceptance'])
    report['SPDX-License-Identifier']='CERN-OHL-S-2.0'
    report['tool_sha256']={str(path.relative_to(ROOT)):sha(path) for path in [Path(__file__),ROOT/'tools/convex_geometry.py',ROOT/'tools/screen-converter-inductor-locality.py']}
    output.parent.mkdir(parents=True,exist_ok=True); output.write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')


if __name__=='__main__': main()
