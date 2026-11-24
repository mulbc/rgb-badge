<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0243: Exact PAIR01 supply routing prototype

Date: 2026-11-20
Status: Accepted for ignored prototype and complete validation; unselected.

Freeze `mechanical/review/pair01-supply-routing-plan.json` against selected
24-open source SHA230b0c9f456837a0dd1b5e432497aa5223da95334ac2909ff8cd39d2edea804a.
Move only existing trial NTLJD3119CTBG_TRIAL_ONLY PAIR01 on F from
(76.100,4.300)/270° to (80.000,5.200)/180°, without a flip or substitution.
The independent pad transform is x'=84.300-y, y'=x-70.900 mm. Keep all
fields, local package geometry, numbered nets and other 482 parts unchanged.

Retire exactly ADR0239's 62 obsolete package-leaf items: the preceding
PAIR01 front-ground plan's 61 additions and only the R6-plan F/In1 gate
microvia at (76.600,4.300). Preserve its In1/In2 gate port, all original
color/row copper and all other 19,322 source copper items. Freeze every
retired signature/type and native outside-contact catalogue before writing.

Add exactly the plan's 27 deterministic copper items: eleven fixed items
qualified in ADR0239/0242 (direct F ground, three-segment F supply, three
package straps, two F/In1 accesses and two In1 gate/row leads), plus sixteen
selector items from ADR0242's successful 12,450-node search. Its 4.099138 mm
selector conductor uses three F/In1 0.30/0.10 mm transitions at
(81.100,5.300), (82.450,6.400), (84.000,7.250), and reaches original driver
In1 segment de96a271-92f1-5663-beaa-4f8a0e5658a4 near (84.000,7.425).
No In1/In2 selector via was needed. All tracks are ordinary 0.20 mm.
The direct F supply is 4.625 mm; the In1 row lead remains below 6 mm.
No new centre or through via is permitted. Require every source/new hole
and actual F courtyard check under the unchanged policy.

Before adoption require matching native/physical 23 opens, all 212 original
groups and retained attached copper preserved, zero orphan copper, GND197,
VLED38 including all prior37 and PAIR01.4, ROW00A18, GATE00 four and
SEL00 three pads. Require exact serialized source/new ledgers and package
identity, profiles and board structure. Normalize only six intrinsic own-
PAIR01 pad-pair clearance findings (twelve item occurrences) using the
independent pad transform; no external finding may normalize. Apply the
preceding exact104 DRC comparison after this transform. Require stable
independent replays, byte-identical 24-open inverse including all nine zone
XORs, native disconnection/source/policy fault controls and visual review.

The ignored prototype is not a selected successor until every gate passes.
Current/protection/default-off, timing/return/thermal, trial package,
assembly/optical/fit, process/controlled-stack and independent Gate A holds
remain open; no fabrication release is permitted.

All complete successor gates pass; select the23-open CAD checkpoint on
2026-11-20. See the development record and machine-readable checkpoint.
All qualification/Gate A/fabrication holds remain unchanged.
