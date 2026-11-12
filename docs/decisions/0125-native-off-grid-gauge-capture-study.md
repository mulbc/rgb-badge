<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0125: Gauge endpoint and capture study

Date: 2026-11-12
Status: Accepted for ignored additive feasibility only.

Continue from the validated 33-open source, SHA-256
`14f0c49582063bab84ea685a8cec798011eb4cd66389b085a3a47777180a13ce`.
U35.2/3 remains a separate two-pad +BAT_GAUGE_SW group. Ordinary 0.05 mm-grid
search exposes no usable endpoint there, while the native 0.025 mm relative
escape screen identifies a clear 0.30/0.10 mm In4/B capture at
(101.415,22.125) mm, directly overlapping original U35.2. This is a finite
geometry result; neither a via alone nor a search limitation is a circuit join.

Permit an ignored trial of exactly that ordinary adjacent microvia, retaining
all original copper, parts, poses, pad shapes and nets. Confirm direct native
pad contact, all 221 source groups after refill and the full unchanged 104
findings before using it as a routing endpoint. Its coordinate is not rounded
to a blocked grid point. No clearance, drill, annular ring or pad is reduced.

Subsequent additive routing may connect this actual capture to the existing
six-pad gauge-switch/repeater/pull-up group using ordinary 0.20 mm tracks and
the previously authorized supported spans, including explicitly screened
In2 tracks. New mixed-drill transitions must be separated with actual stubs,
not accepted as co-located-hole warnings. Retain every prior group after
refill. No source retirement, footprint/net/pin/current change, general
narrowing or new centre microvia is permitted.

The Analog Devices MAX17048/MAX17049 Rev 7, November 2016, page 6 pin table
identifies TDFN pins 2 CELL and 3 VDD; both existing terminals remain on the
physical switched gauge supply. Its ordering table on page 18 identifies exact
MAX17048G+T10 as the TDFN-EP option. The published PDF is readable through the
web viewer; a direct download failed with an HTTP/2 stream error. No different
package, vendor mirror or access workaround is used, and no local PDF hash is
claimed. Source: https://www.analog.com/media/en/technical-documentation/data-sheets/MAX17048-MAX17049.pdf

A selected successor requires native/physical opens below 33, every old group,
exact unchanged 104 findings, exact ledger/contacts, stable independent
replays/refills, source/fault checks and visual review. Via-in-pad fill/cap,
assembly, bypass/current/return/bus and rail-transition behaviour, controlled
stack, 557 historical centre vias, process/fit and independent Gate A remain
unqualified. The selected source stays at 33 opens until every gate passes;
no fabrication or powered-operation claim is authorized.

## Capture-only native result

The exact capture preserves all 221 source groups and 33 native/physical opens
through three stable refills. Native DRC retains the exact 104 baseline
findings plus one `via_dangling` warning on this new capture's own UUID:
`b46464b5-2a84-5c46-a5cb-930683813a92`. Its In4 end has no route yet. This
capture-only board is rejected as a successor and is not called complete.

Amend the preliminary before-routing condition above only for this isolated
ignored experiment: continuation may use that exact capture after verifying
that this one dangling finding is the sole addition and that all 104 baseline
findings remain exact. Completing the actual eight-pad gauge-supply join must
remove the warning. Final selection still requires exactly 104 findings,
matching native/physical count below 33 and every original source group; no
clearance, hole, topology or final-DRC requirement is waived.


## Endpoint-radius diagnosis

The initial empty-endpoint result does **not** establish a pad/grid escape
failure. Repeating endpoint inventory on the unchanged 33-open source finds
360 usable source endpoints at U35. A 45 mm target-radius limit excludes every
other gauge group (zero target endpoints); 70 mm includes 4,187 target
endpoints. The temporary capture is physically valid but not proven necessary.
Prefer further direct routing from the unchanged source with the complete
target group included. Both directions may be explored under the same full
source/group/DRC rules. Search reports now record source/target endpoint counts,
radius and the empty side without changing routing behaviour or claiming that
bounded failure proves infeasibility. No temporary capture is adopted.

A further ignored direct-routing screen may refine the path grid from 0.05 to
0.025 mm while retaining 0.20 mm copper, exact native clearance/hole screening
and supported spans. Scale heuristic via costs with grid resolution; existing
source/contact probes may remain a subset at their original spacing. This is
a finite search experiment, not a clearance reduction or completeness claim.
Keep native/physical source retention, exact final DRC, deterministic replay
and every other selection gate unchanged.
