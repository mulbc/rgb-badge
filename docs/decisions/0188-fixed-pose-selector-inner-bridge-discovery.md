<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0188: Fixed-pose selector inner bridge discovery

Date: 2026-11-16
Status: Accepted for read-only complete-interface discovery only.

All eleven ADR0187 full-height left detours meet the adjacent ROW_SEL_06 B
route. Keep every original part/pose and power-stage/bypass geometry fixed.
Read-only test an inner-layer replacement for only the lower ROW_SEL_08 B
bridge, rather than shifting that column into its neighbor.

Freeze the exact immutable 28-open source catalog before omitting: original
B vertical db361ff2-8ade-5ab0-bd15-6c1bbad753f9; only ROW_SEL_08 B tracks with
both endpoints inside x=56.200–56.900 / y=16.250–17.650 mm; and the two original
0.30/0.10 mm outer microvias e71af429-046e-5f47-bee3-886a38e0c014 (B/In4) and
51a1212f-c8c1-52b5-9db6-d60ec6200e0e (In3/In4) at (56.900,17.650) mm.
The source lower port has only one outside In3 track,
401b8b44-9f6a-5db2-9684-00f87af760dd, (56.900,17.650)–(57.850,17.650) mm;
there is no outside In4 branch. Preserve this actual interface and all original
B outside contacts. No arbitrary other source copper, via or part omission.

Retain the original upper B column geometry from (56.200,10.600) mm to a
sampled upper endpoint x=56.200 / y=11.000–13.900 mm at 0.050 mm steps.
Screen supported aligned 0.30/0.10 mm B/In4 and In3/In4 captures there. The
later selector bridge must reach the exact retained lower In3 wire interface;
its route remains unresolved by clear upper captures. New source widths stay
ordinary 0.20 mm, all actual foreign/no-net copper, source edge and full-board
ADR0147 hole checks remain unchanged.

Mutually screen ADR0187's fixed U39 VDD ordinary two-segment B escapes ≤2.250
mm at x=56.100–56.250 / capture y=14.100–14.650 mm, with B/In4 captures and
optional aligned In3/In4 access. Both actual selector and power copper/holes
must clear each other and every original source obstacle. Write no PCB.

A clear cohort is incomplete until the original three-pad selector group and
original USB supply group join together with all 216 source groups/interfaces,
matching reduced native/physical count, exact104 and all source/contact/hole/
replay/inverse/orphan/fault/visual gates under a separately frozen prototype.
All C49/converter/thermal/bypass geometry stays fixed; C51/U40 locality remains
an explicit unresolved qualification finding. No current/threshold/protection/
NTC/timer/default-off/part/HDI/stack/process/fit/Gate A or fabrication hold change.
