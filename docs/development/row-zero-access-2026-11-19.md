<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Row-zero access continuation on the 26-open source

The selected front-R11 board remains **26 native/physical opens**, with all
prior groups preserved and exact original104. This read-only continuation
selects no successor and writes no PCB. Its exact raw evidence hashes are in
[the continuation manifest](../../mechanical/review/row-zero-access-continuation.json).
ADRs0218–0221 bound the source, regions, widths, interfaces and searches.

The former R11 region now has 151 legal lower VLED captures among 8,591
samples, but none has supported In3 access or actual main VLED contact.
The corresponding row-zero capture screen finds no complete gate neck.
The native B graph from PAIR01.5 alone exhausts at 425 nodes. Including all
three actual connected gate pads/retained endpoints expands that graph to
870 nodes and still finds no supported gateway. Source-group seeding avoids
requiring unnecessary new tracks through existing intrinsic package copper.

At otherwise B-clear reachable nodes, exact COL_09_R In4 wire
`88aa7fc4-2e84-5bb4-847e-f3ce1119f29a` is the sole inner blocker at
171 nodes; exact COL_09_B wire `7d3b740c-3700-5948-afb0-514468ad24d2`
is sole blocker at another 29. Native contact catalogues identify every
original interface and no intermediate branch or filled-plane contact.
Neither wire is retired in selected source.

Prospectively omitting only the red wire exposes thirteen supported paired
gate gateways, including (74.825,3.250) mm. Its retained original In3/In4
via centres at (60.900,3.250) and (78.600,3.250) mm define the replacement
interfaces. Ordinary In3 routing between them exhausts its bounded graph at
1,573 nodes. A local In3 hop samples 51 supported captures and finds no pair.
An independent ordinary B hop has eight clear left and fifteen clear right
captures, but all 120 pairs / 12,120 orthogonal detours fail. Native B graph
refinement exhausts at 2,625 nodes. Those finite misses do not establish
that a wider coordinated routing change is impossible.

The independent blue-wire alternative retains the entire red net and omits
only its own exact original wire. All 870 reachable paired captures remain
copper-blocked, so its dependent local-hop study does not proceed. No source
interface, part, value/current limit or routing rule changes.

The old six-item R6 supply cohort was also re-inventoried. Its original In2
stem has several outside interfaces; it cannot be treated as an unbranched
leaf. ADR0119 already requires retaining a shortened shared stem. No item
from that cohort is removed here. The remaining-net layer inventory records
actual retained interfaces for future complete routing studies.

Both hosted checks for selected commit `b6bdbcd2c412bb4d381de79464aad51c1cb625da`
passed: [run 44604635498](https://github.com/mulbc/rgb-badge/actions/runs/44604635498)
and [run 44604608982](https://github.com/mulbc/rgb-badge/actions/runs/44604608982).
They supplement the recorded local native workflow, not fabrication approval.
Electrical/thermal/return/bypass, part/assembly/fit, controlled stack/process,
556 unsupported historical centre microvias and independent Gate A remain
open. Fabrication is prohibited, and the zero-open goal remains unfinished.
