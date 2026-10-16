#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Generate an unlinked two-part charger EN2 source candidate."""

import importlib.util
from pathlib import Path
import uuid

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / "hardware/coupon/rev-a"
SPEC = importlib.util.spec_from_file_location("coupon_3v3_generator", ROOT / "tools/generate-coupon-3v3.py")
h = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(h)
h.SCOPE = uuid.UUID("eb56e9ca-7c2d-5f28-aabc-6fcf28f33f46")
h.FILE_UUID = str(uuid.uuid5(h.SCOPE, "file"))
h.PARTS = {
    "R88": ("ERJ2RKF1002X", "10k 1%", "R_Panasonic_ERJ2_0402", "Panasonic", "https://industrial.panasonic.com/ww/products/pt/general-purpose-chip-resistors/models/ERJ2RKF1002X", 2),
    "U38": ("LM4040A25IDBZT", "2.5V shunt", "SOT23_TI_DBZ0003A", "Texas Instruments", "https://www.ti.com/lit/ds/symlink/lm4040.pdf", 3),
}


def generate():
    candidate = PROJECT / "staging/charger-en2"
    shunt_lib = (candidate / "charger-en2-candidate.kicad_sym").read_text()
    shunt = shunt_lib[shunt_lib.index('(symbol "LM4040A25IDBZT"'):].rsplit('\n)', 1)[0]
    shunt = shunt.replace('(symbol "LM4040A25IDBZT"', '(symbol "rgb-badge-coupon:LM4040A25IDBZT"', 1)
    resistor = h.cached_symbol('ERJ2RKF1002X')
    local_resistor = resistor.replace('(symbol "rgb-badge-coupon:ERJ2RKF1002X"', '(symbol "ERJ2RKF1002X"', 1)
    local_shunt = shunt.replace('(symbol "rgb-badge-coupon:LM4040A25IDBZT"', '(symbol "LM4040A25IDBZT"', 1)
    (candidate / 'charger-en2-candidate-symbols.kicad_sym').write_text(
        '(kicad_symbol_lib (version 20251024) (generator "rgb_badge")\n'
        + local_resistor + '\n' + local_shunt + '\n)\n')
    lines = [
        '(kicad_sch', '(version 20260306)', '(generator "rgb_badge_charger_en2_candidate")',
        '(generator_version "1.0")', f'(uuid {h.q(h.FILE_UUID)})', '(paper "A4")',
        '(title_block (title "Unlinked charger EN2 local clamp candidate") (rev "A-draft") (comment 1 "SPDX-License-Identifier: CERN-OHL-S-2.0") (comment 2 "NOT ROOT-LINKED; EN2 load and transitions unqualified"))',
        '(lib_symbols\n' + resistor + '\n' + shunt + '\n)',
        f'(text "Candidate only: E1 OUT / BQ IN = CHARGER_IN; BQ EN2 = CHARGER_EN2." (at 20.32 20.32 0) {h.effects(justify="left")} (uuid {h.q(h.uid("note"))}))',
    ]
    lines.extend(h.component('R88', 76.20, 80.01))
    lines.extend(h.component('U38', 111.76, 80.01))
    lines.extend(h.labelled('CHARGER_IN', 71.12, 80.01, 50.80, 80.01, 'R88/in'))
    lines.extend(h.labelled('CHARGER_EN2', 81.28, 80.01, 96.52, 80.01, 'R88/out'))
    lines.extend(h.labelled('CHARGER_EN2', 104.14, 80.01, 99.06, 80.01, 'U38/K'))
    lines.extend(h.labelled('GND', 119.38, 80.01, 139.70, 80.01, 'U38/A'))
    lines.extend(h.labelled('GND', 119.38, 82.55, 139.70, 82.55, 'U38/third'))
    lines.extend(['(embedded_fonts no)', ')'])
    return '\n'.join(lines) + '\n'


if __name__ == '__main__':
    (PROJECT / 'staging/charger-en2/charger-en2-candidate.kicad_sch').write_text(generate())
