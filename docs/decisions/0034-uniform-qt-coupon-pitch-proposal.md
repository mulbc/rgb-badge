<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0034: Uniform 1515 coupon pitch for routable matrix

- Date: 2026-10-16
- Status: Accepted by owner 2026-10-18
- Scope: 16 × 16 validation coupon only; no final 48 × 16 pitch change is approved

## Context

DSP-002 requires a coupon/final pixel pitch no greater than 1.95 mm. DSP-007 puts both LED finalists at exactly 1.95 mm on the coupon, and DSP-008/ADR 0008 rotate the `QBLP1515A-RGB2A` half in a 0°/90° checkerboard to preserve its exact 0.60 × 0.40 mm manufacturer lands. This is valuable for an equal-pitch optical comparison and final-badge dimensional relevance.

The [114 mm checkerboard routing trial](../development/led-1515-row-red-hdi-screen-2026-10-16.md) joins all anode rows and 1010 RGB trunks, plus the 1515 red trunks. It still has 774 open KiCad connectivity edges. Simply stacking blue pad vias and joining straight blue trunks produces 92 shorts with the sloping red trunks. Reversing red/blue layer order leaves 65 new geometric findings. These source probes do not prove a more sophisticated 1.95 mm route impossible, but it has not yielded a complete route quickly.

A separate [2.2 mm horizontal-pitch, 1.95 mm vertical-pitch 1515 study](../development/led-qt-uniform-2p2-matrix-study-2026-10-16.md) holds the 1010 half at 1.95 mm and gives every 1515 LED the same 0° orientation. It preserves the exact manufacturer pad shapes. The 1515 block grows by **1.75 mm** across its eight columns, within the current 114 mm working PCB outline. Native KiCad DRC has no added geometry finding beyond 104 intrinsic fine-pitch pad-gap findings, and the fully joined LED matrix has 534 open edges elsewhere on the board. This is routing geometry, not board, process or optical qualification.

## Decision

For the coupon only, change the `QBLP1515A-RGB2A` half to 2.2 mm **horizontal** pitch, retain 1.95 mm vertical pitch, use uniform 0° orientation, and retain the manufacturer's pad geometry. Keep the `EAST10105RGBA0` half at 1.95 mm in both axes. This supersedes ADR 0008's checkerboard decision for the coupon. The final 48 × 16 badge remains limited to 1.95 mm pitch; its package and routing require a separate design decision.

## Consequences and review gates

The two coupon halves would no longer provide a same-pitch optical comparison. The trial would validate electronics and assembly at different horizontal spacings, and would not establish that the 1515 package meets the final 1.95 mm pixel-pitch target. Revisit optical test interpretation and final-package choice. Check the resulting 1515 optical field, diffuser/case openings, RF/battery/USB fit, assembler land/mask/paste rules, HDI stack-up/via fill and all driver/power connections. Independent Gate A still precedes fabrication.

The owner accepted this coupon-only geometry tradeoff on 2026-10-18. The routed KiCad boards remain engineering studies until their footprints, nets, process and enclosure are reconciled with the canonical schematic and reviewed; accepting pitch alone does not select the candidate onsemi row-pair device or release fabrication.
