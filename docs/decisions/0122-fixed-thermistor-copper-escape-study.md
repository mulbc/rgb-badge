<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0122: Fixed thermistor copper escape study

Date: 2026-11-12
Status: Accepted for ignored geometry and routing feasibility only.

Continue from the selected 34-open source, SHA-256
`92f942e46281475cbdadf6e9a0ad7a0d531e38c3032f85a4206bbf9e9bc1fccd`.
TH1.1 remains isolated on CHARGER_TS. Keep the exact thermistor, all poses,
footprints, pin nets, charge thresholds and every safety boundary unchanged.
The native read-only escape screen identifies one In4.Cu colour track,
`7ffcb702-53ec-5778-9cd1-6c4d4972e179`, COL_01_R, from
(77.4,16.25) to (48.75,16.25) mm, obstructing a possible In4/B capture at
(54.85,16.225) mm. This observation is not a circuit join.

First screen a local 0.20 mm COL_01_R transfer on In3.Cu with two supported
In3/In4 0.30/0.10 mm microvias. Bound its two transfer sites to x=53.5–54.4
and x=55.3–56.0 mm, y=16.25 mm, retaining the original In4 endpoints and
all original direct same-net contacts. The intervening In4 portion alone may
be replaced in an ignored trial after exact contact inventory. No other
original copper may be retired, no footprint moved, no clearance or width
reduced, and no centre-layer microvia added.

A geometry-clear transfer alone cannot be selected. A complete subsequent
CHARGER_TS join must retain every prior physical pad group, including all
colour and supply/return groups after native zone fills, reduce both native
and independent physical opens, retain the exact original 104 DRC findings,
and pass exact ledger, replay, source, fault and visual checks. Record the
actual new sense route and contact ledger before a successor is adopted.
The existing supply/thermal/protection/timing/current limits remain fixed.
Finite screens do not prove general feasibility or impossibility. No hardware
measurement, thermistor thermal qualification or fabrication release is implied.
All controlled-stack, process/fit, 557 centre-via and independent Gate A holds
remain open.

The first 285 same-y transfer templates all intersect retained COL_01_G on
In3.Cu. Extend only the read-only screen to transfer y=15.80–16.30 mm, with
short 0.20 mm In4 stubs back to the original y=16.25 mm line at each end.
Keep both x bounds, source-contact retention and the TS capture reservation.
This expands the finite geometry search; no PCB is selected or saved by it.

## Recorded geometry result

The [controlled native screen](../development/fixed-thermistor-transfer-2026-11-12.md)
rejects all 285 same-y and 3,135 offset templates at copper clearance. No PCB
is saved and no placement or retirement is selected. The exact 34-open source
remains unchanged; different transfer geometry and the zero-open goal remain
open.
