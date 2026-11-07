<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# VLED pair supply restoration and exact obsolete-copper study

Date: 2026-11-01. **Unselected native geometry experiment, not an operating
converter, canonical routing increment or fabrication release.** ADRs
[0075](../decisions/0075-vled-pair-supply-restoration-feasibility.md) and
[0076](../decisions/0076-obsolete-u37-copper-cleanup-feasibility.md) bound the work.
The accepted board remains **58 native/physical opens and 104 intrinsic DRC
findings**, SHA-256
`3451177253a021d8706ff818696212afabf539a108f15ef9e5d6921e46435acc`.

## Result

The ignored two-part U37/L2 move can preserve all **246** accepted physical pad
groups while connecting both local switching nets. Supply restoration and an
exact 23-item obsolete-copper cleanup produce **56 native / 56 physical opens**
and exactly the original **104 intrinsic clearance findings**, with no new
dangling findings. Three successive filled PCB files and two independent replays
are byte-identical, SHA-256
`fbea2f0430ec77d84da598f9d13a8434aa002d61efc0fe5334a40bfa662b3010`.
Only U37 and L2 move; all 483 footprints retain exact identities, local pad
geometry, fields and layers. All other poses, zones, nets, stack, outline,
settings and rule/profile files remain fixed.

This is a connectivity result from KiCad 10.0.6, not a current-capacity or
converter-loop qualification. The other eleven stage parts remain at their
accepted poses; their locality, feedback and return paths still require
coordinated work. Exact capacitor-land/order-code findings, L1/U36, effective
capacitance, electrical/thermal/EMI/process/assembly/fit qualification and
independent Gate A remain open. No protection, current limit, enable pull-down,
firmware or display-interlock behavior changes.

## Additive supply restoration

The input is ADR 0074's deterministic pair probe, SHA-256
`9e244a34515d42cf3b5bdf7b1bba52c55fcdd4ce319c8fbeb86159c1f202828b`.
It already contains two 3.215685425 mm B.Cu switching paths with no switching
vias. New SYS/VLED connections use 47 ordinary 0.20 mm track segments and twelve
0.30/0.10 mm adjacent-layer microvias at unchanged 0.20 mm clearance.

| Net | New track length (calculated) | Tracks | Adjacent vias |
| --- | ---: | ---: | ---: |
| +SYS_APP_IN_DRAFT | 9.849282295 mm | 30 | 5 |
| VLED | 14.869653529 mm | 17 | 7 |

The first forward VLED search splits two old ground groups and is rejected.
Layer-cost variants restore all groups. The retained search directory's
`no-in2` name describes **grid steps only**: endpoint leads may still use In2.
The selected replay has two short SYS In2 segments (0.050000000 and
0.070710678 mm), plus a **0.813941030 mm VLED In2 endpoint lead** from
(58.45, 20.60) to (59.00, 20.00) mm. It must not be described as containing no
new In2 copper. Full native connectivity, rather than a layer-name heuristic,
checks old ground retention. No ground repair is added.

With all old copper retained this intermediate is 58 native / 56 physical
opens and 110 DRC findings: the 104 intrinsic clearances plus three dangling
tracks and three dangling vias at the former U37 site.

## Bounded obsolete-copper inventory

The local simulation removes newly dangling old copper only within the ADR
0076 window. Seven inspected states remove 21 items, then stop at two long
F.Cu SYS branches outside the boundary. Each branch now contacts only the shared
SYS bus; in the frozen 58-edge source it additionally contacts its own vacated
via. The ADR's exact leaf extension precedes their private removal. The shared
bus remains untouched.

The complete retirement cohort is **five tracks and eighteen adjacent vias**:
three vacated B.Cu ties/stubs, two SYS F.Cu branches and four obsolete via stacks.
Eight VLED stack vias originate in the frozen 215-edge source; the other fifteen
items are previously accepted additions. Origin is explicit; this is not a
blanket original-orphan exception. Every other accepted copper item survives:
18,315 retained accepted items plus 65 new items (six switching tracks and the
59 supply items) give 18,380 final copper items. Every cleanup state retains all
246 old groups and the exact intrinsic clearance identities.

The [exact plan](../../mechanical/review/vled-supply-cleanup-plan-2026-11-01.json)
records each signature, UUID, origin, removal round, same-net direct contacts,
filled-zone contacts, boundary findings and leaf frozen/current contacts.
It grants no retirement exception to the canonical source checker.

## Validation and replay

The [validation record](../../mechanical/review/vled-supply-cleanup-validation-2026-11-01.json)
includes both replay hashes, three stable fills, native and independent
physical-pad counts, the independent audit, four CLI rejection cases and four
native fault cases. Missing new supply copper, restored original VLED copper,
an unapproved U36 move and altered U37 pad geometry are rejected. CLI checks
reject input overwrite, output outside ignored build, wrong source and changed
plan before producing a candidate.

The [full native DRC](vled-supply-cleanup-drc-2026-11-01.json) retains the exact
104 finding descriptions, severities and pad identities. Only the positions of
findings wholly within the unchanged U37 package translate to its exact recorded
pose; every other coordinate stays exact. Original ignored-check and severity
settings are unchanged. The canonical DRC policy is not modified.

A separate restoration fixture adds the three original retired +3V3_APP
microvias back. Full DRC becomes exactly 104 intrinsic clearances plus those
three known dangling-via findings; all old groups and 56 physical/native opens
survive. This proof remains distinct from the new 23-item obsolete cohort.

From the repository root, using KiCad's bundled Python:

```sh
KPY=/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/3.9/bin/python3
"$KPY" tools/probe-vled-local-switching.py --scope pair --output hardware/coupon/rev-a/build/vled-replay/pair/trial.kicad_pcb
"$KPY" tools/probe-vled-supply-cleanup.py --source hardware/coupon/rev-a/build/vled-replay/pair/trial.kicad_pcb --output hardware/coupon/rev-a/build/vled-replay/restored/trial.kicad_pcb
"$KPY" tools/check-vled-supply-cleanup-probe.py --board hardware/coupon/rev-a/build/vled-replay/restored/trial.kicad_pcb
```

Raw search/cleanup/replay evidence remains ignored under
`hardware/coupon/rev-a/build/vled-{supply,cleanup,supply-replay}-2026-11-01/`.
Search outputs and vendor PDFs are not redistributed. Further coordinated local
bypass/return and power-path work precedes any decision to adopt this pose.
