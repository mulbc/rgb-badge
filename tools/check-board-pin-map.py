#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Derive/check a provisional U3 pin inventory; never configures hardware."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import runpy
import sys
import xml.etree.ElementTree as ET

TOOLS = Path(__file__).resolve().parent
ROOT = TOOLS.parent
CHECK = runpy.run_path(str(TOOLS / "check-coupon-controller.py"))
PROJECT = CHECK["PROJECT"]
DEFAULT_MANIFEST = ROOT / "firmware/boards/coupon-rev-a.json"
DATASHEET = {
    "url": "https://documentation.espressif.com/esp32-s3-wroom-1_wroom-1u_datasheet_en.pdf",
    "version": "1.8",
    "sha256": "27d71971da07c280c6068d08c74720d1a25b8f20cf8494dc1765bdd28d40d435",
    "reviewed_pages": [3, 10, 11, 12, 13],
    "reviewed_on": "2026-10-21",
}
BOUNDARIES = [
    {"ref": "U3", "pin": "12", "net": "ROW_ENABLE_REQ_N"},
    {"ref": "U2", "pin": "23", "net": "ROW_ENABLE_N"},
    {"ref": "U3", "pin": "17", "net": "DISPLAY_ENABLE"},
    {"ref": "TP13", "pin": "1", "net": "VLED_ENABLE_CANDIDATE"},
    {"ref": "TP14", "pin": "1", "net": "ROW_ENABLE_N_CANDIDATE"},
]


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def require(condition, message):
    if not condition:
        raise ValueError(message)


def derive(project=PROJECT):
    connections = CHECK["check_sources"](project)
    controller = CHECK["parse"](project / "controller.kicad_sch")
    instance = next(s for s in CHECK["children"](controller, "symbol") if CHECK["props"](s)["Reference"] == "U3")
    properties = CHECK["props"](instance)
    require(properties.get("Manufacturer") == "Espressif Systems", "Source U3 manufacturer differs")
    require(properties.get("Datasheet") == DATASHEET["url"], "Source U3 datasheet identity differs")
    lib = CHECK["LIB"]
    symbols = {s[1]: s for s in lib["children"](lib["parse"](project / "symbols/rgb-badge-coupon.kicad_sym"), "symbol")}
    mpn, _, footprint = CHECK["PARTS"]["U3"]
    module = lib["library_pins"](symbols[mpn])
    lands = lib["children"](lib["footprint"](project, "ESP32-S3-WROOM-1U"), "pad")
    multiplicity = Counter(pad[1] for pad in lands)
    pins = []
    for number in range(1, 42):
        key = str(number)
        pin = module[key]
        symbol_name = lib["one"](pin, "name", "module pin")[1]
        match = re.match(r"GPIO([0-9]+)(?:/|$)", symbol_name)
        gpio = int(match[1]) if match else None
        manufacturer_name = ("RXD0" if gpio == 44 else "TXD0" if gpio == 43 else
                             f"IO{gpio}" if gpio is not None else "EPAD" if number == 41 else symbol_name)
        net = connections.get(("U3", key))
        pins.append({
            "module_pin": number, "manufacturer_name": manufacturer_name,
            "symbol_name": symbol_name, "electrical_type": pin[1], "gpio": gpio,
            "net": net, "explicit_no_connect": key in CHECK["MODULE_NC"],
            "physical_land_count": multiplicity[key],
            "strapping_pin": gpio in (0, 3, 45, 46),
            "reserved_for_octal_psram": gpio in (35, 36, 37),
        })
    require(len({p["gpio"] for p in pins if p["gpio"] is not None}) == 36, "GPIO identities are not unique")
    require(all(p["explicit_no_connect"] and p["net"] is None for p in pins if p["reserved_for_octal_psram"]),
            "Octal PSRAM pins must remain unconnected")
    canonical = sorted(project.glob("*.kicad_sch"))
    canonical += [project / "symbols/rgb-badge-coupon.kicad_sym",
                  project / "footprints/rgb-badge-coupon.pretty/ESP32-S3-WROOM-1U.kicad_mod"]
    return {
        "SPDX-License-Identifier": "Apache-2.0", "schema_version": 1,
        "hardware_revision": "coupon-rev-a", "status": "PROVISIONAL_NOT_FROZEN",
        "production_gpio_configuration_allowed": False,
        "canonical_project": "hardware/coupon/rev-a/rgb-badge-coupon.kicad_pro",
        "controller_reference": "U3", "manufacturer": "Espressif Systems",
        "manufacturer_part_number": mpn, "footprint": footprint,
        "manufacturer_source": DATASHEET,
        "canonical_source_sha256": {str(p.relative_to(project)): sha(p) for p in canonical},
        "generation_tool_sha256": {p.name: sha(p) for p in (
            Path(__file__), TOOLS / "check-coupon-controller.py", TOOLS / "check-controller-libraries.py")},
        "required_native_boundaries": BOUNDARIES, "pins": pins,
    }


def render(document):
    return json.dumps(document, indent=2, sort_keys=True, allow_nan=False) + "\n"


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, f"Duplicate JSON key: {key}")
        result[key] = value
    return result


def check_manifest(path, expected):
    text = path.read_text()
    document = json.loads(text, object_pairs_hook=unique_object)
    require(render(document) == render(expected), "Pin inventory/source metadata differs; review then regenerate")
    require(text == render(expected), "Pin inventory serialization differs; regenerate deterministically")


def check_native(path, document):
    # Independent native export must also satisfy the entire existing coupon contract.
    CHECK["check_netlist"](path)
    root = ET.parse(path).getroot()
    modules = root.findall("./components/comp[@ref='U3']")
    require(len(modules) == 1, "Expected one native U3")
    module = modules[0]
    mpn = document["manufacturer_part_number"]
    require(module.findtext("value") == mpn and module.findtext("footprint") == document["footprint"],
            "Native U3 part/footprint differs")
    require(module.findtext("./fields/field[@name='MPN']") == mpn, "Native U3 exact MPN field differs")
    require(module.findtext("./fields/field[@name='Manufacturer']") == document["manufacturer"],
            "Native U3 manufacturer differs")
    require(module.findtext("datasheet") == document["manufacturer_source"]["url"], "Native U3 datasheet differs")
    source = module.find("libsource")
    require(source is not None and source.get("lib") == "rgb-badge-coupon" and source.get("part") == mpn,
            "Native U3 library identity differs")
    native = {}
    for net in root.findall("./nets/net"):
        for node in net.findall("node"):
            key = (node.get("ref"), node.get("pin"))
            require(key not in native, f"Duplicate native pin: {key}")
            native[key] = (net.get("name"), node)
    require({pin for ref, pin in native if ref == "U3"} == {str(p["module_pin"]) for p in document["pins"]},
            "Native U3 pin inventory differs")
    for pin in document["pins"]:
        number = str(pin["module_pin"])
        net, node = native["U3", number]
        expected_net = (f"unconnected-(U3-{pin['symbol_name']}-Pad{number})"
                        if pin["explicit_no_connect"] else pin["net"])
        require(net == expected_net, f"Native U3.{number} net differs")
        require(node.get("pinfunction") == f"{pin['symbol_name']}_{number}", f"Native U3.{number} function differs")
        expected_type = pin["electrical_type"] + ("+no_connect" if pin["explicit_no_connect"] else "")
        require(node.get("pintype") == expected_type, f"Native U3.{number} electrical/NC type differs")
    for boundary in document["required_native_boundaries"]:
        key = boundary["ref"], boundary["pin"]
        require(key in native and native[key][0] == boundary["net"], f"Native display boundary differs: {key}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-dir", type=Path, default=PROJECT)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--write", action="store_true", help="Regenerate derived JSON after source review")
    parser.add_argument("--netlist", type=Path, help="Also check a complete native KiCad XML export")
    args = parser.parse_args()
    try:
        document = derive(args.project_dir)
        if args.netlist:
            check_native(args.netlist, document)
        if args.write:
            args.manifest.parent.mkdir(parents=True, exist_ok=True)
            args.manifest.write_text(render(document))
        else:
            check_manifest(args.manifest, document)
        print("Coupon pin inventory passed: 41 module pins, 36 GPIO identities, 25 connected / 16 explicit NC; PROVISIONAL.")
        if args.netlist:
            print("Complete native XML and module pin/function/type/MPN/display-boundary checks passed.")
        return 0
    except (OSError, ValueError, KeyError, IndexError, ET.ParseError) as error:
        print(f"Pin inventory check failed: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
