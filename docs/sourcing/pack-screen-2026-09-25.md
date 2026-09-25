<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Single-cell pack screening, 2026-09-25

These are documented **candidates**, not approved pack MPNs, a purchase list or permission to fabricate. Compare the terminated pack, not just the bare cell. Both 800 mAh and 700 mAh nominal alternatives illustrate why the current charge setting cannot be frozen ahead of pack selection. The owner prefers a US distributor for development batteries; DigiKey is a potential channel, but domestic stocking does not mean a cell was manufactured in the US.

| Exact terminated pack | Documented properties | Disposition |
|---|---|---|
| GlobTek `BL0750F5030481S1PCTC` | Manufacturer drawing Rev D: nominal **700 mAh** despite `0750` in the ordering code; protected 1S pouch, 10k NTC, three-wire Molex 51021-0300, 50.5 × 30.5 × 5.3 mm, approximately 22 g. Maximum charge **1C = 700 mA**, continuous discharge 1C = 700 mA. Manufacturer drawing has an internal part-number inconsistency on page 2 (`BL0700...`), and does not establish the NTC B value in the reviewed electrical table. | Good dimensional and documented US distributor candidate for a **revised charge-current setting**, subject to manufacturer confirmation of the exact drawing, NTC curve, protection circuit, discharge peaks and connector polarity. Draft charge ceiling 872 mA exceeds pack maximum by **172 mA**. |
| GlobTek `BL0800F5424651S1PSXH` | Manufacturer drawing Rev F1: 800 mAh, protected, 10k NTC with B = 3950 K and integrated BQ27542 fuel gauge, 24 × 71 × 6 mm, approximately 30 g. Maximum charge **0.5C = 400 mA**; continuous discharge 1.4 A. Five-wire Molex 51021-0500 exposes pack I²C. | Fits bounding box, but duplicates the planned on-board MAX17048, adds a five-pin battery interface and requires charger limit ≤400 mA. At 30 g it leaves 45 g for all other items under the 75 g stretch goal. Do not substitute it into the draft. |
| LiPol `LP402480` configured with PCM/NTC/Molex 78172-0003 | Manufacturer page: 800 mAh; cell 4 × 24 × 80 mm, pack listed 16 g; protected, NTC, maximum charge 400 mA and discharge 800 mA. Stock is quote-dependent, and the 4 × 24 × 80 mm specification is described as **cell** size, not a verified maximum terminated-pack envelope. | May help later if measured mass dominates, but charging limit and connector require revisions; pack dimensions, NTC curve, current peaks and US supply have not been established. |

## Calculation and implications

The existing BQ24074 ISET network has a calculated **0.698–0.872 A** charge-current range under the repo's retained programming-error assumptions. The 700 mAh GlobTek part is rated at no more than 0.700 A; the other two packs at no more than 0.400 A. Normal temperature regulation or input current limiting is not a valid substitute for setting a safe maximum charge current. Select the exact pack and protection/NTC evidence before choosing the final ISET resistor or claiming the 45–60-minute 80% goal.

Energy-only upper bounds at nominal capacity are **2.59 Wh / 6 h ≈ 432 mW** for the 700 mAh pack and **2.96 Wh / 6 h ≈ 493 mW** for an 800 mAh pack. These are gross power ceilings before converter losses, usable-depth limits, pack aging and any case/LED measurements. Neither number establishes six-hour runtime. The preliminary layout must include actual wrap and lead exit, mounting, swelling clearance and the three-pin keyed plug; nominal pouch dimensions alone are not a mechanical fit sign-off.

As of this screening, DigiKey displayed 1,640 units of `BL0750F5030481S1PCTC` at $11.85 for one and an 18-week manufacturer standard lead time. Stock/price are snapshots, not reservations. Do not order now; an exact pack, revised charger setting and Gate A must precede the PCB release. The battery for an **isolated development test** can be chosen separately if its charger settings are explicitly compatible.

## Evidence

- [GlobTek 700 mAh drawing Rev D](https://www.globtek.com/pdf/manual-datasheets/BL0750F5030481S1PCTC.pdf), pages 3 and 5, and [DigiKey listing](https://www.digikey.com/en/products/detail/globtek-inc/BL0750F5030481S1PCTC/16515787), inspected 2026-09-25.
- [GlobTek 800 mAh drawing Rev F1](https://www.globtek.com/pdf/manual-datasheets/BL0800F5424651S1PSXH.pdf), pages 3–4, and [DigiKey listing](https://www.digikey.com/en/products/detail/globtek-inc/BL0800F5424651S1PSXH/14318830), inspected 2026-09-25.
- [LiPol 800 mAh manufacturer page](https://www.lipobattery.us/un38-3-iec62133-msds-certified-lipo-battery-lp402480-800mah-3-7v-2-96wh-with-pcm-ntc-wires-molex-78172-0003/), inspected 2026-09-25.
- [Existing BQ24074 programming analysis](../../hardware/coupon/rev-a/power-pre-capture.md); this screen does not redo its resistor/source verification.
