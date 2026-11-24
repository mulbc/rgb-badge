<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0135: Exact U52/C71 local cluster prototype

Date: 2026-11-14
Status: Accepted for ignored complete-cluster feasibility; no successor selected.

The immutable selected source remains 33 native/physical opens, SHA-256
`14f0c49582063bab84ea685a8cec798011eb4cd66389b085a3a47777180a13ce`.
Continue from ADR 0134's exact-interface B.Cu detour prototype,
`72ddb67b3530d15a19b06252e707460f7534964f5a3e9edea38eaf296e80cb5e`.
It retains all 221 original live groups and the exact original 104 findings
plus only the unfinished U51 output capture. No source board is selected by
this decision.

Freeze exactly two B-side poses, retaining manufacturer part identity, fields,
local lands, pad numbers and nets:

- U52 SN74LVC1G08DSFR: (69.25,1.0) mm / 180 degrees to
  (103.2,5.275) mm / 90 degrees.
- C71 GRM155R71C104KA88D: (68.1,3.295) mm / 90 degrees to
  (103.0,6.75) mm / 180 degrees.

Co-locate the original bypass with the gate. The owner-supplied Murata reference
is dated 2014 and is not current approval or a recommended land pattern.
Keep the existing footprint unchanged; part approval, capacitance and
assembly/process qualification remain open.

Permit only these six additional original private-leaf retirements, with
native catalog SHA-256 `9ad4446e8d7b6516797a3a3739e9fc341df90776738aa1708e703eb6d483d0a3`:

- `9bf66294-f9fb-5c34-b774-02b3000f6dfa`: U52 APP 0.12 mm B.Cu head.
- `15254fa2-f738-593f-8c07-41f52b5e7bff`: its 0.20 mm B.Cu tail.
- `68b7363f-10d2-5d5c-8091-0cf040b2a189`: its private APP B/In4 capture.
- `92bb2acd-fe8a-5220-bf9c-212fe569e9a9`: C71 APP 0.20 mm B.Cu leaf.
- `b4491996-43cd-5299-9200-6a7d40282591`: its private APP B/In4 capture.
- `2f3709dd-8895-5e91-8827-796974de6d2d`: U52 GND 0.12 mm B.Cu head.

The private APP captures terminate in individually native-witnessed APP In4
filled components, with no other copper/terminal contact. The ground head
contacts the original grounded B.Cu component and retained ground tail.
Retain every other original copper item/native via type and every other part,
pose, rule/profile, net and board/zone outline, including the exact prior
MODE_BOOT_N and two-track ROW_SEL_14 obligations.

Test a supported B/In4 0.30/0.10 mm C71 APP capture at (103.4,6.4) mm.
Gate APP and input captures may use straight 0.12 mm B.Cu necks no longer than
0.750 mm, under the unchanged exact U52 package/net rule. Prefer capture
positions near (104.0,5.4) and (103.975,6.275) mm respectively; select actual
clear points within ±0.125 mm of each preference, freezing their exact
geometry before selection. Every neck must intersect the actual new courtyard.
Check native foreign/no-net/mechanical copper, all holes and actual board edges.
Use ordinary 0.20 mm copper beyond those exact local necks; no new centre
microvia or rule/clearance relaxation.

Restore U52 GND with a bounded existing-rule neck to original retained ground
contact (102.4,5.75) mm and C71 GND with ordinary local B.Cu copper to that same
contact. Power/ground branches are bounded to 3 mm each. Refill and restore all
221 original live groups before signal continuation. No current, rail-domain,
protection or default-off setting may change. A temporary partial prototype
is unselected and cannot count as an actual new terminal connection.

Check each new pad position against an independent integer transform of its
original position. A completed successor must join U51.4–U52.1 and match
native/physical opens below 33, with no extra finding. Only U52's original
intrinsic finding-item coordinates may follow that one frozen pose; every
original UUID/pair/description/actual-clearance/severity field must remain
identical. No C71 or other finding allowance, ignored check or waiver.

Final selection requires complete exact pose/retirement/addition/contact ledger,
independent stable replay/refills, original-orphan proof, native faults,
source checks and visual review. All electrical, bypass/return/timing,
controlled-stack/process/fit and independent Gate A holds remain. No fabrication
or powered-operation qualification is authorized.

The initial APP preference at (103.95,5.1) mm is blocked. A complete straight-neck screen on a 0.025 mm grid within 0.750 mm of pad 6 finds nine clear captures, including (104.0,5.4) mm. Use that exact revised preference; the source and rules remain unchanged.
