#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Separate UUID-based audit of ADR 0083's successful ignored land trials."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import runpy
import pcbnew as p

ROOT=Path(__file__).resolve().parents[1]
SOURCES={'accepted58':'3451177253a021d8706ff818696212afabf539a108f15ef9e5d6921e46435acc',
         'cleaned52':'7c5196b19decc3a4fbaf5724a24aae479a0fdb9c2679706f3cc5f86253992e11'}
REF187={'C40','C41','C46','C47','C48','C49','C56','C61'}
REF219={'C42','C43'}


def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def pads(board):return {q.m_Uuid.AsString():q for f in board.GetFootprints() for q in f.Pads()}
def cluster(board,pad):
    return frozenset(q.m_Uuid.AsString() for q in board.GetConnectivity().GetConnectedItems(pad) if isinstance(q,p.PAD))


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--basis',choices=SOURCES,required=True)
    ap.add_argument('--source',type=Path,required=True)
    ap.add_argument('--board',type=Path,required=True)
    args=ap.parse_args();path=args.board.resolve();source=args.source.resolve()
    assert (ROOT/'hardware/coupon/rev-a/build').resolve() in path.parents
    assert sha(source)==SOURCES[args.basis]
    old,new=(p.LoadBoard(str(x)) for x in (source,path))
    oldparts={f.GetReference():f for f in old.GetFootprints()}
    parts={f.GetReference():f for f in new.GetFootprints()}
    assert len(parts)==len(list(new.GetFootprints()))==len(oldparts)==483
    assert set(parts)==set(oldparts)
    c=runpy.run_path(str(ROOT/'tools/check-routing-progress-trial.py'))
    for ref,a in oldparts.items():
        b=parts[ref]
        assert a.GetPosition()==b.GetPosition() and a.GetLayer()==b.GetLayer()
        assert a.GetOrientation().AsDegrees()==b.GetOrientation().AsDegrees()
        assert sorted((f.GetName(),f.GetText()) for f in a.GetFields())==sorted((f.GetName(),f.GetText()) for f in b.GetFields())
        if ref in REF187|REF219:
            stem='GRM187R61A226ME15' if ref in REF187 else 'GRM219R60J476ME44'
            name='C_Murata_'+stem+('_0603' if ref in REF187 else '_0805')
            assert b.GetField('MPN').GetText()==stem
            assert b.GetFPIDAsString()=='rgb-badge-coupon-land-study:'+name
            assert len(list(b.Pads()))==2 and {q.GetNumber() for q in b.Pads()}=={'1','2'}
            for q in b.Pads():
                x=775000 if ref in REF187 else 950000
                assert q.GetFPRelativePosition()==p.VECTOR2I(-x if q.GetNumber()=='1' else x,0)
                size=(750000,900000) if ref in REF187 else (700000,1300000)
                assert q.GetSize()==p.VECTOR2I(*size)
                assert q.GetShape()==p.PAD_SHAPE_RECT
            oldpads={q.GetNumber():q for q in a.Pads()}
            for q in b.Pads():
                expected=c['local_pad_signature'](oldpads[q.GetNumber()])
                actual=list(c['local_pad_signature'](q));actual[2:6]=expected[2:6]
                assert tuple(actual)==expected, 'Other corrected-pad attributes changed'
        else:
            assert a.GetFPIDAsString()==b.GetFPIDAsString()
            assert Counter(map(c['local_pad_signature'],a.Pads()))==Counter(map(c['local_pad_signature'],b.Pads()))
    a,b=pads(old),pads(new);assert set(a)==set(b) and len(a)==2092
    def retained_groups(parent):
        groups={}
        for key,q in pads(parent).items():
            assert q.GetNumber()==b[key].GetNumber() and q.GetNetname()==b[key].GetNetname()
            if q.GetNetname():groups.setdefault(cluster(parent,q),key)
        assert all(group<=cluster(new,b[key]) for group,key in groups.items()), 'Prior UUID pad group split'
        return len(groups)
    count=retained_groups(old)
    accepted=ROOT/'hardware/coupon/rev-a/staging/led-routing-progress-trial-114mm.kicad_pcb'
    assert sha(accepted)==SOURCES['accepted58']
    assert retained_groups(p.LoadBoard(str(accepted)))==246
    oldtracks={t.m_Uuid.AsString():t for t in old.GetTracks()}
    newtracks={t.m_Uuid.AsString():t for t in new.GetTracks()}
    assert set(oldtracks)<=set(newtracks)
    for key,t in oldtracks.items():
        u=newtracks[key]
        assert t.GetNetname()==u.GetNetname() and t.GetLayer()==u.GetLayer()
        assert t.GetStart()==u.GetStart() and t.GetEnd()==u.GetEnd()
        if isinstance(t,p.PCB_VIA):
            assert isinstance(u,p.PCB_VIA) and t.TopLayer()==u.TopLayer() and t.BottomLayer()==u.BottomLayer()
            assert t.GetWidth(t.TopLayer())==u.GetWidth(u.TopLayer()) and t.GetDrillValue()==u.GetDrillValue()
        else:assert t.GetWidth()==u.GetWidth()
    added=set(newtracks)-set(oldtracks)
    assert len(added)==(1 if args.basis=='cleaned52' else 0)
    for key in added:
        t=newtracks[key]
        assert not isinstance(t,p.PCB_VIA) and t.GetNetname()=='VLED' and t.GetWidth()==200000 and t.GetLayer()==p.B_Cu
        assert t.GetStart()==p.VECTOR2I(51300000,18900001) and t.GetEnd()==p.VECTOR2I(51775000,18900001)
    structure=runpy.run_path(str(ROOT/'tools/check-routing-progress-plan.py'))['immutable_board_structure']
    assert structure(source)==structure(path)
    for ext in ('.kicad_pro','.kicad_dru'):assert source.with_suffix(ext).read_bytes()==path.with_suffix(ext).read_bytes()
    drc=path.with_suffix('.drc.json')
    runpy.run_path(str(ROOT/'tools/check-vled-supply-cleanup-probe.py'))['check_drc'](old,new,drc)
    opens=runpy.run_path(str(ROOT/'tools/report-coupon-board-connectivity.py'))['open_edges_by_net'](path)
    assert opens['native_open_edges']==opens['pad_cluster_open_edges']==(58 if args.basis=='accepted58' else 52)
    result={'SPDX-License-Identifier':'CERN-OHL-S-2.0','status':'PASS_UNSELECTED_GEOMETRY_ONLY',
        'source_sha256':sha(source),'board_sha256':sha(path),'tool_sha256':sha(Path(__file__)),
        'all_246_accepted_uuid_pad_groups_preserved':True,'all_input_uuid_pad_groups_preserved':count,
        'all_existing_copper_uuids_geometry_and_nets_preserved':True,'exact_added_tracks':len(added),
        'opens':opens,'exact_intrinsic_findings':104,'drc_sha256':sha(drc),'fabrication_release_allowed':False}
    path.with_suffix('.audit.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print('PASS:',args.basis,'exact geometry, all prior UUID pad groups, exact copper, full 104 findings')


if __name__=='__main__':main()
