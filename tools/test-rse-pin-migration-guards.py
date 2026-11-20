#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Native adversarial checks for ADR 0117's package and connection boundaries."""
import argparse
import json
from pathlib import Path
import runpy
import shutil
import subprocess
import sys
import pcbnew as p

ROOT=Path(__file__).resolve().parents[1]
FOLDER=ROOT/'hardware/coupon/rev-a/build/rse-pin-correction/faults'
CASES=['old-pin-map','swap-q-outputs','preset-low','move-u50','retire-accepted-copper',
       'touch-inverse-output','narrow-new-track','new-centre-microvia','disconnect-clock']


def fault(source,name):
    policy=runpy.run_path(str(ROOT/'tools/audit-rse-pin-migration.py'))
    b=p.LoadBoard(str(source));held=[];f=b.FindFootprintByReference('U50')
    pads={q.GetNumber():q for q in f.Pads()}
    if name=='old-pin-map':
        import rse_pin_migration as m
        for n,q in pads.items():q.SetNetCode(b.FindNet(m.LEGACY['U50'][n]).GetNetCode() if m.LEGACY['U50'][n] else 0)
    elif name=='swap-q-outputs':
        pads['5'].SetNetCode(pads['3'].GetNetCode());pads['3'].SetNetCode(0)
    elif name=='preset-low':pads['1'].SetNetCode(b.FindNet('GND').GetNetCode())
    elif name=='move-u50':f.SetPosition(f.GetPosition()+p.VECTOR2I(250000,0))
    elif name=='retire-accepted-copper':
        old=p.LoadBoard(str(policy['SOURCE']));original={t.m_Uuid.AsString() for t in old.GetTracks()}
        t=next(t for t in b.GetTracks() if t.m_Uuid.AsString() in original);b.Remove(t);held.append(t)
    elif name=='touch-inverse-output':
        q=pads['5'];t=p.PCB_TRACK(b);t.SetStart(q.GetPosition());t.SetEnd(q.GetPosition()+p.VECTOR2I(-200000,0));t.SetLayer(p.B_Cu);t.SetWidth(200000);t.SetNetCode(b.FindNet('ARM_LATCH').GetNetCode());b.Add(t)
    elif name=='narrow-new-track':
        original={row['uuid'] for row in json.loads((ROOT/'mechanical/review/rse-pin-migration-plan.json').read_text())['added_copper']}
        t=next(t for t in b.GetTracks() if not isinstance(t,p.PCB_VIA) and t.m_Uuid.AsString() in original);t.SetWidth(120000)
    elif name=='new-centre-microvia':
        t=p.PCB_VIA(b);t.SetPosition(p.VECTOR2I(10000000,3000000));t.SetViaType(p.VIATYPE_MICROVIA);t.SetLayerPair(p.In2_Cu,p.In3_Cu);t.SetWidth(300000);t.SetDrill(100000);t.SetNetCode(b.FindNet('DISPLAY_ARM_CLK').GetNetCode());b.Add(t)
    elif name=='disconnect-clock':
        added={row['uuid'] for row in json.loads((ROOT/'mechanical/review/rse-pin-migration-plan.json').read_text())['added_copper']}
        tracks=[t for t in b.GetTracks() if not isinstance(t,p.PCB_VIA) and t.GetNetname()=='DISPLAY_ARM_CLK'
                and t.GetLayer()==b.GetLayerID('In3.Cu') and t.m_Uuid.AsString() in added]
        assert len(tracks)==1
        b.Remove(tracks[0]);held.extend(tracks)
        p.ZONE_FILLER(b).Fill(b.Zones());b.BuildConnectivity()
    out=FOLDER/(name+'.kicad_pcb');p.SaveBoard(str(out),b)
    for ext in ('.kicad_pro','.kicad_dru'):shutil.copyfile(source.with_suffix(ext),out.with_suffix(ext))
    try:
        _,_,result=policy['audit'](out)
        assert not result['semantic_group_losses'], 'Prior functional group lost'
        assert result['native_opens']==result['physical_opens']==35
    except AssertionError as error:
        print('REJECTED',name,str(error),flush=True);return
    raise RuntimeError('Fault was accepted: '+name)


def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--board',type=Path,required=True);ap.add_argument('--fault',choices=CASES)
    args=ap.parse_args();FOLDER.mkdir(parents=True,exist_ok=True)
    if args.fault:fault(args.board,args.fault);return
    policy=runpy.run_path(str(ROOT/'tools/audit-rse-pin-migration.py'))
    _,_,baseline=policy['audit'](args.board)
    assert not baseline['semantic_group_losses'] and baseline['native_opens']==baseline['physical_opens']==35
    rows=[]
    for name in CASES:
        r=subprocess.run([sys.executable,__file__,'--board',str(args.board),'--fault',name],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
        (FOLDER/(name+'.log')).write_text(r.stdout)
        assert r.returncode==0,r.stdout
        rows.append(dict(fault=name,exit_code=r.returncode));print('Rejected:',name,flush=True)
    (FOLDER/'results.json').write_text(json.dumps(rows,indent=2)+'\n')


if __name__=='__main__':main()
