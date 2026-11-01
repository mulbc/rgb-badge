#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Replay the exact unselected ADR 0077/0078 full-stage local candidate.

This preserves two known accepted supply-group losses; it is not source adoption.
Generate the ADR 0074 --scope stage input first. Outputs are restricted to build/.
"""
import argparse
from collections import Counter, defaultdict
import hashlib
import json
import math
from pathlib import Path
import runpy
import shutil
import uuid
import pcbnew as p

ROOT=Path(__file__).resolve().parents[1]
PLAN=ROOT/'mechanical/review/vled-local-stage-plan-2026-11-01.json'
PLAN_SHA='01b9c2eb539546dd35f529c2f5d628b777f2dc95d81eff7cf7854234f49dabb8'
SOURCE_SHA='1b50456d58c23e7582a043dc59185ee79a1699c44f7b7693eb3f1b0c58beb49e'
C=runpy.run_path(str(ROOT/'tools/check-routing-progress-trial.py'))


def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def inventory(board):return Counter(C['signature'](board,t) for t in board.GetTracks())


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--source',type=Path,required=True)
    ap.add_argument('--output',type=Path,required=True)
    args=ap.parse_args();source=args.source.resolve();output=args.output.resolve()
    assert (ROOT/'hardware/coupon/rev-a/build').resolve() in output.parents and output.suffix=='.kicad_pcb', 'Output must be an ignored build PCB'
    assert source!=output, 'Output must not overwrite input'
    assert sha(source)==SOURCE_SHA, 'Exact stage probe required'
    assert sha(PLAN)==PLAN_SHA, 'Exact unselected catalog required'
    assert sha(C['OUTPUT'])=='3451177253a021d8706ff818696212afabf539a108f15ef9e5d6921e46435acc', 'Accepted reference changed'
    plan=json.loads(PLAN.read_text());assert plan['source_sha256']==SOURCE_SHA
    old,board,frozen=[p.LoadBoard(str(path)) for path in (source,source,C['SOURCE'])]
    retired=Counter(map(tuple,plan['removed_copper']));added=Counter(map(tuple,plan['added_copper']))
    assert len(retired)==2 and len(added)==23 and not retired-inventory(old)
    assert not retired & inventory(frozen), 'Only exact accepted UART additions may retire'
    assert not added & inventory(old)
    layers={board.GetLayerName(l):l for l in board.GetEnabledLayers().CuStack()};lengths=defaultdict(float);held=[]
    remaining=retired.copy()
    for t in list(board.GetTracks()):
        key=C['signature'](board,t)
        if remaining[key]:remaining[key]-=1;board.Remove(t);held.append(t)
    assert not +remaining
    for row,count in added.items():
        assert count==1
        if row[0]=='track':
            _,net,x,y,a,b,layer,width=row
            assert width==200000 and (x,y)!=(a,b)
            assert (net=='UART0_TX' and layer=='In4.Cu') or (net in ('+SYS_APP_IN_DRAFT','VLED','VLED_FB','VLED_FB_TOP_MID','VLED_ENABLE_DRAFT') and layer=='B.Cu')
            item=p.PCB_TRACK(board);item.SetStart(p.VECTOR2I(x,y));item.SetEnd(p.VECTOR2I(a,b));item.SetLayer(layers[layer]);item.SetWidth(width)
            lengths[net]+=math.dist((x,y),(a,b))/1e6
        else:
            assert row==('via','UART0_TX',31050000,19500000,'In4.Cu','B.Cu',300000,100000)
            net=row[1];item=p.PCB_VIA(board);item.SetPosition(p.VECTOR2I(row[2],row[3]));item.SetViaType(p.VIATYPE_MICROVIA);item.SetLayerPair(p.In4_Cu,p.B_Cu);item.SetWidth(300000);item.SetDrill(100000)
        item.SetNetCode(board.FindNet(net).GetNetCode());item.SetUuid(p.KIID(str(uuid.uuid5(uuid.NAMESPACE_URL,'rgb-badge:ADR0077-0078:exact-replay:'+repr(row)))));board.Add(item)
    assert lengths['UART0_TX']<=20.65000001 and all(v<=25 for v in lengths.values())
    assert inventory(board)==inventory(old)-retired+added
    parts={f.GetReference():f for f in board.GetFootprints()}
    for f in old.GetFootprints():
        q=parts[f.GetReference()]
        assert q.GetPosition()==f.GetPosition() and q.GetLayer()==f.GetLayer() and q.GetOrientation().AsDegrees()==f.GetOrientation().AsDegrees()
        assert q.GetFPIDAsString()==f.GetFPIDAsString() and Counter(map(C['local_pad_signature'],q.Pads()))==Counter(map(C['local_pad_signature'],f.Pads()))
        assert sorted((v.GetName(),v.GetText()) for v in q.GetFields())==sorted((v.GetName(),v.GetText()) for v in f.GetFields())
    prior={}
    for f in old.GetFootprints():
        for q in f.Pads():
            if q.GetNetname():prior.setdefault(C['physical_cluster'](old,q),C['physical_identity'](q))
    assert len(prior)==257
    lookup={C['physical_identity'](q):q for f in board.GetFootprints() for q in f.Pads()}
    output.parent.mkdir(parents=True,exist_ok=True)
    sorter=runpy.run_path(str(ROOT/'tools/generate-paired-charger-114mm-routing.py'))['sorted_native_tracks'];fills=[]
    for i in range(3):
        p.ZONE_FILLER(board).Fill(board.Zones());board.BuildConnectivity()
        assert all(group<=C['physical_cluster'](board,lookup[key]) for group,key in prior.items())
        assert board.GetConnectivity().GetUnconnectedCount(False)==60
        p.SaveBoard(str(output),board);output.write_text(sorter(output.read_text(),expected=len(list(board.GetTracks()))))
        fills.append(dict(fill=i+1,native_opens=60,all_257_input_stage_groups_preserved=True,board_sha256=sha(output)))
    assert len({row['board_sha256'] for row in fills})==1
    structure=runpy.run_path(str(ROOT/'tools/check-routing-progress-plan.py'))['immutable_board_structure'];assert structure(source)==structure(output)
    for suffix in ('.kicad_pro','.kicad_dru'):shutil.copyfile(source.with_suffix(suffix),output.with_suffix(suffix))
    shutil.copyfile(source.parent/'fp-lib-table',output.parent/'fp-lib-table')
    accepted=p.LoadBoard(str(C['OUTPUT']));groups={}
    for f in accepted.GetFootprints():
        for q in f.Pads():
            if q.GetNetname():groups.setdefault(C['physical_cluster'](accepted,q),C['physical_identity'](q))
    losses=[dict(anchor=list(key),missing=[list(x) for x in sorted(group-C['physical_cluster'](board,lookup[key]))]) for group,key in groups.items() if not group<=C['physical_cluster'](board,lookup[key])]
    assert sorted(losses,key=repr)==sorted(plan['expected_accepted_prior_group_losses'],key=repr) and len(losses)==2
    opens=runpy.run_path(str(ROOT/'tools/report-coupon-board-connectivity.py'))['open_edges_by_net'](output)
    assert opens['native_open_edges']==60 and opens['pad_cluster_open_edges']==57
    result=dict(status='UNSELECTED_LOCAL_STAGE_WITH_TWO_OLD_SUPPLY_GROUP_LOSSES',source_sha256=SOURCE_SHA,plan_sha256=sha(PLAN),tool_sha256=sha(Path(__file__)),board_sha256=sha(output),fills=fills,open_edges=opens,added_items=23,retired_accepted_UART_items=2,track_length_mm_by_net=dict(lengths),accepted_prior_group_losses=losses,all_other_source_copper_and_483_poses_parts_pads_fields_fixed=True,structure_and_profiles_fixed=True,fabrication_release_allowed=False)
    result['SPDX-License-Identifier']='CERN-OHL-S-2.0';output.with_suffix('.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print('Unselected full stage: 60 native / 57 physical opens; two accepted supply-group losses remain',flush=True)


if __name__=='__main__':main()
