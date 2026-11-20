#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""ADR 0077 finite native B.Cu-only local-pair dogleg screen."""
from collections import Counter,defaultdict
from pathlib import Path
import argparse,hashlib,json,math,runpy,shutil,uuid
import pcbnew as p

def main():
    root=Path(__file__).resolve().parents[1]
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--source',type=Path,required=True)
    ap.add_argument('--output',type=Path,required=True)
    args=ap.parse_args();source=args.source.resolve();output=args.output.resolve()
    assert (root/'hardware/coupon/rev-a/build').resolve() in output.parents and output.suffix=='.kicad_pcb', 'Output must be an ignored build PCB'
    assert source!=output, 'Output must not overwrite input'
    base=output.parent;base.mkdir(parents=True,exist_ok=True)
    c=runpy.run_path(str(root/'tools/check-routing-progress-trial.py'))
    assert hashlib.sha256(source.read_bytes()).hexdigest()=='1b50456d58c23e7582a043dc59185ee79a1699c44f7b7693eb3f1b0c58beb49e'
    b=p.LoadBoard(str(source));accepted=p.LoadBoard(str(c['OUTPUT']));parts={f.GetReference():f for f in b.GetFootprints()};initial=Counter(c['signature'](b,t) for t in b.GetTracks());held=[];added=[];records=[];lengths=defaultdict(float)
    lookup={c['physical_identity'](q):q for f in b.GetFootprints() for q in f.Pads()};prior={}
    for q in lookup.values():
     if q.GetNetname():prior.setdefault(c['physical_cluster'](b,q),c['physical_identity'](q))
    accepted_groups={}
    for f in accepted.GetFootprints():
     for q in f.Pads():
      if q.GetNetname():accepted_groups.setdefault(c['physical_cluster'](accepted,q),c['physical_identity'](q))
    def losses():return [dict(anchor=list(key),missing=[list(x) for x in sorted(group-c['physical_cluster'](b,lookup[key]))]) for group,key in accepted_groups.items() if not group<=c['physical_cluster'](b,lookup[key])]
    initial_losses=losses()
    def pad(ref,num):return next(q for q in parts[ref].Pads() if q.GetNumber()==num)
    def identity(item):return ['pad',*c['physical_identity'](item)] if isinstance(item,p.PAD) else ['copper',*c['signature'](b,item)]
    def obstacle(item):
     box=item.GetBoundingBox();return (item.GetNetCode(),box.GetX(),box.GetY(),box.GetRight(),box.GetBottom(),item.GetEffectiveShape(p.B_Cu),identity(item))
    obstacles=[obstacle(t) for t in list(b.GetTracks())+[q for f in b.GetFootprints() for q in f.Pads()] if t.IsOnLayer(p.B_Cu)]
    def hits(track):
     box=track.GetBoundingBox();x0,y0,x1,y1=box.GetX()-200000,box.GetY()-200000,box.GetRight()+200000,box.GetBottom()+200000;shape=track.GetEffectiveShape(p.B_Cu);out=[]
     for net,a,d,z,e,other,key in obstacles:
      if net==track.GetNetCode() or a>x1 or z<x0 or d>y1 or e<y0:continue
      if shape.Collide(other,200000):out.append(key)
     return sorted(out,key=repr)
    pairs=[('input_pin_pair','U37','11','U37','10'),('input_C44','U37','11','C44','1'),('input_C45','C44','1','C45','1'),('output_pin_pair','U37','4','U37','5'),('output_C46','U37','4','C46','1'),('output_C47','C46','1','C47','1'),('output_C48_C49','C48','1','C49','1'),('output_divider_top','C48','1','R84','1'),('output_cap_banks','C47','1','C49','1'),('feedback_midpoint','R84','2','R85','1'),('feedback_bottom','R85','2','R86','1'),('feedback_IC','U37','3','R86','1'),('enable_pulldown','U37','12','R87','1'),('VINA_bypass','U37','1','C63','1')]
    for name,ra,na,rb,nb in pairs:
     a,z=pad(ra,na),pad(rb,nb);assert a.GetNetname()==z.GetNetname();net=a.GetNetname();start=(a.GetPosition().x,a.GetPosition().y);end=(z.GetPosition().x,z.GetPosition().y)
     if c['physical_identity'](z) in c['physical_cluster'](b,a):records.append(dict(pair=name,status='ALREADY_CONNECTED'));continue
     paths=[[start,end],[start,(start[0],end[1]),end],[start,(end[0],start[1]),end]]
     for x in range(math.floor((min(start[0],end[0])-2000000)/50000)*50000,math.ceil((max(start[0],end[0])+2000000)/50000)*50000+1,50000):paths.append([start,(x,start[1]),(x,end[1]),end])
     for y in range(math.floor((min(start[1],end[1])-2000000)/50000)*50000,math.ceil((max(start[1],end[1])+2000000)/50000)*50000+1,50000):paths.append([start,(start[0],y),(end[0],y),end])
     unique={tuple(point for i,point in enumerate(path) if i==0 or point!=path[i-1]) for path in paths};paths=sorted(unique,key=lambda path:(sum(math.dist(x,y) for x,y in zip(path,path[1:])),path));attempts=[];chosen=[]
     for path in paths:
      length=sum(math.dist(x,y) for x,y in zip(path,path[1:]))/1e6
      if length>5.00000001 or lengths[net]+length>25.00000001:attempts.append(dict(points_iu=path,status='LENGTH_BOUND',length_mm=length));continue
      tracks=[];blocked=[]
      for i,(start,end) in enumerate(zip(path,path[1:])):
       t=p.PCB_TRACK(b);t.SetStart(p.VECTOR2I(*start));t.SetEnd(p.VECTOR2I(*end));t.SetLayer(p.B_Cu);t.SetWidth(200000);t.SetNetCode(a.GetNetCode());t.SetUuid(p.KIID(str(uuid.uuid5(uuid.NAMESPACE_URL,'rgb-badge:ADR0077:'+name+':'+repr(path)+':'+str(i)))));tracks.append(t);blocked.extend(hits(t))
      if blocked:attempts.append(dict(points_iu=path,status='FOREIGN_NET_BLOCKED',length_mm=length,blockers=sorted({json.dumps(x) for x in blocked})));continue
      for t in tracks:b.Add(t)
      p.ZONE_FILLER(b).Fill(b.Zones());b.BuildConnectivity()
      lost=[list(key) for group,key in prior.items() if not group<=c['physical_cluster'](b,lookup[key])]
      if lost:
       for t in tracks:b.Remove(t);held.append(t)
       p.ZONE_FILLER(b).Fill(b.Zones());b.BuildConnectivity();attempts.append(dict(points_iu=path,status='PREEXISTING_STAGE_GROUP_SPLIT',length_mm=length,anchors=lost));continue
      assert c['physical_identity'](z) in c['physical_cluster'](b,a)
      chosen=tracks;added.extend(c['signature'](b,t) for t in tracks);lengths[net]+=length;obstacles.extend(obstacle(t) for t in tracks);attempts.append(dict(points_iu=path,status='ACCEPTED_PRIVATE_LOCAL_JOIN',length_mm=length));break
     record=dict(pair=name,net=net,status='LOCAL_JOIN' if chosen else 'NO_PATH_IN_FINITE_SCREEN',attempts=attempts,tracks=[list(c['signature'](b,t)) for t in chosen],native_opens=b.GetConnectivity().GetUnconnectedCount(False),accepted_prior_group_losses=losses())
     records.append(record);print(name,record['status'],'attempts',len(attempts),'opens',record['native_opens'],flush=True)
    assert Counter(c['signature'](b,t) for t in b.GetTracks())==initial+Counter(added)
    fills=[]
    sorter=runpy.run_path(str(root/'tools/generate-paired-charger-114mm-routing.py'))['sorted_native_tracks']
    for i in range(3):
     p.ZONE_FILLER(b).Fill(b.Zones());b.BuildConnectivity();assert all(group<=c['physical_cluster'](b,lookup[key]) for group,key in prior.items());p.SaveBoard(str(output),b);output.write_text(sorter(output.read_text(),expected=len(list(b.GetTracks()))));fills.append(dict(fill=i+1,native_opens=b.GetConnectivity().GetUnconnectedCount(False),all_initial_stage_groups_preserved=True,board_sha256=hashlib.sha256(output.read_bytes()).hexdigest()))
    assert len({row['board_sha256'] for row in fills})==1
    path=output;p.SaveBoard(str(path),b);sorter=runpy.run_path(str(root/'tools/generate-paired-charger-114mm-routing.py'))['sorted_native_tracks'];path.write_text(sorter(path.read_text(),expected=len(list(b.GetTracks()))))
    for suffix in ('.kicad_pro','.kicad_dru'):shutil.copyfile(source.with_suffix(suffix),path.with_suffix(suffix))
    shutil.copyfile(source.parent/'fp-lib-table',base/'fp-lib-table')
    opens=runpy.run_path(str(root/'tools/report-coupon-board-connectivity.py'))['open_edges_by_net'](path)
    report=dict(status='UNSELECTED_FINITE_LOCAL_STAGE_B_CU_SCREEN_NOT_OLD_GROUP_RESTORATION',source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),tool_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),board_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),records=records,track_length_mm_by_net=dict(lengths),added_copper=[list(row) for row in added],initial_accepted_prior_group_losses=initial_losses,final_accepted_prior_group_losses=losses(),fills=fills,open_edges=opens,all_source_copper_retained=True,fabrication_release_allowed=False)
    report['SPDX-License-Identifier']='CERN-OHL-S-2.0';output.with_suffix('.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n');print('FINAL',opens['native_open_edges'],opens['pad_cluster_open_edges'],'NEW',len(added),'OLD LOSSES',len(initial_losses),len(report['final_accepted_prior_group_losses']),flush=True)


if __name__ == "__main__":
    main()
