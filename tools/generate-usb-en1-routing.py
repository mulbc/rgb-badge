#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Replay ADR 0121's two poses and exact ordinary-width USB-control branches."""
import argparse
from pathlib import Path
import runpy
import shutil
import pcbnew as p
import routing_usb_en1 as policy


def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--output',type=Path,required=True)
    args=ap.parse_args();out=args.output.resolve()
    assert out==policy.OUTPUT or (policy.ROOT/'hardware/coupon/rev-a/build').resolve() in out.parents
    assert out.suffix=='.kicad_pcb' and out!=policy.PARENT
    plan=policy.load_plan();b=p.LoadBoard(str(policy.PARENT));held=[]
    signature=policy.helper()['signature']
    retired={r['uuid']:r['signature'] for r in plan['retired_copper']}
    for item in list(b.GetTracks()):
        uid=item.m_Uuid.AsString()
        if uid in retired:
            assert list(signature(b,item))==retired[uid]
            b.Remove(item);held.append(item)
    assert len(held)==3
    for ref,row in plan['poses'].items():
        f=b.FindFootprintByReference(ref)
        assert list(f.GetPosition())==row['old_position_iu'] and f.GetOrientation().AsDegrees()%360==row['old_angle_deg']%360
        f.SetPosition(p.VECTOR2I(*row['position_iu']));f.SetOrientationDegrees(row['requested_angle_deg'])
    for entry in plan['added_copper']:
        _,net,x,y,a,c,layer,width=entry['signature']
        t=p.PCB_TRACK(b);t.SetStart(p.VECTOR2I(x,y));t.SetEnd(p.VECTOR2I(a,c));t.SetLayer(b.GetLayerID(layer));t.SetWidth(width)
        t.SetNetCode(b.FindNet(net).GetNetCode());t.SetUuid(p.KIID(entry['uuid']));b.Add(t)
    out.parent.mkdir(parents=True,exist_ok=True)
    for ext in ['.kicad_pro','.kicad_dru']:shutil.copyfile(policy.PARENT.with_suffix(ext),out.with_suffix(ext))
    old=p.LoadBoard(str(policy.PARENT));old.BuildConnectivity()
    sort=runpy.run_path(str(policy.ROOT/'tools/generate-paired-charger-114mm-routing.py'))['sorted_native_tracks']
    hashes=[]
    for _ in range(3):
        p.ZONE_FILLER(b).Fill(b.Zones());b.BuildConnectivity();policy.connectivity(old,b)
        p.SaveBoard(str(out),b);out.write_text(sort(out.read_text(),expected=len(list(b.GetTracks()))));hashes.append(policy.sha(out))
    assert len(set(hashes))==1, 'Refill bytes unstable'
    for ext in ['.kicad_pro','.kicad_dru']:shutil.copyfile(policy.PARENT.with_suffix(ext),out.with_suffix(ext))
    policy.audit(out)
    print('USB EN1 exact replay:',hashes[-1],'; 34 native/physical opens; all 223 prior groups retained',flush=True)


if __name__=='__main__':main()
