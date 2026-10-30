#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Explore low-speed control routes without editing accepted PCB sources.

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
    parser.add_argument('--max-nodes', type=int, default=400000)
    parser.add_argument('--source', type=Path, default=SOURCE)
    parser.add_argument('--output', type=Path, default=OUTPUT)
    parser.add_argument('--report', type=Path, default=REPORT)
    parser.add_argument('--nets', nargs='+', default=['SYS_I2C_SDA'])
    parser.add_argument('--heuristic', choices=('manhattan', 'empty-grid'), default='manhattan',
                        help='Use exact goal distance or a precomputed layer-cost-aware lower bound')
    parser.add_argument('--reverse', action='store_true',
                        help='Search from the anchor group toward the isolated endpoint instead')
    parser.add_argument('--native-grid', action='store_true',
                        help='Screen masked grid points and steps against exact native track/pad shapes')
    args = parser.parse_args()
    try:
        source, output, report_path = review_paths(args.source, args.output, args.report)
    except ValueError as error:
        parser.error(str(error))
    scope = SCOPE
    allowed = set(NETS) | {'MODE_BOOT_N', 'ESP_EN', 'ROW_A0', 'ROW_A1', 'ROW_A2', 'ROW_A3',
        'SYS_I2C_SCL', 'SYS_I2C_SDA', 'GAUGE_I2C_SCL', 'GAUGE_I2C_SDA',
        'CHARGER_GATE_EN', 'CHARGER_EN2', 'DISPLAY_HEARTBEAT', 'USB_LOGIC_SENSE',
        'USB_CC_HIGH', 'USB_RAW_OUT1', 'USB_RAW_OUT2', 'ROW_ENABLE_N',
        'UART0_RX', 'UART0_TX_RAW', 'UART0_TX'}
    nets = sorted(set(args.nets))
    if not nets or set(nets)-allowed or args.max_nodes <= 0:
        parser.error('Select supported low-speed controls and a positive node bound')
    output.parent.mkdir(parents=True, exist_ok=True)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    tool_paths = [Path(__file__), ROOT/'tools/routing_goal_distance.py',
                  ROOT/'tools/generate-colour-fanout-grid-trial.py',
                  ROOT/'tools/generate-paired-charger-114mm-routing.py',
                  ROOT/'tools/routing_clearance.py']
    tool_hashes = {str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest()
                   for path in tool_paths}
    import pcbnew as p
    r = module('grid', 'generate-colour-fanout-grid-trial.py')
    r.X0, r.Y0, r.X1, r.Y1 = .7, .7, 113.3, 31.8
    r.NX = round((r.X1-r.X0)/r.STEP)+1
    r.NY = round((r.Y1-r.Y0)/r.STEP)+1
    r.SIZE = r.NX*r.NY
    r.LAYERS = (p.B_Cu, p.In4_Cu, p.In3_Cu, p.In2_Cu, p.In1_Cu, p.F_Cu)
    r.LAYER_INDEX = {layer: index for index, layer in enumerate(r.LAYERS)}
    source_digest = hashlib.sha256(source.read_bytes()).hexdigest()
    board = p.LoadBoard(str(source))
    initial_tracks = len(list(board.GetTracks()))
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

    bins = defaultdict(list)
    def cells(box, gap=0):
        return [(x,y) for x in range((box.GetX()-gap)//1000000,(box.GetRight()+gap)//1000000+1)
                for y in range((box.GetY()-gap)//1000000,(box.GetBottom()+gap)//1000000+1)]
    def rebuild_bins():
        bins.clear()
        for item in list(board.GetTracks()) + [pad for part in board.GetFootprints() for pad in part.Pads()]:
            for layer in r.LAYERS:
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

    def native_via_clear(layer, other, cell, net):
        _, x, y = r.grid_point(layer*r.SIZE+cell)
        via = p.PCB_VIA(board)
        via.SetPosition(r.point(x,y))
        via.SetViaType(p.VIATYPE_MICROVIA)
        via.SetLayerPair(r.LAYERS[layer],r.LAYERS[other])
        via.SetWidth(p.FromMM(.3))
        via.SetDrill(p.FromMM(.1))
        via.SetNetCode(net)
        for native in (r.LAYERS[layer],r.LAYERS[other]):
            others={item.m_Uuid.AsString():item for key in cells(via.GetBoundingBox()) for item in bins[(native,*key)]}
            if any(item.GetNetCode()!=net and via.GetEffectiveShape(native).Collide(item.GetEffectiveShape(native),p.FromMM(.2)-10)
                   for item in others.values()):
                return False
        return True

    def group_endpoints(pad):
        # Each grid cell retains its exact native endpoint, so joining the grid
        # does not merely approach an existing track without touching it.
        result = {}
        items = list(board.GetConnectivity().GetConnectedItems(pad)) + [pad]
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
                ax,ay=r.xy(item.GetStart()); bx,by=r.xy(item.GetEnd())
                steps=max(1,math.ceil(math.hypot(bx-ax,by-ay)/.1))
                positions=[r.point(ax+(bx-ax)*i/steps,ay+(by-ay)*i/steps) for i in range(steps+1)]
                layers = [r.LAYER_INDEX[item.GetLayer()]]
            else:
                # Filled zones are excluded: an arbitrary zone anchor need not
                # lie in the connected filled region.
                continue
            for point in positions:
                x, y = r.xy(point)
                # A valid pad may sit just outside the grid (e.g. y=0.65 mm).
                # Keep its existing 0.60 mm probe reach; candidate grid points
                # and every connecting lead still undergo the usual checks.
                if r.X0-.6 <= x <= r.X1+.6 and r.Y0-.6 <= y <= r.Y1+.6:
                    for layer in layers:
                        for dx in range(-12,13):
                            for dy in range(-12,13):
                                gx=round((x+dx*.05)/.05)*.05; gy=round((y+dy*.05)/.05)*.05
                                if not(r.X0<=gx<=r.X1 and r.Y0<=gy<=r.Y1):continue
                                index=r.grid_index(layer,gx,gy)
                                if index in result or not screen.node(index):continue
                                if native_trace_clear((x,y),(gx,gy),layer,pad.GetNetCode()):result[index]=(x,y)
        return result

    heuristic_storage_bytes = 0

    def search(starts, goals, net):
        nonlocal heuristic_storage_bytes
        if not starts or not goals:
            return None, 0
        distance = module('distance', 'routing_goal_distance.py')
        if args.heuristic == 'empty-grid':
            field = distance.EmptyGridGoals(r.NX, r.NY,
                [5 if layer == p.B_Cu else None if layer == p.In2_Cu else 1 for layer in r.LAYERS],
                20, ((i % r.SIZE % r.NX, i % r.SIZE // r.NX, i // r.SIZE) for i in goals))
            heuristic_storage_bytes = max(heuristic_storage_bytes, field.storage_bytes)
            return search_with_heuristic(starts, goals, net, field.distance)
        goals_index = distance.ManhattanGoals(
            (i % r.SIZE % r.NX, i % r.SIZE // r.NX, i // r.SIZE * 20) for i in goals)
        def h(index):
            layer,cell=divmod(index,r.SIZE)
            gy,gx=divmod(cell,r.NX)
            return goals_index.distance((gx,gy,layer*20))
        return search_with_heuristic(starts, goals, net, h)

    def search_with_heuristic(starts, goals, net, h):
        costs = {i: 0 for i in starts if screen.node(i)}
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
            for dx, dy in (() if r.LAYERS[layer] == p.In2_Cu else ((-1, 0), (0, -1), (1, 0), (0, 1))):
                if 0 <= gx+dx < r.NX and 0 <= gy+dy < r.NY:
                    other = cell+dy*r.NX+dx
                    if screen.step(index, layer*r.SIZE+other):
                        neighbours.append((layer*r.SIZE+other, 5 if r.LAYERS[layer] == p.B_Cu else 1))
            for other in (layer-1, layer+1):
                if 0 <= other < len(r.LAYERS) and screen.node(other*r.SIZE+cell):
                    if ((router.via_free(layer,cell,net) and router.via_free(other,cell,net)) or
                            native_via_clear(layer,other,cell,net)):
                        neighbours.append((other*r.SIZE+cell,20))
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
        anchor = pads[0]
        # Initial clusters choose one representative each. Copper may merge
        # multiple groups en route, so rebuild native connectivity each time.
        for pad in pads[1:]:
            board.BuildConnectivity()
            if identities(board, pad) == identities(board, anchor):
                continue
            net = pad.GetNetCode()
            # Geometry caches are scoped to this immutable transaction only.
            screen = new_screen(net)
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
            if path: rebuild_bins()
            print(entry, flush=True)
    assert hashlib.sha256(source.read_bytes()).hexdigest() == source_digest, 'Source changed during search'
    assert all(hashlib.sha256((ROOT/name).read_bytes()).hexdigest() == digest
               for name, digest in tool_hashes.items()), 'Search code changed during execution'
    p.ZONE_FILLER(board).Fill(board.Zones())
    p.SaveBoard(str(output), board)
    helper = module('save', 'generate-paired-charger-114mm-routing.py')
    data = helper.sorted_native_tracks(output.read_text(), expected=len(list(board.GetTracks())))
    sequence = iter(range(data.count('(uuid "')))
    data = re.sub(r'\(uuid "[0-9a-f-]{36}"\)',
                  lambda _: '(uuid "'+str(uuid.uuid5(scope, str(next(sequence))))+'")', data)
    output.write_text(data)
    loaded = p.LoadBoard(str(output))
    report = dict(status='UNQUALIFIED_LOCAL_CONTROL_STUDY',
                  source_sha256=source_digest,
                  search_tool_sha256=tool_hashes[str(Path(__file__).relative_to(ROOT))],
                  heuristic_sha256=tool_hashes['tools/routing_goal_distance.py'],
                  tool_source_sha256=tool_hashes,
                  heuristic=('exact_empty_grid_layer_costs' if args.heuristic == 'empty-grid'
                             else 'exact_nearest_goal_manhattan_with_minimum_layer_cost'),
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
