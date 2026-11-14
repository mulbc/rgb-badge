<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Exact E0 input capacitor and TDK C1608 land

2026-10-11. Candidate library for [ADR 0027](../../../docs/decisions/0027-e0-protected-usb-source-selection.md); not yet placed.

TDK lists exact `C1608X7R1H105K080AB` as in production: 1 µF ±10%, 50 Vdc, X7R, 0603 C1608 body 1.60 ±0.10 × 0.80 ±0.10 mm and 0.80 ±0.10 mm thick. It has two nonpolar terminals with minimum 0.20 mm terminal width. The manufacturer [part page](https://product.tdk.com/en/search/capacitor/ceramic/mlcc/info?part_no=C1608X7R1H105K080AB) and [commercial MLCC specification](https://product.tdk.com/system/files/dam/doc/product/capacitor/ceramic/mlcc/specification/mlccspec_commercial_general_c1608x7r1a106_en.pdf) give reflow land A/B/C ranges of 0.6–0.8 mm. The project-local `C_TDK_C1608_0603` footprint uses the midpoint 0.7 mm center gap, 0.7 mm pad length and 0.7 mm pad width: two 0.7 × 0.7 mm pads at x = ±0.7 mm. Body and courtyard are 1.6 × 0.8 and 2.6 × 1.2 mm. The land dimensions are source-derived; solder process and DC-bias capacitance remain review items. The Murata-named 0603 land is intentionally not reused.

KiCad CLI 10.0.6 exported the new symbol and footprint to `/private/tmp/rgb-e0-lib-preview/`; the footprint copper, body and courtyard were visually inspected. No manufacturer curve has yet established effective capacitance under all specified bias, aging and temperature conditions; the nominal 1 µF and 50 V labels alone do not close connector transient suitability. Source placement and full native ERC/XML still await the E0 capture.
