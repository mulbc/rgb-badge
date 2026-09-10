#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Generate the Coupon Rev A row-selection sheet in a NEW output directory.

This is a deterministic capture helper, not an electrical validator. It never
overwrites canonical KiCad sources. Review and validate the generated sheet
before copying it into the project.
"""

import argparse
import json
from pathlib import Path
import re
import runpy
import uuid


TOOLS = Path(__file__).resolve().parent
LED = runpy.run_path(str(TOOLS / "check-led-libraries.py"))
ROW = runpy.run_path(str(TOOLS / "check-row-libraries.py"))
PROJECT_DIR = TOOLS.parent / "hardware" / "coupon" / "rev-a"
SYMBOL_LIBRARY = PROJECT_DIR / "symbols" / "rgb-badge-coupon.kicad_sym"
ROOT_UUID = "207fb68e-2ddb-46bb-8712-eba2f8c5eef6"
SHEET_UUID = "bb12d62e-fd97-516e-9e94-af2c7615caf5"
FILE_UUID = "2a21bafc-2155-5152-9b8f-db9a5063a2ae"
NAMESPACE = uuid.UUID(ROOT_UUID)
PROJECT = "rgb-badge-coupon"


def uid(name):
    return str(uuid.uuid5(NAMESPACE, "rows-rev-a/" + name))


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
    "74HC4514PW,118": ("Nexperia", "https://assets.nexperia.com/documents/data-sheet/74HC_HCT4514.pdf", "rgb-badge-coupon:TSSOP_Nexperia_SOT355-1_24"),
    "DMP2066LSN-7": ("Diodes Incorporated", "https://www.diodes.com/datasheet/download/DMP2066LSN.pdf", "rgb-badge-coupon:SC59_Diodes_DMP2066LSN"),
    "2N7002K-7": ("Diodes Incorporated", "https://www.diodes.com/assets/Datasheets/2N7002K.pdf", "rgb-badge-coupon:SOT23_Diodes_2N7002K"),
    "ERJ-2RKF1001X": ("Panasonic", "https://industrial.panasonic.com/cdbs/www-data/pdf/RDA0000/AOA0000C304.pdf", "rgb-badge-coupon:R_Panasonic_ERJ2_0402"),
    "ERJ-2RKF1003X": ("Panasonic", "https://industrial.panasonic.com/cdbs/www-data/pdf/RDA0000/AOA0000C304.pdf", "rgb-badge-coupon:R_Panasonic_ERJ2_0402"),
    "GRM155R71C104KA88D": ("Murata", "https://pim.murata.com/asset/pim4/ceramicCapacitorSMD/GRM155R71C104KA88-01A-EN_PDF_CERAMICCAPACITORSMD", "rgb-badge-coupon:C_Murata_GRM15_0402"),
    "PWR_FLAG": ("", "", ""),
}


PIN_NUMBERS = {
    "74HC4514PW,118": [str(i) for i in range(1, 25)],
    "DMP2066LSN-7": ["1", "2", "3"],
    "2N7002K-7": ["1", "2", "3"],
    "ERJ-2RKF1001X": ["1", "2"],
    "ERJ-2RKF1003X": ["1", "2"],
    "GRM155R71C104KA88D": ["1", "2"],
    "PWR_FLAG": ["1"],
}


def component(mpn, ref, value, x, y):
    manufacturer, datasheet, footprint = METADATA[mpn]
    virtual = mpn == "PWR_FLAG"
    if mpn == "74HC4514PW,118":
        reference_y, value_y = y - 29.21, y - 26.67
    elif mpn in {"DMP2066LSN-7", "2N7002K-7"}:
        reference_y, value_y = y - 8.89, y - 6.35
    elif mpn == "GRM155R71C104KA88D":
        reference_y, value_y = y - 6.35, y - 3.81
    else:
        reference_y, value_y = y - 5.08, y - 2.54
    lines = [
        f'(symbol (lib_id "rgb-badge-coupon:{mpn}") (at {x:.3f} {y:.3f} 0) (unit 1)',
        f'(exclude_from_sim no) (in_bom {"no" if virtual else "yes"}) (on_board {"no" if virtual else "yes"}) (dnp no)',
        f'(uuid {quote(uid(ref))})',
        prop("Reference", ref, x, reference_y),
        prop("Value", value, x, value_y),
        prop("Footprint", footprint, x, y, hidden=True),
        prop("Datasheet", datasheet, x, y, hidden=True),
        prop("Manufacturer", manufacturer, x, y, hidden=True),
        prop("MPN", "" if virtual else mpn, x, y, hidden=True),
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


def stage(index, x, y):
    row = f"{index:02d}"
    p_ref, n_ref = f"Q{index + 1}", f"Q{index + 17}"
    pullup_ref, pulldown_ref = f"R{index + 6}", f"R{index + 22}"
    result = [note(f"ROW {row}", x - 22.86, y - 10.16, f"row-{row}/title", 1.27)]
    result += component("DMP2066LSN-7", p_ref, "DMP2066LSN-7", x, y)
    result += wire_label("VLED", x - 6.35, y, x - 16.51, y, 180, p_ref + "/S")
    result += wire_label(f"ROW_{row}_A", x + 6.35, y, x + 16.51, y, 0, p_ref + "/D")
    result += wire_label(f"ROW_GATE_{row}", x, y + 5.08, x + 15.24, y + 10.16, 0, p_ref + "/G")

    result += component("ERJ-2RKF1001X", pullup_ref, "1k 1%", x + 55.88, y + 12.70)
    result += wire_label("VLED", x + 50.80, y + 12.70, x + 40.64, y + 12.70, 180, pullup_ref + "/1")
    result += wire_label(f"ROW_GATE_{row}", x + 60.96, y + 12.70, x + 71.12, y + 12.70, 0, pullup_ref + "/2")

    result += component("2N7002K-7", n_ref, "2N7002K-7", x, y + 30.48)
    result += wire_label("GND", x - 6.35, y + 30.48, x - 16.51, y + 30.48, 180, n_ref + "/S")
    result += wire_label(f"ROW_GATE_{row}", x + 6.35, y + 30.48, x + 16.51, y + 30.48, 0, n_ref + "/D")
    result += wire_label(f"ROW_SEL_{row}", x, y + 35.56, x + 15.24, y + 40.64, 0, n_ref + "/G")

    result += component("ERJ-2RKF1003X", pulldown_ref, "100k 1%", x + 55.88, y + 43.18)
    result += wire_label(f"ROW_SEL_{row}", x + 50.80, y + 43.18, x + 40.64, y + 43.18, 180, pulldown_ref + "/1")
    result += wire_label("GND", x + 60.96, y + 43.18, x + 71.12, y + 43.18, 0, pulldown_ref + "/2")
    return result


def generate():
    ROW["check_libraries"](PROJECT_DIR)
    used_symbols = ["74HC4514PW,118", "DMP2066LSN-7", "2N7002K-7", "ERJ-2RKF1001X", "ERJ-2RKF1003X", "GRM155R71C104KA88D", "PWR_FLAG"]
    lines = [
        '(kicad_sch', '(version 20260306)', '(generator "rgb_badge_rows")', '(generator_version "1.0")',
        f'(uuid {quote(FILE_UUID)})', '(paper "A2")',
        '(title_block (title "Coupon Rev A - 16 row selectors") (rev "A-draft") (comment 1 "SPDX-License-Identifier: CERN-OHL-S-2.0") (comment 2 "Controller captured; VLED source and interlock pending"))',
        '(lib_symbols\n' + '\n'.join(cached_symbol(name) for name in used_symbols) + '\n)',
        note('16 decoded high-side row selectors', 20.32, 20.32, 'title', 2.0),
        note('E=HIGH blanks every decoder output. Firmware must blank, change A0..A3, wait, then enable.', 20.32, 27.94, 'timing'),
    ]

    # Decoder and its controller-side boundary nets.
    lines += component("74HC4514PW,118", "U2", "74HC4514PW,118", 60.96, 58.42)
    decoder_pins = {
        24: ("+3V3_APP", -15.24, 21.59), 2: ("ROW_A0", -15.24, 12.70),
        3: ("ROW_A1", -15.24, 10.16), 21: ("ROW_A2", -15.24, 7.62),
        22: ("ROW_A3", -15.24, 5.08), 1: ("+3V3_APP", -15.24, -2.54),
        23: ("ROW_ENABLE_N", -15.24, -7.62), 12: ("GND", -15.24, -21.59),
    }
    for pin, (net, px, py) in decoder_pins.items():
        lines += wire_label(net, 60.96 + px, 58.42 - py, 35.56, 58.42 - py, 180, f"U2/{pin}")
    q_pins = [11, 9, 10, 8, 7, 6, 5, 4, 18, 17, 20, 19, 14, 13, 16, 15]
    for index, pin in enumerate(q_pins):
        py = 19.05 - index * 2.54
        lines += wire_label(f"ROW_SEL_{index:02d}", 76.20, 58.42 - py, 91.44, 58.42 - py, 0, f"U2/{pin}")

    lines += component("GRM155R71C104KA88D", "C2", "100n 16V X7R", 132.08, 38.10)
    lines += wire_label("+3V3_APP", 127.00, 38.10, 116.84, 38.10, 180, "C2/1")
    lines += wire_label("GND", 137.16, 38.10, 147.32, 38.10, 0, "C2/2")
    for index in range(4):
        ref, y = f"R{38 + index}", 53.34 + index * 10.16
        lines += component("ERJ-2RKF1003X", ref, "100k 1%", 132.08, y)
        lines += wire_label(f"ROW_A{index}", 127.00, y, 116.84, y, 180, ref + "/1")
        lines += wire_label("GND", 137.16, y, 147.32, y, 0, ref + "/2")
    lines += component("ERJ-2RKF1003X", "R42", "100k 1%", 193.04, 38.10)
    lines += wire_label("+3V3_APP", 187.96, 38.10, 177.80, 38.10, 180, "R42/1")
    lines += wire_label("ROW_ENABLE_N", 198.12, 38.10, 208.28, 38.10, 0, "R42/2")
    lines += component("PWR_FLAG", "#FLG03", "PWR_FLAG", 193.04, 58.42)
    lines += wire_label("VLED", 193.04, 58.42, 208.28, 58.42, 0, "#FLG03/1")
    lines += [
        note('DRAFT VLED boundary flag only; it is not a regulator or startup interlock.', 177.80, 73.66, 'flag-note'),
        note('The later power sheet must hold VLED off through boot/reset/rail sequencing.', 177.80, 81.28, 'power-note'),
        note('2N7002K at 3.3 V sinks only the 1 kΩ pull-up current; Gate A acceptance and coupon measurement required.', 177.80, 88.90, 'nmos-note', 1.016),
    ]

    for index in range(16):
        x = 55.88 + (index % 4) * 134.62
        # Keep the final stage below y=358 mm, clear of the A2 title block.
        y = 121.92 + (index // 4) * 63.50
        lines += stage(index, x, y)
    lines += [
        note('One selected row: about 3.9 mA in its 1 kΩ gate pull-up at provisional 3.9 V VLED; value is calculated, not measured.', 20.32, 396.24, 'current-note', 1.016),
        note('Never fabricate from this sheet alone. Real rails, VLED interlock, DRC/DFM, Gate A and timing/ghosting tests remain.', 20.32, 403.86, 'release-note', 1.016),
        '(embedded_fonts no)', ')',
    ]
    return '\n'.join(lines) + '\n'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True, type=Path, help='New directory; existing paths are rejected')
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=False)
    (args.output / 'rows.kicad_sch').write_text(generate(), encoding='utf-8')
    print(f'Generated row-selection draft: U2, 16 P-MOSFETs, 16 N-MOSFETs, 37 resistors and C2 in {args.output}')


if __name__ == '__main__':
    main()
