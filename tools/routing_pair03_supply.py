# SPDX-License-Identifier: Apache-2.0
"""Frozen additive PAIR03 supply continuation; CAD continuity only."""
import json,runpy,subprocess,math
from pathlib import Path
from decimal import Decimal
from routing_pair01_supply import sha,serialized_copper,components,hole_audit,helper,PROFILES
from routing_gauge_supply import contacts
ROOT=Path(__file__).resolve().parents[1]
PARENT=ROOT/'hardware/coupon/rev-a/staging/led-pair01-supply-routing-trial-114mm.kicad_pcb'
PARENT_SHA='9574949d6bd56caa6f79b9db78af3531b0150cfba1f110d727c829effcaf62b3'
OUTPUT=PARENT.with_name('led-pair03-supply-routing-trial-114mm.kicad_pcb')
PLAN=ROOT/'mechanical/review/pair03-supply-routing-plan.json'
BOARD_SHA='03e74104c51811a18d558cdc7bd28513f9f1fcb5058ef8a7c7f62f612d8a252d'
PLAN_SHA='f7a1e57ece3039d58a20f15118869d80e0a939ecda95f21461e493753362d7e6'
def load_plan():
 assert sha(PARENT)==PARENT_SHA and sha(PLAN)==PLAN_SHA,'Frozen source/plan changed'
 plan=json.loads(PLAN.read_text());assert plan['source_sha256']==PARENT_SHA and plan['expected_board_sha256']==BOARD_SHA
 assert plan['selected'] is False and plan['fabrication_release_allowed'] is False and plan['poses']=={} and plan['retired_copper']==[]
 return plan
def serialized_ledger(path,plan):
 old,new=serialized_copper(PARENT),serialized_copper(path);retired={r['uuid'] for r in plan['retired_copper']};added={r['uuid']:r for r in plan['added_copper']}
 assert old.keys()-new.keys()==retired and new.keys()-old.keys()==added.keys(),'Serialized Cu inventory differs'
 for uid in old.keys()&new.keys():assert old[uid]==new[uid],'Serialized source Cu changed: '+uid
 def iu(v):
  n=Decimal(v)*1000000;assert n==n.to_integral_value();return int(n)
 for uid,row in added.items():
  node=new[uid];attrs={v[0]:v[1:] for v in node[1:] if isinstance(v,list)};s=row['signature']
  if s[0]=='track':
   assert node[0]=='segment' and len(node)==7 and set(attrs)=={'start','end','width','layer','net','uuid'}
   actual=['track',attrs['net'][0],*map(iu,attrs['start']),*map(iu,attrs['end']),attrs['layer'][0],iu(attrs['width'][0])]
  else:
   assert node[:2]==['via','micro'] and len(node)==8 and set(attrs)=={'at','size','drill','layers','net','uuid'}
   actual=['via',attrs['net'][0],*map(iu,attrs['at']),*attrs['layers'],iu(attrs['size'][0]),iu(attrs['drill'][0])]
  assert actual==s,'Serialized new Cu differs: '+uid

def fixed_structure(path):
 # Compare all serialized non-conductor declarations, including footprint/pad
 # nets and identities, before native import can normalize any declaration.
 code="""import json,runpy,sys
from pathlib import Path
t=runpy.run_path(sys.argv[1])['parse_sexpr'](Path(sys.argv[2]))
def strip(n):
 if not isinstance(n,list):return n
 return [strip(v) for v in n if not (isinstance(v,list) and v and v[0] in ['filled_polygon','fill_segments'])]
print(json.dumps([strip(n) for n in t[1:] if not (isinstance(n,list) and n and n[0] in ['segment','via','arc'])]))
"""
 return json.loads(subprocess.check_output(['python3','-c',code,str(ROOT/'tools/check-led-libraries.py'),str(path)],text=True))

def connectivity(old,new):
 import pcbnew as p
 aa,original,oa=components(old);bb,current,na=components(new);assert aa.keys()==bb.keys() and len(original)==211
 lookup={u:(g,cu) for g,(_,cu) in current.items() for u in g}
 for g,(uid,cu) in original.items():
  ng,nc=lookup[uid];assert g<=ng,'Original group split';assert cu<=nc,'Retained attached source Cu lost'
 assert len(oa)==19349 and len(na)==len(list(new.GetTracks()))==19367,'Orphan or unexpected copper'
 def group(board,ref,pin,table):
  q=next(q for q in board.FindFootprintByReference(ref).Pads() if q.GetNumber()==pin);return table[q.m_Uuid.AsString()][0]
 oldlookup={u:(g,cu) for g,(_,cu) in original.items() for u in g}
 assert len(group(old,'PAIR03','4',oldlookup))==1 and len(group(old,'R18','1',oldlookup))==38
 assert group(new,'PAIR03','4',lookup)==group(new,'R18','1',lookup) and len(group(new,'R18','1',lookup))==39
 assert len(group(new,'C71','2',lookup))==197 and len(group(new,'U31','12',lookup))==32
 nets=len({q.GetNetname() for q in bb.values()});native=new.GetConnectivity().GetUnconnectedCount(False)
 assert native==len(current)-nets==22 and len(current)==210 and nets==188
 return dict(native_opens=22,physical_opens=22,physical_groups=210,prior_groups_preserved=211,net_count=188,retained_attached_source_copper=19349,main_ground_pads=197,main_vled_pads=39,main_usb_pads=32,orphan_copper=0)

def audit(path,plan=None):
 import pcbnew as p
 path=Path(path);plan=load_plan() if plan is None else plan;assert plan==load_plan()
 serialized_ledger(path,plan);assert fixed_structure(PARENT)==fixed_structure(path),'Serialized part/pad/field/pose/net/board structure changed'
 for ext,digest in PROFILES.items():assert sha(path.with_suffix(ext))==digest and PARENT.with_suffix(ext).read_bytes()==path.with_suffix(ext).read_bytes(),'Profile changed'
 old,new=(p.LoadBoard(str(x)) for x in (PARENT,path));h=helper();ot={t.m_Uuid.AsString():t for t in old.GetTracks()};nt={t.m_Uuid.AsString():t for t in new.GetTracks()};added={r['uuid'] for r in plan['added_copper']};assert len(ot)==19349 and len(nt)==19367 and nt.keys()-ot.keys()==added and len(added)==18
 assert len(list(old.GetFootprints()))==len(list(new.GetFootprints()))==483
 for uid,t in ot.items():
  assert h['signature'](old,t)==h['signature'](new,nt[uid])
  if isinstance(t,p.PCB_VIA):assert t.GetViaType()==nt[uid].GetViaType()
 length=0;via_count=0
 for row in plan['added_copper']:
  t=nt[row['uuid']];assert list(h['signature'](new,t))==row['signature'] and t.GetNetname()=='VLED'
  kind=int(t.GetViaType()) if isinstance(t,p.PCB_VIA) else None;assert kind==row['via_type']
  if isinstance(t,p.PCB_VIA):
   assert kind==p.VIATYPE_MICROVIA and (t.TopLayer(),t.BottomLayer())==(p.In4_Cu,p.B_Cu) and t.GetWidth(t.TopLayer())==300000 and t.GetDrillValue()==100000;via_count+=1
  else:
   assert t.GetWidth()==200000 and t.GetLayer() in [p.B_Cu,p.In4_Cu] and t.GetStart()!=t.GetEnd();length+=t.GetLength()/1e6
 assert via_count==1 and abs(length-5.235660171779819)<1e-8
 assert contacts(old,new,added)==plan['original_contacts'],'Original source contact catalogue differs'
 witness='85ad9ca5-5c6b-5aa4-a068-b51753571be9';anchor=next(q for q in old.FindFootprintByReference('R18').Pads() if q.GetNumber()=='1')
 assert witness in {o.m_Uuid.AsString() for o in old.GetConnectivity().GetConnectedItems(anchor)}
 assert any(r['source_uuid']==witness and r['layer']=='In4.Cu' for r in plan['original_contacts'])
 assert any(r['pad']==['PAIR03','4'] for r in plan['original_contacts'])
 result=connectivity(old,new);result.update(exact_part_inventory=483,retired_copper=0,added_copper=18,added_track_length_mm=length,new_vias=1,hole_audit=hole_audit(new,added),fabrication_release_allowed=False);return result

def check_drc(path,board):
 from routing_pair01_supply import check_drc as check
 return check(path,board)
