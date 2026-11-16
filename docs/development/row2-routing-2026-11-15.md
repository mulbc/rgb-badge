<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Complete row-two routing checkpoint — 2026-11-15

The selected successor `led-row2-routing-trial-114mm` has **28 native and
independently counted physical opens**, reduced from 29. All 217 preceding
physical groups survive. The complete four-physical-pad ROW_GATE_02 is joined;
the original ROW_SEL_15, VLED and GND groups remain connected.

ADRs 0167–0169 scope the exact two-part exchange. R8 ERJ2RKF1001X flips about
its fixed supply pad to (72.575,8.000) mm / 90°. R37 ERJ2RKF1003X moves to
(72.200,9.500) mm / 180°. Nineteen original selector leaf tracks are replaced
by one ordinary 0.20 mm B.Cu lead (calculated 0.961770 mm); all six retained
external track witnesses directly touch it. Two 0.30/0.10 mm B/In4 microvias
and one ordinary 0.20 mm In4 lead join the row gate over 2.250 mm. All four
old ground branches stay in the original main-ground group; the relocated
R37 ground pad contacts actual connected filled copper with a retained source
witness. No other copper or part pose changes. There are 483 parts and 19,381
copper items; 19,377 retained source items preserve exact geometry and via types.

Validation passed: exact original 104 design-rule finding payloads under only
the preceding U48/U52 transforms, all prior groups, exact part fields/local
pads and independently transformed global pads, immutable board/net/zone/setup,
byte-identical profiles/rules, and independent hole audit. Two separate
three-fill replays produce the exact selected bytes. Removing four additions,
restoring nineteen source tracks and both source poses reproduces the parent
byte for byte across three fills, with all 217 original groups, all original
copper/types and empty integer XOR for all nine zone fills. Twenty-one injected
faults are rejected, including direct row/selector/ground/supply disconnections;
eight supported-span hole controls pass (three accepted, five rejected).
All 37 source-workflow commands pass. Native B.Cu/In4.Cu renders at the row and
old selector site were visually compared before selection: moved courtyards,
fixed supply contact, short gate route, selector lead and ground contact agree
with the recorded geometry. This is CAD geometry review, not hardware validation.

The [checkpoint](../../mechanical/review/row2-routing-checkpoint.json) binds the
source, exact plan, selected PCB and ignored raw validation/visual evidence by
SHA-256. Reproduce with `tools/check-row2-routing.sh` on native KiCad 10.0.6.
The immutable 29-open parent and its validation remain available.

The preceding ADR 0160–0166 studies did not select a board. Plane-preserving
USB corridor screens found no route within their finite bounds. A complete
private USB bridge replacement retained all groups with 29 opens and exact
104 findings, and inversely restored the parent exactly; subsequent heartbeat
attempts still split other original groups. The front-access heartbeat
prototype preserved all groups, but bounded cardinal/diagonal and short-hop
searches did not complete a join. These finite misses establish no global
infeasibility. Their [evidence manifest](../../mechanical/review/row2-preceding-studies.json)
retains source hashes and raw artifacts; none of their geometry is adopted by
this row-two checkpoint.

The zero-open goal remains unfinished. The 557 historical unsupported centre
microvias remain in this selected source. Every electrical, effective-capacitance,
part approval, provisional paired-row identity, timing, return/thermal, controlled
stack, process and fit hold remains. Independent Gate A is still required;
fabrication remains prohibited. No current, fail-safe, NTC, protection, timer or
default-off boundary changed.
