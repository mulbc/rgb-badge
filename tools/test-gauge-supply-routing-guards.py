#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Native source/geometry faults and independent physical disconnection gates."""
import argparse
import json
from pathlib import Path
import shutil
import subprocess
import sys
import pcbnew as p
import routing_gauge_supply as policy
BUILD=policy.ROOT/'hardware/coupon/rev-a/build/gauge-supply-routing/faults'
CASES=['wrong-part','wrong-net','move-part','retire-source','narrow-track','extra-track','wrong-via-type','wrong-via-drill','omit-contacts','disconnect-longest-track','remove-whole-join']
def trial(source,name):
    plan=policy.load_plan();b=p.LoadBoard(str(source));held=[];added={r['uuid'] for r in plan['added_copper']};tracks=[t for t in b.GetTracks() if t.m_Uuid.AsString() in added and not isinstance(t,p.PCB_VIA)];central=next(t for t in b.GetTracks() if t.m_Uuid.AsString() in added and isinstance(t,p.PCB_VIA) and {b.GetLayerName(t.TopLayer()),b.GetLayerName(t.BottomLayer())}=={'In2.Cu','In3.Cu'});part=b.FindFootprintByReference('C64')
    if name=='wrong-part':part.GetField('MPN').SetText('GRM155R61A104KA01D')
    elif name=='wrong-net':next(q for q in part.Pads() if q.GetNumber()=='1').SetNetCode(b.FindNet('+3V3_USB').GetNetCode())
    elif name=='move-part':part.SetPosition(part.GetPosition()+p.VECTOR2I(250000,0))
    elif name=='retire-source':
        t=next(t for t in b.GetTracks() if t.m_Uuid.AsString() not in added);b.Remove(t);held.append(t)
    elif name=='narrow-track':tracks[0].SetWidth(120000)
    elif name=='extra-track':
        t=p.PCB_TRACK(b);t.SetStart(p.VECTOR2I(1000000,1000000));t.SetEnd(p.VECTOR2I(2000000,1000000));t.SetLayer(p.B_Cu);t.SetWidth(200000);t.SetNetCode(b.FindNet('+BAT_GAUGE_SW').GetNetCode());b.Add(t)
    elif name=='wrong-via-type':central.SetViaType(p.VIATYPE_MICROVIA)
    elif name=='wrong-via-drill':central.SetDrill(100000)
    elif name=='omit-contacts':plan['original_contacts']=[]
    elif name in ['disconnect-longest-track','remove-whole-join']:
        remove=[max(tracks,key=lambda t:t.GetLength())] if name=='disconnect-longest-track' else [t for t in b.GetTracks() if t.m_Uuid.AsString() in added]
        for t in remove:b.Remove(t);held.append(t)
        p.ZONE_FILLER(b).Fill(b.Zones());b.BuildConnectivity();old=p.LoadBoard(str(policy.PARENT))
        try:policy.connectivity(old,b)
        except AssertionError as e:print('REJECTED actual native disconnection',name,str(e),flush=True);return
        raise RuntimeError('Native disconnection accepted: '+name)
    out=BUILD/(name+'.kicad_pcb');p.SaveBoard(str(out),b)
    for ext in ['.kicad_pro','.kicad_dru']:shutil.copyfile(source.with_suffix(ext),out.with_suffix(ext))
    try:policy.audit(out,plan)
    except AssertionError as e:print('REJECTED',name,str(e),flush=True);return
    raise RuntimeError('Fault accepted: '+name)
def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--board',type=Path,required=True);ap.add_argument('--fault',choices=CASES);args=ap.parse_args();BUILD.mkdir(parents=True,exist_ok=True)
    if args.fault:trial(args.board,args.fault);return
    policy.audit(args.board);rows=[]
    for name in CASES:
        r=subprocess.run([sys.executable,__file__,'--board',str(args.board),'--fault',name],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True);(BUILD/(name+'.log')).write_text(r.stdout);assert r.returncode==0,r.stdout;rows.append(dict(fault=name,exit_code=r.returncode));print('Rejected:',name,flush=True)
    (BUILD/'results.json').write_text(json.dumps(rows,indent=2)+'\n')
if __name__=='__main__':main()
