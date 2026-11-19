# SPDX-License-Identifier: Apache-2.0
"""Exact complete R21 supply relocation ledger; CAD continuity only."""
import hashlib
import json
from pathlib import Path
import runpy
import subprocess
import sys
from decimal import Decimal
from routing_row2 import contact_catalog, hole_audit, check_drc, helper

ROOT=Path(__file__).resolve().parents[1]
PARENT=ROOT/'hardware/coupon/rev-a/staging/led-row2-routing-trial-114mm.kicad_pcb'
PARENT_SHA='1723cb53524f7907c784cc401e3b73c5e0ee93b667dedd246a87bf60c673ac34'
OUTPUT=ROOT/'hardware/coupon/rev-a/staging/led-r21-routing-trial-114mm.kicad_pcb'
PLAN=ROOT/'mechanical/review/r21-routing-plan.json'
PLAN_SHA='bfb966c9644382d0f426d2abf7e1c6f809ad30eb455a465de1abb303870dc7ad'
BOARD_SHA='e7748bee49f33b3b5c021c9215d441a047718b284e3a1ee27975e3832ddfb5d2'
PROFILES={'.kicad_pro':'1141b004ecffd1e7e8e0c30cf21aeae7ce6381093df674998133d226ab9c27fb','.kicad_dru':'80c92b0cdef868dd0ef0037aa2f63d1266f709a2dd0326094735c75ffbd31a2e'}

def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def load_plan():
 assert sha(PARENT)==PARENT_SHA and sha(PLAN)==PLAN_SHA,'Frozen source/plan changed'
 plan=json.loads(PLAN.read_text())
 assert plan['source_sha256']==PARENT_SHA and plan['expected_board_sha256']==BOARD_SHA and plan['fabrication_release_allowed'] is False
 for ext,digest in PROFILES.items():assert sha(PARENT.with_suffix(ext))==digest,'Source profile changed'
 return plan

def serialized_copper(path):
 """Read declarations before native import can repair a track's net label."""
 parser=ROOT/'tools/check-led-libraries.py'
 if sys.version_info<(3,10):
  code="import json,runpy,sys;from pathlib import Path;t=runpy.run_path(sys.argv[1])['parse_sexpr'](Path(sys.argv[2]));print(json.dumps([n for n in t[1:] if isinstance(n,list) and n and n[0] in ['segment','via','arc']]))"
  rows=json.loads(subprocess.run(['python3','-c',code,str(parser),str(path)],stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,check=True).stdout)
 else:rows=[n for n in runpy.run_path(str(parser))['parse_sexpr'](Path(path))[1:] if isinstance(n,list) and n and n[0] in ['segment','via','arc']]
 result={next(n[1] for n in row if isinstance(n,list) and n and n[0]=='uuid'):row for row in rows}
 assert len(result)==len(rows),'Duplicate serialized copper identity'
 return result

def serialized_ledger(path,plan):
 old,new=serialized_copper(PARENT),serialized_copper(path);retired={r['uuid'] for r in plan['retired_copper']};added={r['uuid']:r for r in plan['added_copper']}
 assert old.keys()-new.keys()==retired and new.keys()-old.keys()==added.keys(),'Serialized copper inventory differs'
 for uid in old.keys()&new.keys():assert old[uid]==new[uid],'Serialized source copper changed: '+uid
 def iu(value):
  v=Decimal(value)*1000000;assert v==v.to_integral_value(),'Sub-nanometre serialized coordinate';return int(v)
 for uid,row in added.items():
  node=new[uid];assert node[0]=='segment';attrs={v[0]:v[1:] for v in node[1:] if isinstance(v,list)}
  assert set(attrs)=={'start','end','width','layer','net','uuid'} and len(attrs)==len(node)-1,'Unexpected added copper attributes'
  signature=['track',attrs['net'][0],*map(iu,attrs['start']),*map(iu,attrs['end']),attrs['layer'][0],iu(attrs['width'][0])]
  assert signature==row['signature'],'Serialized added copper differs: '+uid

def components(board):
 import pcbnew as p
 pads={q.m_Uuid.AsString():q for fp in board.GetFootprints() for q in fp.Pads() if q.GetNetname()}
 tracks={t.m_Uuid.AsString() for t in board.GetTracks()};pending=set(pads);groups={};attached=set()
 while pending:
  uid=min(pending);connected=list(board.GetConnectivity().GetConnectedItems(pads[uid]));g=frozenset(q.m_Uuid.AsString() for q in connected if isinstance(q,p.PAD));assert uid in g,'Native component omits its own pad'
  copper={q.m_Uuid.AsString() for q in connected}&tracks;groups[g]=(uid,copper);attached|=copper;pending-=g
 return pads,groups,attached

def connectivity(old,new):
 aa,original,oldattached=components(old);bb,current,newattached=components(new)
 assert aa.keys()==bb.keys() and len(original)==216,'Original live pad/group inventory differs'
 lookup={uid:(g,cu) for g,(_,cu) in current.items() for uid in g};retired={r['uuid'] for r in load_plan()['retired_copper']}
 for g,(uid,cu) in original.items():
  now,newcu=lookup[uid];assert g<=now,'Original pad group split: '+aa[uid].GetNetname()
  assert cu-retired<=newcu,'Retained attached source copper orphaned: '+aa[uid].GetNetname()
 assert retired<=oldattached,'An original orphan was retired'
 added={r['uuid'] for r in load_plan()['added_copper']};assert added<=newattached,'New copper is not attached to live pads'
 gate=[q for q in bb.values() if q.GetNetname()=='ROW_GATE_15'];assert len(gate)==4 and lookup[gate[0].m_Uuid.AsString()][0]==frozenset(q.m_Uuid.AsString() for q in gate),'Full four-pad gate group disconnected'
 def pad(ref,n):return next(q for q in new.FindFootprintByReference(ref).Pads() if q.GetNumber()==n)
 supply=lookup[pad('R18','1').m_Uuid.AsString()][0]
 assert pad('R21','1').m_Uuid.AsString() in supply and len(supply)==36,'Complete main VLED join missing'
 native=new.GetConnectivity().GetUnconnectedCount(False);nets=len({q.GetNetname() for q in bb.values()});physical=len(current)-nets
 assert native==physical==27 and len(current)==215 and nets==188,'Native/physical counts differ'
 return dict(native_opens=native,physical_opens=physical,prior_groups_preserved=216,physical_groups=215,net_count=188,retained_attached_source_copper=len(oldattached-retired),original_orphan_copper_retained=19381-len(oldattached),all_new_copper_attached_to_live_pads=True)

def external_contacts(old,new,plan):
 import pcbnew as p
 tracks={t.m_Uuid.AsString():t for t in new.GetTracks()}
 def pad(board,ref,n):return next(q for q in board.FindFootprintByReference(ref).Pads() if q.GetNumber()==n)
 oldpad=pad(old,'R21','2');via=plan['external_gate_via_uuid'];outside={c['uuid'] for d in plan['source_retirement_contacts'].values() for l,v in d.items() if l=='B.Cu' for c in v['copper_and_pads'] if c['uuid'] not in {r['uuid'] for r in plan['retired_copper']}}
 assert outside=={oldpad.m_Uuid.AsString(),via},'Source gate interfaces changed'
 gate=[tracks[uid] for uid in plan['gate_lead_uuids']]
 for endpoint in [pad(new,'R21','2'),tracks[via]]:assert any(t.GetEffectiveShape(p.B_Cu).Collide(endpoint.GetEffectiveShape(p.B_Cu),0) for t in gate),'Original gate interface not touched'
 source_anchor=pad(old,'R18','1');oldmain=frozenset(o.m_Uuid.AsString() for o in old.GetConnectivity().GetConnectedItems(source_anchor) if isinstance(o,p.PAD));assert len(oldmain)==35
 supply=pad(new,'R21','1');actual=[]
 for t in old.GetTracks():
  if t.GetNetname()=='VLED' and t.IsOnLayer(p.B_Cu) and supply.GetEffectiveShape(p.B_Cu).Collide(t.GetEffectiveShape(p.B_Cu),0):actual.append(dict(uuid=t.m_Uuid.AsString(),signature=list(helper()['signature'](old,t))))
 assert sorted(actual,key=lambda r:r['uuid'])==sorted(plan['supply_source_contacts'],key=lambda r:r['uuid']) and len(actual)==3,'Actual retained supply contacts differ'
 oldtracks={t.m_Uuid.AsString():t for t in old.GetTracks()}
 for row in actual:
  t=oldtracks[row['uuid']];assert frozenset(o.m_Uuid.AsString() for o in old.GetConnectivity().GetConnectedItems(t) if isinstance(o,p.PAD))==oldmain,'Supply contact was not in original main group'
  assert supply.GetEffectiveShape(p.B_Cu).Collide(tracks[row['uuid']].GetEffectiveShape(p.B_Cu),0),'Retained direct supply contact lost'
 assert abs(sum(t.GetLength() for t in gate)/1e6-3.65)<1e-8 and plan['new_supply_copper_mm']==0
 return dict(retained_gate_via=via,source_gate_interfaces=sorted(outside),retained_direct_supply_tracks=[r['uuid'] for r in actual],original_main_vled_pads=35,new_main_vled_pads=36,gate_length_mm=3.65,new_supply_copper_mm=0)

def audit(path,plan=None):
 import pcbnew as p
 plan=load_plan() if plan is None else plan;assert plan==load_plan(),'Plan fields changed'
 serialized_ledger(path,plan)
 old,new=(p.LoadBoard(str(q)) for q in (PARENT,path));h=helper();aa={f.GetReference():f for f in old.GetFootprints()};bb={f.GetReference():f for f in new.GetFootprints()};assert aa.keys()==bb.keys() and len(aa)==len(list(old.GetFootprints()))==len(list(new.GetFootprints()))==483
 assert plan['poses']=={'R21':{'position_iu':[59300000,5600000],'orientation_degrees':0}}
 assert next(v.GetText() for v in bb['R21'].GetFields() if v.GetName()=='MPN')=='ERJ2RKF1001X'
 for ref,a in aa.items():
  b=bb[ref];assert (a.m_Uuid.AsString(),a.GetFPIDAsString(),a.GetValue(),a.GetLayer(),sorted((v.GetName(),v.GetText(),v.m_Uuid.AsString()) for v in a.GetFields()))==(b.m_Uuid.AsString(),b.GetFPIDAsString(),b.GetValue(),b.GetLayer(),sorted((v.GetName(),v.GetText(),v.m_Uuid.AsString()) for v in b.GetFields())),'Part identity/fields changed: '+ref
  assert sorted(h['local_pad_signature'](q) for q in a.Pads())==sorted(h['local_pad_signature'](q) for q in b.Pads()),'Local pad data changed: '+ref
  pose=plan['poses'].get(ref,dict(position_iu=list(a.GetPosition()),orientation_degrees=a.GetOrientationDegrees()%360));assert (list(b.GetPosition()),b.GetOrientationDegrees()%360)==(pose['position_iu'],pose['orientation_degrees']),'Part pose changed: '+ref
  ap={q.m_Uuid.AsString():q for q in a.Pads()};bp={q.m_Uuid.AsString():q for q in b.Pads()};assert ap.keys()==bp.keys() and len(ap)==len(list(a.Pads())) and len(bp)==len(list(b.Pads()))
  for uid,q in ap.items():
   x,y=q.GetPosition();expected=[126550000-x,11350000-y] if ref=='R21' else [x,y];assert list(bp[uid].GetPosition())==expected,'Independent absolute pad transform failed'
 structure=runpy.run_path(str(ROOT/'tools/check-routing-progress-plan.py'))['immutable_board_structure'];assert structure(PARENT)==structure(path),'Immutable board/net/zone/setup structure changed'
 for ext,digest in PROFILES.items():assert sha(Path(path).with_suffix(ext))==digest and PARENT.with_suffix(ext).read_bytes()==Path(path).with_suffix(ext).read_bytes(),'Profile/rules changed'
 ot={t.m_Uuid.AsString():t for t in old.GetTracks()};nt={t.m_Uuid.AsString():t for t in new.GetTracks()};assert len(ot)==19381 and len(nt)==len(list(new.GetTracks()))==19381,'Copper inventory/identity changed'
 retired={r['uuid'] for r in plan['retired_copper']};assert ot.keys()-nt.keys()==retired and len(retired)==2,'Source retirements differ'
 for row in plan['retired_copper']:assert list(h['signature'](old,ot[row['uuid']]))==row['signature'] and row['via_type'] is None
 for uid,t in ot.items():
  if uid in retired:continue
  assert h['signature'](old,t)==h['signature'](new,nt[uid]),'Retained source copper changed: '+uid
  if isinstance(t,p.PCB_VIA):assert t.GetViaType()==nt[uid].GetViaType(),'Original via type changed'
 added={r['uuid']:r for r in plan['added_copper']};assert nt.keys()-ot.keys()==added.keys() and len(added)==2
 for uid,row in added.items():assert list(h['signature'](new,nt[uid]))==row['signature'] and not isinstance(nt[uid],p.PCB_VIA) and row['via_type'] is None and nt[uid].GetWidth()==200000 and nt[uid].GetLayer()==p.B_Cu,'Added copper differs'
 assert contact_catalog(old,retired)==plan['source_retirement_contacts'],'Original layer-specific source contacts differ'
 result=connectivity(old,new);result.update(external_contacts=external_contacts(old,new,plan),hole_audit=hole_audit(new,added),unchanged_source_copper=19379,retired_copper=2,added_copper=2,exact_part_inventory=483,unchanged_profiles_rules_structure=True)
 return result
