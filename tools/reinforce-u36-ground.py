#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Ignored ADR 0090 local return-spine experiment; no core-layer microvia."""
import argparse
import hashlib
import json
import math
from pathlib import Path
import shutil
import uuid
import pcbnew as p

ROOT=Path(__file__).resolve().parents[1]


def signature(board,t):
    if isinstance(t,p.PCB_VIA):
        return ['via',t.GetNetname(),t.GetPosition().x,t.GetPosition().y,board.GetLayerName(t.TopLayer()),board.GetLayerName(t.BottomLayer()),t.GetWidth(t.TopLayer()),t.GetDrillValue()]
    return ['track',t.GetNetname(),t.GetStart().x,t.GetStart().y,t.GetEnd().x,t.GetEnd().y,board.GetLayerName(t.GetLayer()),t.GetWidth()]


def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--source',type=Path,required=True);ap.add_argument('--output',type=Path,required=True)
    args=ap.parse_args();out=args.output.resolve();source=args.source.resolve()
    assert (ROOT/'hardware/coupon/rev-a/build').resolve() in out.parents and source!=out
    before=p.LoadBoard(str(source));b=p.LoadBoard(str(source));parts={f.GetReference():f for f in b.GetFootprints()}
    def pad(ref,n):return next(q for q in parts[ref].Pads() if q.GetNumber()==n)
    def xy(q):return[q.GetPosition().x,q.GetPosition().y]
    gnd=pad('U36','7').GetNetCode();assert pad('C30','2').GetNetCode()==pad('R82','2').GetNetCode()==gnd
    ic,main_ground,lower=xy(pad('U36','7')),[108400000,21850000],xy(pad('R82','2'))
    assert any(isinstance(t,p.PCB_VIA) and t.GetNetCode()==gnd and t.GetPosition()==p.VECTOR2I(*main_ground) and t.IsOnLayer(p.In3_Cu) for t in b.GetTracks())
    outward=[lower[0]+400000,lower[1]];added=[]
    def clear(t):
        for layer in (p.B_Cu,p.In4_Cu,p.In3_Cu):
            if not t.IsOnLayer(layer):continue
            box=t.GetBoundingBox();box.Inflate(200000)
            for other in list(b.GetTracks())+[q for f in b.GetFootprints() for q in f.Pads()]:
                if not other.IsOnLayer(layer) or other.GetNetCode()==gnd or not box.Intersects(other.GetBoundingBox()):continue
                if t.GetEffectiveShape(layer).Collide(other.GetEffectiveShape(layer),200000-10):return False
        return True
    def commit(t):
        row=signature(b,t);t.SetUuid(p.KIID(str(uuid.uuid5(uuid.NAMESPACE_URL,'rgb-badge:ADR0090:ground:'+repr(row)))));b.Add(t);added.append(row)
    def track(a,z,layer):
        t=p.PCB_TRACK(b);t.SetStart(p.VECTOR2I(*a));t.SetEnd(p.VECTOR2I(*z));t.SetWidth(200000);t.SetLayer(layer);t.SetNetCode(gnd);return t
    for point in (ic,outward):
        for top,bottom in ((p.In4_Cu,p.B_Cu),(p.In3_Cu,p.In4_Cu)):
            via=p.PCB_VIA(b);via.SetPosition(p.VECTOR2I(*point));via.SetLayerPair(top,bottom);via.SetViaType(p.VIATYPE_MICROVIA);via.SetWidth(300000);via.SetDrill(100000);via.SetNetCode(gnd)
            assert clear(via),'Ground via foreign-copper obstruction';commit(via)
    for a,z in ((xy(pad('U36','6')),ic),(lower,outward)):
        t=track(a,z,p.B_Cu);assert clear(t);commit(t)
    paths=[]
    for start,end in ((ic,main_ground),(outward,ic)):
        candidates=[[start,end],[start,[start[0],end[1]],end],[start,[end[0],start[1]],end]]
        for y in range(min(start[1],end[1])-1000000,max(start[1],end[1])+1000001,50000):
            candidates.append([start,[start[0],y],[end[0],y],end])
        for x in range(min(start[0],end[0])-1000000,max(start[0],end[0])+1000001,50000):
            candidates.append([start,[x,start[1]],[x,end[1]],end])
        candidates=sorted(candidates,key=lambda row:(sum(math.dist(a,z) for a,z in zip(row,row[1:])),row))
        selected=None
        for points in candidates:
            points=[q for i,q in enumerate(points) if i==0 or q!=points[i-1]]
            length=sum(math.dist(a,z) for a,z in zip(points,points[1:]))/1e6
            if length>6:continue
            tracks=[track(a,z,p.In3_Cu) for a,z in zip(points,points[1:])]
            if not all(clear(t) for t in tracks):continue
            selected=points
            for t in tracks:commit(t)
            paths.append({'points_iu':points,'length_mm':length});break
        assert selected,'No bounded native-clear In4 ground-spine branch'
    p.ZONE_FILLER(b).Fill(b.Zones());b.BuildConnectivity()
    def pads(board):return{q.m_Uuid.AsString():q for f in board.GetFootprints() for q in f.Pads() if q.GetNetname()}
    def cluster(board,q):return frozenset(z.m_Uuid.AsString() for z in board.GetConnectivity().GetConnectedItems(q) if isinstance(z,p.PAD))
    a,z=pads(before),pads(b)
    losses=[{'reference':q.GetParentFootprint().GetReference(),'number':q.GetNumber(),'net':q.GetNetname(),'missing':sorted(cluster(before,q)-cluster(b,z[k]))} for k,q in a.items() if not cluster(before,q)<=cluster(b,z[k])]
    if losses:
        out.parent.mkdir(parents=True,exist_ok=True)
        out.with_suffix('.rejected.json').write_text(json.dumps({'losses':losses,'added_copper':added,'paths':paths},indent=2)+'\n')
        print('Ground spine rejected:',[(r['reference'],r['number'],r['net']) for r in losses[:8]],flush=True)
        raise ValueError('Ground spine splits existing groups')
    out.parent.mkdir(parents=True,exist_ok=True);p.SaveBoard(str(out),b)
    for ext in ('.kicad_pro','.kicad_dru'):shutil.copyfile(source.with_suffix(ext),out.with_suffix(ext))
    report={'SPDX-License-Identifier':'CERN-OHL-S-2.0','status':'IGNORED_LOCAL_GROUND_SPINE_PENDING_FULL_DRC','source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'board_sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'tool_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'added_copper':added,'paths':paths,'all_input_groups_preserved':True,'opens':b.GetConnectivity().GetUnconnectedCount(False),'via_in_pad_fill_cap_qualification_open':True,'fabrication_release_allowed':False}
    out.with_suffix('.ground.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
    print('Explicit GND spine added',len(added),'items; branches',[row['length_mm'] for row in paths],flush=True)


if __name__=='__main__':main()
