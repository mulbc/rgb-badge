#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Independent unit/axis/corner checks for the read-only converter review."""
import importlib.util
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location('calc', Path(__file__).with_name('calculate-converter-review.py'))
calc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(calc)


class Calculations(unittest.TestCase):
    def test_independent_csv_axes_and_farads(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'curves.csv'
            path.write_text('#one,,#two\nDC Bias[V],Capacitance[F],DC Bias[V],Capacitance[F]\n0,40e-6,0,20e-6\n2,20e-6,5,10e-6\n')
            a, b = calc.curves(path)
            self.assertAlmostEqual(calc.interpolate(a, 1) * 1e6, 30)
            self.assertAlmostEqual(calc.interpolate(b, 1) * 1e6, 18)

    def test_no_extrapolation_or_unordered_axis(self):
        for points, voltage in (([(0, 1), (2, 0)], 3), ([(0, 1), (0, 2)], 0),
                                ([(1, 1), (0, 2)], .5), ([(0, 1), (2, 0)], float('nan'))):
            with self.assertRaises(ValueError):
                calc.interpolate(points, voltage)

    def test_boundary_interpolation(self):
        self.assertEqual(calc.interpolate([(0, 3), (2, 1)], 0), 3)
        self.assertEqual(calc.interpolate([(0, 3), (2, 1)], 2), 1)

    def test_feedback_against_independent_rational_corners(self):
        row = calc.feedback(511, 91)
        self.assertAlmostEqual(row['nominal_pwm_V'], 43 / 13)
        self.assertAlmostEqual(row['static_low_V'], .495 * (1 + 505.89 / 91.91))
        self.assertAlmostEqual(row['static_high_V'], .505 * (1 + 516.11 / 90.09))
        hot = calc.feedback(511, 91, 60)
        self.assertLess(hot['static_low_V'], row['static_low_V'])
        self.assertGreater(hot['static_high_V'], row['static_high_V'])

    def test_resistance_si_units_and_scaling(self):
        # A 1 m long, 1 mm wide, 1 mm thick bar has area 1e-6 m².
        self.assertAlmostEqual(calc.resistance(1000, 1, 1000), .0172)
        r = calc.resistance(10, .2, 35)
        self.assertAlmostEqual(calc.resistance(10, .4, 35), r / 2)
        self.assertAlmostEqual(calc.resistance(10, .2, 35, 80), r * 1.2358)
        with self.assertRaises(ValueError):
            calc.resistance(10, 0, 35)

    def test_boost_energy_and_non_ccm_warning(self):
        row = calc.boost_peak(2, 4, .5, 1, 1e6, 1e-6)
        self.assertEqual(row['average_A'], 1)
        self.assertEqual(row['ripple_pp_A'], 1)
        self.assertEqual(row['peak_A'], 1.5)
        self.assertTrue(row['CCM_nonnegative_current_condition'])
        self.assertFalse(calc.boost_peak(2, 4, .01, 1, 1e6, 1e-6)['CCM_nonnegative_current_condition'])
        with self.assertRaises(ValueError):
            calc.boost_peak(4, 2, .5, 1, 1e6, 1e-6)


if __name__ == '__main__':
    unittest.main()
