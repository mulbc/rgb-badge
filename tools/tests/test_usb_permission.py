# SPDX-License-Identifier: Apache-2.0
"""Detector GPIO regression cases and total-port budget boundaries."""

from decimal import Decimal as D
from itertools import product
from pathlib import Path
import runpy
import unittest


TOOLS = Path(__file__).resolve().parents[1]
GPIO = runpy.run_path(str(TOOLS / "check-usb-permission.py"))
POLICY = runpy.run_path(str(TOOLS / "check-power-design.py"))


def pins(tc="default", bc="SDP", **overrides):
    out1, out2 = GPIO["TYPE_C_PINS"][tc]
    allowed, detected, opened = GPIO["BC12_PINS"][bc]
    return dict(out1=out1, out2=out2, chg_al_n=allowed, chg_det=detected,
                sw_open=opened, vbus_valid=True, logic_ready=True,
                switch_on=True, esp_running=True, usb_request=True) | overrides


class UsbPermissionTests(unittest.TestCase):
    def test_all_gpio_and_domain_combinations(self):
        self.assertEqual(GPIO["check"](), 1024)

    def test_manufacturer_encodings_agree_with_product_policy(self):
        for tc, bc, on, configured, suspended in product(
                ("default", "1.5A", "3A"), GPIO["BC12_PINS"],
                (False, True), (False, True), (False, True)):
            with self.subTest(tc=tc, bc=bc, on=on, cfg=configured, suspend=suspended):
                expected = POLICY["selected_usb_state"](
                    switch_on=on, type_c=tc, bc12=bc,
                    configured=configured, suspended=suspended)
                actual = GPIO["permission"](**pins(tc, bc, switch_on=on,
                                                   usb_request=configured and not suspended))
                mode = "external-high" if expected["mode"] == "external-ilim" else expected["mode"]
                self.assertEqual(actual["mode"], mode)
                self.assertEqual((actual["en2"], actual["en1"]), (expected["en2"], expected["en1"]))

    def test_charger_detect_alone_never_grants_bc12_high_current(self):
        result = GPIO["permission"](**pins(chg_al_n=1, chg_det=1))
        self.assertEqual(result["mode"], "standby")

    def test_low_current_non_data_charger_cannot_impersonate_sdp(self):
        self.assertEqual(GPIO["permission"](**pins(bc="unclassified"))["mode"], "standby")

    def test_detach_brownout_and_reset_with_stale_request(self):
        for changes in ({"vbus_valid": False}, {"logic_ready": False},
                        {"out1": 1, "out2": 1}, {"esp_running": False},
                        {"switch_on": False}, {"usb_request": False}):
            state = GPIO["permission"](**pins(**changes))
            self.assertIn(state["mode"], ("standby", "input-asleep"))
            self.assertFalse(state["boost"])

    def test_hardware_charge_survives_application_reset(self):
        for tc, bc in (("1.5A", "SDP"), ("3A", "none"), ("default", "CDP")):
            state = GPIO["permission"](**pins(tc, bc, esp_running=False, switch_on=False, usb_request=False))
            self.assertEqual(state["mode"], "external-high")

    def test_advertisement_reduction_removes_boost(self):
        before = GPIO["permission"](**pins("1.5A"))
        after = GPIO["permission"](**pins("default"))
        self.assertTrue(before["boost"])
        self.assertFalse(after["boost"])
        self.assertEqual(after["mode"], "external-low")
        # Without a valid stack grant the reduced advertisement selects standby.
        self.assertEqual(GPIO["permission"](**pins("default", usb_request=False))["mode"], "standby")

    def test_unresolved_gpio_is_not_silently_treated_as_permission(self):
        for bad in (None, "0", 2, 0.0):
            with self.assertRaises(ValueError):
                GPIO["permission"](**pins(out1=bad))


class UsbBudgetTests(unittest.TestCase):
    def test_fixed_usb500_leaves_no_auxiliary_headroom(self):
        self.assertGreater(POLICY["total_usb_current"]("0.5", "0.000001"), D("0.5"))

    def test_low_ilim_uses_low_range_factor_and_reserves_current(self):
        low, nominal, high = POLICY["selected_input_bounds"]()
        self.assertEqual(low, D("1330") / (D("3650") * D("1.01")))
        self.assertEqual(nominal, D("1525") / D("3650"))
        self.assertEqual(high, D("1720") / (D("3650") * D("0.99")))
        self.assertLess(POLICY["total_usb_current"](high, "0.020", "0.002"), D("0.5"))
        self.assertGreater(POLICY["total_usb_current"](high, "0.025"), D("0.5"))

    def test_boost_resistor_tolerance_corners_and_old_ceiling(self):
        lo, _, hi = POLICY["selected_input_bounds"](boost=True)
        for base, branch, k in product((D("3613.5"), D("3686.5")),
                                       (D("3445.2"), D("3514.8")), (D("1500"), D("1720"))):
            current = k * (1 / base + 1 / branch)
            self.assertGreaterEqual(current + D("1e-25"), lo)
            self.assertLessEqual(current - D("1e-25"), hi)
        self.assertLessEqual(hi, D("1720") / (D("1780") * D("0.99")))

    def test_on_resistance_only_reduces_high_current(self):
        ideal = POLICY["selected_input_bounds"](boost=True)
        lossy = POLICY["selected_input_bounds"](boost=True, switch_resistance_max="20")
        self.assertLess(lossy[0], ideal[0])
        self.assertEqual(lossy[2], ideal[2])
        with self.assertRaises(ValueError):
            POLICY["selected_input_bounds"](boost=True, switch_resistance_max="100000")

    def test_budget_cannot_hide_negative_or_nonfinite_loads(self):
        for bad in ("-0.001", "NaN", "Infinity"):
            with self.assertRaises(ValueError):
                POLICY["total_usb_current"]("0.5", bad)


if __name__ == "__main__":
    unittest.main()
