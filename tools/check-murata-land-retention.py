#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Compare the exact frozen 59-edge board with the six-land migration."""
import argparse
from collections import Counter
import hashlib
import importlib.util
import json
from pathlib import Path
import pcbnew as p

ROOT=Path(__file__).resolve().parents[1]
BEFORE_SHA256='a28258edac032d3dd047f2d7404c0752b25c472af4236b4618b3854717ddfc62'


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--before',type=Path,required=True,help='Exact pre-migration board from commit d88599a (historical evidence remains in Git)')
    parser.add_argument('--after',type=Path,default=ROOT/'hardware/coupon/rev-a/staging/led-routing-progress-trial-114mm.kicad_pcb')
    parser.add_argument('--report',type=Path)
    args=parser.parse_args()
    sha=lambda path:hashlib.sha256(path.read_bytes()).hexdigest()
    assert sha(args.before)==BEFORE_SHA256, 'Not the frozen accepted 59-edge board'
    spec=importlib.util.spec_from_file_location('retention_check',ROOT/'tools/check-routing-progress-trial.py')
    c=importlib.util.module_from_spec(spec);spec.loader.exec_module(c)
    old=p.LoadBoard(str(args.before));new=p.LoadBoard(str(args.after))
    assert Counter(c.signature(old,t) for t in old.GetTracks())==Counter(c.signature(new,t) for t in new.GetTracks()), 'Accepted copper changed'
    assert Counter(c.zone_signature(old,z) for z in old.Zones())==Counter(c.zone_signature(new,z) for z in new.Zones()), 'Accepted zone changed'
    c.module('portable','check-routing-progress-plan.py').validate_zone_structure(args.before,args.after,{'power_zones':[]})
    parts={f.GetReference():f for f in new.GetFootprints()}
    assert set(parts)=={f.GetReference() for f in old.GetFootprints()}
    lookup={c.physical_identity(q):q for f in new.GetFootprints() for q in f.Pads()}
    groups=set();migrated=[]
    for f in old.GetFootprints():
        ref=f.GetReference();other=parts[ref]
        assert (f.GetPosition(),f.GetOrientation().AsDegrees(),f.GetLayer())==(other.GetPosition(),other.GetOrientation().AsDegrees(),other.GetLayer())
        assert sorted((q.GetName(),q.GetText()) for q in f.GetFields())==sorted((q.GetName(),q.GetText()) for q in other.GetFields())
        if ref in c.murata.REFS:
            c.murata.verify_part(f,False);c.murata.verify_part(other,True);migrated.append(ref)
        else:assert f.GetFPIDAsString()==other.GetFPIDAsString()
        assert Counter(c.local_pad_signature(q) for q in f.Pads())==Counter(c.murata.normalized_signature(q,c.local_pad_signature) for q in other.Pads())
        for q in f.Pads():
            if q.GetNetname():
                group=c.physical_cluster(old,q);groups.add(group)
                assert group==c.physical_cluster(new,lookup[c.physical_identity(q)]), 'Accepted 59-edge group changed'
    stable=[]
    for _ in range(3):
        p.ZONE_FILLER(new).Fill(new.Zones());new.BuildConnectivity()
        stable.append(new.GetConnectivity().GetUnconnectedCount(False))
        assert all(group==c.physical_cluster(new,lookup[next(iter(group))]) for group in groups)
    assert stable==[59,59,59] and old.GetConnectivity().GetUnconnectedCount(False)==59
    report={'SPDX-License-Identifier':'CERN-OHL-S-2.0','status':'CHECKED_EXACT_SIX_LAND_MIGRATION_NOT_HARDWARE_MEASUREMENTS',
            'before_sha256':sha(args.before),'after_sha256':sha(args.after),'migrated_references':sorted(migrated),
            'all_accepted_copper_and_zones_preserved':True,'all_accepted_physical_pad_groups_unchanged':True,
            'physical_groups_checked':len(groups),'all_component_poses_and_fields_preserved':True,
            'stable_fill_open_counts':stable,'kicad_version':p.GetBuildVersion(),'fabrication_release_allowed':False}
    if args.report:args.report.write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
    print(json.dumps(report,sort_keys=True))


if __name__=='__main__':main()
