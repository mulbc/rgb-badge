#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Native full-ledger, pad-group and exact-DRC gate for the routing-closure successor."""
import argparse
from collections import Counter
import json
from pathlib import Path
import runpy
import shutil
import subprocess
import uuid
import pcbnew as p
import routing_remaining as policy

CLI='/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli'
BUILD=policy.ROOT/'hardware/coupon/rev-a/build/remaining-routing'


def drc(path,output):
    proc=subprocess.run([CLI,'pcb','drc','--format','json','--output',str(output),str(path)],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
    output.with_suffix('.log').write_text(proc.stdout)
    assert proc.returncode==0,proc.stdout
    return json.loads(output.read_text())


def selected_retirement_probe(path):
    """Diagnostic rejected copy; strict retirement proof belongs to the parent."""
    before=policy.sha(path)
    c=runpy.run_path(str(policy.ROOT/'tools/check-routing-progress-trial.py'))
    source=p.LoadBoard(str(path));b=p.LoadBoard(str(path))
    rows=json.loads(c['PLAN'].read_text())['retired_orphan_microvias'];assert len(rows)==3
    injected={}
    for row in rows:
        _,net,x,y,top,bottom,width,drill=row
        v=p.PCB_VIA(b);v.SetPosition(p.VECTOR2I(x,y));v.SetViaType(p.VIATYPE_MICROVIA)
        v.SetLayerPair(b.GetLayerID(top),b.GetLayerID(bottom));v.SetWidth(width);v.SetDrill(drill);v.SetNetCode(b.FindNet(net).GetNetCode())
        v.SetUuid(p.KIID(str(uuid.uuid5(uuid.NAMESPACE_URL,'rgb-badge:ADR0092:orphan:'+repr(row)))));b.Add(v)
        injected[v.m_Uuid.AsString()]=row
    p.ZONE_FILLER(b).Fill(b.Zones());b.BuildConnectivity()
    pads=lambda board:{q.m_Uuid.AsString():q for f in board.GetFootprints() for q in f.Pads() if q.GetNetname()}
    cluster=lambda board,q:frozenset(z.m_Uuid.AsString() for z in board.GetConnectivity().GetConnectedItems(q) if isinstance(z,p.PAD))
    aa,bb=pads(source),pads(b);items={t.m_Uuid.AsString():t for t in b.GetTracks()}
    observed=[{'expected':row,'observed':list(c['signature'](b,items[uid])) if uid in items else None} for uid,row in injected.items()]
    out=BUILD/'selected-retirement-probe.kicad_pcb';p.SaveBoard(str(out),b)
    for ext in ('.kicad_pro','.kicad_dru'):shutil.copyfile(path.with_suffix(ext),out.with_suffix(ext))
    report=out.with_suffix('.drc.json');raw=drc(out,report)
    assert policy.sha(path)==before,'Diagnostic changed selected source'
    return {'status':'REJECTED_COUNTERFACTUAL_NOT_SELECTED_SOURCE','source_unchanged':True,
        'all_live_pad_groups_identical':all(cluster(source,q)==cluster(b,bb[k]) for k,q in aa.items()),
        'native_opens':b.GetConnectivity().GetUnconnectedCount(False),
        'injected_via_identity':observed,'drc_types':dict(Counter(v['type'] for v in raw['violations'])),
        'drc_sha256':policy.sha(report),'raw_report':str(report.relative_to(policy.ROOT))}


def inherited_retirement_proof():
    parent=runpy.run_path(str(policy.ROOT/'tools/check-switch-routing.py'))
    parent['BUILD'].mkdir(parents=True,exist_ok=True)
    shutil.copyfile(BUILD/'fp-lib-table',parent['BUILD']/'fp-lib-table')
    result=parent['original_orphans'](policy.PARENT)
    result.update(basis='IMMUTABLE_43_OPEN_PARENT',board_sha256=policy.PARENT_SHA)
    return result


def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--board',type=Path,default=policy.OUTPUT)
    ap.add_argument('--check-orphans',action='store_true');args=ap.parse_args()
    path=args.board.resolve();BUILD.mkdir(parents=True,exist_ok=True)
    (BUILD/'fp-lib-table').write_text('(fp_lib_table (lib (name "rgb-badge-coupon")(type "KiCad")(uri "'+str(policy.ROOT/'hardware/coupon/rev-a/footprints/rgb-badge-coupon.pretty')+'")(options "")(descr "Local source")))\n')
    old,new,result=policy.audit(path)
    result.update(native_opens=result['native_open_edges'],physical_opens=result['pad_cluster_open_edges'],all_231_parent_groups_preserved=True)
    report=BUILD/'current.drc.json';drc(path,report)
    runpy.run_path(str(policy.ROOT/'tools/check-vled-supply-cleanup-probe.py'))['check_drc'](old,new,report)
    result.update({'SPDX-License-Identifier':'CERN-OHL-S-2.0','status':'PASS_GEOMETRIC_ROUTING_STUDY_ONLY',
        'board_sha256':policy.sha(path),'parent_sha256':policy.PARENT_SHA,'plan_sha256':policy.PLAN_SHA,
        'policy_sha256':policy.sha(Path(policy.__file__)),'checker_sha256':policy.sha(Path(__file__)),
        'drc_sha256':policy.sha(report),'intrinsic_findings':104,'fabrication_release_allowed':False})
    if args.check_orphans:
        result['inherited_original_orphan_restoration']=inherited_retirement_proof()
        result['selected_retirement_probe']=selected_retirement_probe(path)
    (BUILD/'current.audit.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print('PASS routing successor:',result['native_opens'],'native/physical opens, all 231 parent groups, exact unchanged 104 findings',flush=True)


if __name__=='__main__':main()
