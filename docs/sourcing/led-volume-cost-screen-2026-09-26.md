<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# LED count, traceable sourcing and project budget screen

2026-09-26. These are **representative listed prices**, not quotations or reservations. No purchase or choice of the final LED is approved. The 16 × 16 coupon compares two exact MPNs in equal halves; Gate B selects one for the five 48 × 16 final boards. Three coupon boards are intended to be assembled. The stated **USD 500–800 project target** includes coupon, five full PCBAs, cells, test tools and shipping; it excludes independent engineering review and case filament/design.

## Count before spares and assembly loss

| Quantity | Everlight `EAST10105RGBA0` | QT Brightek `QBLP1515A-RGB2A` | Combined |
|---|---:|---:|---:|
| Three assembled coupons, each 128 + 128 | 384 | 384 | 768 |
| Five 768-pixel finals if Everlight wins | 3,840 | 0 | 3,840 |
| Five 768-pixel finals if QT Brightek wins | 0 | 3,840 | 3,840 |
| **Total with Everlight final** | **4,224** | **384** | **4,608** |
| **Total with QT Brightek final** | **384** | **4,224** | **4,608** |

The totals exclude coupon-board extras (two unassembled spares), placement loss, rework and a supplier's accepted tape/reel minimum. They do not imply that either part's optical bins can be mixed freely.

## Traceable listing snapshot, September 26

| Exact part/channel | Listed stock | Representative USD tiers | Procurement consequence |
|---|---:|---|---|
| [Everlight at DigiKey](https://www.digikey.com/en/products/detail/everlight-electronics-co-ltd/EAST10105RGBA0/8510358) | 21,337 | Cut tape 100: **$0.31390**; 1,000: $0.24261; tape/reel 4,000: **$0.21490** ($859.60 total) | Four thousand may be bought as a full reel; cut tape and spares require the assembler to confirm acceptable carrier and feeders. |
| [QT Brightek at DigiKey](https://www.digikey.com/en/products/detail/qt-brightek-qtb/QBLP1515A-RGB2A/29450018) | 3,490 | Cut tape 100: **$0.25730**; 1,000: **$0.19670**; tape/reel 3,500: **$0.17504** ($612.64 total) | Current stock is **10 below a 3,500-piece reel** and **734 below** the 4,224-piece final-plus-coupon quantity if this part wins. The listed manufacturer standard lead time is 8 weeks, which is not a supplier delivery promise. |
| [Everlight at LCSC, C5681957](https://www.lcsc.com/product-detail/C5681957.html) | Stale crawler view reports out of stock; **current stock not verified** | A cached 1,000-piece reference price of $0.0664; **not an executable quote** | Investigate live lot traceability, stock and JLC/assembler acceptance at quote time. This cached listing cannot close the budget or justify an order. |

No current traceable LCSC/JLC listing for the exact QT Brightek MPN was established by this screen. Alibaba factory or authorized-distributor quotations may change the economics, but a low generic 1010/1515 RGB listing is not an exact-part alternative; require MPN, manufacturer, bin/lot traceability, tape orientation, invoice and assembly-acceptance evidence. AliExpress listings are not evidence for critical ICs or exact LED bin availability.

## Price illustrations, not optimized purchasing carts

- **Everlight final:** one 4,000-piece Everlight reel at $859.60, plus 224 cut-tape Everlight at the listed 100-piece tier ($70.31), plus 384 cut-tape QT at its 100-piece tier ($98.80): **approximately $1,028.72 for LEDs only**. Multiple cut-tape/reeling fees, freight, tax, tariffs and spares are additional.
- **QT Brightek final:** 4,224 cut-tape QT at its listed 1,000-piece tier ($830.86), plus 384 cut-tape Everlight at its 100-piece tier ($120.54): **approximately $951.40 for LEDs only**, *hypothetical because 3,490 QT parts on the listing cannot fulfill 4,224 immediately*. A factory order or replenishment could enable different reel pricing. This assumes the stated volume tier applies across a single order and is not an assembler quote.
- Even a **full-badge-only** QT purchase would be 3,840 × $0.19670 ≈ **$755.33** at the listed cut-tape tier before a single PCB, any other component, battery, shipping or coupon LED. Immediate listed stock would still be short 350.

At these **specific DigiKey retail tiers**, the USD 500–800 all-in target does not close. This is a sourcing and scale finding, not a reason to change the pixel count, pitch, exact coupon comparison or the user's six-hour target. Do not promise that LCSC/Alibaba will meet the budget without a traceable quote. Keep the LED selection contingent on Gate B optical, electrical and assembly data; obtain identical frozen-BOM PCBA quotations for three coupons then five finals. Compare supplier-supplied exact-MPN tape and consigned exact-MPN parts separately, and include loss allowance, optical bin policy and shipping. If all quotations exceed the target, bring a **concrete** budget/quantity trade-off to the owner before authorizing production.
