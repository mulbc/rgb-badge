# SPDX-License-Identifier: Apache-2.0
"""Reject circuit-level mistakes that an all-passive LED ERC can miss."""

from copy import deepcopy
from pathlib import Path
import runpy
import shutil
import tempfile
import unittest
import xml.etree.ElementTree as ET

from fixtures.kicad_cli_stub import matrix_netlist


TOOLS = Path(__file__).resolve().parents[1]
CHECK = runpy.run_path(str(TOOLS / 'check-coupon-matrix.py'))
PROJECT = TOOLS.parent / 'hardware/coupon/rev-a'


class CouponMatrixTests(unittest.TestCase):
    def test_current_source_wiring(self):
        CHECK['read_sources'](PROJECT)

    def test_synthetic_correct_netlist(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'matrix.xml'
            path.write_bytes(ET.tostring(matrix_netlist()))
            CHECK['read_netlist'](path)

    def test_colour_swap_missing_led_column_short_and_duplicate_pin(self):
        for fault in ('colour swap', 'missing LED', 'column short', 'duplicate pin'):
            with self.subTest(fault=fault), tempfile.TemporaryDirectory() as directory:
                root = matrix_netlist()
                if fault == 'colour swap':
                    # D9 is QBLP1515: swap R/G while preserving net sizes.
                    for node in root.findall('./nets/net/node'):
                        if node.get('ref') == 'D9' and node.get('pin') in {'3', '4'}:
                            node.set('pin', {'3': '4', '4': '3'}[node.get('pin')])
                elif fault == 'missing LED':
                    components = root.find('components')
                    components.remove(components.find("comp[@ref='D4']"))
                elif fault == 'column short':
                    root.find("./nets/net[@name='COL_01_R']").set('name', 'COL_00_R')
                else:
                    net = root.find('./nets/net')
                    net.append(deepcopy(net.find('node')))
                path = Path(directory) / 'bad.xml'
                path.write_bytes(ET.tostring(root))
                with self.assertRaises(ValueError):
                    CHECK['read_netlist'](path)

    def test_wire_that_misses_a_pin_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory)
            for source in PROJECT.glob('*.kicad_sch'):
                shutil.copyfile(source, target / source.name)
            sheet = target / 'matrix-r00-c00.kicad_sch'
            original = sheet.read_text()
            broken = original.replace('(xy 48.26 60.96)', '(xy 48.27 60.96)', 1)
            self.assertNotEqual(original, broken)
            sheet.write_text(broken)
            with self.assertRaisesRegex(ValueError, 'D1.1: expected one connected global net'):
                CHECK['read_sources'](target)


if __name__ == '__main__':
    unittest.main()
