#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Route selected local low-speed controls on the checked combined study.

No rail, analog feedback, USB differential, clock or current-setting routes are
selected here. This source geometry does not qualify any electrical behavior.
"""
import argparse
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
SOURCE = STAGING / 'led-row14-bias-trial-114mm.kicad_pcb'
OUTPUT = STAGING / 'led-local-control-trial-114mm.kicad_pcb'
REPORT = ROOT / 'mechanical/review/local-control-trial.json'
SCOPE = uuid.UUID('6bbdb60b-e42a-4feb-b080-aebdf69074b9')
NETS = ['APP_SUPERVISOR_OK', 'DISPLAY_CLEAR_3', 'HEARTBEAT_FALL_CLK',
        'HEARTBEAT_SEEN', 'ROW_ARM', 'ROW_REQUEST', 'DISPLAY_ARM_CLK',
        'ARM_LATCH', 'DISPLAY_ENABLE', 'DISPLAY_CLEAR_OK', 'VLED_WINDOW_OK',
        'ROW_ENABLE_REQ_N', 'ROW_ENABLE_N_CANDIDATE', 'VLED_ENABLE_CANDIDATE',
        'USB_LOGIC_READY', 'USB_CHARGE_REQ', 'USB_VBUS_VALID', 'USB_OUT1',
        'USB_OUT2', 'USB_RAW_LOGIC_READY', 'USB_EN1_RAW_N',
        'USB_RAW_VBUS_VALID', 'TEMP_OK']


def module(name, filename):
    spec = importlib.util.spec_from_file_location(name, ROOT / 'tools' / filename)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


def identities(board, pad):
    return frozenset((q.GetParentFootprint().GetReference(), q.GetNumber(),
                      q.GetPosition().x, q.GetPosition().y)
                     for q in board.GetConnectivity().GetConnectedItems(pad)
                     if isinstance(q, p.PAD))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--max-nodes', type=int, default=200000)
    args = parser.parse_args()
    r = module('grid', 'generate-colour-fanout-grid-trial.py')
    r.X0, r.Y0, r.X1, r.Y1 = .7, .7, 113.3, 31.8
    r.NX = round((r.X1-r.X0)/r.STEP)+1
    r.NY = round((r.Y1-r.Y0)/r.STEP)+1
    r.SIZE = r.NX*r.NY
    r.LAYERS = (p.B_Cu, p.In4_Cu, p.In3_Cu, p.In2_Cu, p.In1_Cu, p.F_Cu)
    r.LAYER_INDEX = {layer: index for index, layer in enumerate(r.LAYERS)}
    board = p.LoadBoard(str(SOURCE))
    router = r.Router(board)
    for item in board.GetTracks():
        router.occupy(item)
    radius = r.WIDTH/2+r.CLEARANCE+r.GUARD
    pads_by_net = {}
    for part in board.GetFootprints():
        for pad in part.Pads():
            pads_by_net.setdefault(pad.GetNetname(), []).append(pad)
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

    def pad_cells(pad):
        x, y = r.xy(pad.GetPosition())
        if not (r.X0 <= x <= r.X1 and r.Y0 <= y <= r.Y1):
            return []
        return [r.grid_index(layer, x, y) for layer, native in enumerate(r.LAYERS)
                if pad.IsOnLayer(native)]

    def search(starts, goals, net):
        if not starts or not goals:
            return None, 0
        cells = [divmod(i % r.SIZE, r.NX) for i in goals]
        xmin, xmax = min(x for y, x in cells), max(x for y, x in cells)
        ymin, ymax = min(y for y, x in cells), max(y for y, x in cells)
        goal_layers = {i//r.SIZE for i in goals}
        def h(index):
            layer, cell = divmod(index, r.SIZE)
            gy, gx = divmod(cell, r.NX)
            return max(xmin-gx, 0, gx-xmax)+max(ymin-gy, 0, gy-ymax)+min(abs(layer-l) for l in goal_layers)*20
        costs = {i: 0 for i in starts if router.free(i//r.SIZE, i % r.SIZE, net)}
        parents = {i: None for i in costs}
        queue = [(h(i), 0, i) for i in costs]
        heapq.heapify(queue)
        expanded = 0
        while queue:
            _, cost, index = heapq.heappop(queue)
            if costs.get(index) != cost:
                continue
            if index in goals:
                path = []
                while index is not None:
                    path.append(index)
                    index = parents[index]
                return path[::-1], expanded
            expanded += 1
            if expanded > args.max_nodes:
                break
            layer, cell = divmod(index, r.SIZE)
            gy, gx = divmod(cell, r.NX)
            neighbours = []
            for dx, dy in ((-1, 0), (0, -1), (1, 0), (0, 1)):
                if 0 <= gx+dx < r.NX and 0 <= gy+dy < r.NY:
                    other = cell+dy*r.NX+dx
                    if router.free(layer, other, net):
                        neighbours.append((layer*r.SIZE+other, 1))
            if router.via_free(layer, cell, net):
                for other in (layer-1, layer+1):
                    if 0 <= other < len(r.LAYERS) and router.via_free(other, cell, net):
                        neighbours.append((other*r.SIZE+cell, 20))
            for other, weight in neighbours:
                new_cost = cost+weight
                if new_cost < costs.get(other, 10**12):
                    costs[other] = new_cost
                    parents[other] = index
                    heapq.heappush(queue, (new_cost+h(other), new_cost, other))
        return None, expanded

    def trace(a, b, layer, net):
        if a != b:
            router.trace(a, b, layer, net)

    def commit(path, start, end, net):
        layer, x, y = r.grid_point(path[0])
        trace(r.xy(start.GetPosition()), (x, y), layer, net)
        pending = direction = None
        for a, b in zip(path, path[1:]):
            la, ax, ay = r.grid_point(a)
            lb, bx, by = r.grid_point(b)
            if la != lb:
                if pending is not None:
                    trace(pending, (ax, ay), la, net)
                pending = None
                router.via((ax, ay), r.LAYERS[lb], r.LAYERS[la], net)
                direction = None
            else:
                new_direction = (round((bx-ax)/r.STEP), round((by-ay)/r.STEP))
                if pending is not None and direction != new_direction:
                    trace(pending, (ax, ay), la, net)
                    pending = None
                if pending is None:
                    pending = (ax, ay)
                direction = new_direction
        layer, x, y = r.grid_point(path[-1])
        if pending is not None:
            trace(pending, (x, y), layer, net)
        trace((x, y), r.xy(end.GetPosition()), layer, net)

    routes = []
    # Put the closest net first, then retain a deterministic name/pad order.
    def span(name):
        positions = [r.xy(q.GetPosition()) for q in pads_by_net[name]]
        return (max(x for x, y in positions)-min(x for x, y in positions) +
                max(y for x, y in positions)-min(y for x, y in positions), name)
    names = sorted(NETS, key=span)
    for name in names:
        pads = sorted(pads_by_net[name], key=lambda q: (q.GetParentFootprint().GetReference(), q.GetNumber()))
        anchor = pads[0]
        # Initial clusters choose one representative each. Copper may merge
        # multiple groups en route, so rebuild native connectivity each time.
        for pad in pads[1:]:
            board.BuildConnectivity()
            if identities(board, pad) == identities(board, anchor):
                continue
            net = pad.GetNetCode()
            goals = {cell for q in pads if identities(board, q) == identities(board, anchor) for cell in pad_cells(q)}
            path, expanded = search(pad_cells(pad), goals, net)
            if path:
                endpoint = next(q for q in pads if path[-1] in pad_cells(q))
                commit(path, pad, endpoint, net)
            entry = dict(net=name, source=[pad.GetParentFootprint().GetReference(), pad.GetNumber()],
                         routed=bool(path), expanded_nodes=expanded)
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
    report = dict(status='UNQUALIFIED_LOCAL_CONTROL_STUDY',
                  source_sha256=hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
                  board_sha256=hashlib.sha256(OUTPUT.read_bytes()).hexdigest(),
                  kicad_version=p.GetBuildVersion(), grid_mm=r.STEP,
                  width_mm=r.WIDTH, clearance_mm=r.CLEARANCE,
                  microvia_diameter_drill_mm=[r.VIA_D, r.VIA_HOLE],
                  max_nodes=args.max_nodes, allowed_nets=NETS, routes=routes,
                  tracks_and_vias=len(list(loaded.GetTracks())),
                  open_edges=loaded.GetConnectivity().GetUnconnectedCount(False))
    report['SPDX-License-Identifier'] = 'CERN-OHL-S-2.0'
    REPORT.write_text(json.dumps(report, indent=2, sort_keys=True)+'\n')
    print('Saved', report['open_edges'], 'open edges', flush=True)


if __name__ == '__main__':
    main()
