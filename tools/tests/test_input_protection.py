# SPDX-License-Identifier: Apache-2.0
"""Independent analytic checks for voltage-divider screening."""
from decimal import Decimal as D
from pathlib import Path
import runpy
import subprocess
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'check-input-protection.py'
CHECK = runpy.run_path(str(SCRIPT))


class InputProtectionTests(unittest.TestCase):
    def test_exact_divider_and_leakage_sign(self):
        # Equal 10k resistors: 1V reference -> 2V trip, +1uA adds 10mV.
        self.assertEqual(CHECK['divider_bounds']('10000','10000',('1','1'),('0.000001','0.000001'),'0'), (D('2.01'),D('2.01')))
        self.assertEqual(CHECK['divider_bounds']('10000','10000',('1','1'),('-0.000001','0.000001'),'0'), (D('1.99'),D('2.01')))

    def test_opposite_resistor_corners(self):
        lo, hi = CHECK['divider_bounds']('10000','10000',('1','1'),('0','0'),'.1')
        self.assertEqual(lo, D(1)+D(9)/D(11))
        self.assertEqual(hi, D(1)+D(11)/D(9))

    def test_legacy_window_cannot_accept_full_normal_source_range(self):
        s = CHECK['screening']()
        self.assertFalse(s['narrow_window_accepts_5v5'])
        self.assertTrue(s['candidate_static_window_passes'])
        self.assertTrue(s['blockers'])
        lo, hi = map(D,s['candidate_ov_trip_v'])
        self.assertGreater(lo,D('5.516'))
        self.assertLess(hi,D('5.894'))

    def test_total_tolerance_cannot_be_relaxed_to_two_percent(self):
        lo, hi=CHECK['divider_bounds']('37400','10000',('1.183','1.223'),('-0.0000001','0.0000001'),'.02')
        self.assertLess(lo,D('5.5'))

    def test_ovlo_recovery_is_evaluated_against_falling_threshold(self):
        # Once OVLO trips, VBUS must fall BELOW the falling threshold to recover.
        # At a steady 5.0 V every screened corner permits recovery; at 5.5 V
        # none guarantees it. This does not bound response time or noise.
        low, high = map(D, CHECK['screening']()['candidate_ov_recovery_v'])
        self.assertLess(D('5.0'), low)
        self.assertGreater(D('5.5'), high)

    def test_pg_leakage_is_asymmetric_and_not_ovlo_leakage(self):
        a=CHECK['divider_bounds']('27400','10000',('1.183','1.223'),('-0.0000001','0.0000003'),'.01')
        b=CHECK['divider_bounds']('27400','10000',('1.183','1.223'),('-0.0000001','0.0000001'),'.01')
        self.assertEqual(a[0],b[0])
        self.assertEqual(a[1]-b[1],D('0.0055348'))

    def test_new_supply_does_not_turn_clamp_screen_into_qualification(self):
        s=CHECK['screening']()
        self.assertEqual(s['fixed_clamp_alternative']['threshold_to_u34_headroom_v'],'0.3')
        self.assertFalse(s['fixed_clamp_alternative']['transient_qualified'])
        self.assertFalse(s['power_good_screen']['direct_off_level_guaranteed_low_at_3v'])
        self.assertFalse(s['current_threshold_example']['guarantees_charger_ceiling_without_limiting_or_trip'])

    def test_invalid_intervals_rejected(self):
        for args in [('NaN','10',('1','2'),('0','0'),'0'),('10','10',('1','Infinity'),('0','0'),'0'),('-1','10',('1','2'),('0','0'),'0'),('10','0',('1','2'),('0','0'),'0'),('10','10',('1','2'),('0','0'),'1'),('10','10',('2','1'),('0','0'),'0')]:
            with self.subTest(args=args),self.assertRaises(ValueError): CHECK['divider_bounds'](*args)

    def test_dc_success_is_not_closure(self):
        r=subprocess.run(['python3',str(SCRIPT),'--require-closure'],capture_output=True,text=True)
        self.assertEqual(r.returncode,1)
        self.assertIn('SCREENING_ONLY_NOT_CAPTURED',r.stdout)
