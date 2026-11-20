<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Fixed sensor and selector routing continuation

The selected row-two source remains **28 native and independently counted
physical opens**, with all 216 groups and its existing acceptance evidence
unchanged. None of these ignored studies is selected. The zero-open goal
remains unfinished. These are CAD calculations and geometry experiments on an
unbuilt board, not measurements or electrical qualification.

Source: `led-row2-routing-trial-114mm.kicad_pcb`, SHA-256
`1723cb53524f7907c784cc401e3b73c5e0ee93b667dedd246a87bf60c673ac34`.
[The machine-readable record](../../mechanical/review/fixed-sensor-selector-continuation.json)
contains exact retirement signatures/types, prototype audits, original-finding
comparisons and local evidence hashes. Raw evidence and generators remain in
the ignored `hardware/coupon/rev-a/build/row2-routing/` directory. ADRs
0185–0198 and the affected requirements bound the experiments before use.

The wider sensor/programming/bypass study finds no complete placement.
Both 5,672-pose sensor port screens reject all poses. C51 belongs to fixed
U40, not U39; its corrected ≤3 mm locality screen rejects all 11,344 poses.
The four-part sensor/gate-stair template preserves the original external gate
contacts but conflicts with fixed VLED output capacitor C49. C49 and the
qualified converter placements are therefore kept fixed throughout the
subsequent routing studies. C51/U40 bypass locality remains unresolved.

| Fixed-placement discovery | Result |
| --- | --- |
| Full-height selector-eight B detour | All eleven paths meet selector-six copper. |
| Lower selector-eight upper captures | All 59 points meet retained copper. |
| Capture near fixed R30 | All 1,257 B/In4 points meet retained copper. |
| Original selector B-prefix captures | 33 supported aligned B/In4/In3 captures clear. |
| Extended two-segment supply necks | 244 B necks clear; no capture clears. |
| Local colour and selector-six layer hops | No supported endpoint captures clear. |
| Bent supply necks | 311 B necks clear; no capture clears. |
| Native eight-neighbour B path search | Sixteen supported supply escapes mutually clear the selector prefix. |

The last search checks exact native shapes on every ordinary 0.20 mm edge;
the blocked hand-defined diagonal prefix is not reused. Captures retain the
0.30/0.10 mm supported outer geometry and original full-board hole/edge rules.
Clearance discovery alone establishes neither a supply join nor a restored
selector circuit.

Four complete ignored prototypes were constructed and independently audited:

| Prototype | Original retirements | Native / physical opens | Original groups retained | Additional rejecting findings |
| --- | ---: | ---: | ---: | ---: |
| First selector/supply captures | 80 | 29 / 29 | 215 / 216 | 3 |
| Later selector/supply captures | 80 | 29 / 29 | 215 / 216 | 3 |
| Replacement selector In3 port | 81 | 29 / 29 | 215 / 216 | 2 |
| Port plus verified GND plane substitution; six-layer routing | 98 | 29 / 29 | 215 / 216 | 2 |

Every prototype retains all 483 part identities/fields, local pads and
independently checked absolute pad positions; every non-retired source copper
item and via type, profile/rules and immutable board structure remains exact.
New ordinary widths and supported hole spans pass the independent hole audit.
All four lose only the original R30.1 selector group; all other original
groups, including main USB supply and ground, remain intact in the retained
trial outputs. The original 104 finding payloads compare exactly, but the full
reports contain the additional unfinished track/via findings above. Comparing
the original subset is not full DRC acceptance or a waiver of those findings.

The first trial finds only over-budget supply paths and no selector join.
The later-capture and replacement-port three-layer graphs exhaust without
joins. The final six-layer trial finds an 8.106535 mm additional supply path,
exceeding the 8 mm complete-net budget after its fixed 2.937082 mm prefix.
Its selector paths exceed the bounded inner-plane copper allowance and also
split the old USB supply group at R61.2 in rejected snapshots. Those paths
are rolled back. These bounded misses establish no global impossibility.

The first prepared prototype's inverse restores all eighty original copper
items and types and removes every addition. Reloading the sorted reconstruction
before filling restores the original native insertion order: three refills
are byte-identical to the selected source, all 216 groups match and integer
XOR is empty for all nine original zone fills. This is restoration evidence,
not acceptance of the incomplete circuit. No full successor fault/visual or
electrical qualification is claimed for these rejected prototypes.

Validation of this record passes all 37 source workflow commands, every
recorded local evidence hash, selected-source SHA and whitespace checks. The
revision README now opens the selected row-two project rather than its
historical inverter parent. No selected PCB bytes change.

All current limits, thresholds, protection/NTC/timer/default-off behavior,
component identities and electrical/thermal/bypass/controlled-stack/process/
fit/Gate A holds remain unchanged. Fabrication remains prohibited. Further
work must preserve the exact outside selector contacts and the complete
supply group rather than adopt a clear but unfinished escape.
