<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# R6 continuation after the 25-open checkpoint

The selected 25-open board remains byte-identical. ADR0227/0228 discovery
writes no PCB and selects no R6 move. Exact ignored evidence digests and
finite search outcomes are in
`mechanical/review/r6-after-pair01-continuation.json`.

The vacated B R11 pose clears courtyards/pads but has no direct main VLED
contact; its proposed staggered core transition collides with COL_06_B,
COL_08_G and a retained historical hole. The bounded B supply search to
actual main R8.1 exhausts 1,200 nodes.

The fixed front R6 proposal has no qualifying supply route in the recorded
bounds. Its first In1 search exhausts 769 nodes, the front-only search
13,674 nodes, and the 31-start In2 search 489 nodes. A 2,499-point supported
outer-access grid yields 31 clear adjacent access pairs, or 656 clear first
accesses. A fixed-root two-layer heuristic examines 1,260 nodes and 308
transition sites (11 clear); the multi-root variant examines 5,294 nodes and
1,285 sites (42 clear). Neither reaches an actual retained main-supply port
under the 8 mm combined conductor and six-transition bounds. These are
bounded heuristic outcomes, not a proof that no route exists.

The pull-up supply study does not connect PAIR01.4 or relax its separate
high-side/row-current lead limit. No source copper is removed, no unsupported
centre or through transition is added, and current/protection/default-off,
trial package, return/thermal, stack/process, optical/fit and independent
Gate A/fabrication holds all remain open. The zero-open goal remains unfinished.
