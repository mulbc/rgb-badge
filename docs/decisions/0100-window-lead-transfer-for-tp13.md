<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0100: Bounded window-permission lead transfer for TP13

Date: 2026-11-07
Status: Unselected feasibility; ADR 0101 later selects an additive TP13 join.

The fixed U55 VLED_ENABLE_CANDIDATE output faces an existing VLED_WINDOW_OK
B.Cu lead. Study replacing only these exact ordinary 0.20 mm B.Cu tracks:

- (25.500,21.300)–(25.500,14.050) mm
- (26.250,21.375)–(25.500,21.300) mm

Retain a B.Cu feed from (25.500,14.050) to a new adjacent B.Cu/In4.Cu capture
near (25.500,20.100) mm, and return from In4.Cu through a second capture at
U55.6 (26.250,21.375) mm. New microvias remain 0.30/0.10 mm and span only
B.Cu/In4.Cu. Bound the In4.Cu detour to x=24.5–28.0 / y=19.5–22.0 mm and
5 mm of added inner trace. Do not add a skipped-layer or central transition.
Preserve the original outer B.Cu endpoints and every original external
boundary contact, including the existing upper via and numbered lower pad.
Every other accepted copper item and all prior live pad groups must survive.

Only a completed TP13 join under ADR 0098 can justify selection. Its existing
1.0 mm circular test land, fields, net, orientation, mask/paste and B.Cu layer
remain unchanged, with at most 5 mm of new ordinary B.Cu lead. No other part
moves. Preserve the exact SN74LVC2G08DCUR logic and all source/sink pin nets;
this reroute neither bypasses the VLED window nor changes any threshold,
current/protection setting, hardware permission, default or firmware.

Record the exact new routing and complete source-contact ledger before
selection. Require unchanged full native 104 findings, independent native/
physical reduction, all preceding groups/copper outside this exact cohort,
source contracts, stable replay/fills, isolated faults and native visual
review. Probe access/loading, signal/return, stack/process/fit and independent
Gate A remain unqualified; no fabrication release follows this study.

The initial locality screen also finds fixed courtyard/heartbeat obstructions
beyond the window lead. Permit the same exact window replacement to support
an ordinary-width ADR 0091 connection to TP13 at its unchanged position,
instead of relocating the land. An additional adjacent B.Cu/In4.Cu output
escape may be studied at (25.400,20.875) mm. This does not select a partial
escape or remove the requirement for an actual complete TP13 join, retained
external window contacts, unchanged DRC and all successor validation. A
longer signal route must record its calculated length and unqualified loading.

The partial escape preserves all 226 source groups at 38 opens but has one
additional dangling VLED_ENABLE_CANDIDATE microvia warning. A 2.5-million-node
search stops at its bound; a six-million bound exhausts its sampled graph
after 4,282,705 expansions, and reverse search exhausts after 2,574. No
complete fixed-TP13 join is established. These finite results do not prove
wider routing impossible. The selected ADR 0101 source retains the original
window lead and adopts none of this experiment's retirements or replacement
vias. Exact pad-centre capture and local probe relocation resolve the join
in that separate validated continuation.
