<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0096: Ground-plane substitution for the TMP390 output exit

Date: 2026-11-07
Status: Selected as a 39-open CAD successor; fabrication prohibited.

U39.4 and U39.6 are both TEMP_OK in the unchanged source, matching the two
open-drain outputs in the visually read TI pin table. An accepted B.Cu GND
strap through the IC body blocks their local full-width connection. Study
substituting the already defined B.Cu ground plane for this exact five-track
GND chain (all 0.20 mm B.Cu):

- (57.550,10.850)–(57.550,16.300) mm
- (57.550,16.300)–(57.500,16.300) mm
- (57.500,16.300)–(57.500,16.400) mm
- (57.500,16.400)–(57.450,16.400) mm
- (57.450,16.400)–(57.450,17.650) mm

Retain all boundary copper, including the bottom ground via and intersecting
accepted diagonal ground lead. Require a single individually filled B.Cu GND
component touching every original external boundary contact and both chain
endpoints, not just a shared zone identifier. Retain all preceding live pad
groups and every other copper item, including ADR 0094's exact return. Do not
change zone definitions, parts, poses, nets, current limits, temperature
programming, NTC/protection, firmware or default-disabled permissions.

Add only ordinary 0.20 mm B.Cu TEMP_OK routing between the existing U39.4/6
pads. No new via or additional retirement is authorized by this study. Full
native/physical agreement, exact unchanged 104 findings, complete source and
boundary-plane evidence, replay/fills and fault checks precede selection.
Any failed ground, pad-group, net or DRC check rejects the candidate. Ground
impedance/noise, thermal/supply completeness and electrical/process/fit/Gate A
qualification remain open; this is CAD feasibility, never fabrication release.

The selected source has 39 native/physical opens and exact unchanged 104
findings. Three new ordinary TEMP_OK tracks total 2.330 mm; the retired ground
chain totals 6.900 mm. All 228 preceding groups and 216 preceding additions
survive, with one individual filled ground component retaining all five
boundary contacts and both endpoint disks. Stable replays/fills, eighteen
fault guards, source checks and native visual review pass. See the
[checkpoint record](../development/remaining-routing-2026-11-07.md) for hashes
and the inherited retirement-proof scope. No part moves or vias are added.
