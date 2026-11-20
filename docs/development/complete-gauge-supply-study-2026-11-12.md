<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Complete gauge supply restoration study, 2026-11-12

**No successor is selected.** Continue from the immutable validated 33-open
board, SHA-256
`14f0c49582063bab84ea685a8cec798011eb4cd66389b085a3a47777180a13ce`.
[ADR 0126](../decisions/0126-complete-gauge-supply-group-restoration-study.md)
bounds these ignored additive trials. All parts, local pads, poses, nets,
original copper/via types, profiles and board/zone structures remain unchanged.

The direct U35 route joins the actual eight switched-gauge terminals, but
initially splits existing return and supply groups. Four independent GND
repairs restore the original main ground group, including TH1 and converter
returns. The original isolated PAIR01 ground pad remains an open. A separate
VBUS repair restores TP32's complete original input group. Subsequent ordinary
APP paths that re-isolate TP32 are rejected.

| Ignored stage | Native / physical opens | Original source groups still split |
|---|---|---|
| Direct gauge route | 39 / 39 | GND, VBUS, APP, protected battery |
| Four ground joins | 35 / 35 | VBUS, APP, protected battery |
| USB-input restoration | 34 / 34 | APP, protected battery |
| APP bridge with reserved captures | 33 / 33 | Protected battery |

Every listed stage retains the **exact original 104 DRC findings**. None
retires source copper. The final row's unchanged count does not establish
source retention: it exchanges one new gauge join for one broken original
battery group, so it remains rejected as a successor.

The APP bridge uses one new adjacent In3/In4 0.30/0.10 mm capture at the exact
existing R106 supply capture, (94.453742,26.250001) mm. Its In4 copper footprint
matches that already present at the In4/B source capture. The new In3 contact
retains all current groups; it is not treated as a completed route alone.
Candidate filled-plane endpoints are reserved 0.151 mm inside their actual
native-witnessed component so a complete 0.30 mm capture fits. The resulting
three-item route restores APP in 1,214 expansions while preserving VBUS and
all ground groups. Full native DRC again equals the exact 104 baseline.

Independent comparison against the selected 33-open source verifies all
19,178 preceding copper items, 483 parts/fields/poses/local lands and all
profiles/net/setup/zone/outline structure. Only the original protected-battery
group remains split: J2.1/SW2.6 and C53.1/U41.2/U41.3 are still separate.
The original 221-group retention requirement therefore has not passed.

Remaining battery searches retain ordinary widths and supported spans. A
six-layer inner variant is rejected when it splits restored ground, VLED and
USB-supply groups; it is not used as a new source. Sampled two-layer and
three-layer alternatives select no join. Further bounded layer alternatives
remain experiments, with no general impossibility claim. The latest actual
filled-region inventory places the left battery region's edge at x=57.924047
mm and the right region's edge at x=79.080256 mm; these are not interchangeable
with the earlier CC1 study's different topology.

A four-layer battery bridge, restricted to B/In4/In3/In2, does retain VLED,
APP, VBUS and the actual eight-pad gauge group. It restores all five original
battery terminals, but leaves two original groups split: GND and the main USB
logic supply. Its independent audit retains all 19,178 source copper items,
483 parts and immutable profiles/structure, with exact original 104 findings.
The trial has 35 native/physical opens and remains unselected.

The USB supply now has groups of 25, seven and one pads. The one-pad U39 supply
was already open; restoring only the 25-to-seven split is the immediate repair.
Native filled-component inspection places the left In3 region's furthest
extent at x=67.819102 mm and the right component's closest extent at
x=75.666954 mm. A supported adjacent In1/In2 extension on an existing right-side
capture retains all current groups, but its In1/In2/In3 search exhausts the
sampled graph after 964,574 expansions. It is an unfinished capture, not a
join. A 6,561-point track-interior capture screen produces no candidate: every
point either misses source copper or misses the left filled component. The
separate 0.025 mm outer battery search reaches its three-million-node bound
from both sides without a join; this is a bounded result, not impossibility.

Two subsequent ground repairs add seven ordinary items and restore the entire
original main ground group. The independent original-source audit then finds
only the seven-pad USB supply loss: 33 native/physical opens, exact original
104 findings and all original parts/copper/structure retained. This exchanges
a new gauge connection for the USB split and still cannot be selected.
The four-layer USB search exhausts its sampled graph from the right and left
components after 943,515 and 1,973,612 expansions. The six-layer right-side
alternative exhausts after 1,670,136 expansions. Full-span and original-USB-plane
reservation alternatives remain separate ignored trials.

The [machine record](../../mechanical/review/complete-gauge-supply-study-2026-11-12.json)
records stage hashes, full ledgers, original-group losses, exact DRC and
rejected-path witnesses. All trial boards and source variants remain ignored.
The reporting fingerprint fix `6b4fd97` passes both remote suites as well as
all 32 local source checks. The selected 33-open source is unchanged.

Gauge bypass/current/return/bus and rail-transition behaviour, controlled
stack, 557 historical centre vias, electrical/thermal/assembly/process/fit and
independent Gate A remain unqualified. No hardware measurement or fabrication
release is claimed. The zero-open goal remains in progress.
