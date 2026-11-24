<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Fixed thermistor transfer geometry, 2026-11-12

The selected board remains at **34 native/physical opens**, SHA-256
`92f942e46281475cbdadf6e9a0ad7a0d531e38c3032f85a4206bbf9e9bc1fccd`.
Both remote check suites for commit `3488395` passed. No result below selects
a successor, changes a component or closes the zero-open goal.

[ADR 0122](../decisions/0122-fixed-thermistor-copper-escape-study.md) keeps
TH1 fixed and screens a local transfer of its obstructing In4 COL_01_R track.
The exact native contact inventory identifies four retained same-net tracks
near the right endpoint and the original In3/In4 via at the left endpoint.
It does not infer contact from a shared zone pointer.

All **285** same-y templates fail native copper clearance, principally at the
retained In3 COL_01_G staircase. The expanded **3,135** templates, allowing
short ordinary-width In4 stubs to different transfer y positions, also fail
native copper clearance. These misses are finite geometry results, not proof
that a different transfer or floorplan cannot work. No PCB, footprint, copper,
zone, profile or net is saved or changed by the screen. Hole, sense-capture,
contact, refill and DRC acceptance cannot be inferred from a template already
rejected at copper screening.

Reproduce with native KiCad Python using
`tools/screen-thermistor-copper-escape.py --output <ignored-build-json>`;
add `--offset` for the expanded screen. Both controlled runs preserve the exact
source SHA. The tool also rejects output paths outside the ignored build tree.
The [machine record](../../mechanical/review/fixed-thermistor-transfer-2026-11-12.json)
records both full outputs, exact blockers, original contacts, tool/raw hashes
and selected-source CI evidence. Earlier exploratory files stay ignored.

Separate additive searches from this source select no join: nine older
control attempts at 250,000 nodes; nineteen all-group supply/control attempts
at 180,000; thirteen through-enabled control attempts at 600,000; and two
outer-layer CC1 attempts at 1,200,000. Node bounds are not impossibility
proofs. Direct full-span plane capture adds no via. The through-enabled CC1
path that splits APP/battery groups is rejected and remains a separate
ADR 0123 restoration experiment. It must not be counted as selected progress.

The thermistor location, TS protection, charge thresholds/current limits and
all hardware default-off boundaries remain unchanged. The 557 historical
centre microvias, controlled stack, electrical/thermal/process/fit qualification
and independent Gate A remain unresolved; fabrication remains prohibited.
