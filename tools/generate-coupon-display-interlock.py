#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Generate the source-connected, output-isolated display-interlock trial."""

import argparse
import importlib.util
from pathlib import Path
import runpy
import uuid


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / "hardware/coupon/rev-a"
spec = importlib.util.spec_from_file_location("coupon_3v3_generator", ROOT / "tools/generate-coupon-3v3.py")
h = importlib.util.module_from_spec(spec)
spec.loader.exec_module(h)
h.SCOPE = uuid.UUID("4b19920a-0e81-552f-87aa-aee5c816de7d")
h.FILE_UUID = str(uuid.uuid5(h.SCOPE, "file"))
SHEET_UUID = str(uuid.uuid5(h.SCOPE, "root-sheet"))
ROOT_UUID = "207fb68e-2ddb-46bb-8712-eba2f8c5eef6"
lib = runpy.run_path(str(ROOT / "tools/check-power-libraries.py"))
library = lib["parse"](h.LIBRARY)
symbols = {node[1]: node for node in lib["children"](library, "symbol")}


def ti(mpn, land, slug, count):
    return (mpn, mpn, land, "Texas Instruments", f"https://www.ti.com/lit/ds/symlink/{slug}.pdf", count)


def resistor(mpn):
    return (mpn, mpn, "R_Panasonic_ERJ2_0402", "Panasonic",
            f"https://industrial.panasonic.com/ww/products/pt/general-purpose-chip-resistors/models/{mpn}", 2)


CAP = ("GRM155R71C104KA88D", "100n 16V X7R", "C_Murata_GRM15_0402", "Murata",
       "https://pim.murata.com/asset/pim4/ceramicCapacitorSMD/GRM155R71C104KA88-01A-EN_PDF_CERAMICCAPACITORSMD", 2)
TP = ("TestPoint_Pad", "TestPoint_Pad", "TestPoint_Pad_D1.0mm", "", "", 1)

h.PARTS = {
    "U47": ti("TPS3823A-33DBVR", "SOT23_TI_DBV0005A", "tps3823", 5),
    "U48": ti("SN74LVC1G04DSFR", "X2SON_TI_DSF0006A_1x1mm_P0.35mm", "sn74lvc1g04", 6),
    "U49": ti("SN74LVC1G74RSER", "UQFN_TI_RSE0008A_1.5x1.5mm_P0.5mm", "sn74lvc1g74", 8),
    "U50": ti("SN74LVC1G74RSER", "UQFN_TI_RSE0008A_1.5x1.5mm_P0.5mm", "sn74lvc1g74", 8),
    "U51": ti("SN74LVC1G11DRYR", "USON_TI_DRY0006A_1p45x1mm_P0p5mm", "sn74lvc1g11", 6),
    "U52": ti("SN74LVC1G08DSFR", "X2SON_TI_DSF0006A_1x1mm_P0.35mm", "sn74lvc1g08", 6),
    "U53": ti("TLV6700DSER", "WSON_TI_DSE0006A_1p5x1p5mm_P0p5mm", "tlv6700", 6),
    "U54": ti("SN74LVC2G00DCUR", "VSSOP_TI_DCU0008A", "sn74lvc2g00", 8),
    "U55": ti("SN74LVC2G08DCUR", "VSSOP_TI_DCU0008A", "sn74lvc2g08", 8),
    **{f"C{n}": CAP for n in range(66, 75)},
    "R103": resistor("ERJ2RKF1001X"),
    "R104": resistor("ERJ2RKF1002X"),
    "R105": resistor("ERJ2RKF1002X"),
    "R106": resistor("ERJ2RKF1002X"),
    "R107": resistor("ERJ2RKF1003X"),
    "R108": resistor("ERJ2RKF1003X"),
    "R109": resistor("ERJ2RKF1603X"),
    "R110": resistor("ERJ2RKF2002X"),
    "R111": resistor("ERJ2RKF1963X"),
    "R112": resistor("ERJ2RKF2002X"),
    "R113": resistor("ERJ2RKF4701X"),
    "TP13": TP,
    "TP14": TP,
}

PIN_NETS = {
    "U47": {1: "APP_SUPERVISOR_OK", 2: "GND", 3: "+3V3_APP", 4: "DISPLAY_HEARTBEAT", 5: "+3V3_APP"},
    "U48": {2: "DISPLAY_HEARTBEAT", 3: "GND", 4: "HEARTBEAT_FALL_CLK", 6: "+3V3_APP"},
    "U49": {1: "HEARTBEAT_FALL_CLK", 2: "+3V3_APP", 4: "GND", 5: "HEARTBEAT_SEEN", 6: "DISPLAY_CLEAR_OK", 7: "+3V3_APP", 8: "+3V3_APP"},
    "U50": {1: "DISPLAY_ARM_CLK", 2: "HEARTBEAT_SEEN", 4: "GND", 5: "ARM_LATCH", 6: "DISPLAY_CLEAR_OK", 7: "+3V3_APP", 8: "+3V3_APP"},
    "U51": {1: "APP_SUPERVISOR_OK", 2: "GND", 3: "ESP_EN", 4: "DISPLAY_CLEAR_3", 5: "+3V3_APP", 6: "MODE_BOOT_N"},
    "U52": {1: "DISPLAY_CLEAR_3", 2: "DISPLAY_ENABLE", 3: "GND", 4: "DISPLAY_CLEAR_OK", 6: "+3V3_APP"},
    "U53": {1: "VLED_WINDOW_OK", 2: "+3V3_APP", 3: "VLED_HIGH_SENSE", 4: "VLED_LOW_SENSE", 5: "GND", 6: "VLED_WINDOW_OK"},
    "U54": {1: "ROW_ENABLE_REQ_N", 2: "ROW_ENABLE_REQ_N", 3: "ROW_ENABLE_N_CANDIDATE", 4: "GND", 5: "ROW_ARM", 6: "ROW_REQUEST", 7: "ROW_REQUEST", 8: "+3V3_APP"},
    "U55": {1: "ARM_LATCH", 2: "DISPLAY_ENABLE", 3: "ROW_ARM", 4: "GND", 5: "ARM_LATCH", 6: "VLED_WINDOW_OK", 7: "VLED_ENABLE_CANDIDATE", 8: "+3V3_APP"},
}

RESISTOR_NETS = {
    "R103": ("DISPLAY_HEARTBEAT", "GND"),
    "R104": ("+3V3_APP", "VLED_WINDOW_OK"),
    "R105": ("DISPLAY_ENABLE", "GND"),
    "R106": ("+3V3_APP", "ROW_ENABLE_REQ_N"),
    "R107": ("DISPLAY_ARM_CLK", "GND"),
    "R108": ("DISPLAY_CLEAR_OK", "GND"),
    "R109": ("VLED", "VLED_LOW_SENSE"),
    "R110": ("VLED_LOW_SENSE", "GND"),
    "R111": ("VLED", "VLED_HIGH_SENSE"),
    "R112": ("VLED_HIGH_SENSE", "GND"),
    "R113": ("VLED", "GND"),
}


def label(net, x, y, angle, name):
    justify = "right" if angle == 180 else "left"
    return (f'(global_label {h.q(net)} (shape passive) (at {x:.3f} {y:.3f} {angle}) '
            f'{h.effects(justify=justify)} (uuid {h.q(h.uid(name))}) '
            f'{h.prop("Intersheetrefs", "${INTERSHEET_REFS}", x, y, True)})')


def attached(ref, pin, net, x, y):
    node = lib["library_pins"](symbols[h.PARTS[ref][0]])[str(pin)]
    at = lib["one"](node, "at", "symbol pin")
    rel_x, rel_y = float(at[1]), float(at[2])
    px, py = x + rel_x, y - rel_y
    if rel_x < 0:
        ex, ey, angle = px - 12.7, py, 180
    elif rel_x > 0:
        ex, ey, angle = px + 12.7, py, 0
    else:
        ex, ey, angle = px, py - 5.08 if rel_y > 0 else py + 5.08, 0
    name = f"{ref}/{pin}"
    return [h.wire(px, py, ex, ey, name + "/wire"), label(net, ex, ey, angle, name + "/label")]


def generate():
    lines = ["(kicad_sch", "(version 20260306)", '(generator "rgb_badge_display_interlock")',
             '(generator_version "1.0")', f'(uuid {h.q(h.FILE_UUID)})', '(paper "A2")',
             '(title_block (title "Coupon Rev A - provisional display interlock") (rev "A-draft") (comment 1 "SPDX-License-Identifier: CERN-OHL-S-2.0") (comment 2 "Outputs isolated from VLED EN and row decoder E"))',
             "(lib_symbols\n" + "\n".join(h.cached_symbol(mpn) for mpn in dict.fromkeys(p[0] for p in h.PARTS.values())) + "\n)",
             f'(text "Source-connected interlock trial. Candidate outputs reach test pads only; the display stays dark." (at 20.320 20.320 0) {h.effects(justify="left")} (uuid {h.q(h.uid("note/dark"))}))',
             f'(text "Qualify clear timing, rail loss, VLED decay, GPIO defaults and assembler stencil before output connection." (at 20.320 27.940 0) {h.effects(justify="left")} (uuid {h.q(h.uid("note/holds"))}))']
    positions = {
        "U47": (65.0, 100.0), "U48": (160.0, 100.0), "U49": (260.0, 100.0), "U50": (380.0, 100.0),
        "U51": (65.0, 190.0), "U52": (160.0, 190.0), "U53": (260.0, 190.0),
        "U54": (380.0, 190.0), "U55": (495.0, 190.0),
        **{f"C{66+i}": (45.0 + 54.0 * i, 265.0) for i in range(9)},
        **{f"R{103+i}": (70.0 + 90.0 * (i % 6), 315.0 + 40.0 * (i // 6))
           for i in range(11)},
        "TP13": (470.0, 235.0), "TP14": (540.0, 235.0),
    }
    positions = {ref: (round(x / 1.27) * 1.27, round(y / 1.27) * 1.27)
                 for ref, (x, y) in positions.items()}
    for ref, (x, y) in positions.items():
        lines.extend(h.component(ref, x, y))
        if ref in PIN_NETS:
            for pin in range(1, h.PARTS[ref][5] + 1):
                if pin in PIN_NETS[ref]:
                    lines.extend(attached(ref, pin, PIN_NETS[ref][pin], x, y))
                else:
                    node = lib["library_pins"](symbols[h.PARTS[ref][0]])[str(pin)]
                    at = lib["one"](node, "at", "symbol pin")
                    px, py = x + float(at[1]), y - float(at[2])
                    lines.append(f'(no_connect (at {px:.3f} {py:.3f}) (uuid {h.q(h.uid(ref + "/" + str(pin) + "/nc"))}))')
        elif ref.startswith("C"):
            lines.extend(attached(ref, 1, "+3V3_APP", x, y))
            lines.extend(attached(ref, 2, "GND", x, y))
        elif ref in RESISTOR_NETS:
            for pin, net in enumerate(RESISTOR_NETS[ref], 1):
                lines.extend(attached(ref, pin, net, x, y))
        else:
            lines.extend(attached(ref, 1, "VLED_ENABLE_CANDIDATE" if ref == "TP13" else "ROW_ENABLE_N_CANDIDATE", x, y))
    lines.extend(["(embedded_fonts no)", ")"])
    source = "\n".join(lines) + "\n"
    return source.replace(f'(path "/{h.FILE_UUID}"', f'(path "/{ROOT_UUID}/{SHEET_UUID}"')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=False)
    (args.output / "display-interlock.kicad_sch").write_text(generate(), encoding="utf-8")


if __name__ == "__main__":
    main()
