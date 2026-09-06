<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0007: Populate the coupon with two final-product LED candidates

- Status: Accepted
- Date: 2026-09-06

## Context

Coupon Rev A reserves eight columns for a 1010 RGB LED and eight columns for a larger 1515-class RGB LED. Two useful experiments were considered: use clear LEDs from one manufacturer to isolate package size, or populate the most promising final-product candidates even though their package, lens and manufacturer also differ.

The coupon is intended to reduce final-product risk, so a direct comparison of realistic finalists is more valuable than a controlled package-size experiment.

## Decision

- Populate columns 0–7 with Everlight `EAST10105RGBA0`: 1.0 × 1.0 mm, clear lens, common anode.
- Populate columns 8–15 with QT Brightek `QBLP1515A-RGB2A`: 1.55 × 1.50 mm, white diffused lens, common anode.
- Keep both halves at the same 1.95 mm pixel pitch.
- Treat both manufacturer part numbers as exact. A supplier may not substitute an LED manufacturer, package, pinout or optical bin without a written design change and review.
- First characterize both halves under matched raw electrical conditions. Separately characterize each part at its usable white balance, diffuser stack and fixed brightness so the end-product trade-off is visible.
- Select one LED for the full badge only after Gate B compares efficacy, contrast, uniformity, colour balance, viewing angle, camera banding, solder yield, routing margin and the measured runtime impact.

## Consequences

- The experiment intentionally compares two complete optical/package systems; it does not isolate package size as the only variable.
- Results are more directly applicable to the final badge than a same-vendor clear-lens comparison.
- Project-local footprints, pad numbering, polarity marks, tape orientation, reflow requirements and controlled optical bins still require verification before coupon release.
- Everlight `EAST1616RGBA3` remains a documented fallback candidate but is not populated on Coupon Rev A.
