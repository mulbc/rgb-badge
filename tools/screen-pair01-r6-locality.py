#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""ADR 0120 read-only coordinated local-circuit screen; never saves a PCB."""
import argparse
from collections import Counter, defaultdict
import hashlib
import json
import math
from pathlib import Path
import runpy
import pcbnew as p

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT/'hardware/coupon/rev-a/staging/led-rse-corrected-routing-trial-114mm.kicad_pcb'
SOURCE_SHA = '3967bb66e89e0005f6859ce78a766b4536d06883b76fce130e75a6fdeefaf96e'
MOVING = {'PAIR01', 'R6'}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    out = args.output.resolve()
    assert (ROOT/'hardware/coupon/rev-a/build').resolve() in out.parents
    assert out.suffix=='.json' and sha(SOURCE)==SOURCE_SHA
    h = runpy.run_path(str(ROOT/'tools/screen-converter-inductor-locality.py'))
    g = h['geometry']
    courts, cells, overlap, box = (h[n] for n in ('courtyards','cells','overlap','native_box'))
    b = p.LoadBoard(str(SOURCE))
    parts = {f.GetReference():f for f in b.GetFootprints()}
    assert parts['PAIR01'].GetValue()=='NTLJD3119CTBG_TRIAL_ONLY'
    assert parts['PAIR01'].GetFPIDAsString()=='rgb-badge-coupon:WDFN6_2x2_onsemi_NTLJD3119C'
    assert parts['R6'].GetField('MPN').GetText()=='ERJ2RKF1001X'
    old = {ref:(p.VECTOR2I(parts[ref].GetPosition()),parts[ref].GetOrientation().AsDegrees()) for ref in MOVING}
    anchor = p.VECTOR2I(77250000,4400000)
    assert any(isinstance(t,p.PCB_VIA) and t.GetPosition()==anchor and t.GetNetname()=='ROW_00_A' for t in b.GetTracks())
    fixed, fixed_bins = [], defaultdict(list)
    for f in b.GetFootprints():
        if f.GetReference() in MOVING or f.GetLayer()!=p.B_Cu:
            continue
        for poly in courts(f):
            bounds = g.bounds(poly)
            i = len(fixed)
            fixed.append((f.GetReference(),bounds,poly))
            for cell in cells(bounds):
                fixed_bins[cell].append(i)
    layers = list(b.GetEnabledLayers().CuStack())
    copper = {l:[] for l in layers}
    bins = {l:defaultdict(list) for l in layers}
    items = list(b.GetTracks())+[q for f in b.GetFootprints() if f.GetReference() not in MOVING for q in f.Pads()]
    for item in items:
        for l in layers:
            if not item.IsOnLayer(l):
                continue
            i = len(copper[l])
            copper[l].append((item.GetNetCode(),item.GetEffectiveShape(l),item.m_Uuid.AsString()))
            for cell in cells(box(item.GetBoundingBox())):
                bins[l][cell].append(i)

    def blocked(shape, rect, layer, net):
        rect.Inflate(200000)
        indices = {i for c in cells(box(rect)) for i in bins[layer][c]}
        return any(copper[layer][i][0]!=net and shape.Collide(copper[layer][i][1],199990) for i in indices)

    def rotate(pos, angle):
        x,y = pos
        return {0:(x,y),90:(-y,x),180:(-x,-y),270:(y,-x)}[angle]

    template = {'PAIR01':((0,0),180),'R6':((-2750000,0),0)}
    net_gate = b.FindNet('ROW_GATE_00').GetNetCode()
    net_vled = b.FindNet('VLED').GetNetCode()
    local_paths = [(net_gate,[(-2250000,0),(-925000,0)]),
                   (net_vled,[(-3250000,0),(-3250000,900000),(-925000,900000),(-925000,650000)])]
    stack = [('In1.Cu','In2.Cu',p.VIATYPE_MICROVIA,300000,100000),
             ('In2.Cu','In3.Cu',p.VIATYPE_BURIED,500000,300000),
             ('In3.Cu','In4.Cu',p.VIATYPE_MICROVIA,300000,100000),
             ('In4.Cu','B.Cu',p.VIATYPE_MICROVIA,300000,100000)]
    counts = Counter()
    observations = Counter()
    clear = []
    capture_clear = []
    for rotation in (0,90,180,270):
        offsets = {}
        for ref,(pos,angle) in template.items():
            x,y = rotate(pos,rotation)
            f = parts[ref]
            f.SetPosition(p.VECTOR2I(x,y))
            f.SetOrientationDegrees((angle+rotation)%360)
            poly = courts(f)
            assert len(poly)==1
            offsets[ref] = poly[0]
        assert not g.intersects(offsets['PAIR01'],offsets['R6'])
        for x in range(80500000,96000001,100000):
            for y in range(1750000,12000001,100000):
                counts['sampled']+=1
                for ref,(relative,angle) in template.items():
                    dx,dy = rotate(relative,rotation)
                    parts[ref].SetPosition(p.VECTOR2I(x+dx,y+dy))
                drain_distance = min(math.dist(tuple(q.GetPosition()),tuple(anchor)) for q in parts['PAIR01'].Pads() if q.GetNumber()=='3')
                if drain_distance>6000000:
                    counts['drain_distance_over_6mm']+=1
                    continue
                hit = set()
                for ref,poly in offsets.items():
                    translated = [(a+x,c+y) for a,c in poly]
                    bounds = g.bounds(translated)
                    if bounds[0]<0 or bounds[1]<0 or bounds[2]>114000000 or bounds[3]>32500000:
                        hit.add('BOARD_EDGE')
                    indices = {i for c in cells(bounds) for i in fixed_bins[c]}
                    hit.update(fixed[i][0] for i in indices if overlap(bounds,fixed[i][1]) and g.intersects(translated,fixed[i][2]))
                if hit:
                    counts['fixed_courtyard']+=1
                    observations.update(hit)
                    continue
                counts['courtyard_clear']+=1
                bad = False
                for ref in MOVING:
                    for q in parts[ref].Pads():
                        qb = q.GetBoundingBox()
                        if qb.GetX()<500000 or qb.GetY()<500000 or qb.GetRight()>113500000 or qb.GetBottom()>32000000 or blocked(q.GetEffectiveShape(p.B_Cu),qb,p.B_Cu,q.GetNetCode()):
                            bad = True
                            break
                    if bad:
                        break
                if bad:
                    counts['fixed_copper_or_edge']+=1
                    continue
                for net,path in local_paths:
                    points = [(x+a,y+c) for a,c in (rotate(pt,rotation) for pt in path)]
                    for first,last in zip(points,points[1:]):
                        t = p.PCB_TRACK(b)
                        t.SetStart(p.VECTOR2I(*first));t.SetEnd(p.VECTOR2I(*last))
                        t.SetLayer(p.B_Cu);t.SetWidth(200000);t.SetNetCode(net)
                        if blocked(t.GetEffectiveShape(p.B_Cu),t.GetBoundingBox(),p.B_Cu,net) or any(
                            q.GetNetCode()!=net and t.GetEffectiveShape(p.B_Cu).Collide(q.GetEffectiveShape(p.B_Cu),199990)
                            for ref in MOVING for q in parts[ref].Pads()):
                            bad = True
                            break
                    if bad:
                        break
                if bad:
                    counts['local_lead_copper']+=1
                    continue
                counts['local_circuit_shapes_clear']+=1
                row = dict(centre_iu=[x,y],rotation_deg=rotation,drain_distance_lower_bound_mm=drain_distance/1e6,
                           poses={ref:dict(position_iu=list(parts[ref].GetPosition()),angle_deg=parts[ref].GetOrientation().AsDegrees()) for ref in sorted(MOVING)})
                if len(clear)<200:
                    clear.append(row)
                supply = next(q for q in parts['R6'].Pads() if q.GetNumber()=='1')
                for top,bottom,kind,width,hole in stack:
                    v = p.PCB_VIA(b)
                    v.SetPosition(supply.GetPosition());v.SetViaType(kind)
                    v.SetLayerPair(b.GetLayerID(top),b.GetLayerID(bottom));v.SetWidth(width);v.SetDrill(hole)
                    if any(blocked(v.GetEffectiveShape(l),v.GetBoundingBox(),l,net_vled) for l in [b.GetLayerID(top),b.GetLayerID(bottom)]):
                        bad = True
                        break
                if not bad:
                    counts['capture_shapes_clear']+=1
                    if len(capture_clear)<200:
                        capture_clear.append(row)
        print(rotation,dict(counts),flush=True)
    for ref,(pos,angle) in old.items():
        parts[ref].SetPosition(pos);parts[ref].SetOrientationDegrees(angle)
    assert sha(SOURCE)==SOURCE_SHA
    result={'SPDX-License-Identifier':'CERN-OHL-S-2.0','status':'UNSELECTED_READ_ONLY_COORDINATED_SCREEN',
            'source_sha256':SOURCE_SHA,'source_unchanged':True,'counts':dict(counts),
            'fixed_courtyard_observations':dict(observations),'local_circuit_clear_samples':clear,
            'local_capture_clear_samples':capture_clear,'step_iu':100000,'clearance_iu':200000,
            'copper_edge_iu':500000,'drain_lower_bound_limit_mm':6,'fabrication_release_allowed':False,
            'tool_sha256':sha(Path(__file__)),
            'limitations':['Finite rigid template only; no proof against other arrangements',
                           'Filled zones, drill clearance and actual source-contact restoration not screened',
                           'No routing, refills, connectivity, DRC or process acceptance','No PCB saved']}
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')


if __name__=='__main__':
    main()
