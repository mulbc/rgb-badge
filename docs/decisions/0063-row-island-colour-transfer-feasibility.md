<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0063: Exact row-island colour-transfer feasibility

Date: 2026-10-29
Status: Exact 60-edge transfer selected after its complete acceptance gate.

The accepted board has 61 native/physical opens. A 0.025 mm local full-width
search from the PAIR06/07/08 ground island reaches 13,101 B.Cu cells but no
legal adjacent via or main-ground contact. Fifteen tested via sites have exactly
one original obstruction across the complete B/In4/In3/In2 ground stack:
COL_03_B, (81.70, 12.10) to (78.30, 12.10) mm, In4.Cu, width 0.20 mm.
This finite result does not establish global routing impossibility.

Permit ignored replacement of only that exact original track with retained In4
end portions and a full-width In3 dogleg using two adjacent microvias. Preserve
both original endpoints and every source-derived direct In4 contact. Bound the
transferred original interval to 2 mm, vertical displacement to 1 mm, and total
replacement length to original plus 2 mm. Keep all tracks/clearance at 0.20 mm
and adjacent microvias at 0.30/0.10 mm. This case adds no narrow pin neck.
Keep every other original and accepted copper item, component/pose, zone,
physical pad group, previous exception and electrical setting unchanged.

The unchanged TLC59581RTQT is covered by
[TI TLC59581/82 Rev. A](https://www.ti.com/lit/ds/symlink/tlc59581.pdf).
COL_03_B is a constant-current LED output; the original track width and driver
settings remain fixed. Pin maps and package geometry remain unchanged. Native
routing evidence cannot establish copper/via current capacity or thermal,
switching, return-path, process or assembly qualification.

Canonical adoption requires an exact independently enforced source/interface/
length catalog, frozen 61-edge preservation, lower native and physical counts,
unchanged full 104 findings, stable fills/replay, source/fault checks and the
unchanged original-orphan proof. Independent Gate A precedes fabrication.

## Exact selected outcome

The [60-edge study](../development/led-routing-progress-60-study-2026-10-29.md)
selects the 1 mm interval x = 80.225–81.225 mm with an In3 dogleg at y = 11.60 mm.
Its aggregate replacement is 4.4 mm versus 3.4 mm original, with all seven
original In4 contacts preserved. The full-width ground continuation calculates
to 4.924330 mm with five adjacent microvias; no new narrow copper is used.
The exact catalog, frozen 61-edge preservation, native/physical counts, full
unchanged DRC, refill/replay/fault/source and original-orphan evidence pass.
All engineering and fabrication holds remain open.
