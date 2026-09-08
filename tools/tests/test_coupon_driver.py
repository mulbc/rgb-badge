# SPDX-License-Identifier: Apache-2.0
"""Fault injection for the new driver and its complete netlist contract."""
from copy import deepcopy
from pathlib import Path
import runpy
import shutil
import tempfile
import unittest
import xml.etree.ElementTree as ET
from fixtures.kicad_cli_stub import coupon_netlist

TOOLS=Path(__file__).resolve().parents[1]
CHECK=runpy.run_path(str(TOOLS/'check-coupon-driver.py'))
PROJECT=TOOLS.parent/'hardware/coupon/rev-a'

class CouponDriverTests(unittest.TestCase):
    def test_readback_has_physical_probe_connection(self):
        # A one-pin labelled net produced native KiCad isolated_pin_label.
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'probe.xml';p.write_bytes(ET.tostring(coupon_netlist()))
            CHECK['check_netlist'](p)
            root=ET.parse(p).getroot()
            nodes=root.findall("./nets/net[@name='LED_SOUT']/node")
            self.assertEqual({(n.get('ref'),n.get('pin')) for n in nodes}, {('U1','42'),('TP1','1')})
            net=root.find("./nets/net[@name='LED_SOUT']")
            net.remove(net.find("node[@ref='TP1']"))
            p.write_bytes(ET.tostring(root))
            with self.assertRaises(ValueError):CHECK['check_netlist'](p)

    def test_current_sources(self):
        CHECK['check_sources'](PROJECT)

    def test_complete_synthetic_netlist(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'fixture.xml';p.write_bytes(ET.tostring(coupon_netlist()))
            CHECK['check_netlist'](p)

    def test_netlist_faults(self):
        for fault in ('missing driver','swapped outputs','ground pad removed','IREF short','resistor decade','extra component','duplicate pin'):
            with self.subTest(fault=fault),tempfile.TemporaryDirectory() as d:
                root=coupon_netlist()
                if fault=='missing driver':
                    root.find('components').remove(root.find("./components/comp[@ref='U1']"))
                elif fault=='swapped outputs':
                    for node in root.findall('./nets/net/node'):
                        if node.get('ref')=='U1' and node.get('pin') in {'8','9'}:node.set('pin',{'8':'9','9':'8'}[node.get('pin')])
                elif fault=='ground pad removed':
                    net=root.find("./nets/net[@name='GND']");net.remove(net.find("node[@ref='U1'][@pin='57']"))
                elif fault=='IREF short':root.find("./nets/net[@name='LED_IREF']").set('name','GND')
                elif fault=='resistor decade':root.find("./components/comp[@ref='R1']/value").text='3.92k 1%'
                elif fault=='extra component':ET.SubElement(root.find('components'),'comp',ref='R2')
                else:
                    net=root.find("./nets/net[@name='GND']");net.append(deepcopy(net.find("node[@ref='U1'][@pin='57']")))
                p=Path(d)/'bad.xml';p.write_bytes(ET.tostring(root))
                with self.assertRaises(ValueError):CHECK['check_netlist'](p)

    def test_source_faults(self):
        faults=[
            ('driver.kicad_sch','(xy 109.220 167.640)','(xy 109.221 167.640)'),
            ('driver.kicad_sch','"39.2k 1%"','"3.92k 1%"'),
            ('driver.kicad_sch','(property "MPN" "ERJ-2RKF3922X"','(property "MPN" "ERJ-2RKF3921X"'),
            ('driver.kicad_sch','(global_label "COL_00_R"','(global_label "COL_01_R"'),
        ]
        for name,old,new in faults:
            with self.subTest(old=old),tempfile.TemporaryDirectory() as d:
                p=Path(d)/'project';shutil.copytree(PROJECT,p,ignore=shutil.ignore_patterns('build','.history'))
                file=p/name;s=file.read_text();self.assertIn(old,s);file.write_text(s.replace(old,new,1))
                with self.assertRaises(ValueError):CHECK['check_sources'](p)

    def test_library_faults(self):
        fp='footprints/rgb-badge-coupon.pretty/QFN_TI_RTQ0056E_8x8mm_P0.5mm_EP5.7mm.kicad_mod'
        faults=[
            (fp,'(pad "57" smd rect','(pad "58" smd rect'),
            (fp,'(at -3.900 -3.250)','(at 3.900 -3.250)'),
            (fp,'(size 5.7 5.7) (layers "F.Cu" "F.Mask")','(size 5.7 5.7) (layers "F.Cu" "F.Paste" "F.Mask")'),
            (fp,'(size 1.15 1.15)','(size 2.15 2.15)'),
            ('symbols/rgb-badge-coupon.kicad_sym','(name "GND_EP"','(name "NC"'),
        ]
        for name,old,new in faults:
            with self.subTest(old=old),tempfile.TemporaryDirectory() as d:
                p=Path(d)/'project';shutil.copytree(PROJECT,p,ignore=shutil.ignore_patterns('build','.history'))
                file=p/name;s=file.read_text();self.assertIn(old,s);file.write_text(s.replace(old,new,1))
                with self.assertRaises(ValueError):CHECK['check_libraries'](p)

if __name__=='__main__':unittest.main()
