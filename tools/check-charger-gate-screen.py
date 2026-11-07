#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Static ADR 0026 E1-EN divider screen; not a startup or hardware proof."""

from decimal import Decimal as D
from itertools import product


def resistance_bounds(nominal):
    r = D(nominal)
    # ±1% initial resistance and ±100 ppm/K across 65 K, multiplicatively.
    return r * D('0.99') * D('0.9935'), r * D('1.01') * D('1.0065')


def node_bounds(rail, signed_leakage):
    """Return all divider corners; positive current enters EN."""
    rail, signed_leakage = D(rail), D(signed_leakage)
    values = []
    for top, bottom in product(resistance_bounds('220000'), resistance_bounds('270000')):
        values.append((rail / top + signed_leakage) / (1 / top + 1 / bottom))
    return min(values), max(values)


def check():
    # 1.6 uA is an explicit provisional aggregate allowance, not a guaranteed
    # bound for the three AUP outputs and TPS259474 across partial supply.
    allowed = D('0.0000016')
    enabled_min = node_bounds('3.0', -allowed)[0]
    early_max = node_bounds('1.65', allowed)[1]
    if enabled_min <= D('1.223') or early_max >= D('1.183'):
        raise ValueError('Selected E1 divider fails the conditional static threshold screen')
    pull_up_at_0v8 = D('0.8') / resistance_bounds('220000')[0]
    return enabled_min, early_max, pull_up_at_0v8


if __name__ == '__main__':
    high, early, current = check()
    print(f'E1 EN conditional DC screen: >= {high:.4f} V at 3.0 V rail; <= {early:.4f} V at 1.65 V rail; 0.8 V pull-up <= {current * D(1000000):.3f} uA.')
    print('Assumed 1.6 uA aggregate leakage; no partial-rail, transient or hardware qualification.')
