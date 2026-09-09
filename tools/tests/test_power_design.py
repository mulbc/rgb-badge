# SPDX-License-Identifier: Apache-2.0
"""Tests for the Coupon Rev A power pre-capture calculations."""

from decimal import Decimal as D
from pathlib import Path
import runpy
import unittest


CHECK = runpy.run_path(str(Path(__file__).resolve().parents[1] / "check-power-design.py"))


class PowerDesignTests(unittest.TestCase):
    def test_frozen_results(self):
        result = CHECK["check"]()
        self.assertEqual(result["always_on_max_uA"], D("20"))
        self.assertEqual(result["off_budget_remaining_uA"], D("30"))

    def test_ratio_worst_cases_use_opposite_resistor_tolerances(self):
        low, nominal, high = CHECK["bounded_ratio"]("459", "500", "1000", "0.01")
        self.assertLess(low, nominal)
        self.assertLess(nominal, high)
        self.assertEqual(low, D("459") / D("1010"))
        self.assertEqual(high, D("500") / D("990"))

    def test_parallel_branch(self):
        self.assertEqual(CHECK["parallel"]("1000", "665"), D("665000") / D("1665"))

    def test_rail_dividers(self):
        self.assertAlmostEqual(float(CHECK["divider"]("0.5", "511000", "91000")), 3.3076923)
        self.assertAlmostEqual(float(CHECK["divider"]("0.5", "1240000", "180000")), 3.9444444)


if __name__ == "__main__":
    unittest.main()
