#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""ADR 0091 additive remaining-net exploration; accepted sources remain immutable.

The exact nearest-goal heuristic ignores obstacles. Native shape screening and
per-join filled-zone/pad-group guards still apply, and full DRC/independent
acceptance must follow. Outputs are restricted to the ignored Rev A build tree.
No electrical qualification, current-setting or fabrication release is implied.
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
from urllib.parse import quote
import uuid
from routing_contact_endpoints import end_cap_points
from routing_zone_targets import connected_polygons

ROOT = Path(__file__).resolve().parents[1]
STAGING = ROOT / 'hardware/coupon/rev-a/staging'
SOURCE = STAGING / 'led-native-control-trial-114mm.kicad_pcb'
BUILD = ROOT / 'hardware/coupon/rev-a/build'
OUTPUT = BUILD / 'native-control-search/trial.kicad_pcb'
REPORT = BUILD / 'native-control-search/search.json'
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


def review_paths(source, output, report, build=BUILD):
    source, output, report, build = (Path(x).resolve() for x in (source, output, report, build))
    if any(build not in path.parents or path == source for path in (output, report)):
        raise ValueError('Outputs must be distinct from source and inside the ignored Rev A build tree')
    if output == report:
        raise ValueError('Board and report outputs must be different files')
    return source, output, report


def rejection_snapshot_path(output, source, net, reference, pin):
    output, source = Path(output).resolve(), Path(source).resolve()
    directory = output.parent/(output.stem+'-rejected')
    filename = '-'.join(quote(str(x), safe='') for x in (net, reference, pin))+'.kicad_pcb'
    snapshot = directory/filename
    if source in (snapshot, snapshot.with_suffix('.json')):
        raise ValueError('Rejected-route snapshot would overwrite the source')
    return snapshot


def main():
    global p
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--max-nodes', type=int, default=120000)
    parser.add_argument('--through-vias',action='store_true',help='ADR0092 full-span 0.50/0.30 mm vias, screened on every layer')
    parser.add_argument('--zone-targets',action='store_true',help='Target individually copper-witnessed filled-plane components')
    parser.add_argument('--endpoint-radius',type=float,default=None,help='Limit actual copper targets around the current isolated pad')
    parser.add_argument('--preferred-layer', default=None, help='Prefer one physical layer; other layers cost five')
    parser.add_argument('--weight', type=float, default=2.0, help='Weighted A* search; no optimality claim')
    parser.add_argument('--source', type=Path, default=SOURCE)
    parser.add_argument('--output', type=Path, default=OUTPUT)
    parser.add_argument('--report', type=Path, default=REPORT)
    parser.add_argument('--nets', nargs='+', default=['SYS_I2C_SDA'])
    parser.add_argument('--heuristic', choices=('manhattan', 'empty-grid'), default='empty-grid',
                        help='Use exact goal distance or a precomputed layer-cost-aware lower bound')
    parser.add_argument('--reverse', action='store_true',
                        help='Search from the anchor group toward the isolated endpoint instead')
    parser.add_argument('--layers', nargs='+', default=['B.Cu','In4.Cu','In3.Cu','In2.Cu','In1.Cu','F.Cu'], help='Physical copper layer order, adjacent only')
    parser.add_argument('--native-grid', action='store_true',
                        help='Screen masked grid points and steps against exact native track/pad shapes')
    args = parser.parse_args()
    try:
        source, output, report_path = review_paths(args.source, args.output, args.report)
    except ValueError as error:
        parser.error(str(error))
    scope = SCOPE
    nets = sorted(set(args.nets))
    if not nets or args.max_nodes <= 0:
        parser.error('Select actual source nets and a positive node bound')
    output.parent.mkdir(parents=True, exist_ok=True)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    tool_paths = [Path(__file__), ROOT/'tools/routing_goal_distance.py',
                  ROOT/'tools/generate-colour-fanout-grid-trial.py',
                  ROOT/'tools/generate-paired-charger-114mm-routing.py',
                  ROOT/'tools/routing_clearance.py',ROOT/'tools/routing_contact_endpoints.py',ROOT/'tools/routing_zone_targets.py']
    tool_hashes = {str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest()
                   for path in tool_paths}
    import pcbnew as p
    r = module('grid', 'generate-colour-fanout-grid-trial.py')
    r.X0, r.Y0, r.X1, r.Y1 = .7, .7, 113.3, 31.8
    r.NX = round((r.X1-r.X0)/r.STEP)+1
    r.NY = round((r.Y1-r.Y0)/r.STEP)+1
    r.SIZE = r.NX*r.NY
    r.LAYERS = tuple({'B.Cu':p.B_Cu,'In4.Cu':p.In4_Cu,'In3.Cu':p.In3_Cu,'In2.Cu':p.In2_Cu,'In1.Cu':p.In1_Cu,'F.Cu':p.F_Cu}[name] for name in args.layers)
    r.LAYER_INDEX = {layer: index for index, layer in enumerate(r.LAYERS)}
    physical=['F.Cu','In1.Cu','In2.Cu','In3.Cu','In4.Cu','B.Cu']
    assert all(abs(physical.index(a)-physical.index(b))==1 or (args.through_vias and {a,b}=={'B.Cu','F.Cu'}) for a,b in zip(args.layers,args.layers[1:])), 'Physical adjacency or explicit whole-board through span required'
    all_copper=(p.F_Cu,p.In1_Cu,p.In2_Cu,p.In3_Cu,p.In4_Cu,p.B_Cu)
    via_cost=100 if len(r.LAYERS)==2 and set(args.layers)=={'B.Cu','F.Cu'} else 20
    through_centres=p.SHAPE_POLY_SET()

    def step_cost(layer):
        if r.LAYERS[layer]==p.In2_Cu:return None
        if args.preferred_layer:return 1 if args.layers[layer]==args.preferred_layer else 5
        return 5 if r.LAYERS[layer]==p.B_Cu else 1
    def via_geometry(a,b):
        if {a,b}=={p.F_Cu,p.B_Cu}:
            assert args.through_vias
            return p.VIATYPE_THROUGH,500000,300000
        central={a,b}=={p.In2_Cu,p.In3_Cu}
        return (p.VIATYPE_BURIED,500000,300000) if central else (p.VIATYPE_MICROVIA,300000,100000)
    def place_via(pos,top,bottom,net):
        kind,width,hole=via_geometry(top,bottom)
        v=p.PCB_VIA(board);v.SetPosition(r.point(*pos));v.SetViaType(kind);v.SetLayerPair(top,bottom);v.SetWidth(width);v.SetDrill(hole);v.SetNetCode(net);board.Add(v);router.occupy(v)
    source_digest = hashlib.sha256(source.read_bytes()).hexdigest()
    board = p.LoadBoard(str(source))
    if set(nets)-{q.GetNetname() for f in board.GetFootprints() for q in f.Pads()}:
        parser.error('Net absent from source')
    original_ids={t.m_Uuid.AsString() for t in board.GetTracks()}
    initial_tracks = len(original_ids)
    if args.through_vias:
        assert board.GetBoardPolygonOutlines(through_centres,False)
        through_centres.Inflate(-751000,p.CORNER_STRATEGY_ROUND_ALL_CORNERS,1000)
    router = r.Router(board)
    router.via=place_via
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

    bins = defaultdict(list)
    def cells(box, gap=0):
        return [(x,y) for x in range((box.GetX()-gap)//1000000,(box.GetRight()+gap)//1000000+1)
                for y in range((box.GetY()-gap)//1000000,(box.GetBottom()+gap)//1000000+1)]
    def rebuild_bins():
        bins.clear()
        for item in list(board.GetTracks()) + [pad for part in board.GetFootprints() for pad in part.Pads()]:
            for layer in all_copper:
                if item.IsOnLayer(layer):
                    for cell in cells(item.GetBoundingBox(), p.FromMM(.201)):
                        bins[(layer,*cell)].append(item)
    rebuild_bins()
    screen_statistics = []
    clearance = module('clearance', 'routing_clearance.py')

    def new_screen(net):
        def xy(index):
            _, x, y = r.grid_point(index)
            return x, y
        result = clearance.GridClearance(
            lambda i: router.free(i//r.SIZE, i % r.SIZE, net),
            lambda i: native_trace_clear(xy(i), xy(i), i//r.SIZE, net),
            lambda a, b: native_trace_clear(xy(a), xy(b), a//r.SIZE, net),
            enabled=args.native_grid)
        return result
    def native_trace_clear(origin, end, layer, net):
        track = p.PCB_TRACK(board)
        track.SetStart(r.point(*origin)); track.SetEnd(r.point(*end))
        track.SetWidth(p.FromMM(.2)); track.SetLayer(r.LAYERS[layer]); track.SetNetCode(net)
        others={item.m_Uuid.AsString():item for key in cells(track.GetBoundingBox()) for item in bins[(r.LAYERS[layer],*key)]}
        return not any(item.GetNetCode()!=net and track.GetEffectiveShape(r.LAYERS[layer]).Collide(item.GetEffectiveShape(r.LAYERS[layer]),p.FromMM(.2)-10)
                       for item in others.values())

    via_cache={}
    def native_via_clear(layer, other, cell, net):
        key=(min(layer,other),max(layer,other),cell,net)
        if key in via_cache:return via_cache[key]
        result=uncached_via_clear(layer,other,cell,net)
        via_cache[key]=result
        return result

    def uncached_via_clear(layer, other, cell, net):
        _, x, y = r.grid_point(layer*r.SIZE+cell)
        via = p.PCB_VIA(board)
        via.SetPosition(r.point(x,y))
        kind,width,hole=via_geometry(r.LAYERS[layer],r.LAYERS[other])
        via.SetViaType(kind)
        via.SetLayerPair(r.LAYERS[layer],r.LAYERS[other])
        via.SetWidth(width)
        via.SetDrill(hole)
        via.SetNetCode(net)
        natives=all_copper if kind==p.VIATYPE_THROUGH else (r.LAYERS[layer],r.LAYERS[other])
        if kind==p.VIATYPE_THROUGH and not through_centres.Contains(via.GetPosition()):return False
        for native in natives:
            others={item.m_Uuid.AsString():item for key in cells(via.GetBoundingBox()) for item in bins[(native,*key)]}
            if any(item.GetNetCode()!=net and via.GetEffectiveShape(native).Collide(item.GetEffectiveShape(native),p.FromMM(.2)-10)
                   for item in others.values()):
                return False
        if kind==p.VIATYPE_THROUGH:
            near={item.m_Uuid.AsString():item for native in natives for key in cells(via.GetBoundingBox()) for item in bins[(native,*key)]}
            for item in near.values():
                if isinstance(item,p.PCB_VIA) or (isinstance(item,p.PAD) and max(item.GetDrillSize().x,item.GetDrillSize().y)>0):
                    if via.GetEffectiveHoleShape().Collide(item.GetEffectiveHoleShape(),250000):return False
        return True

    endpoint_centre=None
    def group_endpoints(pad):
        # Each grid cell retains its exact native endpoint, so joining the grid
        # does not merely approach an existing track without touching it.
        result = {}
        actual={item.m_Uuid.AsString():item for item in list(board.GetTracks())+[q for f in board.GetFootprints() for q in f.Pads()]+list(board.Zones())}
        items = [actual[q.m_Uuid.AsString()] for q in board.GetConnectivity().GetConnectedItems(pad)] + [pad]
        items.sort(key=lambda q: (q.GetClass(), q.GetPosition().x,
                                  q.GetPosition().y, q.m_Uuid.AsString()))
        for item in items:
            if isinstance(item, p.PAD):
                # Start on actual land boundaries as well as the centre. A
                # full-width cap still overlaps the pad, while its new copper
                # need not inherit an existing neighbouring land's tight gap.
                centre=item.GetPosition();size=item.GetSize();angle=item.GetOrientation().AsRadians()
                positions=[centre]+[p.VECTOR2I(
                    centre.x+round(dx*math.cos(angle)-dy*math.sin(angle)),
                    centre.y+round(dx*math.sin(angle)+dy*math.cos(angle)))
                    for dx,dy in [(size.x/2,0),(-size.x/2,0),(0,size.y/2),(0,-size.y/2)]]
                layers = [i for i, native in enumerate(r.LAYERS) if item.IsOnLayer(native)]
            elif isinstance(item, p.PCB_VIA):
                positions = [item.GetPosition()]
                layers = [i for i, native in enumerate(r.LAYERS) if item.IsOnLayer(native)]
            elif isinstance(item, p.PCB_TRACK):
                if item.GetLayer() not in r.LAYER_INDEX:continue
                ax,ay=r.xy(item.GetStart()); bx,by=r.xy(item.GetEnd())
                steps=max(1,math.ceil(math.hypot(bx-ax,by-ay)/.1))
                positions=[r.point(ax+(bx-ax)*i/steps,ay+(by-ay)*i/steps) for i in range(steps+1)]
                # A full-width route cap may overlap the existing end cap while
                # its centre lies outside the old centreline. Retain 5 um overlap.
                positions += [p.VECTOR2I(*pt) for pt in end_cap_points((item.GetStart().x,item.GetStart().y),(item.GetEnd().x,item.GetEnd().y),item.GetWidth(),p.FromMM(r.WIDTH))]
                layers = [r.LAYER_INDEX[item.GetLayer()]]
            else:
                # Filled zones are excluded: an arbitrary zone anchor need not
                # lie in the connected filled region.
                continue
            for point in positions:
                x, y = r.xy(point)
                if args.endpoint_radius is not None and endpoint_centre is not None and math.dist((x,y),endpoint_centre)>args.endpoint_radius:continue
                # A valid pad may sit just outside the grid (e.g. y=0.65 mm).
                # Keep its existing 0.60 mm probe reach; candidate grid points
                # and every connecting lead still undergo the usual checks.
                if r.X0-.6 <= x <= r.X1+.6 and r.Y0-.6 <= y <= r.Y1+.6:
                    for layer in layers:
                        for dx in (range(-12,13) if isinstance(item,p.PAD) else range(-2,3)):
                            for dy in (range(-12,13) if isinstance(item,p.PAD) else range(-2,3)):
                                gx=round((x+dx*.05)/.05)*.05; gy=round((y+dy*.05)/.05)*.05
                                if not(r.X0<=gx<=r.X1 and r.Y0<=gy<=r.Y1):continue
                                index=r.grid_index(layer,gx,gy)
                                if index in result or not screen.node(index):continue
                                if native_trace_clear((x,y),(gx,gy),layer,pad.GetNetCode()):result[index]=(x,y)
        if args.zone_targets:
            centre=endpoint_centre or r.xy(pad.GetPosition())
            radius=args.endpoint_radius or 6.0
            for native,unit,zone_id,polygon,witness in connected_polygons(board,pad):
                if native not in r.LAYER_INDEX:continue
                layer=r.LAYER_INDEX[native];box=unit.BBox()
                # Sparse exact grid points, not arbitrary zone anchors. Each
                # polygon carries a same-group native copper-contact witness.
                for gy in range(max(0,round((centre[1]-radius-r.Y0)/r.STEP)),min(r.NY,round((centre[1]+radius-r.Y0)/r.STEP)+1),4):
                    for gx in range(max(0,round((centre[0]-radius-r.X0)/r.STEP)),min(r.NX,round((centre[0]+radius-r.X0)/r.STEP)+1),4):
                        x,y=r.X0+gx*r.STEP,r.Y0+gy*r.STEP
                        if math.dist((x,y),centre)>radius:continue
                        index=layer*r.SIZE+gy*r.NX+gx
                        if index in result or not unit.Contains(r.point(x,y)) or not screen.node(index):continue
                        result[index]=(x,y)
        return result

    heuristic_storage_bytes = 0

    def search(starts, goals, net):
        nonlocal heuristic_storage_bytes
        if not starts or not goals:
            return None, 0
        distance = module('distance', 'routing_goal_distance.py')
        if args.heuristic == 'empty-grid':
            field = distance.EmptyGridGoals(r.NX, r.NY,
                [step_cost(i) for i in range(len(r.LAYERS))],
                via_cost, ((i % r.SIZE % r.NX, i % r.SIZE // r.NX, i // r.SIZE) for i in goals))
            heuristic_storage_bytes = max(heuristic_storage_bytes, field.storage_bytes)
            return search_with_heuristic(starts, goals, net, field.distance)
        goals_index = distance.ManhattanGoals(
            (i % r.SIZE % r.NX, i % r.SIZE // r.NX, i // r.SIZE * via_cost) for i in goals)
        def h(index):
            layer,cell=divmod(index,r.SIZE)
            gy,gx=divmod(cell,r.NX)
            return goals_index.distance((gx,gy,layer*via_cost))
        return search_with_heuristic(starts, goals, net, h)

    def search_with_heuristic(starts, goals, net, h):
        costs = {i: 0 for i in starts if screen.node(i)}
        parents = {i: None for i in costs}
        queue = [(args.weight*h(i), 0, i) for i in costs]
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
            for dx, dy in (() if step_cost(layer) is None else ((-1, 0), (0, -1), (1, 0), (0, 1))):
                if 0 <= gx+dx < r.NX and 0 <= gy+dy < r.NY:
                    other = cell+dy*r.NX+dx
                    if screen.step(index, layer*r.SIZE+other):
                        neighbours.append((layer*r.SIZE+other, step_cost(layer)))
            via_neighbours={layer-1,layer+1}
            if args.through_vias and r.LAYERS[layer] in (p.F_Cu,p.B_Cu):
                via_neighbours.update(i for i,native in enumerate(r.LAYERS) if native in (p.F_Cu,p.B_Cu) and i!=layer)
            for other in sorted(via_neighbours):
                if 0 <= other < len(r.LAYERS) and screen.node(other*r.SIZE+cell):
                    if native_via_clear(layer,other,cell,net):
                        weight=100 if {r.LAYERS[layer],r.LAYERS[other]}=={p.F_Cu,p.B_Cu} else 20
                        neighbours.append((other*r.SIZE+cell,weight))
            for other, weight in neighbours:
                new_cost = cost+weight
                if new_cost < costs.get(other, 10**12):
                    costs[other] = new_cost
                    parents[other] = index
                    heapq.heappush(queue, (new_cost+args.weight*h(other), new_cost, other))
        return None, expanded

    def trace(a, b, layer, net):
        if a != b:
            router.trace(a, b, layer, net)

    def commit(path, start, end, net):
        layer, x, y = r.grid_point(path[0])
        trace(start, (x, y), layer, net)
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
        trace((x, y), end, layer, net)

    routes = []
    def current_groups():
        seen, groups = set(), []
        for pads in pads_by_net.values():
            for pad in pads:
                if not pad.GetNetname():
                    continue
                identity = identities(board, pad)
                if identity not in seen:
                    seen.add(identity)
                    groups.append((pad, identity))
        return groups

    # Put the closest net first, then retain a deterministic name/pad order.
    def span(name):
        positions = [r.xy(q.GetPosition()) for q in pads_by_net[name]]
        return (max(x for x, y in positions)-min(x for x, y in positions) +
                max(y for x, y in positions)-min(y for x, y in positions), name)
    if set(nets)-set(pads_by_net):
        parser.error('Selected control net is absent from the source board')
    names = sorted(nets, key=span)
    for name in names:
        pads = sorted(pads_by_net[name], key=lambda q: (q.GetParentFootprint().GetReference(), q.GetNumber()))
        anchor = max(pads,key=lambda q:len(identities(board,q)))
        # Initial clusters choose one representative each. Copper may merge
        # multiple groups en route, so rebuild native connectivity each time.
        for pad in pads:
            board.BuildConnectivity()
            if identities(board, pad) == identities(board, anchor):
                continue
            net = pad.GetNetCode()
            # Geometry caches are scoped to this immutable transaction only.
            print('SEARCH',name,pad.GetParentFootprint().GetReference(),pad.GetNumber(),flush=True)
            via_cache.clear()
            screen = new_screen(net)
            endpoint_centre=r.xy(pad.GetPosition())
            starts = group_endpoints(pad)
            targets = group_endpoints(anchor)
            goals = set(targets)
            if args.reverse:
                path, expanded = search(targets, set(starts), net)
                if path:
                    path.reverse()
            else:
                path, expanded = search(starts, goals, net)
            if path:
                assert path[0] in starts and path[-1] in targets
            screen_statistics.append(screen.statistics())
            rejection = None
            rejected_snapshot = None
            if path:
                groups_before = current_groups()
                tracks_before = {t.m_Uuid.AsString() for t in board.GetTracks()}
                mask_before = [mask[:] for mask in router.mask]
                commit(path, starts[path[0]], targets[path[-1]], net)
                # New signal copper can cut an existing plane's narrow
                # bridge despite passing clearance. Reject that transaction
                # before it becomes a target for subsequent searches.
                p.ZONE_FILLER(board).Fill(board.Zones())
                board.BuildConnectivity()
                if any(not group <= identities(board, q) for q, group in groups_before):
                    rejection = 'existing_pad_cluster_split_after_zone_refill'
                elif identities(board, pad) != identities(board, anchor):
                    rejection = 'native_endpoint_join_not_established'
                if rejection:
                    split=[]
                    for q,group in groups_before:
                        current=identities(board,q)
                        if not group<=current:
                            split.append(dict(net=q.GetNetname(),anchor=[q.GetParentFootprint().GetReference(),q.GetNumber()],lost=sorted(group-current)))
                    snapshot = rejection_snapshot_path(output, source, name,
                        pad.GetParentFootprint().GetReference(), pad.GetNumber())
                    snapshot.parent.mkdir(exist_ok=True)
                    p.SaveBoard(str(snapshot),board)
                    (snapshot.with_suffix('.json')).write_text(json.dumps(split,indent=2)+'\n')
                    rejected_snapshot = dict(path=str(snapshot.relative_to(ROOT)),
                        board_sha256=hashlib.sha256(snapshot.read_bytes()).hexdigest(),
                        physical_pad_groups=split)
                    print('SPLIT DETAILS',split,flush=True)
                    for item in list(board.GetTracks()):
                        if item.m_Uuid.AsString() not in tracks_before:
                            board.Remove(item)
                    router.mask = mask_before
                    p.ZONE_FILLER(board).Fill(board.Zones())
                    board.BuildConnectivity()
                    assert all(group <= identities(board, q) for q, group in groups_before)
                    path = None
            entry = dict(net=name, source=[pad.GetParentFootprint().GetReference(), pad.GetNumber()],
                         routed=bool(path), expanded_nodes=expanded,
                         search_outcome=('accepted_join' if path else rejection or
                             ('node_bound' if expanded > args.max_nodes else
                              'exhausted_grid' if expanded else 'no_usable_grid_endpoint')))
            if rejection:
                entry['rejected_reason'] = rejection
                entry['rejected_snapshot'] = rejected_snapshot
            routes.append(entry)
            if path:
                rebuild_bins()
                p.SaveBoard(str(output.with_name(output.stem+'-progress.kicad_pcb')),board)
            print(entry, flush=True)
    assert hashlib.sha256(source.read_bytes()).hexdigest() == source_digest, 'Source changed during search'
    assert all(hashlib.sha256((ROOT/name).read_bytes()).hexdigest() == digest
               for name, digest in tool_hashes.items()), 'Search code changed during execution'
    p.ZONE_FILLER(board).Fill(board.Zones())
    # Deterministic UUIDs only for this additive transaction; preserve old identities.
    for item in board.GetTracks():
        if item.m_Uuid.AsString() not in original_ids:
            row=(item.GetClass(),item.GetNetname(),item.GetStart().x,item.GetStart().y,item.GetEnd().x,item.GetEnd().y,item.GetLayer(),item.GetWidth(item.TopLayer()) if isinstance(item,p.PCB_VIA) else item.GetWidth())
            item.SetUuid(p.KIID(str(uuid.uuid5(scope,source_digest+repr(row)))))
    p.SaveBoard(str(output), board)
    helper = module('save', 'generate-paired-charger-114mm-routing.py')
    data = helper.sorted_native_tracks(output.read_text(), expected=len(list(board.GetTracks())))
    output.write_text(data)
    import shutil
    for ext in ('.kicad_pro','.kicad_dru'):
        shutil.copyfile(source.with_suffix(ext),output.with_suffix(ext))
    loaded = p.LoadBoard(str(output))
    report = dict(status='IGNORED_ADR0091_ROUTING_SEARCH',
                  source_sha256=source_digest,
                  search_tool_sha256=tool_hashes[str(Path(__file__).relative_to(ROOT))],
                  heuristic_sha256=tool_hashes['tools/routing_goal_distance.py'],
                  tool_source_sha256=tool_hashes,
                  search_weight=args.weight,
                  heuristic=('weighted_empty_grid_layer_costs' if args.heuristic == 'empty-grid'
                             else 'weighted_nearest_goal_manhattan'),
                  heuristic_storage_bytes=heuristic_storage_bytes,
                  reverse_search=args.reverse,
                  exact_native_grid_fallback=args.native_grid,
                  native_grid_statistics={key: sum(s[key] for s in screen_statistics)
                                          for key in ('native_point_queries', 'native_clear_masked_points',
                                                      'native_edge_queries', 'native_clear_masked_edges')},
                  fabrication_release_allowed=False,
                  board_sha256=hashlib.sha256(output.read_bytes()).hexdigest(),
                  kicad_version=p.GetBuildVersion(), grid_mm=r.STEP,
                  width_mm=r.WIDTH, clearance_mm=r.CLEARANCE,
                  microvia_diameter_drill_mm=[r.VIA_D, r.VIA_HOLE],
                  through_vias_enabled=args.through_vias, through_diameter_drill_mm=[.5,.3] if args.through_vias else None,
                  max_nodes=args.max_nodes, allowed_nets=nets, routes=routes,
                  connected_copper_endpoints=True,
                  preserve_clusters_after_each_join=True,
                  added_tracks_and_vias=len(list(loaded.GetTracks()))-initial_tracks,
                  tracks_and_vias=len(list(loaded.GetTracks())),
                  open_edges=loaded.GetConnectivity().GetUnconnectedCount(False))
    report['SPDX-License-Identifier'] = 'CERN-OHL-S-2.0'
    report_path.write_text(json.dumps(report, indent=2, sort_keys=True)+'\n')
    print('Saved', report['open_edges'], 'open edges', flush=True)


if __name__ == '__main__':
    main()
