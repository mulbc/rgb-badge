#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Static input-protection screening; no transient or fabrication approval.

Divider convention: top from monitored rail to input, bottom to GND.
Positive input leakage flows INTO the IC. Thus rail trip voltage is
Vthreshold * (1 + Rtop/Rbottom) + Ileak * Rtop.
TPS25947 SLVSFC9C table 6.5; see the accompanying capture assessment.
"""
import argparse
from decimal import Decimal as D
from itertools import product
import json


def divider_bounds(top, bottom, threshold, leakage, tolerance):
    top, bottom, tolerance = D(top), D(bottom), D(tolerance)
    threshold = tuple(map(D, threshold))
    leakage = tuple(map(D, leakage))
    if not all(v.is_finite() for v in (top, bottom, tolerance, *threshold, *leakage)):
        raise ValueError('Non-finite divider input')
    if top <= 0 or bottom <= 0 or not 0 <= tolerance < 1:
        raise ValueError('Invalid divider resistance or tolerance')
    if threshold[0] <= 0 or threshold[0] > threshold[1] or leakage[0] > leakage[1]:
        raise ValueError('Invalid threshold or leakage interval')
    values = []
    for a, b, v, current in product((-tolerance, tolerance), (-tolerance, tolerance), threshold, leakage):
        rt, rb = top * (1+a), bottom * (1+b)
        values.append(v * (1+rt/rb) + current * rt)
    return min(values), max(values)


def screening():
    rising = ('1.183', '1.223')
    falling = ('1.076', '1.116')
    leakage = ('-0.0000001', '0.0000001')
    # These are nominal networks for screening, NOT selected resistor MPNs.
    # ±1% is TOTAL error, not permission to use an unqualified 1% resistor.
    ov = divider_bounds('37400', '10000', rising, leakage, '.01')
    recovery = divider_bounds('37400', '10000', falling, leakage, '.01')
    wider_ov = divider_bounds('38300', '10000', rising, leakage, '.01')
    wider_recovery = divider_bounds('38300', '10000', falling, leakage, '.01')
    legacy = divider_bounds('34620', '10000', rising, leakage, '.002')
    pg_rise = divider_bounds('27400', '10000', rising, ('-0.0000001', '0.0000003'), '.01')
    pg_fall = divider_bounds('27400', '10000', falling, ('-0.0000001', '0.0000003'), '.01')
    return {
        'power_good_screen': {
            'monitored_rail': 'protected output, not connector VBUS',
            'divider_nominal_ohm': ['27400', '10000'],
            'rising_v': list(map(str, pg_rise)),
            'falling_v': list(map(str, pg_fall)),
            'pg_off_max_v_at_specified_pullups': '1',
            'receiver_vt_minus_min_at_3v_only': '0.8',
            'direct_off_level_guaranteed_low_at_3v': D('1') < D('0.8'),
            'full_supply_range_or_transient_qualified': False,
        },
        'fixed_clamp_alternative': {
            'candidate': 'TPS259472ARPWR',
            'selection': 'NOT_SELECTED',
            'ovcsel': 'open',
            'clamp_threshold_v': ['5.25', '6.2'],
            'clamped_output_v_at_10ma': ['5.0', '6.12'],
            'u34_operating_max_v': '6.5',
            'threshold_to_u34_headroom_v': str(D('6.5')-D('6.2')),
            'removed_ov_divider_resistors_if_selected': 2,
            'transient_qualified': False,
        },
        'current_threshold_example': {
            'rilm_ohm_table_test_value': '3320',
            'trip_or_limit_a': ['0.850', '1.150'],
            'charger_ceiling_a': '0.9753',
            'guarantees_charger_ceiling_without_limiting_or_trip': D('0.850') > D('0.9753'),
            'includes_resistor_tolerance': False,
        },
        'status': 'SCREENING_ONLY_NOT_CAPTURED',
        'source_normal_max_v': '5.5',
        'candidate': 'TPS259474ARPWR',
        'candidate_ov_trip_v': list(map(str, ov)),
        'candidate_ov_recovery_v': list(map(str, recovery)),
        'wider_ovlo_example': {
            'selection': 'NOT_SELECTED',
            'divider_nominal_ohm': ['38300', '10000'],
            'rising_v': list(map(str, wider_ov)),
            'falling_v': list(map(str, wider_recovery)),
            'normal_5v5_static_margin_min_v': str(wider_ov[0]-D('5.5')),
            'u34_6v5_static_gap_at_max_trip_v': str(D('6.5')-wider_ov[1]),
            'transient_qualified': False,
        },
        'narrow_window_ov_trip_v': list(map(str, legacy)),
        'narrow_window_accepts_5v5': legacy[0] > D('5.5'),
        'candidate_static_window_passes': ov[0] > D('5.5') and ov[1] < D('6.0'),
        'blockers': [
            'OVLO delay/overshoot and exact fault waveform are not bounded by these DC calculations.',
            'Resistor MPNs, total tolerance and assembled drift remain unqualified.',
            'Power-good startup levels, VBUS thresholds, current limit and inrush remain uncaptured.',
            'Physical charger inhibit and complete-port budget remain open.',
        ],
    }


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--require-closure', action='store_true')
    args = p.parse_args()
    result = screening()
    print(json.dumps(result, indent=2))
    return 1 if args.require_closure else 0


if __name__ == '__main__':
    raise SystemExit(main())
