#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Native exact ledger, UUID-group, converter-pin and full-DRC child acceptance."""
import argparse
from collections import Counter
import json
from pathlib import Path
import runpy
import subprocess
import shutil
import uuid
import pcbnew as p
import converter_checkpoint as policy


def check_orphans(path,parent,expected):
    c=policy.native_helpers();base=policy.ROOT/'hardware/coupon/rev-a/build/converter-checkpoint-review/orphans'
    base.mkdir(parents=True,exist_ok=True);out=base/'trial.kicad_pcb'
    b=p.LoadBoard(str(path));old=p.LoadBoard(str(path))
    rows=json.loads(c['PLAN'].read_text())['retired_orphan_microvias'];assert len(rows)==3
    pads=lambda board:{q.m_Uuid.AsString():q for f in board.GetFootprints() for q in f.Pads()}
    def cluster(board,q):return frozenset(z.m_Uuid.AsString() for z in board.GetConnectivity().GetConnectedItems(q) if isinstance(z,p.PAD))
    before=pads(old)
    for row in rows:
        kind,net,x,y,top,bottom,width,drill=row;assert kind=='via'
        via=p.PCB_VIA(b);via.SetPosition(p.VECTOR2I(x,y));via.SetViaType(p.VIATYPE_MICROVIA)
        via.SetLayerPair(b.GetLayerID(top),b.GetLayerID(bottom));via.SetWidth(width);via.SetDrill(drill)
        via.SetNetCode(b.FindNet(net).GetNetCode());via.SetUuid(p.KIID(str(uuid.uuid5(uuid.NAMESPACE_URL,'rgb-badge:ADR0085:orphan:'+repr(row)))));b.Add(via)
    p.ZONE_FILLER(b).Fill(b.Zones());b.BuildConnectivity();after=pads(b)
    assert all(cluster(old,q)==cluster(b,after[key]) for key,q in before.items() if q.GetNetname())
    count=old.GetConnectivity().GetUnconnectedCount(False);assert b.GetConnectivity().GetUnconnectedCount(False)==count==expected
    inv=lambda board:Counter(c['signature'](board,t) for t in board.GetTracks())
    assert inv(b)-inv(old)==Counter(map(tuple,rows)) and not inv(old)-inv(b)
    p.SaveBoard(str(out),b)
    for ext in ('.kicad_pro','.kicad_dru'):shutil.copyfile(path.with_suffix(ext),out.with_suffix(ext))
    (base/'fp-lib-table').write_text('(fp_lib_table (lib (name "rgb-badge-coupon")(type "KiCad")(uri "'+str(policy.ROOT/'hardware/coupon/rev-a/footprints/rgb-badge-coupon.pretty')+'")(options "")(descr "Local source")))\n')
    drc=out.with_suffix('.drc.json')
    proc=subprocess.run(['/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli','pcb','drc','--format','json','--output',str(drc),str(out)],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
    drc.with_suffix('.log').write_text(proc.stdout);assert proc.returncode==0
    raw=json.loads(drc.read_text());assert len(raw['violations'])==107
    dangling=[v for v in raw['violations'] if v['type']=='via_dangling'];assert len(dangling)==3
    items={t.m_Uuid.AsString():t for t in b.GetTracks()};witnessed=Counter()
    for v in dangling:
        assert v['severity']=='warning' and len(v['items'])==1
        item=v['items'][0];via=items[item['uuid']]
        assert item['pos']=={'x':via.GetPosition().x/1e6,'y':via.GetPosition().y/1e6}
        witnessed[c['signature'](b,via)]+=1
    assert witnessed==Counter(map(tuple,rows))
    raw['violations']=[v for v in raw['violations'] if v['type']!='via_dangling']
    filtered=drc.with_suffix('.intrinsic.json');filtered.write_text(json.dumps(raw))
    runpy.run_path(str(policy.ROOT/'tools/check-vled-supply-cleanup-probe.py'))['check_drc'](parent,b,filtered)
    return {'all_selected_groups_preserved':True,'native_opens':expected,'exact_restored_vias':rows,'full_findings':107,'only_three_exact_dangling_vias_added':True,'drc_sha256':policy.sha(drc)}


def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--board',type=Path,default=policy.OUTPUT)
    ap.add_argument('--check-orphans',action='store_true')
    args=ap.parse_args();path=args.board.resolve();plan=policy.load_plan()
    old,new,opens,witnesses=policy.audit_geometry(policy.PARENT,path,plan)
    drc=(policy.ROOT/'hardware/coupon/rev-a/build/converter-checkpoint-review/current.drc.json') if path==policy.OUTPUT else path.with_suffix('.drc.json')
    drc.parent.mkdir(parents=True,exist_ok=True)
    proc=subprocess.run(['/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli','pcb','drc','--format','json','--output',str(drc),str(path)],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
    drc.with_suffix('.log').write_text(proc.stdout);assert proc.returncode==0,proc.stdout
    runpy.run_path(str(policy.ROOT/'tools/check-vled-supply-cleanup-probe.py'))['check_drc'](old,new,drc)
    result={'SPDX-License-Identifier':'CERN-OHL-S-2.0','status':'PASS_EXACT_CONVERTER_CHILD_GEOMETRY_NOT_ELECTRICAL_QUALIFICATION',
        'parent_sha256':policy.PARENT_SHA,'board_sha256':policy.sha(path),'plan_sha256':policy.PLAN_SHA,
        'policy_sha256':policy.sha(Path(policy.__file__)),'checker_sha256':policy.sha(Path(__file__)),
        'retired_original_items':plan['removed_original_items'],'retired_accepted_items':plan['removed_accepted_items'],'added_copper_items':len(plan['added_copper']),'exact_poses':len(plan['poses']),
        'all_246_parent_uuid_groups_preserved':True,'converter_pin_witnesses':witnesses,'opens':opens,
        'full_intrinsic_findings':104,'drc_sha256':policy.sha(drc),'fabrication_release_allowed':False}
    if args.check_orphans:result['original_orphan_restoration']=check_orphans(path,old,plan['native_opens'])
    drc.with_suffix('.audit.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print('PASS converter child:',plan['native_opens'],'native/physical opens, all 246 parent groups, exact 104 findings',flush=True)


if __name__=='__main__':main()
