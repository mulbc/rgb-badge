<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0114: Local row pull-up replacement of obsolete remote branches

Date: 2026-11-10
Status: Accepted for ignored feasibility; no successor selected.

ADR 0113's two-millimetre screens select no join. Place R11 beside PAIR06,
or R21 beside PAIR16, independently, instead of retaining a remote pull-up
location. Each remains exact ERJ2RKF1001X / 1 kΩ, with unchanged local lands,
fields and pin nets. The controlled source is the selected 36-open board,
SHA-256 `a24e9220226b77411ae8e8baea5cd629ce0fea8a97c377a708510d6791c2e439`.

Freeze the exact source inventory in
`mechanical/review/local-pullup-source-2026-11-10.json` before trial. A gate
net must have exactly the resistor pad 2 and its own paired-MOSFET gate/drain
lands; no other logical pad may be disconnected. Retire only that net's
catalogued original tracks/vias, preserving its two local B.Cu package
straps. Re-derive the complete original contact inventory independently.
The removed remote branches may not leave dangling vias or stubs. Preserve
every other copper item, accepted addition, live pad group and net identity.

Keep the resistor centre within 3 mm of its own MOSFET centre, with cardinal
orientation. New gate and VLED leads must each use ordinary 0.20 mm B.Cu
tracks of at most 3 mm, with no new vias. The gate lead must touch the
retained local gate network and moved pad 2; the VLED lead must touch pad 1
and the same MOSFET's already-connected VLED pad 4. Preserve the original
pull-up association, resistance, transistor geometry and all limits and
protection/default settings. Check complete courtyards and foreign copper.

No source successor is selected without native/physical open reduction,
every old group/accepted addition retained, exact original-contact and
retirement-scope proof, unchanged exact 104 native findings, deterministic
replay, fault/source checks and visual review. These local geometry trials
do not qualify pull-up transients, supply current, thermal/process/fit or
hardware operation. Independent Gate A still precedes fabrication.

The first coarse R11 local candidate joins VLED but separates the existing
PAIR07.1/PAIR08.1 ground return, leaving 37 opens. It is rejected as a
successor. Permit an ignored ordinary-width additive ground restoration
using ADR 0092's standard adjacent 0.30/0.10 mm transitions and, only if
needed, its 0.50/0.30 mm In2.Cu–In3.Cu buried transition. No new unsupported
central microvia or other retirement is permitted. Preserve every new gate/
VLED join and all old groups; both displaced ground pads must return to the
original main-ground group, not merely merge with each other. Native/physical
reduction and the full exact-DRC/scope/replay/fault/visual gate still precede
selection. These returns are unqualified CAD geometry only.

The fine R11 placements retain the same displaced ground islands. Permit a
local adjacent In4.Cu/B.Cu transfer of its new VLED lead, with at most two
0.30/0.10 mm microvias and 3 mm combined ordinary-width lead. Keep the
moved resistor, retained local gate straps and every new gate connection.
The transfer must restore both former ground members and preserve all
source groups and exact foreign copper/net identities. No other retirement
or width exception is authorized; full successor gates remain mandatory.

Outcome: no full localization is selected. R11's coarse and finer local
variants join VLED but separate PAIR07.1/PAIR08.1; R21 finds no complete
local gate lead within the sampled placement. A ground search on the R11
partial candidate connects U38/U52 but does not restore the displaced returns.
The selective restoration in ADR 0115 retains all original gate routing
except its single terminal leaf and avoids the local ground losses.
