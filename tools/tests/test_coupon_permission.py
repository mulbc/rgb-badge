# SPDX-License-Identifier: Apache-2.0
"""Circuit faults must fail even when a static abstract policy still passes."""

from copy import deepcopy
from pathlib import Path
import runpy
import shutil
import subprocess
import tempfile
import unittest
import xml.etree.ElementTree as ET

from fixtures.kicad_cli_stub import controller_coupon_netlist

TOOLS=Path(__file__).resolve().parents[1]
CHECK=runpy.run_path(str(TOOLS/'check-coupon-permission.py'))
COMPLETE=runpy.run_path(str(TOOLS/'check-coupon-controller.py'))
PROJECT=TOOLS.parent/'hardware/coupon/rev-a'


class PermissionCaptureTests(unittest.TestCase):
    def test_canonical_sources_and_16_logic_cases(self):
        CHECK['check_sources'](PROJECT)

    def test_gate_evaluation_catches_dangerous_connections_independently(self):
        original=CHECK['trace_sources'](PROJECT)
        cases=[(('U17','6'),'+3V3_USB'),
               (('U17','3'),'+3V3_USB'),
               (('U17','1'),'+3V3_USB'),
               (('U23','2'),'USB_OUT1')]
        for node,net in cases:
            with self.subTest(node=node,net=net):
                bad=deepcopy(original);bad[node]=net
                with self.assertRaises(ValueError):CHECK['check_logic'](bad)

    def test_unattached_defaults_and_off_charging(self):
        nets=CHECK['trace_sources'](PROJECT)
        detached=CHECK['evaluate'](nets,(1,1,1,1))
        self.assertFalse(detached['USB_CHARGE_REQ'])
        self.assertTrue(detached['USB_EN1_RAW_N'])
        charging=CHECK['evaluate'](nets,(0,1,1,1))
        self.assertTrue(charging['USB_CHARGE_REQ'])
        self.assertFalse(charging['USB_EN1_RAW_N'])

    def test_out2_diagnostic_pad_must_terminate_buffer_output(self):
        project=self.project_copy()
        path=project/'usb-conditioning.kicad_sch'
        source=path.read_text()
        # The final OUT2 label is TP21, after the U24 buffer output label.
        before, label, after=source.rpartition('(global_label "USB_OUT2"')
        self.assertTrue(label)
        path.write_text(before+'(global_label "USB_RAW_OUT2"'+after)
        with self.assertRaises(ValueError):CHECK['check_sources'](project)

    def project_copy(self):
        temporary=tempfile.TemporaryDirectory(prefix='rgb-permission-')
        self.addCleanup(temporary.cleanup)
        target=Path(temporary.name)/'project'
        shutil.copytree(PROJECT,target,ignore=shutil.ignore_patterns('build','.history'))
        return target

    def test_canonical_wiring_and_population_faults(self):
        cases=[
            ('usb-permission.kicad_sch','(global_label "USB_CHARGE_REQ"','(global_label "USB_USB_REQUEST"'),
            ('usb-conditioning.kicad_sch','(property "Value" "10k 1%"','(property "Value" "100k 1%"'),
            ('usb-conditioning.kicad_sch','(xy 73.660 73.660)','(xy 73.661 73.660)'),
            ('usb-permission.kicad_sch','(property "Reference" "C11"','(property "Reference" "C99"'),
            ('usb-permission.kicad_sch','(no_connect (at 68.580 73.660)','(no_connect (at 68.590 73.660)'),
        ]
        for filename,old,new in cases:
            with self.subTest(old=old):
                project=self.project_copy();path=project/filename
                text=path.read_text();self.assertIn(old,text)
                path.write_text(text.replace(old,new,1))
                with self.assertRaises(ValueError):CHECK['check_sources'](project)

    def test_complete_xml_rejects_missing_capacitor_and_firmware_boost_route(self):
        for fault in ('missing capacitor','firmware boost'):
            with self.subTest(fault=fault),tempfile.TemporaryDirectory() as directory:
                root=controller_coupon_netlist()
                if fault=='missing capacitor':
                    root.find('components').remove(root.find("./components/comp[@ref='C17']"))
                else:
                    node=root.find("./nets/net/node[@ref='U17'][@pin='6']")
                    for net in root.findall('./nets/net'):
                        if node in list(net):net.remove(node);break
                    root.find("./nets/net[@name='+3V3_USB']").append(node)
                path=Path(directory)/'bad.xml';path.write_bytes(ET.tostring(root))
                with self.assertRaises(ValueError):COMPLETE['check_netlist'](path)

    def test_regeneration_matches_canonical_and_refuses_overwrite(self):
        with tempfile.TemporaryDirectory() as directory:
            output=Path(directory)/'new'
            command=['python3',str(TOOLS/'generate-coupon-permission.py'),'--output',str(output)]
            subprocess.run(command,check=True,capture_output=True)
            for filename in CHECK['SHEETS']:
                self.assertEqual((output/filename).read_bytes(),(PROJECT/filename).read_bytes())
            failed=subprocess.run(command,capture_output=True)
            self.assertNotEqual(failed.returncode,0)


if __name__=='__main__':unittest.main()
