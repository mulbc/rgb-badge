# SPDX-License-Identifier: Apache-2.0
"""Fault injection for USB polarity, power domains and source qualification."""

from pathlib import Path
import runpy
import shutil
import subprocess
import tempfile
import unittest
import xml.etree.ElementTree as ET

from fixtures.kicad_cli_stub import controller_coupon_netlist

TOOLS=Path(__file__).resolve().parents[1]
CHECK=runpy.run_path(str(TOOLS/'check-coupon-usb.py'))
COMPLETE=runpy.run_path(str(TOOLS/'check-coupon-controller.py'))
PROJECT=TOOLS.parent/'hardware/coupon/rev-a'


class UsbCaptureTests(unittest.TestCase):
    def project_copy(self):
        td=tempfile.TemporaryDirectory(prefix='rgb-usb-')
        self.addCleanup(td.cleanup)
        target=Path(td.name)/'project'
        shutil.copytree(PROJECT,target,ignore=shutil.ignore_patterns('build','.history'))
        return target

    def test_canonical_source_and_resistor_temperature_interval(self):
        nets=CHECK['check_sources'](PROJECT)
        self.assertEqual(len(nets)+len(CHECK['NC_NAMES']),84)
        lo,hi=CHECK['check_added_libraries'](PROJECT)
        self.assertGreater(lo,855)
        self.assertLess(hi,920)

    def test_wiring_faults_cannot_pass_source_check(self):
        faults=[('USB_CC2','USB_CC1'),                    # incorrect CC short
                ('USB_BC_HOST_DP','USB_BC_HOST_DM'),    # reversed data path
                ('USB_RAW_OUT1','USB_RAW_OUT2'),        # wrong current decode
                ('USB_RAW_CHG_AL_N','USB_RAW_SW_OPEN'), # detection permission confused
                ('USB_BC_VBUS','+3V3_APP'),             # loses autonomous OFF detection
                ('+5V_USB','VBUS_CONNECTOR'),           # bypasses unqualified input stage
                ('USB_D+','USB_CONN_DP')]               # bypasses OFF isolation
        for old,new in faults:
            with self.subTest(old=old):
                project=self.project_copy();p=project/'usb-interface.kicad_sch'
                before=p.read_text();target=f'(global_label "{old}"'
                self.assertIn(target,before)
                p.write_text(before.replace(target,f'(global_label "{new}"',1))
                with self.assertRaises(ValueError):CHECK['check_sources'](project)

    def test_wrong_capacitor_and_resistor_metadata_rejected(self):
        for old,new in [('887k 1%','887R 1%'),('10u 6.3V X5R','100n 16V X7R'),
                        ('(property "Reference" "C37"','(property "Reference" "C99"')]:
            with self.subTest(old=old):
                project=self.project_copy();p=project/'usb-interface.kicad_sch'
                before=p.read_text();self.assertIn(old,before);p.write_text(before.replace(old,new,1))
                with self.assertRaises(ValueError):CHECK['check_sources'](project)

    def test_synthetic_complete_xml_rejects_power_and_isolation_faults(self):
        for ref,pin,net in [('U32','8','+3V3_USB'),('U30','5','GND'),
                            ('U31','3','+3V3_USB'),('U32','3','USB_D+'),('J1','B6','USB_CONN_DM')]:
            with self.subTest(ref=ref,pin=pin),tempfile.TemporaryDirectory() as td:
                root=controller_coupon_netlist()
                node=root.find(f"./nets/net/node[@ref='{ref}'][@pin='{pin}']")
                self.assertIsNotNone(node)
                for parent in root.findall('./nets/net'):
                    if node in list(parent):parent.remove(node);break
                root.find(f"./nets/net[@name='{net}']").append(node)
                p=Path(td)/'bad.xml';p.write_bytes(ET.tostring(root))
                with self.assertRaises(ValueError):COMPLETE['check_netlist'](p)

    def test_missing_no_connect_and_duplicate_pin_rejected(self):
        for fault in ('missing NC','duplicate node'):
            with self.subTest(fault=fault),tempfile.TemporaryDirectory() as td:
                root=controller_coupon_netlist();net=root.find("./nets/net[@name='unconnected-(U31-ADDR-Pad5)']")
                if fault=='missing NC':net.remove(net.find('node'))
                else:ET.SubElement(net,'node',ref='U31',pin='5')
                p=Path(td)/'bad.xml';p.write_bytes(ET.tostring(root))
                with self.assertRaises(ValueError):COMPLETE['check_netlist'](p)

    def test_regeneration_is_exact_and_refuses_overwrite(self):
        with tempfile.TemporaryDirectory() as td:
            out=Path(td)/'new'
            command=['python3',str(TOOLS/'generate-coupon-usb.py'),'--output',str(out)]
            subprocess.run(command,check=True,capture_output=True)
            self.assertEqual((out/'usb-interface.kicad_sch').read_bytes(),(PROJECT/'usb-interface.kicad_sch').read_bytes())
            self.assertNotEqual(subprocess.run(command,capture_output=True).returncode,0)

    def test_connector_and_esd_values_clear_body_outlines(self):
        # Native d502e65 PDF showed the value baseline on each top edge.
        # These independent dimensions are from the controlled symbol bodies.
        source=CHECK['parse'](PROJECT/'usb-interface.kicad_sch')
        symbols={CHECK['props'](s)['Reference']:s for s in CHECK['children'](source,'symbol')}
        for ref,body_top in [('J1',17.78),('U33',10.16)]:
            with self.subTest(ref=ref):
                symbol=symbols[ref]
                y=float(CHECK['one'](symbol,'at','instance')[2])
                value=next(p for p in CHECK['children'](symbol,'property') if p[1]=='Value')
                vy=float(CHECK['one'](value,'at','value')[2])
                self.assertGreaterEqual(round(y-body_top-vy,3),2.54)


if __name__=='__main__':unittest.main()
