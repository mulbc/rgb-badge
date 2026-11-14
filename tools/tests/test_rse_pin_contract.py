# SPDX-License-Identifier: Apache-2.0
"""Reject wrong-package pin maps independently of routing and capture generators."""
import contextlib
import copy
import io
import json
from pathlib import Path
import runpy
import tempfile
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[2]
CHECK = runpy.run_path(str(ROOT/'tools/check-coupon-display-interlock.py'))
LIB = runpy.run_path(str(ROOT/'tools/check-interlock-symbols.py'))


class RSEPinContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        data = json.loads((ROOT/'mechanical/review/coupon-canonical-net-contract.json').read_text())
        cls.xml = ET.Element('export')
        components = ET.SubElement(cls.xml, 'components')
        nets = ET.SubElement(cls.xml, 'nets')
        grouped = {}
        for ref, part in data['components'].items():
            c = ET.SubElement(components, 'comp', ref=ref)
            ET.SubElement(c, 'value').text = part['value']
            for pin, entry in part['pins'].items():
                grouped.setdefault(entry['native_net'], []).append((ref, pin))
        for name, nodes in grouped.items():
            net = ET.SubElement(nets, 'net', name=name)
            for ref, pin in nodes:
                ET.SubElement(net, 'node', ref=ref, pin=pin)

    def check(self, xml):
        with tempfile.TemporaryDirectory() as folder, contextlib.redirect_stdout(io.StringIO()):
            path = Path(folder)/'pins.xml'
            ET.ElementTree(xml).write(path)
            CHECK['check_netlist'](path)

    def test_corrected_native_snapshot_passes(self):
        self.check(self.xml)

    def test_complete_circuit_preserves_function_under_exact_terminal_permutation(self):
        folder = ROOT/'mechanical/review'
        before = json.loads((folder/'coupon-canonical-net-contract-before-rse-correction.json').read_text())
        after = json.loads((folder/'coupon-canonical-net-contract.json').read_text())
        self.assertEqual(set(before['components']), set(after['components']))
        mapping = {'1':'7', '2':'6', '3':'5', '4':'4', '5':'3', '6':'2', '7':'1', '8':'8'}
        for ref, part in before['components'].items():
            if ref not in ('U49', 'U50'):
                self.assertEqual(after['components'][ref], part, ref)
                continue
            self.assertEqual({k:v for k,v in part.items() if k!='pins'},
                             {k:v for k,v in after['components'][ref].items() if k!='pins'})
            for old, new in mapping.items():
                entry = part['pins'][old]
                actual = after['components'][ref]['pins'][new]
                self.assertEqual(entry['no_connect'], actual['no_connect'])
                if entry['no_connect']:
                    self.assertEqual(new, '5')
                    self.assertTrue(actual['native_net'].startswith('unconnected-('))
                else:
                    self.assertEqual(entry, actual, ref+'.'+old+'→'+new)

    def test_every_rse_terminal_is_checked_including_nc_and_defaults(self):
        for ref in ('U49', 'U50'):
            for pin in map(str, range(1, 9)):
                with self.subTest(ref=ref, pin=pin):
                    xml = copy.deepcopy(self.xml)
                    original = next(n for n in xml.findall('./nets/net')
                                    if any(q.get('ref')==ref and q.get('pin')==pin for q in n.findall('node')))
                    node = next(q for q in original.findall('node') if q.get('ref')==ref and q.get('pin')==pin)
                    original.remove(node)
                    ET.SubElement(xml.find('nets'), 'net', name='WRONG').append(node)
                    with self.assertRaises(ValueError):
                        self.check(xml)

    def test_manufacturer_rse_function_marks_are_distinct_from_other_packages(self):
        # TI Rev F RSE column and Rev G Fig 5-2. Q-bar is a graphical inverted
        # output; pin 5 must not accidentally become the arming Q output.
        expected = {
            1: ('PRE', 'input', 'inverted'), 2: ('CLR', 'input', 'inverted'),
            3: ('Q', 'output', 'line'), 4: ('GND', 'power_in', 'line'),
            5: ('Q', 'output', 'inverted'), 6: ('D', 'input', 'line'),
            7: ('CLK', 'input', 'clock'), 8: ('VCC', 'power_in', 'line'),
        }
        root = LIB['LIB']['parse'](ROOT/'hardware/coupon/rev-a/symbols/rgb-badge-coupon.kicad_sym')
        symbol = next(s for s in LIB['children'](root, 'symbol') if s[1]=='SN74LVC1G74RSER')
        actual = {int(n):(LIB['one'](p,'name','pin')[1],p[1],p[2])
                  for n,p in LIB['pins'](symbol).items()}
        self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
