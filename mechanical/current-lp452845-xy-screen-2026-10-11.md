<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Current LP452845 rear-courtyard XY screen, 2026-10-11

The [deterministic screen](../tools/screen-current-lp452845-xy.py) reads the current KiCad 10.0.6 XML (SHA-256 `d5e9040209f4a4719500a2c35e432013ace3f7b863a3630429d1d9051a1cb9c4`) and project-local footprint courtyards. Its [full result](review/current-lp452845-xy.json) and [dual-package view](review/current-lp452845-dual-xy.svg) replace the old inventory assumption with the current 466-item coupon circuit. They are **geometric stress screens, not a KiCad PCB or a fit approval**.

The screen uses the 106 × 32.5 mm trial final board, the selected LP452845 maximum 47 × 28.5 mm body at the October 9 position, the exact J2 9.2 × 10.2 mm courtyard, the existing MCU/USB/switch/decoder guides and three projected final-driver bodies. It reserves 10 × 8 mm at the battery center for sensing. Each freely packed component box has 0.5 mm added to its footprint width and height. Only 108 small 0402/NTC candidates may occupy the battery body's XY area; this is conditional on insulation, height and actual thermal coupling. The sensor components are counted but **not forced into the sensor reservation**, so the trial does not satisfy sensing placement.

| Row-stage boxes and greedy order | Captured/candidate boxes left without XY position |
|---|---:|
| Canonical 32 separate Q1–Q32; largest first | 18, including 13 N-MOS row parts, L1/L2, U35 and E0/E1 |
| Canonical 32 separate Q1–Q32; row parts first | 16, including VLED/gauge/charger and USB permission parts |
| Sixteen unapproved `DMC1229UFDB-7` dual-package boxes; largest first | 0 |
| Same dual-package boxes; row parts first | 0 |

The canonical failures are **first-fit failures, not a proof of no possible placement**. The zero-unplaced result for the dual-package *geometry* is evidence that [ADR 0020](../docs/decisions/0020-dual-row-mosfet-package-proposal.md) is worth a focused electrical and layout audit. However, reserving an empty 10 × 10 mm interlock pocket left of the pack makes even that variant leave **four** current packages unplaced in both orders. A 7 × 12 mm pocket beside the decoder leaves **one or two**. These are reservation sensitivities, not a required interlock shape or a no-fit proof; they show that the apparent zero-unplaced result has no demonstrated interlock margin. The [first electrical screen](../docs/design/dual-row-electrical-screen-2026-10-11.md) narrows but does not close the row-package decision.

The dual package is not approved for substitution: row-current/thermal limits, exact pin orientation, gate drive, assembly, actual row locality, routing channels and switching copper are unverified. The SVG's dense perimeter packing illustrates why a courtyard-only result must not be treated as a route or DRC result. The actual hardware display interlock, RF cable, mounting, pack wire bend/PCM protrusion, swelling, case tolerance and final sensor stack are still absent. A final board must be placed and routed in KiCad, then pass DRC, mechanical section review and independent Gate A before fabrication.

As a quick simplification check, retaining eight trial-access pads and omitting fourteen coupon-only pads from the *screen* did **not** change the 7 × 12 mm interlock-pocket result: one or two larger ICs still lacked positions. Coupon test pads remain in the canonical circuit. A real final-board manufacturing test plan may choose a smaller pad set, but pad omission alone is not a demonstrated solution to the present component-space constraint.
