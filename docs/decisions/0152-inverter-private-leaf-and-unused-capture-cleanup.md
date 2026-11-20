<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0152: Inverter obsolete leaf and unused capture cleanup

Date: 2026-11-14
Status: Accepted for ignored successor qualification; no board selected.

ADR 0151's isolated prototype has a real clock join and restored local APP
supply after native routing, while both 500,001-node heartbeat-input searches
stop at their bounds. The unfinished input preparation is unnecessary for a
clock-only successor. Before considering selection, remove only these two
new prototype items: pin-2 neck `a6ca30a3-8d06-5e6b-9ab6-1b239591522b`
and its unused B/In4 capture `4d2d9a69-a2ec-5e9d-bb75-273d41e55eb5`.
U48.2 remains DISPLAY_HEARTBEAT and disconnected as in the selected parent;
no no-connect designation or logic change is permitted.

The exact old APP supply leaf loses its U48 courtyard width exception and
physical endpoint after relocation. Retire only original 0.12 mm B track
`15606914-5a77-520f-891e-15e122b1afc8` from (63.850,0.650) to (63.300,0.650)
mm and original B/In4 0.30/0.10 mm microvia
`0f1184fa-3b7b-5bbc-9b14-39fb0d58d95c` at (63.300,0.650) mm. Complete native
source contact catalog SHA-256:
`14f1ba870bd60e713df9154d16359da549668ea3ff4d74f269431402363282cb`.
Keep both contacted external In4 tracks `60e01f83-f71a-5075-a05f-7bb6b2aa0ac9`
and `7ffffe04-6468-5761-a7bc-1fb7684213d0`, their actual contact with source
zone `626b02a6-8846-59f7-b7df-a75c78241fe0`, and every other source item.
Independently prove each external branch still joins the original APP group
through actual retained copper/filled-zone witnesses; pad count alone is not
sufficient. No old ground or C67 supply item is retired.

Keep the exact ADR 0151 U48/C67 poses and all other declared local additions
and successful ordinary-width clock/supply routes. After cleanup require all
218 original selected-source groups, actual native/physical reduction below
30, exact original 104 findings under the independently verified U48 and prior
U52 transforms, all retained item types/signatures, native external-contact
and hole audits, stable independent replays, inverse-source/orphan proof,
native fault/source/visual gates before any selection. Any failed restoration
or new dangling/width/clearance finding rejects this successor.

All current/protection/NTC/timer/fail-safe/default-off boundaries and every
part/electrical/timing/return/thermal/HDI/stack/process/fit/Gate A hold remain.
No fabrication release or hardware performance claim is authorized.
