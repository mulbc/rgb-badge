# SPDX-License-Identifier: Apache-2.0
"""ADR0096 exact GND-strap substitution with one witnessed filled component."""
from collections import Counter
from routing_track_replacements import contacts
COHORT=[
 ('track','GND',57550000,10850000,57550000,16300000,'B.Cu',200000),
 ('track','GND',57550000,16300000,57500000,16300000,'B.Cu',200000),
 ('track','GND',57500000,16300000,57500000,16400000,'B.Cu',200000),
 ('track','GND',57500000,16400000,57450000,16400000,'B.Cu',200000),
 ('track','GND',57450000,16400000,57450000,17650000,'B.Cu',200000),
]
ENDPOINTS=[[57550000,10850000],[57450000,17650000]]
def validate_plan(plan):
 entry=plan.get('ground_plane_replacement')
 if entry is None:return Counter()
 assert entry['original_copper']==list(map(list,COHORT)),'Unreviewed plane-substitution cohort'
 assert entry['endpoints_iu']==ENDPOINTS and entry['layer']=='B.Cu' and entry['net']=='GND','Plane endpoint/layer/net inventory differs'
 assert entry['boundary_contacts'],'Plane boundary inventory missing'
 return Counter(COHORT)
def verify_native(old,new,plan,signature,physical_identity):
 import pcbnew as p
 entry=plan.get('ground_plane_replacement')
 if entry is None:return None
 validate_plan(plan);retired=Counter(map(tuple,plan['removed_copper']));retired_ids={t.m_Uuid.AsString() for t in old.GetTracks() if signature(old,t) in retired};boundary={}
 for row in COHORT:
  t=next(t for t in old.GetTracks() if signature(old,t)==row)
  for key,item in contacts(old,t,signature,physical_identity):
   uid=item.m_Uuid.AsString()
   if uid not in retired_ids:boundary[uid]=(key,item)
 assert sorted([key for key,_ in boundary.values()],key=repr)==sorted(entry['boundary_contacts'],key=repr),'Plane replacement boundary inventory differs'
 actual={q.m_Uuid.AsString():q for q in list(new.GetTracks())+[q for f in new.GetFootprints() for q in f.Pads()]};kept=[]
 for uid,(key,item) in boundary.items():
  assert uid in actual,'Original plane boundary copper missing'
  q=actual[uid];now=['pad',*physical_identity(q)] if isinstance(q,p.PAD) else ['copper',*signature(new,q)]
  assert now==key and q.IsOnLayer(p.B_Cu),'Original plane boundary identity/layer differs';kept.append(q)
 for zone in new.Zones():
  if zone.GetLayer()!=p.B_Cu or zone.GetNetname()!='GND':continue
  filled=zone.GetFilledPolysList(p.B_Cu)
  for i in range(filled.OutlineCount()):
   unit=filled.UnitSet(i)
   if not all(unit.Collide(q.GetEffectiveShape(p.B_Cu),0) for q in kept):continue
   if not all(unit.Collide(p.SHAPE_CIRCLE(p.VECTOR2I(*point),100000),0) for point in ENDPOINTS):continue
   return {'zone_uuid':zone.m_Uuid.AsString(),'filled_component_index':i,'boundary_contact_count':len(kept),'both_endpoint_disks_touch':True,'single_individual_bcu_ground_component':True}
 raise AssertionError('No single filled B.Cu GND component retains every boundary contact and endpoint')
