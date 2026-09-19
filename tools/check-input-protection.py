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
    legacy = divider_bounds('34620', '10000', rising, leakage, '.002')
    return {
        'status': 'SCREENING_ONLY_NOT_CAPTURED',
        'source_normal_max_v': '5.5',
        'candidate': 'TPS259474ARPWR',
        'candidate_ov_trip_v': list(map(str, ov)),
        'candidate_ov_recovery_v': list(map(str, recovery)),
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
