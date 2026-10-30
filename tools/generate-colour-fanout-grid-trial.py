#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Route coupon colour sinks to existing matrix copper on four inner layers.

Engineering study only. Preserves pads, row routing and current settings; uses
the existing provisional adjacent-layer 0.30/0.10 mm microvia process.
"""

import argparse
from array import array
from collections import Counter
import heapq
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import re
import time
import uuid

import pcbnew as p

ROOT = Path(__file__).resolve().parents[1]
STAGING = ROOT / 'hardware/coupon/rev-a/staging'
SOURCE = STAGING / 'led-qt-uniform-2p2-row-bank-onsemi-trial-114mm.kicad_pcb'
MATRIX = STAGING / 'led-qt-uniform-2p2-matrix-trial-114mm.kicad_pcb'
OUTPUT = STAGING / 'led-colour-fanout-grid-trial-114mm.kicad_pcb'
REPORT = ROOT / 'mechanical/review/colour-fanout-grid-trial.json'
SCOPE = uuid.UUID('12c9510a-2c47-4cef-91d4-7a3f57bf172a')
STEP = 0.05
X0, Y0, X1, Y1 = 39.5, 0.4, 94.0, 32.1
NX, NY = round((X1-X0)/STEP)+1, round((Y1-Y0)/STEP)+1
SIZE = NX*NY
LAYERS = (p.In1_Cu, p.In2_Cu, p.In3_Cu, p.In4_Cu)
LAYER_INDEX = {layer: index for index, layer in enumerate(LAYERS)}
CLEARANCE, WIDTH, VIA_D, VIA_HOLE = 0.2, 0.2, 0.3, 0.1
GUARD = 0.012


def xy(pos):
    return p.ToMM(pos.x), p.ToMM(pos.y)


def signature(item):
    width = item.GetWidth(item.TopLayer()) if isinstance(item,p.PCB_VIA) else item.GetWidth()
    common = (item.GetNetname(), width)
    if isinstance(item, p.PCB_VIA):
        return ('via', *common, *xy(item.GetPosition()), item.TopLayer(),
                item.BottomLayer(), item.GetDrillValue())
    return ('track', *common, *xy(item.GetStart()), *xy(item.GetEnd()), item.GetLayer())


def point(x, y):
    return p.VECTOR2I(p.FromMM(x), p.FromMM(y))


def grid_point(index):
    layer, cell = divmod(index, SIZE)
    y, x = divmod(cell, NX)
    return layer, X0+x*STEP, Y0+y*STEP


def grid_index(layer, x, y):
    return layer*SIZE + round((y-Y0)/STEP)*NX + round((x-X0)/STEP)


def distance2(x, y, ax, ay, bx, by):
    dx, dy = bx-ax, by-ay
    t = max(0., min(1., ((x-ax)*dx+(y-ay)*dy)/(dx*dx+dy*dy))) if dx or dy else 0.
    return (x-ax-t*dx)**2+(y-ay-t*dy)**2


class Router:
    def __init__(self, board):
        self.mask = [array('i', [0])*SIZE for _ in LAYERS]
        self.board = board
        self.targets = {}
        self.bounds = {}
        self.stats = []

    def raster(self, layer, a, b, radius, net, targets=None):
        ax, ay = a
        bx, by = b
        xmin = max(0, math.ceil((min(ax,bx)-radius-X0)/STEP))
        xmax = min(NX-1, math.floor((max(ax,bx)+radius-X0)/STEP))
        ymin = max(0, math.ceil((min(ay,by)-radius-Y0)/STEP))
        ymax = min(NY-1, math.floor((max(ay,by)+radius-Y0)/STEP))
        mask = self.mask[layer]
        for gy in range(ymin,ymax+1):
            y = Y0+gy*STEP
            base = gy*NX
            for gx in range(xmin,xmax+1):
                if distance2(X0+gx*STEP,y,ax,ay,bx,by) > radius*radius:
                    continue
                cell = base+gx
                if targets is not None:
                    targets.add(layer*SIZE+cell)
                elif mask[cell] in (0,net):
                    mask[cell] = net
                else:
                    mask[cell] = -1

    def occupy(self, item):
        net = item.GetNetCode()
        width = item.GetWidth(item.TopLayer()) if isinstance(item,p.PCB_VIA) else item.GetWidth()
        radius = p.ToMM(width)/2+CLEARANCE+WIDTH/2+GUARD
        if isinstance(item,p.PCB_VIA):
            position = xy(item.GetPosition())
            for layer in LAYERS:
                if item.IsOnLayer(layer):
                    self.raster(LAYER_INDEX[layer],position,position,radius,net)
        elif item.GetLayer() in LAYER_INDEX:
            self.raster(LAYER_INDEX[item.GetLayer()],xy(item.GetStart()),
                        xy(item.GetEnd()),radius,net)

    def free(self, layer, cell, net):
        return self.mask[layer][cell] in (0,net)

    def via_free(self, layer, cell, net):
        # The mask already includes the selected track's radius. Expand it
        # for the remaining via radius, including narrower trial tracks.
        extra = math.ceil(max(0, VIA_D-WIDTH)/(2*STEP))
        gy,gx=divmod(cell,NX)
        if gx < extra or gx >= NX-extra or gy < extra or gy >= NY-extra:
            return False
        return all(self.free(layer,cell+dy*NX+dx,net)
                   for dx in range(-extra,extra+1)
                   for dy in range(-extra,extra+1))

    def search(self, net, start, max_nodes):
        goals = self.targets[net]
        goal_layers = {index//SIZE for index in goals}
        xmin,ymin,xmax,ymax = self.bounds[net]
        def heuristic(index):
            layer,cell=divmod(index,SIZE)
            gy,gx=divmod(cell,NX)
            return (max(xmin-gx,0,gx-xmax)+max(ymin-gy,0,gy-ymax)+
                    min(abs(layer-target) for target in goal_layers)*35)
        # Every driver pad can enter any inner layer through an adjacent-layer
        # stack. Reserve these sites before routing so early paths cannot trap
        # the remaining pads on one layer of the driver perimeter.
        starts = {layer*SIZE+start%SIZE:(3-layer)*35 for layer in range(4)}
        costs = {index:cost for index,cost in starts.items()
                 if self.free(index//SIZE,index%SIZE,net)}
        parents = {index:None for index in costs}
        queue = [(cost+heuristic(index),cost,index) for index,cost in costs.items()]
        heapq.heapify(queue)
        expanded=0
        while queue:
            _,cost,index=heapq.heappop(queue)
            if costs.get(index) != cost:
                continue
            if index in goals:
                path=[index]
                while parents[index] is not None:
                    index=parents[index]
                    path.append(index)
                return path[::-1],expanded
            expanded += 1
            if expanded > max_nodes:
                return None,expanded
            layer,cell=divmod(index,SIZE)
            gy,gx=divmod(cell,NX)
            neighbours=[]
            for dx,dy in ((-1,0),(0,-1),(1,0),(0,1)):
                if 0 <= gx+dx < NX and 0 <= gy+dy < NY:
                    nxt=cell+dy*NX+dx
                    if self.free(layer,nxt,net):
                        neighbours.append((layer*SIZE+nxt,1))
            if self.via_free(layer,cell,net):
                for other in (layer-1,layer+1):
                    if 0 <= other < 4 and self.via_free(other,cell,net):
                        neighbours.append((other*SIZE+cell,35))
            for nxt,weight in neighbours:
                new=cost+weight
                if new < costs.get(nxt,10**12):
                    costs[nxt]=new
                    parents[nxt]=index
                    heapq.heappush(queue,(new+heuristic(nxt),new,nxt))
        return None,expanded

    def trace(self, a, b, layer, net):
        item=p.PCB_TRACK(self.board)
        item.SetStart(point(*a));item.SetEnd(point(*b))
        item.SetLayer(LAYERS[layer]);item.SetWidth(p.FromMM(WIDTH))
        item.SetNetCode(net);self.board.Add(item);self.occupy(item)

    def via(self, pos, top, bottom, net):
        item=p.PCB_VIA(self.board);item.SetPosition(point(*pos))
        item.SetViaType(p.VIATYPE_MICROVIA);item.SetLayerPair(top,bottom)
        item.SetWidth(p.FromMM(VIA_D));item.SetDrill(p.FromMM(VIA_HOLE))
        item.SetNetCode(net);self.board.Add(item);self.occupy(item)

    def commit(self,path,net,pad):
        start_layer=path[0]//SIZE
        driver_layers=(*LAYERS[start_layer:],p.B_Cu)
        for top,bottom in zip(driver_layers,driver_layers[1:]):
            self.via(xy(pad.GetPosition()),top,bottom,net)
        # Collapse collinear grid edges to native KiCad tracks.
        pending=None
        last_direction=None
        for a,b in zip(path,path[1:]):
            la,ax,ay=grid_point(a);lb,bx,by=grid_point(b)
            if la != lb:
                if pending:
                    self.trace(pending[0],(ax,ay),la,net)
                    pending=None
                self.via((ax,ay),LAYERS[min(la,lb)],LAYERS[max(la,lb)],net)
                last_direction=None
                continue
            direction=(round((bx-ax)/STEP),round((by-ay)/STEP))
            if pending and direction != last_direction:
                self.trace(pending[0],(ax,ay),la,net)
                pending=None
            if not pending:
                pending=((ax,ay),la)
            last_direction=direction
        if pending:
            layer,x,y=grid_point(path[-1])
            self.trace(pending[0],(x,y),layer,net)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--max-nodes',type=int,default=400000)
    parser.add_argument('--retry-nodes',type=int,default=1500000)
    parser.add_argument('--order',choices=['near','far','pin'],default='near')
    parser.add_argument('--priority-net',action='append',default=None)
    args=parser.parse_args()
    if args.priority_net is None:
        args.priority_net=['COL_06_G','COL_10_B']
    board=p.LoadBoard(str(SOURCE))
    base=p.LoadBoard(str(MATRIX))
    originals=Counter(signature(item) for item in base.GetTracks())
    for item in list(board.GetTracks()):
        if not item.GetNetname().startswith('COL_'):
            continue
        sig=signature(item)
        if originals[sig]:
            originals[sig]-=1
        else:
            board.Delete(item)
    assert len(list(board.GetTracks())) == 2464
    router=Router(board)
    for item in board.GetTracks():
        router.occupy(item)
        if (not isinstance(item,p.PCB_VIA) and
                item.GetNetname().startswith('COL_') and
                item.GetLayer() in LAYER_INDEX):
            net=item.GetNetCode()
            goals=router.targets.setdefault(net,set())
            router.raster(LAYER_INDEX[item.GetLayer()],xy(item.GetStart()),
                          xy(item.GetEnd()),0.026,net,targets=goals)
    driver=next(part for part in board.GetFootprints() if part.GetReference()=='U1')
    pads=[pad for pad in driver.Pads() if pad.GetNetname().startswith('COL_')]
    assert len(pads)==48 and len(router.targets)==48
    for pad in pads:
        net=pad.GetNetCode()
        goals=router.targets[net]
        cells=[divmod(index%SIZE,NX) for index in goals]
        router.bounds[net]=(min(x for y,x in cells),min(y for y,x in cells),
                            max(x for y,x in cells),max(y for y,x in cells))
        pos=xy(pad.GetPosition())
        for layer in range(4):
            router.raster(layer,pos,pos,VIA_D/2+CLEARANCE+WIDTH/2+GUARD,net)
    if args.order=='pin':
        pads.sort(key=lambda pad:int(pad.GetNumber()))
    else:
        pads.sort(key=lambda pad:(-1 if args.order=='far' else 1)*
                  (xy(pad.GetPosition())[0]-(X0+router.bounds[pad.GetNetCode()][2]*STEP)))
    priorities={name:index for index,name in enumerate(args.priority_net)}
    pads.sort(key=lambda pad:priorities.get(pad.GetNetname(),len(priorities)))
    for pad in pads:
        net=pad.GetNetCode();start=grid_index(3,*xy(pad.GetPosition()))
        stamp=time.monotonic()
        path,expanded=router.search(net,start,args.max_nodes)
        if path:
            router.commit(path,net,pad)
        stat={'net':pad.GetNetname(),'driver_pin':pad.GetNumber(),
              'connected':bool(path),'expanded_nodes':expanded,
              'seconds':round(time.monotonic()-stamp,2),
              'grid_edges':len(path)-1 if path else None}
        router.stats.append(stat)
        print(json.dumps(stat),flush=True)
    by_net={pad.GetNetname():pad for pad in pads}
    for stat in router.stats:
        if stat['connected'] or args.retry_nodes <= args.max_nodes:
            continue
        pad=by_net[stat['net']];net=pad.GetNetCode()
        start=grid_index(3,*xy(pad.GetPosition()))
        stamp=time.monotonic()
        path,expanded=router.search(net,start,args.retry_nodes)
        if path:
            router.commit(path,net,pad)
        stat.update(connected=bool(path),expanded_nodes=expanded,
                    seconds=round(time.monotonic()-stamp,2),
                    grid_edges=len(path)-1 if path else None,retried=True)
        print(json.dumps(stat),flush=True)
    p.SaveBoard(str(OUTPUT),board)
    spec=importlib.util.spec_from_file_location('route_base',ROOT/'tools/generate-paired-charger-114mm-routing.py')
    helper=importlib.util.module_from_spec(spec);spec.loader.exec_module(helper)
    text=helper.sorted_native_tracks(OUTPUT.read_text(),expected=len(list(board.GetTracks())))
    serial=iter(range(text.count('(uuid "')))
    text=re.sub(r'\(uuid "[0-9a-f-]{36}"\)',
                lambda _:'(uuid "'+str(uuid.uuid5(SCOPE,str(next(serial))))+'")',text)
    OUTPUT.write_text(text)
    loaded=p.LoadBoard(str(OUTPUT))
    native_driver=next(part for part in loaded.GetFootprints() if part.GetReference()=='U1')
    native_pads={pad.GetNetname():pad for pad in native_driver.Pads()
                 if pad.GetNetname().startswith('COL_')}
    for stat in router.stats:
        cluster=loaded.GetConnectivity().GetConnectedItems(native_pads[stat['net']])
        led_refs=sorted({item.GetParentFootprint().GetReference() for item in cluster
                         if isinstance(item,p.PAD) and
                         item.GetParentFootprint().GetReference().startswith('D')})
        stat['native_connected_leds']=len(led_refs)
        assert len(led_refs) == (16 if stat['connected'] else 0), stat
    report={'SPDX-License-Identifier':'CERN-OHL-S-2.0',
            'status':'UNQUALIFIED_ROUTING_STUDY','order':args.order,
            'priority_nets':args.priority_net,
            'kicad_version':p.GetBuildVersion(),
            'source_sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
            'matrix_sha256':hashlib.sha256(MATRIX.read_bytes()).hexdigest(),
            'board_sha256':hashlib.sha256(OUTPUT.read_bytes()).hexdigest(),
            'initial_node_limit':args.max_nodes,'retry_node_limit':args.retry_nodes,
            'grid_mm':STEP,'track_mm':WIDTH,'clearance_mm':CLEARANCE,
            'search_bounds_mm':[X0,Y0,X1,Y1],'search_guard_mm':GUARD,
            'microvia_diameter_drill_mm':[VIA_D,VIA_HOLE],
            'connected_colours':sum(stat['connected'] for stat in router.stats),
            'tracks_and_vias':len(list(loaded.GetTracks())),
            'open_edges':loaded.GetConnectivity().GetUnconnectedCount(False),
            'routes':[{key:value for key,value in stat.items() if key!='seconds'}
                      for stat in router.stats]}
    REPORT.write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
    print(f"Saved {OUTPUT}: {report['connected_colours']}/48 colours, {report['open_edges']} open edges",flush=True)
    assert report['connected_colours']==48,'Incomplete routing trial saved for diagnosis'


if __name__=='__main__':
    main()
