#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Connect all candidate row selects across the five rear/inner copper layers."""

import hashlib
import importlib.util
import json
import heapq
import math
from pathlib import Path
import re
import uuid

import pcbnew as p

root=Path(__file__).resolve().parents[1]
staging=root/'hardware/coupon/rev-a/staging'
source=staging/'led-row-gate-tie-trial-114mm.kicad_pcb'
output=staging/'led-row-select-five-layer-trial-114mm.kicad_pcb'
manifest=root/'mechanical/review/row-select-five-layer-trial.json'
scope=uuid.UUID('cb604444-4dc4-419b-b170-be600c37a24e')
spec=importlib.util.spec_from_file_location('r',root/'tools/generate-colour-fanout-grid-trial.py');r=importlib.util.module_from_spec(spec);spec.loader.exec_module(r)
r.X0=69.5;r.X1=112.8;r.Y0=.7;r.Y1=31.8;r.NX=round((r.X1-r.X0)/r.STEP)+1;r.NY=round((r.Y1-r.Y0)/r.STEP)+1;r.SIZE=r.NX*r.NY;r.LAYERS=(p.B_Cu,p.In4_Cu,p.In3_Cu,p.In2_Cu,p.In1_Cu);r.LAYER_INDEX={v:k for k,v in enumerate(r.LAYERS)}
b=p.LoadBoard(str(source));parts={f.GetReference():f for f in b.GetFootprints()};router=r.Router(b)
assert len(parts)==483 and len(list(b.GetTracks()))==6656
for item in b.GetTracks():router.occupy(item)
rad=r.WIDTH/2+r.CLEARANCE+r.GUARD
for f in b.GetFootprints():
 for pad in f.Pads():
  if not any(pad.IsOnLayer(layer) for layer in r.LAYERS):continue
  z=pad.GetBoundingBox();xmin,xmax,ymin,ymax=z.GetX()/1e6,z.GetRight()/1e6,z.GetY()/1e6,z.GetBottom()/1e6
  gx0=max(0,math.floor((xmin-rad-r.X0)/r.STEP));gx1=min(r.NX-1,math.ceil((xmax+rad-r.X0)/r.STEP))
  gy0=max(0,math.floor((ymin-rad-r.Y0)/r.STEP));gy1=min(r.NY-1,math.ceil((ymax+rad-r.Y0)/r.STEP))
  net=pad.GetNetCode() or -100
  for layer in range(5):
   if not pad.IsOnLayer(r.LAYERS[layer]):continue
   mask=router.mask[layer]
   for gy in range(gy0,gy1+1):
    y=r.Y0+gy*r.STEP;dy=max(ymin-y,0,y-ymax)
    for gx in range(gx0,gx1+1):
     x=r.X0+gx*r.STEP;dx=max(xmin-x,0,x-xmax)
     if dx*dx+dy*dy>rad*rad:continue
     ix=gy*r.NX+gx;mask[ix]=net if mask[ix] in (0,net) else -1
def search(net,start,target,limit):
 def h(ix):
  layer,cell=divmod(ix,r.SIZE);y,x=divmod(cell,r.NX);ty,tx=divmod(target%r.SIZE,r.NX)
  return abs(x-tx)+abs(y-ty)+layer*35
 pq=[(h(start),0,start)];cost={start:0};parent={start:None};n=0
 while pq:
  _,g,ix=heapq.heappop(pq)
  if cost.get(ix)!=g:continue
  if ix==target:
   path=[]
   while ix is not None:path.append(ix);ix=parent[ix]
   return path[::-1],n
  n+=1
  if n>limit:return None,n
  layer,cell=divmod(ix,r.SIZE);y,x=divmod(cell,r.NX)
  nbr=[]
  for dx,dy in ((-1,0),(0,-1),(1,0),(0,1)):
   if 0<=x+dx<r.NX and 0<=y+dy<r.NY:
    j=cell+dy*r.NX+dx
    if router.free(layer,j,net):nbr.append((layer*r.SIZE+j,1))
  for other in (layer-1,layer+1):
   if 0<=other<5 and router.via_free(layer,cell,net) and router.via_free(other,cell,net):nbr.append((other*r.SIZE+cell,35))
  for j,w in nbr:
   ng=g+w
   if ng<cost.get(j,10**12):cost[j]=ng;parent[j]=ix;heapq.heappush(pq,(ng+h(j),ng,j))
 return None,n
def track(a,end,layer,net):
 item=p.PCB_TRACK(b);item.SetStart(r.point(*a));item.SetEnd(r.point(*end));item.SetWidth(p.FromMM(.2));item.SetLayer(r.LAYERS[layer]);item.SetNetCode(net);b.Add(item);router.occupy(item)
def via(a,layer,other,net):
 item=p.PCB_VIA(b);item.SetPosition(r.point(*a));item.SetViaType(p.VIATYPE_MICROVIA);item.SetLayerPair(r.LAYERS[max(layer,other)],r.LAYERS[min(layer,other)]);item.SetWidth(p.FromMM(.3));item.SetDrill(p.FromMM(.1));item.SetNetCode(net);b.Add(item);router.occupy(item)
def commit(path,a,z,net):
 start=r.grid_point(path[0]);end=r.grid_point(path[-1]);track(r.xy(a.GetPosition()),(start[1],start[2]),0,net)
 pending=None;direction=None
 for i,j in zip(path,path[1:]):
  il,ix,iy=r.grid_point(i);jl,jx,jy=r.grid_point(j)
  if il!=jl:
   if pending:track(pending,(ix,iy),il,net);pending=None
   via((ix,iy),il,jl,net);direction=None;continue
  d=(round((jx-ix)/r.STEP),round((jy-iy)/r.STEP))
  if pending and d!=direction:track(pending,(ix,iy),il,net);pending=None
  if pending is None:pending=(ix,iy)
  direction=d
 if pending:track(pending,(end[1],end[2]),end[0],net)
 track((end[1],end[2]),r.xy(z.GetPosition()),0,net)

routes=[]
for row in [3,2,0,1,*reversed(range(4,16))]:
 name=f'ROW_SEL_{row:02d}'
 a=next(q for q in parts[f'PAIR{row+1:02d}'].Pads() if q.GetNetname()==name);z=next(q for q in parts['U2'].Pads() if q.GetNetname()==name)
 net=a.GetNetCode();start=r.grid_index(0,*r.xy(a.GetPosition()));target=r.grid_index(0,*r.xy(z.GetPosition()))
 path,n=search(net,start,target,800000)
 print(name,len(path) if path else None,n,flush=True)
 if path: commit(path,a,z,net)
 routes.append({'net':name,'connected':bool(path),'expanded_nodes':n})

p.SaveBoard(str(output),b)
helper_spec=importlib.util.spec_from_file_location('route_base',root/'tools/generate-paired-charger-114mm-routing.py')
helper=importlib.util.module_from_spec(helper_spec);helper_spec.loader.exec_module(helper)
data=helper.sorted_native_tracks(output.read_text(),expected=len(list(b.GetTracks())))
sequence=iter(range(data.count('(uuid "')))
data=re.sub(r'\(uuid "[0-9a-f-]{36}"\)',
            lambda _: '(uuid "'+str(uuid.uuid5(scope,str(next(sequence))))+'")',data)
output.write_text(data)
loaded=p.LoadBoard(str(output))
connected=loaded.GetConnectivity()
parts={f.GetReference():f for f in loaded.GetFootprints()}
for row in range(16):
 name=f'ROW_SEL_{row:02d}'
 a=next(q for q in parts[f'PAIR{row+1:02d}'].Pads() if q.GetNetname()==name)
 z=next(q for q in parts['U2'].Pads() if q.GetNetname()==name)
 assert z in connected.GetConnectedItems(a),name
report={'SPDX-License-Identifier':'CERN-OHL-S-2.0',
        'status':'UNQUALIFIED_ROUTING_STUDY',
        'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
        'board_sha256':hashlib.sha256(output.read_bytes()).hexdigest(),
        'grid_mm':r.STEP,'width_mm':r.WIDTH,
        'candidate_microvia_diameter_drill_mm':[r.VIA_D,r.VIA_HOLE],
        'layers':['B.Cu','In4.Cu','In3.Cu','In2.Cu','In1.Cu'],
        'connected_selects':sum(route['connected'] for route in routes),
        'tracks_and_vias':len(list(loaded.GetTracks())),
        'open_edges':connected.GetUnconnectedCount(False),
        'routes':routes}
manifest.write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
print('Saved',output,report['connected_selects'],'/16 selects;',
      report['open_edges'],'open edges',flush=True)
assert report['connected_selects']==16
