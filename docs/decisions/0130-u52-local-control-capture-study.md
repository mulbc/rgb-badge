<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0130: Bounded U52 control-capture placement

Date: 2026-11-14
Status: Accepted for ignored feasibility only; no successor selected.

Continue the ignored ADR 0129 interface-restored trial from immutable selected
33-open source `14f0c49582063bab84ea685a8cec798011eb4cd66389b085a3a47777180a13ce`.
Its actual U51 output capture reaches the larger routing graph, but U52.1's
fixed edge component exhausts after 5,884 expansions. Its adjacent capture is
blocked chiefly by retained COL_13_R In4 copper; no colour copper retirement
is authorized.

Permit exactly U52's translation from (69.25,1.0) to (68.75,1.0) mm, retaining
180-degree orientation, board side, exact SN74LVC1G08DSFR, fields, pin numbers,
local pads and NCs. TI SCES217AA page 3 and DSF0006A PDF page 35 retain the
existing 0.6 × 0.17 mm lands, 0.35 mm pitch and 0.8 mm row spacing. Retire only
its original 0.20 mm +3V3_APP B.Cu leaf
`9bf66294-f9fb-5c34-b774-02b3000f6dfa` (68.85,0.65)–(68.2,0.65) mm.
The moved VCC land must directly retain contact to original track
`15254fa2-f738-593f-8c07-41f52b5e7bff`; no replacement supply limit or domain.

Retain original ground track `2f3709dd-8895-5e91-8827-796974de6d2d` and restore
U52.3 through ordinary 0.20 mm B.Cu segments
(69.15,1.5)–(69.65,1.5)–(69.65,1.35) mm. Test one supported B/In4 0.30/0.10 mm
capture at (69.15,0.5) mm overlapping U52.1. Require native copper/hole/edge,
moved courtyard, power/ground contact and every one of the original 221 live
groups. Retain all other source parts/copper outside the exact ADR 0129 and
this one-leaf retirement cohorts. No new centre microvia or narrower route.

For this feasibility move only, the existing intrinsic U52 pad-pair finding
coordinates translate by exactly −0.500 mm in x. A future successor must
compare all 104 original findings with only that predetermined U52-item
coordinate transform; every UUID, pair, description, actual clearance,
severity and other finding field must remain identical. No finding may be
removed, added, ignored or waived. The selected source's existing exact DRC
gate remains unchanged. Unfinished output captures remain unselected until
their dangling findings disappear in an actual U51.4–U52.1 join.

Selection still requires matching native/physical count below 33, every prior
live group, exact pose/retirement/addition ledger, independent stable replay,
fault/source and visual checks. All electrical/stack/process/fit and independent
Gate A holds remain; fabrication and powered-operation claims are prohibited.

The first pose is rejected before saving: U52.4 approaches retained
ROW_SEL_01 track `0813a7ad-ae92-5570-9240-c7161eb21750` at y=1.55 mm.
Revise the sole proposed U52 pose to (68.75,0.90) mm (−0.50,−0.10 mm).
Use ground segments (69.15,1.4)–(69.65,1.4)–(69.65,1.35) mm and the supported
input capture at (69.15,0.40) mm. Preserve the same exact one-leaf retirement
and all other boundaries. The predetermined intrinsic U52-item coordinate
transform is now exactly (−0.500,−0.100) mm; every other finding field remains
unchanged. The original pose and all preceding selected sources stay immutable.

The upward revision is also rejected before saving for the same retained
ROW_SEL_01 track. Replace the leftward proposal with the single exact U52 pose
(69.75,1.0) mm: +0.500 mm in x, unchanged y/orientation/layer. Extend the exact
retirement cohort only to its original ground leaf
`2f3709dd-8895-5e91-8827-796974de6d2d`, (69.65,1.35)–(70.35,1.35) mm.
The moved ground land must directly retain that leaf's original outer ground
contact at (70.35,1.35) mm; freeze its full native contact catalog first.
The replacement supply is an ordinary 0.20 mm B.Cu segment from original
(68.2,0.65) to (69.35,0.5) mm, retaining the original external supply contact.
Use the supported input capture at (70.25,0.5) mm. No proposed leftward ground
branches are retained. All other source contacts/groups and every other source
copper item remain required. The sole predetermined finding transform is now
U52-item x +0.500 mm, unchanged y; every other finding field remains exact.

Before saving any rightward candidate, use a bounded native pose/capture screen
rather than assuming clearance to the original ground tail. Permit U52-only
translations dx=−0.750..+0.750 mm and dy=−0.250..+0.250 mm in 0.025 mm
increments (1,281 poses), retaining orientation/layer/MPN/local lands. The same
exact two-leaf retirement cohort applies; retain all other source copper and
freeze any successful exact pose before successor validation. Screen actual
moved pads/courtyards and supported B/In4 captures overlapping U52.1. Any
needed ordinary-width power/ground restoration is bounded to 3 mm per branch,
with the original complete external contacts and all 221 source groups required.
No other pose, retirement, finding normalization or rule change is allowed.
An eventual finding comparison may inverse-transform only U52 items by that
one frozen pose; all 104 pairs and all remaining fields stay exact.

The 1,281-pose screen finds 137 geometrically clear poses but no overlapping
capture across the complete sampled contact range (±0.425 mm x, ±0.225 mm y).
Also permit a fixed-pose alternative retaining both original U52 leaves: an
ordinary B.Cu fan no longer than 3 mm to a supported adjacent capture within
1.5 mm of U52.1, on a 0.025 mm native-screened local graph. This adds no pose
or retirement permission; all original groups, exact findings and full final
successor gates still apply. A sampled failure is not general infeasibility.

For the same 137 geometrically clear poses, permit that short B.Cu fan screen
with the exact two-leaf cohort removed, retaining its complete source contacts
for subsequent restoration. Keep the 1.5 mm capture reach and 3 mm branch
length limits, actual copper/board/hole checks and the single frozen-pose
comparison. No other source retirement, rule or part change is authorized.
