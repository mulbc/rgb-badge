<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0179: Complete two-part sensor routing alternative

Date: 2026-11-16
Status: Accepted for ignored complete-circuit feasibility only; no successor selected.

The first ADR0177 cohort restores hot/output connections but its cold and USB
supply paths remain unresolved under both tested route orders. Permit a second
exact prototype using only the already screened second ADR0172 sensor pose
and first ADR0174 cold-resistor pose: U39 TMP390A2DRLR (57.900,16.200) mm /
270°, R90 ERJ2RKF1402X (60.150,16.750) mm / 0°. Keep R89 ERJ2RKF2151X at its
original (59.865,15.000) mm / 270° and every other part/field/land/pin net fixed.
All courtyard/pad checks and ≤3 mm programming/ground, thermal reservation,
sensor movement and no-worse C50 pad-distance bounds remain mandatory.

Use immutable selected 28-open source and exactly the same seventeen original
ordinary B.Cu study retirements/full native contact catalog. No source via or
other copper may be retired or changed. The exact supply neck is 0.20 mm B.Cu
from (57.900,16.940) to (57.950,17.640) mm, with one supported 0.30/0.10 mm
B/In4 capture at its end. Independently transform every moved integer pad.

All ADR0177 routing classes, source profiles, x=52–64/y=12–21 mm cardinal
0.050 mm grid, 500,000-node and per-join/per-net length bounds apply unchanged,
including the fixed new supply neck within its 8 mm net budget. Route-order
variants are permitted. Only the same five local restoration nets may gain
copper. Any original-current-group split must reject/undo the new join.

A source successor requires every original external branch/contact, all 216
original groups and complete hot/cold/output/ground/bypass/supply continuity,
matching native/physical reduction below 28, exact original 104 findings and
all independent source/contact/hole/replay/inverse/orphan/fault/visual gates.
A partial prototype or lower isolated count is never selection. No thermal
error, threshold/current/protection/NTC/timer/default-off/part/HDI/stack/process/
fit/Gate A or fabrication boundary changes. Zero opens remains unfinished.
