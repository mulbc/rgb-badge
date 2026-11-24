<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Remaining gauge endpoint continuation, 2026-11-12

The selected board remains **33 native/physical opens**, SHA-256
`14f0c49582063bab84ea685a8cec798011eb4cd66389b085a3a47777180a13ce`.
Both remote check suites for selected commit `0e4b154` pass. No trial below
is selected, and U35.2/3 remains physically separate from the six-pad switched
repeater/pull-up supply group.

## Endpoint-limit correction

Native inventory on the unchanged board identifies **360 usable U35 source
endpoints**. A 45 mm endpoint-radius limit selects **zero target endpoints**;
70 mm selects **4,187**. The radius limit caused the earlier empty endpoint-pair
result. That result did not establish a package/grid escape failure.

`tools/search-routing-closure.py` now records source and target endpoint counts,
the radius and any empty side. Existing outcome names and routing behaviour
are retained. Six existing path/source tests and the native two-boundary join,
source/ground-retention and exact-replay fixture pass. Canonical 45/70 mm
one-expansion diagnostic runs verify the new fields; those runs are endpoint
inventory checks, not routing feasibility results.

## Rejected temporary capture

[ADR 0125](../decisions/0125-native-off-grid-gauge-capture-study.md) records a
0.30/0.10 mm In4/B capture at (101.415,22.125) mm directly touching U35.2.
It preserves all 221 source groups and 33 native/physical opens through three
stable refills. Native DRC retains every original 104 finding plus one warning
on the new via's unconnected In4 end. The capture-only board is rejected as a
successor. It proves a geometrically clear contact, not the need for that via
or a completed gauge connection. Direct routing from the unchanged board is
preferred after correcting the endpoint radius.

The manufacturer MAX17048/MAX17049 Rev 7 pin table identifies TDFN pin 2 CELL
and pin 3 VDD, both retaining their existing switched-supply assignment. The
PDF is readable in the web viewer; its direct download fails with an HTTP/2
stream error. No local manufacturer-PDF hash, visual package-drawing review or
package change is claimed. The exact manufacturer URL and page references
remain in ADR 0125.

## Bounded route results

Capture-based, direct, reversed and finer-grid searches reach their finite
node bounds without selecting a join. The 0.025 mm path-grid experiment
retains ordinary widths and native clearance rules. These misses do not prove
that routing or placement is impossible.

A direct unweighted search with supported whole-board transitions finds a
route after 1,955,898 expansions, but native refills split original GND,
VBUS_CONNECTOR, +3V3_APP and protected-battery groups. The transaction guard
rejects it before it can become selected progress. Source returns, USB input,
application and charger supply groups cannot be traded for a gauge join.

An earlier finite frontier reaches In3 at (74.30,4.95) mm. Exact native
neighbour witnesses identify COL_08_G via
`57ab6f90-7601-5609-a75a-f77b4cdce814` and ROW_01_A track
`9a5e5e3b-6dda-536b-84d0-fb9c6813999e` as local obstructions. A read-only contact
catalog records their actual layer interfaces and rejects a straight same-shape
ROW_01_A transfer to In2 against existing copper. No source row/colour track or
via is retired, moved or retyped. A finite frontier is not a proof of a global
routing cut.

The [machine record](../../mechanical/review/gauge-endpoint-continuation-2026-11-12.json)
contains counts, complete rejection witnesses, exact source/capture hashes,
raw evidence and validation references. All trial boards and temporary search
variants remain ignored. Gauge bypass/current/return/bus behaviour, rail
transitions, controlled stack, 557 historical centre vias, electrical/process/
fit and independent Gate A remain open. No hardware measurement or fabrication
release is implied; the zero-open goal remains in progress.


## Reporting fingerprint follow-up

Remote checks for the reporting-only commit `e5ff23d` reject the stale search
tool digest in the historical remaining-routing manifest; current board,
canonical circuit and gauge checkpoint checks pass. The fix retains the
historical digest and its source revision, records an exact byte proof that
removing only the three added report lines reproduces that source, and enforces
the new digest. All 32 source-workflow commands pass after the update. No board,
plan, native acceptance rule or historical geometry evidence changes.
