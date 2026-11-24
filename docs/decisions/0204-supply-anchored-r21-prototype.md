<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0204: Supply-anchored R21 prototype

Date: 2026-11-16
Status: Accepted for exact ignored complete-circuit feasibility only.

ADR0203 finds no main supply target near the small translated poses. The
native R21 inventory instead identifies a private 10.750 mm B gate leaf
ending at an existing supported outer via near connected VLED resistor R18.
Keep exact R21 ERJ2RKF1001X and every other component/value/net unchanged.
Screen exact R21 at (59.300,5.600) mm, 0 degrees: VLED pad 1
(58.800,5.600), ROW_GATE_15 pad 2 (59.800,5.600) mm. No other part moves. The initial y=5.750 mm candidate meets the retained
VLED rail at y=6.200 mm; the frozen y=5.600 mm pose clears that rail and
the retained upper gate route without changing either source item.

Freeze full source contacts/signatures/types before retiring only these two
original 0.20 mm B ROW_GATE_15 tracks:

- d25db091-cafe-51d4-b153-6ad69339ab4e: (66.750,5.000)–(56.750,5.000) mm.
- e10a833e-5a12-5e19-b8b4-85f4670985f6: (66.750,5.750)–(66.750,5.000) mm.

Retain original B/In4 via cb9294d1-c465-51d9-8d7a-b4344a70b4fc at
(56.750,5.000) and every original outside source-layer contact. Add only
three ordinary 0.20 mm B tracks: VLED (57.750,5.750)–(58.800,5.600),
ROW_GATE_15 (59.800,5.600)–(59.800,5.000)–(56.750,5.000) mm. The
supply lead must touch actual connected R18.1 copper; no plane is invented.
The replacement gate leaf is 3.650 mm, shorter than its original 10.750 mm.
No new via, unsupported transition or source-rule exception.

Before writing an ignored prototype, native-check every mutual/new/source
foreign or no-net copper shape, exact part/local-pad/net identity, source
edge, fixed courtyards and all outside contacts. Refill and require all 216
original groups, matching native/physical opens below 28 and exact original
104 findings. Incomplete gate restoration or any rail split rejects the trial.

Selection requires full independent source/absolute-pad/type/profile/contact/
hole/replay/inverse/orphan/fault/visual gates. No current/resistance/protection/
default-off/part/electrical/thermal/stack/process/fit/Gate A or fabrication
hold changes. A source merge is not a fabrication release.
