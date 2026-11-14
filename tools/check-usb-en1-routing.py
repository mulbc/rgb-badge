#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Native full ledger, connection and exact-DRC gate for ADR 0121."""
import argparse
from collections import Counter
import json
from pathlib import Path
import shutil
import subprocess
import pcbnew as p
import routing_usb_en1 as policy

BUILD=policy.ROOT/'hardware/coupon/rev-a/build/usb-en1-locality'
CLI='/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli'


def drc(board,report):
    r=subprocess.run([CLI,'pcb','drc','--format','json','--output',str(report),str(board)],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
    report.with_suffix('.log').write_text(r.stdout)
    assert r.returncode==0,r.stdout
    return json.loads(report.read_text())


def restored_probe(source,plan):
    b=p.LoadBoard(str(source))
    for row in plan['retired_copper']:
        s=row['signature']
        if s[0]=='track':
            _,net,x,y,a,c,layer,width=s;t=p.PCB_TRACK(b);t.SetStart(p.VECTOR2I(x,y));t.SetEnd(p.VECTOR2I(a,c));t.SetLayer(b.GetLayerID(layer));t.SetWidth(width)
        else:
            _,net,x,y,top,bottom,width,hole=s;t=p.PCB_VIA(b);t.SetPosition(p.VECTOR2I(x,y));t.SetViaType(p.VIATYPE_MICROVIA);t.SetLayerPair(b.GetLayerID(top),b.GetLayerID(bottom));t.SetWidth(width);t.SetDrill(hole)
        t.SetNetCode(b.FindNet(net).GetNetCode());t.SetUuid(p.KIID(row['uuid']));b.Add(t)
    p.ZONE_FILLER(b).Fill(b.Zones());b.BuildConnectivity()
    out=BUILD/'restored-obsolete.kicad_pcb';p.SaveBoard(str(out),b)
    for ext in ['.kicad_pro','.kicad_dru']:shutil.copyfile(source.with_suffix(ext),out.with_suffix(ext))
    raw=drc(out,BUILD/'restored-obsolete-drc.json')
    counts=Counter(v['type'] for v in raw['violations'])
    assert len(raw['violations'])>104 and any(k in counts for k in ['track_dangling','via_dangling','isolated_copper'])
    return dict(status='REJECTED_COUNTERFACTUAL',native_opens=b.GetConnectivity().GetUnconnectedCount(False),drc_types=dict(counts),findings=len(raw['violations']))


def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--board',type=Path,default=policy.OUTPUT)
    args=ap.parse_args();board=args.board.resolve();BUILD.mkdir(parents=True,exist_ok=True)
    (BUILD/'fp-lib-table').write_text('(fp_lib_table (lib (name "rgb-badge-coupon")(type "KiCad")(uri "'+str(policy.ROOT/'hardware/coupon/rev-a/footprints/rgb-badge-coupon.pretty')+'")(options "")(descr "Local source")))\n')
    before=policy.sha(board);_,_,result=policy.audit(board)
    report=BUILD/'current-drc.json';drc(board,report);policy.check_drc(report)
    result.update({'SPDX-License-Identifier':'CERN-OHL-S-2.0','status':'PASS_GEOMETRIC_ROUTING_STUDY_ONLY',
        'source_sha256':policy.PARENT_SHA,'board_sha256':before,'plan_sha256':policy.PLAN_SHA,
        'drc_sha256':policy.sha(report),'intrinsic_findings':104,'retirement_probe':restored_probe(board,policy.load_plan())})
    assert policy.sha(board)==before and policy.sha(policy.PARENT)==policy.PARENT_SHA
    (BUILD/'current-audit.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print('USB EN1: 34 native/physical opens; every prior group and exact 104 findings retained; obsolete source copper rejected',flush=True)


if __name__=='__main__':main()
