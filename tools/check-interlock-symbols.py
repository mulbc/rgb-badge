#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Check the first exact interlock symbols against TI package pin tables."""

from pathlib import Path
import runpy


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / "hardware/coupon/rev-a"
LIB = runpy.run_path(str(ROOT / "tools/check-power-libraries.py"))
children = LIB["children"]
one = LIB["one"]
pins = LIB["library_pins"]
props = LIB["property_map"]

EXPECTED = {
    "TPS3823A-33DBVR": ("SOT23_TI_DBV0005A", "tps3823", {
        1: ("RESET", "output", "inverted"), 2: ("GND", "power_in", "line"),
        3: ("MR", "input", "inverted"), 4: ("WDI", "input", "line"),
        5: ("VDD", "power_in", "line"),
    }),
    "SN74LVC1G74RSER": ("UQFN_TI_RSE0008A_1.5x1.5mm_P0.5mm", "sn74lvc1g74", {
        1: ("CLK", "input", "clock"), 2: ("D", "input", "line"),
        3: ("Q", "output", "inverted"), 4: ("GND", "power_in", "line"),
        5: ("Q", "output", "line"), 6: ("CLR", "input", "inverted"),
        7: ("PRE", "input", "inverted"), 8: ("VCC", "power_in", "line"),
    }),
    "SN74LVC1G04DSFR": ("X2SON_TI_DSF0006A_1x1mm_P0.35mm", "sn74lvc1g04", {
        1: ("NC", "no_connect", "line"), 2: ("A", "input", "line"),
        3: ("GND", "power_in", "line"), 4: ("Y", "output", "inverted"),
        5: ("NC", "no_connect", "line"), 6: ("VCC", "power_in", "line"),
    }),
    "SN74LVC1G08DSFR": ("X2SON_TI_DSF0006A_1x1mm_P0.35mm", "sn74lvc1g08", {
        1: ("A", "input", "line"), 2: ("B", "input", "line"),
        3: ("GND", "power_in", "line"), 4: ("Y", "output", "line"),
        5: ("NC", "no_connect", "line"), 6: ("VCC", "power_in", "line"),
    }),
    "SN74LVC2G00DCUR": ("VSSOP_TI_DCU0008A", "sn74lvc2g00", {
        1: ("1A", "input", "line"), 2: ("1B", "input", "line"),
        3: ("2Y", "output", "inverted"), 4: ("GND", "power_in", "line"),
        5: ("2A", "input", "line"), 6: ("2B", "input", "line"),
        7: ("1Y", "output", "inverted"), 8: ("VCC", "power_in", "line"),
    }),
    "SN74LVC2G08DCUR": ("VSSOP_TI_DCU0008A", "sn74lvc2g08", {
        1: ("1A", "input", "line"), 2: ("1B", "input", "line"),
        3: ("2Y", "output", "line"), 4: ("GND", "power_in", "line"),
        5: ("2A", "input", "line"), 6: ("2B", "input", "line"),
        7: ("1Y", "output", "line"), 8: ("VCC", "power_in", "line"),
    }),
}


def main():
    root = LIB["parse"](PROJECT / "symbols/rgb-badge-coupon.kicad_sym")
    by_name = {symbol[1]: symbol for symbol in children(root, "symbol")}
    for mpn, (land, slug, pin_table) in EXPECTED.items():
        symbol = by_name[mpn]
        properties = props(symbol)
        assert properties["MPN"] == mpn and properties["Value"] == mpn
        assert properties["Manufacturer"] == "Texas Instruments"
        assert properties["Footprint"] == f"rgb-badge-coupon:{land}"
        assert properties["Datasheet"] == f"https://www.ti.com/lit/ds/symlink/{slug}.pdf"
        assert (PROJECT / "footprints/rgb-badge-coupon.pretty" / f"{land}.kicad_mod").exists()
        actual = {int(number): (one(pin, "name", "pin")[1], pin[1], pin[2])
                  for number, pin in pins(symbol).items()}
        assert actual == pin_table, f"{mpn}: manufacturer pin number/function/type mismatch"
    print("Six TI interlock symbols: exact MPN, land and 41 numbered pin functions passed")


if __name__ == "__main__":
    main()
