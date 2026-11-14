<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0120: Screen PAIR01 and R6 as a coordinated local circuit

Date: 2026-11-12
Status: Accepted for read-only geometry study; no PCB migration selected.

ADR 0119's finite R6-only screen selects no complete gate/supply arrangement.
Before replacing unrelated routing, test whether exact PAIR01 and its exact
R6 pull-up can fit together just beyond the crowded matrix fanout. Use the
corrected 35-open source, SHA-256
`3967bb66e89e0005f6859ce78a766b4536d06883b76fce130e75a6fdeefaf96e`.
No footprint, circuit, part, value, current limit or permission changes.

The read-only template retains PAIR01's current local geometry and places R6
2.75 mm to its gate side, outside both courtyards. A 1.325 mm ordinary B.Cu
lead joins the existing P-gate/N-drain node. A separate ordinary B.Cu lead
joins the 1 kΩ supply to the P-source VLED land. Test four whole-template
right-angle rotations, actual pad/track/via shapes and back-side courtyards,
with unchanged 0.2 mm conductor/clearance and 0.5 mm copper-edge constraints.
All fixed source components and copper remain obstructions. The preliminary
drain-distance screen must retain a ≤6 mm straight-line lower bound to actual
retained ROW_00_A copper at the old through-via centre, not an invented net
anchor. Optionally screen a supported-size local supply stack; this cannot
prove filled-plane connectivity or a controlled manufacturing process.

Do not save a PCB from this screen. A later trial requires a new exact ledger
for both poses, internal straps and obsolete external leaves, with all actual
source contacts re-derived and preserved. Inventory any affected accepted
addition explicitly. Require the real row-current route to be ≤6 mm at its
original width, a bounded local gate/pull-up association, explicit main-VLED
and main-GND continuity, full ROW_SEL_00 restoration and every original live
group. Preserve all ADR 0117 copper and exact corrected flip-flop pins.
No new unsupported central microvia, current increase or protection bypass.

Finite clear samples are not layout acceptance. Selection still requires
native refills, independent physical groups, exact full DRC identities,
contact/retirement proof, deterministic replays, native/source/fault and visual
checks. Any translated intrinsic package findings require independently
verified unchanged local geometry and exact current pad coordinates; no new
finding, waiver or severity change is allowed. Electrical/thermal/process/fit
qualification and independent Gate A remain open; fabrication is prohibited.

## Read-only result

The [controlled record](../../mechanical/review/pair01-r6-locality-2026-11-12.json)
tests 64,272 poses. Of those, 56,417 exceed the 6 mm drain-distance lower
bound, and all remaining 7,855 fail fixed courtyards. U1, PAIR02 and U38 are
the most frequently observed fixed blockers. No pad/capture-clear candidate,
PCB migration, copper retirement or count reduction is selected. Source bytes
remain unchanged at 35 opens. The result covers only this finite rigid template;
it does not prove that another coordinated floorplan is impossible.


The first screen's 90°/270° coordinate sine sign was corrected to KiCad's
Y-down orientation convention. All four manual template transforms are now
asserted against actual native terminal positions before sampling. The
corrected native replay gives the same courtyard/distance counts and no-fit
conclusion. No source PCB was changed by either read-only run.
