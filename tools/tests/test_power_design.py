# SPDX-License-Identifier: Apache-2.0
"""Tests for the Coupon Rev A power pre-capture calculations."""

from decimal import Decimal as D
from pathlib import Path
import runpy
import subprocess
import sys
import unittest


CHECK = runpy.run_path(str(Path(__file__).resolve().parents[1] / "check-power-design.py"))


class PowerDesignTests(unittest.TestCase):
    def test_historical_passive_resistor_is_outside_programming_range(self):
        with self.assertRaisesRegex(ValueError, "outside the documented"):
            CHECK["validate_bq_unknown_input"]("1000", "0.5")

    def test_in_range_setting_still_exceeds_usb_host_budgets(self):
        for permitted in ("0.1", "0.5"):
            with self.subTest(permitted=permitted), self.assertRaisesRegex(ValueError, "exceeds"):
                CHECK["validate_bq_unknown_input"]("950", permitted)

    def test_high_branch_requires_sufficient_source_and_unknown_classification(self):
        resistance = CHECK["parallel"]("1000", "665")
        low, nominal, high = CHECK["validate_bq_unknown_input"](resistance, "1.5")
        self.assertEqual(nominal, D("478") / resistance)
        self.assertLess(low, nominal)
        self.assertLess(high, D("1.5"))
        with self.assertRaisesRegex(ValueError, "exceeds"):
            CHECK["validate_bq_unknown_input"](resistance, "0.5")
        for source in ("SDP", "CDP", "DCP"):
            with self.subTest(source=source), self.assertRaisesRegex(ValueError, "BC1.2"):
                CHECK["validate_bq_unknown_input"](resistance, "1.5", classification=source)

    def test_usb_closure_gate_rejects_current_incomplete_design(self):
        script = Path(__file__).resolve().parents[1] / "check-power-design.py"
        result = subprocess.run([sys.executable, str(script), "--require-usb-closure"],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 1)
        self.assertIn("USB/input capture remains BLOCKED", result.stdout)

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
