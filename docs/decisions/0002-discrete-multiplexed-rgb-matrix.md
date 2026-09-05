<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0002: Discrete multiplexed RGB matrix

- Status: Accepted
- Date: 2026-09-05

## Context

Tiny addressable RGB LEDs simplify routing but their per-pixel controller current is incompatible with the six-hour target. A representative SK6805-class part specifies approximately 0.5 mA static current per pixel, or 384 mA for 768 pixels before producing light.

## Decision

Use discrete four-pad common-anode RGB LEDs with 1:16 row multiplexing. Three TLC59581 constant-current devices provide 144 colour-column sinks. Sixteen P-channel high-side switches use source-referenced gate pull-ups and N-channel level-shift pull-downs driven by an active-high decoder with global inhibit.

Initial peak-current and timing values are provisional and must be selected from coupon measurements.

## Consequences

- The design adds matrix timing and row-switch complexity.
- Hardware current references bound output current independently of application brightness settings.
- Fine-pitch LED routing and assembly must be proven on the coupon.
