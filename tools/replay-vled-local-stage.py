#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Replay the exact unselected ADR 0077/0078 full-stage local candidate.

The local phase retains two old supply-group losses; the restored phase fixes
those losses while keeping old dangling power copper. The cleaned phase applies
the exact ADR 0081 cohort. No phase is canonical source adoption.
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
RESTORED_PLAN=ROOT/'mechanical/review/vled-restored-stage-plan-2026-11-01.json'
RESTORED_PLAN_SHA='2b04732afa9ebd55b56f1c69e061031035c3e55f9657d0e5b639677a31d1969a'
CLEANED_PLAN=ROOT/'mechanical/review/vled-cleaned-stage-plan-2026-11-01.json'
CLEANED_PLAN_SHA='22429a26d1c86f87a003423160e3e49b895aeeb4cbda98e0d463559e6a32007e'
SOURCE_SHA='1b50456d58c23e7582a043dc59185ee79a1699c44f7b7693eb3f1b0c58beb49e'
C=runpy.run_path(str(ROOT/'tools/check-routing-progress-trial.py'))


def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def inventory(board):return Counter(C['signature'](board,t) for t in board.GetTracks())


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--phase',choices=('local','restored','cleaned'),default='local')
    ap.add_argument('--source',type=Path,required=True)
    ap.add_argument('--output',type=Path,required=True)
    args=ap.parse_args();source=args.source.resolve();output=args.output.resolve()
    assert (ROOT/'hardware/coupon/rev-a/build').resolve() in output.parents and output.suffix=='.kicad_pcb', 'Output must be an ignored build PCB'
    assert source!=output, 'Output must not overwrite input'
    assert sha(source)==SOURCE_SHA, 'Exact stage probe required'
    global_phase=args.phase!='local'
    plan_path,plan_sha={'local':(PLAN,PLAN_SHA),'restored':(RESTORED_PLAN,RESTORED_PLAN_SHA),'cleaned':(CLEANED_PLAN,CLEANED_PLAN_SHA)}[args.phase]
    assert sha(plan_path)==plan_sha, 'Exact unselected catalog required'
    assert sha(C['OUTPUT'])=='3451177253a021d8706ff818696212afabf539a108f15ef9e5d6921e46435acc', 'Accepted reference changed'
    plan=json.loads(plan_path.read_text());assert plan['source_sha256']==SOURCE_SHA
    old,board,frozen=[p.LoadBoard(str(path)) for path in (source,source,C['SOURCE'])]
    retired=Counter(map(tuple,plan['removed_copper']));added=Counter(map(tuple,plan['added_copper']))
    assert len(retired)==(54 if args.phase=='cleaned' else 2) and len(added)==(95 if global_phase else 23) and not retired-inventory(old)
    if args.phase=='cleaned':
        ledger=plan['cleanup_ledger'];assert len(ledger)==52
        assert Counter(tuple(row['signature']) for row in ledger)+Counter(map(tuple,json.loads(PLAN.read_text())['removed_copper']))==retired
        original=inventory(frozen)
        for row in ledger:
            assert row['origin']==('frozen_215_source' if original[tuple(row['signature'])] else 'accepted_addition')
        assert sum((retired & original).values())==16, 'Exact original-source cleanup cohort differs'
    else:
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
            assert ((net=='UART0_TX' and layer=='In4.Cu')
                    or (net in ('+SYS_APP_IN_DRAFT','VLED') and (layer=='B.Cu' or global_phase))
                    or (net in ('VLED_FB','VLED_FB_TOP_MID','VLED_ENABLE_DRAFT') and layer=='B.Cu')
                    or (global_phase and row==('track','GND',48600000,20350000,48600000,20150000,'B.Cu',200000)))
            item=p.PCB_TRACK(board);item.SetStart(p.VECTOR2I(x,y));item.SetEnd(p.VECTOR2I(a,b));item.SetLayer(layers[layer]);item.SetWidth(width)
            lengths[net]+=math.dist((x,y),(a,b))/1e6
        else:
            _,net,x,y,top,bottom,diameter,drill=row
            assert row[0]=='via' and (diameter,drill)==(300000,100000)
            assert abs(list(layers).index(top)-list(layers).index(bottom))==1
            assert (row==('via','UART0_TX',31050000,19500000,'In4.Cu','B.Cu',300000,100000)
                    or (global_phase and net in ('+SYS_APP_IN_DRAFT','VLED'))
                    or (global_phase and net=='GND' and (x,y)==(48600000,20150000) and (top,bottom) in (('In4.Cu','B.Cu'),('In3.Cu','In4.Cu'),('In2.Cu','In3.Cu'))))
            item=p.PCB_VIA(board);item.SetPosition(p.VECTOR2I(x,y));item.SetViaType(p.VIATYPE_MICROVIA);item.SetLayerPair(layers[top],layers[bottom]);item.SetWidth(diameter);item.SetDrill(drill)
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
        assert board.GetConnectivity().GetUnconnectedCount(False)==plan['native_opens']
        p.SaveBoard(str(output),board);output.write_text(sorter(output.read_text(),expected=len(list(board.GetTracks()))))
        fills.append(dict(fill=i+1,native_opens=plan['native_opens'],all_257_input_stage_groups_preserved=True,board_sha256=sha(output)))
    assert len({row['board_sha256'] for row in fills})==1
    structure=runpy.run_path(str(ROOT/'tools/check-routing-progress-plan.py'))['immutable_board_structure'];assert structure(source)==structure(output)
    for suffix in ('.kicad_pro','.kicad_dru'):shutil.copyfile(source.with_suffix(suffix),output.with_suffix(suffix))
    shutil.copyfile(source.parent/'fp-lib-table',output.parent/'fp-lib-table')
    accepted=p.LoadBoard(str(C['OUTPUT']));groups={}
    for f in accepted.GetFootprints():
        for q in f.Pads():
            if q.GetNetname():groups.setdefault(C['physical_cluster'](accepted,q),C['physical_identity'](q))
    losses=[dict(anchor=list(key),missing=[list(x) for x in sorted(group-C['physical_cluster'](board,lookup[key]))]) for group,key in groups.items() if not group<=C['physical_cluster'](board,lookup[key])]
    assert sorted(losses,key=repr)==sorted(plan['expected_accepted_prior_group_losses'],key=repr) and len(losses)==(0 if global_phase else 2)
    opens=runpy.run_path(str(ROOT/'tools/report-coupon-board-connectivity.py'))['open_edges_by_net'](output)
    assert opens['native_open_edges']==plan['native_opens'] and opens['pad_cluster_open_edges']==plan['physical_opens']
    result=dict(status=('UNSELECTED_CLEANED_FULL_STAGE_REQUIRES_CANONICAL_ADOPTION_POLICY' if args.phase=='cleaned' else 'UNSELECTED_ALL_OLD_GROUPS_RESTORED_WITH_OLD_DANGLING_POWER_COPPER' if global_phase else 'UNSELECTED_LOCAL_STAGE_WITH_TWO_OLD_SUPPLY_GROUP_LOSSES'),phase=args.phase,source_sha256=SOURCE_SHA,plan_sha256=sha(plan_path),tool_sha256=sha(Path(__file__)),board_sha256=sha(output),fills=fills,open_edges=opens,added_items=sum(added.values()),retired_accepted_UART_items=2,retired_cleanup_items=52 if args.phase=='cleaned' else 0,track_length_mm_by_net=dict(lengths),accepted_prior_group_losses=losses,all_other_source_copper_and_483_poses_parts_pads_fields_fixed=True,structure_and_profiles_fixed=True,fabrication_release_allowed=False)
    result['SPDX-License-Identifier']='CERN-OHL-S-2.0';output.with_suffix('.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print('Unselected full stage:',opens['native_open_edges'],'native /',opens['pad_cluster_open_edges'],'physical opens;',len(losses),'accepted group losses; canonical source unchanged',flush=True)


if __name__=='__main__':main()
