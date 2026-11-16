<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0168: Complete row-two and selector passive exchange prototype

Date: 2026-11-15
Status: Accepted for ignored complete-circuit feasibility; no successor selected.

Start only from the immutable selected 29-open inverter source. The first
complete ADR 0167 sample freezes R8 ERJ2RKF1001X at (72.575,8.000) mm / +90
on B and R37 ERJ2RKF1003X at (72.200,9.500) mm / 180 on B. R8 VLED pad 1
stays exactly (72.575,8.500); its gate pad moves to (72.575,7.500). R37 pads
become ROW_SEL_15 at (72.700,9.500) and GND at (71.700,9.500). Independently
verify all pad coordinates using original integer transforms. No part/value/
field/local pad/net or other pose changes; keep literal paired-row trial status.

Retire exactly the nineteen B.Cu ROW_SEL_15 segments in the full native source
contact catalog SHA-256
`173455e43b0e21ab5b4b63e2d233e2e14082243c1b3d6cc49f3e59833c55700f`.
The scope runs from original R37.1 to (73.550,9.049999) mm. No old GND, VLED,
other selector/colour trace or via may be retired. Restore every original
retained external selector contact with one ordinary 0.20 mm B.Cu lead from
new R37.1 to that retained boundary, calculated length 0.961770 mm. The source
catalog's six distinct retained track witnesses must all physically touch the
replacement. Restore the original three-pad selector group together.

Add the two supported 0.30/0.10 mm B/In4 gate captures at (72.575,7.500) and
(74.825,7.500) mm and their ordinary 0.20 mm In4 ROW_GATE_02 lead, 2.250 mm.
Retain all original R8 supply copper and actual fixed-pad contacts. New R37.2
must attach to the original main GND group through actual filled copper and
retained witnesses. All four original direct GND copper contacts at the old
R37 position stay unchanged and must independently remain in that same live
ground group; no dangling branch may be excused. Original ground source unit
42 with witness `8e95d641-8b62-5a97-be89-437598eff082` is the preliminary
contact; recompute actual individual filled components after refill.

Require exact all-layer foreign/no-net/mechanical copper, mutual holes under
ADR 0147's bounded supported-span model, source 0.500 mm edge minimum and
courtyard checks. Keep default 0.20 mm routing and every profile/rule value.
The prototype has nineteen retirements/four additions, no new centre microvia,
and no unrelated source change. A selector cut alone is never progress.

Selection needs matching native/physical reduction below 29, complete four-pad
ROW_GATE_02 plus original GND/VLED/ROW_SEL_15 continuity and every one of the
217 original groups/items except the exact retired leaf. Preserve all 483
parts/fields/local pads and exact original 104 finding payloads under only
existing U48/U52 transforms. Complete source/contact/hole/replay/inverse/orphan/
fault/source/visual gates precede selection. No current/protection/NTC/timer/
fail-safe/default-off change, part approval or fabrication release is inferred.
Every electrical/part/timing/return/thermal/HDI/stack/process/fit/Gate A hold
remains; zero opens is unfinished.
