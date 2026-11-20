<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0180: Read-only private row-bus hops for sensor supply

Date: 2026-11-16
Status: Accepted for read-only complete-interface discovery only.

The exact ADR0179 sensor cohort restores hot/cold programming, but a short
B.Cu supply feed from its VDD escape to existing C50.1 crosses two retained
ordinary B.Cu row-gate segments. Read-only test complete local hop replacements
for only original ROW_GATE_10 UUID `1764c886-a4cb-5802-8866-4d441138d241`
(56.750,18.150)–(69.550,18.150) mm and ROW_GATE_12 UUID
`d4a23a8f-a1c2-5026-8592-436695b66cdb` (56.650,18.600)–(69.400,18.600) mm.
Both are 0.20 mm B.Cu. Freeze all exact source signatures and complete native
source contacts against the immutable selected 28-open board before screening.
No original via, other source copper or further part may be omitted.

Use the exact ADR0179 poses and seventeen-item local cohort in memory. Keep
unchanged outer portions of each bus on B.Cu and bridge only its local gap with
two supported 0.30/0.10 mm B/In4 captures and ordinary 0.20 mm In4 lead ≤2.5 mm.
Sample capture x positions at 0.050 mm increments within ±0.300 mm of centres
(57.050,18.150)/(58.400,18.150) for gate 10 and
(56.800,18.600)/(58.150,18.600) for gate 12. Preserve all external source-layer
contacts physically with the replacement, including endcaps/intermediate
branches; a same-net/group label alone is insufficient.

Include the prospective ordinary B.Cu USB supply path from U39.5 through
(57.950,17.640) mm to original C50.1 (57.285,19.295) mm as a mutual obstacle.
The unused proposed VDD microvia may be omitted because it is not original
source copper; this authorizes no original via retirement. Require exact
foreign/no-net/source/mutual copper clearance, original source edge minimum,
actual source hole policy and all moved part/courtyard/programming/thermal
bounds. Write no PCB and record finite misses or exact complete hop cohorts.

Any later prototype requires a further exact complete-circuit scope restoring
all 216 original groups, both original row-gate groups, every original external
branch and full sensor hot/cold/output/ground/supply continuity. Matching reduced
native/physical count, exact original 104 findings and all source/contact/hole/
replay/inverse/orphan/fault/visual gates precede selection. No current/threshold/
protection/NTC/timer/default-off/part/HDI/stack/process/fit/Gate A or fabrication
approval changes. Zero opens remains unfinished.
