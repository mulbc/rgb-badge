<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0157: PAIR07 exact VLED capture continuation

Date: 2026-11-15
Status: Accepted for ignored additive feasibility; no successor selected.

Use only ADR 0153's immutable selected 29-open source. ADR 0155's native
read-only screen finds an exact supported capture at PAIR07.4 VLED,
(74.825,15.650) mm. PAIR07 remains exact NTLJD3119CTBG with its unchanged
manufacturer-checked pin map: S2 pin 4, G2 pin 5, D1 pin 6; no row assignment,
local pad, side, pose, source copper or current/default-off function changes.
The cached onsemi NTLJD3119C/D Rev. 6 April 2024 pin drawing remains the source.

Test exactly one 0.30/0.10 mm B/In4 microvia and one aligned 0.30/0.10 mm
In3/In4 microvia at that actual pad centre. The first via must physically touch
PAIR07.4. Screen every actual foreign/no-net/mechanical copper layer, board
edge, source hole and candidate interaction under ADR 0147's narrowly bounded
supported-span model and independent actual-hole audit. Refill and require all
217 original physical groups before continuing. An unfinished capture is not
a terminal join, and a zone name alone is not a supply contact.

Then allow only additive 0.20 mm VLED routing through actual same-net groups
or individually filled plane components with native copper witnesses. Preserve
every live group after each filled join. New VLED track length is bounded to
120 mm. Use supported outer adjacent 0.30/0.10 mm microvias and mechanical
0.50/0.30 mm In2/In3 buried vias only. No source retirement/move, new centre
microvia, width exception, native rule/profile change or voltage/current raise.

A selected successor must preserve all 217 source groups and all 19,396 source
items/types, reduce matching native/physical opens below 29, retain the exact
original 104 findings under the existing U48/U52 transforms, and pass complete
additive/contact/hole/replay/inverse/orphan/fault/source/visual gates. The CAD
bridge is not VLED current-capacity, switch/return/timing, thermal or fabrication
qualification. Every electrical/part/HDI/stack/process/fit/Gate A hold remains;
zero opens is unfinished and fabrication prohibited.

Preserve the literal source value `NTLJD3119CTBG_TRIAL_ONLY`, absence of an
MPN field and its provisional paired-row status. Do not rename that value, add
an MPN, change the BOM or infer canonical row-package approval from this study.
