<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# KiCad 10.0.6 3.3 V passive library review at 8014947

2026-09-30. First-author review of the owner's macOS native export `3v3-cap-review-8014947.zip`, SHA-256 `32dad21b7ec915e794e49efc2413806df3b4a1ee38fba88057e0c203b7406073`, and its accompanying command log. The logged branch checkout reached exact source commit `8014947`, and `git status --short` produced no reported changes. The run exported all project symbols and footprint layer views, then completed configured KiCad ERC with **zero errors and zero warnings**. Native XML checks reported **400 PCB items and 1,507 logical pins** in the previously staged circuit. These totals exclude the new unplaced passives and do not validate the 3.3 V converter circuit.

## Render inspection

| Native export inspected | First-author disposition |
|---|---|
| `symbols/GRM187R61A226ME15_unit1.svg` | Two readable, nonpolar capacitor terminals 1/2; reference and exact base MPN value are legible and clear of the symbol. |
| `symbols/GRM219R60J476ME44_unit1.svg` | Same readable, nonpolar pin map and property placement; no visible heading overlap. |
| `footprints/fabrication/C_Murata_GRM21_0805.svg` | Two lands, 1 on the left and 2 on the right; visible body and courtyard outlines and a readable reference above. Fab value extends below the part as expected; no polarity mark is invented. The plotted numeral position is for a library review, not a component silkscreen mark. |
| `footprints/copper/C_Murata_GRM21_0805.svg`, `footprints/paste/C_Murata_GRM21_0805.svg` | Two separated rectangular lands in each view; paste follows both lands with no bridge or unexpected center opening. Dimensions are source-checked by `tools/check-3v3-capacitor-footprints.py`, rather than inferred from the pixels. |
| `footprints/mechanical/C_Murata_GRM21_0805.svg` | Single body outline/value view, no extra mechanical land. |
| `symbols/ERJ-2RKF5113X_unit1.svg`, `symbols/ERJ-2RKF9102X_unit1.svg` | Both staged feedback symbols also render clearly as two passive terminals with legible reference/value. Existing `R_Panasonic_ERJ2_0402` fabrication/copper render was inspected; no newly introduced geometry issue. This is **visual acceptance only**; reconcile the manufacturer's unhyphenated order code before selecting BOM parts. |

The source geometry comparison is recorded in the [Murata capacitor library audit](../../hardware/coupon/rev-a/3v3-capacitor-footprint-audit.md). The native run and this visual inspection close the **first-author export/render checkpoint** for the staged capacitor and feedback symbols. They do not qualify the older reference sheets as current manufacturer approval drawings, prove component derating, approve assembly placement, or test the unbuilt regulator. The exact capacitor packaging suffix, combined effective capacitance over bias/temperature/aging, `SYS` fault transients, passives' final placement, native converter ERC/XML and independent Gate A review remain open. No fabrication files or battery order are authorized.
