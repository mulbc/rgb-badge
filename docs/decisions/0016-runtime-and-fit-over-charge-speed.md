<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0016: Prioritize runtime and fit over charging speed

- Status: Accepted by owner; exact-pack selection and validation pending
- Date: 2026-09-27
- Supersedes: numeric 80%/full-charge targets in CHG-001 and the project plan
- Retains: Type-C source policy (ADR 0013), pack current limit (CHG-002), hardware NTC and safety timer (CHG-003), physical and weight limits, Gate A

## Context

The provisional 48 × 16 badge energy model needs roughly 859 mAh nominal for six hours at 0.45 W average, 3.7 V nominal and 85% usable capacity. A nominal 900 mAh pack yields about 6.29 h in that calculation, with only 0.29 h margin before measured variation. The trial pack space is no wider than 32.0 mm and no thicker than 6.1 mm **for the entire terminated pack**; neither dimension is a validated production drawing.

The currently listed LiPol `LP452845` pack has nominal 900 mAh, protection and two wires but **no NTC**. Its manufacturer lists a 450 mA maximum charging current and offers customization; an exact orderable three-wire NTC version with a complete assembly drawing has not been documented. At 450 mA, the ideal constant-current lower bound for charging 80% of 900 mAh is 96 min, before taper, thermal effects and input loads. The previous 45–60 min target cannot be applied to that candidate safely. Its stated 900 mA maximum discharge is not explicitly a continuous rating; the provisional full-white case requires about 0.83 A at 3.0 V before transient margin. Evidence: [pack shortlist](../sourcing/pack-shortlist-2026-09-27.md) and [manufacturer listing](https://www.lipobattery.us/900mah-lipo-battery-lp452845-3-7v-900mah-3-33wh-with-protection-circuit-and-wires-50mm-and-jst-phr-2/).

## Decision

Select for the badge's approximately six-hour reference workload and its 110 × 35 × 11 mm / <100 g finished constraints first. A slower **pack-rated** USB-C charge is acceptable. Remove the old 45–60 min to 80% and 75–100 min to full acceptance numbers. Before Gate A, define new *pack-specific planning times* using an exact manufacturer pack drawing and charging profile, the actual ISET maximum, and modeled input/thermal limits. Measure 80% and full charge times on the coupon and final board at a stated ambient with display OFF and a qualified Type-C source. Publish real observed times rather than implying fast charge from the ISET calculation.

Pursue a protected ~900 mAh, three-wire 10k-NTC thin pack based on the `LP452845` family **only as a manufacturer inquiry**. A bare-cell size or two-wire listing is insufficient. Obtain a separately identified orderable assembly, revision-controlled drawing, maximum finished width/thickness including PCM and lead exit, charge and continuous/peak discharge ratings, NTC curve and connector/polarity, protection standby current, compliance evidence, availability and pricing. If this assembly cannot satisfy fit, discharge margin and safety limits, screen a different pack or revisit runtime/geometry with the owner before choosing a BOM part. A qualified smaller GlobTek pack may be used on the development coupon only with its own reviewed charger configuration.

## Consequences

No battery, ISET resistor, charger connector or PCB is selected or released by this decision. The 1.13 kΩ ISET draft can reach approximately 0.872 A in the existing error budget and **must not** be used with a 450 mA-rated pack. Never rely on thermal foldback or the input limit to mask an excessive programmed charging current. Record separate coupon and final assembly population if their batteries differ. The existing switch, source permission, NTC, timer, thermal and Gate A checks still apply.
