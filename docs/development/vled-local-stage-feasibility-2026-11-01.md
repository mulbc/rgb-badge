<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Local VLED stage and exact UART obstruction study

Date: 2026-11-01. **Unselected native geometry, with prior supply-group losses;
not a canonical routing increment or qualified converter.**
[ADR 0077](../decisions/0077-local-vled-stage-connections-feasibility.md) fixes the
thirteen current exact component poses and permits bounded ordinary-width B.Cu
local joins. [ADR 0078](../decisions/0078-local-vled-uart-obstruction-feasibility.md)
subsequently permits only one exact obstructing UART transfer.

The accepted source remains **58 native/physical opens / 104 intrinsic DRC
findings** at SHA-256
`3451177253a021d8706ff818696212afabf539a108f15ef9e5d6921e46435acc`.
The separate [two-part supply/cleanup study](vled-supply-cleanup-feasibility-2026-11-01.md)
retains all 246 accepted groups at 56 opens; its remote passives are a remaining
layout limitation. This study moves all thirteen stage components together.

## Bounded results

| Ignored state | Native opens | Physical-pad opens | Full DRC | Accepted old groups split |
| --- | ---: | ---: | ---: | ---: |
| ADR 0074 full-stage input | 72 | 69 | 118 | 3 |
| Initial local B.Cu screen | 62 | 59 | 118 | 2 |
| Exact UART transfer | 62 | 59 | 118 | 2 |
| Post-transfer local screen | 60 | 57 | 118 | 2 |

All 118 findings remain exactly the input stage's 104 intrinsic clearances,
six vacated dangling tracks and eight vacated dangling vias. There is no new
finding. Both SYS and VLED old-group losses persist: fewer physical opens alone
is not sufficient for selection. No old power copper is cleaned up here.

The final candidate preserves all **257 input-stage physical pad groups**, every
other input copper item, all 483 poses/exact parts/local pads/fields, zones,
outline, nets, stack, electrical settings and rule/profile files. The feedback
midpoint's earlier accepted group is restored. Local feedback-to-IC and
output-bank connections remain incomplete.

## Local screen and actual obstruction

The initial finite screen accepts ten joins using sixteen 0.20 mm B.Cu tracks.
Each pair has a 5 mm new-track bound and each net a 25 mm bound. Direct paths,
orthogonal elbows and x/y doglegs use a 0.05 mm coordinate grid with ±2 mm
excursions. Native foreign-net shapes screen the unchanged 0.20 mm clearance;
a fill follows every prospective addition and rejects any split of an input
stage group. Original ground cluster membership is preserved, but does not
qualify a low-inductance converter return.

There are 1,008 evaluated paths: 529 exceed a length bound, 469 are blocked and
ten are accepted. All length-compliant output-C46 (171), feedback-IC (108) and
VINA-bypass (141) candidates cross the same UART0_TX B.Cu segment from
(31.05,19.50) to (47.70,19.50) mm. This is a concrete obstruction in the fixed
pose; the finite screen does not establish impossibility of other topologies.
The output-bank direct path is blocked by C47.2; its doglegs exceed 5 mm.

## Exact UART transfer

Read-only source/current contact inventories show that the obstructing segment
contacts only its left retained B.Cu approach and its right In4.Cu/B.Cu via.
That via's only other contact is the retained In3.Cu/In4.Cu via at the same
coordinate. Both retired items are accepted additions, absent from the frozen
215-edge source. These are not new original-source deletion exceptions.

The private transfer retires those two exact items, adds one 0.30/0.10 mm
In4.Cu/B.Cu via at the left endpoint and two collinear **0.20 mm In4.Cu tracks**
with calculated combined length **16.65 mm**. The right retained lower via and
left retained B.Cu approach remain connected. No new narrow track is added;
the retired long B.Cu track was 0.12 mm. All current groups and the entire DRC
inventory survive before repeating the local screen.

The repeat adds four more B.Cu tracks, joining U37.4 to C46.1 and U37.1 to C63.1.
The latter uses a calculated 4.3 mm dogleg around C46's ground land. Ten earlier
joins remain unchanged. The final exact plan therefore has twenty new local
B.Cu tracks, two new UART In4.Cu tracks and one new adjacent via, with exactly
two UART retirements. Both local switching paths from the stage input remain.
The IC feedback path and inter-bank output connection still fail this finite
screen. Global supply reconnection is outside this policy.

## Evidence and replay

The [plan](../../mechanical/review/vled-local-stage-plan-2026-11-01.json) pins the
full-stage input, exact additions/retirements, frozen/current UART contacts and
remaining old-group losses. The [validation record](../../mechanical/review/vled-local-stage-validation-2026-11-01.json)
contains obstruction counts and shortest witnesses, every selected path, exact
native/physical counts, an independent audit and six native CLI rejection
cases. Raw complete candidate attempts remain in the ignored build directories.
Three filled files and two final exact replays are byte-identical. The final
independent audit matches the private candidate's copper inventory and all
257 input groups. The [full native DRC](vled-local-stage-drc-2026-11-01.json)
preserves each finding's type, severity, description, pad/copper identity and
position, with unchanged ignored-check and included-severity settings.

```sh
KPY=/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/3.9/bin/python3
"$KPY" tools/probe-vled-local-switching.py --scope stage --output hardware/coupon/rev-a/build/vled-stage-replay/input/trial.kicad_pcb
"$KPY" tools/probe-vled-local-stage.py --source hardware/coupon/rev-a/build/vled-stage-replay/input/trial.kicad_pcb --output hardware/coupon/rev-a/build/vled-stage-replay/initial-local/trial.kicad_pcb
"$KPY" tools/replay-vled-local-stage.py --source hardware/coupon/rev-a/build/vled-stage-replay/input/trial.kicad_pcb --output hardware/coupon/rev-a/build/vled-stage-replay/with-uart-transfer/trial.kicad_pcb
```

The first local probe retains all copper; the final replay independently pins
the exact transfer and subsequent local routes. Neither tool changes the
canonical checker, selected PCB or source-retirement policy. No vendor PDF or
unsigned manufacturing output is redistributed.

Suitable power widths/loops, local decoupling effectiveness, control-ground/
PGND and feedback returns, exact capacitor lands/order codes/effective
capacitance, electrical/thermal/EMI/process/assembly/fit qualification and
independent Gate A remain open. The current, protection, boot/programming dark
state, EN pull-down and display-interlock requirements do not change.
Further work should restore the two old supply groups and investigate the two
remaining local paths with exact contact and geometry evidence.
