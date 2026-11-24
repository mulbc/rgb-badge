<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0146: Anchored selector-resistor capture screen

Date: 2026-11-14
Status: Accepted for read-only native screening; no successor selected.

ADR 0145's ignored prototype completes ROW_GATE_02 but isolates R37.1 from
its original ROW_SEL_15 group. Its full-board ordinary restoration exhausts
R37's sampled component and reaches the 300,001-node bound in reverse. The
validated source remains ADR 0142's immutable 30-open board.

Screen exact R37 Panasonic ERJ2RKF1003X / 100 kΩ / 1% in 5-degree orientations
about its fixed GND pad-2 centre (66.75,7.25) mm, retaining B side, local lands,
fields and numbered nets. Pad 1 stays ROW_SEL_15. Keep every original direct
copper contact of both pads and each original filled-zone contact, rather than
assuming fixed pad centre preserves connectivity. Check actual same-side
courtyards, native foreign/no-net/mechanical copper and all holes/board edges.
No source copper or rule changes are authorized by this read-only screen.

Use ADR 0145's exact ignored R8/selector prototype as the geometry input.
Read-only test a 0.30/0.10 mm B/In4 capture at each actual new R37.1 centre and,
where clear, an exact shared-hole In3/In4 transition. No new centre microvia or
narrow-width rule. The Panasonic ERJ2R package reference already reviewed for
R8 covers this retained exact resistor family; no part/value substitution or
new manufacturer land pattern is inferred.

Before any relocated PCB, freeze the exact clear pose, integer pad geometry,
source-contact proof and prospective capture cohort in an additional decision
paragraph. All selected 218 original live groups, complete original selector
and pull-up supply groups and the real new gate join must coexist with exact
old findings and full replay/inverse/orphan/native-fault/source/visual gates.
Non-cardinal placement, electrical/default-state/timing/return/thermal/HDI/
stack/process/fit and independent Gate A qualification remain open. No current,
rail, protection, NTC, timer, fail-safe permission or fabrication authority changes.
