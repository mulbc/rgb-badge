#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Independent native audit of the ignored ADR 0075/0076 candidate.

This does not extend the accepted source checker or authorize fabrication.
"""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import runpy
import subprocess
import pcbnew as p

ROOT = Path(__file__).resolve().parents[1]
C = runpy.run_path(str(ROOT/'tools/check-routing-progress-trial.py'))
PLAN = ROOT/'mechanical/review/vled-supply-cleanup-plan-2026-11-01.json'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate(board_path):
    assert sha(C['OUTPUT']) == '3451177253a021d8706ff818696212afabf539a108f15ef9e5d6921e46435acc'
    assert sha(PLAN) == '2394f14ceda5e7616889cc791eee8f5865984be3d4cdd44a6979b0aa6fd816e1'
    plan = json.loads(PLAN.read_text())
    structure = runpy.run_path(str(ROOT/'tools/check-routing-progress-plan.py'))['immutable_board_structure']
    assert structure(C['OUTPUT']) == structure(board_path), 'Outline, stack, setup, nets or zone definitions changed'
    old, new = (p.LoadBoard(str(path)) for path in (C['OUTPUT'], board_path))
    before = Counter(C['signature'](old, t) for t in old.GetTracks())
    after = Counter(C['signature'](new, t) for t in new.GetTracks())
    retired = Counter(tuple(row['signature']) for row in plan['removed_copper'])
    switching = json.loads((ROOT/'mechanical/review/vled-local-switching-pair-2026-10-31.json').read_text())
    added = Counter(map(tuple, plan['added_supply_copper']))
    for route in switching['routes']:
        added.update(map(tuple, route['tracks']))
    assert len(retired) == 23 and len(added) == 65
    assert before-after == retired, 'Exact removal cohort differs'
    assert after-before == added, 'Exact addition cohort differs'
    oldparts = {f.GetReference(): f for f in old.GetFootprints()}
    parts = {f.GetReference(): f for f in new.GetFootprints()}
    assert set(parts) == set(oldparts) and len(parts) == 483
    for ref, a in oldparts.items():
        b = parts[ref]
        assert a.GetFPIDAsString() == b.GetFPIDAsString() and a.GetLayer() == b.GetLayer()
        assert Counter(map(C['local_pad_signature'], a.Pads())) == Counter(map(C['local_pad_signature'], b.Pads()))
        assert sorted((f.GetName(),f.GetText()) for f in a.GetFields()) == sorted((f.GetName(),f.GetText()) for f in b.GetFields())
        expected = {'U37': (45500000,17500000,0), 'L2': (49550000,17500000,-90)}.get(ref, (a.GetPosition().x,a.GetPosition().y,a.GetOrientation().AsDegrees()))
        assert (b.GetPosition().x,b.GetPosition().y,b.GetOrientation().AsDegrees()) == expected
    assert Counter(C['zone_signature'](old,z) for z in old.Zones()) == Counter(C['zone_signature'](new,z) for z in new.Zones())
    assert new.GetCopperLayerCount() == old.GetCopperLayerCount()
    for suffix in ('.kicad_pro','.kicad_dru'):
        assert board_path.with_suffix(suffix).read_bytes() == C['OUTPUT'].with_suffix(suffix).read_bytes()
    prior = {}
    for f in old.GetFootprints():
        for pad in f.Pads():
            if pad.GetNetname():
                prior.setdefault(C['physical_cluster'](old,pad),C['physical_identity'](pad))
    lookup = {C['physical_identity'](pad):pad for f in new.GetFootprints() for pad in f.Pads()}
    assert len(prior) == 246
    assert all(group <= C['physical_cluster'](new,lookup[key]) for group,key in prior.items())
    helper = runpy.run_path(str(ROOT/'tools/routing_track_replacements.py'))
    for leaf in plan['leaf_branch_contacts']:
        key = tuple(leaf['signature'])
        item = next(t for t in old.GetTracks() if C['signature'](old,t) == key)
        assert [row for row,_ in helper['contacts'](old,item,C['signature'],C['physical_identity'])] == leaf['frozen_58_contacts']
        assert len(leaf['current_contacts']) == 1
        bus = tuple(leaf['current_contacts'][0][1:])
        assert after[bus] == before[bus] == 1
    reporter = runpy.run_path(str(ROOT/'tools/report-coupon-board-connectivity.py'))
    opens = reporter['open_edges_by_net'](board_path)
    assert opens['native_open_edges'] == opens['pad_cluster_open_edges'] == 56
    return old,new,opens


def check_drc(old,new,path):
    baseline = json.loads((ROOT/'docs/development/led-routing-progress-58-drc-2026-10-30.json').read_text())
    actual = json.loads(path.read_text())
    oldpads = {q.m_Uuid.AsString():q for f in old.GetFootprints() for q in f.Pads()}
    newpads = {q.m_Uuid.AsString():q for f in new.GetFootprints() for q in f.Pads()}
    u37 = {q.m_Uuid.AsString() for f in new.GetFootprints() if f.GetReference()=='U37' for q in f.Pads()}
    def key(v,translated=False):
        assert v['type'] == 'clearance' and len(v['items']) == 2
        ids = {row['uuid'] for row in v['items']}
        rows = []
        for row in v['items']:
            uid = row['uuid']; pad = (newpads if translated else oldpads)[uid]
            pos = {axis:round(value/1e6,4) for axis,value in zip(('x','y'),(pad.GetPosition().x,pad.GetPosition().y))}
            assert row['pos'] == pos, 'DRC coordinates do not match exact current pad positions'
            if translated and uid in u37:
                assert ids <= u37, 'Translation only allowed within the unchanged U37 package'
                pad = oldpads[uid]
                pos = {axis:round(value/1e6,4) for axis,value in zip(('x','y'),(pad.GetPosition().x,pad.GetPosition().y))}
            rows.append((uid,row['description'],pos['x'],pos['y']))
        return v['type'],v['description'],v['severity'],tuple(sorted(rows))
    assert len(actual['violations']) == len(baseline['violations']) == 104
    assert Counter(key(v,True) for v in actual['violations']) == Counter(key(v) for v in baseline['violations'])
    assert actual['ignored_checks'] == baseline['ignored_checks']
    assert actual['included_severities'] == baseline['included_severities']
    return dict(clearance=104)


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--board',type=Path,required=True)
    args=ap.parse_args();path=args.board.resolve()
    assert (ROOT/'hardware/coupon/rev-a/build').resolve() in path.parents
    old,new,opens=validate(path)
    drc=path.with_suffix('.drc.json')
    proc=subprocess.run(['/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli','pcb','drc','--format','json','--output',str(drc),str(path)],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
    drc.with_suffix('.log').write_text(proc.stdout)
    assert proc.returncode == 0,proc.stdout
    types=check_drc(old,new,drc)
    result=dict(status='PASS_UNSELECTED_GEOMETRY_ONLY',board_sha256=sha(path),tool_sha256=sha(Path(__file__)),plan_sha256=sha(PLAN),
                exact_additions=65,exact_removals=23,retained_accepted_items=18315,all_246_old_groups_preserved=True,
                exact_parts_local_pads_poses_zones_and_profiles_checked=True,full_drc_types=types,
                drc_sha256=sha(drc),drc_position_policy='Only exact U37 intra-package pad positions translate; identities/descriptions/severity and all other positions remain exact',
                open_edges=opens,fabrication_release_allowed=False)
    result['SPDX-License-Identifier']='CERN-OHL-S-2.0'
    path.with_suffix('.audit.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print('PASS: exact geometry; all 246 previous groups; 56 native/physical opens; full DRC 104 intrinsic findings',flush=True)


if __name__=='__main__':
    main()
