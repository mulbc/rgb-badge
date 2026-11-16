<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0200: Fixed-pad supply resistor prototype

Date: 2026-11-16
Status: Accepted for ignored complete-circuit feasibility only.

ADR0199's twelve cardinal poses yield two clear alternatives in addition to
the three original controls, with every old direct contact retained. Neither
new supply pad directly joins main VLED. Freeze exact R21 ERJ2RKF1001X at
(66.250,5.750) mm, 0 degrees, fixed gate pad 2 (66.750,5.750); and exact
R11 ERJ2RKF1001X at (72.250,3.750), 270 degrees, fixed gate pad 2
(72.250,4.250). R71 and every other part remain fixed. No source copper
retirement or initial addition is permitted; both original connected gate
groups and every original contact must survive native refills.

Write an ignored exact-pose prototype only after full native mutual pad,
foreign/no-net copper, courtyard, source-edge and direct-contact checks.
Verify all 216 original groups, original 104 finding payloads, unchanged
parts/local pads, independently transformed global pads, all 19,381 source
copper items/types, profiles/rules and board structure. A count change due
only to pose is not acceptance without all successor gates.

Permit bounded additive ordinary 0.20 mm VLED routing only from the actual
new R21/R11 pad groups to actual retained main VLED copper or individually
witnessed source-plane units. Native eight-neighbour 0.050 mm full-board
grid, supported 0.30/0.10 outer microvias and 0.50/0.30 mechanical In2/In3
vias only, ≤1,000,000 expanded nodes per attempt. New resistor-feed copper
≤12 mm per resistor; at most 4 mm new In2 copper in segments ≤4 mm.
Preserve actual source edge/clearance/hole/ordinary-width rules and every
current group after every refill. No current limit or resistor value changes.

Selection requires all original groups and outside contacts, matching native/
physical reduction below 28, exact104 and full source/replay/inverse/contact/
hole/orphan/fault/visual gates. Incomplete paths or rail splits reject the
candidate. No part/process/stack/fit/electrical/Gate A/fabrication hold changes.
