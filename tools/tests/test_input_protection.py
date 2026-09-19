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

    def test_invalid_intervals_rejected(self):
        for args in [('NaN','10',('1','2'),('0','0'),'0'),('10','10',('1','Infinity'),('0','0'),'0'),('-1','10',('1','2'),('0','0'),'0'),('10','0',('1','2'),('0','0'),'0'),('10','10',('1','2'),('0','0'),'1'),('10','10',('2','1'),('0','0'),'0')]:
            with self.subTest(args=args),self.assertRaises(ValueError): CHECK['divider_bounds'](*args)

    def test_dc_success_is_not_closure(self):
        r=subprocess.run(['python3',str(SCRIPT),'--require-closure'],capture_output=True,text=True)
        self.assertEqual(r.returncode,1)
        self.assertIn('SCREENING_ONLY_NOT_CAPTURED',r.stdout)
