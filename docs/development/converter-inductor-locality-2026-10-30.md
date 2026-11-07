<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Converter-inductor locality screen on the corrected 59-edge board

Date: 2026-10-30. Coupon Rev A is unbuilt. These are first-author native
geometry/source experiments, not hardware measurements. Firmware and electrical
settings are unchanged. No new inductor or converter pose is selected.

[ADR 0054](../decisions/0054-local-converter-inductor-placement-study.md)
permits moving only L1/L2 beside fixed U36/U37, preserving every accepted copper
item, other pose and physical group. The input is the exact corrected 59-edge
board at commit `73a6c26`, SHA-256
`95d7b7679319cdd64f8e22d428bd2a78454b91298ca17432d34ede0c824ab214`.

The owner resupplied `m_dfe252012p.pdf`, SHA-256
`ce259ba611fb3ea196baf60e2c7080a21cd897cdb662bf77552cc842c2b91c3e`.
Its one-page drawing was rendered and visually checked. It confirms exact
DFE252012P-1R0M=P2 and DFE252012P-1R5M=P2 with unchanged 2.8 mm outer land
span, 1.2 mm inner gap and 2.0 mm transverse width. Each project-local land is
0.8 × 2.0 mm at ±1.0 mm. These inductors are nonpolar. No package substitution,
land change or increased current limit follows from this recheck. The current
ratings describe separate inductance-decrease and temperature-rise conditions,
not an enclosure qualification.

TI TPS631000 Rev C §7.4 and TPS63020 Rev I §10 were re-read, including rendered
layout figures. Their nearby passive placement, short/wide power paths,
feedback separation and return guidance remain requirements for subsequent
engineering review. A long switching-node route is not accepted to improve
an open count. Relevant source URLs remain in ADR 0054; vendor PDFs and rendered
pages stay local and outside Git.

| Part | Existing centre, mm | Existing angle | Fixed converter centre, mm |
|---|---|---|---|
| L1 | (12.000, 7.375) | 180° | U36: (103.125, 5.500) |
| L2 | (16.000, 7.375) | −90° | U37: (93.750, 2.250) |

The initial 0.2 mm four-angle pad/copper screen within 6 mm finds 124 L1 poses
and no L2 poses. That incomplete screen does not establish package fit. Expanding
to an 8 mm radius and checking courtyards rejects all 424 L1 and 14 L2 pad-clear
poses in that four-angle screen; the obstructing courtyard observations include
U2 and SW1.

The final reusable [native screen](../../tools/screen-converter-inductor-locality.py)
uses 0.1 mm centre spacing and 15° orientations within 8 mm of each fixed IC.
It checks actual transformed convex courtyard polygons against other fixed
back-side courtyards, keeps the courtyard inside the board, and checks every
land against native other-net pad/track/via shapes at 0.20 mm clearance and
0.50 mm copper-edge clearance. It excludes filled zones from clearance screening;
full native fill/DRC/group checks would still be required for any surviving pose.

| Final screen | L1 | L2 |
|---|---:|---:|
| Sampled centre/orientation pairs | 481,944 | 481,944 |
| Courtyard outside board | 107,522 | 226,638 |
| Courtyard obstructed | 374,336 | 255,306 |
| Courtyard clear | 86 | 0 |
| Passing courtyard and copper/edge checks | **0** | **0** |

The 86 courtyard-clear L1 poses fail pad/copper or edge checks. No pose advances
to switching-node routing, refill or adoption. This is a finite grid result,
not proof of impossibility between samples, on the other side, or after a
separately authorized coordinated floorplan change. The 8 mm radius is an
exploration bound, not permission to exceed ADR 0054's 5 mm switching-path bound.
Reported pad-centre distances are planning observations, not pad-edge path
lower bounds or routing acceptance.

The exact-integer convex intersection predicate has four host regressions,
including diagonal shapes whose bounding boxes overlap without intersection,
edge touching, winding/large-coordinate invariance and invalid polygon rejection.
A [native oracle](../../tools/test-convex-native.py) compares 2,000 deterministic
rotated rectangle pairs against KiCad polygon collision. The screen rejects
courtyard holes/nonconvex outlines rather than silently applying an invalid
convex test. These checks validate the screening implementation, not hardware.

[Native results](../../mechanical/review/converter-inductor-locality-59-2026-10-30.json),
[native oracle](../../mechanical/review/converter-locality-native-oracle-2026-10-30.json)
and [validation fingerprints](../../mechanical/review/converter-locality-validation-2026-10-30.json)
record inputs and local raw locations. Source bytes remain unchanged by the
screen. Run KiCad Python on `tools/screen-converter-inductor-locality.py
--source PATH --step-iu 100000`; PATH must identify the exact corrected 59-edge
board, including an ignored archived copy extracted from commit `73a6c26`.
Outputs are restricted to ignored build storage.

The follow-on ordinary-width supply/ground search is separate. The original
four-direction GND screen makes no join, and its failures do not prove general
impossibility. The exact preceding open-net report is archived as
`routing-progress-59-before-murata-open-nets.json`; the current report now names
the corrected PCB hash, with the same counts. New supply candidates require
their own complete acceptance evidence under ADR 0070.

The next locality investigation must explicitly address the surrounding fixed
floorplan and nearby capacitors/feedback, with new bounded scope before moving
other components. Electrical/current/thermal/bypass/return/EMI, mechanical and
assembly/process qualification plus independent Gate A remain open. Fabrication
remains prohibited.
