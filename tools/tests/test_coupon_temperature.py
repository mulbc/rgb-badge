# SPDX-License-Identifier: Apache-2.0
"""Fault injection for the battery-facing temperature pin contract."""

from copy import deepcopy
from pathlib import Path
import runpy
import tempfile
import unittest
import xml.etree.ElementTree as ET

from fixtures.kicad_cli_stub import controller_coupon_netlist


CHECK = runpy.run_path(str(Path(__file__).resolve().parents[1] / 'check-coupon-temperature.py'))


class CouponTemperatureTests(unittest.TestCase):
    def test_current_source_and_synthetic_pin_map(self):
        CHECK['check_source']()
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'synthetic.xml'
            path.write_bytes(ET.tostring(controller_coupon_netlist()))
            CHECK['check_netlist'](path)

    def test_wrong_ts_or_fault_gate_net_is_rejected(self):
        for ref, pin, destination in [('TH1', '1', 'GND'), ('U40', '4', 'TEMP_OK')]:
            with self.subTest(ref=ref), tempfile.TemporaryDirectory() as directory:
                root = controller_coupon_netlist()
                node = root.find(f"./nets/net/node[@ref='{ref}'][@pin='{pin}']")
                for net in root.findall('./nets/net'):
                    if node in list(net):
                        net.remove(node)
                        break
                root.find(f"./nets/net[@name='{destination}']").append(deepcopy(node))
                path = Path(directory) / 'fault.xml'
                path.write_bytes(ET.tostring(root))
                with self.assertRaisesRegex(ValueError, 'Temperature pin-to-net mismatch'):
                    CHECK['check_netlist'](path)


if __name__ == '__main__':
    unittest.main()
