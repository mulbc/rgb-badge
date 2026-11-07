<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0064: Exact accepted colour-segment rework feasibility

Date: 2026-10-29
Status: Ignored feasibility only; no accepted-addition retirement selected.

The PAIR01 ground escape is obstructed by the already accepted COL_09_R In4
replacement segment from (60.90, 3.25) to (78.60, 3.25) mm, width 0.20 mm.
This is an accepted addition, not an original 215-edge source item. Existing
checkpoint and replacement catalogs prohibit its canonical retirement.

Permit ignored feasibility trials on only this exact segment: retain its two
In4 endpoint contacts and all direct same-layer contacts, replacing at most
2 mm of its original interval with one full-width layer excursion using adjacent microvia stacks (at most four
adjacent pairs per endpoint). Limit vertical displacement to 1 mm and replacement length to the
retired segment plus 2 mm. Preserve every other original/accepted copper item,
pose, zone, completed physical group and prior electrical/geometry exception.
Ground routing remains 0.20 mm; clearance remains 0.20 mm and adjacent microvias
0.30/0.10 mm. No new narrow neck or electrical-setting change is permitted.

The exact TLC59581RTQT and its constant-current output pin map remain covered
by [TI TLC59581/82 Rev. A](https://www.ti.com/lit/ds/symlink/tlc59581.pdf).
The source WDFN pair and all pad geometry/nets stay fixed. No current, transient,
return, thermal or manufacturing qualification follows from geometric feasibility.

Canonical adoption requires a separate exact accepted-addition retirement policy,
independent derivation of the current segment's contacts, a frozen checkpoint
witness proving its prior presence, and preservation of every other accepted
item/group. The older original-source replacement and its contacts must remain
independently checked through the exact new substitution. Require lower native/
physical counts, unchanged 104 full findings, stable fills/replay, source/fault
checks and the original-orphan proof. Until those requirements pass, the frozen
accepted segment must remain in the canonical plan. Independent Gate A remains
mandatory before fabrication.

## Finite screens

The 2026-10-29 symmetric endpoint screens find no geometrically clear transfer
among 1,380 In3 dogleg cases, 1,380 B.Cu dogleg cases and 230 straight In1/F
stack cases. No accepted-addition retirement is selected or implemented. These
finite results do not establish impossibility; the current 60-edge board retains
the protected COL_09_R segment unchanged.
