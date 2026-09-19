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


def pins(tc='default', **overrides):
    a,b=GPIO['TYPE_C_PINS'][tc]
    return dict(out1=a,out2=b,vbus_valid=True,logic_ready=True)|overrides

class UsbPermissionTests(unittest.TestCase):
    def test_all_gpio_and_domain_combinations(self):
        self.assertEqual(GPIO['check'](),16)

    def test_only_advertised_type_c_sources_can_charge(self):
        for tc in GPIO['TYPE_C_PINS']:
            self.assertEqual(GPIO['permission'](**pins(tc))['charge'],tc in ('1.5A','3A'))

    def test_either_invalid_supply_inhibits_both_supported_sources(self):
        for tc,field in product(('1.5A','3A'),('vbus_valid','logic_ready')):
            self.assertFalse(GPIO['permission'](**pins(tc,**{field:False}))['charge'])

    def test_advertisement_reduction_selects_standby(self):
        self.assertTrue(GPIO['permission'](**pins('1.5A'))['charge'])
        self.assertEqual(GPIO['permission'](**pins('default'))['mode'],'standby')

    def test_application_or_bc_grant_is_not_an_input(self):
        for field in ('usb_request','switch_on','esp_running','chg_det','chg_al_n','sw_open'):
            with self.subTest(field=field), self.assertRaises(TypeError):
                GPIO['permission'](**(pins()|{field:True}))

    def test_unresolved_gpio_is_rejected(self):
        for bad in (None,'0',2,0.0,False):
            with self.assertRaises(ValueError):GPIO['permission'](**pins(out1=bad))


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
