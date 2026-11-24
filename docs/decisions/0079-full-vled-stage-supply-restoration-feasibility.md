<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0079: Full VLED stage supply restoration feasibility

Date: 2026-11-01
Status: Ignored additive search only; no canonical reconnection or retirement.

The ADR 0077/0078 exact full-stage replay has 60 native / 57 physical opens,
retains all 257 stage-input groups, but still splits two earlier accepted SYS/
VLED groups. Its three SYS pad clusters comprise the original seven-pad supply,
new U37.1/C63.1 and new U37.10/11/C44.1/C45.1. Its local VLED output and outer
capacitor/divider clusters also remain separate from the original distribution.
Use exact replay SHA-256
`5aa4dff127f623453b6a7c2d032ddc1062ef47f152ffffca476e3051ece85cf2`.

A read-only screen rejects direct reuse of ADR 0075's complete supply inventory:
47 items are individually clear but twelve clash with the new EN pull-down
route or transferred UART. Do not selectively import a disconnected subset or
move those newly established local connections implicitly.

Permit ignored ordinary-width additive global restoration only on
+SYS_APP_IN_DRAFT and VLED, connecting the fixed thirteen-stage pads to the
largest current pad cluster of each net. Preserve all current copper, including
both switching paths, twenty local tracks and the exact UART transfer, all 483
poses/parts/local pads/metadata, zones, profile/rules and electrical settings.
Keep 0.20 mm tracks, 0.20 mm clearance and 0.30/0.10 mm adjacent-layer microvias;
no new narrow copper, removal, source/pose change or extra net is permitted.
Bound new global track length to 25 mm per net, reporting both new global and
combined local/global lengths. This is only a geometric search limit, not
power-path or bypass-loop approval.

Use finite 0.05 mm native-grid searches with at most 600,000 expanded nodes per
attempt. An In2 grid-step exclusion may be compared, but endpoint leads on In2
must be reported explicitly rather than claiming no new In2 copper. After each
join, fill and require every current physical pad group to survive; reject
collateral ground, signal or supply splits regardless of aggregate open count.
Report all routes/rejections, accepted old-group losses and complete physical/
native counts. A complete restoration must independently prove all 246 accepted
58-edge groups, exact inventory/geometry/settings and full native DRC.

Old power-copper cleanup is outside this policy. Any full-stage retirement,
canonical placement/DRC normalization or source adoption requires a separate
exact independent catalog and all standing replay/fault/source/original-orphan
checks. Local output-bank and IC feedback paths, suitable power geometry,
capacitor part/land/order-code/effective capacitance, quiet return layout,
electrical/thermal/EMI/process/assembly/fit and independent Gate A remain open.
No current, protection, EN pull-down, display-interlock or firmware change is
included; fabrication remains prohibited.

## Recorded result

The [native study](../development/vled-restored-stage-feasibility-2026-11-01.md)
records complete restoration of all 246 accepted groups and retention of all
257 stage-input groups at 55 native / 52 physical opens. The feedback path,
short C47 return and outer VLED join retain the exact 118 input-stage findings.
Deterministic replays/stable fills, independent audit, replay rejection and
original-orphan checks pass. Old dangling power copper and source adoption
remain outside the selected scope; canonical source stays at 58 opens.
