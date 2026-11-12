#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Audit an ignored ADR 0117 PCB migration; report losses without accepting them.

The source is frozen. Functional terminal identities, rather than the old
wrong physical-pad identities, define connections which must survive.
This read-only audit does not select a PCB or authorize fabrication.
"""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import runpy
import pcbnew as p
import rse_pin_migration as mapping

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT/'hardware/coupon/rev-a/staging/led-remaining-routing-trial-114mm.kicad_pcb'
SOURCE_SHA = 'da3764ddf5c8c615529340c33c92974cff3fd036b937b5e4a53c408e0b141637'
RETIRED = {
    'a19a5928-5dec-5a62-a738-6b2f7769e217', 'e0ee2639-b200-5dbf-9c43-57813a69e234',
    'cff72e1e-b062-5a84-bfc3-b45fb76a7d69', '2e514485-4464-59f2-a6ba-1397d4fad179',
    '288b2d15-1433-5042-87a6-7f1436e992e4', '6be521a2-c717-5172-96b7-f2f9e6bc46f8',
    '6fced5d8-797a-56fa-a82b-87a9a87056ff', 'd27e9101-48d6-553e-9b60-c2bb73866a79',
}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def terminal(pad):
    return (pad.GetParentFootprint().GetReference(), pad.GetNumber())


def corrected(key):
    return (key[0], mapping.FORWARD[key[1]]) if key[0] in mapping.LEGACY else key


def group(board, pad):
    return frozenset(terminal(q) for q in board.GetConnectivity().GetConnectedItems(pad)
                     if isinstance(q,p.PAD) and q.GetNetname())


def audit(path):
    assert sha(SOURCE) == SOURCE_SHA, 'Historical source changed'
    helpers = runpy.run_path(str(ROOT/'tools/check-routing-progress-trial.py'))
    old, new = (p.LoadBoard(str(f)) for f in (SOURCE,path))
    old.BuildConnectivity();new.BuildConnectivity()
    oldparts = {f.GetReference():f for f in old.GetFootprints()}
    newparts = {f.GetReference():f for f in new.GetFootprints()}
    assert oldparts.keys() == newparts.keys() and len(newparts)==483
    for ref, f in oldparts.items():
        other = newparts[ref]
        assert f.m_Uuid.AsString()==other.m_Uuid.AsString()
        assert (f.GetFPIDAsString(),f.GetLayer(),f.GetPosition(),f.GetOrientation().AsDegrees()) == (
            other.GetFPIDAsString(),other.GetLayer(),other.GetPosition(),other.GetOrientation().AsDegrees()), ref
        assert sorted((q.GetName(),q.GetText()) for q in f.GetFields()) == sorted(
            (q.GetName(),q.GetText()) for q in other.GetFields()), 'Part fields changed: '+ref
        before = {q.GetNumber():q for q in f.Pads() if q.GetNumber()}
        after = {q.GetNumber():q for q in other.Pads() if q.GetNumber()}
        if ref in mapping.LEGACY:
            assert f.GetValue()==mapping.MPN and f.GetFPIDAsString()==mapping.FOOTPRINT
            assert len(list(f.Pads()))==len(list(other.Pads()))==8
            assert {n:q.GetNetname() for n,q in before.items()}==mapping.LEGACY[ref]
            assert {n:q.GetNetname() for n,q in after.items()}==mapping.CORRECTED[ref]
            unused=after['5']
            assert not any(t.IsOnLayer(p.B_Cu) and t.GetEffectiveShape(p.B_Cu).Collide(
                unused.GetEffectiveShape(p.B_Cu),0) for t in new.GetTracks()), 'Inverse output touched by copper: '+ref
        def normalized(q):
            row = list(helpers['local_pad_signature'](q))
            if ref in mapping.LEGACY:
                row[1] = mapping.LEGACY[ref][q.GetNumber()]
            return tuple(row)
        assert Counter(map(helpers['local_pad_signature'],f.Pads())) == Counter(
            normalized(q) for q in other.Pads()), 'Physical pad changed: '+ref
    structure = runpy.run_path(str(ROOT/'tools/check-routing-progress-plan.py'))['immutable_board_structure']
    assert structure(SOURCE)==structure(path), 'Outline/stack/setup/net/zone structure changed'
    for ext in ('.kicad_pro','.kicad_dru'):
        assert path.with_suffix(ext).read_bytes()==SOURCE.with_suffix(ext).read_bytes(), 'Profile changed'
    olditems = {t.m_Uuid.AsString():t for t in old.GetTracks()}
    newitems = {t.m_Uuid.AsString():t for t in new.GetTracks()}
    assert olditems.keys()-newitems.keys()==RETIRED, 'Obsolete copper retirement differs'
    accepted=Counter(map(tuple,json.loads((ROOT/'mechanical/review/remaining-routing-plan.json').read_text())['added_copper']))
    for uid in RETIRED:
        t=olditems[uid];row=helpers['signature'](old,t)
        # The historical plan includes a via-type suffix; the shared signature
        # predates that field. Normalize only that representation difference.
        candidates=[tuple(row),tuple(row)+(int(t.GetViaType()),)] if isinstance(t,p.PCB_VIA) else [tuple(row)]
        assert not any(accepted[q] for q in candidates), 'Previously accepted addition retired'
    assert all(helpers['signature'](old,t)==helpers['signature'](new,newitems[uid])
               for uid,t in olditems.items() if uid not in RETIRED), 'Retained copper changed'
    additions=[]
    layers = [p.F_Cu,p.In1_Cu,p.In2_Cu,p.In3_Cu,p.In4_Cu,p.B_Cu]
    for uid in sorted(newitems.keys()-olditems.keys()):
        t=newitems[uid]
        if isinstance(t,p.PCB_VIA):
            assert t.GetViaType()==p.VIATYPE_MICROVIA
            assert (t.GetWidth(t.TopLayer()),t.GetDrillValue())==(300000,100000)
            assert abs(layers.index(t.TopLayer())-layers.index(t.BottomLayer()))==1
            assert {t.TopLayer(),t.BottomLayer()}!={p.In2_Cu,p.In3_Cu}
        else:
            assert t.GetWidth()==200000 and t.GetStart()!=t.GetEnd()
        assert t.GetNetname() in {'+3V3_APP','DISPLAY_CLEAR_OK','DISPLAY_ARM_CLK','ARM_LATCH'}
        additions.append(dict(uuid=uid,signature=helpers['signature'](new,t)))
    oldpads={terminal(q):q for f in old.GetFootprints() for q in f.Pads() if q.GetNetname()}
    newpads={terminal(q):q for f in new.GetFootprints() for q in f.Pads() if q.GetNetname()}
    assert {corrected(k) for k in oldpads}==set(newpads)
    groups={group(old,q) for q in oldpads.values()}
    assert len(groups)==223
    losses=[]
    for g in sorted(groups,key=repr):
        expected=frozenset(corrected(k) for k in g);anchor=min(expected)
        actual=group(new,newpads[anchor])
        if not expected<=actual:
            losses.append(dict(net=newpads[anchor].GetNetname(),expected=sorted(expected),
                               missing=sorted(expected-actual)))
    newgroups={group(new,q) for q in newpads.values()}
    native=new.GetConnectivity().GetUnconnectedCount(False)
    physical=len(newgroups)-len({q.GetNetname() for q in newpads.values()})
    result={'SPDX-License-Identifier':'CERN-OHL-S-2.0','status':'DIAGNOSTIC_NOT_SELECTED',
        'source_sha256':SOURCE_SHA,'candidate_sha256':sha(path),'native_opens':native,
        'physical_opens':physical,'source_semantic_groups':len(groups),'candidate_groups':len(newgroups),
        'semantic_group_losses':losses,'retired_copper':[dict(uuid=uid,signature=helpers['signature'](old,olditems[uid])) for uid in sorted(RETIRED)],
        'added_copper':additions,'source_structure_profiles_and_all_other_parts_preserved':True,
        'fabrication_release_allowed':False}
    return old,new,result


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--board',type=Path,required=True)
    ap.add_argument('--report',type=Path,required=True)
    ap.add_argument('--require-complete',action='store_true')
    ap.add_argument('--drc',type=Path)
    args=ap.parse_args();path=args.board.resolve()
    build=(ROOT/'hardware/coupon/rev-a/build').resolve()
    selected=ROOT/'hardware/coupon/rev-a/staging/led-rse-corrected-routing-trial-114mm.kicad_pcb'
    assert (build in path.parents or path==selected) and build in args.report.resolve().parents
    old,new,result=audit(path)
    # Persist honest diagnostics before a selection gate may reject them.
    args.report.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print('Diagnostic:',result['native_opens'],'native /',result['physical_opens'],
          'physical opens;',len(result['semantic_group_losses']),'lost functional groups')
    if args.require_complete:
        assert not result['semantic_group_losses'], 'Prior functional connections remain lost'
        assert result['native_opens']==result['physical_opens']<=35, 'Migration is incomplete'
        assert args.drc is not None, 'Complete native DRC evidence required'
        # All package poses are fixed, so compare full findings without translation.
        baseline=json.loads((ROOT/'docs/development/remaining-routing-drc-2026-11-07.json').read_text())
        actual=json.loads(args.drc.read_text())
        assert len(actual['violations'])==len(baseline['violations'])==104
        def finding(v):
            # The order of two implicated items has no physical meaning.
            v=dict(v);v['items']=sorted(v['items'],key=lambda row:row['uuid'])
            return json.dumps(v,sort_keys=True)
        assert Counter(map(finding,actual['violations']))==Counter(map(finding,baseline['violations']))
        assert actual['ignored_checks']==baseline['ignored_checks']
        assert actual['included_severities']==baseline['included_severities']
        print('Complete migration geometry gate passed; replay/fault/visual review and selection still required')


if __name__=='__main__':main()
