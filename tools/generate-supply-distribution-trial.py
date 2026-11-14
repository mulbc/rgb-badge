#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Add a provisional supply pour and routed escapes to a checked study.

No source values, current limits, pad nets or placements change. Copper current
capacity, converter loops, RF, thermal and HDI process remain unqualified.
"""
import argparse
from collections import defaultdict, deque
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import re
import uuid
import pcbnew as p

ROOT = Path(__file__).resolve().parents[1]
STAGING = ROOT / 'hardware/coupon/rev-a/staging'
SPECS = {
    'app': dict(source='led-local-control-trial-114mm', net='+3V3_APP',
                plane=p.In4_Cu, source_ref='U36',
                scope='7081af13-0bac-48bd-a3ed-b163c8b25d0e'),
    'vled': dict(source='led-usb-distribution-trial-114mm', net='VLED',
                 plane=p.In1_Cu, source_ref='U37',
                 scope='6f961efb-9e5f-41e2-964d-9ec6d466b0e1'),
    'usb': dict(source='led-app-distribution-trial-114mm', net='+3V3_USB',
                plane=p.In3_Cu, source_ref='U29',
                scope='82cae0ad-4386-4e13-b9ac-d354e2fd3712'),
}


def module(name, filename):
    spec = importlib.util.spec_from_file_location(name, ROOT / 'tools' / filename)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


def pad_group(board, pad):
    return frozenset((q.GetParentFootprint().GetReference(), q.GetNumber(),
                      q.GetPosition().x, q.GetPosition().y)
                     for q in board.GetConnectivity().GetConnectedItems(pad)
                     if isinstance(q, p.PAD))


def direct_vias(board, pads, layers, net, r):
    """Use native shapes, not pad bounding boxes, to screen complete stacks."""
    bins = defaultdict(list)
    def cells(box, gap):
        return [(x, y)
                for x in range((box.GetX()-gap)//1000000, (box.GetRight()+gap)//1000000+1)
                for y in range((box.GetY()-gap)//1000000, (box.GetBottom()+gap)//1000000+1)]
    items = list(board.GetTracks())+[q for f in board.GetFootprints() for q in f.Pads()]
    for item in items:
        if item.GetNetCode() == net:
            continue
        for layer in layers:
            if item.IsOnLayer(layer):
                for cell in cells(item.GetBoundingBox(), p.FromMM(.36)):
                    bins[(layer, *cell)].append(item)
    attempts = []
    for ref, pad in pads:
        point = pad.GetPosition()
        shape = p.SHAPE_CIRCLE(point, p.FromMM(.15))
        conflicts = sum(item.GetEffectiveShape(layer).Collide(shape, p.FromMM(.2)+10)
                        for layer in layers
                        for item in bins[(layer, point.x//1000000, point.y//1000000)])
        if not conflicts:
            for a, b in zip(layers, layers[1:]):
                via = p.PCB_VIA(board)
                via.SetPosition(point)
                via.SetViaType(p.VIATYPE_MICROVIA)
                via.SetLayerPair(a, b)
                via.SetWidth(p.FromMM(r.VIA_D))
                via.SetDrill(p.FromMM(r.VIA_HOLE))
                via.SetNetCode(net)
                board.Add(via)
        attempts.append(dict(ref=ref, pad=pad.GetNumber(),
                             position_mm=list(r.xy(point)),
                             added=not bool(conflicts), shape_conflicts=conflicts))
    return attempts


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--rail', choices=SPECS, default='app')
    parser.add_argument('--max-nodes', type=int, default=500000)
    args = parser.parse_args()
    spec = SPECS[args.rail]
    source = STAGING / (spec['source']+'.kicad_pcb')
    output = STAGING / ('led-'+args.rail+'-distribution-trial-114mm.kicad_pcb')
    report_path = ROOT / ('mechanical/review/'+args.rail+'-distribution-trial.json')
    r = module('grid', 'generate-colour-fanout-grid-trial.py')
    r.X0, r.Y0, r.X1, r.Y1 = .7, .7, 113.3, 31.8
    r.NX, r.NY = round((r.X1-r.X0)/r.STEP)+1, round((r.Y1-r.Y0)/r.STEP)+1
    r.SIZE = r.NX*r.NY
    r.LAYERS = (p.B_Cu, p.In4_Cu, p.In3_Cu, p.In2_Cu, p.In1_Cu, p.F_Cu)
    r.LAYER_INDEX = {layer: index for index, layer in enumerate(r.LAYERS)}
    target_layer = r.LAYER_INDEX[spec['plane']]
    board = p.LoadBoard(str(source))
    assert all(z.GetNetname() != spec['net'] for z in board.Zones())
    net = board.FindNet(spec['net']).GetNetCode()
    pads = sorted(((f.GetReference(), q) for f in board.GetFootprints() for q in f.Pads()
                   if q.GetNetCode() == net and q.IsOnLayer(p.B_Cu)),
                  key=lambda pair: (pair[0], pair[1].GetNumber(), *r.xy(pair[1].GetPosition())))
    direct = direct_vias(board, pads, r.LAYERS[:target_layer+1], net, r)
    zone = p.ZONE(board)
    zone.SetLayer(spec['plane'])
    zone.SetNetCode(net)
    zone.SetLocalClearance(p.FromMM(.2))
    zone.SetPadConnection(p.ZONE_CONNECTION_FULL)
    zone.SetIslandRemovalMode(p.ISLAND_REMOVAL_MODE_ALWAYS)
    zone.Outline().NewOutline()
    for x, y in ((.5, .5), (113.5, .5), (113.5, 32), (.5, 32)):
        zone.Outline().Append(p.FromMM(x), p.FromMM(y))
    board.Add(zone)
    p.ZONE_FILLER(board).Fill(board.Zones())
    fill = zone.GetFilledPolysList(spec['plane'])
    main_polygon = max(range(fill.OutlineCount()), key=lambda i: fill.COutline(i).Area())
    initial_groups = {pad_group(board, pad) for _, pad in pads}
    main_group = max(initial_groups, key=len)
    main_pads = [list(node[:2]) for node in sorted(main_group)]
    missing = [(ref, pad) for ref, pad in pads if pad_group(board, pad) != main_group]
    router = r.Router(board)
    for item in board.GetTracks():
        router.occupy(item)
    radius = r.WIDTH/2+r.CLEARANCE+r.GUARD
    for part in board.GetFootprints():
        for pad in part.Pads():
            box = pad.GetBoundingBox()
            xmin, xmax, ymin, ymax = box.GetX()/1e6, box.GetRight()/1e6, box.GetY()/1e6, box.GetBottom()/1e6
            gx0 = max(0, math.floor((xmin-radius-r.X0)/r.STEP))
            gx1 = min(r.NX-1, math.ceil((xmax+radius-r.X0)/r.STEP))
            gy0 = max(0, math.floor((ymin-radius-r.Y0)/r.STEP))
            gy1 = min(r.NY-1, math.ceil((ymax+radius-r.Y0)/r.STEP))
            owner = pad.GetNetCode() or -100
            for layer, native in enumerate(r.LAYERS):
                if not pad.IsOnLayer(native):
                    continue
                mask = router.mask[layer]
                for gy in range(gy0, gy1+1):
                    dy = max(ymin-(r.Y0+gy*r.STEP), 0, r.Y0+gy*r.STEP-ymax)
                    for gx in range(gx0, gx1+1):
                        dx = max(xmin-(r.X0+gx*r.STEP), 0, r.X0+gx*r.STEP-xmax)
                        if dx*dx+dy*dy <= radius*radius:
                            cell = gy*r.NX+gx
                            mask[cell] = owner if mask[cell] in (0, owner) else -1

    def search(pad):
        x, y = r.xy(pad.GetPosition())
        if not (r.X0 <= x <= r.X1 and r.Y0 <= y <= r.Y1):
            return None, 0
        start = r.grid_index(0, x, y)
        if not router.free(0, start, net):
            return None, 0
        queue, parent = deque([start]), {start: None}
        while queue and len(parent) <= args.max_nodes:
            index = queue.popleft()
            layer, cell = divmod(index, r.SIZE)
            if layer == target_layer and fill.Contains(r.point(*r.grid_point(index)[1:]), main_polygon):
                path = []
                while index is not None:
                    path.append(index)
                    index = parent[index]
                return path[::-1], len(parent)
            gy, gx = divmod(cell, r.NX)
            neighbours = []
            for other in (layer-1, layer+1):
                if (0 <= other < len(r.LAYERS) and router.via_free(layer, cell, net)
                        and router.via_free(other, cell, net)):
                    neighbours.append(other*r.SIZE+cell)
            for dx, dy in ((-1, 0), (0, -1), (1, 0), (0, 1)):
                if 0 <= gx+dx < r.NX and 0 <= gy+dy < r.NY:
                    other = cell+dy*r.NX+dx
                    if router.free(layer, other, net):
                        neighbours.append(layer*r.SIZE+other)
            for other in neighbours:
                if other not in parent:
                    parent[other] = index
                    queue.append(other)
        return None, len(parent)

    def trace(a, b, layer):
        if a != b:
            router.trace(a, b, layer, net)

    def commit(path, pad):
        _, x, y = r.grid_point(path[0])
        trace(r.xy(pad.GetPosition()), (x, y), 0)
        pending = direction = None
        for a, b in zip(path, path[1:]):
            la, ax, ay = r.grid_point(a)
            lb, bx, by = r.grid_point(b)
            if la != lb:
                if pending is not None:
                    trace(pending, (ax, ay), la)
                pending = None
                router.via((ax, ay), r.LAYERS[lb], r.LAYERS[la], net)
                direction = None
            else:
                new_direction = (round((bx-ax)/r.STEP), round((by-ay)/r.STEP))
                if pending is not None and direction != new_direction:
                    trace(pending, (ax, ay), la)
                    pending = None
                if pending is None:
                    pending = (ax, ay)
                direction = new_direction
        if pending is not None:
            layer, x, y = r.grid_point(path[-1])
            trace(pending, (x, y), layer)

    routes = []
    for ref, pad in missing:
        path, expanded = search(pad)
        if path:
            commit(path, pad)
        entry = dict(ref=ref, pad=pad.GetNumber(), position_mm=list(r.xy(pad.GetPosition())),
                     routed=bool(path), discovered_nodes=expanded)
        routes.append(entry)
        print(entry, flush=True)
    p.ZONE_FILLER(board).Fill(board.Zones())
    p.SaveBoard(str(output), board)
    helper = module('save', 'generate-paired-charger-114mm-routing.py')
    data = helper.sorted_native_tracks(output.read_text(), expected=len(list(board.GetTracks())))
    sequence = iter(range(data.count('(uuid "')))
    scope = uuid.UUID(spec['scope'])
    data = re.sub(r'\(uuid "[0-9a-f-]{36}"\)',
                  lambda _: '(uuid "'+str(uuid.uuid5(scope, str(next(sequence))))+'")', data)
    output.write_text(data)
    loaded = p.LoadBoard(str(output))
    supply_pads = [q for f in loaded.GetFootprints() for q in f.Pads() if q.GetNetname() == spec['net']]
    groups = {pad_group(loaded, pad) for pad in supply_pads}
    main = max(groups, key=len)
    report = dict(status='UNQUALIFIED_SUPPLY_DISTRIBUTION_STUDY', rail=args.rail, net=spec['net'],
                  source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
                  board_sha256=hashlib.sha256(output.read_bytes()).hexdigest(),
                  kicad_version=p.GetBuildVersion(), grid_mm=r.STEP, width_mm=r.WIDTH,
                  clearance_mm=r.CLEARANCE, microvia_diameter_drill_mm=[r.VIA_D, r.VIA_HOLE],
                  max_nodes=args.max_nodes, direct_vias=direct, escapes=routes,
                  initial_main_cluster_pads=main_pads,
                  main_cluster_pads=[list(node[:2]) for node in sorted(main)],
                  source_ref=spec['source_ref'],
                  source_connected_to_main=any(node[0] == spec['source_ref'] for node in main),
                  zones=[dict(net=z.GetNetname(), layer=loaded.GetLayerName(z.GetLayer()),
                              polygons=z.GetFilledPolysList(z.GetLayer()).OutlineCount(),
                              area_mm2=round(z.GetFilledPolysList(z.GetLayer()).Area()/1e12, 3))
                         for z in loaded.Zones()],
                  tracks_and_vias=len(list(loaded.GetTracks())), supply_open_edges=len(groups)-1,
                  open_edges=loaded.GetConnectivity().GetUnconnectedCount(False))
    report['SPDX-License-Identifier'] = 'CERN-OHL-S-2.0'
    report_path.write_text(json.dumps(report, indent=2, sort_keys=True)+'\n')
    print('Saved', report['open_edges'], 'opens;', report['supply_open_edges'], spec['net'], flush=True)


if __name__ == '__main__':
    main()
