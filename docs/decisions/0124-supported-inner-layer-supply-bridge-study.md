<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0124: Supported inner-layer supply-bridge study

Date: 2026-11-12
Status: Selected for the exact validated 33-open gauge successor; other trials remain unselected.

Continue independently from the immutable selected 34-open source, SHA-256
`92f942e46281475cbdadf6e9a0ad7a0d531e38c3032f85a4206bbf9e9bc1fccd`.
The ordinary additive search normally disables In2.Cu movement as a heuristic
preference. The coupled CC1 experiment demonstrates that explicit supported
central transfers can expose additional geometric paths. This does not adopt
any rejected CC1 candidate or relax a design rule.

Permit ignored additive exploration on VLED, +BAT_GAUGE_SW, +3V3_USB and GND,
including ordinary 0.20 mm tracks on In2.Cu. Every endpoint must be an actual
pad/copper contact or an individually filled polygon with a native same-group
copper witness. Retain every original part, pose, net, copper item and all 222
live groups after every refill. Any split rejects the transaction. Do not
introduce a new centre microvia: In2/In3 transitions remain 0.50/0.30 mm buried
vias, adjacent outer spans remain 0.30/0.10 mm, and an optional complete F/B
via remains 0.50/0.30 mm. All original clearance, hole and edge limits apply.
Different drill sizes cannot be stacked at one point to waive native warnings.

A search hit is not selected progress. Require an exact additive ledger,
matching native/physical count below 34, exact unchanged 104 findings, stable
independent replays/refills, all preceding groups, source/fault checks and
visual review before adoption. General narrowing, source retirement, footprint
moves, circuit changes and current-limit increases are outside this study.
Existing current limits and every protection/default-off boundary remain fixed.

These narrow bridges are CAD continuity only. Ground-return quality, current
capacity, voltage drop, thermal performance, controlled stack, 557 historical
centre microvias, assembly/fit and independent Gate A remain unresolved.
No hardware measurement, electrical qualification or fabrication is authorized.

## Bounded switched-gauge candidate

The independent search finds a +BAT_GAUGE_SW join merging the three-pad
SW2.7/U46.1/C39.1 group with C64.1/R101.1/R102.1. U35.2/3 remains a separate
two-pad supply group. Freeze the exact candidate in
`mechanical/review/gauge-supply-routing-plan.json`: 105 ordinary 0.20 mm tracks
and nine supported vias, no source retirements or pose changes. Calculated new
track length is 39.560971250 mm. Native/physical count is 33 with every one of
the 222 original groups retained and exact unchanged 104 findings. These
preliminary passes authorize only exact replay and successor validation.

The cached TI TCA9517A SCPS245E, October 2025, page 4 Figure 4-1/Table 4-1,
visually confirms DGK pin 1 as VCCA and pins 2/3 as SCLA/SDAA. All parts,
local bypass/pull-up wiring and the existing printed switch terminal map are
retained. No pin/net/land or packaging substitution is involved. Final
selection still requires deterministic replays/refills, counterfactual removal,
native faults, current source checks and visual review. Gauge-device power,
current/return/bus performance and all independent Gate A holds remain open.


## Selected successor

The [implementation review](../development/gauge-supply-routing-2026-11-12.md)
selects the exact 114-item additive gauge join: 33 native/physical opens,
all 222 preceding groups, exact 104 findings, two byte-identical independent
replays with stable fills, eleven native faults, 32 source checks and visual
review. Counterfactual removal restores every parent group and exact filled
geometry/DRC; cached collinear vertices differ in serialization only. Every
parent source byte remains unchanged. U35 supply and all electrical, process,
controlled-stack/fit and independent Gate A requirements remain open.
