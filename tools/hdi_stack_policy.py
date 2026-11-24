# SPDX-License-Identifier: Apache-2.0
"""Fail-closed geometric stack/via eligibility; never substitutes for DFM review."""
from decimal import Decimal
import math


def require(condition, message):
    if not condition:
        raise ValueError(message)


def validate_plan(plan):
    require(plan.get('schema_version') == 1, 'unsupported stack schema')
    layers = plan['copper_layers']
    require(len(layers) == 6 and len(set(layers)) == 6, 'six distinct copper layers required')
    require(len(plan['copper_um']) == 6 and len(plan['dielectric_um']) == 5, 'layer dimensions missing')
    for value in plan['copper_um'] + plan['dielectric_um']:
        require(type(value) is int and value > 0, 'positive integer micrometres required')
    total = sum(plan['copper_um']) + sum(plan['dielectric_um'])
    require(total == plan['laminate_and_copper_sum_um'], 'stack thickness sum differs')
    require(plan['finished_target_um'] > 0, 'finished target missing')
    keys = set()
    for rule in plan['via_policies']:
        top, bottom = rule['layers']
        require(top in layers and bottom in layers and layers.index(top) < layers.index(bottom), 'invalid via span')
        key = (rule['kind'], top, bottom)
        require(key not in keys, 'duplicate via policy')
        keys.add(key)
        hole, pad = rule['hole_um'], rule['minimum_pad_um']
        require(type(hole) is int and type(pad) is int and 0 < hole < pad, 'invalid via dimensions')
        require((pad - hole) / 2 >= plan['minimum_nominal_annular_ring_um'], 'annular-ring floor violated')
        require(rule['kind'] in ('microvia', 'buried', 'through'), 'unsupported via kind')
        if rule['kind'] == 'microvia':
            require(layers.index(bottom) - layers.index(top) == 1, 'microvia must be adjacent')
        require(rule['maximum_nominal_dielectric_hole_ratio'] > 0, 'aspect ratio missing')
    # Approval is deliberately unavailable in this tool, including for a clean
    # geometric candidate. A separate controlled release workflow must authorize it.
    require(plan.get('fabrication_release_allowed') is False, 'planning policy cannot grant fabrication')
    return total


def via_findings(plan, via):
    """Return physical geometry failures without waiving unknown spans/kinds."""
    if any(type(via.get(key)) not in (int, float) or not math.isfinite(via[key]) or via[key] <= 0
           for key in ('pad_um', 'hole_um')):
        return ['INVALID_VIA_DIMENSIONS']
    layers = plan['copper_layers']
    rule = next((r for r in plan['via_policies'] if
                 (r['kind'], r['layers']) == (via['kind'], via['layers'])), None)
    if rule is None:
        return ['VIA_KIND_OR_SPAN_NOT_ALLOWED']
    result = []
    if via['hole_um'] != rule['hole_um']:
        result.append('VIA_HOLE_DIFFERS')
    if via['pad_um'] < rule['minimum_pad_um']:
        result.append('VIA_PAD_TOO_SMALL')
    if (via['pad_um'] - via['hole_um']) / 2 < plan['minimum_nominal_annular_ring_um']:
        result.append('ANNULAR_RING_TOO_SMALL')
    top, bottom = map(layers.index, via['layers'])
    # An explicitly nominal dielectric-depth screen; supplier depth conventions
    # and copper/interfaces/plating are separately unqualified.
    depth = sum(plan['dielectric_um'][top:bottom])
    if Decimal(depth) > Decimal(str(rule['maximum_nominal_dielectric_hole_ratio'])) * Decimal(via['hole_um']):
        result.append('NOMINAL_ASPECT_RATIO_EXCEEDED')
    return result
