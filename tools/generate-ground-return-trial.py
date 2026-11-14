#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Join accessible ground islands to the existing In2 return region.

Geometry study only: no electrical/current, RF, thermal or process approval.
Run with KiCad's bundled Python. Existing components and copper are preserved.
"""
import argparse
from collections import defaultdict
import hashlib
import heapq
import importlib.util
import json
import math
from pathlib import Path
import re
import uuid
import pcbnew as p

ROOT = Path(__file__).resolve().parents[1]
STAGING = ROOT / 'hardware/coupon/rev-a/staging'
SOURCE = STAGING / 'led-ground-escape-trial-114mm.kicad_pcb'
OUTPUT = STAGING / 'led-ground-return-trial-114mm.kicad_pcb'
REPORT = ROOT / 'mechanical/review/ground-return-trial.json'
SCOPE = uuid.UUID('4d3f95ae-e68e-49fc-9659-9e82b9d1baba')


def module(name, filename):
    spec = importlib.util.spec_from_file_location(name, ROOT / 'tools' / filename)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


def clusters(board):
    connected = board.GetConnectivity()
    groups = defaultdict(list)
    for part in board.GetFootprints():
        for pad in part.Pads():
            if pad.GetNetname() == 'GND':
                group = tuple(sorted((q.GetParentFootprint().GetReference(), q.GetNumber(),
                                      q.GetPosition().x, q.GetPosition().y)
                                     for q in connected.GetConnectedItems(pad)
                                     if isinstance(q, p.PAD)))
                groups[group].append(pad)
    return groups


def rear_zone(board):
    zone = p.ZONE(board)
    zone.SetLayer(p.B_Cu)
    zone.SetNet(board.FindNet('GND'))
    zone.SetPadConnection(p.ZONE_CONNECTION_FULL)
    zone.SetLocalClearance(p.FromMM(.2))
    zone.SetIslandRemovalMode(p.ISLAND_REMOVAL_MODE_ALWAYS)
    zone.Outline().NewOutline()
    for x, y in ((.5, .5), (113.5, .5), (113.5, 32), (.5, 32)):
        zone.Outline().Append(p.FromMM(x), p.FromMM(y))
    board.Add(zone)
    return zone


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--max-nodes', type=int, default=300000)
    args = parser.parse_args()
    r = module('grid', 'generate-colour-fanout-grid-trial.py')
    r.X0, r.Y0, r.X1, r.Y1 = .7, .7, 113.3, 31.8
    r.NX = round((r.X1-r.X0)/r.STEP)+1
    r.NY = round((r.Y1-r.Y0)/r.STEP)+1
    r.SIZE = r.NX*r.NY
    r.LAYERS = (p.B_Cu, p.In4_Cu, p.In3_Cu, p.In2_Cu, p.In1_Cu, p.F_Cu)
    r.LAYER_INDEX = {layer: index for index, layer in enumerate(r.LAYERS)}
    board = p.LoadBoard(str(SOURCE))
    assert len(list(board.Zones())) == 1
    rear = rear_zone(board)
    p.ZONE_FILLER(board).Fill(board.Zones())
    back = rear.GetFilledPolysList(p.B_Cu)
    inner = next(z for z in board.Zones() if z.GetLayer() == p.In2_Cu).GetFilledPolysList(p.In2_Cu)
    # The large region contains the existing C1 ground escape. Small isolated
    # In2 islands must not be mistaken for the target ground network.
    assert inner.Contains(r.point(31.85, 2.75), 0)
    before = clusters(board)
    largest = max(before, key=len)
    assert any(ref == 'C1' and number == '2' for ref, number, _, _ in largest)
    router = r.Router(board)
    for item in board.GetTracks():
        router.occupy(item)
    radius = r.WIDTH/2+r.CLEARANCE+r.GUARD
    for part in board.GetFootprints():
        for pad in part.Pads():
            box = pad.GetBoundingBox()
            xmin, xmax = box.GetX()/1e6, box.GetRight()/1e6
            ymin, ymax = box.GetY()/1e6, box.GetBottom()/1e6
            gx0 = max(0, math.floor((xmin-radius-r.X0)/r.STEP))
            gx1 = min(r.NX-1, math.ceil((xmax+radius-r.X0)/r.STEP))
            gy0 = max(0, math.floor((ymin-radius-r.Y0)/r.STEP))
            gy1 = min(r.NY-1, math.ceil((ymax+radius-r.Y0)/r.STEP))
            net = pad.GetNetCode() or -100
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
                            mask[cell] = net if mask[cell] in (0, net) else -1
    ground = board.FindNet('GND').GetNetCode()

    def seeds(pads):
        polygons = {i for pad in pads if pad.IsOnLayer(p.B_Cu)
                    for i in range(back.OutlineCount())
                    if back.Contains(pad.GetPosition(), i)}
        points = set()
        for i in sorted(polygons):
            box = back.COutline(i).BBox()
            gx0 = max(0, math.floor((box.GetX()/1e6-r.X0)/r.STEP))
            gx1 = min(r.NX-1, math.ceil((box.GetRight()/1e6-r.X0)/r.STEP))
            gy0 = max(0, math.floor((box.GetY()/1e6-r.Y0)/r.STEP))
            gy1 = min(r.NY-1, math.ceil((box.GetBottom()/1e6-r.Y0)/r.STEP))
            for gy in range(gy0, gy1+1):
                for gx in range(gx0, gx1+1):
                    cell = gy*r.NX+gx
                    if router.free(0, cell, ground) and back.Contains(r.point(r.X0+gx*r.STEP, r.Y0+gy*r.STEP), i):
                        points.add(cell)
        # A pad without retained rear fill can still use its own centre.
        for pad in pads:
            x, y = r.xy(pad.GetPosition())
            if r.X0 <= x <= r.X1 and r.Y0 <= y <= r.Y1:
                for layer, native in enumerate(r.LAYERS):
                    if pad.IsOnLayer(native):
                        index = r.grid_index(layer, x, y)
                        if router.free(layer, index % r.SIZE, ground):
                            points.add(index)
        return points

    def search(starts):
        costs = {index: 0 for index in starts}
        parent = {index: None for index in starts}
        queue = [(abs(index//r.SIZE-3)*8, 0, index) for index in starts]
        heapq.heapify(queue)
        expanded = 0
        while queue:
            _, cost, index = heapq.heappop(queue)
            if costs.get(index) != cost:
                continue
            layer, cell = divmod(index, r.SIZE)
            _, x, y = r.grid_point(index)
            if layer == 3 and inner.Contains(r.point(x, y), 0):
                path = []
                while index is not None:
                    path.append(index)
                    index = parent[index]
                return path[::-1], expanded
            expanded += 1
            if expanded > args.max_nodes:
                break
            gy, gx = divmod(cell, r.NX)
            neighbours = []
            for dx, dy in ((-1, 0), (0, -1), (1, 0), (0, 1)):
                if 0 <= gx+dx < r.NX and 0 <= gy+dy < r.NY:
                    other = cell+dy*r.NX+dx
                    if router.free(layer, other, ground):
                        neighbours.append((layer*r.SIZE+other, 1))
            if router.via_free(layer, cell, ground):
                for other in (layer-1, layer+1):
                    if 0 <= other < len(r.LAYERS) and router.via_free(other, cell, ground):
                        neighbours.append((other*r.SIZE+cell, 8))
            for other, weight in neighbours:
                new_cost = cost+weight
                if new_cost < costs.get(other, 10**12):
                    costs[other] = new_cost
                    parent[other] = index
                    heuristic = abs(other//r.SIZE-3)*8
                    heapq.heappush(queue, (new_cost+heuristic, new_cost, other))
        return None, expanded

    def commit(path):
        pending = None
        direction = None
        for a, b in zip(path, path[1:]):
            la, ax, ay = r.grid_point(a)
            lb, bx, by = r.grid_point(b)
            if la != lb:
                if pending is not None and pending != (ax, ay):
                    router.trace(pending, (ax, ay), la, ground)
                pending = None
                router.via((ax, ay), r.LAYERS[lb], r.LAYERS[la], ground)
                direction = None
            else:
                new_direction = (round((bx-ax)/r.STEP), round((by-ay)/r.STEP))
                if pending is not None and direction != new_direction:
                    if pending != (ax, ay):
                        router.trace(pending, (ax, ay), la, ground)
                    pending = None
                if pending is None:
                    pending = (ax, ay)
                direction = new_direction
        if pending is not None:
            layer, x, y = r.grid_point(path[-1])
            if pending != (x, y):
                router.trace(pending, (x, y), layer, ground)

    routes = []
    for group, pads in sorted(before.items(), key=lambda pair: (-len(pair[0]), pair[0])):
        if group == largest:
            continue
        starts = seeds(pads)
        path, expanded = search(starts)
        if path:
            commit(path)
        entry = dict(pads=[list(pad[:2]) for pad in group],
                     seed_cells=len(starts), expanded_nodes=expanded, routed=bool(path))
        if path:
            entry['start'] = list(r.grid_point(path[0]))
            entry['end'] = list(r.grid_point(path[-1]))
        routes.append(entry)
        print(entry, flush=True)
    p.ZONE_FILLER(board).Fill(board.Zones())
    p.SaveBoard(str(OUTPUT), board)
    helper = module('save', 'generate-paired-charger-114mm-routing.py')
    data = helper.sorted_native_tracks(OUTPUT.read_text(), expected=len(list(board.GetTracks())))
    sequence = iter(range(data.count('(uuid "')))
    data = re.sub(r'\(uuid "[0-9a-f-]{36}"\)',
                  lambda _: '(uuid "'+str(uuid.uuid5(SCOPE, str(next(sequence))))+'")', data)
    OUTPUT.write_text(data)
    loaded = p.LoadBoard(str(OUTPUT))
    report = dict(status='UNQUALIFIED_GROUND_RETURN_STUDY',
                  source_sha256=hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
                  board_sha256=hashlib.sha256(OUTPUT.read_bytes()).hexdigest(),
                  kicad_version=p.GetBuildVersion(), grid_mm=r.STEP,
                  trace_width_mm=r.WIDTH, clearance_mm=r.CLEARANCE,
                  microvia_diameter_drill_mm=[r.VIA_D, r.VIA_HOLE],
                  max_nodes=args.max_nodes, routes=routes,
                  zones=[dict(layer=loaded.GetLayerName(z.GetLayer()),
                              polygons=z.GetFilledPolysList(z.GetLayer()).OutlineCount(),
                              area_mm2=round(z.GetFilledPolysList(z.GetLayer()).Area()/1e12, 3))
                         for z in loaded.Zones()],
                  tracks_and_vias=len(list(loaded.GetTracks())),
                  ground_open_edges=len(clusters(loaded))-1,
                  open_edges=loaded.GetConnectivity().GetUnconnectedCount(False))
    report['SPDX-License-Identifier'] = 'CERN-OHL-S-2.0'
    REPORT.write_text(json.dumps(report, indent=2, sort_keys=True)+'\n')
    print('Saved', report['open_edges'], 'open edges;', report['ground_open_edges'], 'GND', flush=True)


if __name__ == '__main__':
    main()
