<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Coupon Rev A row-selection library audit

Status: exact-part KiCad libraries authored; native KiCad rendering and independent Gate A review pending; row circuit not yet captured

## Selected chain

| Function | Exact part | Package | Controlled source |
|---|---|---|---|
| Active-high 1-of-16 decoder | `74HC4514PW,118` | Nexperia SOT355-1 / TSSOP24 | [Nexperia datasheet](https://assets.nexperia.com/documents/data-sheet/74HC_HCT4514.pdf), rev. 6.1, 2024-08-12 |
| High-side row switch | `DMP2066LSN-7` | Diodes SC-59 | [Diodes datasheet](https://www.diodes.com/datasheet/download/DMP2066LSN.pdf), DS31467 rev. 4-2, 2011-08 |
| Gate pull-down / level shift | `2N7002K-7` | Diodes SOT23 | [Diodes datasheet](https://www.diodes.com/assets/Datasheets/2N7002K.pdf), DS30896 rev. 20-2, 2024-07 |
| P-MOSFET gate pull-up | `ERJ-2RKF1001X` | Panasonic 0402 | [Panasonic ERJ data sheet](https://industrial.panasonic.com/cdbs/www-data/pdf/RDA0000/AOA0000C304.pdf); 1 kΩ, ±1% |

The first three downloaded source files hashed as follows during transcription. A later upstream revision requires a fresh comparison, not an automatic hash update.

| File | SHA-256 |
|---|---|
| `74HC_HCT4514.pdf` | `7f86698694e793b0a7534e7c76ca3518aa80ab26033f0fed64ea37342dcf81a3` |
| `DMP2066LSN.pdf` | `e6195720f2b4b134fba5701bac41181863f237bcea199f9418f53e3dfd90af82` |
| `2N7002K.pdf` | `669e5d68d6458e0879d7396416bdcdb3ef9966ea60f054773d4c891d735aa818` |

These are candidate BOM lines, not purchasing approval. Critical semiconductor lots must remain exact and traceable through an authorized source or the selected PCBA supplier. Alibaba quotes may propose the same MPNs but may not silently substitute them. AliExpress remains development-only unless a listing is demonstrably manufacturer-authorized and traceable.

## Decoder pin audit

The project symbol follows Nexperia's physical pin table exactly:

| Pins | Signals |
|---|---|
| 1, 2, 3 | `LE`, `A0`, `A1` |
| 4–11 | `Q7`, `Q6`, `Q5`, `Q4`, `Q3`, `Q1`, `Q2`, `Q0` |
| 12 | `GND` |
| 13–20 | `Q13`, `Q12`, `Q15`, `Q14`, `Q9`, `Q8`, `Q11`, `Q10` |
| 21–24 | `A2`, `A3`, active-low `E`, `VCC` |

At `LE = HIGH`, the outputs follow the address. With `E = LOW`, exactly the selected output is high. With `E = HIGH`, all outputs are low. The planned circuit therefore names pin 23 `ROW_ENABLE_N` and pulls it up to `+3V3_APP`, making the decoder's normal un-driven state all-low. The four address inputs receive pull-downs and `LE` is tied high.

The decoder is valid at a 3.3 V supply, but its timing is not inferred from the 4.5 V headline numbers. Firmware must blank the rows, change the address, wait for measured settling/dead-time, and only then enable the next row.

## MOSFET pin and land-pattern audit

Both Diodes top views use pin 1 gate, pin 2 source and pin 3 drain. The project symbols preserve that mapping.

The SC-59 footprint copies the manufacturer's suggested `X = 0.8`, `Y = 1.0`, `C = 2.4`, `E = 1.35` and `Z = 3.4 mm` geometry: pins 1 and 2 are centred at `(−0.675, 1.2)` and `(0.675, 1.2)`, and pin 3 at `(0, −1.2)`. The SOT23 footprint uses the manufacturer's `X = 0.8`, `Y = 0.9`, `C = 2.0`, lower-pad pitch `1.35` and overall `Y1 = 2.9 mm`: pins 1 and 2 are centred at `(−0.675, 1.0)` and `(0.675, 1.0)`, and pin 3 at `(0, −1.0)`.

Nexperia publishes the SOT355-1 body/lead outline but not a recommended board land pattern in the decoder datasheet. The project footprint therefore uses a documented IPC-derived gull-wing pattern: 1.475 × 0.4 mm pads, row centres at ±2.8625 mm, and 0.65 mm pitch. It fits the 4.3–4.5 × 7.7–7.9 mm manufacturer body envelope and requires assembler DFM plus independent Gate A comparison before fabrication.

## Planned row circuit and limits

Each active-high decoder output will drive a `2N7002K-7` gate. That N-MOSFET pulls one `DMP2066LSN-7` P-MOSFET gate low; the P-MOSFET then connects VLED to one common-anode row. A 1 kΩ source-to-gate pull-up turns the P-MOSFET off, and a 100 kΩ N-MOSFET gate pull-down prevents a floating decoder output from turning it on.

At a provisional 3.9 V VLED, the selected channel draws about 3.9 mA through the 1 kΩ gate pull-up and dissipates about 15.2 mW in that resistor. Only one row may be selected. The DMP2066LSN is specified at −2.5 V and −4.5 V gate drive and has 10.1 nC typical total gate charge under its stated test conditions. The coupon must measure turn-on, turn-off, overlap and visible ghosting.

The 2N7002K only guarantees `RDS(on)` at 5 V and 10 V gate drive. Its proposed 3.3 V use sinks only the approximately 3.9 mA pull-up current, but that conclusion is not a manufacturer guarantee. Gate A must either accept this bounded use or select a replacement with explicit low-voltage drive limits; Gate B must measure the actual drain voltage and switching edges across temperature-representative conditions.

The decoder pull-up is not, by itself, a complete startup interlock. Rail ramps and unpowered logic can be indeterminate. The later power sheet must keep VLED disabled in hardware until the controller deliberately enables the display. Passing this library check says nothing about that uncaptured safety path.

## Automated and visual checks

`python3 tools/check-row-libraries.py` independently checks the exact MPN properties, all 32 symbol pins, three pad maps, pad positions/sizes/layers and pin-1 markers. `tools/check-kicad.sh` additionally asks KiCad 10 to load and render every new symbol and footprint. Neither test is simulation, DRC, assembler DFM, measurement or independent review.

For the native review, verify:

- the decoder shows four address inputs, `LE`, an inverted `E`, both supply pins, and sixteen separately numbered outputs;
- each MOSFET symbol shows pin 1 gate, pin 2 source and pin 3 drain;
- every package has separate copper pads and a pin-1 marker by the gate pad;
- TSSOP pins 1–12 run down the left side and 13–24 run up the right side when viewed from the top;
- no text hides a pin or pad number in the fabrication view.

The next milestone captures U2, its decoupling/defaults and all sixteen row stages only after this native render passes.
