#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Native ledger/group/exact-DRC and additive-removal proof for ADR 0124."""
import argparse
import json
from pathlib import Path
import runpy
import shutil
import subprocess
import pcbnew as p
import routing_gauge_supply as policy
BUILD=policy.ROOT/'hardware/coupon/rev-a/build/gauge-supply-routing'
CLI='/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli'
def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--board',type=Path,default=policy.OUTPUT);args=ap.parse_args();board=args.board.resolve();BUILD.mkdir(parents=True,exist_ok=True)
    (BUILD/'fp-lib-table').write_text('(fp_lib_table (lib (name "rgb-badge-coupon")(type "KiCad")(uri "'+str(policy.ROOT/'hardware/coupon/rev-a/footprints/rgb-badge-coupon.pretty')+'")(options "")(descr "Local source")))\n')
    before=policy.sha(board);result=policy.audit(board);report=BUILD/'current-drc.json'
    r=subprocess.run([CLI,'pcb','drc','--format','json','--output',str(report),str(board)],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True);(BUILD/'current-drc.log').write_text(r.stdout);assert r.returncode==0,r.stdout;policy.check_drc(report)
    b=p.LoadBoard(str(board));added={r['uuid'] for r in policy.load_plan()['added_copper']};held=[]
    for t in list(b.GetTracks()):
        if t.m_Uuid.AsString() in added:b.Remove(t);held.append(t)
    assert len(held)==114
    out=BUILD/'removed-additions.kicad_pcb';sort=runpy.run_path(str(policy.ROOT/'tools/generate-paired-charger-114mm-routing.py'))['sorted_native_tracks'];hashes=[]
    for _ in range(3):
        p.ZONE_FILLER(b).Fill(b.Zones());b.BuildConnectivity();assert b.GetConnectivity().GetUnconnectedCount(False)==34;p.SaveBoard(str(out),b);out.write_text(sort(out.read_text(),expected=len(list(b.GetTracks()))));hashes.append(policy.sha(out))
    assert len(set(hashes))==1,'Counterfactual refills unstable'
    # Native filling may insert/remove collinear cached vertices. Compare exact
    # integer polygon sets, all pad groups and full DRC, not serialized vertices.
    parent=p.LoadBoard(str(policy.PARENT));other={z.m_Uuid.AsString():z for z in b.Zones()};xor_zones=[]
    for z in parent.Zones():
        layer=z.GetLayer();delta=p.SHAPE_POLY_SET(z.GetFilledPolysList(layer));delta.BooleanXor(other[z.m_Uuid.AsString()].GetFilledPolysList(layer));assert delta.OutlineCount()==0,'Counterfactual fill geometry changed';xor_zones.append(z.m_Uuid.AsString())
    def groups(board):
        return {frozenset(v.m_Uuid.AsString() for v in board.GetConnectivity().GetConnectedItems(q) if isinstance(v,p.PAD)) for f in board.GetFootprints() for q in f.Pads() if q.GetNetname()}
    assert groups(parent)==groups(b) and len(groups(b))==222,'Counterfactual pad groups differ'
    for ext in ['.kicad_pro','.kicad_dru']:shutil.copyfile(policy.PARENT.with_suffix(ext),out.with_suffix(ext))
    removed_report=BUILD/'removed-additions-drc.json';rr=subprocess.run([CLI,'pcb','drc','--format','json','--output',str(removed_report),str(out)],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True);(BUILD/'removed-additions-drc.log').write_text(rr.stdout);assert rr.returncode==0;policy.check_drc(removed_report)
    assert policy.sha(board)==before and policy.sha(policy.PARENT)==policy.PARENT_SHA
    result.update({'SPDX-License-Identifier':'CERN-OHL-S-2.0','status':'PASS_CAD_CONTINUITY_ONLY','source_sha256':policy.PARENT_SHA,'board_sha256':before,'plan_sha256':policy.PLAN_SHA,'intrinsic_findings':104,'drc_sha256':policy.sha(report),'removal_probe_hashes':hashes,'removal_probe_parent_bytes_equal':hashes[0]==policy.PARENT_SHA,'removal_probe_exact_integer_fill_xor_empty':xor_zones,'removal_probe_parent_groups_equal':True,'removal_probe_exact104':True,'fabrication_release_allowed':False})
    (BUILD/'current-audit.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print(result,flush=True)
if __name__=='__main__':main()
