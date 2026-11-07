#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Independently audit ADR 0081's ignored cleaned full-stage candidate.

No exception is added to the canonical source checker or fabrication gate.
"""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import runpy
import subprocess
import pcbnew as p

ROOT=Path(__file__).resolve().parents[1]
C=runpy.run_path(str(ROOT/'tools/check-routing-progress-trial.py'))
PLAN=ROOT/'mechanical/review/vled-cleaned-stage-plan-2026-11-01.json'
PLAN_SHA='22429a26d1c86f87a003423160e3e49b895aeeb4cbda98e0d463559e6a32007e'
SEED=ROOT/'mechanical/review/vled-rigid-floorplan-58-2026-10-30.json'


def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def inventory(board):return Counter(C['signature'](board,t) for t in board.GetTracks())


def validate(path):
    assert sha(C['OUTPUT'])=='3451177253a021d8706ff818696212afabf539a108f15ef9e5d6921e46435acc', 'Accepted source changed'
    assert sha(PLAN)==PLAN_SHA, 'Exact cleaned-stage catalog required'
    assert sha(SEED)=='6b2e6d000ba8d6b47e9be789cd501bd474891ba230dfeec0b6a16b76745d9f7d'
    plan=json.loads(PLAN.read_text());poses=json.loads(SEED.read_text())['clear_poses'][0]['poses']
    old,new,frozen=(p.LoadBoard(str(x)) for x in (C['OUTPUT'],path,C['SOURCE']))
    retired=Counter(map(tuple,plan['removed_copper']));added=Counter(map(tuple,plan['added_copper']))
    switching=json.loads((ROOT/'mechanical/review/vled-local-switching-stage-2026-10-31.json').read_text())
    for route in switching['routes']:added.update(map(tuple,route['tracks']))
    assert len(retired)==54 and len(added)==101
    before,after=inventory(old),inventory(new)
    assert before-after==retired, 'Exact retirement cohort differs'
    assert after-before==added, 'Exact added copper differs'
    assert all(before[row]==1 for row in retired)
    original=inventory(frozen);assert sum((retired & original).values())==16
    assert Counter(row['origin'] for row in plan['cleanup_ledger'])=={'frozen_215_source':16,'accepted_addition':36}
    newparts=list(new.GetFootprints());parts={f.GetReference():f for f in newparts};assert len(newparts)==len(parts)==483, 'Footprint count or duplicate reference changed'
    for f in old.GetFootprints():
        ref=f.GetReference();q=parts[ref]
        assert q.GetLayer()==f.GetLayer() and q.GetFPIDAsString()==f.GetFPIDAsString(), 'Footprint identity/layer changed: '+ref
        assert Counter(map(C['local_pad_signature'],q.Pads()))==Counter(map(C['local_pad_signature'],f.Pads())), 'Local pad geometry changed: '+ref
        assert sorted((v.GetName(),v.GetText()) for v in q.GetFields())==sorted((v.GetName(),v.GetText()) for v in f.GetFields()), 'Fields changed: '+ref
        expected=(*poses[ref]['position_iu'],poses[ref]['angle_deg']) if ref in poses else (f.GetPosition().x,f.GetPosition().y,f.GetOrientation().AsDegrees())
        assert (q.GetPosition().x,q.GetPosition().y,q.GetOrientation().AsDegrees())==expected, 'Unapproved pose: '+ref
    structure=runpy.run_path(str(ROOT/'tools/check-routing-progress-plan.py'))['immutable_board_structure']
    assert structure(C['OUTPUT'])==structure(path), 'Zone, net, outline, stack or setup changed'
    for suffix in ('.kicad_pro','.kicad_dru'):assert C['OUTPUT'].with_suffix(suffix).read_bytes()==path.with_suffix(suffix).read_bytes()
    groups={}
    for f in old.GetFootprints():
        for q in f.Pads():
            if q.GetNetname():groups.setdefault(C['physical_cluster'](old,q),C['physical_identity'](q))
    assert len(groups)==246
    lookup={C['physical_identity'](q):q for f in new.GetFootprints() for q in f.Pads()}
    for _ in range(3):
        p.ZONE_FILLER(new).Fill(new.Zones());new.BuildConnectivity()
        assert all(group<=C['physical_cluster'](new,lookup[key]) for group,key in groups.items()), 'Accepted physical pad group split'
        assert new.GetConnectivity().GetUnconnectedCount(False)==52
    def pad(ref,num):
        matches=[q for q in parts[ref].Pads() if q.GetNumber()==num];assert len(matches)==1;return matches[0]
    witnesses={
        'U37_L1_node':[('L2','1'),('U37','8'),('U37','9')],
        'U37_L2_node':[('L2','2'),('U37','6'),('U37','7')],
        'feedback':[('U37','3'),('R85','2'),('R86','1')],
        'feedback_midpoint':[('R84','2'),('R85','1')],
        'enable_pulldown':[('U37','12'),('R87','1')],
        'local_output':[('U37','4'),('U37','5'),('C46','1'),('C47','1'),('C48','1'),('C49','1'),('R84','1')],
        'input_and_VINA':[('U37','1'),('U37','10'),('U37','11'),('C44','1'),('C45','1'),('C63','1')],
        'C47_control_ground':[('C47','2'),('U37','2')],
    }
    for name,entries in witnesses.items():
        cluster=C['physical_cluster'](new,pad(*entries[0]))
        assert all(C['physical_identity'](pad(*entry)) in cluster for entry in entries), 'Required converter join missing: '+name
    opens=runpy.run_path(str(ROOT/'tools/report-coupon-board-connectivity.py'))['open_edges_by_net'](path)
    assert opens['native_open_edges']==opens['pad_cluster_open_edges']==52
    return old,new,opens,witnesses


def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--board',type=Path,required=True);args=ap.parse_args();path=args.board.resolve()
    assert (ROOT/'hardware/coupon/rev-a/build').resolve() in path.parents
    old,new,opens,witnesses=validate(path);drc=path.with_suffix('.drc.json')
    proc=subprocess.run(['/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli','pcb','drc','--format','json','--output',str(drc),str(path)],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True);drc.with_suffix('.log').write_text(proc.stdout);assert proc.returncode==0,proc.stdout
    # Reuse the strict 104-finding comparator: only unchanged U37 intra-package
    # pad positions may translate, and exact recorded poses were checked above.
    types=runpy.run_path(str(ROOT/'tools/check-vled-supply-cleanup-probe.py'))['check_drc'](old,new,drc)
    report=dict(status='PASS_UNSELECTED_CLEANED_STAGE_GEOMETRY_NOT_FABRICATION_APPROVAL',board_sha256=sha(path),tool_sha256=sha(Path(__file__)),plan_sha256=sha(PLAN),exact_added_items_from_58_edge_source=101,exact_retired_items=54,cleanup_original_source_items=16,all_246_accepted_groups_preserved=True,all_483_parts_fields_local_pads_and_exact_poses_checked=True,structure_profiles_and_rules_fixed=True,independent_converter_pad_witnesses=witnesses,open_edges=opens,full_drc_types=types,drc_sha256=sha(drc),fabrication_release_allowed=False)
    report['SPDX-License-Identifier']='CERN-OHL-S-2.0';path.with_suffix('.audit.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n');print('PASS unselected cleaned stage: 52 native/physical opens, all 246 old groups, exact 104 intrinsic findings',flush=True)


if __name__=='__main__':main()
