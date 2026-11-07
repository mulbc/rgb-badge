<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# TCA9517ADGKR local library audit, 2026-10-11

[ADR 0030](../../../docs/decisions/0030-gauge-bus-buffer-selection.md) selects TI `TCA9517ADGKR` in DGK0008A VSSOP-8. The [project-local symbol](symbols/rgb-badge-coupon.kicad_sym) maps pins **1 VCCA, 2 SCLA, 3 SDAA, 4 GND, 5 EN, 6 SDAB, 7 SCLB, 8 VCCB**, matching TI's Rev E top-view pin table. The [project-local land](footprints/rgb-badge-coupon.pretty/VSSOP_TI_DGK0008A.kicad_mod) places pads 1–4 down the left and 5–8 up the right, with 0.65 mm pitch, 1.4 × 0.45 mm contact lands and 4.4 mm overall copper span from TI's DGK example board layout. The 3.0 × 3.0 mm nominal body and 4.9 × 3.7 mm first-author courtyard are source assumptions for fit review; the footprint carries no external 3D model.

The [library checker](../../../tools/check-gauge-buffer-library.py) fixes exact part name, pin names/numbers, contact coordinates/sizes/layers, courtyard and local-model rule. KiCad CLI 10.0.6 exported the symbol and copper/mechanical SVG views to `/private/tmp/rgb-gauge-lib-review/`; the rendered symbol and mechanical view were visually inspected. This is library validation only. The symbol and land are not yet placed in the root schematic, and neither bus behavior nor powered-off leakage has been measured.

Primary sources: [TI exact orderable part](https://www.ti.com/product/TCA9517A/part-details/TCA9517ADGKR); [TI TCA9517A Rev E datasheet](https://www.ti.com/lit/ds/symlink/tca9517a.pdf), pin table and DGK0008A example board layout.
