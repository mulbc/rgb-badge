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
    def test_actuator_shared_rail_corner_and_ron_envelope(self):
        result = CHECK['actuator_supply_screen']()
        self.assertEqual(result['charger_fall_min_v'], D('2.9'))
        self.assertEqual(result['rise_static_margin_v'], D('0.5'))
        self.assertEqual(result['fall_remaining_margin_v'], D('0.2'))
        self.assertEqual(result['ron_supply_gap_at_fall_v'], D('1.6'))

    def test_actuator_drop_and_delay_can_exhaust_static_margin(self):
        result = CHECK['actuator_supply_screen'](local_drop_v='.05',
            fall_slew_v_per_us='.01', response_us='20')
        self.assertEqual(result['fall_remaining_margin_v'], D('-.05'))
        self.assertEqual(CHECK['actuator_supply_screen'](
            local_drop_v='.2')['fall_remaining_margin_v'], D('0'))
        for value in ('-.1', 'NaN', 'Infinity'):
            with self.subTest(value=value), self.assertRaises(ValueError):
                CHECK['actuator_supply_screen'](response_us=value)

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
        self.assertEqual(result["always_on_max_uA"], D("11.5"))
        self.assertEqual(result["off_budget_remaining_uA"], D("38.5"))

    def test_off_charging_requires_hardware_qualified_source(self):
        for type_c, bc12 in (("default", "SDP"), ("default", "none"),
                             ("default", "unclassified")):
            with self.subTest(type_c=type_c, bc12=bc12):
                state = CHECK["selected_usb_state"](switch_on=False, type_c=type_c, bc12=bc12)
                self.assertEqual(state["mode"], "standby")
                self.assertFalse(state["data_connected"])
        for type_c, bc12 in (("default", "CDP"), ("default", "DCP"),
                             ("default", "dedicated"), ("1.5A", "none"), ("3A", "SDP")):
            with self.subTest(type_c=type_c, bc12=bc12):
                state = CHECK["selected_usb_state"](switch_on=False, type_c=type_c, bc12=bc12)
                self.assertEqual(state["mode"], "external-ilim")
                self.assertIn(state["permission"], ("bc1.2-hardware", "type-c-hardware"))
                self.assertFalse(state["data_connected"])

    def test_sdp_requires_on_configured_and_unsuspended(self):
        cases = (
            (False, False, False, "standby"),
            (True, False, False, "standby"),
            (True, True, True, "standby"),
            (True, True, False, "external-low"),
        )
        for switch_on, configured, suspended, expected in cases:
            with self.subTest(switch_on=switch_on, configured=configured, suspended=suspended):
                state = CHECK["selected_usb_state"](
                    switch_on=switch_on, type_c="default", bc12="SDP",
                    configured=configured, suspended=suspended)
                self.assertEqual(state["mode"], expected)

    def test_hardware_high_current_has_priority_and_survives_suspend(self):
        for type_c, bc12 in (("1.5A", "SDP"), ("3A", "SDP"), ("default", "CDP")):
            with self.subTest(type_c=type_c, bc12=bc12):
                state = CHECK["selected_usb_state"](
                    switch_on=True, type_c=type_c, bc12=bc12,
                    configured=True, suspended=True)
                self.assertEqual(state["mode"], "external-ilim")
                self.assertNotEqual(state["permission"], "usb-stack")

    def test_data_isolated_while_off_and_on_for_data_ports(self):
        for switch_on in (False, True):
            for bc12 in ("SDP", "CDP", "DCP"):
                with self.subTest(switch_on=switch_on, bc12=bc12):
                    state = CHECK["selected_usb_state"](
                        switch_on=switch_on, type_c="default", bc12=bc12)
                    self.assertEqual(state["data_connected"], switch_on and bc12 in ("SDP", "CDP"))

    def test_good_bat_does_not_time_out_off_state_charging(self):
        for bc12 in ("SDP", "CDP", "DCP", "dedicated", "unclassified"):
            with self.subTest(bc12=bc12):
                state = CHECK["selected_usb_state"](
                    switch_on=False, type_c="default", bc12=bc12)
                self.assertTrue(state["good_bat"])
                self.assertFalse(state["app_data_isolator_powered"])
                self.assertFalse(state["data_connected"])

    def test_application_data_isolator_tracks_physical_switch(self):
        for switch_on in (False, True):
            with self.subTest(switch_on=switch_on):
                state = CHECK["selected_usb_state"](
                    switch_on=switch_on, type_c="default", bc12="CDP")
                self.assertEqual(state["app_data_isolator_powered"], switch_on)

        detached = CHECK["selected_usb_state"](
            switch_on=True, type_c="none", bc12="none")
        self.assertTrue(detached["app_data_isolator_powered"])
        self.assertFalse(detached["good_bat"])
        self.assertFalse(detached["data_connected"])

    def test_unattached_rejects_impossible_protocol_state(self):
        state = CHECK["selected_usb_state"](switch_on=False, type_c="none", bc12="none")
        self.assertEqual(state["mode"], "input-asleep")
        with self.assertRaisesRegex(ValueError, "without an attached"):
            CHECK["selected_usb_state"](switch_on=True, type_c="none", bc12="SDP")

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
