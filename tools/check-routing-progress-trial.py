#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Independently verify retained source copper, physical groups and full DRC."""
import argparse
from collections import Counter
import hashlib
import importlib.util
import json
from collections import defaultdict
from pathlib import Path
import pcbnew as p

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT/'hardware/coupon/rev-a/staging/led-native-control-trial-114mm.kicad_pcb'
OUTPUT = ROOT/'hardware/coupon/rev-a/staging/led-routing-progress-trial-114mm.kicad_pcb'
PLAN = ROOT/'mechanical/review/routing-progress-plan.json'
MANIFEST = ROOT/'mechanical/review/routing-progress-trial.json'



def module(name, filename):
    spec = importlib.util.spec_from_file_location(name, ROOT/'tools'/filename)
    result = importlib.util.module_from_spec(spec); spec.loader.exec_module(result)
    return result


def signature(board, item):
    if isinstance(item, p.PCB_VIA):
        return ('via', item.GetNetname(), item.GetPosition().x, item.GetPosition().y,
                board.GetLayerName(item.TopLayer()), board.GetLayerName(item.BottomLayer()),
                item.GetWidth(item.TopLayer()), item.GetDrillValue())
    return ('track', item.GetNetname(), item.GetStart().x, item.GetStart().y,
            item.GetEnd().x, item.GetEnd().y, board.GetLayerName(item.GetLayer()), item.GetWidth())


def physical_identity(pad):
    pos=pad.GetFPRelativePosition()
    return (pad.GetParentFootprint().GetReference(),pad.GetNumber(),pos.x,pos.y)


def physical_cluster(board,pad):
    return frozenset(physical_identity(q) for q in board.GetConnectivity().GetConnectedItems(pad)
                     if isinstance(q,p.PAD))


def local_pad_signature(pad):
    pos=pad.GetFPRelativePosition();drill=pad.GetDrillSize();offset=pad.GetOffset()
    return (pad.GetNumber(),pad.GetNetname(),pos.x,pos.y,pad.GetSize().x,pad.GetSize().y,
            pad.GetFPRelativeOrientation().AsDegrees()%360,pad.GetShape(),tuple(pad.GetLayerSet().Seq()),
            pad.GetAttribute(),pad.GetDrillShape(),drill.x,drill.y,offset.x,offset.y,
            pad.GetRoundRectRadiusRatio(),pad.GetChamferRectRatio(),pad.GetChamferPositions(),
            pad.GetLocalClearance(),pad.GetLocalSolderMaskMargin(),pad.GetLocalSolderPasteMargin(),
            pad.GetLocalSolderPasteMarginRatio(),pad.GetPinFunction())


def validate_geometry(old, new, plan):
    old_parts = {f.GetReference(): f for f in old.GetFootprints()}
    new_parts = {f.GetReference(): f for f in new.GetFootprints()}
    assert old_parts.keys() == new_parts.keys() and len(new_parts) == 483, 'Component inventory changed'
    poses={entry['reference']:entry for entry in plan['placements']}
    assert len(poses)==len(plan['placements'])
    allowed_moves={'C51','C55','C71','R109','R3','R38','R39','R5','R63','R70','R71','R8','R81','R84','R85','R87','R88','R89','R97','R99'}
    assert poses.keys()<=allowed_moves
    lookup = {}
    for ref, part in old_parts.items():
        other = new_parts[ref]
        assert (part.GetValue(),part.GetFPIDAsString(),part.GetLayer()) == (
            other.GetValue(),other.GetFPIDAsString(),other.GetLayer()), ('Part identity changed',ref)
        if ref in poses:
            entry=poses[ref]
            assert [part.GetPosition().x,part.GetPosition().y]==entry['old_position_iu']
            assert part.GetOrientation().AsDegrees()==entry['old_angle_deg']
            assert [other.GetPosition().x,other.GetPosition().y]==entry['new_position_iu']
            assert other.GetOrientation().AsDegrees()==entry['new_angle_deg']
            # ADR 0044 permits only pads with no direct nonzero source copper contact.
            for pad in part.Pads():
                for item in old.GetTracks():
                    if not isinstance(item,p.PCB_VIA) and item.GetStart()==item.GetEnd():continue
                    if item.GetNetname()!=pad.GetNetname() or not item.GetBoundingBox().Intersects(pad.GetBoundingBox()):continue
                    assert not any(item.IsOnLayer(layer) and pad.IsOnLayer(layer) and
                        item.GetEffectiveShape(layer).Collide(pad.GetEffectiveShape(layer),0)
                        for layer in old.GetEnabledLayers().CuStack()), ('Moved pad has source copper contact',ref,pad.GetNumber())
        else:
            assert (part.GetPosition(),part.GetOrientation().AsDegrees()) == (
                other.GetPosition(),other.GetOrientation().AsDegrees()), ('Unexpected placement change',ref)
        assert Counter(map(local_pad_signature,part.Pads()))==Counter(map(local_pad_signature,other.Pads())), ('Physical pad changed',ref)
        assert sorted((f.GetName(), f.GetText()) for f in part.GetFields()) == sorted(
            (f.GetName(), f.GetText()) for f in other.GetFields()), ('Component metadata changed', ref)
        for pad in other.Pads():
            key = physical_identity(pad)
            assert key not in lookup
            lookup[key] = pad
    assert list(old.GetEnabledLayers().CuStack()) == list(new.GetEnabledLayers().CuStack())
    retired = []
    retained = Counter()
    for item in old.GetTracks():
        if not isinstance(item, p.PCB_VIA) and item.GetStart() == item.GetEnd():
            retired.append([item.GetNetname(), item.GetStart().x, item.GetStart().y,
                            old.GetLayerName(item.GetLayer()), item.GetWidth()])
        else:
            retained[signature(old, item)] += 1
    assert sorted(retired) == plan['retired_zero_length_tracks'] and len(retired) == 116
    actual = Counter(signature(new, item) for item in new.GetTracks())
    assert not retained-actual, 'Previously retained source copper removed or changed'
    added = actual-retained
    assert added == Counter(map(tuple, plan['added_copper'])), 'Added copper differs from selected integer plan'
    stack = list(new.GetEnabledLayers().CuStack())
    for item in new.GetTracks():
        sig = signature(new, item)
        if not added[sig]:
            continue
        if isinstance(item, p.PCB_VIA):
            assert item.GetViaType() == p.VIATYPE_MICROVIA
            assert item.GetWidth(item.TopLayer()) == 300000 and item.GetDrillValue() == 100000
            assert abs(stack.index(item.TopLayer())-stack.index(item.BottomLayer())) == 1
        else:
            assert item.GetStart() != item.GetEnd()
            assert item.GetWidth() == 200000
    critical={'APP_3V3_FB','VLED_FB','VLED_FB_TOP_MID','LED_IREF','CHARGER_ILIM','CHARGER_ISET','E0_ILM','E1_ILM','E0_DVDT','E1_DVDT','TMP_COLD_SET','TMP_HOT_SET','USB_LOGIC_CT'}
    added_lengths=defaultdict(float)
    for item in new.GetTracks():
        if not isinstance(item,p.PCB_VIA) and signature(new,item) in added:
            added_lengths[item.GetNetname()]+=item.GetLength()/1e6
    assert all(added_lengths[name]<=5.00001 for name in critical), 'Sensitive setting net exceeds 5 mm total added copper'
    changed = set()
    groups = {}
    for part in old_parts.values():
        for pad in part.Pads():
            if not pad.GetNetname():
                continue
            before = physical_cluster(old, pad)
            groups.setdefault(before, pad)
    joins = []
    for before, pad in groups.items():
        after = physical_cluster(new, lookup[physical_identity(pad)])
        assert before <= after, ('Existing physical pad group split', physical_identity(pad))
        if before != after:
            changed.add(pad.GetNetname())
            joins.append([pad.GetNetname(), sorted(before), sorted(after)])
    assert sorted(changed) == plan['changed_nets'], 'Changed net set differs'
    # A physical witness includes coordinates, including repeated logical pad numbers.
    normalized = json.loads(json.dumps(sorted(joins)))
    assert normalized == plan['physical_group_witnesses'], 'Physical join witness differs'
    reporter = module('connectivity', 'report-coupon-board-connectivity.py')
    opens = reporter.open_edges_by_net(OUTPUT)
    assert old.GetConnectivity().GetUnconnectedCount(False) == 215
    assert new.GetConnectivity().GetUnconnectedCount(False) == plan['open_edges']
    assert opens['native_open_edges'] == opens['pad_cluster_open_edges'] == plan['open_edges']
    assert opens['by_net'] == plan['open_edges_by_net']
    module('rows', 'check-row-drain-tie-trial.py').check_physical_rows(new)
    return dict(checked_footprints=483, relocated_passives=len(poses), all_existing_physical_pad_groups_preserved=True,
                retained_source_copper=sum(retained.values()), retired_zero_length_tracks=116,
                added_copper=sum(added.values()),
                added_tracks=sum(n for row,n in added.items() if row[0]=='track'),
                added_microvias=sum(n for row,n in added.items() if row[0]=='via'),
                changed_nets=sorted(changed),
                native_open_edges=plan['open_edges'], pad_cluster_open_edges=opens['pad_cluster_open_edges'])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--drc', required=True, type=Path)
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    manifest = json.loads(MANIFEST.read_text()); plan = json.loads(PLAN.read_text())
    for path, key in [(SOURCE, 'source_sha256'), (OUTPUT, 'board_sha256'), (PLAN, 'plan_sha256'),
                      (ROOT/'tools/generate-routing-progress-trial.py', 'generator_sha256')]:
        assert hashlib.sha256(path.read_bytes()).hexdigest() == manifest[key], (key, 'Fingerprint changed')
    assert plan['source_sha256'] == manifest['source_sha256']
    assert plan['open_edges'] == manifest['native_open_edges'] <= 150
    old, new = p.LoadBoard(str(SOURCE)), p.LoadBoard(str(OUTPUT))
    result = validate_geometry(old, new, plan)
    assert hashlib.sha256((ROOT/'mechanical/review/coupon-canonical-net-contract.json').read_bytes()).hexdigest()==manifest['canonical_contract_sha256']
    assert manifest['shared_footprints_with_canonical_metadata']==465
    for key,manifest_key in [('checked_footprints','footprints'),('relocated_passives','relocated_passives'),
                             ('retained_source_copper','retained_nonzero_source_copper'),
                             ('retired_zero_length_tracks','retired_zero_length_tracks'),
                             ('added_tracks','added_tracks'),('added_microvias','added_microvias')]:
        assert result[key]==manifest[manifest_key], (key,'Manifest count differs')
    assert len(list(new.GetTracks()))==manifest['tracks_and_vias']
    raw_drc=json.loads(args.drc.read_text())
    assert raw_drc['source']==OUTPUT.name and len(raw_drc['unconnected_items'])==plan['open_edges']
    drc = module('drc', 'check-colour-fanout-trial.py')
    assert drc.findings(args.drc) == drc.findings(ROOT/'docs/development/led-native-control-drc-2026-10-21.json')
    assert len(drc.findings(args.drc)) == 104
    result.update(kicad_version=p.GetBuildVersion(), full_drc='104_UNCHANGED_INTRINSIC_FINDINGS',
                  fabrication_release_allowed=False, board_sha256=manifest['board_sha256'],
                  drc_sha256=hashlib.sha256(args.drc.read_bytes()).hexdigest())
    if args.report: args.report.write_text(json.dumps(result, indent=2, sort_keys=True)+'\n')
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
