#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Generate the unlinked, default-disabled TPS63020 VLED power stage."""

import argparse
import importlib.util
from pathlib import Path
import uuid


ROOT = Path(__file__).resolve().parents[1]
HELPER_PATH = ROOT / "tools/generate-coupon-3v3.py"
SPEC = importlib.util.spec_from_file_location("coupon_3v3_generator", HELPER_PATH)
helper = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(helper)
helper.SCOPE = uuid.UUID("9798f67a-1602-50f4-b414-6cd78f1329d9")
helper.FILE_UUID = str(uuid.uuid5(helper.SCOPE, "file"))
helper.PARTS = {
    "U37": ("TPS63020DSJT", "TPS63020DSJT", "VSON_TI_DSJ0014_4x3mm_P0.5mm_EP2.85x1.58mm", "Texas Instruments", "https://www.ti.com/lit/ds/symlink/tps63020.pdf", 15),
    "L2": ("DFE252012P-1R5M=P2", "1.5u 20%", "L_Murata_DFE252012P", "Murata", "https://www.murata.com/~/media/webrenewal/products/inductor/chip/tokoproducts/wirewoundmetalalloychiptype/m_dfe252012p.ashx", 2),
    "C44": ("GRM188R60J106ME47D", "10u 6.3V X5R", "C_Murata_GRM18_0603", "Murata", "https://pim.murata.com/en-global/pim/details/?partNum=GRM188R60J106ME47D", 2),
    "C45": ("GRM188R60J106ME47D", "10u 6.3V X5R", "C_Murata_GRM18_0603", "Murata", "https://pim.murata.com/en-global/pim/details/?partNum=GRM188R60J106ME47D", 2),
    "C46": ("GRM187R61A226ME15", "22u 10V X5R", "C_Murata_GRM18_0603", "Murata", "https://pim.murata.com/en-global/pim/details/?partNum=GRM187R61A226ME15", 2),
    "C47": ("GRM187R61A226ME15", "22u 10V X5R", "C_Murata_GRM18_0603", "Murata", "https://pim.murata.com/en-global/pim/details/?partNum=GRM187R61A226ME15", 2),
    "C48": ("GRM187R61A226ME15", "22u 10V X5R", "C_Murata_GRM18_0603", "Murata", "https://pim.murata.com/en-global/pim/details/?partNum=GRM187R61A226ME15", 2),
    "C49": ("GRM187R61A226ME15", "22u 10V X5R", "C_Murata_GRM18_0603", "Murata", "https://pim.murata.com/en-global/pim/details/?partNum=GRM187R61A226ME15", 2),
    "C50": ("GRM155R71C104KA88D", "100n 16V X7R", "C_Murata_GRM15_0402", "Murata", "https://pim.murata.com/asset/pim4/ceramicCapacitorSMD/GRM155R71C104KA88-01A-EN_PDF_CERAMICCAPACITORSMD", 2),
    "R84": ("ERJ2RKF6203X", "620k 1%", "R_Panasonic_ERJ2_0402", "Panasonic", "https://industrial.panasonic.com/ww/products/pt/general-purpose-chip-resistors/models/ERJ2RKF6203X", 2),
    "R85": ("ERJ2RKF6203X", "620k 1%", "R_Panasonic_ERJ2_0402", "Panasonic", "https://industrial.panasonic.com/ww/products/pt/general-purpose-chip-resistors/models/ERJ2RKF6203X", 2),
    "R86": ("ERJ2RKF1803X", "180k 1%", "R_Panasonic_ERJ2_0402", "Panasonic", "https://industrial.panasonic.com/ww/products/pt/general-purpose-chip-resistors/models/ERJ2RKF1803X", 2),
    "R87": ("ERJ2RKF1003X", "100k 1%", "R_Panasonic_ERJ2_0402", "Panasonic", "https://industrial.panasonic.com/ww/products/pt/general-purpose-chip-resistors/models/ERJ2RKF1003X", 2),
}


def label(net, x, y, name, angle=0):
    justify = "right" if angle == 180 else "left"
    return f'(global_label {helper.q(net)} (shape passive) (at {x:.3f} {y:.3f} {angle}) {helper.effects(justify=justify)} (uuid {helper.q(helper.uid(name))}) {helper.prop("Intersheetrefs", "${INTERSHEET_REFS}", x, y, True)})'


def junction(x, y, name):
    return f'(junction (at {x:.3f} {y:.3f}) (diameter 0) (color 0 0 0 0) (uuid {helper.q(helper.uid(name))}))'


def generate():
    h = helper
    symbols = dict.fromkeys(part[0] for part in h.PARTS.values())
    lines = [
        "(kicad_sch", "(version 20260306)", '(generator "rgb_badge_vled_candidate")',
        '(generator_version "1.0")', f'(uuid {h.q(h.FILE_UUID)})', '(paper "A3")',
        '(title_block (title "Coupon Rev A - unlinked VLED converter candidate") (rev "A-draft") (comment 1 "SPDX-License-Identifier: CERN-OHL-S-2.0") (comment 2 "DO NOT LINK: SYS and display interlock pending"))',
        "(lib_symbols\n" + "\n".join(h.cached_symbol(mpn) for mpn in symbols) + "\n)",
        f'(text "Default-disabled power stage. EN requires hardware interlock; input source remains draft." (at 20.32 20.32 0) {h.effects(justify="left")} (uuid {h.q(h.uid("note/enable"))}))',
        f'(text "PG deliberately unused here. VLED discharge, row blanking and load-step tests remain." (at 20.32 27.94 0) {h.effects(justify="left")} (uuid {h.q(h.uid("note/pg"))}))',
    ]
    positions = {
        "U37": (147.32, 96.52), "L2": (147.32, 137.16),
        "C44": (76.20, 55.88), "C45": (76.20, 73.66), "C50": (76.20, 139.70),
        "C46": (254.00, 66.04), "C47": (254.00, 83.82),
        "C48": (254.00, 101.60), "C49": (254.00, 119.38),
        "R84": (254.00, 139.70), "R85": (254.00, 157.48),
        "R86": (254.00, 175.26), "R87": (76.20, 119.38),
    }
    for ref, (x, y) in positions.items():
        lines.extend(h.component(ref, x, y))
    # All IC pins match the manufacturer's DSJ top-view numbering. L1/L2
    # nodes are local switching copper, not global intersheet labels.
    for name, y in [("VINA", 86.36), ("VIN10", 88.90), ("VIN11", 91.44)]:
        lines.append(h.wire(133.35, y, 118.11, y, "U37/" + name + "/wire"))
    lines.append(h.wire(118.11, 86.36, 118.11, 91.44, "U37/VIN/vertical"))
    lines.append(junction(118.11, 88.90, "U37/VIN/junction"))
    lines.append(h.wire(91.44, 86.36, 118.11, 86.36, "U37/VIN/label_wire"))
    lines.append(label("+SYS_APP_IN_DRAFT", 91.44, 86.36, "U37/VIN/label", 180))
    for name, y in [("VOUT4", 86.36), ("VOUT5", 88.90)]:
        lines.append(h.wire(161.29, y, 180.34, y, "U37/" + name + "/wire"))
    lines.append(h.wire(180.34, 86.36, 180.34, 88.90, "U37/VOUT/vertical"))
    lines.append(label("VLED", 180.34, 86.36, "U37/VOUT/label"))
    lines.extend(h.labelled("VLED_ENABLE_DRAFT", 133.35, 101.60, 76.20, 101.60, "U37/EN"))
    lines.extend(h.labelled("GND", 133.35, 104.14, 118.11, 104.14, "U37/PS"))
    lines.extend(h.labelled("VLED_FB", 161.29, 104.14, 193.04, 104.14, "U37/FB"))
    for name, x in [("GND", 144.78), ("PGND_EP", 149.86)]:
        lines.append(h.wire(x, 111.76, x, 119.38, "U37/" + name + "/wire"))
    lines.append(h.wire(144.78, 119.38, 180.34, 119.38, "U37/GND/bus"))
    lines.append(junction(149.86, 119.38, "U37/GND/junction"))
    lines.append(label("GND", 180.34, 119.38, "U37/GND/label"))
    lines.append(f'(no_connect (at 161.290 101.600) (uuid {h.q(h.uid("U37/PG/no-connect"))}))')
    for side, pin_x, bend_x, coil_x, pin_y1, pin_y2 in [
        ("L1", 133.35, 124.46, 142.24, 93.98, 96.52),
        ("L2", 161.29, 170.18, 152.40, 93.98, 96.52),
    ]:
        lines.extend([
            h.wire(pin_x, pin_y1, bend_x, pin_y1, side + "/top"),
            h.wire(pin_x, pin_y2, bend_x, pin_y2, side + "/bottom_pin"),
            h.wire(bend_x, pin_y1, bend_x, 137.16, side + "/vertical"),
            h.wire(bend_x, 137.16, coil_x, 137.16, side + "/coil"),
        ])
        lines.append(f'(junction (at {bend_x:.3f} {pin_y2:.3f}) (diameter 0) (color 0 0 0 0) (uuid {h.q(h.uid(side + "/junction"))}))')
    two_pin_nets = {
        "C44": ("+SYS_APP_IN_DRAFT", "GND"),
        "C45": ("+SYS_APP_IN_DRAFT", "GND"),
        "C50": ("+SYS_APP_IN_DRAFT", "GND"),
        "C46": ("VLED", "GND"), "C47": ("VLED", "GND"),
        "C48": ("VLED", "GND"), "C49": ("VLED", "GND"),
        "R84": ("VLED", "VLED_FB_TOP_MID"),
        "R85": ("VLED_FB_TOP_MID", "VLED_FB"),
        "R86": ("VLED_FB", "GND"),
        "R87": ("VLED_ENABLE_DRAFT", "GND"),
    }
    for ref, (upper, lower) in two_pin_nets.items():
        x, y = positions[ref]
        lines.extend(h.labelled(upper, x - 5.08, y, x - 20.32, y, ref + "/1"))
        lines.extend(h.labelled(lower, x + 5.08, y, x + 20.32, y, ref + "/2"))
    lines.extend(["(embedded_fonts no)", ")"])
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=False)
    (args.output / "vled-converter.kicad_sch").write_text(generate(), encoding="utf-8")


if __name__ == "__main__":
    main()
