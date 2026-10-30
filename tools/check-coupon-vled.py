#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Check the unlinked VLED source with native KiCad XML and isolated ERC."""

import os
from pathlib import Path
import runpy
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
    "GND": {"C44.2", "C45.2", "C46.2", "C47.2", "C48.2", "C49.2",
            "C50.2", "R86.2", "R87.2", "U37.2", "U37.13", "U37.15"},
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


def check_linked(xml_path):
    project = ROOT / "hardware/coupon/rev-a"
    source = project / "vled-converter.kicad_sch"
    generated = runpy.run_path(str(GENERATOR))["generate"](True)
    assert source.read_text() == generated, "Root-linked dark VLED sheet differs from generator"
    root_source = (project / "rgb-badge-coupon.kicad_sch").read_text()
    assert root_source.count('(property "Sheetfile" "vled-converter.kicad_sch"') == 1
    assert '(property "Reference" "#FLG03"' not in (project / "rows.kicad_sch").read_text()
    root = ET.parse(xml_path).getroot()
    refs = {"U37", "L2", "C44", "C45", "C46", "C47", "C48", "C49",
            "C63", "R84", "R85", "R86", "R87"}
    actual = {}
    for net in root.findall("./nets/net"):
        for node in net.findall("node"):
            if node.get("ref") in refs:
                key = (node.get("ref"), node.get("pin"))
                assert key not in actual, f"Duplicate VLED pin {key}"
                actual[key] = net.get("name")
    expected = {(('C63' if ref == 'C50' else ref), pin): name
                for name, nodes in EXPECTED.items()
                for ref, pin in (node.split('.') for node in nodes)}
    assert actual == expected, "Root-linked VLED pin map differs from the dark stage"
    assert len(actual) == 39
    print("Root-linked dark VLED stage passed: 13 exact parts, 39 pins; EN has only U37.12 and R87.1.")


if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "--linked-netlist":
        check_linked(Path(sys.argv[2]))
    elif len(sys.argv) == 1:
        check()
    else:
        raise SystemExit("Usage: check-coupon-vled.py [--linked-netlist XML]")
