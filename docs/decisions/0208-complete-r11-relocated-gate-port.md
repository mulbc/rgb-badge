<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0208: Complete R11 relocated gate port

Date: 2026-11-16
Status: Accepted for exact ignored complete-circuit feasibility only.

ADR0207 finds supported B/In4 access directly at R11's new gate pad. Keep
the exact R11/R21 poses, VLED leads and proven two-track ground substitution.
Add supported 0.30/0.10 mm B/In4 gate via at (71.500,7.500) mm, touching
R11.2. No initial gate neck is needed. Retire additional original B/In4 via
55768222-e337-59d5-84e8-9cdd42f4ad9a at (72.150,4.250) mm, whose only
outside inner contact is retained 0.20 mm In4 wire
6df0bbfc-ab37-5f5e-98d4-b7e151596a3d,
(72.150,4.250)–(76.650,4.250) mm. Its original B leaf was already frozen
for retirement. This removes the obsolete surface transition rather than
leaving a disconnected via layer or an artificial stub. Freeze its full
source contacts; the combined original retirement cohort is six items.

Complete the gate lead to that exact retained In4 wire endpoint, not an
arbitrary point elsewhere in its group. Native 0.050 mm eight-neighbour
graph, x=70–77 / y=3.5–9 mm, ≤300,000 expanded nodes per attempt and
≤8 mm total new ROW_GATE_05 trace. Prefer B/In4 first; B/In4/In3 may be
tested as a separate bounded alternative. New outer transitions only use
supported 0.30/0.10 mm microvias; no centre or full-span transition.

Preserve every native foreign/no-net/mutual copper, original edge/clearance/
ordinary-width/hole rule and current group after each refill. Require actual
new copper contact at the retained original In4 endpoint, all original gate
and ground interfaces, all 216 immutable groups, matching reduced native/
physical opens and exact original 104 findings. All source/part/pad/profile/
type/contact/hole/replay/inverse/orphan/fault/visual gates precede selection.
Any new dangling item or rail split rejects the candidate. All current/value/
protection/default-off/electrical/thermal/part/stack/process/fit/Gate A and
fabrication holds remain unchanged.
