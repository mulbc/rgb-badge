<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0078: Exact UART obstruction transfer feasibility

Date: 2026-11-01
Status: Ignored finite transfer experiment; no accepted-source replacement.

ADR 0077's B.Cu-only screen obtains ten local joins but every length-compliant
output-C46, feedback-IC and VINA candidate crosses the same accepted UART0_TX
B.Cu segment. Investigate an exact In4.Cu transfer in the ignored local-stage
trial SHA-256 `f8b103cea1733b59a240996cf33bdb875a5d342956e4370b13af3c8723d5c3c1`.

Permit private retirement of only two previously accepted additions:

- UART0_TX, 0.12 mm B.Cu, (31.05,19.50) → (47.70,19.50) mm.
- UART0_TX, 0.30/0.10 mm In4.Cu/B.Cu microvia at (47.70,19.50) mm.

Read-only native inventory proves the segment contacts only the retained B.Cu
track (31.075,22.575) → (31.05,19.50) mm and that top via. The via contacts only
the retired segment on B.Cu and the retained In3.Cu/In4.Cu via at its coordinate.
Neither retired item is in the frozen 215-edge source. Preserve both retained
interfaces, every other copper item and every current physical pad group.

Add exactly one 0.30/0.10 mm adjacent In4.Cu/B.Cu microvia at (31.05,19.50) mm
and only ordinary 0.20 mm In4.Cu tracks to the retained right-hand In3.Cu/In4.Cu
via. Require unchanged 0.20 mm foreign-net clearance, at most 20.65 mm new track
(original 16.65 mm plus 4 mm), fixed endpoints and finite direct/orthogonal
0.05 mm doglegs within ±2 mm. Reject any new split after native fill or any new
full DRC finding. No new narrow track, other removal/pose/zone, via geometry,
protection, current/enable/firmware or capacitor change is permitted.

If a complete transfer passes, rerun only the ADR 0077 local-pair screen in a
private descendant retaining the exact transfer. The existing switching paths,
all local-stage geometry and all current groups remain fixed. Any resulting
local join still grants no global reconnection, source-adoption/retirement or
converter qualification exception. Native/physical counts, frozen/current exact
contacts, added/removed signatures and full DRC must be recorded. All electrical,
process, assembly, part/order-code and independent Gate A holds remain open;
fabrication remains prohibited.

## Recorded result

The [native study](../development/vled-local-stage-feasibility-2026-11-01.md)
records ten initial local joins, a contact-preserving ordinary-width UART
transfer and two additional local joins. The ignored full-stage candidate has
60 native / 57 physical opens, the exact input-stage 118 findings and two
remaining accepted SYS/VLED group losses. Deterministic replay/stable fills,
independent native audit and CLI rejection checks pass. No canonical source
move or retirement is selected; further supply/local-path and qualification
work remains open.
