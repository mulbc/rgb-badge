#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Replay one exact ADR 0090 nine-part placement in ignored build output."""
import argparse
from collections import Counter
import hashlib
import json
import math
from pathlib import Path
import shutil
import uuid
import pcbnew as p

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'hardware/coupon/rev-a/staging/led-converter-routing-trial-114mm.kicad_pcb'
SHA='5e07fb866cc059de670e34102045d9dfd88c88f101355fcdbb27253c0ae26e43'


def signature(b,t):
    assert not isinstance(t,p.PCB_VIA)
    return ['track',t.GetNetname(),t.GetStart().x,t.GetStart().y,t.GetEnd().x,t.GetEnd().y,b.GetLayerName(t.GetLayer()),t.GetWidth()]


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--plan',type=Path,required=True);ap.add_argument('--output',type=Path,required=True)
    args=ap.parse_args();out=args.output.resolve()
    assert (ROOT/'hardware/coupon/rev-a/build').resolve() in out.parents and out.suffix=='.kicad_pcb'
    assert hashlib.sha256(SOURCE.read_bytes()).hexdigest()==SHA
    plan=json.loads(args.plan.read_text());assert plan['source_sha256']==SHA
    b=p.LoadBoard(str(SOURCE));parts={f.GetReference():f for f in b.GetFootprints()}
    assert set(plan['poses'])=={'U36','L1','C40','C41','C42','C43','R81','R82','R83'}
    for ref,row in plan['poses'].items():
        f=parts[ref]
        assert [f.GetPosition().x,f.GetPosition().y]==row['old_position_iu']
        assert f.GetOrientation().AsDegrees()==row['old_angle_deg']
        assert f.GetField('MPN').GetText()==row['mpn']
        f.SetPosition(p.VECTOR2I(*row['position_iu']));f.SetOrientationDegrees(row['angle_deg'])
    wanted=Counter(map(tuple,plan['removed_copper']));held=[]
    for t in list(b.GetTracks()):
        if isinstance(t,p.PCB_VIA):continue
        key=tuple(signature(b,t))
        if wanted[key]:
            wanted[key]-=1;b.Remove(t);held.append(t)
    assert not +wanted and len(held)==6
    for row in plan['added_switching_copper']:
        _,net,x,y,a,z,layer,width=row
        t=p.PCB_TRACK(b);t.SetStart(p.VECTOR2I(x,y));t.SetEnd(p.VECTOR2I(a,z))
        t.SetLayer(b.GetLayerID(layer));t.SetWidth(width);t.SetNetCode(b.FindNet(net).GetNetCode())
        t.SetUuid(p.KIID(str(uuid.uuid5(uuid.NAMESPACE_URL,'rgb-badge:ADR0090:'+repr(row)))));b.Add(t)
    out.parent.mkdir(parents=True,exist_ok=True)
    for ext in ('.kicad_pro','.kicad_dru'):shutil.copyfile(SOURCE.with_suffix(ext),out.with_suffix(ext))
    (out.parent/'fp-lib-table').write_text('(fp_lib_table (lib (name "rgb-badge-coupon")(type "KiCad")(uri "'+str(ROOT/'hardware/coupon/rev-a/footprints/rgb-badge-coupon.pretty')+'")(options "")(descr "Local source")))\n')
    p.ZONE_FILLER(b).Fill(b.Zones());b.BuildConnectivity();p.SaveBoard(str(out),b)
    assert hashlib.sha256(SOURCE.read_bytes()).hexdigest()==SHA
    print('Unselected nine-part stage candidate:',b.GetConnectivity().GetUnconnectedCount(False),'opens',flush=True)


if __name__=='__main__':main()
