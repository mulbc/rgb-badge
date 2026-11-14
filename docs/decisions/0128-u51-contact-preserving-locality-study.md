<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0128: Bounded contact-preserving U51 placement study

Date: 2026-11-14
Status: Accepted for ignored feasibility only; no successor selected.

The selected board remains the immutable 33-open source
`14f0c49582063bab84ea685a8cec798011eb4cd66389b085a3a47777180a13ce`.
ADR 0127's wider edge grid finds actual endpoints at U52.1 but exhausts its
sampled graph from both sides. Exact fixed-pose adjacent capture screening
finds no clear B/In4 0.30/0.10 mm capture at U51.4 or U52.1.

Permit only an ignored U51 translation within ±0.250 mm in each coordinate,
in 0.025 mm increments (441 poses), preserving its existing orientation and
layer. Retain exact SN74LVC1G11DRYR, fields, pin numbers, local lands and every
original copper item/via type. Keep all other parts/poses, net assignments,
profiles, board/zone outlines and protection/current/default-off settings fixed.
TI SCES487I page 3 identifies DRY pin 4 as Y; PDF pages 31–32 show DRY0006A
and the existing 0.5 mm pitch/0.6 mm row spacing land geometry. The current
manufacturer PDF is cached verbatim in the ignored reference directory.

Screen all moved copper lands against actual foreign copper on their copper
layers, mechanical/no-net lands and board edges, and moved courtyards against
other same-side parts. Screen a supported B/In4 0.30/0.10 mm capture overlapping
U51.4 against actual copper and every hole, without new centre microvias or
narrower traces. A proxy or unfinished capture is not a new circuit join.
Before continuation, refill and preserve all 221 source live groups; reject
any lost original group. Native DRC remains the exact original 104 findings
for any selected successor; an unfinished capture's dangling finding is not
an acceptance waiver.

Final selection requires a real U51.4–U52.1 join, native/physical count below
33, every original live group and copper item, exact frozen pose/addition
ledger, stable independent replay/refills, isolated faults, source checks and
visual review. No fabrication or powered-operation qualification is implied.

The 441-pose native land screen retains seven geometrically clear poses, but
none has a clear capture overlapping the output land. Extend only this ignored
screen to a capture within 0.750 mm of U51.4, reached through ordinary 0.20 mm
B.Cu copper. Sample the local escape graph at 0.025 mm with actual native
copper/board-edge checks; source end caps must overlap the actual pad by at
least 0.005 mm. A proxy path still requires all original groups and exact DRC
before it can support a completed join. No other source item may change.
