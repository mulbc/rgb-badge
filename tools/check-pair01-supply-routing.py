#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Native complete-ledger gate and original-orphan reconstruction proof."""
import argparse
import json
from pathlib import Path
import runpy
import shutil
import subprocess
import pcbnew as p
import routing_pair01_supply as policy
BUILD=policy.ROOT/'hardware/coupon/rev-a/build/pair01-supply-routing'
CLI='/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli'
def drc(board,out):
 r=subprocess.run([CLI,'pcb','drc','--format','json','--output',str(out),str(board)],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True);out.with_suffix('.log').write_text(r.stdout);assert r.returncode==0,r.stdout

def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--board',type=Path,default=policy.OUTPUT);args=ap.parse_args();board=args.board.resolve();BUILD.mkdir(parents=True,exist_ok=True)
 (BUILD/'fp-lib-table').write_text('(fp_lib_table (lib (name "rgb-badge-coupon")(type "KiCad")(uri "'+str(policy.ROOT/'hardware/coupon/rev-a/footprints/rgb-badge-coupon.pretty')+'")(options "")(descr "Local source")))\n')
 before=policy.sha(board);result=policy.audit(board);report=BUILD/'current-drc.json';drc(board,report);policy.check_drc(report,board)
 plan=policy.load_plan();b=p.LoadBoard(str(board));old=p.LoadBoard(str(policy.PARENT));added={r['uuid'] for r in plan['added_copper']};retired={r['uuid'] for r in plan['retired_copper']};held=[]
 for t in list(b.GetTracks()):
  if t.m_Uuid.AsString() in added:b.Remove(t);held.append(t)
 assert len(held)==len(policy.load_plan()['added_copper'])
 add=runpy.run_path(str(policy.ROOT/'tools/generate-gauge-supply-routing.py'))['add']
 for row in plan['retired_copper']:add(b,row)
 for ref in plan['poses']:
  a=old.FindFootprintByReference(ref);z=b.FindFootprintByReference(ref);replacement=p.FOOTPRINT(a);fields={v.GetName():v for v in a.GetFields()}
  for v in replacement.GetFields():v.SetUuid(fields[v.GetName()].m_Uuid)
  b.Remove(z);held.append(z);b.Add(replacement)
 out=BUILD/'original-restored.kicad_pcb';sort=runpy.run_path(str(policy.ROOT/'tools/generate-paired-charger-114mm-routing.py'))['sorted_native_tracks'];hashes=[]
 def groups(board):return {frozenset(v.m_Uuid.AsString() for v in board.GetConnectivity().GetConnectedItems(q) if isinstance(v,p.PAD)) for fp in board.GetFootprints() for q in fp.Pads() if q.GetNetname()}
 h=policy.helper();ot={t.m_Uuid.AsString():t for t in old.GetTracks()};nt={t.m_Uuid.AsString():t for t in b.GetTracks()};assert ot.keys()==nt.keys()
 for uid,t in ot.items():
  assert h['signature'](old,t)==h['signature'](b,nt[uid])
  if isinstance(t,p.PCB_VIA):assert t.GetViaType()==nt[uid].GetViaType()
 original_inverse_board=b
 p.SaveBoard(str(out),b);out.write_text(sort(out.read_text(),expected=len(list(b.GetTracks()))))
 for ext in ['.kicad_pro','.kicad_dru']:shutil.copyfile(policy.PARENT.with_suffix(ext),out.with_suffix(ext))
 b=p.LoadBoard(str(out))
 for _ in range(3):
  p.ZONE_FILLER(b).Fill(b.Zones());b.BuildConnectivity();assert b.GetConnectivity().GetUnconnectedCount(False)==24 and groups(b)==groups(old) and len(groups(b))==212;p.SaveBoard(str(out),b);out.write_text(sort(out.read_text(),expected=len(list(b.GetTracks()))));hashes.append(policy.sha(out))
 assert hashes==[policy.PARENT_SHA]*3,'Inverse is not byte-identical to the original source'
 for ext in ['.kicad_pro','.kicad_dru']:shutil.copyfile(policy.PARENT.with_suffix(ext),out.with_suffix(ext))
 other={z.m_Uuid.AsString():z for z in b.Zones()};xor=[]
 for z in old.Zones():
  layer=z.GetLayer();delta=p.SHAPE_POLY_SET(z.GetFilledPolysList(layer));delta.BooleanXor(other[z.m_Uuid.AsString()].GetFilledPolysList(layer));assert delta.OutlineCount()==0,'Inverse original filled geometry differs';xor.append(z.m_Uuid.AsString())
 rr=BUILD/'original-restored-drc.json';drc(out,rr);policy.check_drc(rr,out)
 assert policy.sha(board)==before and policy.sha(policy.PARENT)==policy.PARENT_SHA
 result.update({'SPDX-License-Identifier':'CERN-OHL-S-2.0','status':'PASS_CAD_CONTINUITY_ONLY','source_sha256':policy.PARENT_SHA,'board_sha256':before,'plan_sha256':policy.PLAN_SHA,'intrinsic_findings':104,'drc_sha256':policy.sha(report),'inverse_hashes':hashes,'inverse_parent_bytes_equal':hashes[0]==policy.PARENT_SHA,'inverse_exact_integer_fill_xor_empty':xor,'inverse_all212_groups_equal':True,'inverse_exact104':True,'fabrication_release_allowed':False});(BUILD/'current-audit.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print(result,flush=True)
if __name__=='__main__':main()
