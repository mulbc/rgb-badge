# SPDX-License-Identifier: Apache-2.0
"""ADR0092 exact routing successor validation, separate from qualification."""
from collections import Counter
import hashlib,json,math,runpy
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PARENT=ROOT/'hardware/coupon/rev-a/staging/led-switch-routing-trial-114mm.kicad_pcb'
PARENT_SHA='b847f59f8a13a63d8db7a3c2ed2e7efc37239edc03c16fe12adc8b5758b4d524'
OUTPUT=ROOT/'hardware/coupon/rev-a/staging/led-remaining-routing-trial-114mm.kicad_pcb'
PLAN=ROOT/'mechanical/review/remaining-routing-plan.json'
PLAN_SHA='ece3b0976f9b396c72d2df74e9d4b11ba99789479470fe8dc12e81efd9249722'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load_plan():
 assert sha(PARENT)==PARENT_SHA and sha(PLAN)==PLAN_SHA,'Frozen routing source/plan changed'
 plan=json.loads(PLAN.read_text());assert plan['parent_sha256']==PARENT_SHA
 assert plan['native_opens']==plan['physical_opens'] and 0<=plan['native_opens']<43
 assert not plan['fabrication_release_allowed']
 return plan

def signature(board,t):
 import pcbnew as p
 if isinstance(t,p.PCB_VIA):return ('via',t.GetNetname(),t.GetPosition().x,t.GetPosition().y,board.GetLayerName(t.TopLayer()),board.GetLayerName(t.BottomLayer()),t.GetWidth(t.TopLayer()),t.GetDrillValue(),int(t.GetViaType()))
 return ('track',t.GetNetname(),t.GetStart().x,t.GetStart().y,t.GetEnd().x,t.GetEnd().y,board.GetLayerName(t.GetLayer()),t.GetWidth())

def audit(path,plan=None,fill=True):
 import pcbnew as p
 plan=plan or load_plan();old,new=[p.LoadBoard(str(x)) for x in (PARENT,path)]
 inventory=lambda b:Counter(signature(b,t) for t in b.GetTracks())
 a,b=inventory(old),inventory(new)
 assert a-b==Counter(map(tuple,plan['removed_copper'])),'Exact copper retirement differs'
 assert b-a==Counter(map(tuple,plan['added_copper'])),'Exact added copper differs'
 layers=['F.Cu','In1.Cu','In2.Cu','In3.Cu','In4.Cu','B.Cu']
 for row in plan['added_copper']:
  if row[0]=='track':assert row[-1]==200000,'General narrowing forbidden'
  elif row[-1]==int(p.VIATYPE_MICROVIA):
   assert row[6:8]==[300000,100000] and abs(layers.index(row[4])-layers.index(row[5]))==1
   assert set(row[4:6])!={'In2.Cu','In3.Cu'},'New unsupported centre microvia'
  else:assert row[4:] in (['In2.Cu','In3.Cu',500000,300000,int(p.VIATYPE_BURIED)],['F.Cu','B.Cu',500000,300000,int(p.VIATYPE_THROUGH)]),'Unreviewed via type/geometry'
 helpers=runpy.run_path(str(ROOT/'tools/check-routing-progress-trial.py'));local=helpers['local_pad_signature']
 aa={f.GetReference():f for f in old.GetFootprints()};bb={f.GetReference():f for f in new.GetFootprints()};assert aa.keys()==bb.keys() and len(aa)==483
 for ref,f in aa.items():
  g=bb[ref];assert f.m_Uuid.AsString()==g.m_Uuid.AsString()
  assert f.GetFPIDAsString()==g.GetFPIDAsString() and f.GetLayer()==g.GetLayer()
  assert Counter(map(local,f.Pads()))==Counter(map(local,g.Pads())),'Local pad/net geometry changed: '+ref
  assert sorted((q.GetName(),q.GetText()) for q in f.GetFields())==sorted((q.GetName(),q.GetText()) for q in g.GetFields()),'Part fields changed'
  pose=plan['poses'].get(ref)
  expected=(*pose['position_iu'],pose['angle_deg']) if pose else (f.GetPosition().x,f.GetPosition().y,f.GetOrientation().AsDegrees())
  assert (g.GetPosition().x,g.GetPosition().y,g.GetOrientation().AsDegrees())==expected,'Pose differs: '+ref
 structure=runpy.run_path(str(ROOT/'tools/check-routing-progress-plan.py'))['immutable_board_structure'];assert structure(PARENT)==structure(path),'Board structure changed'
 for ext in ('.kicad_pro','.kicad_dru'):assert path.with_suffix(ext).read_bytes()==PARENT.with_suffix(ext).read_bytes(),'Rule/project profile changed'
 pads=lambda board:{q.m_Uuid.AsString():q for f in board.GetFootprints() for q in f.Pads()}
 cluster=lambda board,q:frozenset(z.m_Uuid.AsString() for z in board.GetConnectivity().GetConnectedItems(q) if isinstance(z,p.PAD))
 pa,pb=pads(old),pads(new);assert pa.keys()==pb.keys() and len(pa)==2092
 groups={cluster(old,q):key for key,q in pa.items() if q.GetNetname()};assert len(groups)==231
 for _ in range(3 if fill else 1):
  if fill:p.ZONE_FILLER(new).Fill(new.Zones());new.BuildConnectivity()
  assert all(group<=cluster(new,pb[key]) for group,key in groups.items()),'Parent pad group split'
  assert new.GetConnectivity().GetUnconnectedCount(False)==plan['native_opens'],'Native open count differs'
 def pin(ref,n):
  qs=[q for q in bb[ref].Pads() if q.GetNumber()==n];assert len(qs)==1
  return qs[0]
 for entries in plan['joined_pads']:
  assert len({cluster(new,pin(*entry)) for entry in entries})==1,'Selected pin witness missing'
 # Preserve intentional source boundaries as separate net names, irrespective of routing completeness.
 assert pin('U36','6').GetNetname()=='GND' and pin('U37','12').GetNetname()=='VLED_ENABLE_DRAFT'
 assert pin('SW2','3').GetNetname()=='APP_ON_SW_DRAFT'
 if 'R1' in plan['poses']:
  for x,y in [('1','1'),('2','56')]:
   assert math.dist((pin('R1',x).GetPosition().x,pin('R1',x).GetPosition().y),(pin('U1',y).GetPosition().x,pin('U1',y).GetPosition().y))<=3000000,'IREF resistor locality lost'
 result=runpy.run_path(str(ROOT/'tools/report-coupon-board-connectivity.py'))['open_edges_by_net'](path)
 assert result['native_open_edges']==result['pad_cluster_open_edges']==plan['native_opens']
 return old,new,result
