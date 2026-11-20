<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0226: PAIR01 front ground prototype

Date: 2026-11-20
Status: Accepted for a frozen ignored CAD prototype and full successor gates.

ADR0225's two-part candidate is rejected: it splits the existing R6 VLED
supply group after refill. The explicit supply lead and bounded replacement
capture searches do not establish a legal ≤6 mm connection. Keep all raw
failed evidence and do not select that candidate.

Starting from the unchanged qualified 26-open source, move only the exact
trial PAIR01 package to F (76.100,4.300) mm / 270 degrees using a native
top-bottom flip. Keep R6, its six original supply items and all other parts
fixed. Preserve original isolated PAIR01.4 VLED and the original independent
R6 gate group; do not claim either open closed. The independent PAIR01 pad
transform is (79850000-y,80050000-x) integer nm.

Freeze mechanical/review/pair01-front-ground-plan.json before PCB generation.
Retire only the previously proved 32 private selector items, four obsolete
row-output items and two old gate straps. Add the three screened F package
gate/output straps, the F lead to the original row port, supported F/In1
GND/selector accesses, the screened In1 GND lead and exact selector path.
Do not add any power lead, VLED via, R6 lead or shortened supply stem.
Retain every original shared selector/row interface and all other source Cu.
No new central/through transitions are authorized.

Expected reduction is exactly 26→25 native and independently physical opens,
214→213 groups / 188 nets. Preserve every original group, attached retained
Cu and numbered pad; new Cu must all attach. Main GND grows 196→197 and
main VLED stays 37. Keep complete original PAIR gate three-pad, R6 isolated
gate one-pad, selector three-pad and row-output eighteen-pad groups intact.
Require exact raw copper and part transforms, all holes/front courtyards,
stable deterministic replay/refill, full inverse source-byte and nine zone
XOR equality, full baseline104 DRC after only exact intrinsic PAIR01 pad
normalization, and fault/visual checks before canonical selection.

The package remains trial-only, with no silent MPN/BOM substitution. All
current/protection/default-off, electrical/return/thermal, process/filled-via,
controlled-stack, assembly/optical/fit and independent Gate A holds remain.
This authorizes no fabrication release or hardware performance claim.

All required successor gates pass; the 25-open CAD candidate is selected on
2026-11-20. Exact evidence is in the paired checkpoint and development record.
This selection does not resolve any fabrication or electrical qualification hold.
