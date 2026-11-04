<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# L1/U36 locality after the full VLED cleanup

Recorded: 2026-11-04. [ADR 0082](../decisions/0082-corrected-l1-u36-locality-feasibility.md)
bounds the two finite screens started from the 2026-11-01 cleaned-stage result.
These are native geometry observations, not hardware measurements. No L1/U36
pose or route is selected and no new board is exported.

Both screens use the exact ignored 52-edge PCB, SHA-256
`7c5196b19decc3a4fbaf5724a24aae479a0fdb9c2679706f3cc5f86253992e11`.
It remains byte-unchanged at 52 native/physical opens / 104 intrinsic findings.
The accepted board remains the 58-edge source; no canonical adoption policy,
current limit, protection, firmware or fabrication restriction changes.

## Fixed U36, L1-only screen

U36 remains at (103.125,5.50) mm, 180° B.Cu. Exact TPS631000DRLR and
DFE252012P-1R0M=P2 identities and current local pads remain fixed. L1 samples
0.10 mm positions in an 8 mm radius, every 15°, at unchanged native 0.20 mm
foreign-net and 0.50 mm copper-edge clearance.

| Outcome | Sampled poses |
| --- | ---: |
| Other courtyard obstruction | 374,336 |
| Courtyard outside board | 107,522 |
| Courtyard clear, pad/copper or edge obstruction | 86 |
| Clear courtyard and pads | 0 |
| Total | 481,944 |

All 86 courtyard-clear failures have a recorded first pad/edge rejection
witness, including the source item's UUID/net/reference when copper blocks it.
This repeats the historical fixed-regulator approach on the corrected, cleaned
candidate rather than treating the earlier 59-edge result as automatically
applicable after thirteen other parts move.

## Compact U36/L1 template screen

U36 samples 0.125 mm offsets in dx = -12…+2 mm, dy = -4.5…+2.5 mm, within a
12 mm displacement radius, at cardinal rotations. L1 sits 2.65/2.90/3.15/3.40 mm
outward from its actual native LX side, with -0.25/0/+0.25 mm tangential offsets.
Its numbered lands align with U36.3/LX1 and U36.2/LX2 using actual B-side native
pad coordinates. A proposed node would use a 0.60 mm outward lead and direct
fanout, 0.20 mm B.Cu width, at most 5 mm/node, without a new via or retirement.

| Exclusive outcome | Templates |
| --- | ---: |
| IC external courtyard obstruction | 259,008 |
| IC courtyard outside board | 12,672 |
| IC pad/copper or edge obstruction | 30,348 |
| Mutual IC/coil courtyard obstruction | 117 |
| Coil external courtyard obstruction | 351 |
| Coil courtyard outside board | 144 |
| Clear short-switching template | 0 |
| Total | 302,640 |

Only 51 sampled IC poses clear both its own courtyard and copper/edge tests.
For their twelve coil variants, 117 collide internally, 351 hit fixed component
courtyards and 144 extend beyond the board. None reaches a clear coil pose or
route/fill qualification. All 351 external coil failures retain exact pose and
blocker-reference witnesses. Counts below are per blocking component and can
overlap within a failed template:

| Fixed blocker | Captured MPN | Blocked templates |
| --- | --- | ---: |
| C70 | GRM155R71C104KA88D | 126 |
| U51 | SN74LVC1G11DRYR | 126 |
| U1 | TLC59581RTQT | 108 |
| U17 | SN74LVC1G11DBVR | 108 |
| U2 | 74HC4514PW,118 | 9 |
| U11 | SN74LVC1G04DBVR | 3 |

These are captured-source identities, not permission to move or substitute
these blockers. This finite regional/template result does not establish global
impossibility, rule out a different arrangement, or justify relaxing source
contacts/clearance. Wider/coordinated floorplanning, including regulator bypass,
feedback and EN pull-down locality, needs its own recorded scope. The current
source uses R81 as 511 kΩ upper feedback, R82 as 91 kΩ lower feedback and R83 as
100 kΩ EN pull-down; verify actual net/MPN assignments rather than inferring
reference numbers from historical prose.

## Source and reproducibility

The cached TI Rev C pin table, layout example and DRL0008A land drawing were
re-rendered/read (PDF pages 3,18,26); the supplied Murata DFE page 1 was likewise
rechecked. U36.7 is ground and U36.6 is MODE tied low. The current DRL 0.67 ×
0.30 mm, 0.5 mm-pitch lands and DFE 0.80 × 2.00 mm lands at ±1.00 mm remain
unchanged. No current, bypass, thermal or assembly qualification follows from
this drawing comparison; TI's short/wide power and quiet-FB guidance remains.
Vendor PDFs/renders remain local and ignored.

The [machine-readable evidence](../../mechanical/review/l1-cleaned-locality-2026-11-04.json)
includes both full finite outcomes, 86 pad witnesses, 51 clear-IC observations,
351 coil obstruction witnesses, captured blocker identities, source/tool hashes
and seven CLI rejection cases. Private/public probe outcome counts agree.
Input overwrite, output outside ignored build, wrong input and the wrong
historical source-basis selection are rejected without changing source bytes.

```sh
KPY=/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/3.9/bin/python3
"$KPY" tools/screen-converter-inductor-locality.py --basis cleaned52 --source hardware/coupon/rev-a/build/vled-cleaned-stage-2026-11-01/a/trial.kicad_pcb --output hardware/coupon/rev-a/build/l1-review/fixed.json --step-iu 100000 --angle-step 15
"$KPY" tools/screen-u36-l1-pair.py --source hardware/coupon/rev-a/build/vled-cleaned-stage-2026-11-01/a/trial.kicad_pcb --output hardware/coupon/rev-a/build/l1-review/pair.json
```

Generate the exact input through the [cleaned-stage replay](vled-cleaned-stage-feasibility-2026-11-01.md)
if absent. The older corrected59 mode retains its separate exact source hash;
selecting it does not admit the cleaned candidate or silently broaden history.
All existing part/order-code, electrical/return/process/assembly/fit and
independent Gate A holds remain open; fabrication remains prohibited.
