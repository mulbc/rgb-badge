<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0292: Supported mechanical transition for the row

Date: 2026-11-24
Status: Accepted for bounded RAM-only continuity discovery.

The early single In1/In2 transition graph exhausts70844 states without
a real In2 row join. Keep the exact cell, source cohort and clear F row
escape. Search In1/In2/In3 with one early supported0.30/0.10 mm In1/In2
microvia and at most one supported0.50/0.30 mm mechanically drilled
In2/In3 buried via. The first transition is within0.75 mm conductor of
the existing proposed F/In1 access; then remain on In2 until the central
transition and on In3 until an actual original ROW04 Cu/pad destination.
Bound x76..85/y10..16 mm,0.025 mm/100000 states/12 mm total conductor.
No unsupported centre microvia, through hole or additional source change.

Both transition kinds must pass the unchanged full source and mutual drill
policy: no mechanical same-position stacking exception, no unsupported
source exception. Ordinary0.20 mm Cu clearance remains unchanged. Require
ROW18/VLED40/GND197/gate4,21 matching opens, all209 original groups except
pending selector, all19256 retained attached source Cu and no orphans.
A full20-open/all210-group cell, separate exact PCB qualification and
original DRC/replay/inverse/fault/visual/part/electrical/stack/Gate A holds
still precede selection. No PCB write; fabrication is prohibited.
