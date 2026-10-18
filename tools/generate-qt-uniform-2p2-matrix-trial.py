#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Accepted coupon LED pitch in a partial, non-fabrication routing trial."""

import importlib.util
from pathlib import Path
import re
import uuid

import pcbnew as p

ROOT = Path(__file__).resolve().parents[1]
STAGING = ROOT / 'hardware/coupon/rev-a/staging'
src = STAGING / 'led-1010-front-row-rgb-hdi-trial-114mm.kicad_pcb'
out = STAGING / 'led-qt-uniform-2p2-matrix-trial-114mm.kicad_pcb'
SCOPE = uuid.UUID('859dad3a-0097-4823-9b04-4562a7cceae4')
PLACEMENT_SPEC = importlib.util.spec_from_file_location(
    'base_placement', ROOT / 'tools/generate-paired-charger-114mm-placement.py')
placement = importlib.util.module_from_spec(PLACEMENT_SPEC)
PLACEMENT_SPEC.loader.exec_module(placement)
ROUTING_SPEC = importlib.util.spec_from_file_location(
    'base_routing', ROOT / 'tools/generate-paired-charger-114mm-routing.py')
routing = importlib.util.module_from_spec(ROUTING_SPEC)
ROUTING_SPEC.loader.exec_module(routing)
b=p.LoadBoard(str(src));fs={f.GetReference():f for f in b.GetFootprints()}
assert len(fs) == 483 and len(list(b.GetTracks())) == 1144
first=fs['D9'].GetPosition();x0=p.ToMM(first.x);y0=p.ToMM(first.y)
for row in range(16):
 for col in range(8,16):
  f=fs[f'D{16*row+col+1}']
  f.SetOrientationDegrees(0)
  f.SetPosition(p.VECTOR2I(p.FromMM(x0+2.2*(col-8)),p.FromMM(y0+1.95*row)))
def pt(x,y):return p.VECTOR2I(p.FromMM(x),p.FromMM(y))
def mm(v):return p.ToMM(v)
def trace(a,z,layer,net):
 s=p.PCB_TRACK(b);s.SetStart(a);s.SetEnd(z);s.SetWidth(p.FromMM(.2));s.SetLayer(layer);s.SetNet(net);b.Add(s)
def via(pos,top,bot,net):
 v=p.PCB_VIA(b);v.SetPosition(pos);v.SetViaType(p.VIATYPE_MICROVIA);v.SetLayerPair(top,bot);v.SetWidth(p.FromMM(.3));v.SetDrill(p.FromMM(.1));v.SetNet(net);b.Add(v)
def stack(pos,net,layers):
 for a,z in zip(layers,layers[1:]):via(pos,a,z,net)
for row in range(16):
 qt=[]
 for col in range(8,16):
  f=fs[f'D{16*row+col+1}'];pads={q.GetNumber():q for q in f.Pads()}
  assert all(pads[n].GetNetname()==f'COL_{col:02d}_{c}' for n,c in [('2','B'),('3','G'),('4','R')])
  a=pads['1'];assert a.GetNetname()==f'ROW_{row:02d}_A';qt.append(a)
  for n in ('2','4'):via(pads[n].GetPosition(),p.F_Cu,p.In1_Cu,pads[n].GetNet())
  center=f.GetPosition();g=pads['3']
  trace(g.GetPosition(),center,p.F_Cu,g.GetNet());stack(center,g.GetNet(),(p.F_Cu,p.In1_Cu,p.In2_Cu))
  for n,layer in [('2',p.In1_Cu),('3',p.In2_Cu),('4',p.In1_Cu)]:
   if row==0:continue
   prev=next(q for q in fs[f'D{16*(row-1)+col+1}'].Pads() if q.GetNumber()==n)
   start=prev.GetPosition() if n!='3' else fs[f'D{16*(row-1)+col+1}'].GetPosition()
   end=pads[n].GetPosition() if n!='3' else center
   trace(start,end,layer,pads[n].GetNet())
 # Same 1515 row bus for all eight uniform footprints.
 net=qt[0].GetNet();bus_y=mm(qt[0].GetPosition().y)+.575
 for a in qt:
  x=mm(a.GetPosition().x)
  trace(a.GetPosition(),pt(x,bus_y),p.F_Cu,net)
 right_x=mm(qt[-1].GetPosition().x)+.625
 trace(pt(mm(qt[0].GetPosition().x),bus_y),pt(right_x,bus_y),p.F_Cu,net)
 # Join the 1010 bus and 1515 bus on In3 at open edges.
 a1010=next(q for q in fs[f'D{16*row+1}'].Pads() if q.GetNumber()=='1')
 left=pt(40.6,mm(a1010.GetPosition().y)-.55)
 trace(left,pt(mm(a1010.GetPosition().x),mm(a1010.GetPosition().y)-.55),p.F_Cu,net)
 stack(left,net,(p.F_Cu,p.In1_Cu,p.In2_Cu,p.In3_Cu))
 right=pt(right_x,bus_y)
 stack(right,net,(p.F_Cu,p.In1_Cu,p.In2_Cu,p.In3_Cu))
 trace(left,right,p.In3_Cu,net)
assert len(list(b.GetTracks())) == 2416
assert p.SaveBoard(str(out),b)
contents = placement.sort_footprints(out.read_text())
contents = routing.sorted_native_tracks(contents, expected=2416)
serial = iter(range(contents.count('(uuid "')))
contents = re.sub(r'\(uuid "[0-9a-f-]{36}"\)',
                  lambda _: '(uuid "' + str(uuid.uuid5(SCOPE, str(next(serial)))) + '")',
                  contents)
out.write_text(contents)
loaded = p.LoadBoard(str(out))
assert loaded.GetConnectivity().GetUnconnectedCount(False) == 534
print(f'{out}: 2416 tracks/vias, 534 open edges; accepted coupon pitch trial')
