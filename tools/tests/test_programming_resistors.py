# SPDX-License-Identifier: Apache-2.0
"""Reject programming-resistor error and exact-library regressions."""

from decimal import Decimal as D
from pathlib import Path
import runpy
import shutil
import tempfile
import unittest

TOOLS = Path(__file__).resolve().parents[1]
AUDIT = runpy.run_path(str(TOOLS / 'check-programming-resistors.py'))
PROJECT = TOOLS.parent / 'hardware/coupon/rev-a'


class ProgrammingResistorTests(unittest.TestCase):
    def test_multiplicative_allocations_fit_total_envelope(self):
        self.assertEqual(AUDIT['check_budget'](),
                         (D('.992389741875'), D('1.007639758125')))

    def test_generic_resistor_and_excess_service_drift_rejected(self):
        for kwargs in ({'tolerance': '.01', 'tcr': '.0001', 'drift': '0'},
                       {'drift': '.01'}):
            with self.subTest(kwargs=kwargs), self.assertRaises(ValueError):
                AUDIT['check_budget'](**kwargs)

    def test_invalid_error_inputs_rejected(self):
        for key in ('tolerance', 'tcr', 'delta_t', 'drift'):
            for value in ('-1', 'NaN', 'Infinity'):
                with self.subTest(key=key, value=value), self.assertRaises(ValueError):
                    AUDIT['resistance_factors'](**{key: value})
        with self.assertRaises(ValueError):
            AUDIT['resistance_factors'](tcr='.1')

    def test_exact_libraries_pass(self):
        AUDIT['check_libraries'](PROJECT)

    def test_wrong_metadata_pin_and_land_geometry_rejected(self):
        symbol = 'symbols/rgb-badge-coupon.kicad_sym'
        footprint = 'footprints/rgb-badge-coupon.pretty/R_Panasonic_ERA2_0402.kicad_mod'
        mutations = [
            (symbol, 'RDM0000/AOA0000C307.pdf', 'RDA0000/AOA0000C304.pdf'),
            (symbol, '(number "1"', '(number "3"'),
            (footprint, '(size 0.5 0.5)', '(size 0.6 0.5)'),
            (footprint, '(end 1 0.55)', '(end 1 0.5)'),
        ]
        for name, old, new in mutations:
            with self.subTest(old=old), tempfile.TemporaryDirectory() as td:
                project = Path(td)
                for folder in ('symbols', 'footprints'):
                    shutil.copytree(PROJECT / folder, project / folder)
                path = project / name
                text = path.read_text()
                # Mutate only the new part, not its audited reference template.
                start = text.index('(symbol "ERA2AEB3651X"') if name == symbol else 0
                self.assertIn(old, text[start:])
                path.write_text(text[:start] + text[start:].replace(old, new, 1))
                with self.assertRaises(ValueError):
                    AUDIT['check_libraries'](project)


if __name__ == '__main__':
    unittest.main()
