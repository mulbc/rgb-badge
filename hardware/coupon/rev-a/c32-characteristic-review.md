<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# C32 manufacturer characteristic review

2026-09-19. Applies to the TPS70933DBVR USB-only regulator introduced by ADR 0014. This is document screening, not a board measurement or fabrication release.

## Evidence

Owner-supplied `Product Details_Murata Manufacturing Co., Ltd_.pdf`, five pages, footer date 2026-09-19. SHA-256: `243fb5e15c5ba955544da0d1ec30d89c099871b0504bfa0f5e170b6769a445df`.

Manufacturer family URL printed in the PDF: https://pim.murata.com/en-us/pim/details/?partNum=GRM188R60J106ME47%23 . The uploaded PDF supplies the evidence; access to the live endpoint is not claimed. The original attachment is retained in the project conversation. Pages 4 and 5 were rendered and visually inspected, not inferred from text extraction alone.

Page 1 explicitly includes `GRM188R60J106ME47D`; the family wildcard denotes packaging. Page 3 identifies D as 4,000-piece reel packaging. Pages 2–3 confirm 0603, 1.6 by 0.8 by 0.8 mm nominal, 10 µF ±20%, 6.3 V, X5R and -55 to +85 C. The document labels the family in production at its stated date; this does not establish distributor stock.

## Approximate readings and test conditions

| Evidence | Observation | Limit of inference |
|---|---|---|
| Page 4, DC-bias curve | At 3.3–3.366 V, approximately -52% to -54% change, or roughly 4.6–4.8 µF from 10 µF | Typical curve at 25 C, AC 0.5 Vrms; readings are approximate, not guaranteed minima |
| Page 4, AC-voltage curve | Capacitance also decreases at smaller AC excitation | DC 0 V, 25 C; do not multiply this curve with the DC-bias curve as if joint behavior were established |
| Page 4, temperature curve | Modest change around room temperature, decreasing toward the hot end | DC 0 V, AC 0.5 Vrms; does not establish biased hot/cold behavior |
| Page 5, resistance curve | Approximately 0.02–0.03 ohm at 10 kHz; a few milliohms around 100 kHz–1 MHz | DC 0 V, 25 C; ESR is frequency-dependent, not guaranteed below 0.2 ohm at every frequency |

No aging rate or guaranteed combined bias/temperature/AC-amplitude characteristic is supplied. The footer explicitly describes typical specifications and directs users to detailed product specifications for ordering.

TI TPS709 SBVS186H section 8.1.1 requires 1.5–47 µF **effective** output capacitance for outputs at or above 1.5 V, and ESR 0–0.2 ohm. The previously inspected TI PDF has SHA-256 `8c14e3efae738a27b857b789aa87369de9037a8ef3616a9f71a423587cdc6949`.

For perspective only, applying the -20% nominal tolerance to the low approximate curve reading gives 4.6 × 0.8 = 3.68 µF, about 2.45 times the 1.5 µF minimum. This is a sensitivity calculation under an assumed separable tolerance, not a guaranteed lower bound: combined temperature, excitation and aging effects remain unbounded by this export. Do not present that ratio as a qualified stability margin.

## Disposition

- Close the missing-source access item and retain C32 in the draft. The curves support continued design without an immediate capacitor substitution or another owner download.
- Preserve effective-capacitance/ESR verification in Gate A and stability testing in coupon bring-up, including startup, input removal and load transitions over the intended temperature/load envelope. Establish the total output capacitance, including connected bypass capacitors, against TI's upper limit as well.
- No pin, footprint, net, BOM MPN or generator changes. Previous host-test results remain applicable; no new native KiCad run is requested for this document-only review.
- Continue protected-input and charger standby design. This review does not close those circuits or release fabrication.
