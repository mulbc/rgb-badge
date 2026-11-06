#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Finite nine-part stage screen with U36/L1 fixed; selected PCB is never edited."""
import argparse
from collections import Counter, defaultdict
import hashlib
import json
import math
from pathlib import Path
import runpy
import pcbnew as p

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'hardware/coupon/rev-a/staging/led-converter-routing-trial-114mm.kicad_pcb'
SHA = '5e07fb866cc059de670e34102045d9dfd88c88f101355fcdbb27253c0ae26e43'
MOVING = ['C40', 'C41', 'C42', 'C43', 'R81', 'R82', 'R83']


def screen(ic_pose=None, rotation=0):
    assert hashlib.sha256(SOURCE.read_bytes()).hexdigest() == SHA
    h = runpy.run_path(str(ROOT / 'tools/screen-converter-inductor-locality.py'))
    g, cells, box, courts = h['geometry'], h['cells'], h['native_box'], h['courtyards']
    b = p.LoadBoard(str(SOURCE)); parts = {f.GetReference(): f for f in b.GetFootprints()}
    if ic_pose is not None:
        centre = parts['U36'].GetPosition()
        delta = parts['L1'].GetPosition() - centre
        radians = math.radians(rotation)
        dx = round(delta.x * math.cos(radians) + delta.y * math.sin(radians))
        dy = round(-delta.x * math.sin(radians) + delta.y * math.cos(radians))
        parts['U36'].SetPosition(p.VECTOR2I(*ic_pose)); parts['U36'].SetOrientationDegrees(180+rotation)
        parts['L1'].SetPosition(p.VECTOR2I(ic_pose[0]+dx,ic_pose[1]+dy)); parts['L1'].SetOrientationDegrees(90+rotation)
    plan=json.loads((ROOT/'mechanical/review/converter-routing-checkpoint-plan.json').read_text())
    ignored_switches=[row for route in plan['app_switching_routes'] for row in route['tracks']] if ic_pose is not None else []
    if ic_pose is not None:
        ignored_switches.append(['track','+SYS_APP_IN_DRAFT',109155000,13250000,108550000,13600000,'B.Cu',200000])
        ignored_switches.append(['track','+3V3_APP',109490000,11600000,109600000,11000000,'B.Cu',200000])
    def old_switch(item):
        if isinstance(item,p.PCB_VIA) or isinstance(item,p.PAD):return False
        row=['track',item.GetNetname(),item.GetStart().x,item.GetStart().y,item.GetEnd().x,item.GetEnd().y,b.GetLayerName(item.GetLayer()),item.GetWidth()]
        return row in ignored_switches
    external, ebins, copper, cbins = [], defaultdict(list), [], defaultdict(list)
    for f in b.GetFootprints():
        if f.GetReference() in MOVING:
            continue
        if f.GetLayer() == p.B_Cu:
            for poly in courts(f):
                index = len(external); external.append((f.GetReference(), poly))
                for cell in cells(g.bounds(poly)): ebins[cell].append(index)
    for t in list(b.GetTracks()) + [q for f in b.GetFootprints() if f.GetReference() not in MOVING for q in f.Pads()]:
        if not t.IsOnLayer(p.B_Cu) or old_switch(t): continue
        index = len(copper)
        copper.append((t.GetNetCode(), t.GetEffectiveShape(p.B_Cu),t.GetParentFootprint().GetReference() if isinstance(t,p.PAD) else None))
        for cell in cells(box(t.GetBoundingBox())): cbins[cell].append(index)
    through_pads=[]
    for fp in b.GetFootprints():
        for q in fp.Pads():
            if q.GetAttribute() in (p.PAD_ATTRIB_PTH,p.PAD_ATTRIB_NPTH):
                bb=q.GetBoundingBox()
                through_pads.append((fp.GetReference(),q.GetNumber(),[(bb.GetX(),bb.GetY()),(bb.GetRight(),bb.GetY()),(bb.GetRight(),bb.GetBottom()),(bb.GetX(),bb.GetBottom())]))
    pin = lambda ref, n: next(q for q in parts[ref].Pads() if q.GetNumber() == n)
    pair_failures=[]
    for ref in ('U36','L1'):
        f=parts[ref]
        for poly in courts(f):
            for other,number,shape in through_pads:
                if g.intersects(poly,shape):pair_failures.append(['through_pad_courtyard',ref,other,number])
            for other,shape in external:
                if other!=ref and g.intersects(poly,shape):pair_failures.append(['courtyard',ref,other])
        for q in f.Pads():
            qb=q.GetBoundingBox();qb.Inflate(200000)
            ids={i for cell in cells(box(qb)) for i in cbins[cell]}
            if any(net!=q.GetNetCode() and origin not in ('U36','L1') and q.GetEffectiveShape(p.B_Cu).Collide(shape,200000) for net,shape,origin in (copper[i] for i in ids)):
                pair_failures.append(['foreign_copper',ref,q.GetNumber()])
    pair_poses={ref:{'position_iu':[parts[ref].GetPosition().x,parts[ref].GetPosition().y],'angle_deg':parts[ref].GetOrientation().AsDegrees()} for ref in ('U36','L1')}
    if pair_failures:
        return {'source_sha256':SHA,'status':'PAIR_POSE_REJECTED','pair_poses':pair_poses,'pair_failures':pair_failures,'fabrication_release_allowed':False}
    targets = {'C40': ('1','4',3), 'C41': ('1','4',6), 'C42': ('1','1',4),
               'C43': ('1','1',6), 'R81': ('2','8',3), 'R82': ('1','8',3), 'R83': ('1','5',3)}
    return_limits={'C40':3.5,'C41':6,'C42':4,'C43':6}
    records, totals = {}, {}
    for ref in MOVING:
        f = parts[ref]; anchor, icpin, maximum = targets[ref]; target = pin('U36', icpin).GetPosition()
        cx, cy = parts['U36'].GetPosition().x, parts['U36'].GetPosition().y
        original = (f.GetPosition(), f.GetOrientation().AsDegrees())
        good, counts, blockers = [], Counter(), Counter()
        step=125000 if ref=='C43' else 250000
        for angle in (0,90,180,270):
            f.SetOrientationDegrees(angle)
            for x in range(cx-6000000, cx+6000001, step):
                for y in range(cy-6000000, cy+6000001, step):
                    counts['sampled'] += 1
                    f.SetPosition(p.VECTOR2I(x,y)); a = pin(ref, anchor).GetPosition()
                    distance = math.hypot(a.x-target.x,a.y-target.y)/1e6
                    if distance > maximum: counts['locality'] += 1; continue
                    return_distance=0
                    if ref in return_limits:
                        q=pin(ref,'2').GetPosition();ground=pin('U36','7').GetPosition()
                        return_distance=math.hypot(q.x-ground.x,q.y-ground.y)/1e6
                        if return_distance>return_limits[ref]:
                            counts['return_locality']+=1;continue
                    polys = courts(f); assert len(polys) == 1
                    poly = polys[0]; bounds = g.bounds(poly)
                    if bounds[0]<0 or bounds[1]<0 or bounds[2]>114000000 or bounds[3]>32500000:
                        counts['edge'] += 1; continue
                    if any(g.intersects(poly,shape) for _,_,shape in through_pads):
                        counts['through_pad_courtyard'] += 1;continue
                    ids = {i for cell in cells(bounds) for i in ebins[cell]}
                    hits = {external[i][0] for i in ids if g.intersects(poly,external[i][1])}
                    if hits:
                        counts['courtyard'] += 1; blockers.update(hits); continue
                    bad = False
                    for q in f.Pads():
                        qb=q.GetBoundingBox()
                        if qb.GetX()<500000 or qb.GetY()<500000 or qb.GetRight()>113500000 or qb.GetBottom()>32000000:
                            bad=True;break
                        qb.Inflate(200000)
                        ids={i for cell in cells(box(qb)) for i in cbins[cell]}
                        if any(net!=q.GetNetCode() and q.GetEffectiveShape(p.B_Cu).Collide(shape,200000) for net,shape,_ in (copper[i] for i in ids)):
                            bad=True; break
                    if bad: counts['foreign_copper'] += 1; continue
                    counts['clear'] += 1
                    good.append({'position_iu':[x,y],'angle_deg':angle,'anchor_distance_mm':distance,'return_distance_mm':return_distance,'court':poly})
        f.SetPosition(original[0]); f.SetOrientationDegrees(original[1])
        records[ref]=sorted(good,key=lambda r:(r['anchor_distance_mm']+r['return_distance_mm'],r['anchor_distance_mm'],r['position_iu'],r['angle_deg']))[:1000]
        totals[ref]={'counts':dict(counts),'courtyard_blockers':dict(blockers),'retained':len(records[ref])}
        print(ref,dict(counts),'retained',len(records[ref]),flush=True)
    # Forward-checking domains avoid spending the bound on combinations that
    # leave another component with no remaining courtyard-clear position.
    names = list(MOVING)
    compatibility = {}
    bounds = {ref:[g.bounds(r['court']) for r in rows] for ref,rows in records.items()}
    for i, ref in enumerate(names):
        for other in names[i+1:]:
            left, right = records[ref], records[other]
            forward, reverse = [0]*len(left), [0]*len(right)
            for a, row in enumerate(left):
                aa = bounds[ref][a]
                for z, candidate in enumerate(right):
                    bb = bounds[other][z]
                    separate = aa[2]<bb[0] or bb[2]<aa[0] or aa[3]<bb[1] or bb[3]<aa[1]
                    if separate or not g.intersects(row['court'],candidate['court']):
                        forward[a] |= 1 << z
                        reverse[z] |= 1 << a
            compatibility[ref,other] = forward
            compatibility[other,ref] = reverse
    visited=0; selected={}; exhausted=False
    def solve(domains):
        nonlocal visited, exhausted
        if not domains: return True
        ref=min(domains,key=lambda k:bin(domains[k]).count('1'))
        available=domains[ref]
        while available:
            if visited>=200000:
                exhausted=True; return False
            visited+=1
            bit=available & -available; available-=bit; index=bit.bit_length()-1
            row=records[ref][index]
            following={other:mask & compatibility[ref,other][index] for other,mask in domains.items() if other!=ref}
            if any(mask==0 for mask in following.values()):continue
            f=parts[ref];f.SetPosition(p.VECTOR2I(*row['position_iu']));f.SetOrientationDegrees(row['angle_deg'])
            if any(a.GetNetCode()!=z.GetNetCode() and a.GetEffectiveShape(p.B_Cu).Collide(z.GetEffectiveShape(p.B_Cu),200000)
                   for other in selected for a in f.Pads() for z in parts[other].Pads()):continue
            selected[ref]=row
            if solve(following):return True
            del selected[ref]
        return False
    found=solve({ref:(1<<len(records[ref]))-1 for ref in names}) if all(records.values()) else False
    assert hashlib.sha256(SOURCE.read_bytes()).hexdigest()==SHA
    return {'SPDX-License-Identifier':'CERN-OHL-S-2.0','status':'UNSELECTED_COMPLETE_STAGE_PACKING_SCREEN',
            'source_sha256':SHA,'tool_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'pair_poses':pair_poses,'ignored_copper_for_replacement':ignored_switches,'U36_L1_poses_fixed':ic_pose is None,'moving_refs':MOVING,'grid_mm':.25,'radius_mm':6,
            'return_distance_limits_mm':return_limits,'locality_targets':{ref:{'anchor_pad':v[0],'IC_pin':v[1],'maximum_centre_distance_mm':v[2]} for ref,v in targets.items()},
            'grid_step_by_ref_mm':{ref:(.125 if ref=='C43' else .25) for ref in MOVING},'per_part':totals,'retained_poses':records,'packing_found':found,
            'packing':selected if found else None,'packing_states_visited':visited,'maximum_packing_states':200000,'packing_bound_exhausted':exhausted,
            'limitations':['Finite fixed-pair placement screen only; excludes zone fill and route/return proof',
                           'No copper retirement, reconnection or canonical selection'],
            'fabrication_release_allowed':False}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--ic-mm',type=float,nargs=2)
    parser.add_argument('--rotation-deg',type=int,choices=(0,90,180,270),default=0)
    args=parser.parse_args()
    out=args.output.resolve();assert (ROOT/'hardware/coupon/rev-a/build').resolve() in out.parents
    result=screen(None if args.ic_mm is None else [round(v*1e6) for v in args.ic_mm],args.rotation_deg);out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print('Complete stage packing found:',result.get('packing_found',False),flush=True)


if __name__=='__main__':main()
