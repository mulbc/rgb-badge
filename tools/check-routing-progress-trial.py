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


def zone_signature(board, zone):
    poly=zone.Outline();geometry=[]
    for i in range(poly.OutlineCount()):
        chains=[poly.COutline(i)]+[poly.CHole(i,h) for h in range(poly.HoleCount(i))]
        geometry.append(tuple(tuple((chain.CPoint(j).x,chain.CPoint(j).y) for j in range(chain.PointCount())) for chain in chains))
    return (zone.GetZoneName(),zone.GetNetname(),board.GetLayerName(zone.GetLayer()),
            zone.GetAssignedPriority(),zone.GetLocalClearance(),zone.GetMinThickness(),
            zone.GetPadConnection(),zone.GetIslandRemovalMode(),zone.GetThermalReliefGap(),
            zone.GetThermalReliefSpokeWidth(),tuple(geometry))


def validate_geometry(old, new, plan):
    module('necks','routing_pad_necks.py').validate_necks(plan)
    portable=module('plan','check-routing-progress-plan.py')
    portable.validate_zone_structure(SOURCE,OUTPUT,plan)
    original_zones=Counter(zone_signature(old,z) for z in old.Zones())
    other_zones=Counter(zone_signature(new,z) for z in new.Zones() if not z.GetZoneName().startswith('ADR0049-'))
    assert original_zones==other_zones, 'Original native zone changed'
    new_zones={z.GetZoneName():z for z in new.Zones() if z.GetZoneName().startswith('ADR0049-')}
    assert set(new_zones)=={z['name'] for z in plan.get('power_zones',[])}
    for entry in plan.get('power_zones',[]):
        z=new_zones[entry['name']]
        assert (z.GetNetname(),new.GetLayerName(z.GetLayer()))==(entry['net'],entry['layer'])
        assert z.GetAssignedPriority()==10 and z.GetLocalClearance()==200000 and z.GetMinThickness()==200000
        assert z.GetPadConnection()==p.ZONE_CONNECTION_FULL and z.GetIslandRemovalMode()==p.ISLAND_REMOVAL_MODE_ALWAYS
        assert z.GetThermalReliefGap()==z.GetThermalReliefSpokeWidth()==200000
        poly=z.Outline();polygons=[]
        for i in range(poly.OutlineCount()):
            chain=poly.COutline(i)
            outer=[[chain.CPoint(j).x,chain.CPoint(j).y] for j in range(chain.PointCount())]
            holes=[]
            for hi in range(poly.HoleCount(i)):
                hole=poly.CHole(i,hi)
                holes.append([[hole.CPoint(j).x,hole.CPoint(j).y] for j in range(hole.PointCount())])
            polygons.append(dict(outer=outer,holes=holes))
        assert polygons==entry['polygons_iu'], 'Selected native zone polygon changed'
    old_parts = {f.GetReference(): f for f in old.GetFootprints()}
    new_parts = {f.GetReference(): f for f in new.GetFootprints()}
    assert old_parts.keys() == new_parts.keys() and len(new_parts) == 483, 'Component inventory changed'
    testpad_policy=module('testpads','routing_testpad_placements.py')
    testpad_entries=testpad_policy.validate_plan(plan,required=True)
    poses={entry['reference']:entry for entry in plan['placements']}
    assert len(poses)==len(plan['placements'])
    assert all(ref.startswith(('R','C')) and ref[1:].isdigit() and ref not in {'R45','R46'} for ref in poses), 'Unreviewed component move'
    assert not set(poses)&{entry['reference'] for entry in testpad_entries}
    poses.update({entry['reference']:entry for entry in testpad_entries})
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
            # ADR 0045 permits contacted passives while preserving all prior groups.
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
    orphan=Counter(map(tuple,plan.get('retired_orphan_microvias',[])))
    prior=json.loads((ROOT/'mechanical/review/routing-progress-150-checkpoint.json').read_text())
    baseline_inventory=retained+Counter(map(tuple,prior['added_copper']))
    assert not orphan-baseline_inventory, 'Retired via absent from accepted 150-edge inventory'
    assert all(row[0]=='via' and n==1 for row,n in orphan.items()), 'Only exact orphan microvias may retire'
    assert not any(actual[row] for row in orphan), 'Retired via restored without review'
    retained.subtract(orphan);retained=+retained
    replacements=module('replacements','routing_track_replacements.py')
    replaced=replacements.verify_native(old,new,plan,signature,physical_identity)
    retained.subtract(replaced);retained=+retained
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
            assert item.GetWidth() in {120000,200000}
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
    prior_check=module('prior_checkpoint', 'check-routing-progress-plan.py')
    prior_check.validate_prior_checkpoint(plan)
    prior_check.validate_100_checkpoint(plan)
    prior_check.validate_94_checkpoint(plan)
    prior_check.validate_91_checkpoint(plan)
    prior_check.validate_84_checkpoint(plan)
    prior_check.validate_82_checkpoint(plan)
    prior_check.validate_76_checkpoint(plan)
    prior_check.validate_71_checkpoint(plan)
    prior_check.validate_70_checkpoint(plan)
    prior_check.validate_69_checkpoint(plan)
    prior_check.validate_65_checkpoint(plan)
    prior_check.validate_64_checkpoint(plan)
    prior_check.validate_63_checkpoint(plan)
    prior_check.validate_62_checkpoint(plan)
    digital_count=module('digital_width','routing_digital_width.py').verify_native(new,plan,signature,physical_cluster)
    testpad_policy.verify_native(old,new,plan,signature,physical_identity,physical_cluster)
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
    return dict(checked_footprints=483, relocated_passives=len(plan['placements']), relocated_testpads=len(testpad_entries), all_existing_physical_pad_groups_preserved=True,
                digital_narrow_tracks=digital_count, digital_nets=len(plan.get('digital_width',{}).get('nets',[])),
                retained_source_copper=sum(retained.values()), retired_zero_length_tracks=116,
                retired_orphan_microvias=sum(orphan.values()), replaced_source_tracks=sum(replaced.values()),
                added_power_zones=len(plan.get('power_zones',[])),
                added_copper=sum(added.values()),
                added_tracks=sum(n for row,n in added.items() if row[0]=='track'),
                added_microvias=sum(n for row,n in added.items() if row[0]=='via'),
                changed_nets=sorted(changed),
                native_open_edges=plan['open_edges'], pad_cluster_open_edges=opens['pad_cluster_open_edges'])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--drc', required=True, type=Path)
    parser.add_argument('--report', type=Path)
    parser.add_argument('--restored-via-board',type=Path)
    parser.add_argument('--restored-via-drc',type=Path)
    args = parser.parse_args()
    manifest = json.loads(MANIFEST.read_text()); plan = json.loads(PLAN.read_text())
    portable=module('plan','check-routing-progress-plan.py')
    portable.validate(plan,manifest);portable.validate_profile(plan,manifest)
    for path, key in [(SOURCE, 'source_sha256'), (OUTPUT, 'board_sha256'), (PLAN, 'plan_sha256'),
                      (ROOT/'tools/generate-routing-progress-trial.py', 'generator_sha256')]:
        assert hashlib.sha256(path.read_bytes()).hexdigest() == manifest[key], (key, 'Fingerprint changed')
    assert plan['source_sha256'] == manifest['source_sha256']
    assert plan['open_edges'] == manifest['native_open_edges'] <= 100
    old, new = p.LoadBoard(str(SOURCE)), p.LoadBoard(str(OUTPUT))
    result = validate_geometry(old, new, plan)
    assert hashlib.sha256((ROOT/'mechanical/review/coupon-canonical-net-contract.json').read_bytes()).hexdigest()==manifest['canonical_contract_sha256']
    assert manifest['shared_footprints_with_canonical_metadata']==465
    for key,manifest_key in [('checked_footprints','footprints'),('relocated_passives','relocated_passives'),
                             ('retained_source_copper','retained_nonzero_source_copper'),
                             ('relocated_testpads','relocated_testpads'),
                             ('digital_narrow_tracks','digital_narrow_tracks'),('digital_nets','digital_nets'),
                             ('retired_zero_length_tracks','retired_zero_length_tracks'),
                             ('retired_orphan_microvias','retired_orphan_microvias'),
                             ('replaced_source_tracks','replaced_source_tracks'),
                             ('added_power_zones','power_zones'),
                             ('added_tracks','added_tracks'),('added_microvias','added_microvias')]:
        assert result[key]==manifest[manifest_key], (key,'Manifest count differs')
    assert len(list(new.GetTracks()))==manifest['tracks_and_vias']
    raw_drc=json.loads(args.drc.read_text())
    assert raw_drc['source']==OUTPUT.name and len(raw_drc['unconnected_items'])==plan['open_edges']
    drc = module('drc', 'check-colour-fanout-trial.py')
    assert drc.findings(args.drc) == drc.findings(ROOT/'docs/development/led-native-control-drc-2026-10-21.json')
    assert len(drc.findings(args.drc)) == 104
    retired=Counter(map(tuple,plan.get('retired_orphan_microvias',[])))
    if retired:
        assert args.restored_via_board and args.restored_via_drc, 'Orphan restoration evidence required'
        restored=p.LoadBoard(str(args.restored_via_board))
        assert Counter(zone_signature(new,z) for z in new.Zones())==Counter(zone_signature(restored,z) for z in restored.Zones()), 'Restoration changes zone definitions'
        actual=Counter(signature(restored,t) for t in restored.GetTracks())
        selected=Counter(signature(new,t) for t in new.GetTracks())
        assert not selected-actual and actual-selected==retired, 'Restoration inventory differs'
        lookup={physical_identity(q):q for f in restored.GetFootprints() for q in f.Pads()}
        parts={f.GetReference():f for f in restored.GetFootprints()}
        assert parts.keys()=={f.GetReference() for f in new.GetFootprints()}
        for part in new.GetFootprints():
            other=parts[part.GetReference()]
            assert (part.GetPosition(),part.GetOrientation().AsDegrees(),part.GetFPIDAsString())==(other.GetPosition(),other.GetOrientation().AsDegrees(),other.GetFPIDAsString())
            assert Counter(map(local_pad_signature,part.Pads()))==Counter(map(local_pad_signature,other.Pads()))
            for pad in part.Pads():
                if pad.GetNetname():assert physical_cluster(new,pad)==physical_cluster(restored,lookup[physical_identity(pad)]), 'Restoration changes selected groups'
        assert restored.GetConnectivity().GetUnconnectedCount(False)==plan['open_edges']
        raw=json.loads(args.restored_via_drc.read_text())
        assert raw['source']==args.restored_via_board.name
        assert len(raw['unconnected_items'])==plan['open_edges']
        dangling=[v for v in raw['violations'] if v['type']=='via_dangling']
        assert len(dangling)==sum(retired.values())
        by_uuid={t.m_Uuid.AsString():t for t in restored.GetTracks()}
        witnessed=Counter()
        for violation in dangling:
            assert violation['severity']=='warning' and len(violation['items'])==1
            item=violation['items'][0];via=by_uuid[item['uuid']]
            assert isinstance(via,p.PCB_VIA) and via.GetViaType()==p.VIATYPE_MICROVIA
            assert item['pos']==dict(x=via.GetPosition().x/1e6,y=via.GetPosition().y/1e6)
            witnessed[signature(restored,via)]+=1
        assert witnessed==retired, 'A retired via lacks an exact dangling witness'
        filtered=dict(raw);filtered['violations']=[v for v in raw['violations'] if v['type']!='via_dangling']
        filtered_path=args.restored_via_drc.with_suffix('.intrinsic.json')
        filtered_path.write_text(json.dumps(filtered))
        assert drc.findings(filtered_path)==drc.findings(args.drc), 'Restoration introduces a different finding'
        result.update(orphan_restoration_preserves_all_selected_groups=True,
                      orphan_restoration_drc_sha256=hashlib.sha256(args.restored_via_drc.read_bytes()).hexdigest())
    result.update(kicad_version=p.GetBuildVersion(), full_drc='104_UNCHANGED_INTRINSIC_FINDINGS',
                  fabrication_release_allowed=False, board_sha256=manifest['board_sha256'],
                  drc_sha256=hashlib.sha256(args.drc.read_bytes()).hexdigest())
    if args.report: args.report.write_text(json.dumps(result, indent=2, sort_keys=True)+'\n')
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
