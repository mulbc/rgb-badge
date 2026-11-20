<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# PAIR01 front ground continuation — 2026-11-20

Selected CAD checkpoint: 25 native and independently physical opens.
All validation gates below pass.
This is an unbuilt trial board and is not a fabrication release.

The ADR0225 two-part front template reaches 24 opens but splits R6's original
VLED supply group after refill. It is rejected. Its apparent pre-refill plane
contact is not evidence of a preserved connection. The subsequent bounded
short supply/capture searches did not produce a qualifying connection.
R71's independent edge/lower-access studies also produce no accepted route.
Exact source/evidence digests are in
`mechanical/review/row-zero-front-discovery.json`; ignored raw results remain
under `hardware/coupon/rev-a/build/r11-front-routing/`.

ADR0226 preserves R6 and its entire supply group by moving only the original
trial PAIR01 package from B (75.750,3.750) mm / 180 degrees to F
(76.100,4.300) mm / 270 degrees, with a native top-bottom flip. No symbol,
numbered net, BOM or package substitution is made. The independent pad
transform is x'=79.850-y / y'=80.050-x mm. Package qualification is still open.

The exact ledger retires 32 private ROW_SEL_00 items, four obsolete ROW_00_A
items and two gate straps. It retains the shared selector junction/via and
both LED-half row connections. It adds 59 ordinary 0.20 mm conductors and
two supported 0.30/0.10 mm F/In1 accesses. The selector restores the original
three-pad group via a 7.913657 mm route; the row restores all eighteen pads.
The ground lead joins PAIR01.1 to retained main GND at (82.600,5.250) mm.
The original separate gate resistor and PAIR01 VLED opens remain explicit.
No new supply conductor or central/through transition is added.

The selected checkpoint has 25 matching native/physical opens, 213 groups
on 188 nets and all 214 source groups intact. Main GND grows from 196 to 197
pads, main VLED remains 37, all 19,319 retained source Cu stay attached, all
61 new Cu attach and there are no orphans. Removing the obsolete selector
centre access reduces the historical unsupported centre-microvia count from
556 to 555; every remaining one remains held. New via-in-pad transitions are
CAD geometry only and remain subject to filled/capped-via/process approval.

Validation evidence belongs under
`hardware/coupon/rev-a/build/pair01-front-ground-routing/`:

- Exact raw source/new Cu declarations, all 483 part identities/fields/pads,
  independent absolute pad transforms and unchanged profiles/rules/structure.
- All 259 actual front courtyards, new full-board hole checks and native DRC.
- Exact original 104 intrinsic findings; only the twelve item occurrences
  belonging to the six moved PAIR01 pad-pad findings map back to their
  original B coordinates/layer text. External findings cannot normalize.
- Four stable exploratory fills and two independent three-fill replays,
  each producing `ec0bf7fc842f3dd4f9210e7667925cffc388d3d82906e44c5bde4e10f428ee88`.
- Full inverse yields the original 26-open source bytes on all three refills,
  with all 214 source groups equal and all nine integer filled-zone XORs empty.
- All 28 deliberate fault rejections, eight shared hole controls and two front
  courtyard controls pass. All 40 portable source workflow commands pass.
- Reviewed native F/B/In1 copper exports and actual F/B courtyard overlays,
  with exact image digests in the ignored visual manifest.

The duplicate-part control exposed an initial checker omission: a reference
map alone hid duplicate footprint instances. The final checker also asserts
actual footprint count. Moving only one old selector via did not disconnect
the restored selector because it has other real retained same-net contacts;
that proposed negative control was rejected as ineffective. The final
physical control removes the actual new selector route and must prove
separate native terminal groups before exercising the connectivity guard.

The goal remains zero opens with every original live group preserved. All
current/default-off/protection limits and all electrical, return, thermal,
stack, process, optical/fit and independent Gate A holds remain open.
