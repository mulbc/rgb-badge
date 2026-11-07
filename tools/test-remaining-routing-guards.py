#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Native disconnection and isolated ledger faults for ADR0091 remaining routing."""
import json,shutil
from pathlib import Path
import pcbnew as p
import routing_remaining as policy
BUILD=policy.ROOT/'hardware/coupon/rev-a/build/remaining-routing/faults'

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
 case('usb-dp-open',disconnect('USB_DP_MCU',[('U3','14'),('R46','1')]))
 case('usb-dn-open',disconnect('USB_DN_MCU',[('U3','13'),('R45','1')]))
 case('usb-supply-open',disconnect('+3V3_USB',[('R75','1'),('U31','12')]))
 case('app-supply-open',disconnect('+3V3_APP',[('U3','2'),('U48','6')]))
 def wrong_span(b):selected(b,'USB_DP_MCU',True)[0].SetLayerPair(p.F_Cu,p.B_Cu)
 case('unsupported-full-span-microvia',wrong_span)
 def small_via(b):
  v=selected(b,'USB_DP_MCU',True)[0];v.SetWidth(200000);v.SetDrill(75000)
 case('outer-microvia-shrunk',small_via)
 case('ordinary-track-narrowed',lambda b:selected(b,'USB_DP_MCU')[0].SetWidth(120000))
 def mode(b):next(q for q in b.FindFootprintByReference('U36').Pads() if q.GetNumber()=='6').SetNetCode(b.FindNet('+3V3_APP').GetNetCode())
 case('converter-default-changed',mode)
 def previous(b):
  t=next(t for t in b.GetTracks() if t.GetNetname()=='APP_ON_SW_DRAFT' and not isinstance(t,p.PCB_VIA));b.Remove(t);held.append(t)
 case('previous-switch-copper-removed',previous)
 def reinsert(b):
  v=p.PCB_VIA(b);v.SetPosition(p.VECTOR2I(45250000,8750000));v.SetViaType(p.VIATYPE_MICROVIA);v.SetLayerPair(p.In4_Cu,p.B_Cu);v.SetWidth(300000);v.SetDrill(100000);v.SetNetCode(b.FindNet('+3V3_APP').GetNetCode());b.Add(v)
 case('retired-via-reintroduced',reinsert)
 assert policy.sha(source)==before and len(results)==10
 (BUILD/'results.json').write_text(json.dumps({'SPDX-License-Identifier':'CERN-OHL-S-2.0','source_sha256':before,'cases':results,'fabrication_release_allowed':False},indent=2,sort_keys=True)+'\n')
 print('PASS ten remaining-routing faults, including real USB/supply disconnections')
if __name__=='__main__':main()
