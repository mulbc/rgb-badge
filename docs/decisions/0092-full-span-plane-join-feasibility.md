<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0092: Full-span switch routing and plane-bridge feasibility

Date: 2026-11-06
Status: Accepted for bounded feasibility and exact 43-open successor validation.

## Context and decision

The active zero-open goal is at the validated ADR 0091 44-open checkpoint.
The additive search considers adjacent blind-via steps and a provisional
mechanical centre transition. It does not yet consider a complete plated
through-hole transition, although sixteen 0.50/0.30 mm through vias already
exist and the ADR 0090 planning stack explicitly retains that geometry.

Clarify ADR 0091: a newly added full-span F.Cu–B.Cu plated through via may use
exactly 0.50 mm capture / 0.30 mm drill, preserving the existing nominal
0.10 mm ring and mechanical-hole floor. The 0.50/0.30 mm buried-via constraint
continues to apply to a separate In2.Cu–In3.Cu transition. Neither permits a
new unsupported central microvia or adopts the provisional supplier stack.

Screen each full-span capture against pads/tracks on all six copper layers,
all existing drilled holes including same-net holes, and board/cutout edges.
Retain part identities, pad geometry, circuits, current/protection/default-off
settings and all previous live pad groups. Require a real new pad-group join
after zone refill; a pad-free artifact or a disconnected same-net plane island
cannot count as progress. Full native DRC must add no finding. Save trials only
in the ignored build tree until an exact ledger, deterministic replay, native
connectivity and fault/source checks support successor selection.

Via-in-pad assembly, solder wicking, fill/cap, finished thickness, plating,
power-copper/current, thermal/USB performance and supplier reliability remain
unqualified. This feasibility decision grants no fabrication permission and
makes no claim about an unbuilt board's operation. Independent Gate A remains
mandatory. The accepted 44-open source stays unchanged during exploration.

## Bounded successor under validation — 2026-11-07

The exact switch-routing ledger retains the immutable 44-open parent and adds
254 ordinary-width tracks, fifteen adjacent outer microvias and two
0.50/0.30 mm full-span vias at SW2.3 and R83.1. No part moves, existing copper
retires, net changes or rule relaxation are authorized. Pin witnesses are
SW2.3–R83.1–U36.5. The long In4.Cu switch route requires explicit APP, battery
and USB-input supply bridges on other layers; all 232 previous pad groups
must survive refill. These added 0.20 mm bridges are CAD continuity only;
current capacity, voltage drop, return paths and thermal performance remain
unqualified and must be reviewed before fabrication. Existing current limits
and all protection/default-off settings remain unchanged.

A trial's misplaced full-span microvias and missed no-net package pads failed
native DRC. They are excluded. Native via type must be set before its layer
pair, and every pad, including no-net/mechanical pads and drilled holes, must
participate in the clearance screen. Native DRC remains the final authority.
The candidate requires exact 104-finding equality, stable replay/fills,
parent groups, source contract, original-orphan and isolated fault checks.
