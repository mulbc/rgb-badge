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
  b=p.LoadBoard(str(source));override=mutate(b);out=BUILD/(name+'.kicad_pcb');p.SaveBoard(str(out),b)
  for ext in ('.kicad_pro','.kicad_dru'):shutil.copyfile(source.with_suffix(ext),out.with_suffix(ext))
  try:policy.audit(out,override if isinstance(override,dict) else plan)
  except AssertionError as e:results.append({'case':name,'rejected':True,'reason':str(e)});print('REJECT',name,str(e),flush=True)
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
 case('temperature-output-open',disconnect('TEMP_OK',[('U39','4'),('U39','6')]))
 case('cold-programming-open',disconnect('TMP_COLD_SET',[('R90','1'),('U39','2')]))
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
 case('cold-resistor-remote',lambda b:b.FindFootprintByReference('R90').SetPosition(p.VECTOR2I(34750000,11750000)))
 case('cold-resistor-retuned',lambda b:b.FindFootprintByReference('R90').SetValue('18k 1%'))
 def restore_return(b):
  row=plan['ground_return_replacement']['original'];_,net,x,y,a,z,layer,width=row
  t=p.PCB_TRACK(b);t.SetStart(p.VECTOR2I(x,y));t.SetEnd(p.VECTOR2I(a,z));t.SetLayer(b.GetLayerID(layer));t.SetWidth(width);t.SetNetCode(b.FindNet(net).GetNetCode());b.Add(t)
 case('obsolete-return-reintroduced',restore_return)
 def lose_return_contact(b):
  row=plan['ground_return_replacement']['replacement'][0]
  t=next(t for t in b.GetTracks() if list(policy.signature(b,t))==row)
  t.SetStart(p.VECTOR2I(60100000,16000000));changed=list(policy.signature(b,t));other=json.loads(json.dumps(plan));other['added_copper'].remove(row);other['added_copper'].append(changed);other['ground_return_replacement']['replacement'][0]=changed;return other
 case('return-endpoint-lost-with-matching-ledger',lose_return_contact)
 assert results[-1]['reason']=='Original return endpoint lost'
 def restore_strap(b):
  row=plan['ground_plane_replacement']['original_copper'][0];_,net,x,y,a,z,layer,width=row
  t=p.PCB_TRACK(b);t.SetStart(p.VECTOR2I(x,y));t.SetEnd(p.VECTOR2I(a,z));t.SetLayer(b.GetLayerID(layer));t.SetWidth(width);t.SetNetCode(b.FindNet(net).GetNetCode());b.Add(t)
 case('obsolete-body-ground-strap-reintroduced',restore_strap)
 def omit_plane_boundary(b):
  other=json.loads(json.dumps(plan));other['ground_plane_replacement']['boundary_contacts'].pop();return other
 case('plane-boundary-omitted-with-matching-copper',omit_plane_boundary)
 assert results[-1]['reason']=='Plane replacement boundary inventory differs'


 case('row-enable-probe-open',disconnect('ROW_ENABLE_N_CANDIDATE',[('TP14','1'),('U54','3')]))
 case('permission-lead-open',disconnect('USB_RAW_LOGIC_READY',[('U43','1'),('U25','3')]))
 def restore_permission(b):
  row=plan['permission_lead_replacement']['original_copper'][0];_,net,x,y,a,z,layer,width=row
  t=p.PCB_TRACK(b);t.SetStart(p.VECTOR2I(x,y));t.SetEnd(p.VECTOR2I(a,z));t.SetLayer(b.GetLayerID(layer));t.SetWidth(width);t.SetNetCode(b.FindNet(net).GetNetCode());b.Add(t)
 case('obsolete-permission-lead-reintroduced',restore_permission)
 def lose_permission_endpoint(b):
  row=plan['permission_lead_replacement']['replacement'][0]
  t=next(t for t in b.GetTracks() if list(policy.signature(b,t))==row);t.SetStart(p.VECTOR2I(92900000,18650000));changed=list(policy.signature(b,t));other=json.loads(json.dumps(plan));other['added_copper'].remove(row);other['added_copper'].append(changed);other['permission_lead_replacement']['replacement'][0]=changed;return other
 case('permission-endpoint-lost-with-matching-ledger',lose_permission_endpoint)
 assert results[-1]['reason']=='Permission outer endpoint lost'
 case('tp14-remote-again',lambda b:b.FindFootprintByReference('TP14').SetPosition(p.VECTOR2I(*plan['poses']['TP14']['old_position_iu'])))
 def omit_permission_contact(b):
  other=json.loads(json.dumps(plan));other['permission_lead_replacement']['boundary_contacts'].pop();return other
 case('permission-boundary-omitted-with-matching-copper',omit_permission_contact)
 assert results[-1]['reason']=='Permission boundary inventory differs'
 def contact_old_probe(b):
  x,y=plan['poses']['TP14']['old_position_iu'];t=p.PCB_TRACK(b);t.SetStart(p.VECTOR2I(x,y));t.SetEnd(p.VECTOR2I(x+100000,y));t.SetLayer(p.B_Cu);t.SetWidth(200000);t.SetNetCode(b.FindNet('ROW_ENABLE_N_CANDIDATE').GetNetCode());b.Add(t);other=json.loads(json.dumps(plan));other['added_copper'].append(list(policy.signature(b,t)));return other
 case('tp14-prior-contact-with-matching-ledger',contact_old_probe)
 assert results[-1]['reason']=='TP14 prior copper-contact proof failed'

 case('vled-enable-probe-open',disconnect('VLED_ENABLE_CANDIDATE',[('TP13','1'),('U55','7')]))
 def rounded_native_capture(b):
  row=next(row for row in plan['native_testpad_escape']['copper'] if row[0]=='via' and row[2:4]==[26250000,20875000]);v=next(t for t in b.GetTracks() if list(policy.signature(b,t))==row);v.SetPosition(p.VECTOR2I(26250000,20850000));changed=list(policy.signature(b,v));other=json.loads(json.dumps(plan));other['added_copper'].remove(row);other['added_copper'].append(changed);other['native_testpad_escape']['copper'].remove(row);other['native_testpad_escape']['copper'].append(changed);return other
 case('native-source-rounded-with-matching-ledger',rounded_native_capture)
 assert results[-1]['reason']=='Native source capture moved'
 def contact_old_tp13(b):
  x,y=plan['poses']['TP13']['old_position_iu'];t=p.PCB_TRACK(b);t.SetStart(p.VECTOR2I(x,y));t.SetEnd(p.VECTOR2I(x+100000,y));t.SetLayer(p.B_Cu);t.SetWidth(200000);t.SetNetCode(b.FindNet('VLED_ENABLE_CANDIDATE').GetNetCode());b.Add(t);other=json.loads(json.dumps(plan));other['added_copper'].append(list(policy.signature(b,t)));return other
 case('tp13-prior-contact-with-matching-ledger',contact_old_tp13)
 assert results[-1]['reason']=='TP13 prior copper-contact proof failed'
 case('tp13-remote-again',lambda b:b.FindFootprintByReference('TP13').SetPosition(p.VECTOR2I(*plan['poses']['TP13']['old_position_iu'])))
 def forge_isolation(b):
  other=json.loads(json.dumps(plan));other['native_testpad_escape']['isolation_pad_group'].append(next(q for q in b.FindFootprintByReference('U55').Pads() if q.GetNumber()=='7').m_Uuid.AsString());return other
 case('tp13-forged-historical-isolation',forge_isolation)
 assert results[-1]['reason']=='Test-land historical isolation group differs'

 def original_c32_pose(b):
  other=json.loads(json.dumps(plan));position=plan['poses']['C32']['old_position_iu'];b.FindFootprintByReference('C32').SetPosition(p.VECTOR2I(*position));other['poses']['C32']['position_iu']=position
  p.ZONE_FILLER(b).Fill(b.Zones());b.BuildConnectivity()
  pad=lambda ref,n:next(q for q in b.FindFootprintByReference(ref).Pads() if q.GetNumber()==n)
  group=lambda q:frozenset(x.m_Uuid.AsString() for x in b.GetConnectivity().GetConnectedItems(q) if isinstance(x,p.PAD))
  assert group(pad('C32','2'))!=group(pad('U35','9')), 'Ground-disconnection fixture did not disconnect'
  return other
 case('c32-actual-ground-open-with-matching-ledger',original_c32_pose)
 assert results[-1]['reason']=='Actual C32 ground join missing'
 def omit_c32_contact(b):
  other=json.loads(json.dumps(plan));contacts=other['capacitor_microplacement']['land_contacts'];next(rows for rows in contacts.values() if rows).pop();return other
 case('c32-contact-omitted-with-matching-copper',omit_c32_contact)
 assert results[-1]['reason']=='Original C32 contact inventory differs'
 def c32_remote(b):
  other=json.loads(json.dumps(plan));position=[89250000,10200000];b.FindFootprintByReference('C32').SetPosition(p.VECTOR2I(*position));other['poses']['C32']['position_iu']=position;return other
 case('c32-outside-bound-with-matching-ledger',c32_remote)
 assert results[-1]['reason']=='C32 translation exceeds 0.25 mm'
 def forge_c32_source(b):
  other=json.loads(json.dumps(plan));other['capacitor_microplacement']['source_sha256']='0'*64;return other
 case('c32-forged-historical-source',forge_c32_source)
 assert results[-1]['reason']=='C32 historical source differs'
 def remove_c32_guard(b):
  other=json.loads(json.dumps(plan));other.pop('capacitor_microplacement');return other
 case('c32-contact-guard-omitted',remove_c32_guard)
 assert results[-1]['reason']=='C32 contact guard missing'
 def c32_substitution(b):next(q for q in b.FindFootprintByReference('C32').GetFields() if q.GetName()=='MPN').SetText('GRM188R60J106ME47J')
 case('c32-silent-packaging-substitution',c32_substitution)
 assert results[-1]['reason']=='Part fields changed'

 assert policy.sha(source)==before and len(results)==36
 (BUILD/'results.json').write_text(json.dumps({'SPDX-License-Identifier':'CERN-OHL-S-2.0','source_sha256':before,'cases':results,'fabrication_release_allowed':False},indent=2,sort_keys=True)+'\n')
 print('PASS thirty-six remaining-routing faults, including actual C32 ground disconnection')
if __name__=='__main__':main()
