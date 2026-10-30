#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Check the output-isolated interlock capture and its native KiCad nets."""

import argparse
from pathlib import Path
import runpy
import sys
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / "hardware/coupon/rev-a"
generator = runpy.run_path(str(ROOT / "tools/generate-coupon-display-interlock.py"))
lib = runpy.run_path(str(ROOT / "tools/check-power-libraries.py"))


def require(condition, message):
    if not condition:
        raise ValueError(message)


def check_source(project):
    source = (project / "display-interlock.kicad_sch").read_text()
    require(source == generator["generate"](), "Interlock sheet differs from deterministic capture")
    root = lib["parse"](project / "rgb-badge-coupon.kicad_sch")
    sheets = [s for s in lib["children"](root, "sheet")
              if lib["property_map"](s)["Sheetfile"] == "display-interlock.kicad_sch"]
    require(len(sheets) == 1, "Interlock sheet must have exactly one root link")
    require(lib["one"](sheets[0], "uuid", "interlock sheet")[1] == generator["SHEET_UUID"],
            "Interlock sheet path differs from generated symbol-instance path")


def check_netlist(path):
    root = ET.parse(path).getroot()
    parts = {part.get("ref"): part.findtext("value") for part in root.findall("./components/comp")}
    for ref, (mpn, _, _, _, _, _) in generator["h"].PARTS.items():
        require(parts.get(ref) == mpn or (ref.startswith("C") and parts.get(ref) == "100n 16V X7R")
                or (ref.startswith("TP") and parts.get(ref) == "TestPoint_Pad"),
                f"{ref}: exact interlock part missing or substituted")
    nets = {}
    for net in root.findall("./nets/net"):
        for node in net.findall("node"):
            key = (node.get("ref"), node.get("pin"))
            require(key not in nets, f"Duplicate native pin: {key}")
            nets[key] = net.get("name")
    critical = {
        ("U3", "8"): "DISPLAY_HEARTBEAT", ("U3", "9"): "DISPLAY_ARM_CLK",
        ("U47", "4"): "DISPLAY_HEARTBEAT", ("U47", "1"): "APP_SUPERVISOR_OK",
        ("U48", "2"): "DISPLAY_HEARTBEAT", ("U48", "4"): "HEARTBEAT_FALL_CLK",
        ("U49", "1"): "HEARTBEAT_FALL_CLK", ("U49", "5"): "HEARTBEAT_SEEN",
        ("U49", "6"): "DISPLAY_CLEAR_OK", ("U50", "1"): "DISPLAY_ARM_CLK",
        ("U50", "2"): "HEARTBEAT_SEEN", ("U50", "5"): "ARM_LATCH",
        ("U50", "6"): "DISPLAY_CLEAR_OK", ("U51", "1"): "APP_SUPERVISOR_OK",
        ("U51", "3"): "ESP_EN", ("U51", "6"): "MODE_BOOT_N",
        ("U52", "2"): "DISPLAY_ENABLE", ("U52", "4"): "DISPLAY_CLEAR_OK",
        ("U53", "1"): "VLED_WINDOW_OK", ("U53", "6"): "VLED_WINDOW_OK",
        ("U53", "3"): "VLED_HIGH_SENSE", ("U53", "4"): "VLED_LOW_SENSE",
        ("U54", "1"): "ROW_ENABLE_REQ_N", ("U54", "2"): "ROW_ENABLE_REQ_N",
        ("U54", "7"): "ROW_REQUEST", ("U54", "6"): "ROW_REQUEST",
        ("U54", "5"): "ROW_ARM", ("U54", "3"): "ROW_ENABLE_N_CANDIDATE",
        ("U55", "7"): "VLED_ENABLE_CANDIDATE", ("U55", "3"): "ROW_ARM",
        ("TP13", "1"): "VLED_ENABLE_CANDIDATE",
        ("TP14", "1"): "ROW_ENABLE_N_CANDIDATE",
        ("U37", "12"): "VLED_ENABLE_DRAFT", ("U2", "23"): "ROW_ENABLE_N",
        ("R87", "1"): "VLED_ENABLE_DRAFT", ("R42", "2"): "ROW_ENABLE_N",
    }
    for key, expected in critical.items():
        require(nets.get(key) == expected,
                f"{key}: expected {expected!r}, got {nets.get(key)!r}")
    candidate_refs = {"U54", "U55", "TP13", "TP14"}
    for candidate in ("VLED_ENABLE_CANDIDATE", "ROW_ENABLE_N_CANDIDATE"):
        connected = {ref for (ref, _), net in nets.items() if net == candidate}
        require(connected <= candidate_refs and len(connected) == 2,
                f"{candidate}: candidate output must remain isolated at its test pad")
    print("Native interlock: 9 exact ICs, 20 support parts, 2 candidate test pads; heartbeat/clear/window/row pins and dark output isolation passed")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-dir", type=Path, default=PROJECT)
    parser.add_argument("--netlist", type=Path)
    args = parser.parse_args()
    try:
        check_source(args.project_dir)
        if args.netlist:
            check_netlist(args.netlist)
        else:
            print("Deterministic output-isolated interlock sheet and root path passed")
    except (OSError, ValueError, KeyError, ET.ParseError) as error:
        print(f"Interlock check failed: {error}", file=sys.stderr)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
