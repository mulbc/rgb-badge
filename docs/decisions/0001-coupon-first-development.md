<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0001: Coupon-first development

- Status: Accepted
- Date: 2026-09-05

## Context

The highest risks are LED optical efficiency, fine-pitch assembly yield, multiplex timing, system power, charging behaviour and RF performance. A full 48 × 16 board would multiply cost before those risks are measured.

## Decision

Build a 16 × 16 production-intent coupon first. Populate eight columns with a qualified 1010 candidate and eight with a qualified 1515 candidate at the final 1.95 mm pitch. Include the intended controller, one TLC59581, all 16 row stages, USB-C, charger, gauges, regulators, controls and antenna. Order five coupon PCBs and three assembled units.

## Consequences

- Coupon results, not estimates, select the final LED and operating parameters.
- No off-the-shelf HUB75 panel counts as electrical validation.
- The five full badges cannot be released until Gate B acceptance evidence exists.
