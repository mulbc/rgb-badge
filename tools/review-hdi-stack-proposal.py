#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Read-only comparison of the owner's 2026-11-06 HDI proposal and selected CAD."""
import argparse
from collections import Counter
from decimal import Decimal
import hashlib
import json
from pathlib import Path
import pcbnew as p

ROOT = Path(__file__).resolve().parents[1]
BOARD = ROOT / 'hardware/coupon/rev-a/staging/led-converter-routing-trial-114mm.kicad_pcb'
BOARD_SHA = '5e07fb866cc059de670e34102045d9dfd88c88f101355fcdbb27253c0ae26e43'


def review():
    digest = hashlib.sha256(BOARD.read_bytes()).hexdigest()
    if digest != BOARD_SHA:
        raise ValueError('selected board differs from reviewed checkpoint')
    board = p.LoadBoard(str(BOARD))
    counts = Counter()
    witnesses = {}
    for item in board.GetTracks():
        if not isinstance(item, p.PCB_VIA):
            continue
        kind = {p.VIATYPE_MICROVIA: 'microvia', p.VIATYPE_THROUGH: 'through'}[item.GetViaType()]
        key = (kind, board.GetLayerName(item.TopLayer()), board.GetLayerName(item.BottomLayer()),
               item.GetWidth(item.TopLayer()), item.GetDrillValue())
        counts[key] += 1
        witness = {'uuid': item.m_Uuid.AsString(), 'net': item.GetNetname(),
                   'position_mm': [item.GetPosition().x / 1e6, item.GetPosition().y / 1e6]}
        if key not in witnesses or witness['uuid'] < witnesses[key]['uuid']:
            witnesses[key] = witness
    rows = []
    unsupported = 0
    for key, number in sorted(counts.items()):
        kind, top, bottom, pad, hole = key
        inner = kind == 'microvia' and top != 'F.Cu' and bottom != 'B.Cu'
        unsupported += number if inner else 0
        rows.append({'type': kind, 'layers': [top, bottom], 'pad_mm': pad / 1e6,
                     'hole_mm': hole / 1e6, 'count': number, 'witness': witnesses[key],
                     'span_absent_from_owner_1plus4plus1_scheme': inner})
    # Owner input: explicit approximate metric values; copper counted once.
    dielectric = list(map(Decimal, ('.076', '.100', '.710', '.100', '.076')))
    copper = Decimal('.035') * 6
    total = sum(dielectric) + copper
    assert total == Decimal('1.272') and unsupported == 1670
    assert sum(counts.values()) == 3300
    return {
        'SPDX-License-Identifier': 'CERN-OHL-S-2.0',
        'date': '2026-11-06', 'status': 'OWNER_PROPOSAL_REVIEW_NOT_FABRICATOR_APPROVAL',
        'board_sha256': digest, 'tool_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'kicad_version': p.GetBuildVersion(),
        'current_board_thickness_mm': board.GetDesignSettings().GetBoardThickness() / 1e6,
        'current_vias': rows, 'inner_microvias_not_supported_by_proposed_scheme': unsupported,
        'owner_proposed_copper_um_per_layer': [35] * 6,
        'owner_proposed_dielectric_mm': list(map(float, dielectric)),
        'listed_total_without_mask_finish_mm': float(total),
        'stated_target_thickness_mm': 1.6,
        'unaccounted_thickness_mm': float(Decimal('1.6') - total),
        'central_dielectric_if_only_it_were_changed_to_reach_1p6_mm_NOT_ADOPTED':
            float(Decimal('.710') + Decimal('1.6') - total),
        'outer_dielectric_to_nominal_hole_ratio': .76,
        'owner_microvia_nominal_annular_ring_mm': .075,
        'current_microvia_nominal_annular_ring_mm': .10,
        'owner_PTH_nominal_aspect_ratio_at_1p6mm': 8,
        'GRM188_pdf_sha256': 'f51cff8dad7a6983263ab35b5705f4d1d4b9977b1f03739c653381ba03d94ea8',
        'exact_part_combined_C_bound_received': False,
        'fabricator_controlled_stack_received': False,
        'source_board_or_rules_changed': False, 'fabrication_release_allowed': False,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    args.output.write_text(json.dumps(review(), indent=2, sort_keys=True) + '\n')
    print('HDI proposal audited: 1.272 mm listed, 1670 unsupported inner microvias; no source changes')


if __name__ == '__main__':
    main()
