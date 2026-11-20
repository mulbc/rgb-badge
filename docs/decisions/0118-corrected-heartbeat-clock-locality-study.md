<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0118: Study corrected heartbeat-clock locality

Date: 2026-11-12
Status: Accepted for read-only geometry study; no placement change selected.

Continue the zero-open goal from ADR 0117's corrected 35-open board,
SHA-256 `3967bb66e89e0005f6859ce78a766b4536d06883b76fce130e75a6fdeefaf96e`.
The first additive control pass selects no join. U48's clock output and U49's
corrected clock input remain far apart, so test whether exact U49 can fit
within 8 mm of U48 before proposing further copper changes.

The first screen may move an in-memory U49 geometry proxy through finite
0.1 mm positions and 90-degree orientations. Retain its exact corrected RSE
pin mapping and all fixed source components/copper in the obstruction screen.
Compare actual convex back-side courtyards, actual native pad/track/via shapes
at ordinary 0.2 mm clearance, and the unchanged 0.5 mm copper-edge constraint.
Do not save a PCB or alter any source file. Filled zones are excluded from
this preliminary obstruction screen and must be checked by native refills in
any later routing trial. Finite misses do not prove that placement is impossible.

A clear sampled pose alone cannot be selected. Before a later PCB migration,
record its exact U49/support/bypass poses, original contacts, bounded obsolete
copper cohort and replacement paths. Preserve the fail-safe R108 clear
pull-down, every functional group, accepted converter geometry, exact parts,
current/protection/permission boundaries and original DRC finding identities.
Any replacement of an ADR 0117 addition must be explicitly inventoried and
justified, rather than silently exempted from copper retention. Existing DSF
clock-neck exceptions remain bounded to their exact pins and lengths; general
narrowing and new unsupported centre microvias remain forbidden.

The controlled stack, electrical/process/fit qualification, 557 historical
centre vias and independent Gate A still prohibit fabrication. This study is
neither a hardware measurement nor approval to enable the display.

## Recorded screen

The [read-only screen](../development/corrected-clock-locality-2026-11-12.md)
finds no clear sampled pose among 80,324. All 9,232 courtyard-clear samples fail
pad/copper or edge screening. The corrected PCB bytes remain unchanged at
35 opens. No placement, retirement or route is authorized by this result.
