<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Layer-cost distance fields and isolated routing evidence

Status: **search-tool improvement only; accepted PCB unchanged and fabrication prohibited**.

The [guarded routing explorer](../../tools/search-native-control-routes.py) now
supports `--heuristic empty-grid` and `--reverse`. The previous Manhattan mode
remains the default. Width, clearance, layer adjacency, microvia dimensions,
source geometry and post-refill physical-pad-group guards are unchanged.

## Distance table

The [new distance field](../../tools/routing_goal_distance.py) computes exact
shortest costs in the obstacle-free grid using layer-specific travel costs and
adjacent-layer transitions. Rear steps cost five, other permitted layer steps
one and transitions twenty. In2 still permits transitions only; the explorer
adds no planar routing on that ground plane. A via transform, independent planar
transforms and another via transform suffice: an empty-grid optimum can perform
all planar movement on one cheapest visited layer. Actual obstacles only remove
edges, so these distances are admissible lower bounds, not physical routes.

Construction is linear in grid cells/layers. Each subsequent query is a direct
array lookup rather than a nearest-point tree traversal. The full 2,253 × 623 × 6
field uses **33,686,856 bytes**. The option is explicit because preprocessing
and memory may be unnecessary for small searches. Positive costs, valid goals,
query bounds and uint32 overflow are checked before use/allocation.

On the retained 225-open application-data fixture, both final modes produce
**byte-identical candidate boards**, also identical to the earlier validated
candidate. The new mode reaches the U46.6 join in **50,772 expansions** versus
**66,263** for the default, or **23.4% fewer**. This compares node counts, not
wall-clock runtime. Full KiCad 10.0.6 DRC on the positive fixture retains the
exact normalized 104 intrinsic findings and 224 opens, with the correct local
footprint-library context. It is not clean DRC or hardware qualification.

Fourteen test methods retain the old 900-query/5,100-neighbor checks and add
complete comparisons against an independent heap/Dijkstra solver for twenty
weighted-grid fixtures, including disabled layers, single rows/columns and
singleton grids. They also check the rear-layer/via tradeoff, source-order
invariance, dominance of the old lower bound, invalid inputs and integer bounds.
Both host Python and KiCad Python 3.9 pass. Source-only CI runs the same suite.

## Direction and evidence

Reverse mode searches from the existing anchor group toward the isolated pin.
It reverses the returned path before committing so both native endpoint leads
retain their original source/target identities. The graph costs are symmetric;
this is an alternative exploration order, not a rule relaxation.

Each rejection now has a directory named for its output board, plus the snapshot
SHA-256, project-relative path and exact split pad groups in the report. Different
probe outputs no longer overwrite a shared rejected filename. All destination
paths are normalized before native processing; snapshot components are escaped,
and source/sidecar overwrites are rejected. Six host-only tests cover relative
outputs, per-probe separation, escaped names, output/source collisions and CLI
help/errors without importing KiCad. A relative-path reporting failure exposed
by the first reversed probe is fixed and covered by these regressions.

The explorer records fingerprints of itself, its heuristic and its two source
helpers before execution; changed source files fail before final board/report
output. Reports distinguish accepted joins, node bounds, exhausted grid regions,
unusable endpoints and rejected physical-group splits. Every report explicitly
prohibits fabrication. Native pads/tracks and transaction refill still need
independent full DRC/source review before any candidate can enter accepted source.

Example exploratory commands, using KiCad's bundled Python:

```sh
/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/3.9/bin/python3 tools/search-native-control-routes.py --nets GAUGE_I2C_SDA --heuristic empty-grid --reverse --max-nodes 800000
python3 -m unittest discover -s tools/tests -p test_routing_goal_distance.py -v
python3 -m unittest discover -s tools/tests -p test_native_route_paths.py -v
```

## Rejected probes and current checkpoint

Reverse gauge data reaches **U35.8 / R101.2 / U46.3** in 540,461 expansions,
but refilling zones disconnects the existing application-supply group at
**R42.1, R43.1, R44.1 and R79.1**. The saved snapshot's hash and all four losses
are verified. Bounded rear and adjacent-layer supply-bridge probes find no
accepted repair. The candidate is rolled back. Forward gauge data/clock each
reach the 1.6-million-node bound; UART finds a transmit-pad path but splits old
supply/ground groups. The tested row-address/heartbeat bounds also yield no
accepted route. None proves a net impossible to route.

No rejected candidate, local project/build file or vendor PDF is committed.
The accepted PCB remains byte-identical to `fb46e74`:
`9844ae5d0d9ff9ed5e839cefa9734e89693dd405fce39092f68e8c3c7e62bc04`.
It still has 224 opens and 104 intrinsic clearance findings. Canonical circuit,
parts, metadata, firmware, current limits, physical routing, existing interlock
isolation and fabrication gates are unchanged. No hardware was measured.

[Current tool validation](../../mechanical/review/native-route-search-upgrade-2026-10-22.json).
The earlier [native board validation](../../mechanical/review/native-control-validation.json)
records its historical tool/source identities at the unchanged 224-open checkpoint;
new search code does not regenerate or qualify a different board. Routing,
package reconciliation, electrical/process/fit qualification and independent
Gate A remain open.
