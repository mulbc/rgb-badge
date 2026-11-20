#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Deterministic exact remaining-routing replay; no search and no fabrication release."""
import argparse
from collections import Counter
from pathlib import Path
import runpy
import shutil
import uuid
import pcbnew as p
import routing_remaining as policy


def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--output',type=Path,required=True)
    args=ap.parse_args();out=args.output.resolve()
    assert out==policy.OUTPUT or (policy.ROOT/'hardware/coupon/rev-a/build').resolve() in out.parents
    assert out.suffix=='.kicad_pcb' and out!=policy.PARENT.resolve()
    plan=policy.load_plan();board=p.LoadBoard(str(policy.PARENT))
    parts={f.GetReference():f for f in board.GetFootprints()}
    for ref,row in plan['poses'].items():
        f=parts[ref]
        assert (f.GetPosition().x,f.GetPosition().y,f.GetOrientation().AsDegrees())==(*row['old_position_iu'],row['old_angle_deg'])
        f.SetPosition(p.VECTOR2I(*row['position_iu']));f.SetOrientationDegrees(row['angle_deg'])
    removed=Counter(map(tuple,plan['removed_copper']));held=[]
    for item in list(board.GetTracks()):
        key=policy.signature(board,item)
        if removed[key]:removed[key]-=1;board.Remove(item);held.append(item)
    assert not +removed
    for row in plan['added_copper']:
        if row[0]=='track':
            _,net,x,y,a,b,layer,width=row
            t=p.PCB_TRACK(board);t.SetStart(p.VECTOR2I(x,y));t.SetEnd(p.VECTOR2I(a,b));t.SetLayer(board.GetLayerID(layer));t.SetWidth(width)
        else:
            _,net,x,y,top,bottom,width,drill,kind=row
            t=p.PCB_VIA(board);t.SetPosition(p.VECTOR2I(x,y));t.SetViaType(kind)
            t.SetLayerPair(board.GetLayerID(top),board.GetLayerID(bottom));t.SetWidth(width);t.SetDrill(drill)
        t.SetNetCode(board.FindNet(net).GetNetCode())
        t.SetUuid(p.KIID(str(uuid.uuid5(uuid.NAMESPACE_URL,'rgb-badge:ADR0091:remaining:'+repr(row)))));board.Add(t)
    out.parent.mkdir(parents=True,exist_ok=True)
    for ext in ('.kicad_pro','.kicad_dru'):shutil.copyfile(policy.PARENT.with_suffix(ext),out.with_suffix(ext))
    if out.parent!=policy.PARENT.parent:
        (out.parent/'fp-lib-table').write_text('(fp_lib_table (lib (name "rgb-badge-coupon")(type "KiCad")(uri "'+str(policy.ROOT/'hardware/coupon/rev-a/footprints/rgb-badge-coupon.pretty')+'")(options "")(descr "Local source")))\n')
    sorter=runpy.run_path(str(policy.ROOT/'tools/generate-paired-charger-114mm-routing.py'))['sorted_native_tracks']
    fills=[]
    for _ in range(3):
        p.ZONE_FILLER(board).Fill(board.Zones());board.BuildConnectivity()
        assert board.GetConnectivity().GetUnconnectedCount(False)==plan['native_opens']
        p.SaveBoard(str(out),board);out.write_text(sorter(out.read_text(),expected=len(list(board.GetTracks()))));fills.append(policy.sha(out))
    assert len(set(fills))==1,'Fill bytes unstable'
    for ext in ('.kicad_pro','.kicad_dru'):shutil.copyfile(policy.PARENT.with_suffix(ext),out.with_suffix(ext))
    policy.audit(out,plan)
    print('Exact remaining-routing replay:',fills[-1],flush=True)


if __name__=='__main__':main()
