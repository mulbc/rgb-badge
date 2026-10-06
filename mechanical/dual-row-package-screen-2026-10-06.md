<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Conditional dual-row package XY screen

The [to-scale rear plan](review/dual-row-package-plan.svg) and [machine-readable positions](review/fit-trial.json) test the geometry consequence of [proposed ADR 0020](../docs/decisions/0020-dual-row-mosfet-package-proposal.md). Regenerate both with `python3 tools/screen-final-fit-trial.py`. This is an **unrouted package-area screen**, not a new schematic, footprint, selected battery termination or qualified PCB fit.

The starting point is the [connector-first trial](connector-first-trial-2026-10-06.md): 106 × 32.5 mm board, centred 56 × 30.5 mm LP503055 projected body, illustrative 8 × 8 mm Molex connector pocket, relocated switch and decoder, three projected driver bodies and 77 conditional 0402 positions below a separately supported pack. This screen removes only the **32 original row MOSFET courtyards** from that trial and reserves sixteen **3 × 3 mm candidate courtyards** for `DMC1229UFDB-7` complementary N/P pairs, read from the [first-author project footprint](../hardware/coupon/rev-a/dual-row-package-library-audit.md). It retains every other captured coupon part and adds the body/courtyard minima already recorded for one BQ24074, one TPS63020, two TPS259474 and one optional INA232. These minima are **not complete power circuits**.

| XY screening result | Count or area |
|---|---:|
| Original separate row MOSFET courtyards | 32; 397.6 mm² |
| Hypothetical dual-package allowances | 16; 144.0 mm² |
| Nominal row-stage courtyard area recovered | 253.6 mm² |
| Retained captured non-row parts without an XY position | 0 |
| Proposed power-IC package minima without an XY position | 0 of 5 |
| Conditional under-pack 0402 trial positions | 77 |

All drawn XY boxes are nonoverlapping, sometimes with **zero added gap**. The candidate land geometry was transcribed from the manufacturer Type B package file, but its pin numbering, paste/mask, mounting and actual routing have not passed independent review. The proposal also omits the charger/protector/converter passives and inductors, gauge buffering, hardware display interlock, two extra driver support networks, USB/RF and battery cable routes, thermal copper, assembly access and full 11 mm section tolerances. The LP503055 is still an unselected terminated-pack candidate; its cell/body drawing does not settle protection, connector polarity or wire bend. None of those omissions can be inferred to fit from this drawing.

**Disposition:** the pair package is a credible way to free plan-view area, so preserve this screen for electrical and Gate A review. Its area benefit alone does not authorize a row-stage substitution or justify full-board routing. Independently check the candidate pin/land geometry and bound final-row current and compact-board heat, then decide whether the coupon should carry the new row stage. Continue the complete coupon power circuit and exact-pack search in parallel. The manufacturer's [dual MOSFET datasheet](https://www.diodes.com/datasheet/download/DMC1229UFDB.pdf) supplies package and electrical screening values; the 3 × 3 mm courtyard is a project placement allowance.
