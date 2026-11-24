#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Read-only ADR 0119 R6 placement/capture screen; never saves a PCB."""
import pcbnew as p, runpy, json, math, sys, hashlib, argparse
from pathlib import Path
from collections import defaultdict, Counter

def main():
    root = Path(__file__).resolve().parents[1]
    folder = root / 'hardware/coupon/rev-a/build/r6-locality'
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--capture', choices=['full', 'outer', 'none'], default='full')
    args = parser.parse_args()
    out = args.output.resolve()
    assert (root / 'hardware/coupon/rev-a/build').resolve() in out.parents and out.suffix == '.json'
    source = root / 'hardware/coupon/rev-a/staging/led-rse-corrected-routing-trial-114mm.kicad_pcb'
    source_sha = '3967bb66e89e0005f6859ce78a766b4536d06883b76fce130e75a6fdeefaf96e'
    assert hashlib.sha256(source.read_bytes()).hexdigest() == source_sha
    b = p.LoadBoard(str(source))
    parts = {f.GetReference(): f for f in b.GetFootprints()}
    f = parts['R6']
    assert f.GetField('MPN').GetText() == 'ERJ2RKF1001X'
    h = runpy.run_path(str(root / 'tools/screen-converter-inductor-locality.py'))
    g = h['geometry']
    cells = h['cells']
    box = h['native_box']
    courts = h['courtyards']
    overlap = h['overlap']
    retire = {'430f9728-db9a-55c3-bc3a-c15f77000cfa', '37dd7533-43cb-5304-82c1-189a29f31d7b', '2538e05f-0e95-52a5-813a-3f61b41300a2', '750bfacf-ba86-5c75-9580-95e8142b8407', '42fd1a41-569a-505d-a7f3-ff8a9a5bd1b8', 'b0d25ba3-c6d5-5224-8d60-741e3760ff1a'}
    fixed = []
    fixed_bins = defaultdict(list)
    for part in b.GetFootprints():
        if part.GetReference() == 'R6' or part.GetLayer() != p.B_Cu:
            continue
        for poly in courts(part):
            z = g.bounds(poly)
            i = len(fixed)
            fixed.append((part.GetReference(), z, poly))
            for c in cells(z):
                fixed_bins[c].append(i)
    items = [t for t in b.GetTracks() if t.m_Uuid.AsString() not in retire] + [q for part in b.GetFootprints() if part.GetReference() != 'R6' for q in part.Pads()]
    layers = list(b.GetEnabledLayers().CuStack())
    indexed = {layer: [] for layer in layers}
    bins = {layer: defaultdict(list) for layer in layers}
    for t in items:
        for layer in layers:
            if not t.IsOnLayer(layer):
                continue
            i = len(indexed[layer])
            indexed[layer].append((t.GetNetCode(), t.GetEffectiveShape(layer), t.m_Uuid.AsString()))
            for c in cells(box(t.GetBoundingBox())):
                bins[layer][c].append(i)

    def blockers(shape, rect, layer, net):
        rect.Inflate(200000)
        ids = {i for c in cells(box(rect)) for i in bins[layer][c]}
        return [indexed[layer][i][2] for i in ids if indexed[layer][i][0] != net and shape.Collide(indexed[layer][i][1], 199990)]
    point = lambda a: p.VECTOR2I(*a)
    counts = Counter()
    clear = []
    old = p.VECTOR2I(f.GetPosition())
    gatepads = [q for q in parts['PAIR01'].Pads() if q.GetNumber() in {'5', '6'}]
    tops = [(b.GetLayerID('In1.Cu'), b.GetLayerID('In2.Cu'), p.VIATYPE_MICROVIA, 300000, 100000), (b.GetLayerID('In2.Cu'), b.GetLayerID('In3.Cu'), p.VIATYPE_BURIED, 500000, 300000), (b.GetLayerID('In3.Cu'), b.GetLayerID('In4.Cu'), p.VIATYPE_MICROVIA, 300000, 100000), (b.GetLayerID('In4.Cu'), p.B_Cu, p.VIATYPE_MICROVIA, 300000, 100000)]
    for angle in [0, 90, 180, 270]:
        f.SetPosition(old)
        f.SetOrientationDegrees(angle)
        poly = courts(f)[0]
        offset = [(x - old.x, y - old.y) for x, y in poly]
        for x in range(71000000, 79000001, 50000):
            for y in range(800000, 5600001, 50000):
                counts['sampled'] += 1
                poly = [(x + a, y + c) for a, c in offset]
                z = g.bounds(poly)
                ids = {i for c in cells(z) for i in fixed_bins[c]}
                if any((overlap(z, fixed[i][1]) and g.intersects(poly, fixed[i][2]) for i in ids)):
                    counts['courtyard'] += 1
                    continue
                f.SetPosition(p.VECTOR2I(x, y))
                pads = {q.GetNumber(): q for q in f.Pads()}
                bad = False
                for q in pads.values():
                    if q.GetBoundingBox().GetY() < 500000 or blockers(q.GetEffectiveShape(p.B_Cu), q.GetBoundingBox(), p.B_Cu, q.GetNetCode()):
                        bad = True
                        break
                if bad:
                    counts['pad_copper'] += 1
                    continue
                vpos = pads['1'].GetPosition()
                vias = []
                for top, bottom, kind, width, drill in tops if args.capture == 'full' else tops[-1:] if args.capture == 'outer' else []:
                    v = p.PCB_VIA(b)
                    v.SetPosition(vpos)
                    v.SetViaType(kind)
                    v.SetLayerPair(top, bottom)
                    v.SetWidth(width)
                    v.SetDrill(drill)
                    v.SetNetCode(pads['1'].GetNetCode())
                    vias.append(v)
                    if any((blockers(v.GetEffectiveShape(layer), v.GetBoundingBox(), layer, v.GetNetCode()) for layer in [top, bottom])):
                        bad = True
                        break
                if bad:
                    counts['via_copper'] += 1
                    continue
                counts['pad_and_via_clear'] += 1
                start = tuple(pads['2'].GetPosition())
                paths = []
                for target in gatepads:
                    end = tuple(target.GetPosition())
                    mid = [end, (end[0], start[1]), (start[0], end[1])]
                    for q in mid:
                        pts = [start, end] if q == end else [start, q, end]
                        pts = [v for i, v in enumerate(pts) if i == 0 or v != pts[i - 1]]
                        if sum((math.dist(a, c) for a, c in zip(pts, pts[1:]))) > 3000000:
                            continue
                        okay = True
                        for a, c in zip(pts, pts[1:]):
                            t = p.PCB_TRACK(b)
                            t.SetStart(point(a))
                            t.SetEnd(point(c))
                            t.SetLayer(p.B_Cu)
                            t.SetWidth(200000)
                            t.SetNetCode(pads['2'].GetNetCode())
                            if blockers(t.GetEffectiveShape(p.B_Cu), t.GetBoundingBox(), p.B_Cu, t.GetNetCode()) or t.GetEffectiveShape(p.B_Cu).Collide(pads['1'].GetEffectiveShape(p.B_Cu), 199990):
                                okay = False
                                break
                        if okay:
                            paths.append(pts)
                if paths:
                    counts['gate_and_supply_shape_clear'] += 1
                    if len(clear) < 100:
                        clear.append(dict(position_iu=[x, y], angle_deg=angle, via_position_iu=list(vpos), gate_path_iu=min(paths, key=lambda z: sum((math.dist(a, c) for a, c in zip(z, z[1:]))))))
        print(angle, dict(counts), flush=True)
    f.SetPosition(old)
    f.SetOrientationDegrees(180)
    if args.capture == 'none' and 'pad_and_via_clear' in counts:
        counts['pad_clear_without_capture'] = counts.pop('pad_and_via_clear')
    assert hashlib.sha256(source.read_bytes()).hexdigest() == source_sha
    out.parent.mkdir(parents=True, exist_ok=True)
    report = {'SPDX-License-Identifier': 'CERN-OHL-S-2.0', 'status': 'UNSELECTED_READ_ONLY_FINITE_SCREEN', 'source_sha256': source_sha, 'source_unchanged': True, 'capture_screen': args.capture, 'counts': dict(counts), 'clear_poses': clear, 'candidate_retired_uuids': sorted(retire), 'grid_step_iu': 50000, 'pose_bounds_iu': [[71000000, 800000], [79000000, 5600000]], 'angles_deg': [0, 90, 180, 270], 'clearance_iu': 200000, 'copper_edge_iu': 500000, 'gate_path_limit_iu': 3000000, 'tool_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(), 'fabrication_release_allowed': False, 'limitations': ['Finite grid and direct/orthogonal gate templates only', 'Filled zones, hole clearance, refills, group retention and full DRC not screened', 'No PCB saved or source modified', 'Without-capture diagnostics do not constitute a supply proposal']}
    out.write_text(json.dumps(report, indent=2, sort_keys=True) + '\n')
if __name__ == '__main__':
    main()
