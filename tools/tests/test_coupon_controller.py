# SPDX-License-Identifier: Apache-2.0
"""Fault injection for the controller and complete-coupon contracts."""

from copy import deepcopy
from pathlib import Path
import runpy
import shutil
import subprocess
import tempfile
import unittest
import xml.etree.ElementTree as ET

from fixtures.kicad_cli_stub import controller_coupon_netlist


TOOLS = Path(__file__).resolve().parents[1]
CHECK = runpy.run_path(str(TOOLS / "check-coupon-controller.py"))
PROJECT = TOOLS.parent / "hardware" / "coupon" / "rev-a"


class CouponControllerTests(unittest.TestCase):
    def test_current_sources(self):
        CHECK["check_sources"](PROJECT)

    def test_complete_synthetic_netlist(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "complete.xml"
            path.write_bytes(ET.tostring(controller_coupon_netlist()))
            CHECK["check_netlist"](path)

    def test_netlist_faults(self):
        for fault in ("boot strap swap", "USB resistor bypass", "missing EN capacitor", "extra part", "duplicate pin"):
            with self.subTest(fault=fault), tempfile.TemporaryDirectory() as directory:
                root = controller_coupon_netlist()
                if fault == "boot strap swap":
                    root.find("./nets/net/node[@ref='U3'][@pin='27']").set("pin", "26")
                elif fault == "USB resistor bypass":
                    node = root.find("./nets/net/node[@ref='R45'][@pin='2']")
                    for net in root.findall("./nets/net"):
                        if node in list(net): net.remove(node); break
                    root.find("./nets/net[@name='USB_DN_MCU']").append(node)
                elif fault == "missing EN capacitor":
                    root.find("components").remove(root.find("./components/comp[@ref='C5']"))
                elif fault == "extra part":
                    ET.SubElement(root.find("components"), "comp", ref="U99")
                else:
                    node = root.find("./nets/net/node[@ref='U3'][@pin='2']")
                    for net in root.findall("./nets/net"):
                        if node in list(net): net.append(deepcopy(node)); break
                path = Path(directory) / "bad.xml"
                path.write_bytes(ET.tostring(root))
                with self.assertRaises(ValueError):
                    CHECK["check_netlist"](path)

    def test_source_faults(self):
        faults = [
            ("controller.kicad_sch", '(global_label "MODE_BOOT_N"', '(global_label "GPIO45"'),
            ("controller.kicad_sch", '(property "Value" "22R 1%"', '(property "Value" "0R"'),
            ("controller.kicad_sch", '(no_connect (at 127.000 106.680)', '(no_connect (at 127.000 106.700)'),
            ("rgb-badge-coupon.kicad_sch", '(property "Sheetfile" "controller.kicad_sch"', '(property "Sheetfile" "control.kicad_sch"'),
        ]
        for name, old, new in faults:
            with self.subTest(old=old), tempfile.TemporaryDirectory() as directory:
                project = Path(directory) / "project"
                shutil.copytree(PROJECT, project, ignore=shutil.ignore_patterns("build", ".history"))
                path = project / name
                source = path.read_text(encoding="utf-8")
                self.assertIn(old, source)
                path.write_text(source.replace(old, new, 1), encoding="utf-8")
                with self.assertRaises(ValueError):
                    CHECK["check_sources"](project)

    def test_generator_is_deterministic_and_refuses_existing_output(self):
        generator = TOOLS / "generate-coupon-controller.py"
        with tempfile.TemporaryDirectory() as directory:
            first, second = Path(directory) / "first", Path(directory) / "second"
            subprocess.run(["python3", str(generator), "--output", str(first)], check=True, capture_output=True)
            subprocess.run(["python3", str(generator), "--output", str(second)], check=True, capture_output=True)
            self.assertEqual((first / "controller.kicad_sch").read_bytes(), (second / "controller.kicad_sch").read_bytes())
            failed = subprocess.run(["python3", str(generator), "--output", str(first)], capture_output=True)
            self.assertNotEqual(failed.returncode, 0)


if __name__ == "__main__":
    unittest.main()
