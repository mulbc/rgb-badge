# SPDX-License-Identifier: Apache-2.0
"""Fault injection for the row-selector and complete-coupon contracts."""

from copy import deepcopy
from pathlib import Path
import runpy
import shutil
import tempfile
import unittest
import xml.etree.ElementTree as ET

from fixtures.kicad_cli_stub import complete_coupon_netlist


TOOLS = Path(__file__).resolve().parents[1]
CHECK = runpy.run_path(str(TOOLS / 'check-coupon-rows.py'))
PROJECT = TOOLS.parent / 'hardware/coupon/rev-a'


class CouponRowTests(unittest.TestCase):
    def test_current_sources(self):
        CHECK['check_sources'](PROJECT)

    def test_complete_synthetic_netlist(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'complete.xml'
            path.write_bytes(ET.tostring(complete_coupon_netlist()))
            CHECK['check_netlist'](path)

    def test_netlist_faults(self):
        for fault in ('missing pullup', 'decoder output swap', 'row drain swap', 'enable pulled down', 'extra part', 'duplicate pin'):
            with self.subTest(fault=fault), tempfile.TemporaryDirectory() as directory:
                root = complete_coupon_netlist()
                if fault == 'missing pullup':
                    root.find('components').remove(root.find("./components/comp[@ref='R6']"))
                elif fault == 'decoder output swap':
                    a = root.find("./nets/net/node[@ref='U2'][@pin='11']")
                    b = root.find("./nets/net/node[@ref='U2'][@pin='9']")
                    a.set('pin', '9'); b.set('pin', '11')
                elif fault == 'row drain swap':
                    root.find("./nets/net/node[@ref='Q1'][@pin='3']").set('pin', '2')
                elif fault == 'enable pulled down':
                    node = root.find("./nets/net/node[@ref='R42'][@pin='1']")
                    for net in root.findall('./nets/net'):
                        if node in list(net):
                            net.remove(node)
                            break
                    root.find("./nets/net[@name='GND']").append(node)
                elif fault == 'extra part':
                    ET.SubElement(root.find('components'), 'comp', ref='Q99')
                else:
                    node = root.find("./nets/net/node[@ref='Q1'][@pin='3']")
                    for net in root.findall('./nets/net'):
                        if node in list(net):
                            net.append(deepcopy(node))
                            break
                path = Path(directory) / 'bad.xml'
                path.write_bytes(ET.tostring(root))
                with self.assertRaises(ValueError):
                    CHECK['check_netlist'](path)

    def test_source_faults(self):
        faults = [
            ('rows.kicad_sch', '(global_label "ROW_00_A"', '(global_label "ROW_01_A"'),
            ('rows.kicad_sch', '(property "Value" "1k 1%"', '(property "Value" "10k 1%"'),
            ('rows.kicad_sch', '(global_label "ROW_ENABLE_N"', '(global_label "GND"'),
            ('rgb-badge-coupon.kicad_sch', '(property "Sheetfile" "rows.kicad_sch"', '(property "Sheetfile" "rowz.kicad_sch"'),
        ]
        for name, old, new in faults:
            with self.subTest(old=old), tempfile.TemporaryDirectory() as directory:
                project = Path(directory) / 'project'
                shutil.copytree(PROJECT, project, ignore=shutil.ignore_patterns('build', '.history'))
                path = project / name
                source = path.read_text(encoding='utf-8')
                self.assertIn(old, source)
                path.write_text(source.replace(old, new, 1), encoding='utf-8')
                with self.assertRaises(ValueError):
                    CHECK['check_sources'](project)

    def test_generator_is_deterministic_and_refuses_existing_output(self):
        generator = TOOLS / 'generate-coupon-rows.py'
        with tempfile.TemporaryDirectory() as directory:
            first, second = Path(directory) / 'first', Path(directory) / 'second'
            import subprocess
            subprocess.run(['python3', str(generator), '--output', str(first)], check=True, capture_output=True)
            subprocess.run(['python3', str(generator), '--output', str(second)], check=True, capture_output=True)
            self.assertEqual((first / 'rows.kicad_sch').read_bytes(), (second / 'rows.kicad_sch').read_bytes())
            failed = subprocess.run(['python3', str(generator), '--output', str(first)], capture_output=True)
            self.assertNotEqual(failed.returncode, 0)


if __name__ == '__main__':
    unittest.main()
