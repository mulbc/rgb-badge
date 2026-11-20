<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0103: Bounded ROW_SEL_15 detour for the anchored R8 flip

Date: 2026-11-09
Status: Accepted for ignored feasibility only; no successor selected.

Study exactly one original 0.20 mm B.Cu ROW_SEL_15 track, from
(68.900,7.850) to (73.350,7.850) mm, UUID
8f141701-3e53-50fe-a1fe-bc2869d6daab. An ordinary B.Cu replacement may detour
inside x=68.85–73.40 mm, y=5.50–9.80 mm, with at most 12 mm total length.
Retain both original endpoints, every direct original B.Cu copper contact,
all other accepted copper and every prior live pad group. Do not retire or
alter ROW_SEL_00/01, the adjoining ROW_SEL_15 vertical, or any other trace.

This study permits the ADR 0095 +90° R8 flip about its fixed VLED pad-1
centre, retaining every original supply contact, exact ERJ2RKF1001X / 1 kΩ
part, fields, numbered nets and local footprint geometry. An ordinary
B.Cu/In4.Cu ROW_GATE_02 lead of at most 5 mm may join R8.2 to PAIR03.5,
using at most two adjacent 0.30/0.10 mm B.Cu/In4.Cu microvias. All other
poses, profiles, zones, current limits, hardware permissions and protections
stay fixed. This explicitly extends the earlier no-retirement R8 screens
only for the single exact track named above.

Check foreign copper and courtyards, including interactions between all new
traces/vias and the rotated footprint. Refill and independently preserve every
prior pad group, source-copper identity and numbered-pad join. Selection
requires exact unchanged 104 native findings, a complete deterministic ledger,
stable replay/fills, source/fault checks and visual review. Finite route
failure is not proof of global impossibility. Keep the validated 37-open
checkpoint selected until all successor gates pass. Power/gate/transient,
assembly/process/fit and independent Gate A qualification remain open;
fabrication is prohibited.

The B.Cu-only 0.05 mm native-shape search exhausts its reachable 851-node
graph without a detour; sampled rectangular jogs also fail. Extend the same
single-track replacement to ordinary B.Cu/In4.Cu routing inside the same
bounds and 12 mm combined length, with at most two additional adjacent
0.30/0.10 mm B.Cu/In4.Cu microvias. Its original endpoints and all six
original direct B.Cu contacts must remain on replacement B.Cu shapes.
The adjoining vertical track and all other source copper remain untouched.
Check the new ROW_SEL_15 path against the entire proposed ROW_GATE_02 path,
including all four possible captures. No central transition or relaxed rule
is permitted. No candidate is selected by this extension.

The recorded B.Cu/In4.Cu capture screen also finds zero eligible left and
right captures in the sampled regions. No copper replacement, resistor
pose or successor is selected. See the
[follow-up record](../development/remaining-routing-followup-2026-11-09.md).
