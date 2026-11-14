#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Add routed ground escapes and one In2 plane; unqualified geometry only.

Run with KiCad's Python. Does not change placement, libraries or current limits.
"""
import argparse
from collections import deque
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
SOURCE = STAGING / 'led-row-combined-partial-trial-114mm.kicad_pcb'
OUTPUT = STAGING / 'led-ground-escape-trial-114mm.kicad_pcb'
REPORT = ROOT / 'mechanical/review/ground-escape-trial.json'
SCOPE = uuid.UUID('1558fa86-c4b4-4cf4-94de-2564898faf5f')


def module(name, filename):
    spec = importlib.util.spec_from_file_location(name, ROOT / 'tools' / filename)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--max-nodes', type=int, default=100000)
    args = parser.parse_args()
    r = module('grid', 'generate-colour-fanout-grid-trial.py')
    r.X0, r.Y0, r.X1, r.Y1 = .7, .7, 113.3, 31.8
    r.NX = round((r.X1-r.X0)/r.STEP)+1
    r.NY = round((r.Y1-r.Y0)/r.STEP)+1
    r.SIZE = r.NX*r.NY
    r.LAYERS = (p.B_Cu, p.In4_Cu, p.In3_Cu, p.In2_Cu)
    r.LAYER_INDEX = {layer: index for index, layer in enumerate(r.LAYERS)}
    board = p.LoadBoard(str(SOURCE))
    assert len(list(board.Zones())) == 0
    router = r.Router(board)
    for item in board.GetTracks():
        router.occupy(item)
    radius = r.WIDTH/2+r.CLEARANCE+r.GUARD
    ground_pads = []
    for part in board.GetFootprints():
        for pad in part.Pads():
            if pad.GetNetname() == 'GND' and pad.IsOnLayer(p.B_Cu):
                ground_pads.append((part.GetReference(), pad))
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

    def search(pad):
        x, y = r.xy(pad.GetPosition())
        if not (r.X0 <= x <= r.X1 and r.Y0 <= y <= r.Y1):
            return None, 0
        start = r.grid_index(0, x, y)
        if not router.free(0, start, ground):
            return None, 0
        queue = deque([start])
        parent = {start: None}
        while queue and len(parent) <= args.max_nodes:
            ix = queue.popleft()
            layer, cell = divmod(ix, r.SIZE)
            if layer == 3:
                path = []
                while ix is not None:
                    path.append(ix)
                    ix = parent[ix]
                return path[::-1], len(parent)
            gy, gx = divmod(cell, r.NX)
            neighbours = []
            if router.via_free(layer, cell, ground) and router.via_free(layer+1, cell, ground):
                neighbours.append((layer+1)*r.SIZE+cell)
            for dx, dy in ((-1, 0), (0, -1), (1, 0), (0, 1)):
                if 0 <= gx+dx < r.NX and 0 <= gy+dy < r.NY:
                    other = cell+dy*r.NX+dx
                    if router.free(layer, other, ground):
                        neighbours.append(layer*r.SIZE+other)
            for other in neighbours:
                if other not in parent:
                    parent[other] = ix
                    queue.append(other)
        return None, len(parent)

    def trace(a, b, layer):
        if a != b:
            router.trace(a, b, layer, ground)

    def commit(path, pad):
        _, x, y = r.grid_point(path[0])
        trace(r.xy(pad.GetPosition()), (x, y), 0)
        pending = None
        direction = None
        for a, b in zip(path, path[1:]):
            la, ax, ay = r.grid_point(a)
            lb, bx, by = r.grid_point(b)
            if la != lb:
                if pending is not None:
                    trace(pending, (ax, ay), la)
                    pending = None
                router.via((ax, ay), r.LAYERS[lb], r.LAYERS[la], ground)
                direction = None
            else:
                d = (round((bx-ax)/r.STEP), round((by-ay)/r.STEP))
                if pending is not None and d != direction:
                    trace(pending, (ax, ay), la)
                    pending = None
                if pending is None:
                    pending = (ax, ay)
                direction = d
        if pending is not None:
            layer, x, y = r.grid_point(path[-1])
            trace(pending, (x, y), layer)

    routes = []
    ground_pads.sort(key=lambda item: (item[0], item[1].GetNumber(), *r.xy(item[1].GetPosition())))
    for ref, pad in ground_pads:
        path, nodes = search(pad)
        if path:
            commit(path, pad)
        entry = dict(ref=ref, pad=pad.GetNumber(), position_mm=list(r.xy(pad.GetPosition())),
                     routed=bool(path), expanded_nodes=nodes)
        routes.append(entry)
        print(ref, pad.GetNumber(), 'routed' if path else 'blocked', nodes, flush=True)
    zone = p.ZONE(board)
    zone.SetLayer(p.In2_Cu)
    zone.SetNetCode(ground)
    zone.SetLocalClearance(p.FromMM(.2))
    zone.SetPadConnection(p.ZONE_CONNECTION_FULL)
    zone.SetIslandRemovalMode(p.ISLAND_REMOVAL_MODE_ALWAYS)
    zone.Outline().NewOutline()
    for x, y in ((.5,.5),(113.5,.5),(113.5,32),(.5,32)):
        zone.Outline().Append(p.FromMM(x),p.FromMM(y))
    board.Add(zone)
    p.ZONE_FILLER(board).Fill(board.Zones())
    p.SaveBoard(str(OUTPUT), board)
    helper = module('save', 'generate-paired-charger-114mm-routing.py')
    data = helper.sorted_native_tracks(OUTPUT.read_text(), expected=len(list(board.GetTracks())))
    sequence = iter(range(data.count('(uuid "')))
    data = re.sub(r'\(uuid "[0-9a-f-]{36}"\)',
                  lambda _: '(uuid "'+str(uuid.uuid5(SCOPE,str(next(sequence))))+'")', data)
    OUTPUT.write_text(data)
    loaded = p.LoadBoard(str(OUTPUT))
    native_zone = next(iter(loaded.Zones()))
    report = dict(status='UNQUALIFIED_GROUND_ESCAPE_STUDY',
                  source_sha256=hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
                  board_sha256=hashlib.sha256(OUTPUT.read_bytes()).hexdigest(),
                  kicad_version=p.GetBuildVersion(), grid_mm=r.STEP,
                  trace_width_mm=r.WIDTH, clearance_mm=r.CLEARANCE,
                  microvia_diameter_drill_mm=[r.VIA_D,r.VIA_HOLE],
                  max_nodes=args.max_nodes, routes=routes,
                  zone_polygons=native_zone.GetFilledPolysList(p.In2_Cu).OutlineCount(),
                  zone_area_mm2=round(native_zone.GetFilledPolysList(p.In2_Cu).Area()/1e12,3),
                  tracks_and_vias=len(list(loaded.GetTracks())),
                  open_edges=loaded.GetConnectivity().GetUnconnectedCount(False))
    report['SPDX-License-Identifier'] = 'CERN-OHL-S-2.0'
    REPORT.write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
    print('Saved', report['open_edges'], 'open edges;', report['zone_polygons'], 'polygons', flush=True)


if __name__ == '__main__':
    main()
