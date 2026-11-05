#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Replay the exact ADR 0085/0088 VLED or dual-converter child; never reroute."""
import argparse
from collections import Counter
import json
from pathlib import Path
import runpy
import shutil
import uuid
import pcbnew as p
import converter_checkpoint as policy


def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--output',type=Path,required=True);ap.add_argument('--stage',choices=('dual','vled52'),default='dual')
    args=ap.parse_args();out=args.output.resolve()
    assert out==policy.OUTPUT or (policy.ROOT/'hardware/coupon/rev-a/build').resolve() in out.parents, 'Output outside allowed checkpoint/build scope'
    assert out.suffix=='.kicad_pcb' and out!=policy.PARENT.resolve()
    assert args.stage=='dual' or out!=policy.OUTPUT
    plan=policy.load_plan(args.stage);assert policy.sha(policy.PARENT)==policy.PARENT_SHA
    c=policy.native_helpers();board=p.LoadBoard(str(policy.PARENT));parts={f.GetReference():f for f in board.GetFootprints()}
    for ref,row in plan['poses'].items():
        f=parts[ref];assert (f.GetPosition().x,f.GetPosition().y,f.GetOrientation().AsDegrees())==(*row['old_position_iu'],row['old_angle_deg'])
        f.SetPosition(p.VECTOR2I(*row['new_position_iu']));f.SetOrientationDegrees(row['new_angle_deg'])
    removed=Counter(map(tuple,plan['removed_copper']));held=[]
    for t in list(board.GetTracks()):
        key=c['signature'](board,t)
        if removed[key]:removed[key]-=1;board.Remove(t);held.append(t)
    assert not +removed
    layers={board.GetLayerName(l):l for l in board.GetEnabledLayers().CuStack()}
    for row in plan['added_copper']:
        if row[0]=='track':
            _,net,x,y,a,b,layer,width=row
            t=p.PCB_TRACK(board);t.SetStart(p.VECTOR2I(x,y));t.SetEnd(p.VECTOR2I(a,b));t.SetLayer(layers[layer]);t.SetWidth(width)
        else:
            _,net,x,y,top,bottom,width,drill=row
            t=p.PCB_VIA(board);t.SetPosition(p.VECTOR2I(x,y));t.SetViaType(p.VIATYPE_MICROVIA)
            t.SetLayerPair(layers[top],layers[bottom]);t.SetWidth(width);t.SetDrill(drill)
        t.SetNetCode(board.FindNet(net).GetNetCode())
        t.SetUuid(p.KIID(str(uuid.uuid5(uuid.NAMESPACE_URL,'rgb-badge:ADR0085:'+repr(row)))));board.Add(t)
    out.parent.mkdir(parents=True,exist_ok=True)
    for ext in ('.kicad_pro','.kicad_dru'):shutil.copyfile(policy.PARENT.with_suffix(ext),out.with_suffix(ext))
    if out.parent!=policy.PARENT.parent:
        (out.parent/'fp-lib-table').write_text('(fp_lib_table\n (lib (name "rgb-badge-coupon")(type "KiCad")(uri "'+str(policy.ROOT/'hardware/coupon/rev-a/footprints/rgb-badge-coupon.pretty')+'")(options "")(descr "Project-local checkpoint")))\n')
    sorter=runpy.run_path(str(policy.ROOT/'tools/generate-paired-charger-114mm-routing.py'))['sorted_native_tracks']
    fills=[]
    for _ in range(3):
        p.ZONE_FILLER(board).Fill(board.Zones());board.BuildConnectivity()
        assert board.GetConnectivity().GetUnconnectedCount(False)==plan['native_opens']
        p.SaveBoard(str(out),board);out.write_text(sorter(out.read_text(),expected=len(list(board.GetTracks()))))
        fills.append(policy.sha(out))
    assert len(set(fills))==1
    policy.audit_geometry(policy.PARENT,out,plan)
    result={'SPDX-License-Identifier':'CERN-OHL-S-2.0','parent_sha256':policy.PARENT_SHA,'board_sha256':policy.sha(out),
        'plan_sha256':policy.VLED_PLAN_SHA if args.stage=='vled52' else policy.PLAN_SHA,'generator_sha256':policy.sha(Path(__file__)),'policy_sha256':policy.sha(Path(policy.__file__)),
        'stable_fill_sha256':fills,'native_opens':plan['native_opens'],'physical_opens':plan['physical_opens'],'fabrication_release_allowed':False}
    report=(policy.ROOT/'hardware/coupon/rev-a/build/converter-checkpoint-review/current.replay.json') if out==policy.OUTPUT else out.with_suffix('.replay.json')
    report.parent.mkdir(parents=True,exist_ok=True)
    report.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print('Checked converter replay:',result['board_sha256'],str(plan['native_opens'])+' native/physical opens',flush=True)


if __name__=='__main__':main()
