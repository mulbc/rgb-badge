<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Programming-resistor library and error-budget audit

Status: first-author source audit, 2026-09-17; [native library rendering passed at 9e71bb5](../../../docs/development/precision-resistor-review-9e71bb5.md). No charger placement or procurement approval.

[ADR 0012](../../../docs/decisions/0012-programming-resistor-error-budget.md) selects Panasonic `ERA2AEB3651X` (3.65 kohm base ILIM), `ERA2AEB3481X` (3.48 kohm boost) and `ERA2AEB1131X` (1.13 kohm ISET). Manufacturer exact-part pages are linked there. Each is a 0402, 0.1%, 25 ppm/K resistor. Symbols use two passive pins, 1 and 2; the resistor is nonpolar. Exact identity, manufacturer, source link and footprint are controlled separately from the displayed circuit value.

## Land and package comparison

The [ERA-A datasheet](https://industrial.panasonic.com/cdbs/www-data/pdf/RDM0000/AOA0000C307.pdf), dated 24-Apr-2024, supplies the ERA2A body dimensions. The [Panasonic recommended lands](https://industrial.panasonic.com/cdbs/www-data/pdf/RDM0000/DMM0000COL17.pdf), dated 24-Dec-2025, explicitly cover ERA as well as ERJ rectangular parts.

| Feature | Source constraint | Project-local ERA2 footprint |
|---|---|---|
| Body L × W | 1.00 ±0.10 × 0.50 +0.10/−0.05 mm | 1.00 × 0.50 mm F.Fab rectangle |
| Land gap | 0.50–0.60 mm | 0.50 mm |
| Outside land span | 1.40–1.60 mm | 1.50 mm |
| Land width | 0.40–0.60 mm | 0.50 mm |
| Pads | Nonpolar two-terminal resistor | 0.50 × 0.50 mm, centers x = ±0.50 mm; F.Cu/F.Paste/F.Mask |
| Courtyard | Project clearance rule | 2.00 × 1.10 mm; 0.25 mm beyond maximum 0.60 mm body width and outer pad ends |

`R_Panasonic_ERA2_0402` deliberately has its own identity and wider courtyard than the ERJ2 template. There is no manufacturer polarity mark to invent. Rotation does not change the resistor's electrical function. No custom paste reduction or solder-mask override is introduced.

## Conditional current-budget calculation

Initial resistance is specified at 20°C. A maximum displacement of 65 K covers the assumed −40..85°C resistor-body range. Initial tolerance, temperature and the **project-allocated** additional ±0.5% assembly/service drift multiply, yielding resistance factors 0.992389741875–1.007639758125. These lie within the retained ±1% total design envelope; the current ceilings therefore remain unchanged. See ADR 0012 for the equations and limits.

The drift allocation is not a manufacturer lifetime guarantee. Qualification must establish the intended assembly/environment/service conditions. Resistor power and local body temperature must be checked using actual ILIM/ISET operating voltages; catalog wattage alone does not establish those conditions. Boost-switch leakage, auxiliary loads and startup behavior remain separate open items.

## Source identity and verification

| Inspected source | SHA-256 |
|---|---|
| ERA-A datasheet | `2ffb715174964a986d8cd22f38607a14465c938bb5ff9817e0948124ebb69a5b` |
| Recommended lands | `fc707b230cce91d464bc3aaf1ed614fa5b412f40cbe7df7cab1541d2c164a882` |

`check-programming-resistors.py` checks the exact symbols, complete footprint geometry and conditional error allocation. Fault tests reject altered source identity, pins, pad dimensions, a reduced courtyard and an excessive error allocation. Wrapper tests require every new symbol and footprint view. These are host/source checks; CLI-stub results are not native KiCad evidence. The next owner-generated bundle must show 45 symbols and 26 footprints per raw view, with the existing 443-item / 1,636-pin circuit and zero ERC violations unchanged.

Host validation on 2026-09-17: all 138 repository tests passed, including five new precision-budget/library tests and the missing-export wrapper cases. `git diff --check` passed. Rechecking the owner's unchanged 2bb0e08 circuit XML/ERC still passes 443 items / 1,636 pins and zero violations. The strict `check-power-design.py --require-usb-closure` gate returned 1 for the recorded unfinished power design. Native exports of the new libraries remain pending.

Native follow-up on 2026-09-18: the owner bundle at 9e71bb5 passed the expected export counts, zero-violation ERC, unchanged complete XML and visual review of all new resistor views. See the linked evidence record. Earlier pending statements above describe the pre-native checkpoint.
