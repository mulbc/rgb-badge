<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0237: Exact R6 direct bottom prototype

Date: 2026-11-20
Status: Accepted for frozen ignored prototype and full successor validation.

ADR0236's exact 23,100-pose screen finds 1,043 complete source/mutual-clear
placements, rejecting 14,480 for courtyards, 4,652 for pads and 2,925 for
lead templates. Select only the shortest combined lead candidate for an
ignored prototype: exact R6 ERJ2RKF1001X B (77.750,5.600) mm / 90 degrees.
Keep every other footprint and every original color/row trace unchanged.
The independent absolute R6 pad transform is x'=86.500-y / y'=x-51.650 mm.

Freeze mechanical/review/r6-direct-bottom-plan.json before PCB generation.
Retire exactly ADR0119's six original R6 supply items, retaining the unchanged
0.20 mm shared-stem remainder (58.750,9.713636)→(58.750,14.050). Add only
the five supported gate vias (four 0.30/0.10 microvias and one 0.50/0.30
mechanical In2/In3 centre), two fixed inner gate leads and the two B leads
frozen by ADR0236. Supply runs R6.1 (77.750,6.100)→original main VLED
PAIR02.4 (78.825,6.650), 1.207529 mm. Gate runs R6.2 (77.750,5.100)→lower
capture (76.650,4.550) and through the frozen supported transition to actual
PAIR01 gate body (76.600,4.300), total conductor 2.224775 mm. Every wire is
0.20 mm. No new power via, color replacement or through transition is allowed.

The intended successor has 24 matching native/physical opens, 212 groups /
188 nets, all 213 prior groups and retained attached Cu intact, zero orphans,
main GND197 and main VLED37. ROW_GATE_00 must contain all four original pads.
The exact original104 DRC must remain; PAIR01's inherited intrinsic mapping
remains exact and no new finding is waived. Require raw serialized Cu,
part/pad/field/source-contact proofs, actual B courtyards and full new/source
drill rules, deterministic replay/refill, byte-exact inverse with all nine
zone XORs empty, fault and native visual checks before selection.

The original PAIR01 VLED pin and all other remaining opens stay explicit.
Current/protection/default-off, exact trial package and all electrical/timing/
return/thermal, fit/process/controlled-stack and independent Gate A/fabrication
holds remain. No hardware performance or release is claimed.

All full successor gates pass; select the exact 24-open CAD checkpoint on
2026-11-20. See the development record and machine-readable checkpoint.
All electrical/process/Gate A/fabrication holds remain unchanged.
