#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Replay the unselected ADR 0075/0076 supply and obsolete-copper experiment.

First generate an ADR 0074 --scope pair probe. This tool only writes build/;
its exact retirement catalog grants no exception to the canonical checker.
"""
import argparse
from collections import Counter, defaultdict
import hashlib
import json
import math
from pathlib import Path
import runpy
import shutil
import uuid
import pcbnew as p

ROOT = Path(__file__).resolve().parents[1]
BUILD = ROOT/'hardware/coupon/rev-a/build'
PLAN = ROOT/'mechanical/review/vled-supply-cleanup-plan-2026-11-01.json'
PLAN_SHA256 = '2394f14ceda5e7616889cc791eee8f5865984be3d4cdd44a6979b0aa6fd816e1'
PAIR_SHA256 = '9e244a34515d42cf3b5bdf7b1bba52c55fcdd4ce319c8fbeb86159c1f202828b'
ACCEPTED_SHA256 = '3451177253a021d8706ff818696212afabf539a108f15ef9e5d6921e46435acc'
C = runpy.run_path(str(ROOT/'tools/check-routing-progress-trial.py'))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def inventory(board):
    return Counter(C['signature'](board, item) for item in board.GetTracks())


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--source', type=Path, required=True, help='Exact ADR 0074 pair probe')
    ap.add_argument('--plan', type=Path, default=PLAN)
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    source, plan_path, output = args.source.resolve(), args.plan.resolve(), args.output.resolve()
    assert BUILD.resolve() in output.parents and output.suffix == '.kicad_pcb', 'Output must be an ignored build PCB'
    assert output != source, 'Output must not overwrite input'
    assert sha(source) == PAIR_SHA256, 'Exact pair probe required'
    assert sha(plan_path) == PLAN_SHA256, 'Exact unselected geometry catalog required'
    assert sha(C['OUTPUT']) == ACCEPTED_SHA256, 'Accepted 58-edge reference changed'
    plan = json.loads(plan_path.read_text())
    assert plan['pair_source_sha256'] == PAIR_SHA256
    assert plan['accepted_source_sha256'] == ACCEPTED_SHA256
    accepted, frozen, board = [p.LoadBoard(str(path)) for path in (C['OUTPUT'], C['SOURCE'], source)]
    before, original, pair = map(inventory, (accepted, frozen, board))
    retired = Counter(tuple(row['signature']) for row in plan['removed_copper'])
    added = Counter(map(tuple, plan['added_supply_copper']))
    assert len(retired) == 23 and sum(retired.values()) == 23
    assert len(added) == 59 and sum(added.values()) == 59
    assert not retired-before and not retired-pair
    origins = Counter()
    for row in plan['removed_copper']:
        key = tuple(row['signature'])
        origin = 'frozen_215_source' if original[key] else 'accepted_addition'
        assert row['origin'] == origin
        origins[origin] += 1
    assert origins == {'frozen_215_source': 8, 'accepted_addition': 15}
    assert not added & retired and not added & pair
    layers = {board.GetLayerName(layer): layer for layer in board.GetEnabledLayers().CuStack()}
    stack = list(layers)
    lengths = defaultdict(float)
    for row, count in added.items():
        assert count == 1 and row[1] in ('+SYS_APP_IN_DRAFT', 'VLED')
        if row[0] == 'track':
            _, net, ax, ay, bx, by, layer, width = row
            assert width == 200000 and (ax, ay) != (bx, by)
            item = p.PCB_TRACK(board)
            item.SetStart(p.VECTOR2I(ax, ay)); item.SetEnd(p.VECTOR2I(bx, by))
            item.SetLayer(layers[layer]); item.SetWidth(width)
            lengths[net] += math.dist((ax, ay), (bx, by))/1e6
        else:
            _, net, x, y, top, bottom, diameter, drill = row
            assert row[0] == 'via' and (diameter, drill) == (300000, 100000)
            assert abs(stack.index(top)-stack.index(bottom)) == 1
            item = p.PCB_VIA(board)
            item.SetPosition(p.VECTOR2I(x, y)); item.SetViaType(p.VIATYPE_MICROVIA)
            item.SetLayerPair(layers[top], layers[bottom])
            item.SetWidth(diameter); item.SetDrill(drill)
        item.SetNetCode(board.FindNet(net).GetNetCode())
        item.SetUuid(p.KIID(str(uuid.uuid5(uuid.NAMESPACE_URL, 'rgb-badge:ADR0075:'+repr(row)))))
        board.Add(item)
    assert all(length <= 25 for length in lengths.values())
    held = []
    remaining = retired.copy()
    for item in list(board.GetTracks()):
        key = C['signature'](board, item)
        if remaining[key]:
            remaining[key] -= 1
            board.Remove(item); held.append(item)
    assert not +remaining
    assert inventory(board) == pair-retired+added, 'Unexpected copper change'
    oldparts = {f.GetReference(): f for f in accepted.GetFootprints()}
    parts = {f.GetReference(): f for f in board.GetFootprints()}
    assert set(oldparts) == set(parts) and len(parts) == 483
    moved = []
    for ref, old in oldparts.items():
        new = parts[ref]
        assert new.GetFPIDAsString() == old.GetFPIDAsString()
        assert new.GetLayer() == old.GetLayer()
        assert Counter(map(C['local_pad_signature'], new.Pads())) == Counter(map(C['local_pad_signature'], old.Pads()))
        assert sorted((q.GetName(), q.GetText()) for q in new.GetFields()) == sorted((q.GetName(), q.GetText()) for q in old.GetFields())
        if (new.GetPosition(), new.GetOrientation().AsDegrees()) != (old.GetPosition(), old.GetOrientation().AsDegrees()):
            moved.append(ref)
    assert sorted(moved) == ['L2', 'U37']
    assert (parts['U37'].GetPosition().x, parts['U37'].GetPosition().y, parts['U37'].GetOrientation().AsDegrees()) == (45500000,17500000,0)
    assert (parts['L2'].GetPosition().x, parts['L2'].GetPosition().y, parts['L2'].GetOrientation().AsDegrees()) == (49550000,17500000,-90)
    assert Counter(C['zone_signature'](accepted, z) for z in accepted.Zones()) == Counter(C['zone_signature'](board, z) for z in board.Zones())
    prior = {}
    for f in accepted.GetFootprints():
        for pad in f.Pads():
            if pad.GetNetname():
                prior.setdefault(C['physical_cluster'](accepted, pad), C['physical_identity'](pad))
    assert len(prior) == 246
    lookup = {C['physical_identity'](q): q for f in board.GetFootprints() for q in f.Pads()}
    output.parent.mkdir(parents=True, exist_ok=True)
    sorter = runpy.run_path(str(ROOT/'tools/generate-paired-charger-114mm-routing.py'))['sorted_native_tracks']
    fills = []
    for iteration in range(3):
        p.ZONE_FILLER(board).Fill(board.Zones()); board.BuildConnectivity()
        assert all(group <= C['physical_cluster'](board, lookup[key]) for group, key in prior.items()), 'Previous pad group split'
        opens = board.GetConnectivity().GetUnconnectedCount(False)
        assert opens == 56
        p.SaveBoard(str(output), board)
        output.write_text(sorter(output.read_text(), expected=len(list(board.GetTracks()))))
        fills.append(dict(fill=iteration+1, native_opens=opens, all_246_old_groups_preserved=True, board_sha256=sha(output)))
    assert len({row['board_sha256'] for row in fills}) == 1, 'Filled PCB bytes unstable'
    output.parent.mkdir(parents=True, exist_ok=True)
    p.SaveBoard(str(output), board)
    sorter = runpy.run_path(str(ROOT/'tools/generate-paired-charger-114mm-routing.py'))['sorted_native_tracks']
    output.write_text(sorter(output.read_text(), expected=len(list(board.GetTracks()))))
    for suffix in ('.kicad_pro', '.kicad_dru'):
        assert source.with_suffix(suffix).read_bytes() == C['OUTPUT'].with_suffix(suffix).read_bytes()
        shutil.copyfile(source.with_suffix(suffix), output.with_suffix(suffix))
    (output.parent/'fp-lib-table').write_text('(fp_lib_table (lib (name "rgb-badge-coupon") (type "KiCad") (uri "'+str(ROOT/'hardware/coupon/rev-a/footprints/rgb-badge-coupon.pretty')+'") (options "") (descr "Unselected geometry probe")))\n')
    reporter = runpy.run_path(str(ROOT/'tools/report-coupon-board-connectivity.py'))
    opens = reporter['open_edges_by_net'](output)
    assert opens['native_open_edges'] == opens['pad_cluster_open_edges'] == 56
    report = dict(status='UNSELECTED_SUPPLY_RESTORATION_AND_EXACT_CLEANUP_NOT_POWER_STAGE_ACCEPTANCE',
                  source_sha256=PAIR_SHA256, accepted_source_sha256=ACCEPTED_SHA256, plan_sha256=sha(plan_path),
                  tool_sha256=sha(Path(__file__)), board_sha256=sha(output), kicad_version=p.GetBuildVersion(),
                  added_supply_items=sum(added.values()), removed_items=sum(retired.values()), removal_origins=dict(origins),
                  supply_track_length_mm=dict(lengths), only_U37_L2_poses_changed=True, fills=fills, open_edges=opens,
                  all_other_copper_retained=True, accepted_source_unchanged=sha(C['OUTPUT']) == ACCEPTED_SHA256,
                  fabrication_release_allowed=False)
    report['SPDX-License-Identifier'] = 'CERN-OHL-S-2.0'
    output.with_suffix('.json').write_text(json.dumps(report, indent=2, sort_keys=True)+'\n')
    print('Unselected replay:', opens['native_open_edges'], 'native /', opens['pad_cluster_open_edges'], 'physical opens;', len(retired), 'exact removals', flush=True)


if __name__ == '__main__':
    main()
