#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""ADR 0083 pad-only trials; preserve source bytes and report every lost group."""
import argparse
from collections import Counter
import hashlib
import json
import uuid
from pathlib import Path
import runpy
import shutil
import subprocess
import typing
if not hasattr(typing, 'TypeAlias'):
    typing.TypeAlias = object  # KiCad's bundled Python 3.9.
import pcbnew as p

ROOT = Path(__file__).resolve().parents[1]
BUILD = ROOT/'hardware/coupon/rev-a/build'
LIB = ROOT/'hardware/coupon/rev-a/staging/library-candidates.pretty'
BASES = {
    'accepted58': '3451177253a021d8706ff818696212afabf539a108f15ef9e5d6921e46435acc',
    'cleaned52': '7c5196b19decc3a4fbaf5724a24aae479a0fdb9c2679706f3cc5f86253992e11',
}
PARTS = {
    'GRM187R61A226ME15': dict(refs=['C40','C41','C46','C47','C48','C49','C56','C61'],
        old='C_Murata_GRM18_0603', name='C_Murata_GRM187R61A226ME15_0603',
        old_offset=800000, offset=775000, old_size=(900000,900000), size=(750000,900000)),
    'GRM219R60J476ME44': dict(refs=['C42','C43'],
        old='C_Murata_GRM21_0805', name='C_Murata_GRM219R60J476ME44_0805',
        old_offset=950000, offset=950000, old_size=(1200000,1300000), size=(700000,1300000)),
}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def candidate_geometry():
    helper = runpy.run_path(str(ROOT/'tools/review-murata-catalogue-lands.py'))
    result = {}
    for mpn, spec in PARTS.items():
        path = LIB/(spec['name']+'.kicad_mod')
        fp = helper['PARSE'](path)
        assert fp[:2] == ['footprint',spec['name']]
        dims = helper['dimensions'](fp)
        expected = {'a':'0.800','b':'0.750','c':'0.900'} if mpn.startswith('GRM187') else {'a':'1.200','b':'0.700','c':'1.300'}
        assert dims == {k:helper['D'](v) for k,v in expected.items()}, 'Candidate midpoint differs'
        for pad in helper['CHILDREN'](fp,'pad'):
            assert pad[2:4] == ['smd','rect']
            assert helper['one'](pad,'layers')[1:] == ['F.Cu','F.Paste','F.Mask']
        oldpath = ROOT/'hardware/coupon/rev-a/footprints/rgb-badge-coupon.pretty'/(spec['old']+'.kicad_mod')
        oldfp = helper['PARSE'](oldpath)
        assert helper['CHILDREN'](fp,'fp_rect') == helper['CHILDREN'](oldfp,'fp_rect'), 'Body/courtyard changed'
        result[mpn] = dict(footprint_sha256=sha(path), dimensions_mm={k:str(v) for k,v in dims.items()})
    return result


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--basis',choices=BASES,required=True)
    ap.add_argument('--source',type=Path,required=True)
    ap.add_argument('--output',type=Path,required=True)
    ap.add_argument('--restore-c49',action='store_true',help='Exact ADR 0083 cleaned52 contact extension only')
    args = ap.parse_args()
    source, out = args.source.resolve(), args.output.resolve()
    assert BUILD.resolve() in out.parents and out.suffix == '.kicad_pcb', 'Output must be an ignored build PCB'
    assert not any(out.with_suffix(s).exists() for s in ('.kicad_pcb','.kicad_pro','.kicad_dru','.review.json','.drc.json','.drc.log')), 'Refuse overwrite'
    assert sha(source) == BASES[args.basis], 'Wrong source bytes for declared basis'
    assert not args.restore_c49 or args.basis=='cleaned52', 'C49 extension only applies to cleaned52'
    drawings = candidate_geometry()
    c = runpy.run_path(str(ROOT/'tools/check-routing-progress-trial.py'))
    old, board = (p.LoadBoard(str(source)) for _ in range(2))
    original = {f.GetReference():f for f in old.GetFootprints()}
    parts = {f.GetReference():f for f in board.GetFootprints()}
    assert len(original) == len(parts) == len(list(board.GetFootprints())) == 483
    changed = {}
    for mpn,spec in PARTS.items():
        assert {ref for ref,f in parts.items() if f.GetField('MPN') and f.GetField('MPN').GetText()==mpn} == set(spec['refs'])
        for ref in spec['refs']:
            f = parts[ref]
            assert f.GetFPIDAsString() == 'rgb-badge-coupon:'+spec['old']
            assert len(list(f.Pads())) == 2
            for pad in f.Pads():
                assert pad.GetNumber() in ('1','2') and pad.GetShape()==p.PAD_SHAPE_RECT
                sign = -1 if pad.GetNumber()=='1' else 1
                assert pad.GetFPRelativePosition() == p.VECTOR2I(sign*spec['old_offset'],0)
                assert pad.GetSize() == p.VECTOR2I(*spec['old_size'])
                pad.SetSize(p.VECTOR2I(*spec['size']))
                pad.SetFPRelativePosition(p.VECTOR2I(sign*spec['offset'],0))
            f.SetFPIDAsString('rgb-badge-coupon-land-study:'+spec['name'])
            changed[ref] = spec
    # Normalize ONLY the exact ten checked pad geometries to their old identities.
    def identity(q):
        ref = q.GetParentFootprint().GetReference()
        if ref in changed:
            sign = -1 if q.GetNumber()=='1' else 1
            return (ref,q.GetNumber(),sign*changed[ref]['old_offset'],0)
        return c['physical_identity'](q)
    def cluster(b,q):
        return frozenset(identity(z) for z in b.GetConnectivity().GetConnectedItems(q) if isinstance(z,p.PAD))
    for ref,a in original.items():
        b = parts[ref]
        assert a.GetPosition()==b.GetPosition() and a.GetOrientation().AsDegrees()==b.GetOrientation().AsDegrees() and a.GetLayer()==b.GetLayer()
        assert sorted((f.GetName(),f.GetText()) for f in a.GetFields()) == sorted((f.GetName(),f.GetText()) for f in b.GetFields())
        if ref not in changed:
            assert a.GetFPIDAsString()==b.GetFPIDAsString()
        normalized = []
        for q in b.Pads():
            sig = list(c['local_pad_signature'](q))
            if ref in changed:
                spec = changed[ref]
                assert tuple(sig[2:6]) == (spec['offset']*(-1 if q.GetNumber()=='1' else 1),0,*spec['size'])
                sig[2:6] = [identity(q)[2],0,*spec['old_size']]
            normalized.append(tuple(sig))
        assert Counter(normalized)==Counter(c['local_pad_signature'](q) for q in a.Pads())
    copper = Counter(c['signature'](old,t) for t in old.GetTracks())
    added = Counter()
    if args.restore_c49:
        expected = ('track','VLED',51300000,18900001,50900000,18750000,'B.Cu',200000)
        assert copper[expected]==1, 'Exact retained C49 interface absent'
        target = next(q for q in parts['C49'].Pads() if q.GetNumber()=='1')
        assert target.GetNetname()=='VLED' and target.GetPosition()==p.VECTOR2I(51775000,18900001)
        track = p.PCB_TRACK(board)
        track.SetStart(p.VECTOR2I(51300000,18900001));track.SetEnd(target.GetPosition())
        track.SetLayer(p.B_Cu);track.SetWidth(200000);track.SetNetCode(target.GetNetCode())
        track.SetUuid(p.KIID(str(uuid.uuid5(uuid.NAMESPACE_URL,'rgb-badge:adr83:exact-c49-land-contact'))))
        board.Add(track);added[c['signature'](board,track)]+=1
    prior = {}
    for f in old.GetFootprints():
        for q in f.Pads():
            if q.GetNetname(): prior.setdefault(cluster(old,q),identity(q))
    lookup = {identity(q):q for f in board.GetFootprints() for q in f.Pads()}
    snapshots = []
    sorter = runpy.run_path(str(ROOT/'tools/generate-paired-charger-114mm-routing.py'))['sorted_native_tracks']
    out.parent.mkdir(parents=True,exist_ok=True)
    for n in range(3):
        p.ZONE_FILLER(board).Fill(board.Zones()); board.BuildConnectivity()
        assert Counter(c['signature'](board,t) for t in board.GetTracks())==copper+added
        lost = []
        for group,key in sorted(prior.items(),key=lambda row:row[1]):
            remaining = cluster(board,lookup[key])
            if not group <= remaining:
                lost.append(dict(anchor=key,net=lookup[key].GetNetname(),old_group_size=len(group),
                    missing_pad_identities=sorted(group-remaining)))
        p.SaveBoard(str(out),board)
        out.write_text(sorter(out.read_text(),expected=len(list(board.GetTracks()))))
        snapshots.append(dict(fill=n+1,sha256=sha(out),native_opens=board.GetConnectivity().GetUnconnectedCount(False),lost_groups=lost))
    assert all({k:v for k,v in s.items() if k!='fill'}=={k:v for k,v in snapshots[0].items() if k!='fill'} for s in snapshots)
    for suffix in ('.kicad_pro','.kicad_dru'): shutil.copyfile(source.with_suffix(suffix),out.with_suffix(suffix))
    table = '(fp_lib_table\n'
    for alias,path in [('rgb-badge-coupon', ROOT/'hardware/coupon/rev-a/footprints/rgb-badge-coupon.pretty'),
                       ('rgb-badge-coupon-land-study', LIB)]:
        table += '  (lib (name "'+alias+'")(type "KiCad")(uri "'+str(path)+'")(options "")(descr "Local land trial"))\n'
    (out.parent/'fp-lib-table').write_text(table+')\n')
    structure = runpy.run_path(str(ROOT/'tools/check-routing-progress-plan.py'))['immutable_board_structure']
    assert structure(source)==structure(out)
    drc = out.with_suffix('.drc.json')
    proc = subprocess.run(['/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli','pcb','drc','--format','json','--output',str(drc),str(out)],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
    drc.with_suffix('.log').write_text(proc.stdout); assert proc.returncode==0,proc.stdout
    actual = json.loads(drc.read_text())
    types = dict(Counter(v['type'] for v in actual['violations']))
    exact104 = False
    if len(actual['violations'])==104 and types=={'clearance':104}:
        runpy.run_path(str(ROOT/'tools/check-vled-supply-cleanup-probe.py'))['check_drc'](old,board,drc)
        exact104 = True
    opens = runpy.run_path(str(ROOT/'tools/report-coupon-board-connectivity.py'))['open_edges_by_net'](out)
    if args.restore_c49:
        assert not snapshots[-1]['lost_groups'] and exact104
        assert opens['native_open_edges']==opens['pad_cluster_open_edges']==52
    assert sha(source)==BASES[args.basis]
    result = dict(status='UNSELECTED_TEN_CAPACITOR_PAD_ONLY_FEASIBILITY',basis=args.basis,
        source_sha256=sha(source),candidate_sha256=sha(out),tool_sha256=sha(Path(__file__)),
        candidate_drawings=drawings,changed_references=sorted(changed),prior_group_count=len(prior),
        added_c49_contact=[list(row) for row in added],
        all_source_copper_retained=True,all_poses_fields_numbered_nets_and_other_pad_data_retained=True,
        all_prior_groups_preserved=not snapshots[-1]['lost_groups'],stable_fills=snapshots,
        opens=opens,full_drc_types=types,exact_104_intrinsic_findings=exact104,drc_sha256=sha(drc),
        fabrication_release_allowed=False,canonical_geometry_changed=False,kicad_version=p.GetBuildVersion())
    result['SPDX-License-Identifier'] = 'CERN-OHL-S-2.0'
    out.with_suffix('.review.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps(dict(basis=args.basis,opens=opens['native_open_edges'],physical_opens=opens['pad_cluster_open_edges'],lost_groups=len(snapshots[-1]['lost_groups']),drc=types),sort_keys=True),flush=True)


if __name__ == '__main__': main()
