#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Native faults for ADR 0121; disconnections exercise connectivity directly."""
import argparse
import copy
import json
from pathlib import Path
import shutil
import subprocess
import sys
import pcbnew as p
import routing_usb_en1 as policy

BUILD=policy.ROOT/'hardware/coupon/rev-a/build/usb-en1-locality/faults'
CASES=['wrong-pullup','wrong-pullup-net','test-pad-size','move-test-pad','retire-retained-copper',
       'restore-obsolete-leaf','narrow-track','new-via','omit-source-contacts',
       'false-branch-endpoint','disconnect-supply','disconnect-output']


def trial(source,name):
    plan=policy.load_plan();b=p.LoadBoard(str(source));held=[]
    r=b.FindFootprintByReference('R70');tp=b.FindFootprintByReference('TP31')
    added={row['uuid']:row for row in plan['added_copper']}
    if name=='wrong-pullup':r.GetField('MPN').SetText('ERJ2RKF1001X')
    elif name=='wrong-pullup-net':next(q for q in r.Pads() if q.GetNumber()=='1').SetNetCode(b.FindNet('+3V3_APP').GetNetCode())
    elif name=='test-pad-size':next(q for q in tp.Pads() if q.GetNumber()=='1').SetSize(p.VECTOR2I(800000,800000))
    elif name=='move-test-pad':tp.SetPosition(tp.GetPosition()+p.VECTOR2I(250000,0))
    elif name=='retire-retained-copper':
        t=next(t for t in b.GetTracks() if t.m_Uuid.AsString() not in added);b.Remove(t);held.append(t)
    elif name=='restore-obsolete-leaf':
        row=next(r for r in plan['retired_copper'] if r['signature'][0]=='track');_,net,x,y,a,c,layer,width=row['signature']
        t=p.PCB_TRACK(b);t.SetStart(p.VECTOR2I(x,y));t.SetEnd(p.VECTOR2I(a,c));t.SetLayer(b.GetLayerID(layer));t.SetWidth(width);t.SetNetCode(b.FindNet(net).GetNetCode());t.SetUuid(p.KIID(row['uuid']));b.Add(t)
    elif name=='narrow-track':next(t for t in b.GetTracks() if t.m_Uuid.AsString() in added).SetWidth(120000)
    elif name=='new-via':
        t=p.PCB_VIA(b);t.SetPosition(p.VECTOR2I(11900000,7750000));t.SetViaType(p.VIATYPE_MICROVIA);t.SetLayerPair(p.In4_Cu,p.B_Cu);t.SetWidth(300000);t.SetDrill(100000);t.SetNetCode(b.FindNet('USB_EN1_RAW_N').GetNetCode());b.Add(t)
    elif name=='omit-source-contacts':plan['original_contacts']={}
    elif name=='false-branch-endpoint':plan['branches'][0]['points_iu'][-1][0]+=250000
    elif name in ['disconnect-supply','disconnect-output']:
        net='+3V3_USB' if name=='disconnect-supply' else 'USB_EN1_RAW_N'
        target=next(row['uuid'] for row in plan['added_copper'] if row['signature'][1]==net and abs(row['signature'][2]-row['signature'][4])>7000000)
        t=next(t for t in b.GetTracks() if t.m_Uuid.AsString()==target);b.Remove(t);held.append(t)
        p.ZONE_FILLER(b).Fill(b.Zones());b.BuildConnectivity()
        old=p.LoadBoard(str(policy.PARENT));old.BuildConnectivity()
        try:policy.connectivity(old,b)
        except AssertionError as error:
            print('REJECTED actual native',name,str(error),flush=True);return
        raise RuntimeError('Physical disconnection accepted: '+name)
    out=BUILD/(name+'.kicad_pcb');p.SaveBoard(str(out),b)
    for ext in ['.kicad_pro','.kicad_dru']:shutil.copyfile(source.with_suffix(ext),out.with_suffix(ext))
    try:policy.audit(out,plan)
    except AssertionError as error:
        print('REJECTED',name,str(error),flush=True);return
    raise RuntimeError('Fault accepted: '+name)


def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--board',type=Path,required=True);ap.add_argument('--fault',choices=CASES)
    args=ap.parse_args();BUILD.mkdir(parents=True,exist_ok=True)
    if args.fault:trial(args.board,args.fault);return
    policy.audit(args.board)
    rows=[]
    for name in CASES:
        r=subprocess.run([sys.executable,__file__,'--board',str(args.board),'--fault',name],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
        (BUILD/(name+'.log')).write_text(r.stdout)
        assert r.returncode==0,r.stdout
        rows.append(dict(fault=name,exit_code=r.returncode));print('Rejected:',name,flush=True)
    (BUILD/'results.json').write_text(json.dumps(rows,indent=2)+'\n')


if __name__=='__main__':main()
