#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Direct ADR 0084 comparison with the frozen pre-migration 58-edge board."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import runpy
import pcbnew as p

ROOT=Path(__file__).resolve().parents[1]


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--before',type=Path,required=True)
    ap.add_argument('--after',type=Path,required=True)
    ap.add_argument('--report',type=Path,required=True)
    args=ap.parse_args();sha=lambda path:hashlib.sha256(path.read_bytes()).hexdigest()
    assert sha(args.before)=='3451177253a021d8706ff818696212afabf539a108f15ef9e5d6921e46435acc'
    c=runpy.run_path(str(ROOT/'tools/check-routing-progress-trial.py'))
    policy=runpy.run_path(str(ROOT/'tools/remaining_murata_migration.py'))
    old,new=(p.LoadBoard(str(x)) for x in (args.before,args.after))
    before={f.GetReference():f for f in old.GetFootprints()};after={f.GetReference():f for f in new.GetFootprints()}
    assert len(before)==len(after)==len(list(new.GetFootprints()))==483 and before.keys()==after.keys()
    for ref,a in before.items():
        b=after[ref]
        assert a.GetPosition()==b.GetPosition() and a.GetOrientation().AsDegrees()==b.GetOrientation().AsDegrees() and a.GetLayer()==b.GetLayer()
        assert sorted((f.GetName(),f.GetText()) for f in a.GetFields())==sorted((f.GetName(),f.GetText()) for f in b.GetFields())
        if ref in policy['REFS']:
            policy['verify_part'](a,False);policy['verify_part'](b,True)
        else:assert a.GetFPIDAsString()==b.GetFPIDAsString()
        assert Counter(map(c['local_pad_signature'],a.Pads()))==Counter(policy['normalized_signature'](q,c['local_pad_signature'](q)) for q in b.Pads())
        def graphics(f):
            rows=[]
            for g in f.GraphicalItems():
                if isinstance(g,p.PCB_TEXT):
                    rows.append(('text',g.GetLayer(),g.GetText(),g.GetPosition().x,g.GetPosition().y,
                        g.GetTextSize().x,g.GetTextSize().y,g.GetTextAngle().AsDegrees(),
                        g.GetTextThickness(),g.IsMirrored(),g.IsVisible()))
                else:
                    rows.append(('shape',g.GetShape(),g.GetLayer(),g.GetStart().x,g.GetStart().y,
                                 g.GetEnd().x,g.GetEnd().y,g.GetWidth()))
            return Counter(rows)
        assert graphics(a)==graphics(b), 'Component body/courtyard changed'
    assert Counter(c['signature'](old,t) for t in old.GetTracks())==Counter(c['signature'](new,t) for t in new.GetTracks())
    assert Counter(c['zone_signature'](old,z) for z in old.Zones())==Counter(c['zone_signature'](new,z) for z in new.Zones())
    structure=runpy.run_path(str(ROOT/'tools/check-routing-progress-plan.py'))['immutable_board_structure']
    assert structure(args.before)==structure(args.after)
    for ext in ('.kicad_pro','.kicad_dru'):assert args.before.with_suffix(ext).read_bytes()==args.after.with_suffix(ext).read_bytes()
    # Persistent UUID groups avoid relying on the corrected-coordinate mapping.
    def pads(board):return {q.m_Uuid.AsString():q for f in board.GetFootprints() for q in f.Pads()}
    def cluster(board,q):return frozenset(z.m_Uuid.AsString() for z in board.GetConnectivity().GetConnectedItems(q) if isinstance(z,p.PAD))
    a,b=pads(old),pads(new);assert a.keys()==b.keys() and len(a)==2092
    groups={}
    for key,q in a.items():
        assert q.GetNumber()==b[key].GetNumber() and q.GetNetname()==b[key].GetNetname()
        if q.GetNetname():groups.setdefault(cluster(old,q),key)
    assert len(groups)==246
    fills=[]
    for _ in range(3):
        p.ZONE_FILLER(new).Fill(new.Zones());new.BuildConnectivity()
        assert all(group==cluster(new,b[key]) for group,key in groups.items()), 'Frozen physical UUID group changed'
        fills.append(new.GetConnectivity().GetUnconnectedCount(False))
    assert fills==[58,58,58]
    opens=runpy.run_path(str(ROOT/'tools/report-coupon-board-connectivity.py'))['open_edges_by_net'](args.after)
    assert opens['native_open_edges']==opens['pad_cluster_open_edges']==58
    result={'SPDX-License-Identifier':'CERN-OHL-S-2.0','status':'EXACT_TEN_LAND_SOURCE_RETENTION_NOT_HARDWARE_EVIDENCE',
        'before_sha256':sha(args.before),'after_sha256':sha(args.after),'tool_sha256':sha(Path(__file__)),
        'migrated_references':list(policy['REFS']),'all_copper_zones_profiles_and_rules_preserved':True,
        'all_483_poses_fields_and_graphics_preserved':True,'all_246_uuid_pad_groups_unchanged':True,
        'stable_fill_counts':fills,'opens':opens,'fabrication_release_allowed':False}
    args.report.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print('PASS exact ten-land retention: all 246 UUID pad groups, all copper/poses; 58 native/physical opens')


if __name__=='__main__':main()
