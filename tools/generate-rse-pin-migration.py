#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Replay ADR 0117's exact corrected-pin PCB successor, without routing search."""
import argparse
import json
from pathlib import Path
import runpy
import shutil
import pcbnew as p
import rse_pin_migration as mapping

ROOT=Path(__file__).resolve().parents[1]
POLICY=runpy.run_path(str(ROOT/'tools/audit-rse-pin-migration.py'))
PLAN=ROOT/'mechanical/review/rse-pin-migration-plan.json'
PLAN_SHA='ca2a86c6678f237fdfbfc29c7c9bbf9426083f1d25fde777268564ecb5777157'
OUTPUT=ROOT/'hardware/coupon/rev-a/staging/led-rse-corrected-routing-trial-114mm.kicad_pcb'


def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--output',type=Path,required=True)
    args=ap.parse_args();out=args.output.resolve();build=(ROOT/'hardware/coupon/rev-a/build').resolve()
    assert out==OUTPUT or build in out.parents
    assert out.suffix=='.kicad_pcb' and out!=POLICY['SOURCE']
    assert POLICY['sha'](PLAN)==PLAN_SHA
    plan=json.loads(PLAN.read_text())
    assert POLICY['sha'](POLICY['SOURCE'])==plan['source_sha256']==POLICY['SOURCE_SHA']
    b=p.LoadBoard(str(POLICY['SOURCE']));held=[]
    removed={q['uuid']:q['signature'] for q in plan['retired_copper']}
    assert set(removed)==POLICY['RETIRED']
    signature=runpy.run_path(str(ROOT/'tools/check-routing-progress-trial.py'))['signature']
    for t in list(b.GetTracks()):
        uid=t.m_Uuid.AsString()
        if uid in removed:
            assert list(signature(b,t))==removed[uid]
            b.Remove(t);held.append(t)
    assert len(held)==8
    for ref,pins in mapping.CORRECTED.items():
        f=b.FindFootprintByReference(ref)
        for q in f.Pads():
            assert q.GetNetname()==mapping.LEGACY[ref][q.GetNumber()]
            net=pins[q.GetNumber()];q.SetNetCode(b.FindNet(net).GetNetCode() if net else 0)
    for entry in plan['added_copper']:
        row=entry['signature']
        if row[0]=='track':
            _,net,x,y,a,c,layer,width=row
            t=p.PCB_TRACK(b);t.SetStart(p.VECTOR2I(x,y));t.SetEnd(p.VECTOR2I(a,c));t.SetLayer(b.GetLayerID(layer));t.SetWidth(width)
        else:
            _,net,x,y,top,bottom,width,drill=row
            t=p.PCB_VIA(b);t.SetPosition(p.VECTOR2I(x,y));t.SetViaType(p.VIATYPE_MICROVIA)
            t.SetLayerPair(b.GetLayerID(top),b.GetLayerID(bottom));t.SetWidth(width);t.SetDrill(drill)
        t.SetNetCode(b.FindNet(net).GetNetCode());t.SetUuid(p.KIID(entry['uuid']));b.Add(t)
    out.parent.mkdir(parents=True,exist_ok=True)
    for ext in ('.kicad_pro','.kicad_dru'):shutil.copyfile(POLICY['SOURCE'].with_suffix(ext),out.with_suffix(ext))
    sorter=runpy.run_path(str(ROOT/'tools/generate-paired-charger-114mm-routing.py'))['sorted_native_tracks']
    hashes=[]
    for _ in range(3):
        p.ZONE_FILLER(b).Fill(b.Zones());b.BuildConnectivity()
        assert b.GetConnectivity().GetUnconnectedCount(False)==35
        p.SaveBoard(str(out),b);out.write_text(sorter(out.read_text(),expected=len(list(b.GetTracks()))))
        hashes.append(POLICY['sha'](out))
    assert len(set(hashes))==1, 'Native fill bytes unstable'
    for ext in ('.kicad_pro','.kicad_dru'):
        shutil.copyfile(POLICY['SOURCE'].with_suffix(ext),out.with_suffix(ext))
    old,new,result=POLICY['audit'](out)
    assert not result['semantic_group_losses'] and result['native_opens']==result['physical_opens']==35
    for key in ('added_copper','retired_copper'):
        assert json.loads(json.dumps(result[key]))==plan[key], 'Exact copper ledger differs: '+key
    print('Exact RSE replay:',hashes[-1],'; 35 native/physical opens; all 223 functional groups retained',flush=True)


if __name__=='__main__':main()
