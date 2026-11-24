# SPDX-License-Identifier: Apache-2.0
"""Source/JSON/native-XML fault injection; synthetic XML is not a KiCad export."""
from copy import deepcopy
import json
from pathlib import Path
import runpy
import shutil
import subprocess
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET

from fixtures.kicad_cli_stub import controller_coupon_netlist

TOOLS = Path(__file__).resolve().parents[1]
MAP = runpy.run_path(str(TOOLS / "check-board-pin-map.py"))
PROJECT = MAP["PROJECT"]


def native_fixture(document):
    root = controller_coupon_netlist()
    module = root.find("./components/comp[@ref='U3']")
    fields = ET.SubElement(module, "fields")
    ET.SubElement(fields, "field", name="MPN").text = document["manufacturer_part_number"]
    ET.SubElement(fields, "field", name="Manufacturer").text = document["manufacturer"]
    ET.SubElement(module, "datasheet").text = document["manufacturer_source"]["url"]
    ET.SubElement(module, "libsource", lib="rgb-badge-coupon", part=document["manufacturer_part_number"])
    pins = {str(pin["module_pin"]): pin for pin in document["pins"]}
    for node in root.findall("./nets/net/node[@ref='U3']"):
        pin = pins[node.get("pin")]
        node.set("pinfunction", f"{pin['symbol_name']}_{pin['module_pin']}")
        node.set("pintype", pin["electrical_type"] + ("+no_connect" if pin["explicit_no_connect"] else ""))
    return root


def copy_project(destination):
    destination.mkdir()
    for source in PROJECT.glob("*.kicad_sch"):
        shutil.copyfile(source, destination / source.name)
    for folder in ("symbols", "footprints/rgb-badge-coupon.pretty"):
        shutil.copytree(PROJECT / folder, destination / folder)


class BoardPinMapTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.document = MAP["derive"]()

    def test_committed_inventory_and_manufacturer_critical_facts(self):
        MAP["check_manifest"](MAP["DEFAULT_MANIFEST"], self.document)
        pins = self.document["pins"]
        self.assertEqual(len(pins), 41)
        self.assertEqual(sum(p["physical_land_count"] for p in pins), 49)
        self.assertEqual(sum(p["explicit_no_connect"] for p in pins), 16)
        self.assertEqual(sum(p["net"] is not None for p in pins), 25)
        self.assertEqual(len({p["gpio"] for p in pins if p["gpio"] is not None}), 36)
        assigned = {p["net"]: (p["module_pin"], p["gpio"]) for p in pins if p["gpio"] is not None and p["net"]}
        self.assertEqual(len(assigned), 20)
        self.assertEqual(assigned["USB_DN_MCU"], (13, 19))
        self.assertEqual(assigned["USB_DP_MCU"], (14, 20))
        self.assertEqual(assigned["MODE_BOOT_N"], (27, 0))
        self.assertEqual(assigned["DISPLAY_HEARTBEAT"], (8, 15))
        self.assertEqual(assigned["DISPLAY_ARM_CLK"], (9, 16))
        self.assertEqual(assigned["ROW_ENABLE_REQ_N"], (12, 8))
        self.assertEqual(assigned["SYS_I2C_SDA"], (10, 17))
        self.assertEqual(assigned["SYS_I2C_SCL"], (11, 18))
        self.assertEqual({p["gpio"] for p in pins if p["strapping_pin"]}, {0, 3, 45, 46})
        self.assertEqual({p["gpio"] for p in pins if p["reserved_for_octal_psram"]}, {35, 36, 37})
        self.assertTrue(all(p["net"] is None and p["explicit_no_connect"] for p in pins if p["reserved_for_octal_psram"]))
        self.assertFalse(self.document["production_gpio_configuration_allowed"])
        self.assertEqual(self.document["status"], "PROVISIONAL_NOT_FROZEN")

    def test_deterministic_regeneration_and_cli(self):
        self.assertEqual(MAP["render"](self.document), MAP["render"](MAP["derive"]()))
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "board.json"
            command = [sys.executable, str(TOOLS / "check-board-pin-map.py"), "--manifest", str(path)]
            result = subprocess.run([*command, "--write"], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(path.read_text(), MAP["render"](self.document))
            result = subprocess.run(command, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("PROVISIONAL", result.stdout)

    def test_metadata_and_pin_mutations_rejected(self):
        for fault in ("production true", "boolean integer", "pin float", "wrong MPN", "wrong package", "missing pin",
                      "extra pin", "pin order", "GPIO swap", "pin number", "PSRAM allocation", "strap flag",
                      "NC flag", "wrong net", "land count", "source hash", "datasheet hash", "unknown key"):
            with self.subTest(fault=fault), tempfile.TemporaryDirectory() as directory:
                changed = deepcopy(self.document)
                pins = changed["pins"]
                if fault == "production true": changed["production_gpio_configuration_allowed"] = True
                elif fault == "boolean integer": changed["production_gpio_configuration_allowed"] = 0
                elif fault == "pin float": pins[0]["module_pin"] = 1.0
                elif fault == "wrong MPN": changed["manufacturer_part_number"] = "ESP32-S3-WROOM-1U-N8R8"
                elif fault == "wrong package": changed["footprint"] = "other:module"
                elif fault == "missing pin": pins.pop()
                elif fault == "extra pin": pins.append(deepcopy(pins[0]))
                elif fault == "pin order": pins.reverse()
                elif fault == "GPIO swap": pins[12]["gpio"], pins[13]["gpio"] = pins[13]["gpio"], pins[12]["gpio"]
                elif fault == "pin number": pins[0]["module_pin"] = 2
                elif fault == "PSRAM allocation": pins[27]["reserved_for_octal_psram"] = False
                elif fault == "strap flag": pins[26]["strapping_pin"] = False
                elif fault == "NC flag": pins[27]["explicit_no_connect"] = False
                elif fault == "wrong net": pins[11]["net"] = "ROW_ENABLE_N"
                elif fault == "land count": pins[40]["physical_land_count"] = 1
                elif fault == "source hash": changed["canonical_source_sha256"]["controller.kicad_sch"] = "0" * 64
                elif fault == "datasheet hash": changed["manufacturer_source"]["sha256"] = "0" * 64
                else: changed["unknown"] = "extra"
                path = Path(directory) / "board.json"
                path.write_text(MAP["render"](changed))
                with self.assertRaises(ValueError): MAP["check_manifest"](path, self.document)

    def test_duplicate_keys_and_serialization_rejected(self):
        text = MAP["render"](self.document)
        for altered in (text.replace('"schema_version": 1', '"schema_version": 1, "schema_version": 1', 1),
                        text.replace('"module_pin": 1,', '"module_pin": 1, "module_pin": 1,', 1),
                        json.dumps(self.document)):
            with self.subTest(), tempfile.TemporaryDirectory() as directory:
                path = Path(directory) / "board.json"
                path.write_text(altered)
                with self.assertRaises(ValueError): MAP["check_manifest"](path, self.document)

    def test_synthetic_complete_native_fixture(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "coupon.xml"
            path.write_bytes(ET.tostring(native_fixture(self.document)))
            MAP["check_native"](path, self.document)

    def test_native_faults(self):
        for fault in ("missing pin", "duplicate pin", "USB pin swap", "MPN field", "manufacturer field", "datasheet", "library identity",
                      "pin function", "electrical type", "NC type", "NC net", "row bypass", "candidate bypass"):
            with self.subTest(fault=fault), tempfile.TemporaryDirectory() as directory:
                root = native_fixture(self.document)
                module = root.find("./components/comp[@ref='U3']")
                node = root.find("./nets/net/node[@ref='U3'][@pin='13']")
                if fault in ("missing pin", "duplicate pin"):
                    net = next(n for n in root.findall("./nets/net") if node in list(n))
                    if fault == "missing pin": net.remove(node)
                    else: net.append(deepcopy(node))
                elif fault == "USB pin swap":
                    other = root.find("./nets/net/node[@ref='U3'][@pin='14']")
                    node.set("pin", "14"); other.set("pin", "13")
                elif fault == "MPN field": module.find("./fields/field[@name='MPN']").text = "other"
                elif fault == "manufacturer field": module.find("./fields/field[@name='Manufacturer']").text = "other"
                elif fault == "datasheet": module.find("datasheet").text = "other"
                elif fault == "library identity": module.find("libsource").set("part", "other")
                elif fault == "pin function": node.set("pinfunction", "GPIO20_13")
                elif fault == "electrical type": node.set("pintype", "output")
                elif fault == "NC type": root.find("./nets/net/node[@ref='U3'][@pin='28']").set("pintype", "bidirectional")
                elif fault == "NC net":
                    nc = root.find("./nets/net/node[@ref='U3'][@pin='28']")
                    next(n for n in root.findall("./nets/net") if nc in list(n)).set("name", "ALLOCATED_PSRAM_PIN")
                else:
                    ref, pin, destination = ("U3", "12", "ROW_ENABLE_N") if fault == "row bypass" else ("TP13", "1", "DISPLAY_ENABLE")
                    moved = root.find(f"./nets/net/node[@ref='{ref}'][@pin='{pin}']")
                    next(n for n in root.findall("./nets/net") if moved in list(n)).remove(moved)
                    root.find(f"./nets/net[@name='{destination}']").append(moved)
                path = Path(directory) / "coupon.xml"
                path.write_bytes(ET.tostring(root))
                with self.assertRaises(ValueError): MAP["check_native"](path, self.document)

    def test_source_edits_detected(self):
        for fault in ("controller net", "ground land", "unrelated schematic drift"):
            with self.subTest(fault=fault), tempfile.TemporaryDirectory() as directory:
                project = Path(directory) / "project"
                copy_project(project)
                if fault == "controller net":
                    path = project / "controller.kicad_sch"
                    path.write_text(path.read_text().replace('"DISPLAY_HEARTBEAT"', '"DISPLAY_ENABLE"', 1))
                    with self.assertRaises(ValueError): MAP["derive"](project)
                elif fault == "ground land":
                    path = project / "footprints/rgb-badge-coupon.pretty/ESP32-S3-WROOM-1U.kicad_mod"
                    text = path.read_text()
                    self.assertIn('(pad "41"', text)
                    path.write_text(text.replace('(pad "41"', '(pad "42"', 1))
                    with self.assertRaises(ValueError): MAP["derive"](project)
                else:
                    path = project / "rows.kicad_sch"
                    path.write_text(path.read_text() + "\n")
                    regenerated = MAP["derive"](project)
                    with self.assertRaises(ValueError): MAP["check_manifest"](MAP["DEFAULT_MANIFEST"], regenerated)

    def test_failed_native_write_preserves_existing_file(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "board.json"
            path.write_text("keep existing artifact")
            netlist = Path(directory) / "invalid.xml"
            netlist.write_text("<broken>")
            result = subprocess.run([sys.executable, str(TOOLS / "check-board-pin-map.py"),
                                     "--manifest", str(path), "--write", "--netlist", str(netlist)],
                                    capture_output=True, text=True)
            self.assertEqual(result.returncode, 1)
            self.assertEqual(result.stdout, "")
            self.assertEqual(path.read_text(), "keep existing artifact")


if __name__ == "__main__":
    unittest.main()
