#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Restore enumerated orphan vias for an independent native DRC witness."""
import argparse
import importlib.util
import json
from pathlib import Path
import shutil
import pcbnew as p

ROOT=Path(__file__).resolve().parents[1]


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',required=True,type=Path)
    args=parser.parse_args();output=args.output.resolve()
    assert ROOT/'hardware/coupon/rev-a/build' in output.parents
    spec=importlib.util.spec_from_file_location('check',ROOT/'tools/check-routing-progress-trial.py')
    c=importlib.util.module_from_spec(spec);spec.loader.exec_module(c)
    plan=json.loads(c.PLAN.read_text());board=p.LoadBoard(str(c.OUTPUT))
    groups={}
    for part in board.GetFootprints():
        for pad in part.Pads():
            if pad.GetNetname():groups.setdefault(c.physical_cluster(board,pad),pad)
    count=board.GetConnectivity().GetUnconnectedCount(False)
    for kind,net,x,y,top,bottom,diameter,drill in plan.get('retired_orphan_microvias',[]):
        assert kind=='via'
        via=p.PCB_VIA(board);via.SetPosition(p.VECTOR2I(x,y));via.SetViaType(p.VIATYPE_MICROVIA)
        via.SetLayerPair(board.GetLayerID(top),board.GetLayerID(bottom))
        via.SetWidth(diameter);via.SetDrill(drill);via.SetNetCode(board.FindNet(net).GetNetCode());board.Add(via)
    p.ZONE_FILLER(board).Fill(board.Zones());board.BuildConnectivity()
    assert board.GetConnectivity().GetUnconnectedCount(False)==count
    assert all(group==c.physical_cluster(board,pad) for group,pad in groups.items())
    output.parent.mkdir(parents=True,exist_ok=True);p.SaveBoard(str(output),board)
    shutil.copyfile(c.OUTPUT.with_suffix('.kicad_pro'),output.with_suffix('.kicad_pro'))
    if c.OUTPUT.with_suffix('.kicad_dru').exists():
        shutil.copyfile(c.OUTPUT.with_suffix('.kicad_dru'),output.with_suffix('.kicad_dru'))
    else:
        output.with_suffix('.kicad_dru').unlink(missing_ok=True)
    library=ROOT/'hardware/coupon/rev-a/footprints/rgb-badge-coupon.pretty'
    (output.parent/'fp-lib-table').write_text('(fp_lib_table (lib (name "rgb-badge-coupon") (type "KiCad") (uri "'+str(library)+'") (options "") (descr "")))\n')
    print('Restored %d candidate orphan vias; all selected groups and %d edges unchanged.'%(len(plan.get('retired_orphan_microvias',[])),count))


if __name__=='__main__':main()
