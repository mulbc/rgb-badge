<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Application data and exact-goal routing continuation

Status: **unbuilt noncanonical geometry study, fabrication prohibited**.

The [saved native-control study](../../hardware/coupon/rev-a/staging/led-native-control-trial-114mm.kicad_pcb)
now connects buffer **U46 pin 6 (SDAB)** to the existing **R79.2 / U3.10**
application-data group. TP11 remains isolated. This adds **65 tracks and four
adjacent-layer microvias**, reduces complete native opens **225 → 224**, and
reduces `SYS_I2C_SDA` from two opens to one. Each gauge IC SDA/SCL connection
still has one open; no physical bus operation is qualified.

All 483 placements, pad assignments, exact canonical metadata, previous copper
and previous physical pad groups survive. No new supply repair is needed. Track
width/clearance stay 0.20 mm and microvias 0.30/0.10 mm on adjacent layers. The
cumulative plan now adds 343 tracks/38 microvias to the frozen row-13 input,
for 14,875 total tracks/vias and ten recorded signal joins. Canonical parts,
schematic/BOM, libraries, firmware, current limits and isolated interlock outputs
are unchanged. No material circuit decision or package adoption follows.

## Search improvement

The old heuristic used the bounding rectangle of a connected copper group. A
large winding group can surround empty space, making that lower bound zero
far from its actual copper. The [new spatial index](../../tools/routing_goal_distance.py)
returns the exact minimum Manhattan distance to actual goal cells, including
minimum adjacent-layer cost. It remains an obstacle-free admissible/consistent
lower bound for this graph; clearance and physical connectivity are separate.

On the same 225-open source and 400,000-node bound, the old heuristic did not
find the U46.6 join; the new one finds it in **66,263 expanded nodes**. This is
a search result, not a wall-clock benchmark or proof about other routing choices.
Seven independent test methods include 900 seeded brute-force queries, 5,100
neighbor-consistency comparisons, distant points inside a group's bounding box,
duplicate/order variants and unbounded integer distances. All pass on host Python
and KiCad's bundled Python 3.9; source-only CI runs the same seven methods.

The [reusable search tool](../../tools/search-native-control-routes.py) restricts
outputs to the ignored Rev A build tree and supports only the listed low-speed
control nets. Exact foreign-net pad/track shapes screen leads and vias; the
existing conservative grid screens routed track steps. After each proposed join,
zone refill must retain every old physical pad group and actually join the
requested endpoints. A failing transaction is rolled back. Filled zones and
complete DRC are not part of the geometric search screen, so saved candidates
always need independent native validation. Four local CLI checks verify rejected
source-tree output, unsupported power nets, invalid node bounds and colliding
board/report destinations. The tool does not move components or write accepted
PCB source.

Run an exploratory search against the current study with KiCad Python:

```sh
/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/3.9/bin/python3 tools/search-native-control-routes.py --nets SYS_I2C_SDA
```

The selected search was repeated on the retained local 225-open input; both
saved candidate boards were byte-identical. Native/source acceptance then
extracts only the selected added copper into the integer replay plan. Accepted
board generation depends on that reviewed plan, not running an exploratory
search. Two accepted-board generations are also byte-identical.

## Validation and remaining work

Full KiCad 10.0.6 DRC retains the exact complete normalized multiset of **104
intrinsic clearance findings**. Native and physical-pad counts agree at **224
opens**. All 256 exact LED placements and **18 isolated native guard cases**
pass. The new case detaches application-data copper without changing item counts;
the existing cases retain power-group, duplicate-land, source-copper, placement,
net and microvia-adjacency protections. All **21 circuit/metadata fault tests**
and a fresh complete native canonical XML comparison pass. The source-only sparse
CI layout reproduces the 21 circuit tests and seven distance tests without KiCad,
XML or vendor PDFs. No board was built or measured.

The bounded TP11 search reaches 1,732 cells without a route. A separate direct
pad-on-existing-rear-copper placement probe tests 419 points without an accepted
courtyard/clearance site; TP11 is not moved. Each gauge IC route reaches the
400,000-node bound. A row-02 pullup probe reaches 380 rear cells without an
adjacent-layer escape. These rejected/local results do not prove routing
impossible and are not included in accepted source.

[Increment/search evidence](../../mechanical/review/native-control-application-data-2026-10-22.json),
[current validation](../../mechanical/review/native-control-validation.json),
[native checker](../../mechanical/review/native-control-check.json),
[per-net opens](../../mechanical/review/native-control-open-nets.json),
[full DRC](led-native-control-drc-2026-10-21.json),
[reproduction](../../mechanical/review/native-control-reproduction.json).

Repeat native acceptance with `./tools/check-native-control.sh` and fresh circuit
comparison with `./tools/check-coupon-study-contract.sh`.
Board SHA-256: `9844ae5d0d9ff9ed5e839cefa9734e89693dd405fce39092f68e8c3c7e62bc04`.

Six gate terminals, TP11, each gauge IC bus leg and remaining power/ground/control/
USB routes remain incomplete. Electrical/bus/return qualification, intrinsic
footprint/process findings, canonical row-package adoption, mechanical fit and
independent Gate A remain open. Vendor PDFs, rejected probes, builds and unsigned
fabrication output remain excluded from Git.
