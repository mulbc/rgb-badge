#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Target-group regressions; optional native routing fixture stays ignored."""
from collections import Counter
import argparse
import json
from pathlib import Path
import subprocess
import sys
from routing_group_targets import other_group_representatives


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--native',action='store_true')
    args=ap.parse_args()
    groups={'s':frozenset('ab'),'same':frozenset('ab'),'t':frozenset('c'),'duplicate':frozenset('c'),'u':frozenset('de')}
    order=['same','t','duplicate','u','s']
    assert other_group_representatives('s',order,groups.__getitem__)==['t','u']
    groups['t']=groups['duplicate']=groups['s']
    assert other_group_representatives('s',order,groups.__getitem__)==['u']
    groups['u']=groups['s']
    assert not other_group_representatives('s',order,groups.__getitem__)
    print('PASS distinct targets, source exclusion and live group changes')
    if not args.native:return
    import pcbnew as p
    root=Path(__file__).resolve().parents[1]
    build=root/'hardware/coupon/rev-a/build/group-target-regression';build.mkdir(parents=True,exist_ok=True)
    b=p.BOARD();b.SetCopperLayerCount(6)
    net=p.NETINFO_ITEM(b,'JOIN',1);wall=p.NETINFO_ITEM(b,'WALL',2);b.Add(net);b.Add(wall)
    for ref,x in [('X1',5),('X2',6),('X3',20),('X4',21)]:
        f=p.FOOTPRINT(b);f.SetReference(ref);b.Add(f)
        q=p.PAD(f);q.SetNumber('1');q.SetAttribute(p.PAD_ATTRIB_SMD);q.SetShape(p.PAD_SHAPE_RECT);q.SetSize(p.VECTOR2I(600000,600000));q.SetPosition(p.VECTOR2I(x*1000000,5000000));ls=p.LSET();ls.AddLayer(p.B_Cu);q.SetLayerSet(ls);q.SetNet(net);f.Add(q)
    def track(a,z,layer,code):
        t=p.PCB_TRACK(b);t.SetStart(p.VECTOR2I(*a));t.SetEnd(p.VECTOR2I(*z));t.SetWidth(200000);t.SetLayer(layer);t.SetNetCode(code);b.Add(t)
    track((20000000,5000000),(21000000,5000000),p.B_Cu,1)
    for layer in [p.F_Cu,p.In1_Cu,p.In2_Cu,p.In3_Cu,p.In4_Cu,p.B_Cu]:track((15000000,0),(15000000,33000000),layer,2)
    v=p.PCB_VIA(b);v.SetPosition(p.VECTOR2I(15000000,1000000));v.SetViaType(p.VIATYPE_THROUGH);v.SetLayerPair(p.F_Cu,p.B_Cu);v.SetWidth(500000);v.SetDrill(300000);v.SetNet(wall);b.Add(v)
    b.BuildConnectivity();assert b.GetConnectivity().GetUnconnectedCount(False)==2,b.GetConnectivity().GetUnconnectedCount(False)
    source=build/'source.kicad_pcb';p.SaveBoard(str(source),b)
    staging=root/'hardware/coupon/rev-a/staging/led-remaining-routing-trial-114mm.kicad_pcb'
    for ext in ['.kicad_pro','.kicad_dru']:source.with_suffix(ext).write_bytes(staging.with_suffix(ext).read_bytes())
    results={}
    for label,extra in [('anchor',[]),('all',['--all-group-targets'])]:
        report=build/(label+'.json');cmd=[sys.executable,str(root/'tools/search-routing-closure.py'),'--source',str(source),'--source-reference','X1','--output',str(build/(label+'.kicad_pcb')),'--report',str(report),'--nets','JOIN','--layers','B.Cu','--max-nodes','1000','--native-grid',*extra]
        run=subprocess.run(cmd,capture_output=True,text=True);(build/(label+'.log')).write_text(run.stdout+run.stderr);assert run.returncode==0,run.stdout+run.stderr
        results[label]=json.loads(report.read_text())
    assert results['anchor']['open_edges']==2 and not any(q['routed'] for q in results['anchor']['routes'])
    assert results['all']['open_edges']==1 and any(q['routed'] for q in results['all']['routes'])
    before=p.LoadBoard(str(source));after=p.LoadBoard(str(build/'all.kicad_pcb'))
    identities=lambda board: {f.GetReference():frozenset(q.GetParentFootprint().GetReference() for q in board.GetConnectivity().GetConnectedItems(next(iter(f.Pads()))) if isinstance(q,p.PAD)) for f in board.GetFootprints()}
    aa,zz=identities(before),identities(after)
    from routing_remaining import signature
    old_copper=Counter(signature(before,t) for t in before.GetTracks())
    new_copper=Counter(signature(after,t) for t in after.GetTracks())
    assert not old_copper-new_copper
    assert all(row[0]=='track' and row[1]=='JOIN' and row[-2:]==('B.Cu',200000) for row in (new_copper-old_copper))
    assert all(g<=zz[ref] for ref,g in aa.items()) and zz['X1']==zz['X2'] and zz['X3']==zz['X4'] and zz['X1']!=zz['X3']
    print('PASS native isolated-group join; largest group and every old group retained')


if __name__=='__main__':main()
