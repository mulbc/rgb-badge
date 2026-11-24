<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0090: Bounded stack proposal and U36 stage corrections

Date: 2026-11-06
Status: Accepted for the 47-edge CAD routing-study successor and a provisional
manufacturing target; no electrical/process qualification or fabrication release.

## Context

The owner requested the necessary corrections after the GRM188/HDI review.
The supplied 1+4+1 proposal neither sums to its stated thickness nor supports
the current inner-layer microvias. ADR 0089 also identifies the incomplete
U36 stage. Its 50-edge parent is a routing study, not a qualified power layout.

## Corrected manufacturing intent

Use 0.80 mm as the connector-driven target pending supplier finished-thickness
tolerance and mask/finish allowance. Investigate a six-layer 2+2+2 build:
four 0.076 mm build-up dielectrics, six 0.035 mm copper layers and a 0.286 mm
central dielectric sum to 0.800 mm before mask/finish. This is a geometric
planning scenario, not a controlled supplier build.

Allow nominal 0.30/0.10 mm microvias only across L1–L2, L2–L3, L4–L5 and
L5–L6. The central L3–L4 transition requires a proposed mechanically drilled
0.50/0.30 mm buried via. Preserve the 0.10 mm annular-ring floor and existing
0.50/0.30 mm through-via geometry. Do not shrink pads or relax the global
mechanical-drill floor to adopt the original 0.25/0.10 or 0.45/0.20 proposal.

Enforce this intent with a fail-closed span/pad/hole/nominal-aspect check.
The current source still has 557 incompatible centre-layer microvias and no
controlled stack. Retyping/enlarging those vias in place loses connections
and creates shorts; no such candidate is selected. The comparison CAD retains
its historical 1.0 mm general thickness until the actual build/topology is
resolved. Layer labels do not turn occupied layers into dedicated planes.

## Complete U36 local-stage correction

Move only U36/L1/C40–C43/R81–R83, preserving exact fields, numbered local pads,
layers, source circuits, protection/current limits and hardware permission nets.
The [exact ledger](../../mechanical/review/u36-stage-checkpoint-plan.json) is
authoritative: nine poses, fourteen exact retirements and forty-seven additions
against the immutable 50-edge parent SHA-256
`5e07fb866cc059de670e34102045d9dfd88c88f101355fcdbb27253c0ae26e43`.

Retire the four old switching tracks and the two obsolete U36 supply tails,
then the exact eight-item cleanup cohort: the old pad-free FB component
(three tracks and two microvias), one old SYS tail, and two old output-cap vias.
Record exact UUID/signature evidence before cleanup. No global cleanup or
unlisted copper retirement is permitted. Every active previous pad group must
survive. Reconnect both numbered switching nodes, both capacitor banks and
returns, R81's output feed, IC feedback and the enable pull-down.

Use C40 as the nearest input capacitor and C43 as the nearest output capacitor;
their values/MPNs/footprints/nets are unchanged. Bound the nearest input
supply/return centre distances to 3/3.5 mm and output to 4/4 mm; keep the
other bank members within 6/6 mm. These are project geometry guards, not
manufacturer qualification limits. Explicit short local capacitor routes
precede global supply restoration. FB and EN additions stay on B.Cu.
Added copper remains ordinary 0.20 mm; the five new vias are B.Cu–In4.Cu only.

## Selection gate and boundaries

Select only after exact ledger/identity/pose/pad/profile/structure checks,
all 238 parent UUID pad groups retained, all local pin witnesses, independent
47 native/physical opens, exact unchanged 104 intrinsic findings, stable fills,
identical replays, native visual review, isolated faults and the original
three-orphan restoration proof. Preserve the 50-edge parent at its old path.
The selected successor is
`hardware/coupon/rev-a/staging/led-u36-stage-routing-trial-114mm.kicad_pcb`.

The SW2 control boundary remains open; the local EN pull-down is joined.
VLED stays held low at its existing boundary. No mode/window, component,
current limit, rule waiver, firmware or fabrication permission changes.
The [implementation record](../development/bounded-corrections-2026-11-06.md)
documents the successful placement and rejected alternatives. Coupled-return
candidates that severed other supply planes, including explicit ground-spine
experiments, were rejected; their copper is absent from the selected ledger.

Effective-C, power-copper/current, stability/transients, thermal, source/load,
VLED window, HDI/fill/cap, procurement, fit and independent Gate A remain open.
A routing-study selection is not a manufacturing topology adoption or a
statement that this unbuilt board works.
