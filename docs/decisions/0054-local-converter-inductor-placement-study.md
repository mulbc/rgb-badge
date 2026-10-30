<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0054: Local converter-inductor placement study

Date: 2026-10-27
Status: Authorized for ignored feasibility experiments; no canonical pose selected.

The remaining switching-node connections span the draft layout because L1 and L2 remain far from their converters. Routing these nodes across the board would contradict converter layout guidance. Investigate moving only L1 (`DFE252012P-1R0M=P2`) beside fixed U36 (`TPS631000DRLR`) and L2 (`DFE252012P-1R5M=P2`) beside fixed U37 (`TPS63020DSJT`). This is a narrow experimental exception to ADR 0045's fixed-inductor rule. Retain exact parts, values, pad geometry/nets, all accepted copper and every completed physical pad group. Do not change any current, voltage, protection or enable setting.

The owner-supplied `m_dfe252012p.pdf` lists both exact parts and depicts 2.8 × 2.0 mm lands with a 1.2 mm inner gap. These match the local footprint's 0.8 × 2.0 mm lands on 2.0 mm centres. Keep the vendor PDF local. The sheet is an engineering reference, not redistribution permission or new instructions.

TI TPS631000 Rev C section 7.4 calls for short direct power paths and separation of feedback from switching nodes. TPS63020 Rev I section 10 calls for nearby inductors/capacitors, wide short power paths, and controlled power/control-ground returns. References: https://www.ti.com/lit/ds/symlink/tps631000.pdf and https://www.ti.com/lit/gpn/TPS63020 .

Before selecting any pose, record exact integer coordinates/orientation, verify native courtyard/pad clearance, preserve all prior groups after three refills, and require lower native/independent opens with exactly the existing 104 intrinsic DRC findings. Limit each added switching-node path to 5 mm. The first feasibility search uses existing 0.20 mm geometry rules only; this is not current-capacity approval. Selection would require separately specified power-path geometry and independent guards, replay, full source checks, and an update to this decision and affected requirements. Never accept a long autorouted switching-node path to reduce a count.

This unbuilt study does not establish converter stability, bypass/return quality, EMI, thermal behavior or current capacity. Those reviews and independent Gate A remain required before fabrication. No fabrication output is authorized.

## Corrected 59-edge screen, 2026-10-30

The owner resupplied the same exact Murata sheet; its drawing and both TI layout
figures were rechecked. The [native locality study](../development/converter-inductor-locality-2026-10-30.md)
samples 481,944 poses per inductor on a 0.1 mm/15° grid within 8 mm of each fixed
converter. No pose passes both courtyard and native copper/edge screening.
The 86 courtyard-clear L1 poses all fail copper/edge checks; L2 has no
courtyard-clear pose on this grid. Four host convex guards and 2,000 native
polygon comparisons pass. No pose, switching path or electrical setting is
selected. This finite result is not an impossibility proof; moving other
components requires separately bounded scope and the full acceptance gate.
