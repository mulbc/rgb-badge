<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0151: Complete local inverter and bypass prototype

Date: 2026-11-14
Status: Accepted for ignored complete-circuit feasibility; no successor selected.

Start only from ADR 0142's immutable 30-open selected source, SHA-256
`90db778d8e44b2c71ab5e1f5d8a1c586ee71c25d46892b1406c4792ac7720abd`.
Use ADR 0150's first complete local bypass cohort: exact U48 SN74LVC1G04DSFR
at (110.000,28.150) mm / 270 degrees on B, exact C67 GRM155R71C104KA88D at
(109.450,29.950) mm / 180 degrees on B. Preserve every local pad/net/field,
NC assignment, every other part/pose, all 19,369 source copper items and their
native types, rules/profiles and board/zone/net structures. Retire nothing.
Independently check all moved pads against integer source-coordinate rotation
and translation. Catalog every direct original support-copper contact before
implementation; any later obsolete-leaf cleanup needs a separate exact scope.

Freeze four existing-rule U48 B.Cu 0.12 mm necks and B/In4 0.30/0.10 mm captures:
pin 2 (110.000,27.750)→(110.000,27.250), pin 4
(110.350,28.550)→(110.450,28.550), pin 3
(110.350,27.750)→(110.450,27.750), pin 6
(109.650,28.550)→(109.550,28.550), all coordinates in mm. Each neck intersects
the moved U48 courtyard and is individually ≤0.750 mm; no width rule changes.
Add B/In4 captures at C67.1 (109.850,29.950) and C67.2 (109.050,29.950).
Add 0.20 mm In4 supply from U48's pin-6 capture to C67.1; add 0.20 mm In4 return
from U48's pin-3 capture through (109.050,27.750) to C67.2. This exact cohort
has thirteen added items: seven tracks and six supported adjacent microvias.
Keep the supply path ≤2.5 mm and local return ≤4 mm. Screen all native foreign,
no-net/mechanical copper, holes, mutual candidate items and board edges using
ADR 0147's bounded supported-span prefilter. No new centre microvia.

Fill and independently report every old group loss, physical/native opens and
complete findings. Placement alone is not restoration: the original APP/GND
source groups, all 218 original groups and original external branch interfaces
must survive in any accepted successor. Old support stubs and unfinished new
captures may create declared prototype findings; none is accepted or waived.
Next ordinary-width routing may join only DISPLAY_HEARTBEAT, HEARTBEAT_FALL_CLK,
+3V3_APP and GND through actual same-net group/filled-zone witnesses. Preserve
all existing groups after each join and bound new signal paths to 120 mm each.
Full original-finding comparison must independently normalize only the exact
U48 rigid pose change, in addition to ADR 0136's frozen U52 transform. No C67
finding allowance. Native/physical reduction below 30, exact complete ledgers,
independent hole audit, stable independent replays, inverse/orphan proofs,
native fault guards, source checks and visual review precede selection.

No electrical limits, protection/NTC/timers, hardware fail-safe or default-off
behavior changes. Read-only template clearance is not bypass/return/timing or
power-integrity qualification. All electrical/part/process/stack/fit/Gate A
holds, historical centre-via holds and fabrication prohibition remain in force.
