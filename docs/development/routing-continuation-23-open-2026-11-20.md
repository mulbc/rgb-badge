<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Routing continuation from the 23-open checkpoint

These are native CAD geometry studies, not measurements or electrical
qualification. The selected board remains
`hardware/coupon/rev-a/staging/led-pair01-supply-routing-trial-114mm.kicad_pcb`,
SHA-256 `9574949d6bd56caa6f79b9db78af3531b0150cfba1f110d727c829effcaf62b3`.
Its independently qualified native/physical count is 23. No study below
writes or selects a successor PCB. The zero-open goal remains unfinished.

ADRs0245–0267 and the corresponding requirements additions authorize the
bounded discovery. The portable
[evidence index](../../mechanical/review/routing-continuation-23-open-discovery.json)
records ignored local evidence paths, SHA-256 digests and result metrics.
The build directory is local evidence, not a fabrication output.

## Row pull-up studies

The bottom-side R9 and R10/R12/R13 screens test 112504 poses in total.
None has the complete required pad/courtyard/lead clearance. A separate
39204-pose front-side R9 screen finds 118 supply-only poses, but a complete
gate connection is still missing. Native original-contact cataloguing
identifies the exact private R9 leaf; no source retirement is selected.

The aligned and staggered lower-access graphs exhaust10171 nodes with
no legal escape. A short COL_05_B layer hop is geometrically possible:
one exact original In4 track would be replaced by7.077817459 mm of
conductor and two supported In3/In4 microvias, preserving all seven
original outside contacts. However, no complete gate-to-centre route is
found. Two core graphs exhaust3271/3924 nodes. A subsequent rescreen
without the proposed colour capture still finds the same92 qualified
centre candidates and no complete gateway. The colour hop is unselected;
there is no partial gate or colour replacement in the selected board.

## Sensor gateway and actual supply escape

The fixed-placement U39 searches exhaust their reachable graphs without
a supply join. Exact native blockers motivate a coordinated, same-side
gateway with these translations only:

| Reference | Exact part | Translation |
| --- | --- | --- |
| U39 | TMP390A2DRLR | +0.375 mm x |
| R89 | ERJ2RKF2151X | +0.100 mm x |
| R90 | ERJ2RKF1402X | +0.400 mm x |

All numbered pads, orientations, part identities, fields, thresholds and
other 480 placements remain fixed. The
[frozen gateway](../../mechanical/review/sensor-gateway-discovery.json)
contains exact six-item typed retirement signatures, their original
outside-contact catalogue and every proposed replacement conductor.
It restores both selectors, TEMP_OK, programming and ground paths.

The native in-memory fill preserves all 211 old physical pad groups and
all 19343 retained attached source copper items, with no orphan copper.
Native and physical counts remain23; main ground/VLED/USB groups remain
197/38/32 pads. Actual bottom courtyards and the new supported-via hole
checks pass. The calculated C50-to-U39 supply-pad distance improves from
3.816022144 to3.795082344 mm; this is geometry, not bypass acceptance.
C51 belongs to U40; its remote bypass limitation is not resolved here.
Thermal reservation and all programming distances remain within the
previously bounded study requirements.

A coarse graph, a100000-state fine graph and a25434-state multiscale
graph find no supply join. A separate native shape-derived search finds
a real 1.287438738 mm ordinary 0.20 mm B.Cu escape from actual U39.5 to
(56.400,14.750). Its integer-coordinate conductor is saved in the
[escape record](../../mechanical/review/sensor-supply-escape-discovery.json).
It follows circumscribed tangent polylines around actual pad/track
geometry, screened against native copper. The 0.00025 mm numerical guard
is not a process capability or qualification. The waypoint is not an
electrical pad, and this partial conductor closes no connection.

The repository [replay check](../../tools/check-sensor-gateway-discovery.py)
reconstructs both frozen records in memory. It checks source hashes,
exact part fields/local pads, independent absolute pad translations,
typed retirements, original contact catalogue, all new external copper
clearances, actual moved courtyards, holes, every original group and
retained attached copper. It verifies 23 matching opens, zero orphans
and unchanged source bytes, writing no PCB. Full CLI DRC/replay/inverse
qualification of a successor has not been performed.

The seeded 0.025 mm graph exhausts 6980 nodes and 7019 blocked capture
positions. Its reachable area hits study boundaries; the wider ADR0266
search carries the exact seed and physical length while retaining the
same physical and source-preservation rules. It exhausts 145182 nodes,
58103 capture positions and 1618 clear captures without a join. ADR0267
therefore permits one further supported In3/In4 transition and ordinary
In3 routing, with full mutual/source hole checks; that graph exhausts 109256 nodes/74336 captures (3339 clear) without a
join. The source-preserving gateway/escape remain unselected. A complete join must reach
an actual conductor in the original 32-pad main USB supply group, refill
to 22 matching opens/USB33 and preserve every old group and retained
copper before a separate successor prototype can be authorized.

All 42 existing portable source checks pass again. The native repository
replay also passes with the frozen licensed records and external Cu screen.
Raw evidence is under `hardware/coupon/rev-a/build/pair01-supply-routing/`
(`fixed-sensor/continuation-source-checks.json` and
`fixed-sensor/public-gateway-check.log`).

## Remaining acceptance

No material from these partial studies is adopted into canonical CAD.
The selected board retains its original 104 findings and 554 unsupported
historical centre microvias. Complete routing, exact-part/electrical,
bypass/return/thermal, controlled-stack/process/assembly/fit qualification
and independent Gate A remain open. Fabrication remains prohibited.

The study checkpoint `e7ceb71a02eb6dee68b97f33abb63fe94269badb` is pushed.
Both hosted runs pass: [44829780125](https://github.com/mulbc/rgb-badge/actions/runs/44829780125)
and [44829767193](https://github.com/mulbc/rgb-badge/actions/runs/44829767193).
ADR0268 subsequently finds a separate additive PAIR03 join; its qualification
and selection are recorded in the [22-open checkpoint](pair03-supply-routing-2026-11-20.md).
