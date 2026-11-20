<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Uniform 1515, 2.2 mm horizontal-pitch matrix trial

This trial establishes the coupon LED geometry accepted by [ADR 0034](../decisions/0034-uniform-qt-coupon-pitch-proposal.md) and revised DSP-002/DSP-007/DSP-008. Its routes are still a **feasibility study**: the rest of the board is incomplete and it is not a schematic-synchronized fabrication source.

The [deterministic generator](../../tools/generate-qt-uniform-2p2-matrix-trial.py) starts from the separate 114 mm 1010-RGB trial, preserves all 483 footprints, and changes the 128 `QBLP1515A-RGB2A` placements to a uniform 0° orientation at **2.2 mm horizontal and 1.95 mm vertical pitch**. Its unmodified QT pad geometry remains 0.60 × 0.40 mm. It adds front-layer 1515 anode buses, red/blue pad-centred F.Cu–In1.Cu microvias and straight In1.Cu columns, green front stubs to the 1515 body centres with stacked F.Cu–In1.Cu/In1.Cu–In2.Cu microvias and In2.Cu columns, and left/right stacked transitions that join both LED families' rows on In3.Cu.

The [saved native board](../../hardware/coupon/rev-a/staging/led-qt-uniform-2p2-matrix-trial-114mm.kicad_pcb) has **2,416 tracks/vias** and **534 full KiCad open edges**, versus 1,022 before routing the 1515 half. It joins every 256 LED's row and three colour nets within the matrix; it does not connect those row/column nets to their driver devices. KiCad 10.0.6 [DRC](led-qt-uniform-2p2-matrix-drc-2026-10-16.json) reports only the same **104 pre-existing fine-pitch pad-gap findings**, with no added finding. Twice-generated board SHA-256: `5caaa613030eb55e97cb793176e9970057823637c17218760c1e8b0f1fcd9a3e`.

The trial is not a selected manufacturing process. It uses 0.30/0.10 mm provisional microvias, including via-in-pad and stacked sites. Fill/cap, paste, mask, yield, 1.0 mm six-layer stack-up and supplier capability remain unqualified. No power tracks were moved from the separate power study. Driver fanout, power/control routing, RF, cell/enclosure fit, assembly access and Gate A engineering review remain open. The changed horizontal pitch weakens the equal-pitch comparison and does not qualify a final ≤1.95 mm display.
