#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Replay the exact R21 supply and shortened gate-leaf relocation."""
import argparse
from pathlib import Path
import runpy
import shutil
import pcbnew as p
import routing_r21 as policy

def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--output',type=Path,required=True);args=ap.parse_args();out=args.output.resolve();assert (policy.ROOT/'hardware/coupon/rev-a/build').resolve() in out.parents and out.suffix=='.kicad_pcb' and out!=policy.PARENT
 plan=policy.load_plan();b=p.LoadBoard(str(policy.PARENT));old=p.LoadBoard(str(policy.PARENT));retired={r['uuid'] for r in plan['retired_copper']};held=[]
 for t in list(b.GetTracks()):
  if t.m_Uuid.AsString() in retired:b.Remove(t);held.append(t)
 assert len(held)==2
 for ref,pose in plan['poses'].items():
  fp=b.FindFootprintByReference(ref);fp.SetOrientationDegrees(pose['orientation_degrees']);fp.SetPosition(p.VECTOR2I(*pose['position_iu']))
 add=runpy.run_path(str(policy.ROOT/'tools/generate-gauge-supply-routing.py'))['add']
 for row in plan['added_copper']:add(b,row)
 out.parent.mkdir(parents=True,exist_ok=True);sort=runpy.run_path(str(policy.ROOT/'tools/generate-paired-charger-114mm-routing.py'))['sorted_native_tracks'];hashes=[]
 for _ in range(3):
  p.ZONE_FILLER(b).Fill(b.Zones());b.BuildConnectivity();policy.connectivity(old,b);p.SaveBoard(str(out),b);out.write_text(sort(out.read_text(),expected=len(list(b.GetTracks()))));hashes.append(policy.sha(out))
 assert len(set(hashes))==1 and hashes[0]==policy.BOARD_SHA,('Replay/refill bytes differ',hashes)
 for ext in ['.kicad_pro','.kicad_dru']:shutil.copyfile(policy.PARENT.with_suffix(ext),out.with_suffix(ext))
 result=policy.audit(out);print(dict(sha256=hashes[-1],stable_refills=3,**result),flush=True)
if __name__=='__main__':main()
