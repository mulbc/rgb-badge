<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0209: Minimal R21 source qualification

Date: 2026-11-19
Status: Accepted for the exact qualified routing source; fabrication remains prohibited.

The complete ADR0204 candidate retains 216 original groups at 27 native/
physical opens with exact104, independent replays and byte-identical inverse.
Its fault campaign establishes that removing the new VLED lead does not
disconnect R21: the moved supply pad already touches retained main VLED
copper. Qualify the smaller exact exchange instead of retaining redundant
new supply copper.

Keep exact R21 ERJ2RKF1001X at (59.300,5.600) mm / 0 degrees and the two
ADR0204 original ROW_GATE_15 retirements. Add only its two ordinary 0.20 mm
B gate replacements, (59.800,5.600)–(59.800,5.000)–(56.750,5.000) mm.
No new VLED trace or via. Freeze every actual retained source B VLED copper
contact with R21.1 and prove that each belonged to the original main VLED
group before the move. Preserve the original gate via and complete four-pad
gate group. Every other original copper item/type, part/pad/net/profile/rule
and immutable board structure remains exact.

Require all 216 original groups and all attached retained source copper,
27 matching native/physical opens, main VLED 35→36 pads, exact original
104 findings, independent exact replays, three stable refills, byte-identical
inverse with all original groups and nine zone XOR checks, actual native
disconnection faults, serialized source-declaration guards and visual review.
Native import can repair a corrupted trace label; compare original serialized
copper before import so such an edit cannot be concealed by repair. No new
orphan copper or altered ignored check is permitted.

Only after every source/contact/hole/replay/inverse/fault/visual gate passes
may this exact smaller successor be selected. R11 and every unselected ground
substitution remain at the immutable parent geometry. Zero opens remains
unfinished. No current/value/protection/default-off/electrical/thermal/part/
stack/process/fit/Gate A or fabrication hold changes.
