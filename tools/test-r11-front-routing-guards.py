#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Reject source/part/copper faults and prove actual native disconnections."""
import argparse
import copy
import json
from pathlib import Path
import runpy
import re
import shutil
import subprocess
import sys
import pcbnew as p
import routing_r11_front as policy

BUILD=policy.ROOT/'hardware/coupon/rev-a/build/r11-front-routing/faults'
CASES=['wrong-mpn','wrong-value','wrong-net','swap-pad-nets','move-r11','wrong-side','move-fixed-part','local-pad-size','wrong-field-id','retire-source','change-source-copper','wrong-original-via-type','narrow-added-track','wrong-layer-added-track','wrong-added-net','extra-track','extra-via','duplicate-track-id','duplicate-footprint','move-supply-pad','remove-gate','move-actual-port']

def trial(source,name):
 plan=policy.load_plan();b=p.LoadBoard(str(source));part=b.FindFootprintByReference('R11');pads={q.GetNumber():q for q in part.Pads()};tracks={t.m_Uuid.AsString():t for t in b.GetTracks()};added={r['uuid'] for r in plan['added_copper']};held=[];supply=tracks[plan['added_copper'][0]['uuid']]
 if name=='wrong-mpn':next(v for v in part.GetFields() if v.GetName()=='MPN').SetText('ERJ2RKF1002X')
 elif name=='wrong-value':part.SetValue('2k 1%')
 elif name=='wrong-net':pads['1'].SetNetCode(b.FindNet('+3V3_USB').GetNetCode())
 elif name=='swap-pad-nets':
  a,z=pads['1'].GetNetCode(),pads['2'].GetNetCode();pads['1'].SetNetCode(z);pads['2'].SetNetCode(a)
 elif name=='move-r11':part.SetPosition(part.GetPosition()+p.VECTOR2I(25000,0))
 elif name=='wrong-side':part.Flip(part.GetPosition(),p.FLIP_DIRECTION_TOP_BOTTOM)
 elif name=='move-fixed-part':
  fp=b.FindFootprintByReference('R18');fp.SetPosition(fp.GetPosition()+p.VECTOR2I(25000,0))
 elif name=='local-pad-size':pads['1'].SetSize(pads['1'].GetSize()+p.VECTOR2I(25000,0))
 elif name=='wrong-field-id':next(v for v in part.GetFields() if v.GetName()=='MPN').SetUuid(p.KIID('00000000-0000-0000-0000-000000000001'))
 elif name=='retire-source':
  t=next(t for uid,t in tracks.items() if uid not in added);b.Remove(t);held.append(t)
 elif name=='change-source-copper':
  t=next(t for uid,t in tracks.items() if uid not in added and not isinstance(t,p.PCB_VIA));t.SetStart(t.GetStart()+p.VECTOR2I(25000,0))
 elif name=='wrong-original-via-type':next(t for t in tracks.values() if isinstance(t,p.PCB_VIA) and t.GetViaType()!=p.VIATYPE_THROUGH).SetViaType(p.VIATYPE_THROUGH)
 elif name=='narrow-added-track':supply.SetWidth(120000)
 elif name=='wrong-layer-added-track':supply.SetLayer(p.B_Cu)
 elif name=='wrong-added-net':pass # Inject after SaveBoard, which repairs connected trace labels.
 elif name in ['extra-track','duplicate-track-id']:
  t=p.PCB_TRACK(b);t.SetStart(supply.GetStart() if name=='duplicate-track-id' else p.VECTOR2I(1000000,1000000));t.SetEnd(supply.GetEnd() if name=='duplicate-track-id' else p.VECTOR2I(2000000,1000000));t.SetLayer(p.B_Cu);t.SetWidth(200000);t.SetNetCode(supply.GetNetCode())
  if name=='duplicate-track-id':t.SetUuid(p.KIID(supply.m_Uuid.AsString()))
  b.Add(t)
 elif name=='extra-via':
  t=p.PCB_VIA(b);t.SetPosition(p.VECTOR2I(2000000,2000000));t.SetViaType(p.VIATYPE_MICROVIA);t.SetLayerPair(p.In4_Cu,p.B_Cu);t.SetWidth(300000);t.SetDrill(100000);t.SetNetCode(supply.GetNetCode());b.Add(t)
 elif name=='duplicate-footprint':
  duplicate=p.FOOTPRINT(part);b.Add(duplicate);held.append(duplicate)
 elif name in ['move-supply-pad','remove-gate','move-actual-port']:
  if name=='move-supply-pad':pads['1'].SetPosition(p.VECTOR2I(1000000,1000000))
  elif name=='move-actual-port':
   for uid,row in plan['source_outside_interfaces'].items():
    if 'signature' not in row:continue
    t=tracks[uid];delta=p.VECTOR2I(-77000000,-9500000);t.SetStart(t.GetStart()+delta);t.SetEnd(t.GetEnd()+delta)
  else:
   uid=plan['added_copper'][0]['uuid'];b.Remove(tracks[uid]);held.append(tracks[uid])
  p.ZONE_FILLER(b).Fill(b.Zones());b.BuildConnectivity()
  def group(q):return frozenset(z.m_Uuid.AsString() for z in b.GetConnectivity().GetConnectedItems(q) if isinstance(z,p.PAD))
  q=pads['1'] if name=='move-supply-pad' else pads['2'];other=next(z for fp in b.GetFootprints() if fp.GetReference()!='R11' for z in fp.Pads() if z.GetNetname()==q.GetNetname() and len(group(z))>1)
  assert group(q)!=group(other),'Fault did not physically disconnect the intended terminals'
  old=p.LoadBoard(str(policy.PARENT))
  try:policy.connectivity(old,b)
  except AssertionError as error:print('REJECTED actual separate native pad groups',name,str(error),flush=True);return
  raise RuntimeError('Actual disconnection accepted: '+name)
 out=BUILD/(name+'.kicad_pcb');p.SaveBoard(str(out),b)
 if name=='wrong-added-net':
  data=out.read_text();i=data.index(plan['added_copper'][0]['uuid']);a=data.rfind('\n\t(segment',0,i);z=data.find('\n\t)',i)+4;assert a>=0 and z>i
  block=data[a:z];altered=re.sub(r'\(net "[^"]*"\)','(net "+3V3_USB")',block,count=1);assert altered!=block;out.write_text(data[:a]+altered+data[z:])
 for ext in policy.PROFILES:shutil.copyfile(source.with_suffix(ext),out.with_suffix(ext))
 try:policy.audit(out)
 except AssertionError as error:print('REJECTED',name,str(error),flush=True);return
 raise RuntimeError('Fault accepted: '+name)

def courtyard_controls(source):
 rows=[]
 for name in ['front-courtyard-overlap','front-courtyard-missing']:
  b=p.LoadBoard(str(source));part=b.FindFootprintByReference('D1');held=[];assert part.GetLayer()==p.F_Cu
  if name=='front-courtyard-overlap':part.SetPosition(b.FindFootprintByReference('R11').GetPosition())
  else:
   for item in list(part.GraphicalItems()):
    if item.GetLayer()==p.F_CrtYd:part.Remove(item);held.append(item)
  try:policy.front_courtyards(b)
  except AssertionError as error:rows.append(dict(fault=name,exit_code=0));print('Rejected front courtyard control:',name,str(error),flush=True)
  else:raise RuntimeError('Front courtyard control accepted: '+name)
 return rows

def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--board',type=Path,required=True);ap.add_argument('--fault',choices=CASES);args=ap.parse_args();BUILD.mkdir(parents=True,exist_ok=True)
 if args.fault:trial(args.board.resolve(),args.fault);return
 before=policy.sha(args.board);policy.audit(args.board);rows=[]
 for name in CASES:
  r=subprocess.run([sys.executable,__file__,'--board',str(args.board.resolve()),'--fault',name],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True);(BUILD/(name+'.log')).write_text(r.stdout);assert r.returncode==0,r.stdout;rows.append(dict(fault=name,exit_code=0));print('Rejected:',name,flush=True)
 for name in ['omit-source-contacts','change-pose-plan']:
  plan=copy.deepcopy(policy.load_plan())
  if name=='omit-source-contacts':plan['source_retirement_contacts']={}
  else:plan['poses']['R11']['position_iu'][0]+=25000
  try:policy.audit(args.board,plan)
  except AssertionError:rows.append(dict(fault=name,exit_code=0))
  else:raise RuntimeError('Plan fault accepted: '+name)
 original=json.loads((BUILD.parent/'current-drc.json').read_text())
 for name in ['shift-intrinsic-position','change-intrinsic-description','drop-intrinsic-finding','ignore-new-check']:
  data=copy.deepcopy(original)
  if name=='shift-intrinsic-position':data['violations'][0]['items'][0]['pos']['x']+=0.025
  elif name=='change-intrinsic-description':data['violations'][0]['description']='altered actual clearance'
  elif name=='drop-intrinsic-finding':data['violations'].pop()
  else:data['ignored_checks'].append({'key':'clearance','description':'not permitted'})
  out=BUILD/(name+'.json');out.write_text(json.dumps(data))
  try:policy.check_drc(out,args.board)
  except AssertionError:rows.append(dict(fault=name,exit_code=0))
  else:raise RuntimeError('DRC fault accepted: '+name)
 rows.extend(runpy.run_path(str(policy.ROOT/'tools/test-row2-routing-guards.py'))['hole_controls']())
 rows.extend(courtyard_controls(args.board))
 assert policy.sha(args.board)==before;policy.audit(args.board)
 (BUILD/'results.json').write_text(json.dumps(rows,indent=2)+'\n');print('28 fault rejections, eight shared hole controls and two front courtyard controls pass.',flush=True)

if __name__=='__main__':main()
