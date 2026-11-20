<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0108: Ordinary GND routing on the designated ground layer

Date: 2026-11-09
Status: Accepted for ignored routing exploration; no successor selected.

The routing search currently disables all horizontal In2.Cu movement,
including the GND net itself. Permit a GND-only search on the existing
In2.Cu ground layer, using ordinary 0.20 mm tracks and unchanged 0.20 mm
foreign-net clearance. Keep horizontal In2 routing disabled for other nets.
This changes a search restriction, not the board's profiles, zones or rules.

Start from actual retained pads/copper and target individually copper-witnessed
main-ground components. Retain every original/accepted item, pose, net,
permission/protection setting and previous live pad group. No source
retirement, narrowing or unsupported central microvia is allowed. Every
transaction must pass refill and actual native/physical group preservation.

No trial is selected without a true ground join, exact unchanged 104 native
findings, a deterministic ledger/replay, source/fault checks and visual review.
Return impedance, current/thermal, supplier stack and process/fit qualification
remain separate. The 36-open source remains selected until the complete gate
passes; independent Gate A still precedes fabrication.

The first 0.05 mm full-layer GND-plane trial still finds no join. Also screen
a bounded 0.025 mm In2-only graph with full-resolution ground-plane targets.
The previous target sampler uses a 0.20 mm stride; this can omit usable
centres in narrow filled corridors. Clip target enumeration to each actual
component's bounding box and retain exact native shape checks. These are
sampling changes only: physical track width/clearance and all acceptance
requirements remain unchanged. No global routing impossibility is inferred.

Outcome: the 0.025 mm In2-only trials exhaust 16,314 nodes for each U38/U52
source; PAIR01 has no usable endpoint. The bounded six-layer fine-grid
variant exhausts 1,007 / 43,339 / 43,339 nodes for PAIR01/U38/U52. Neither
adds copper or reduces 36 opens. These finite searches establish no global
impossibility; no source or production search-tool change is selected.
