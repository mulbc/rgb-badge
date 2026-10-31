#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""ADR 0074 ignored native geometry probe; never writes accepted PCB source."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import runpy
import shutil
import uuid
import pcbnew as p

ROOT=Path(__file__).resolve().parents[1]
BUILD=ROOT/'hardware/coupon/rev-a/build'
SOURCE=ROOT/'hardware/coupon/rev-a/staging/led-routing-progress-trial-114mm.kicad_pcb'
SOURCE_SHA256='3451177253a021d8706ff818696212afabf539a108f15ef9e5d6921e46435acc'
SEED=ROOT/'mechanical/review/vled-rigid-floorplan-58-2026-10-30.json'
SEED_SHA256='6b2e6d000ba8d6b47e9be789cd501bd474891ba230dfeec0b6a16b76745d9f7d'
C=runpy.run_path(str(ROOT/'tools/check-routing-progress-trial.py'))


def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def xy(point):return [point.x,point.y]

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--source',type=Path,default=SOURCE)
    ap.add_argument('--scope',choices=('pair','stage'),required=True)
    ap.add_argument('--output',type=Path,required=True)
    args=ap.parse_args();source=args.source.resolve();output=args.output.resolve()
    assert BUILD.resolve() in output.parents and output.suffix=='.kicad_pcb'
    assert output!=source, 'Output must not overwrite an archived source'
    assert sha(source)==SOURCE_SHA256
    assert sha(SEED)==SEED_SHA256, 'Exact recorded packing seed required'
    seed=json.loads(SEED.read_text());assert seed['source_sha256']==SOURCE_SHA256 and len(seed['clear_poses'])==1
    poses=seed['clear_poses'][0]['poses']
    if args.scope=='pair':poses={ref:poses[ref] for ref in ('U37','L2')}
    old=p.LoadBoard(str(source));board=p.LoadBoard(str(source))
    oldparts={f.GetReference():f for f in old.GetFootprints()};parts={f.GetReference():f for f in board.GetFootprints()}
    assert parts['U37'].GetField('MPN').GetText()=='TPS63020DSJT'
    assert parts['L2'].GetField('MPN').GetText()=='DFE252012P-1R5M=P2'
    for ref,pose in poses.items():
        f=parts[ref];assert f.GetLayer()==p.B_Cu
        f.SetPosition(p.VECTOR2I(*pose['position_iu']));f.SetOrientationDegrees(pose['angle_deg'])
    for ref,f in oldparts.items():
        other=parts[ref]
        assert Counter(map(C['local_pad_signature'],f.Pads()))==Counter(map(C['local_pad_signature'],other.Pads()))
        assert sorted((v.GetName(),v.GetText()) for v in f.GetFields())==sorted((v.GetName(),v.GetText()) for v in other.GetFields())
        if ref not in poses:assert (f.GetPosition(),f.GetOrientation().AsDegrees())==(other.GetPosition(),other.GetOrientation().AsDegrees())
    for f in parts.values():
        if f.GetLayer()==p.B_Cu:f.BuildCourtyardCaches()
    court_hits=[]
    for ref in poses:
        for other,f in parts.items():
            if other==ref or f.GetLayer()!=p.B_Cu:continue
            if parts[ref].GetCourtyard(p.B_CrtYd).Collide(f.GetCourtyard(p.B_CrtYd),0):court_hits.append([ref,other])
    copper=[t for t in board.GetTracks() if t.IsOnLayer(p.B_Cu)]+[q for f in parts.values() for q in f.Pads() if q.IsOnLayer(p.B_Cu)]
    def identity(item):
        return ['pad',*C['physical_identity'](item)] if isinstance(item,p.PAD) else ['copper',*C['signature'](board,item)]
    def blockers(item,skip_parent=None):
        shape=item.GetEffectiveShape(p.B_Cu)
        return [identity(other) for other in copper if other.GetNetCode()!=item.GetNetCode()
                and not (isinstance(other,p.PAD) and other.GetParentFootprint().GetReference()==skip_parent)
                and shape.Collide(other.GetEffectiveShape(p.B_Cu),200000)]
    pad_hits=[]
    for ref in poses:
        for q in parts[ref].Pads():
            if q.IsOnLayer(p.B_Cu):
                hit=blockers(q,skip_parent=ref)
                if hit:pad_hits.append(dict(pad=identity(q),blockers=hit))
    def pad(ref,number):
        matches=[q for q in parts[ref].Pads() if q.GetNumber()==number];assert len(matches)==1;return matches[0]
    tracks=[];routes=[]
    for terminal,first,second in [('1','9','8'),('2','6','7')]:
        a,z,end=pad('U37',first),pad('U37',second),pad('L2',terminal)
        assert a.GetNetname()==z.GetNetname()==end.GetNetname()=='Net-(L2-~-Pad'+terminal+')'
        bend=p.VECTOR2I(end.GetPosition().x-400000,z.GetPosition().y)
        points=[a.GetPosition(),z.GetPosition(),bend,end.GetPosition()];local=[]
        for index,(start,finish) in enumerate(zip(points,points[1:])):
            t=p.PCB_TRACK(board);t.SetStart(start);t.SetEnd(finish);t.SetWidth(200000);t.SetLayer(p.B_Cu);t.SetNetCode(a.GetNetCode())
            t.SetUuid(p.KIID(str(uuid.uuid5(uuid.NAMESPACE_URL,'rgb-badge:ADR0074:'+args.scope+':'+a.GetNetname()+':'+str(index)))))
            local.append(t)
        length=sum(t.GetLength() for t in local)/1e6;assert length<=5
        hits=[dict(track=list(C['signature'](board,t)),blockers=blockers(t)) for t in local]
        routes.append(dict(net=a.GetNetname(),pad_terminal=terminal,track_length_mm=length,tracks=[list(C['signature'](board,t)) for t in local],external_blockers=[h for h in hits if h['blockers']]))
        tracks.extend(local)
    mutual_hits=[]
    for index,track in enumerate(tracks):
        for other in tracks[index+1:]:
            if track.GetNetCode()!=other.GetNetCode() and track.GetEffectiveShape(p.B_Cu).Collide(other.GetEffectiveShape(p.B_Cu),200000):
                mutual_hits.append([list(C['signature'](board,track)),list(C['signature'](board,other))])
    direct_clear=not court_hits and not pad_hits and not mutual_hits and all(not row['external_blockers'] for row in routes)
    if direct_clear:
        for t in tracks:board.Add(t)
    prior={}
    for f in old.GetFootprints():
        for q in f.Pads():
            if q.GetNetname():prior.setdefault(C['physical_cluster'](old,q),C['physical_identity'](q))
    lookup={C['physical_identity'](q):q for f in board.GetFootprints() for q in f.Pads()}
    fills=[]
    for iteration in range(3):
        p.ZONE_FILLER(board).Fill(board.Zones());board.BuildConnectivity()
        lost=[dict(pad=list(key),net=lookup[key].GetNetname(),missing_old_members=[list(v) for v in sorted(group-C['physical_cluster'](board,lookup[key]))]) for group,key in prior.items() if not group<=C['physical_cluster'](board,lookup[key])]
        fills.append(dict(fill=iteration+1,native_opens=board.GetConnectivity().GetUnconnectedCount(False),lost_prior_groups=lost))
    connected={}
    for terminal,numbers in [('1',('8','9')),('2',('6','7'))]:
        group=C['physical_cluster'](board,pad('L2',terminal));connected[terminal]=all(C['physical_identity'](pad('U37',number)) in group for number in numbers)
    retained=Counter(C['signature'](old,t) for t in old.GetTracks());actual=Counter(C['signature'](board,t) for t in board.GetTracks())
    assert not retained-actual
    assert Counter(C['zone_signature'](old,z) for z in old.Zones())==Counter(C['zone_signature'](board,z) for z in board.Zones())
    output.parent.mkdir(parents=True,exist_ok=True);p.SaveBoard(str(output),board)
    sorter=runpy.run_path(str(ROOT/'tools/generate-paired-charger-114mm-routing.py'))['sorted_native_tracks']
    output.write_text(sorter(output.read_text(),expected=len(list(board.GetTracks()))))
    for suffix in ('.kicad_pro','.kicad_dru'):shutil.copyfile(source.with_suffix(suffix),output.with_suffix(suffix))
    (output.parent/'fp-lib-table').write_text('(fp_lib_table (lib (name "rgb-badge-coupon") (type "KiCad") (uri "'+str(ROOT/'hardware/coupon/rev-a/footprints/rgb-badge-coupon.pretty')+'") (options "") (descr "Local geometry study")))\n')
    reporter=runpy.run_path(str(ROOT/'tools/report-coupon-board-connectivity.py'))
    result=dict(status='UNSELECTED_LOCAL_VLED_SWITCHING_GEOMETRY_NOT_POWER_STAGE_ACCEPTANCE',scope=args.scope,
        source_sha256=SOURCE_SHA256,seed_sha256=sha(SEED),tool_sha256=sha(Path(__file__)),board_sha256=sha(output),kicad_version=p.GetBuildVersion(),
        poses=poses,courtyard_blockers=court_hits,moved_pad_external_blockers=pad_hits,direct_routes_clear=direct_clear,
        routes=routes,mutual_route_blockers=mutual_hits,added_tracks=6 if direct_clear else 0,local_switching_pad_groups_connected=connected,fills=fills,
        open_edges=reporter['open_edges_by_net'](output),all_source_copper_retained=True,source_unchanged=sha(source)==SOURCE_SHA256,
        fabrication_release_allowed=False,
        limitations=['No source retirement; vacated old copper may remain dangling',
            'Earlier groups need restoration before any selection',
            '0.20 mm geometry is not power-path current/thermal qualification',
            'Capacitor, feedback, return and full-stage layout qualification remain open'])
    result['SPDX-License-Identifier']='CERN-OHL-S-2.0'
    output.with_suffix('.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(args.scope,'direct clear',direct_clear,'joined',connected,'opens',result['open_edges']['native_open_edges'],result['open_edges']['pad_cluster_open_edges'],'lost groups',len(fills[-1]['lost_prior_groups']),flush=True)


if __name__=='__main__':main()
