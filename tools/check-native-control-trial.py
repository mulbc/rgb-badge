#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Independently check saved native-clearance control routing and native DRC."""
import argparse
from collections import Counter
import hashlib
import importlib.util
import json
from pathlib import Path
import pcbnew as p

ROOT = Path(__file__).resolve().parents[1]
STAGING = ROOT / 'hardware/coupon/rev-a/staging'
SOURCE = STAGING / 'led-row13-bias-trial-114mm.kicad_pcb'
OUTPUT = STAGING / 'led-native-control-trial-114mm.kicad_pcb'


def module(name, filename):
    spec = importlib.util.spec_from_file_location(name, ROOT / 'tools' / filename)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


def identity(pad):
    return (pad.GetParentFootprint().GetReference(), pad.GetNumber(),
            pad.GetPosition().x, pad.GetPosition().y)


def cluster(board, pad):
    return frozenset(identity(q) for q in board.GetConnectivity().GetConnectedItems(pad)
                     if isinstance(q, p.PAD))


def validate_geometry(old, new, intended_joins):
    escape = module('escape', 'check-ground-escape-trial.py')
    grid = module('grid', 'generate-colour-fanout-grid-trial.py')
    before = {f.GetReference(): f for f in old.GetFootprints()}
    after = {f.GetReference(): f for f in new.GetFootprints()}
    assert before.keys() == after.keys() and len(after) == 483
    new_pads = {}
    for ref, part in before.items():
        other = after[ref]
        assert (part.GetValue(), part.GetFPIDAsString(), part.GetPosition(),
                part.GetOrientation().AsDegrees(), part.GetLayer()) == (
                    other.GetValue(), other.GetFPIDAsString(), other.GetPosition(),
                    other.GetOrientation().AsDegrees(), other.GetLayer()), ref
        assert Counter(map(escape.pad_signature, part.Pads())) == Counter(
            map(escape.pad_signature, other.Pads())), ref
        for pad in other.Pads():
            assert identity(pad) not in new_pads
            new_pads[identity(pad)] = pad
    originals = Counter(grid.signature(item) for item in old.GetTracks())
    added = []
    for item in new.GetTracks():
        signature = grid.signature(item)
        if originals[signature]:
            originals[signature] -= 1
        else:
            added.append(item)
    replacement = ('track', 'ROW_SEL_04', 200000, 38.6, 7.25, 54.0, 7.25, int(p.In4_Cu))
    assert +originals == Counter({replacement: 1}), 'Source copper differs from the one reviewed replacement'
    # Only the reviewed signal joins and fixed supply-continuity geometry are
    # allowed. Supply groups stay unchanged; GND has only the reviewed R28 join.
    allowed = {'ROW_GATE_05', 'SYS_I2C_SCL', 'VLED_WINDOW_OK',
               'GAUGE_I2C_SDA', 'GAUGE_I2C_SCL', 'UART0_RX', 'UART0_TX_RAW',
               'SYS_I2C_SDA', 'ROW_ARM', 'USB_CHARGE_REQ', 'GND'}
    power_hashes = {
        '+3V3_APP': (26, 'fda8fe3404655998aceb7616469bf9d6faee7f075ab474304bccf1918ce93e89'),
        '+3V3_USB': (10, '299e9ca0dc333371ab467fdbae07e4c1a5217c950ee0b2fefdf427327c1d5074'),
        'GND': (4, '2e7c42bd66469a53c0bc5357b9d2b7354b625089e0e32a2261ad6afae59f1f9d'),
        'ROW_SEL_04': (5, 'd974f8a1bf104afe6cead3e4cfc87c855539a93e9bae56a924f0c7bd8238cc24'),
    }
    assert added and {item.GetNetname() for item in added} == allowed | set(power_hashes)
    stack = list(new.GetEnabledLayers().CuStack())
    for item in added:
        if isinstance(item, p.PCB_VIA):
            assert item.GetViaType() == p.VIATYPE_MICROVIA
            assert item.GetWidth(item.TopLayer()) == 300000 and item.GetDrillValue() == 100000
            assert abs(stack.index(item.TopLayer())-stack.index(item.BottomLayer())) == 1
        else:
            assert item.GetWidth() == 200000 and item.GetStart() != item.GetEnd()
    changed = set()
    for part in before.values():
        for pad in part.Pads():
            if not pad.GetNetname():
                continue
            a, b = cluster(old, pad), cluster(new, new_pads[identity(pad)])
            assert a <= b, ('Existing physical pad cluster split', identity(pad))
            if a != b:
                changed.add(pad.GetNetname())
    assert changed == allowed, changed
    def power_signature(item):
        if isinstance(item, p.PCB_VIA):
            return ['via', item.GetNetname(), item.GetPosition().x, item.GetPosition().y,
                    new.GetLayerName(item.TopLayer()), new.GetLayerName(item.BottomLayer()),
                    item.GetWidth(item.TopLayer()), item.GetDrillValue()]
        return ['track', item.GetNetname(), item.GetStart().x, item.GetStart().y,
                item.GetEnd().x, item.GetEnd().y, new.GetLayerName(item.GetLayer()), item.GetWidth()]
    for name, (count, digest) in power_hashes.items():
        signatures = sorted(power_signature(t) for t in added if t.GetNetname() == name)
        assert len(signatures) == count
        assert hashlib.sha256(json.dumps(signatures, separators=(',', ':')).encode()).hexdigest() == digest
    assert len(intended_joins) == 15
    for entry in intended_joins:
        name, ref, number = entry['net'], *entry['source']
        assert name in allowed
        source_pad = next(q for q in before[ref].Pads() if q.GetNumber() == number)
        anchor_ref, anchor_number = entry['anchor']
        anchor = next(q for q in before[anchor_ref].Pads() if q.GetNumber() == anchor_number)
        assert source_pad.GetNetname() == anchor.GetNetname() == name
        assert cluster(old, source_pad) != cluster(old, anchor)
        assert cluster(new, new_pads[identity(source_pad)]) == cluster(new, new_pads[identity(anchor)])
    physical = module('physical', 'check-row-drain-tie-trial.py')
    physical.check_physical_rows(new)
    power_pad = next(q for q in after['U3'].Pads() if q.GetNumber() == '2')
    bypass = next(q for q in after['C74'].Pads() if q.GetNumber() == '1')
    assert cluster(new, power_pad) == cluster(new, bypass), 'Controller supply bridge disconnected'
    usb_bypass = next(q for q in after['C38'].Pads() if q.GetNumber() == '1')
    usb_anchor = next(q for q in after['C36'].Pads() if q.GetNumber() == '1')
    assert cluster(new, usb_bypass) == cluster(new, usb_anchor), 'USB logic bypass disconnected'
    ground_pad = next(q for q in after['R28'].Pads() if q.GetNumber() == '2')
    ground_anchor = next(q for q in before['R25'].Pads() if q.GetNumber() == '2')
    assert cluster(new, ground_pad) == cluster(old, ground_anchor) | {identity(ground_pad)}, 'Ground group differs'
    return dict(unchanged_footprints=483, source_copper_preserved=False,
                unaffected_source_copper_preserved=True, reviewed_source_track_replacements=1,
                existing_physical_pad_clusters_preserved=True,
                controller_supply_bridge_preserved=True,
                usb_logic_bypass_group_preserved=True,
                reviewed_power_copper_signatures_checked=True,
                changed_nets=sorted(changed), checked_joins=len(intended_joins),
                added_tracks=sum(not isinstance(t, p.PCB_VIA) for t in added),
                added_microvias=sum(isinstance(t, p.PCB_VIA) for t in added),
                physical_anode_pads_per_row=18)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--drc', required=True, type=Path)
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    manifest = json.loads((ROOT / 'mechanical/review/native-control-trial.json').read_text())
    contract_path = ROOT / 'mechanical/review/coupon-canonical-net-contract.json'
    assert hashlib.sha256(contract_path.read_bytes()).hexdigest() == manifest['canonical_contract_sha256']
    assert manifest['shared_footprints_with_canonical_metadata'] == 465
    plan_path = ROOT / 'mechanical/review/native-control-routing-plan.json'
    plan = json.loads(plan_path.read_text())
    for path, key in ((SOURCE, 'source_sha256'), (OUTPUT, 'board_sha256'),
                      (plan_path, 'plan_sha256'),
                      (ROOT / 'tools/generate-native-control-trial.py', 'generator_sha256')):
        assert hashlib.sha256(path.read_bytes()).hexdigest() == manifest[key]
    old, new = p.LoadBoard(str(SOURCE)), p.LoadBoard(str(OUTPUT))
    result = validate_geometry(old, new, plan['intended_joins'])
    assert result['added_tracks'] == manifest['added_tracks']
    assert result['added_microvias'] == manifest['added_microvias']
    colour = module('colour', 'check-colour-fanout-trial.py')
    assert colour.findings(args.drc) == colour.findings(ROOT / 'docs/development/led-row13-bias-drc-2026-10-21.json')
    assert len(colour.findings(args.drc)) == 104
    reporter = module('connectivity', 'report-coupon-board-connectivity.py')
    opens = reporter.open_edges_by_net(OUTPUT)
    assert opens['native_open_edges'] == opens['pad_cluster_open_edges'] == manifest['native_open_edges'] == 219
    assert manifest['replaced_source_tracks'] == 1
    assert opens['by_net']['GND'] == 26 and opens['by_net']['VLED'] == 14
    assert 'SYS_I2C_SCL' not in opens['by_net']
    assert opens['by_net']['SYS_I2C_SDA'] == 1
    data_pad = next(q for f in new.GetFootprints() if f.GetReference() == 'U46'
                    for q in f.Pads() if q.GetNumber() == '6')
    assert {(ref, number) for ref, number, x, y in cluster(new, data_pad)} == {
        ('U46', '6'), ('U3', '10'), ('R79', '2')}, 'Application data group differs'
    assert 'UART0_RX' not in opens['by_net'] and 'UART0_TX_RAW' not in opens['by_net']
    assert opens['by_net']['UART0_TX'] == 1
    assert opens['by_net']['+3V3_APP'] == 7 and opens['by_net']['+3V3_USB'] == 4
    assert not {'GAUGE_I2C_SDA', 'GAUGE_I2C_SCL', 'ROW_ARM', 'USB_CHARGE_REQ'} & opens['by_net'].keys()
    gauge_pad = next(q for f in new.GetFootprints() if f.GetReference() == 'U35'
                     for q in f.Pads() if q.GetNumber() == '8')
    assert {(ref, number) for ref, number, x, y in cluster(new, gauge_pad)} == {
        ('U35', '8'), ('U46', '3'), ('R101', '2')}, 'Gauge data group differs'
    for ref, pin, expected in [
            ('U35', '7', {('R102', '2'), ('U35', '7'), ('U46', '2')}),
            ('U55', '3', {('U54', '5'), ('U55', '3')}),
            ('U23', '2', {('TP30', '1'), ('U17', '4'), ('U23', '2'), ('U42', '1')})]:
        pad = next(q for f in new.GetFootprints() if f.GetReference() == ref
                   for q in f.Pads() if q.GetNumber() == pin)
        assert {(r, n) for r, n, x, y in cluster(new, pad)} == expected
    assert {name for name in opens['by_net'] if name.startswith('ROW_GATE_')} == {
        'ROW_GATE_00', 'ROW_GATE_02', 'ROW_GATE_03', 'ROW_GATE_04', 'ROW_GATE_06', 'ROW_GATE_07'}
    assert len(list(new.GetTracks())) == manifest['tracks_and_vias']
    result.update(board_sha256=manifest['board_sha256'], kicad_version=p.GetBuildVersion(),
                  native_open_edges=219, ground_open_edges=26, vled_open_edges=14,
                  application_clock_open_edges=0,
                  application_data_open_edges=1,
                  uart_receive_open_edges=0, uart_device_transmit_open_edges=0,
                  uart_test_pad_transmit_open_edges=1,
                  gauge_data_open_edges=0, gauge_clock_open_edges=0,
                  row_arm_open_edges=0, usb_charge_request_open_edges=0,
                  connected_gate_terminals=10, remaining_gate_terminals=6,
                  full_drc='104_UNCHANGED_INTRINSIC_FINDINGS',
                  drc_sha256=hashlib.sha256(args.drc.read_bytes()).hexdigest())
    result['SPDX-License-Identifier'] = 'CERN-OHL-S-2.0'
    if args.report:
        args.report.write_text(json.dumps(result, indent=2, sort_keys=True)+'\n')
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
