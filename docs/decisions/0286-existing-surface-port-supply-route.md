<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0286: Routed supply connection between existing surface ports

Date: 2026-11-24
Status: Accepted for bounded RAM-only additive continuity discovery.

ADR0285 direct/L templates fail copper clearance. Existing F supply
ports are farther apart: retained six-pad capture78.8,10.65 to the
actual34-pad PAIR05.4 at82.75,14.025 has calculated5.19549 mm straight
and7.325 mm orthogonal distance, before obstacles. The former4 mm
surface bound cannot cover that no-new-hole connection.

Keep the same exact cell/cohort/real row path. Test B and In4 under
ADR0285's6 mm bound, and F under an8 mm ordinary0.20 mm bound, each
single-layer0.025 mm/100000-state search. F regionx76..85/y7..17;
B/In4 regionx72..83/y7..16. Starts/goals are actual existing Cu or pads
proved in the six-/34-pad native groups; terminate robustly inside real
pads/vias or on source trace centreline. No new via, source retirement,
width/clearance/profile/current/protection or component change.

A real completed wire and native refill must restore VLED40/GND197,
row18/gate4, every original group except explicitly pending selector,
all19256 retained attached source Cu/no orphans and21 matching opens.
Only final20 opens/all210 original groups may advance. Write no PCB.
Power loss/current-sharing/return/electrical/trial-package/thermal/stack/
process/assembly/fit and independent Gate A holds persist; fabrication
is prohibited.
