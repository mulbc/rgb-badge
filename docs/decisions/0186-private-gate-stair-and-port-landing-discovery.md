<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0186: Read-only local gate stairs and existing supply-port landing

Date: 2026-11-16
Status: Accepted for read-only complete-interface discovery only.

The wider placement screen finds existing row-gate B stair paths through the
candidate sensor pin region. Read-only test one exact four-part core, with
C51 separately relocated near its actual U40 buffer under ADR0185:
U39 (55.025,18.350) mm / 180°; R89 ERJ2RKF2151X (57.600,17.000) mm / 270°;
R90 ERJ2RKF1402X (53.000,18.350) mm / 90°; C50 GRM155R71C104KA88D
(57.685,19.295) mm / 0°. U39/C50 MPNs, all local pads/fields/pin nets, source
thermal reservation/4 mm discovery movement and ≤3 mm programming/ground
bounds remain unchanged. C50's USB pad 1 stays exactly (57.285,19.295) mm.
Keep its entire original supply copper, including the In4 feed and source
microvias, and test a 0.20 mm B neck from new U39 VDD (54.285,18.350) to the
existing C51 USB source port (54.485,18.350) mm. No new supply via is needed.

Prospectively omit only the original seventeen sensor B tracks, verified
seventeen-item GND bridge, the one old C51 B supply leaf track
311027e9-3797-5f1d-bf17-703362aedca5, and these exact local B stair cohorts:
ROW_GATE_10 tracks with both endpoints inside x=56.400–56.750 / y=16.950–18.150
mm; ROW_GATE_12 tracks with both endpoints inside x=55.950–56.650 /
y=17.250–18.600 mm. Freeze every UUID/signature and complete native source
contact catalog before any in-memory omission. Do not omit any original via,
long gate bus or other source item. This is a smaller capacitor-port omission
than ADR0185's prospective six-item leaf; retain the other five USB items.

Test ordinary 0.20 mm B replacements for gate 10 through
(56.400,16.950)→(56.425,16.950)→(56.425,18.150)→(56.750,18.150) mm and gate 12
through (55.950,17.250)→(55.950,17.350)→(55.025,17.350)→(55.025,19.350)→
(56.550,19.350)→(56.550,18.600)→(56.650,18.600) mm. Require every old outside
contact to touch the replacement physically on its original layer, plus
actual moved/fixed courtyard, all retained foreign/no-net and mutual source
copper and edge checks. No source rule/width, skipped layer or centre microvia.

Write no PCB. A clear core does not establish passive placement, original
filled ground, hot/cold/output routing or complete circuit continuity. Any
later implementation must separately freeze all five poses and original
interfaces, retain all 216 groups and matching reduced native/physical/exact104
with full source/contact/hole/replay/inverse/orphan/fault/visual qualification.
No exact part, threshold/current/thermal-error/protection/NTC/timer/default-off/
HDI/stack/process/fit/Gate A or fabrication hold changes. Zero opens is unfinished.
