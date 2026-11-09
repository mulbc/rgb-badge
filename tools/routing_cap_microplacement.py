# SPDX-License-Identifier: Apache-2.0
"""ADR0105 historical land-contact and individual ground-component witnesses."""
from collections import Counter
import hashlib
from pathlib import Path
import subprocess

ROOT=Path(__file__).resolve().parents[1]
SOURCE_SHA='ed6d3ff570f2481b47423d8375d9d4a40d756145cdd49e2c222bacc36edbfa57'
SOURCE_COMMIT='e17fa35733158734a4276d1731dc6819258ba8ac'
SOURCE_PATH='hardware/coupon/rev-a/staging/led-remaining-routing-trial-114mm.kicad_pcb'
OLD_POSITION=[89250000,10500000]
_SOURCE=None


def validate_plan(plan):
 entry=plan.get('capacitor_microplacement')
 assert set(plan['poses']) <= {'R90','TP14','TP13','C32'}, 'Unreviewed placement scope'
 assert ('C32' in plan['poses']) == (entry is not None), 'C32 contact guard missing'
 if entry is None:return
 assert entry['reference']=='C32' and entry['source_sha256']==SOURCE_SHA and entry['source_commit']==SOURCE_COMMIT, 'C32 historical source differs'
 assert entry['copper']==[], 'C32 microplacement is copper-addition-free'
 pose=plan['poses']['C32']
 assert pose['old_position_iu']==OLD_POSITION and pose['old_angle_deg']==pose['angle_deg']==180, 'C32 original pose/orientation differs'
 assert sum((a-z)**2 for a,z in zip(pose['position_iu'],OLD_POSITION)) <= 250000**2, 'C32 translation exceeds 0.25 mm'
 assert entry['joined_pad']==['U35','9'] and entry['land_contacts'], 'C32 contact/join inventory missing'


def historical_source():
 global _SOURCE
 if _SOURCE is not None:return _SOURCE
 import pcbnew as p
 path=ROOT/'hardware/coupon/rev-a/build/remaining-routing/microplacement-37-source.kicad_pcb'
 path.parent.mkdir(parents=True,exist_ok=True)
 if not path.exists() or hashlib.sha256(path.read_bytes()).hexdigest()!=SOURCE_SHA:
  proc=subprocess.run(['git','show',SOURCE_COMMIT+':'+SOURCE_PATH],cwd=ROOT,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
  assert proc.returncode==0, 'Historical C32 source requires the recorded local Git object'
  assert hashlib.sha256(proc.stdout).hexdigest()==SOURCE_SHA, 'Historical C32 source bytes differ'
  path.write_bytes(proc.stdout)
 _SOURCE=p.LoadBoard(str(path));_SOURCE.BuildConnectivity()
 return _SOURCE


def land_contacts(board,footprint,signature,physical_identity):
 import pcbnew as p
 items=list(board.GetTracks())+[q for f in board.GetFootprints() if f.GetReference()!=footprint.GetReference() for q in f.Pads()]
 result={}
 for pad in footprint.Pads():
  rows=[];shape=pad.GetEffectiveShape(p.B_Cu);box=pad.GetBoundingBox()
  for item in items:
   if item.GetNetname()!=pad.GetNetname() or not item.IsOnLayer(p.B_Cu) or not box.Intersects(item.GetBoundingBox()):continue
   if isinstance(item,p.PCB_TRACK) and not isinstance(item,p.PCB_VIA) and item.GetStart()==item.GetEnd():continue
   if shape.Collide(item.GetEffectiveShape(p.B_Cu),0):
    key=['pad',*physical_identity(item)] if isinstance(item,p.PAD) else ['copper',*signature(board,item)]
    rows.append({'uuid':item.m_Uuid.AsString(),'key':key})
  result[pad.m_Uuid.AsString()]=sorted(rows,key=repr)
 return result


def verify_native(new,plan,signature,physical_identity):
 import pcbnew as p
 validate_plan(plan);entry=plan.get('capacitor_microplacement')
 if entry is None:return None
 source=historical_source();before=source.FindFootprintByReference('C32');after=new.FindFootprintByReference('C32')
 assert (before.GetPosition().x,before.GetPosition().y)==tuple(OLD_POSITION)
 assert before.GetOrientationDegrees()==after.GetOrientationDegrees()==180
 assert before.GetValue()==after.GetValue()=='10u 6.3V X5R'
 for fp in (before,after):
  assert fp.GetLayer()==p.B_Cu and fp.GetFPIDAsString()=='rgb-badge-coupon:C_Murata_GRM188R60J106ME47_0603'
  assert next(q.GetText() for q in fp.GetFields() if q.GetName()=='MPN')=='GRM188R60J106ME47D'
 expected=land_contacts(source,before,signature,physical_identity)
 assert expected==entry['land_contacts'], 'Original C32 contact inventory differs'
 items={q.m_Uuid.AsString():q for q in list(new.GetTracks())+[q for f in new.GetFootprints() for q in f.Pads()]}
 after_pads={q.m_Uuid.AsString():q for q in after.Pads()}
 for uid,rows in expected.items():
  pad=after_pads[uid]
  for row in rows:
   assert row['uuid'] in items, 'C32 original contact removed'
   actual=items[row['uuid']]
   key=['pad',*physical_identity(actual)] if isinstance(actual,p.PAD) else ['copper',*signature(new,actual)]
   assert key==row['key'] and actual.IsOnLayer(p.B_Cu), 'C32 original contact identity/layer differs'
   assert pad.GetEffectiveShape(p.B_Cu).Collide(actual.GetEffectiveShape(p.B_Cu),0), 'C32 original land contact lost'
 inventory=lambda board:Counter(signature(board,t) for t in board.GetTracks())
 assert not inventory(source)-inventory(new), 'C32 historical source copper retired'
 pin=lambda board,ref,n:next(q for q in board.FindFootprintByReference(ref).Pads() if q.GetNumber()==n)
 cluster=lambda board,q:frozenset(t.m_Uuid.AsString() for t in board.GetConnectivity().GetConnectedItems(q) if isinstance(t,p.PAD))|{q.m_Uuid.AsString()}
 old_ground=pin(source,'C32','2');ground=pin(new,'C32','2');anchor=pin(new,*entry['joined_pad'])
 assert cluster(source,old_ground)==frozenset([old_ground.m_Uuid.AsString()]) and not expected[old_ground.m_Uuid.AsString()], 'C32 historical ground not isolated'
 assert cluster(new,ground)==cluster(new,anchor) and len(cluster(new,ground))>=194, 'Actual C32 ground join missing'
 old_anchor=pin(source,*entry['joined_pad']);old_items={q.m_Uuid.AsString():q for q in list(source.GetTracks())+[q for f in source.GetFootprints() for q in f.Pads()]}
 main_ids={q.m_Uuid.AsString() for q in source.GetConnectivity().GetConnectedItems(old_anchor)}|{old_anchor.m_Uuid.AsString()}
 witness=None
 for zone in new.Zones():
  if zone.GetLayer()!=p.B_Cu or zone.GetNetname()!='GND':continue
  filled=zone.GetFilledPolysList(p.B_Cu)
  for i in range(filled.OutlineCount()):
   unit=filled.UnitSet(i)
   if not unit.Collide(ground.GetEffectiveShape(p.B_Cu),0):continue
   for uid in sorted(main_ids & old_items.keys() & items.keys()):
    original,actual=old_items[uid],items[uid]
    if not original.IsOnLayer(p.B_Cu) or not actual.IsOnLayer(p.B_Cu):continue
    if isinstance(actual,p.PCB_TRACK) and not isinstance(actual,p.PCB_VIA) and actual.GetStart()==actual.GetEnd():continue
    if unit.BBox().Intersects(actual.GetBoundingBox()) and unit.Collide(actual.GetEffectiveShape(p.B_Cu),0):
     witness={'zone_uuid':zone.m_Uuid.AsString(),'filled_component_index':i,'retained_main_ground_copper_uuid':uid};break
   if witness:break
  if witness:break
 assert witness is not None, 'C32 lacks individual B.Cu main-ground component contact'
 return {'reference':'C32','source_sha256':SOURCE_SHA,'source_commit':SOURCE_COMMIT,
  'original_direct_land_contacts_retained':True,'contact_count':sum(map(len,expected.values())),
  'historical_ground_isolated':True,'historical_source_copper_retained':True,
  'displacement_iu':[after.GetPosition().x-OLD_POSITION[0],after.GetPosition().y-OLD_POSITION[1]],
  'joined_pad':entry['joined_pad'],'single_individual_bcu_ground_component':True,**witness}
