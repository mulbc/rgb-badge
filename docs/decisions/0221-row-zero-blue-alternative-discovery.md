<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0221: Independent row-zero blue alternative discovery

Date: 2026-11-19
Status: Accepted for read-only native discovery only.

The exact red-wire alternatives remain incomplete: the In3 graph exhausts,
its local In3 capture screen has no pair, and the B detour/refinement finds
no complete path. None of their source retirements or new vias is selected.

Independently consider only exact COL_09_B wire
`7d3b740c-3700-5948-afb0-514468ad24d2`, ordinary 0.20 mm In4 from
(77.200,3.750) to (59.500,3.750) mm. Native contact audit identifies only
supported In3/In4 via `a09dda19-2aee-5861-a6a0-b0298904401b` and original
In4 vertical `ebd4e3e3-c6ab-58df-ba62-dfd03aefe713` as outside interfaces,
with no pad, intermediate branch or zone contact. Keep them both, the entire
red net and every other source item/part/rule fixed.

Read-only repeat ADR0218's reachable-group gate capture discovery with only
this blue wire prospectively omitted. If a supported B/In4 + In3/In4 gate
pair is clear, screen an ordinary local In3 hop around it: new supported
In3/In4 colour captures on y=3.750 mm, x=73.750–76.250 mm at 0.050 mm
centres, ordinary exact In4 end fragments to both retained source interfaces,
In3 straight/orthogonal detours in y=2.750–4.750 mm, at most 4.5 mm.
Include all mutual copper and full-board hole checks. Add no other retirement,
unsupported transition, smaller feature, part/value/current/function change.
Write no PCB; complete every original group/contact and full successor gate
with reduced matching counts/exact104 before any selection. All qualification,
Gate A and fabrication holds remain unchanged.
