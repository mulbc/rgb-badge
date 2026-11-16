<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0181: Exact local ground-bridge plane substitution

Date: 2026-11-16
Status: Accepted for ignored contact-preserving feasibility only; no successor selected.

The ADR0180 bus-hop screen finds no complete sample. Native blocker inspection
identifies a local In4 GND staircase and its three-via B→In4→In3→In2 chain.
The selected source already contains GND planes on B and In2. Test whether
those original connected planes preserve every original interface without
this redundant-looking local bridge; redundancy is a hypothesis, not assumed.

Start only from immutable selected 28-open source. Freeze the exact seventeen
GND items enumerated in `build/row2-routing/ground-chain-discovery.json`:
fourteen ordinary 0.20 mm In4 segments spanning (57.450,17.650)–(57.000,18.200)
mm and the original 0.30/0.10 mm vias B/In4 at (57.450,17.650), In3/In4 at
(57.000,18.200), and historical In2/In3 microvia at (57.000,18.200). Verify every
UUID/signature/type and complete native source contact catalog before writing.
No other source item or via may be removed or changed. No part moves/additions,
zone-definition, stack, profile, width or rule changes are authorized.

Require all 216 original pad groups and every retained original copper item/
type, matching native/physical 28 opens and exact original 104 findings, with
no new dangling original item. Every external source-layer copper/pad branch
must remain in original main ground through actual individual filled components;
an In4 outside branch without a replacement rejects the prototype. Both old
endpoint annuli must contact the original respective B/In2 ground-zone UUIDs
with retained main-group copper witnesses after refill. A common net/zone name
alone is insufficient. Three stable native fills, exact byte-identical inverse
restoration of all seventeen items/types/groups/nine zone fills and unchanged
original DRC must pass before using the basis in another scoped study.

This is CAD connectivity only and remains unselected without a complete
subsequent reduction below 28 and full successor source/contact/hole/replay/
inverse/orphan/fault/visual qualification. Removing a historical unsupported
microvia does not qualify the remaining stack or electrical returns. Local
bypass return impedance/noise/thermal behavior still requires engineering and
hardware qualification. No current/temperature/protection/NTC/timer/default-off
or part/HDI/stack/process/fit/Gate A/fabrication hold changes. Zero opens remains
unfinished; fabrication is prohibited.
