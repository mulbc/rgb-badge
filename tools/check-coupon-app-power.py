#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Check provisional root-linked application-power capture against its generator."""

from pathlib import Path
import runpy
import sys


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / 'hardware/coupon/rev-a'
GEN = runpy.run_path(str(ROOT / 'tools/generate-coupon-app-power.py'))


def check():
    control = (PROJECT / 'app-control.kicad_sch').read_text()
    converter = (PROJECT / '3v3-converter.kicad_sch').read_text()
    if control != GEN['generate_control']():
        raise ValueError('Provisional switch-control sheet differs from deterministic source')
    if converter != GEN['generate_converter']():
        raise ValueError('Root-linked converter sheet differs from deterministic source')
    root = (PROJECT / 'rgb-badge-coupon.kicad_sch').read_text()
    if root.count('(property "Sheetfile" "app-control.kicad_sch"') != 1:
        raise ValueError('Switch-control sheet is not linked exactly once')
    if root.count('(property "Sheetfile" "3v3-converter.kicad_sch"') != 1:
        raise ValueError('Converter sheet is not linked exactly once')
    driver = (PROJECT / 'driver.kicad_sch').read_text()
    if '(property "Reference" "#FLG01"' in driver:
        raise ValueError('Superseded +3V3_APP draft source flag remains in the driver')
    if '(property "Reference" "#FLG07"' in control:
        raise ValueError('Obsolete SYS draft source flag remains after charger OUT capture')
    print('Provisional application-power source check passed: root-linked switch control and 3V3; charger OUT now supplies SYS.')


if __name__ == '__main__':
    try:
        check()
    except (OSError, ValueError) as error:
        print('Application-power check failed: ' + str(error), file=sys.stderr)
        sys.exit(1)
