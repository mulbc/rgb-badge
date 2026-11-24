<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Full VLED stage supply and return restoration

Date: 2026-11-01. **Unselected native geometry; no fabricated or measured board.**
[ADR 0079](../decisions/0079-full-vled-stage-supply-restoration-feasibility.md)
bounds ordinary-width global supply restoration. [ADR 0080](../decisions/0080-c47-return-and-feedback-combination-feasibility.md)
permits only the exact finer feedback path and a short C47 return connection.

## Complete old-group restoration

The ignored thirteen-part converter candidate now retains **all 246 accepted
58-edge physical pad groups and all 257 full-stage input groups**, with
**55 native / 52 physical-pad opens**. SYS, VLED and feedback-midpoint old-group
losses are all restored. The accepted source stays at **58 native/physical
opens / 104 intrinsic findings**, SHA-256
`3451177253a021d8706ff818696212afabf539a108f15ef9e5d6921e46435acc`.
No canonical pose, retirement or fabrication output is selected.

The ignored result still has exactly **118** DRC findings: the original 104
intrinsic clearances plus six dangling tracks/eight dangling vias at vacated
component locations. All finding identities, descriptions, severity and
coordinates match the earlier full-stage input. Old padless copper explains
the remaining native/physical count gap. Obsolete power-copper cleanup requires
its own exact bounded policy; this study does not remove it.

| State | Native opens | Physical-pad opens | Accepted groups split |
| --- | ---: | ---: | ---: |
| Accepted source | 58 | 58 | 0 |
| Full-stage local/UART candidate | 60 | 57 | 2 |
| First global supply search | 57 | 54 | 1 |
| Exact feedback combination | 56 | 53 | 1 |
| Short C47 return | 56 | 53 | 1 |
| Outer VLED restoration | 55 | 52 | 0 |

The source poses and all 483 exact identities/local pads/fields stay fixed from
the full-stage seed. All other current copper, zones, stack, outline, nets,
profile/rules and current/protection/enable settings survive. The only private retirements of retained input items are the two exact UART
additions already covered by ADR 0078.

## Why the additions differ from the two-part trial

Read-only comparison finds twelve collisions in the older pair-only supply
inventory: ten SYS pieces clash with the new EN pull-down connection, while a
VLED In4 lead/via clash with the transferred UART. All 59 pieces are screened;
47 individually clear pieces are not imported as a disconnected partial route.

A bounded 0.05 mm native-grid search, at most 600,000 expansions per attempt,
restores both SYS clusters and the inner VLED output cluster. Each fill retains
every current physical pad group. Its attempted outer VLED joins are rejected
because C47.2 becomes isolated from main ground, even though the intended VLED
pads join. Those failed states remain explicit negative evidence.

The finer B.Cu feedback search examines 299 nodes and finds eight 0.20 mm tracks
with calculated total length **4.564213562 mm**, below the unchanged 5 mm pair
bound. It joins U37.3 to R86.1/R85.2, preserving all current groups and full DRC.
A native-shape comparison and subsequent filled/full-DRC combination retain
the existing supply/local/UART routes. This is a CAD connection, not feedback
noise or converter stability qualification.

The return screen finds a three-via adjacent **B/In4/In3/In2** stack at
**(48.60,20.15) mm**, using unchanged 0.30/0.10 mm diameter/drill, plus a
**0.20 mm-long, 0.20 mm-wide B.Cu lead** from C47.2 at (48.60,20.35) mm. The
lower via contacts actual filled In2 ground; all old groups and the full
118-finding inventory survive. Stacked via-in-pad process/assembly suitability
remains unqualified. Ground cluster membership is not a low-inductance-return
or thermal/EMI result.

Only after that return passes does the outer VLED search repeat. It retains
the earlier global length budget, accepts the outer-bank join and independently
restores every accepted source group. The two capacitor banks now connect
through the supply distribution; no additional local B.Cu bank-to-bank path is
claimed. The earlier finite B.Cu-only bank path remains unsuccessful.

## Inventory and calculated lengths

Relative to the exact full-stage input, the final candidate adds **95 items:
78 tracks and 17 adjacent microvias**, and retires only the two UART items.
This comprises the previous 23-item local/UART inventory, sixty global supply
items, eight feedback tracks and four C47 return items. The six switching tracks
already in the full-stage input remain unchanged. Final copper count is 18,437.

| Net | New global track length | Combined new track length from stage input |
| --- | ---: | ---: |
| +SYS_APP_IN_DRAFT | 12.428536888 mm | 20.489058062 mm |
| VLED | 14.345304624 mm | 20.728809357 mm |

Both global and combined supply lengths remain below 25 mm/net. Other new
lengths are UART 16.65 mm, VLED_FB 5.714213562 mm including its earlier divider
join, FB midpoint 1.15 mm, EN 3.1 mm and ground 0.2 mm. Every new track is
0.20 mm wide. No current-capacity approval follows from these geometric bounds.

The search excludes In2 grid steps, **not endpoint leads**. The final inventory
includes one 0.813941030 mm VLED In2 endpoint segment from (58.45,20.60) to
(59.00,20.00) mm. Native filled connectivity proves ground retention; this
candidate must not be described as containing no new In2 copper.

## Independent evidence and remaining work

The [exact restored plan](../../mechanical/review/vled-restored-stage-plan-2026-11-01.json)
pins every addition/retirement and the full-stage input. The [validation record](../../mechanical/review/vled-restored-stage-validation-2026-11-01.json)
contains finite-search results and rejected ground-split witnesses, feedback
paths, return attempts, independent private/replay audits, three filled states,
six current replay rejection cases and the old dangling-contact inventory.
Two exact restored replays and all three filled PCB files are byte-identical,
SHA-256 `7604b4807de28c1058afdb2c297df2053690fd83f0861517f813318fb92ca2f7`.
The earlier local phase remains byte-identical at its original hash.

The [full native DRC](vled-restored-stage-drc-2026-11-01.json) retains all 118
input-stage findings and unchanged exclusions/severity settings. Restoring the
three original retired +3V3_APP microvias produces exactly those three known
additional dangling-via findings (121 total), with all 246 old groups and
55/52 counts retained. Those original orphans remain distinct from the newly
vacated component copper; no new source-orphan exception is granted.

```sh
KPY=/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/3.9/bin/python3
"$KPY" tools/probe-vled-local-switching.py --scope stage --output hardware/coupon/rev-a/build/vled-restored-replay/input/trial.kicad_pcb
"$KPY" tools/replay-vled-local-stage.py --phase restored --source hardware/coupon/rev-a/build/vled-restored-replay/input/trial.kicad_pcb --output hardware/coupon/rev-a/build/vled-restored-replay/restored/trial.kicad_pcb
```

Further work includes exact old-copper cleanup and independent source-adoption
policy/checks, L1/U36 locality, suitable power widths/loops, quiet control/PGND/
feedback returns, exact capacitor lands/order codes/effective capacitance,
electrical/thermal/EMI/process/assembly/fit qualification and independent Gate A.
No current, protection, firmware, pull-down or hardware display-interlock change
is selected. Fabrication remains prohibited. Vendor PDFs and raw PCB probes
remain ignored local evidence.
