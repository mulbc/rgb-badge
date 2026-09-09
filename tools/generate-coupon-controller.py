#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Generate the Coupon Rev A controller sheet in a NEW output directory.

This deterministic capture helper never overwrites canonical KiCad sources.
Its result still requires the independent source checks and native KiCad ERC.
"""

import argparse
import json
from pathlib import Path
import re
import runpy
import uuid


TOOLS = Path(__file__).resolve().parent
AUDIT = runpy.run_path(str(TOOLS / "check-controller-libraries.py"))
PROJECT_DIR = TOOLS.parent / "hardware" / "coupon" / "rev-a"
SYMBOL_LIBRARY = PROJECT_DIR / "symbols" / "rgb-badge-coupon.kicad_sym"
ROOT_UUID = "207fb68e-2ddb-46bb-8712-eba2f8c5eef6"
SHEET_UUID = "c1aa0a05-857c-59e4-b6b1-f737e9508fa3"
FILE_UUID = "8c76aba2-3e70-5442-9e12-3838cdcea085"
NAMESPACE = uuid.UUID(ROOT_UUID)
PROJECT = "rgb-badge-coupon"


def uid(name):
    return str(uuid.uuid5(NAMESPACE, "controller-rev-a/" + name))


def quote(value):
    return json.dumps(str(value), ensure_ascii=False)


def effects(size=1.27, justify="", hidden=False):
    return (f'(effects (font (size {size} {size}))'
            + (f' (justify {justify})' if justify else '')
            + (' (hide yes)' if hidden else '') + ')')


def prop(name, value, x, y, *, hidden=False, size=1.27):
    return f'(property {quote(name)} {quote(value)} (at {x:.3f} {y:.3f} 0) {effects(size, hidden=hidden)})'


def note(text, x, y, name, size=1.27):
    return f'(text {quote(text)} (at {x:.2f} {y:.2f} 0) {effects(size, "left")} (uuid {quote(uid(name))}))'


def cached_symbol(mpn):
    source = SYMBOL_LIBRARY.read_text(encoding="utf-8")
    matches = re.findall(r'^\t\(symbol "' + re.escape(mpn) + r'"\n.*?^\t\)', source, re.M | re.S)
    if len(matches) != 1:
        raise ValueError(f"Cannot extract controlled symbol {mpn}")
    return matches[0].replace(f'(symbol "{mpn}"', f'(symbol "rgb-badge-coupon:{mpn}"', 1)


METADATA = {
    "ESP32-S3-WROOM-1U-N16R8": ("Espressif Systems", "https://documentation.espressif.com/esp32-s3-wroom-1_wroom-1u_datasheet_en.pdf", "rgb-badge-coupon:ESP32-S3-WROOM-1U"),
    "ERJ-2RKF1002X": ("Panasonic", "https://industrial.panasonic.com/cdbs/www-data/pdf/RDA0000/AOA0000C304.pdf", "rgb-badge-coupon:R_Panasonic_ERJ2_0402"),
    "ERJ-2RKF22R0X": ("Panasonic", "https://industrial.panasonic.com/cdbs/www-data/pdf/RDA0000/AOA0000C304.pdf", "rgb-badge-coupon:R_Panasonic_ERJ2_0402"),
    "ERJ-2RKF4990X": ("Panasonic", "https://industrial.panasonic.com/cdbs/www-data/pdf/RDA0000/AOA0000C304.pdf", "rgb-badge-coupon:R_Panasonic_ERJ2_0402"),
    "GRM155C71A105KE11D": ("Murata", "https://pim.murata.com/en-global/pim/details/?partNum=GRM155C71A105KE11D", "rgb-badge-coupon:C_Murata_GRM15_0402"),
    "GRM188R60J106ME47D": ("Murata", "https://pim.murata.com/en-global/pim/details/?partNum=GRM188R60J106ME47D", "rgb-badge-coupon:C_Murata_GRM18_0603"),
    "GRM155R71C104KA88D": ("Murata", "https://pim.murata.com/asset/pim4/ceramicCapacitorSMD/GRM155R71C104KA88-01A-EN_PDF_CERAMICCAPACITORSMD", "rgb-badge-coupon:C_Murata_GRM15_0402"),
    "EVQP7J01P": ("Panasonic", "https://industrial.panasonic.com/cdbs/www-data/pdf/ATK0000/ATK0000C378.pdf", "rgb-badge-coupon:SW_Panasonic_EVQP7J01P"),
    "TestPoint_Pad": ("PCB copper feature", "", "rgb-badge-coupon:TestPoint_Pad_D1.0mm"),
}

PIN_NUMBERS = {
    "ESP32-S3-WROOM-1U-N16R8": [str(i) for i in range(1, 42)],
    "ERJ-2RKF1002X": ["1", "2"], "ERJ-2RKF22R0X": ["1", "2"],
    "ERJ-2RKF4990X": ["1", "2"], "GRM155C71A105KE11D": ["1", "2"],
    "GRM188R60J106ME47D": ["1", "2"], "GRM155R71C104KA88D": ["1", "2"],
    "EVQP7J01P": ["1", "2"], "TestPoint_Pad": ["1"],
}


def component(mpn, ref, value, x, y):
    manufacturer, datasheet, footprint = METADATA[mpn]
    if mpn == "ESP32-S3-WROOM-1U-N16R8":
        reference_y, value_y = y - 39.37, y - 36.83
    elif mpn.startswith("GRM"):
        reference_y, value_y = y - 6.35, y - 3.81
    elif mpn == "EVQP7J01P":
        reference_y, value_y = y - 5.08, y - 2.54
    else:
        reference_y, value_y = y - 5.08, y - 2.54
    purchased = mpn != "TestPoint_Pad"
    lines = [
        f'(symbol (lib_id "rgb-badge-coupon:{mpn}") (at {x:.3f} {y:.3f} 0) (unit 1)',
        f'(exclude_from_sim no) (in_bom {"yes" if purchased else "no"}) (on_board yes) (dnp no)',
        f'(uuid {quote(uid(ref))})',
        prop("Reference", ref, x, reference_y), prop("Value", value, x, value_y),
        prop("Footprint", footprint, x, y, hidden=True), prop("Datasheet", datasheet, x, y, hidden=True),
        prop("Manufacturer", manufacturer, x, y, hidden=True),
        prop("MPN", mpn if purchased else "", x, y, hidden=True),
    ]
    lines.extend(f'(pin {quote(number)} (uuid {quote(uid(ref + "/pin/" + number))}))' for number in PIN_NUMBERS[mpn])
    lines.append(f'(instances (project {quote(PROJECT)} (path "/{ROOT_UUID}/{SHEET_UUID}" (reference {quote(ref)}) (unit 1)))))')
    return lines


def wire_label(net, pin_x, pin_y, end_x, end_y, angle, name):
    justify = "right" if angle == 180 else "left"
    points = [(pin_x, pin_y)]
    if pin_x != end_x and pin_y != end_y:
        points.append((pin_x, end_y))
    points.append((end_x, end_y))
    result = []
    for index, (a, b) in enumerate(zip(points, points[1:])):
        result.append(f'(wire (pts (xy {a[0]:.3f} {a[1]:.3f}) (xy {b[0]:.3f} {b[1]:.3f})) (stroke (width 0) (type default)) (uuid {quote(uid(name + "/wire/" + str(index)))}))')
    result.append(f'(global_label {quote(net)} (shape passive) (at {end_x:.3f} {end_y:.3f} {angle}) {effects(1.016, justify)} (uuid {quote(uid(name + "/label"))}) {prop("Intersheetrefs", "${INTERSHEET_REFS}", end_x, end_y, hidden=True)})')
    return result


def no_connect(x, y, name):
    return f'(no_connect (at {x:.3f} {y:.3f}) (uuid {quote(uid(name + "/nc"))}))'


def two_pin(mpn, ref, value, x, y, left_net, right_net):
    result = component(mpn, ref, value, x, y)
    left_length = 5.08 if mpn != "EVQP7J01P" else 6.35
    result += wire_label(left_net, x - left_length, y, x - left_length - 10.16, y, 180, ref + "/1")
    result += wire_label(right_net, x + left_length, y, x + left_length + 10.16, y, 0, ref + "/2")
    return result


def testpoint(ref, net, x, y):
    result = component("TestPoint_Pad", ref, "TestPoint_Pad", x, y)
    result += wire_label(net, x - 5.08, y, x - 15.24, y, 180, ref + "/1")
    return result


def generate():
    AUDIT["check_libraries"](PROJECT_DIR)
    used_symbols = list(METADATA)
    lines = [
        '(kicad_sch', '(version 20260306)', '(generator "rgb_badge_controller")', '(generator_version "1.0")',
        f'(uuid {quote(FILE_UUID)})', '(paper "A2")',
        '(title_block (title "Coupon Rev A - ESP32-S3 controller") (rev "A-draft") (comment 1 "SPDX-License-Identifier: CERN-OHL-S-2.0") (comment 2 "USB connector/ESD and switched rail sources remain on the pending power sheet"))',
        '(lib_symbols\n' + '\n'.join(cached_symbol(name) for name in used_symbols) + '\n)',
        note('ESP32-S3-WROOM-1U-N16R8 controller and recovery interfaces', 20.32, 20.32, 'title', 2.0),
        note('GPIO35..37 are reserved by the N16R8 octal PSRAM and are deliberately not connected.', 20.32, 27.94, 'psram-note'),
        note('GPIO0 is both the user mode input and ROM boot strap: hold the mode switch while powering ON for recovery.', 20.32, 35.56, 'boot-note'),
    ]

    module_x, module_y = 106.68, 116.84
    lines += component("ESP32-S3-WROOM-1U-N16R8", "U3", "ESP32-S3-WROOM-1U-N16R8", module_x, module_y)
    relative = {}
    controlled = AUDIT["check_libraries"](PROJECT_DIR)["ESP32-S3-WROOM-1U-N16R8"]
    for unit in AUDIT["children"](controlled, "symbol"):
        for pin in AUDIT["children"](unit, "pin"):
            number = AUDIT["one"](pin, "number", "module pin")[1]
            at = AUDIT["one"](pin, "at", "module pin")
            relative[number] = (float(at[1]), float(at[2]))
    nets = {
        "1": "GND", "2": "+3V3_APP", "3": "ESP_EN",
        "4": "ROW_A0", "5": "ROW_A1", "6": "ROW_A2", "7": "ROW_A3",
        "10": "SYS_I2C_SDA", "11": "SYS_I2C_SCL", "12": "ROW_ENABLE_N",
        "13": "USB_DN_MCU", "14": "USB_DP_MCU", "17": "DISPLAY_ENABLE",
        "18": "LED_LAT", "19": "LED_SIN", "20": "LED_SCLK", "21": "LED_GCLK",
        "22": "LED_SOUT", "27": "MODE_BOOT_N", "36": "UART0_RX",
        "37": "UART0_TX_RAW", "40": "GND", "41": "GND",
    }
    for number in map(str, range(1, 42)):
        px, py = relative[number]
        x, y = module_x + px, module_y - py
        if number in nets:
            left = px < 0
            lines += wire_label(nets[number], x, y, 73.66 if left else 139.70, y, 180 if left else 0, f"U3/{number}")
        else:
            lines.append(no_connect(x, y, f"U3/{number}"))

    lines += [note('Local 3.3 V bulk and high-frequency decoupling', 177.80, 50.80, 'decoupling-title')]
    lines += two_pin("GRM188R60J106ME47D", "C3", "10u 6.3V X5R", 213.36, 63.50, "+3V3_APP", "GND")
    lines += two_pin("GRM155R71C104KA88D", "C4", "100n 16V X7R", 213.36, 78.74, "+3V3_APP", "GND")

    lines += [note('EN delay: Espressif baseline 10 kOhm / 1 uF; verify rail ramp on the coupon', 177.80, 101.60, 'en-title', 1.016)]
    lines += two_pin("ERJ-2RKF1002X", "R43", "10k 1%", 213.36, 114.30, "+3V3_APP", "ESP_EN")
    lines += two_pin("GRM155C71A105KE11D", "C5", "1u 10V X7S", 213.36, 129.54, "ESP_EN", "GND")
    lines += testpoint("TP2", "ESP_EN", 213.36, 144.78)

    lines += [note('One side-push user button; normally-open to ground', 177.80, 167.64, 'mode-title')]
    lines += two_pin("ERJ-2RKF1002X", "R44", "10k 1%", 213.36, 180.34, "+3V3_APP", "MODE_BOOT_N")
    lines += two_pin("EVQP7J01P", "SW1", "EVQP7J01P", 213.36, 195.58, "MODE_BOOT_N", "GND")
    lines += testpoint("TP3", "MODE_BOOT_N", 213.36, 210.82)

    lines += [note('Native USB boundary; connector and ESD are captured with the power/input sheet', 299.72, 50.80, 'usb-title', 1.016)]
    lines += two_pin("ERJ-2RKF22R0X", "R45", "22R 1%", 335.28, 66.04, "USB_DN_MCU", "USB_D-")
    lines += two_pin("ERJ-2RKF22R0X", "R46", "22R 1%", 335.28, 81.28, "USB_DP_MCU", "USB_D+")
    lines += [note('Route R45/R46 beside U3 and route USB_D+/D- as a controlled differential pair.', 299.72, 93.98, 'usb-layout-note', 1.016)]

    lines += [note('Hidden recovery / factory-test pads', 299.72, 114.30, 'test-title')]
    lines += two_pin("ERJ-2RKF4990X", "R47", "499R 1%", 335.28, 127.00, "UART0_TX_RAW", "UART0_TX")
    for ref, net, y in (
        ("TP4", "UART0_TX", 142.24), ("TP5", "UART0_RX", 154.94),
        ("TP6", "LED_GCLK", 167.64), ("TP7", "ROW_ENABLE_N", 180.34),
        ("TP8", "+3V3_APP", 193.04), ("TP9", "GND", 205.74),
        ("TP10", "DISPLAY_ENABLE", 218.44), ("TP11", "SYS_I2C_SDA", 231.14),
        ("TP12", "SYS_I2C_SCL", 243.84),
    ):
        lines += testpoint(ref, net, 335.28, y)

    lines += [
        note('DISPLAY_ENABLE is only a controller request. The pending power sheet must default VLED OFF without firmware.', 20.32, 248.92, 'display-safety-note', 1.016),
        note('External antenna: Taoglas FXP75.07.0045B candidate on the module U.FL connector; fitted part, no PCB footprint.', 20.32, 256.54, 'antenna-note', 1.016),
        note('Never fabricate from this sheet alone. USB/power capture, DRC/DFM, Gate A review and coupon measurements remain.', 20.32, 264.16, 'release-note', 1.016),
        '(embedded_fonts no)', ')',
    ]
    return '\n'.join(lines) + '\n'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True, type=Path, help='New directory; existing paths are rejected')
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=False)
    (args.output / 'controller.kicad_sch').write_text(generate(), encoding='utf-8')
    print(f'Generated controller draft: ESP32-S3 module, reset/mode/USB/UART support and 11 test pads in {args.output}')


if __name__ == '__main__':
    main()
