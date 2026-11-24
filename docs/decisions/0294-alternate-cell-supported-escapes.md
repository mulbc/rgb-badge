<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0294: Actual-contact front-cell escapes

Date: 2026-11-24
Status: Accepted for bounded RAM-only complete continuity discovery.

The alternate screen yields PAIR05 F83.4,12.7/90, R10 F83.7,10.7/180,
R26 F83.1,14.7/180 with ten real short conductors. Independently verify
absolute transforms PAIR05:(72.15+y,x-63.05), R10:(36.45+x,14.95-y),
R26:(45.85+x,21.95-y) in mm. Native initial continuity and all source/
identity/field/local-pad/Cu/hole/courtyard boundaries remain mandatory.

On either exact original or alternate cell, starts may be any actual
Cu/PAD member of the new two-pad ROW04 group, including its real package
body contact. Goals remain actual retained16-pad ROW04 Cu/PADs. Search
F/In1 within x76..86/y10..17 mm,0.025 mm/100000 states,11 mm new
conductor, at most three supported0.30/0.10 mm F/In1 microvias. No extra
source retirement, centre/through via, width, clearance or current change.
Use the unchanged full source/mutual hole policy and native refill proof
of ROW18/VLED40/GND197/gate4,209 original groups with only selector
pending,19256 retained attached source Cu and zero orphans,21 opens.

The alternate selector may use the same real U2-side port and supported
F/In1 layer access within the ADR0290 corridor/length/one-microvia bounds.
Complete row+selector must match20 opens and all210 original groups before
separate PCB qualification. No partial source selection or PCB write;
original DRC/replay/inverse/fault/visual/electrical/stack/Gate A holds remain.
Fabrication is prohibited.
