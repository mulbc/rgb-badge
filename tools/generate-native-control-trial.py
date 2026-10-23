#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Replay checked native-clearance gate/control copper on the row-13 study.

The plan records selected added geometry, not a component or electrical release.
Exact shared part metadata comes from checked canonical source; no part, pad,
net or placement is changed and study-only replacements stay unselected.
"""
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import uuid
import pcbnew as p

ROOT = Path(__file__).resolve().parents[1]
STAGING = ROOT / 'hardware/coupon/rev-a/staging'
SOURCE = STAGING / 'led-row13-bias-trial-114mm.kicad_pcb'
OUTPUT = STAGING / 'led-native-control-trial-114mm.kicad_pcb'
PLAN = ROOT / 'mechanical/review/native-control-routing-plan.json'
REPORT = ROOT / 'mechanical/review/native-control-trial.json'
SOURCE_SHA256 = '7541a0f2eb8eabc383e89ae153131e0bc53d14a257033c8e79b72a7b9ead16f0'
SCOPE = uuid.UUID('572f2376-04b3-4c9a-ab11-a7d4d1afda6e')


def main():
    assert hashlib.sha256(SOURCE.read_bytes()).hexdigest() == SOURCE_SHA256
    # The source checker requires modern host Python; KiCad bundles Python 3.9.
    checker = ROOT / 'tools/check-coupon-study-contract.py'
    contract_path = ROOT / 'mechanical/review/coupon-canonical-net-contract.json'
    subprocess.run(['python3', str(checker), '--board', str(SOURCE),
                    '--historical-generator-input'], check=True)
    contract_digest = hashlib.sha256(contract_path.read_bytes()).hexdigest()
    canonical = json.loads(contract_path.read_text())
    plan = json.loads(PLAN.read_text())
    assert plan['source_sha256'] == SOURCE_SHA256 and plan['kicad_iu_per_mm'] == 1000000
    board = p.LoadBoard(str(SOURCE))
    common = set(canonical['components']) & {f.GetReference() for f in board.GetFootprints()}
    metadata_uuids = {}
    for footprint in board.GetFootprints():
        ref = footprint.GetReference()
        if ref not in common:
            continue
        for name, key in [('MPN', 'mpn'), ('Manufacturer', 'manufacturer')]:
            field = footprint.GetField(name)
            if field is None:
                field = p.PCB_FIELD(footprint, p.FIELD_T_USER, name)
                field.SetPosition(footprint.GetPosition())
                field.SetLayer(p.B_Fab if footprint.IsFlipped() else p.F_Fab)
                footprint.Add(field)
            field.SetText(canonical['components'][ref][key])
            field.SetVisible(False)
            identifier = str(uuid.uuid5(SCOPE, 'canonical-metadata:'+ref+':'+name))
            metadata_uuids[field.m_Uuid.AsString()] = identifier
    initial = len(list(board.GetTracks()))
    layers = {board.GetLayerName(layer): layer for layer in board.GetEnabledLayers().CuStack()}
    # Exact source segments are replaced to reserve the reviewed ground escapes.
    # No other source removal is permitted by this replay contract.
    assert plan['removed_source_tracks'] == [dict(net='ROW_SEL_04',
        start_iu=[38600000, 7250000], end_iu=[54000000, 7250000],
        layer='In4.Cu', width_iu=200000), dict(net='COL_07_R',
        start_iu=[81400000, 6050000], end_iu=[56450000, 6050000],
        layer='In4.Cu', width_iu=200000)]
    removed = []
    for entry in plan['removed_source_tracks']:
        matches = [t for t in board.GetTracks() if not isinstance(t, p.PCB_VIA)
                   and t.GetNetname() == entry['net'] and t.GetLayer() == layers[entry['layer']]
                   and [t.GetStart().x, t.GetStart().y] == entry['start_iu']
                   and [t.GetEnd().x, t.GetEnd().y] == entry['end_iu']
                   and t.GetWidth() == entry['width_iu']]
        assert len(matches) == 1
        board.Remove(matches[0])
        removed.extend(matches)
    for entry in plan['tracks']:
        item = p.PCB_TRACK(board)
        item.SetStart(p.VECTOR2I(*entry['start_iu']))
        item.SetEnd(p.VECTOR2I(*entry['end_iu']))
        item.SetLayer(layers[entry['layer']])
        assert entry['width_iu'] == 200000
        item.SetWidth(entry['width_iu'])
        item.SetNet(board.FindNet(entry['net']))
        board.Add(item)
    for entry in plan['vias']:
        item = p.PCB_VIA(board)
        item.SetPosition(p.VECTOR2I(*entry['position_iu']))
        item.SetViaType(p.VIATYPE_MICROVIA)
        item.SetLayerPair(layers[entry['top']], layers[entry['bottom']])
        assert entry['diameter_iu'] == 300000 and entry['drill_iu'] == 100000
        item.SetWidth(entry['diameter_iu'])
        item.SetDrill(entry['drill_iu'])
        item.SetNet(board.FindNet(entry['net']))
        board.Add(item)
    p.ZONE_FILLER(board).Fill(board.Zones())
    p.SaveBoard(str(OUTPUT), board)
    spec = importlib.util.spec_from_file_location('save', ROOT / 'tools/generate-paired-charger-114mm-routing.py')
    helper = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(helper)
    count = len(list(board.GetTracks()))
    data = helper.sorted_native_tracks(OUTPUT.read_text(), expected=count)
    sequence = iter(range(data.count('(uuid "')))
    # Extra hidden fields must not renumber any existing geometry UUID. Their
    # reference/name-derived identities are independent of geometry ordering.
    def normalized_uuid(match):
        if match.group(1) in metadata_uuids:
            return '(uuid "'+metadata_uuids[match.group(1)]+'")'
        return '(uuid "'+str(uuid.uuid5(SCOPE, str(next(sequence))))+'")'
    data = re.sub(r'\(uuid "([0-9a-f-]{36})"\)', normalized_uuid, data)
    OUTPUT.write_text(data)
    subprocess.run(['python3', str(checker)], check=True)
    assert hashlib.sha256(contract_path.read_bytes()).hexdigest() == contract_digest
    loaded = p.LoadBoard(str(OUTPUT))
    report = dict(status='UNQUALIFIED_NATIVE_CONTROL_GEOMETRY_STUDY',
                  source_sha256=SOURCE_SHA256,
                  board_sha256=hashlib.sha256(OUTPUT.read_bytes()).hexdigest(),
                  generator_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                  plan_sha256=hashlib.sha256(PLAN.read_bytes()).hexdigest(),
                  kicad_version=p.GetBuildVersion(), unchanged_footprints=483,
                  canonical_contract_sha256=contract_digest,
                  shared_footprints_with_canonical_metadata=len(common),
                  added_tracks=len(plan['tracks']), added_microvias=len(plan['vias']),
                  replaced_source_tracks=len(removed),
                  source_tracks_and_vias=initial, tracks_and_vias=count,
                  native_open_edges=loaded.GetConnectivity().GetUnconnectedCount(False))
    report['SPDX-License-Identifier'] = 'CERN-OHL-S-2.0'
    REPORT.write_text(json.dumps(report, indent=2, sort_keys=True)+'\n')
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
