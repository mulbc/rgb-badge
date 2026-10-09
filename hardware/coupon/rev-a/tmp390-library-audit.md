<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# TMP390 temperature-switch library audit

2026-10-09. [ADR 0024](../../../docs/decisions/0024-lp452845-pack-and-temperature-window.md) selects TI `TMP390A2DRLR` for the battery-facing charge inhibit. The project-local [symbol](symbols/rgb-badge-coupon.kicad_sym) and [DRL0006A footprint](footprints/rgb-badge-coupon.pretty/SOT563_TI_DRL0006A.kicad_mod) are candidate source parts; neither is populated in the canonical schematic. The source is [TI TMP390 Rev A](https://www.ti.com/lit/ds/symlink/tmp390.pdf), pin diagram and table on page 3, DRL0006A package drawing and example board/stencil layout on pages 24–26.

| Top-view pin | TI function | Symbol electrical type | Footprint pad centre (mm) |
|---:|---|---|---|
| 1 | SETA, hot-trip programming resistor to ground | Input | (−0.74, −0.50) |
| 2 | SETB, cold-trip/hysteresis resistor to ground | Input | (−0.74, 0) |
| 3 | GND | Power input | (−0.74, +0.50) |
| 4 | OUTB, active-low open drain cold fault | Open collector | (+0.74, +0.50) |
| 5 | VDD | Power input | (+0.74, 0) |
| 6 | OUTA, active-low open drain hot fault | Open collector | (+0.74, −0.50) |

The TI example land has six **0.67 × 0.30 mm** pads, 0.50 mm pitch along each row and 1.48 mm row-centre separation. This footprint transcribes those dimensions directly, with a 2.70 × 2.50 mm first-author courtyard and pin-one dot at the upper left in the top view. Copper, mask and paste use the same pad outlines; the drawing's preferred non-solder-mask-defined opening and example 0.1 mm stencil are the assembly starting points, not an assembler approval. No body thermal contact pad exists.

KiCad CLI 10.0.6 parsed and exported the exact symbol and footprint to SVG on 2026-10-09. First-author visual inspection confirmed the top-view left 1–3/right 6–4 order, pin-one marker, six equal lands and symbol names. The unchanged root schematic still reports zero ERC violations, but that does not validate a not-yet-placed component. Independent pin/pad, package orientation and stencil/assembly review remain required before a fabrication release.
