#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Check staged exact-MPN 3.3 V feedback symbols against the audited ERJ2 land.

This is a source comparison, not native KiCad rendering or a circuit check.
"""

from pathlib import Path
import runpy

TOOLS = Path(__file__).resolve().parent
LED = runpy.run_path(str(TOOLS / "check-led-libraries.py"))
parse, children = LED["parse_sexpr"], LED["children"]
PROJECT = TOOLS.parent / "hardware" / "coupon" / "rev-a"
REFERENCE = "ERJ-2RKF1002X"
PARTS = {"ERJ2RKF5113X": 511000, "ERJ2RKF9102X": 91000}


def replace_strings(node, original, new):
    if isinstance(node, list):
        return [replace_strings(item, original, new) for item in node]
    return node.replace(original, new) if isinstance(node, str) else node


def check(project=PROJECT):
    library = parse(project / "symbols" / "rgb-badge-coupon.kicad_sym")
    symbols = {s[1]: s for s in children(library, "symbol")}
    reference = symbols[REFERENCE]
    for mpn, resistance in PARTS.items():
        if mpn not in symbols:
            raise ValueError(f"Missing 3.3 V feedback symbol {mpn}")
        if symbols[mpn] != replace_strings(reference, REFERENCE, mpn):
            raise ValueError(f"{mpn}: MPN, manufacturer source, footprint or passive-pin geometry differs from audited ERJ2")
        code = mpn.removeprefix("ERJ2RKF").removesuffix("X")
        if len(code) != 4 or int(code[:3]) * 10 ** int(code[3]) != resistance:
            raise ValueError(f"{mpn}: value code mismatch")
    return len(PARTS)


if __name__ == "__main__":
    print(f"3.3 V feedback library check passed: {check()} exact Panasonic MPNs, passive pins and reused ERJ2 land.")
    print("Resistors remain unplaced; native export, rail transients and Gate A remain open.")
