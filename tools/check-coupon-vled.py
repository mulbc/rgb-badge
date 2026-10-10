#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Check the unlinked VLED source with native KiCad XML and isolated ERC."""

import os
from pathlib import Path
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
SHEET = ROOT / "hardware/coupon/rev-a/staging/vled-converter.kicad_sch"
GENERATOR = ROOT / "tools/generate-coupon-vled.py"
CLI = Path(os.environ.get("RGB_BADGE_KICAD_CLI", "/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli"))

EXPECTED = {
    "+SYS_APP_IN_DRAFT": {"C44.1", "C45.1", "C50.1", "U37.1", "U37.10", "U37.11"},
    "VLED": {"C46.1", "C47.1", "C48.1", "C49.1", "R84.1", "U37.4", "U37.5"},
    "VLED_ENABLE_DRAFT": {"R87.1", "U37.12"},
    "VLED_FB": {"R85.2", "R86.1", "U37.3"},
    "VLED_FB_TOP_MID": {"R84.2", "R85.1"},
    "Net-(L2-~-Pad1)": {"L2.1", "U37.8", "U37.9"},
    "Net-(L2-~-Pad2)": {"L2.2", "U37.6", "U37.7"},
    "unconnected-(U37-PG-Pad14)": {"U37.14"},
}


def run(*args):
    subprocess.run(args, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)


def check():
    assert SHEET.is_file(), SHEET
    assert CLI.is_file(), CLI
    with tempfile.TemporaryDirectory(prefix="rgb-vled-check-") as tmp:
        temp = Path(tmp)
        run(sys.executable, str(GENERATOR), "--output", str(temp / "generated"))
        assert SHEET.read_bytes() == (temp / "generated/vled-converter.kicad_sch").read_bytes(), "VLED source differs from generator"
        netlist = temp / "vled.xml"
        run(str(CLI), "sch", "export", "netlist", "--format", "kicadxml",
            "--output", str(netlist), str(SHEET))
        root = ET.parse(netlist).getroot()
        components = root.find("components")
        assert len(components) == 13, f"Expected 13 parts, found {len(components)}"
        actual = {}
        for net in root.find("nets"):
            actual[net.attrib["name"]] = {
                node.attrib["ref"] + "." + node.attrib["pin"]
                for node in net.findall("node")
            }
        for name, nodes in EXPECTED.items():
            assert actual.get(name) == nodes, f"{name}: {actual.get(name)} != {nodes}"
        assert sum(map(len, actual.values())) == 39, "Unexpected connected pin count"
        erc = temp / "erc.txt"
        run(str(CLI), "sch", "erc", "--output", str(erc), str(SHEET))
        report = erc.read_text()
        assert report.count("[power_pin_not_driven]") == 2, report
        assert report.count("\n[") == 2, report
        assert "U37 Pin 1 [VINA" in report and "U37 Pin 2 [GND" in report
    print("VLED candidate passed: 13 exact parts, 39 netlisted pins; isolated ERC has only two draft-source errors.")


if __name__ == "__main__":
    check()
