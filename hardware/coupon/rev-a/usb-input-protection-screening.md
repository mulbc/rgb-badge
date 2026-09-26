<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Input protection and wider-input logic supply

2026-09-19. [ADR 0014](../../../docs/decisions/0014-usb-voltage-envelope-and-logic-ldo.md). No input bridge or fabrication release.

## U29 library/capture audit

Exact `TPS70933DBVR`, [TI SBVS186H](https://www.ti.com/lit/ds/symlink/tps709.pdf), SHA-256 `8c14e3efae738a27b857b789aa87369de9037a8ef3616a9f71a423587cdc6949`. Visually inspected pin table on PDF page 3 and DBV drawings on pages 33–35 (4214839/K, 08/2024).

| Pad | Function | Capture |
|---|---|---|
| 1 | IN | +5V_USB, still staged |
| 2 | GND | GND |
| 3 | EN | Intentional open, internal enable |
| 4 | NC | No-connect |
| 5 | OUT | +3V3_USB |

DBV lands match the existing pattern: 1.1 × 0.6 mm, row centres ±1.3 mm, 0.95 mm pin pitch, 0.05 mm corner radius. No footprint changes. Symbol geometry retains existing U29 heading spacing. Native U29 review passed at bad43fa; see [evidence](../../../docs/development/input-review-bad43fa.md). TI's exact-part page lists ACTIVE; its public inventory response is ambiguous with login-required fields, so no stock quantity or purchase recommendation is recorded.

## Protection screening

Candidate only: `TPS259474ARPWR`, [TI SLVSFC9C](https://www.ti.com/lit/ds/symlink/tps25947.pdf), PDF SHA-256 `8f96de389903091650d4f462dcfad3210071c3ae7093623a7978f34baf8a65b4`. Electrical/timing tables on PDF pages 9–11 were visually inspected. This variant combines adjustable OVLO, power-good and circuit-breaker behavior; it is not the active-current-limit variant.

`tools/check-input-protection.py` enumerates reference, leakage and opposite resistor corners using KCL. Positive leakage into the pin raises the required source voltage. A nominal 37.4k/10k OVLO divider with ±1% TOTAL resistor error produces a **calculated** 5.5161–5.8932 V rising trip and 5.0168–5.3779 V recovery interval. These are screening values, not selected resistor MPNs. Recovery hysteresis can require unplugging/replugging after a fault; automatic restart at every normal source voltage is not promised.

A second, still unselected 38.3k/10k numerical example produces a **calculated 5.6204–6.0056 V rising** and **5.1117–5.4805 V falling** interval using the same threshold, ±0.1 µA leakage and ±1% total resistor-error bounds. Its minimum rising trip is about **120 mV above** normal 5.5 V, versus 16 mV for 37.4k/10k. Its largest rising trip is about **494 mV below** U34's 6.5 V recommended input maximum. Those are DC comparisons, not allowable ripple, overshoot or delay guarantees; a fast input surge could exceed U34's limit before the switch disconnects. If a future charger EN2 pull-up uses the protected input, the BQ24074's specified logic-high voltage range only reaches **6.0 V**; the new 6.0056 V static OVLO corner already exceeds that by about 5.6 mV before any disconnection delay. EN2's exact drive arrangement therefore needs separate review. Returning to a steady 5.0 V after an overvoltage event is below the lowest calculated falling trip for either example. Neither example selects resistor MPNs, validates combined manufacturing drift or changes the schematic.

A narrow divider chosen around the old 5.25 V assumption trips below the newly established 5.5 V normal upper boundary, so it is rejected. Merely replacing the old upper number in a comment cannot close this issue.

PG can replace a separate VBUS detector only after checking its threshold, low level and timing against the receiving circuit. OVLO and PG delays are typical values in the reviewed table, not guaranteed worst-case limits. Static trip success must not be presented as a bound on surge overshoot. The optional `--require-closure` command therefore still fails.

Before capture: qualify exact divider parts, PG thresholds and loading, overcurrent/inrush, transient containment and physical charger inhibition. The existing charger current ceiling remains controlling; an eFuse circuit breaker is not a replacement for source-qualified charger current limiting. Whole-port consumption remains unclosed.

## Other actuator candidate screened

`DMN2056U-7` was inspected from the [manufacturer PDF](https://www.diodes.com/assets/Datasheets/DMN2056U.pdf), DS38480 Rev. 2-2. Its 0.4 V minimum gate threshold is specified at 25 C. Do not equate that number to a guaranteed OFF current at the supervisor's worst-case nonzero output voltage, or extend room-temperature limits over temperature. No symbol or circuit substitution was made for this candidate.

Host validation: all 147 tests passed on 2026-09-19, including generator equivalence, independent pin maps, the EN-to-IN fault rejection, export-wrapper tests and six new divider-screening tests. No native KiCad result is claimed for the modified source. The 12a134f bundle remains evidence for the prior circuit.

## C32 source review received

The owner supplied Murata's five-page characteristic PDF on 2026-09-19, resolving the HTTP 403 source-access blocker. See [C32 characteristic review](c32-characteristic-review.md) for the file hash, page-by-page evidence, approximate curve readings and limits. Retain C32 provisionally; no capacitor or schematic change is required by this screening. Combined-condition capacitance, aging and actual regulator stability remain Gate A/coupon qualification items. No further owner document request or native rerun is needed for this evidence-only update.

## Candidate libraries and follow-on screening

The 2026-09-20 [shared package audit](input-protection-library-audit.md) adds unplaced TPS259472ARPWR/TPS259474ARPWR candidates, including their distinct copper/stencil geometry. The screening tool now reports PGTH leakage corners, PG startup-level limitations, fixed-clamp headroom and an ILM threshold counterexample. Neither candidate is selected; no protected-input bridge is captured.

## Charger-path gating alternative

The [2026-09-24 assessment](charger-input-gating-assessment.md) evaluates using the input switch itself for charge permission, with upstream USB logic. It also records the TPS259472 recommended-input/clamp limitation; the earlier static downstream headroom calculation alone does not establish normal 5.5 V operation. This alternative is not selected or captured.
