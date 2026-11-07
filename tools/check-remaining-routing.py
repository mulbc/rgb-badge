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


def original_orphans(path):
    c=runpy.run_path(str(policy.ROOT/'tools/check-routing-progress-trial.py'));source=p.LoadBoard(str(path));b=p.LoadBoard(str(path))
    rows=json.loads(c['PLAN'].read_text())['retired_orphan_microvias'];assert len(rows)==3
    def pads(board):return{q.m_Uuid.AsString():q for f in board.GetFootprints() for q in f.Pads() if q.GetNetname()}
    def cluster(board,q):return frozenset(z.m_Uuid.AsString() for z in board.GetConnectivity().GetConnectedItems(q) if isinstance(z,p.PAD))
    for row in rows:
        kind,net,x,y,top,bottom,width,drill=row;assert kind=='via'
        v=p.PCB_VIA(b);v.SetPosition(p.VECTOR2I(x,y));v.SetViaType(p.VIATYPE_MICROVIA)
        v.SetLayerPair(b.GetLayerID(top),b.GetLayerID(bottom));v.SetWidth(width);v.SetDrill(drill);v.SetNetCode(b.FindNet(net).GetNetCode())
        v.SetUuid(p.KIID(str(uuid.uuid5(uuid.NAMESPACE_URL,'rgb-badge:ADR0092:orphan:'+repr(row)))));b.Add(v)
    p.ZONE_FILLER(b).Fill(b.Zones());b.BuildConnectivity()
    aa,bb=pads(source),pads(b)
    assert all(cluster(source,q)==cluster(b,bb[k]) for k,q in aa.items())
    assert b.GetConnectivity().GetUnconnectedCount(False)==policy.load_plan()['native_opens']
    out=BUILD/'original-orphans.kicad_pcb';p.SaveBoard(str(out),b)
    for ext in ('.kicad_pro','.kicad_dru'):shutil.copyfile(path.with_suffix(ext),out.with_suffix(ext))
    raw=drc(out,out.with_suffix('.drc.json'));assert len(raw['violations'])==107
    extra=[v for v in raw['violations'] if v['type']=='via_dangling'];assert len(extra)==3
    items={t.m_Uuid.AsString():t for t in b.GetTracks()}
    found=Counter(c['signature'](b,items[v['items'][0]['uuid']]) for v in extra)
    assert found==Counter(map(tuple,rows)) and all(v['severity']=='warning' for v in extra)
    raw['violations']=[v for v in raw['violations'] if v['type']!='via_dangling']
    filtered=out.with_suffix('.intrinsic.json');filtered.write_text(json.dumps(raw))
    runpy.run_path(str(policy.ROOT/'tools/check-vled-supply-cleanup-probe.py'))['check_drc'](source,b,filtered)
    return {'all_live_pad_groups_identical':True,'native_opens':policy.load_plan()['native_opens'],'only_three_exact_original_orphan_warnings':True}


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
    if args.check_orphans:result['original_orphan_restoration']=original_orphans(path)
    (BUILD/'current.audit.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print('PASS routing successor:',result['native_opens'],'native/physical opens, all 231 parent groups, exact unchanged 104 findings',flush=True)


if __name__=='__main__':main()
