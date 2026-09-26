# SPDX-License-Identifier: Apache-2.0
"""Corner arithmetic and fault rejection for staged USB rail supervision."""

from decimal import Decimal as D
from pathlib import Path
import runpy
import shutil
import tempfile
import unittest
import xml.etree.ElementTree as ET

from fixtures.kicad_cli_stub import controller_coupon_netlist

TOOLS=Path(__file__).resolve().parents[1]
CALC=runpy.run_path(str(TOOLS/'check-usb-supervision.py'))
SOURCE=runpy.run_path(str(TOOLS/'check-coupon-permission.py'))
COMPLETE=runpy.run_path(str(TOOLS/'check-coupon-controller.py'))
POWER=runpy.run_path(str(TOOLS/'check-power-design.py'))
PROJECT=TOOLS.parent/'hardware/coupon/rev-a'


class SupervisionTests(unittest.TestCase):
    def test_temperature_scales_actual_resistance_and_rejects_bad_inputs(self):
        lo,hi=CALC['resistor_interval']('100000')
        self.assertEqual(lo,D('98356.500000'))
        self.assertEqual(hi,D('101656.500000'))
        for value in ('0','-1','NaN','Infinity'):
            with self.subTest(value=value),self.assertRaises(ValueError):
                CALC['resistor_interval'](value)

    def test_threshold_corners_fit_static_window_but_high_divider_does_not(self):
        low,high,rise=CALC['check'](PROJECT)
        self.assertTrue(D('2.762')<low<D('2.763'))
        self.assertTrue(D('3.075')<high<D('3.077'))
        self.assertTrue(D('3.167')<rise<D('3.169'))
        self.assertGreater(CALC['threshold_bounds']('680000')[2],D('3.3'))
        self.assertLess(CALC['threshold_bounds']('560000')[0],D('2.7'))

    def test_wrong_supervisor_supply_sense_and_ct_paths_rejected(self):
        for old,new in [('(global_label "+5V_USB"','(global_label "+3V3_APP"'),
                        ('(global_label "USB_LOGIC_SENSE"','(global_label "+3V3_USB"'),
                        ('(global_label "USB_LOGIC_CT"','(global_label "GND"'),
                        ('(property "Value" "620k 1%"','(property "Value" "680k 1%"')]:
            with self.subTest(old=old),tempfile.TemporaryDirectory() as td:
                project=Path(td)/'project'
                shutil.copytree(PROJECT,project,ignore=shutil.ignore_patterns('build','.history'))
                path=project/'usb-conditioning.kicad_sch';text=path.read_text()
                self.assertIn(old,text);path.write_text(text.replace(old,new,1))
                with self.assertRaises(ValueError):SOURCE['check_sources'](project)

    def test_synthetic_xml_rejects_missing_supervisor_bypass_capacitor(self):
        with tempfile.TemporaryDirectory() as td:
            root=controller_coupon_netlist()
            root.find('components').remove(root.find("./components/comp[@ref='C38']"))
            path=Path(td)/'bad.xml';path.write_bytes(ET.tostring(root))
            with self.assertRaises(ValueError):COMPLETE['check_netlist'](path)

    def test_old_current_margin_is_not_temperature_qualification(self):
        result=POWER['results']()
        self.assertLess(result['configured_sdp_allocated_total'],D('.5'))
        self.assertGreater(result['sdp_temperature_counterexample'],D('.501'))
        self.assertTrue(any('temperature' in text for text in POWER['usb_capture_blockers']()))


if __name__=='__main__':unittest.main()
