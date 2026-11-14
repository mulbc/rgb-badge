<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0115: R11 leaf clearance for a shunt-ground join

Date: 2026-11-10
Status: Selected geometric checkpoint; fabrication remains prohibited.

ADR 0114's partial board exposes a valid ground route from the U38/U52
island. Comparing that route with the complete selected source identifies
only R11's original B.Cu gate leaf as conflicting copper; the original R11
pad 2 also occupies its via capture. Test the existing ADR 0113 exact leaf
replacement with R11 translated (+0.500,0) mm, orientation unchanged at
180 degrees. Retain all other ROW_GATE_05 copper, its original far-end via,
all other component poses and every original pad group/accepted addition.

Replace only the exact 0.20 mm B.Cu ROW_GATE_05 track from (71.750,4.250)
to (72.150,4.250) mm. Restore direct contact from moved R11.2 to that retained
via using an ordinary 0.20 mm B.Cu lead. Keep exact ERJ2RKF1001X / 1 kΩ,
local lands, fields and numbered nets. No VLED connection is required by
this variant: its possible progress is the ground join, with the original
VLED singleton preserved. No other original retirement is permitted.

The proposed ground route is the exact native endpoint route recorded in
ignored `build/zero-open-routing/new-ground-intersections.json`: fourteen
0.20 mm tracks and one 0.30/0.10 mm In4.Cu–B.Cu microvia. It must physically
join the old U38/U52 group to original main ground without cutting any
preceding group or changing retained copper/net identities. No rule, zone,
width, current, protection or new central transition change is permitted.

Selection requires exact historical leaf/contact proof, actual native and
independent physical reduction, all previous groups and accepted additions,
unchanged exact 104 findings, stable ledger/replay, native fault/source checks
and visual review. These are CAD continuity calculations on an unbuilt board;
electrical/return/transient/process/fit qualification and independent Gate A
remain unresolved. Source remains 36 opens until all gates pass.

Before selection, extend both ground captures to the retained via centres,
using two additional 0.195 mm ordinary-width tracks. The search's original
end-cap overlaps establish native continuity but are not the intended final
landings. Keep the same exact source endpoint contacts, and independently
require a new track endpoint at each retained via centre. This avoids relying
on narrow cap-overlap geometry. Recheck full clearance, replay and faults
on the strengthened route; no source/profile exception is introduced.

Selection: the strengthened route reaches 35 native/physical opens and
main ground grows 194→196 pads. Every 224 preceding group and 226 accepted
addition survives, as do all 231 immutable parent groups. Exact unchanged
104 findings, identical canonical/two-replay bytes, three stable fills each,
44 native fault cases, 28 source checks and native B.Cu/In4.Cu visual review
pass. Only the original R11 leaf is retired relative to the 36-open source;
the other 64 experimentally removed gate items are retained.
