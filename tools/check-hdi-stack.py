#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Audit native CAD against corrected stack intent. Geometry check is no release."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import pcbnew as p
from hdi_stack_policy import validate_plan, via_findings

ROOT = Path(__file__).resolve().parents[1]
PLAN = ROOT / 'manufacturing/planning/coupon-six-layer-stack.json'
BOARD = ROOT / 'hardware/coupon/rev-a/staging/led-u36-stage-routing-trial-114mm.kicad_pcb'


def audit(path, plan):
    validate_plan(plan)
    board = p.LoadBoard(str(path))
    failures, counts = [], Counter()
    kinds = {p.VIATYPE_MICROVIA: 'microvia', p.VIATYPE_THROUGH: 'through',
             p.VIATYPE_BLIND: 'blind', p.VIATYPE_BURIED: 'buried'}
    for via in board.GetTracks():
        if not isinstance(via, p.PCB_VIA):
            continue
        row = {'uuid': via.m_Uuid.AsString(), 'net': via.GetNetname(),
               'kind': kinds.get(via.GetViaType(), 'unknown'),
               'layers': [board.GetLayerName(via.TopLayer()), board.GetLayerName(via.BottomLayer())],
               'pad_um': via.GetWidth(via.TopLayer()) / 1000, 'hole_um': via.GetDrillValue() / 1000,
               'position_mm': [via.GetPosition().x / 1e6, via.GetPosition().y / 1e6]}
        errors = via_findings(plan, row)
        counts[tuple([row['kind']] + row['layers'])] += 1
        if errors:
            failures.append(dict(row, errors=errors))
    board_failures = []
    actual_layers=[board.GetLayerName(layer) for layer in board.GetEnabledLayers().CuStack()]
    if actual_layers!=plan['copper_layers']:
        board_failures.append('COPPER_LAYER_STACK_DIFFERS_FROM_PLAN')
    if board.GetDesignSettings().GetBoardThickness() / 1000 != plan['finished_target_um']:
        board_failures.append('CAD_THICKNESS_DIFFERS_FROM_TARGET')
    if '(stackup' not in path.read_text():
        board_failures.append('EXPLICIT_STACKUP_MISSING')
    return {
        'board_geometry_findings': board_failures,
        'SPDX-License-Identifier': 'CERN-OHL-S-2.0',
        'status': 'GEOMETRY_INELIGIBLE' if failures or board_failures else 'VIA_GEOMETRY_ELIGIBLE_ONLY',
        'board_sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
        'checker_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'policy_sha256': hashlib.sha256((ROOT/'tools/hdi_stack_policy.py').read_bytes()).hexdigest(),
        'actual_copper_layers': actual_layers,
        'plan_sha256': hashlib.sha256(PLAN.read_bytes()).hexdigest(),
        'via_count': sum(counts.values()), 'ineligible_vias': sorted(failures, key=lambda r: r['uuid']),
        'counts': [{'kind': k[0], 'layers': list(k[1:]), 'count': n} for k, n in sorted(counts.items())],
        'cad_general_thickness_um': board.GetDesignSettings().GetBoardThickness() / 1000,
        'stackup_explicit_in_source': '(stackup' in path.read_text(),
        'fabrication_release_allowed': False,
        'unresolved': ['controlled supplier build', 'finished thickness and mask/finish allowance',
                       'material/impedance', 'via fill/cap/stack reliability', 'connector/case fit', 'Gate A'],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--board', type=Path, default=BOARD)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--expect-ineligible', action='store_true', help='regression assertion, never permission to fabricate')
    args = parser.parse_args()
    result = audit(args.board, json.loads(PLAN.read_text()))
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    failed = bool(result['ineligible_vias'] or result['board_geometry_findings'])
    print(result['status'], len(result['ineligible_vias']), 'ineligible vias; fabrication prohibited')
    if args.expect_ineligible:
        raise SystemExit(0 if failed else 1)
    raise SystemExit(1 if failed else 0)


if __name__ == '__main__':
    main()
