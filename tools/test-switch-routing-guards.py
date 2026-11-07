#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Native disconnection and isolated ledger faults for ADR0092 switch routing."""
import json,shutil
from pathlib import Path
import pcbnew as p
import routing_switch_closure as policy
BUILD=policy.ROOT/'hardware/coupon/rev-a/build/switch-routing/faults'

def main():
 plan=policy.load_plan();source=policy.OUTPUT;before=policy.sha(source);BUILD.mkdir(parents=True,exist_ok=True);results=[];held=[]
 def case(name,mutate):
  b=p.LoadBoard(str(source));mutate(b);out=BUILD/(name+'.kicad_pcb');p.SaveBoard(str(out),b)
  for ext in ('.kicad_pro','.kicad_dru'):shutil.copyfile(source.with_suffix(ext),out.with_suffix(ext))
  try:policy.audit(out,plan)
  except AssertionError as e:results.append({'case':name,'rejected':True,'reason':str(e)})
  else:raise AssertionError('Fault accepted: '+name)
 def selected(b,net,via=False):return [t for t in b.GetTracks() if t.GetNetname()==net and isinstance(t,p.PCB_VIA)==via and list(policy.signature(b,t)) in plan['added_copper']]
 def disconnect(net,refs):
  def apply(b):
   qs=[next(q for q in b.FindFootprintByReference(ref).Pads() if q.GetNumber()==pin) for ref,pin in refs]
   group=lambda q:frozenset(x.m_Uuid.AsString() for x in b.GetConnectivity().GetConnectedItems(q) if isinstance(x,p.PAD))
   assert group(qs[0])==group(qs[1])
   for t in selected(b,net)+selected(b,net,True):
    b.Remove(t);p.ZONE_FILLER(b).Fill(b.Zones());b.BuildConnectivity()
    if group(qs[0])!=group(qs[1]):held.append(t);return
    b.Add(t);p.ZONE_FILLER(b).Fill(b.Zones());b.BuildConnectivity()
   raise AssertionError('Native disconnection fixture unavailable: '+net)
  return apply
 case('switch-open',disconnect('APP_ON_SW_DRAFT',[('SW2','3'),('U36','5')]))
 case('battery-plane-bridge-open',disconnect('+BAT_PROTECTED_DRAFT',[('J2','1'),('U41','2')]))
 def wrong_span(b):selected(b,'APP_ON_SW_DRAFT',True)[0].SetViaType(p.VIATYPE_MICROVIA)
 case('full-span-retyped-microvia',wrong_span)
 def small_via(b):
  v=selected(b,'APP_ON_SW_DRAFT',True)[0];v.SetWidth(300000);v.SetDrill(100000)
 case('full-span-shrunk',small_via)
 case('ordinary-track-narrowed',lambda b:selected(b,'APP_ON_SW_DRAFT')[0].SetWidth(120000))
 def mode(b):next(q for q in b.FindFootprintByReference('U36').Pads() if q.GetNumber()=='6').SetNetCode(b.FindNet('+3V3_APP').GetNetCode())
 case('converter-default-changed',mode)
 def previous(b):
  t=next(t for t in b.GetTracks() if t.GetNetname()=='LED_IREF' and not isinstance(t,p.PCB_VIA));b.Remove(t);held.append(t)
 case('previous-iref-copper-removed',previous)
 assert policy.sha(source)==before and len(results)==7
 (BUILD/'results.json').write_text(json.dumps({'SPDX-License-Identifier':'CERN-OHL-S-2.0','source_sha256':before,'cases':results,'fabrication_release_allowed':False},indent=2,sort_keys=True)+'\n')
 print('PASS seven switch-routing faults, including real switch/battery disconnections')
if __name__=='__main__':main()
