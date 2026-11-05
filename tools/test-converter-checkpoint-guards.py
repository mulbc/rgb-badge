#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Eight isolated native faults for the exact selected converter checkpoint."""
from pathlib import Path
from collections import Counter
import copy,json,sys,shutil,subprocess,os,pcbnew as p
root=Path(__file__).resolve().parents[1];sys.path.insert(0,str(root/'tools'));import converter_checkpoint as policy
base=root/'hardware/coupon/rev-a/build/converter-checkpoint-review/guard-faults';base.mkdir(parents=True,exist_ok=True);plan=policy.load_plan();c=policy.native_helpers()
results=[]
names=['missing-app-switch','missing-vled-tail-lead','original-retired-via-restored','wrong-IC-pose','wrong-cap-pad','extra-copper-retirement','wrong-numbered-net','wrong-origin-ledger']
if len(sys.argv)==1:
 for case in names:subprocess.run([sys.executable,__file__,case],check=True)
 results=[json.loads((base/('fault-'+case+'.json')).read_text()) for case in names]
 (base/'native-faults.json').write_text(json.dumps(results,indent=2)+'\n');print('All eight isolated converter faults passed',flush=True);os._exit(0)
for name in [sys.argv[1]]:
 b=p.LoadBoard(str(policy.OUTPUT));parts={f.GetReference():f for f in b.GetFootprints()};caseplan=copy.deepcopy(plan);held=[]
 if name in ['missing-app-switch','missing-vled-tail-lead']:
  row=plan['app_switching_routes'][0]['tracks'][0] if name=='missing-app-switch' else ['track','VLED',51300000,18900001,51775000,18900001,'B.Cu',200000]
  t=next(t for t in b.GetTracks() if c['signature'](b,t)==tuple(row));b.Remove(t);held.append(t)
 elif name=='original-retired-via-restored':
  original=p.LoadBoard(str(c['SOURCE']));orig={c['signature'](original,t):t for t in original.GetTracks()}
  row=next(tuple(row) for row in plan['removed_copper'] if row[0]=='via' and tuple(row) in orig)
  _,net,x,y,top,bottom,width,drill=row;t=p.PCB_VIA(b);t.SetPosition(p.VECTOR2I(x,y));t.SetViaType(p.VIATYPE_MICROVIA);t.SetLayerPair(b.GetLayerID(top),b.GetLayerID(bottom));t.SetWidth(width);t.SetDrill(drill);t.SetNetCode(b.FindNet(net).GetNetCode());b.Add(t)
 elif name=='wrong-IC-pose':parts['U36'].Move(p.VECTOR2I(100000,0))
 elif name=='wrong-cap-pad':next(iter(parts['C48'].Pads())).SetSize(p.VECTOR2I(900000,900000))
 elif name=='extra-copper-retirement':
  t=next(t for t in b.GetTracks() if t.GetNetname()=='ROW_00_A');b.Remove(t);held.append(t)
 elif name=='wrong-numbered-net':next(q for q in parts['L1'].Pads() if q.GetNumber()=='1').SetNetCode(b.FindNet('VLED').GetNetCode())
 elif name=='wrong-origin-ledger':caseplan['cleanup_ledger'][0]['origin']='WRONG'
 out=base/('fault-'+name)/'trial.kicad_pcb';out.parent.mkdir(exist_ok=True);p.SaveBoard(str(out),b)
 for ext in ['.kicad_pro','.kicad_dru']:shutil.copyfile(policy.PARENT.with_suffix(ext),out.with_suffix(ext))
 try:policy.audit_geometry(policy.PARENT,out,caseplan)
 except AssertionError as e:results.append({'case':name,'passed':True,'rejected_reason':str(e)})
 else:raise AssertionError('Fault accepted: '+name)
(base/('fault-'+name+'.json')).write_text(json.dumps(results[0],indent=2)+'\n');print(results,flush=True);os._exit(0)
