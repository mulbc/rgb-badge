#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Replay the exact additive ADR 0124 gauge-supply ledger."""
import argparse
from pathlib import Path
import runpy
import shutil
import pcbnew as p
import routing_gauge_supply as policy

def add(b,row):
    s=row['signature']
    if s[0]=='track':
        _,net,x,y,a,c,layer,width=s;t=p.PCB_TRACK(b);t.SetStart(p.VECTOR2I(x,y));t.SetEnd(p.VECTOR2I(a,c));t.SetLayer(b.GetLayerID(layer));t.SetWidth(width)
    else:
        _,net,x,y,top,bottom,width,hole=s;t=p.PCB_VIA(b);t.SetPosition(p.VECTOR2I(x,y));t.SetViaType(row['via_type']);t.SetLayerPair(b.GetLayerID(top),b.GetLayerID(bottom));t.SetWidth(width);t.SetDrill(hole)
    t.SetNetCode(b.FindNet(net).GetNetCode());t.SetUuid(p.KIID(row['uuid']));b.Add(t)

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--output',type=Path,required=True);args=ap.parse_args();out=args.output.resolve()
    assert out==policy.OUTPUT or (policy.ROOT/'hardware/coupon/rev-a/build').resolve() in out.parents
    assert out.suffix=='.kicad_pcb' and out!=policy.PARENT
    plan=policy.load_plan();b=p.LoadBoard(str(policy.PARENT));old=p.LoadBoard(str(policy.PARENT))
    for row in plan['added_copper']:add(b,row)
    out.parent.mkdir(parents=True,exist_ok=True);sort=runpy.run_path(str(policy.ROOT/'tools/generate-paired-charger-114mm-routing.py'))['sorted_native_tracks'];hashes=[]
    for _ in range(3):
        p.ZONE_FILLER(b).Fill(b.Zones());b.BuildConnectivity();policy.connectivity(old,b);p.SaveBoard(str(out),b);out.write_text(sort(out.read_text(),expected=len(list(b.GetTracks()))));hashes.append(policy.sha(out))
    assert len(set(hashes))==1,'Refill bytes unstable'
    for ext in ['.kicad_pro','.kicad_dru']:shutil.copyfile(policy.PARENT.with_suffix(ext),out.with_suffix(ext))
    result=policy.audit(out);print(dict(sha256=hashes[-1],stable_refills=3,**result),flush=True)
if __name__=='__main__':main()
