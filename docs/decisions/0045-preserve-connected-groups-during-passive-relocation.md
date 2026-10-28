<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0045: Preserve connected groups during passive relocation

Date: 2026-10-23
Status: Accepted for an unqualified routing study only; selected poses require independent replay validation.

## Context

The 150-edge checkpoint retains first-fit support parts far from their ICs. Restricting relocation to passives with no direct frozen-source copper contact excludes bypass capacitors and pull resistors whose ground/supply terminals already contact copper. Initial additive control and plane-stitch probes do not resolve those placement constraints; some proposed routes split existing filled-zone groups and are rejected.

## Decision

Permit additional resistor and capacitor poses in a separately validated continuation of the 150-edge study. Keep USB differential series resistors R45/R46 fixed. Keep ICs, inductors, connectors, test pads, thermal sensors and row-pair packages fixed. Preserve exact MPN/manufacturer fields, footprint, value, numbered nets, polarity and footprint-relative pad geometry. No circuit, current-setting, protection or enable-domain change is permitted.

Direct contact to earlier copper is no longer an eligibility exclusion for these R/C parts. Existing tracks and vias remain at their original coordinates: retain all nonzero frozen 215-edge source copper and all copper in the accepted 150-edge checkpoint. A displaced branch is not evidence of a functioning return or adequate current capacity. Accept a pose only after reconnecting every moved pad to every member of its previous physical pad group, identified independently of absolute pose. Preserve every other 150-edge group too. Record all poses and exact integer copper additions in deterministic replay data.

Require actual native and physical-pad-cluster edge reduction, unchanged 104 intrinsic DRC findings after zone refill, board-edge and courtyard clearance, 0.20 mm selected tracks/clearance, 0.30/0.10 mm adjacent-layer microvias and the unchanged project rules. Keep added sensitive reference/current/feedback copper within 5 mm total per net. Do not accept narrower-signal local probes through this decision.

## Consequences

This is a placement/routing source study, not electrical or manufacturing approval. Bypass locality, obsolete branch cleanup, feedback/Kelvin returns, switching loops, copper/via current capacity, RF/thermal/mechanical fit and HDI process remain review work. No source merge releases fabrication files; independent Gate A remains required.

## Local R96 follow-up screen, 2026-10-28

The fixed-pose E1_ILM probe calculates to 4.81452 mm but splits U44.8 from ground, and its initial local ground repairs fail; that probe is excluded. ADR 0045 already permits an ignored R96 placement screen with exact Panasonic `ERJ2RKF3321X`, 3.32 kΩ ±1%, unchanged two 0.50 × 0.50 mm lands at ±0.50 mm, pin 1/E1_ILM and pin 2/GND. Rechecked Panasonic's ERJ datasheet (29-May-25) and recommended lands (24-Dec-25): https://industrial.panasonic.com/cdbs/www-data/pdf/RDA0000/AOA0000C304.pdf and https://industrial.panasonic.com/cdbs/www-data/pdf/RDM0000/DMM0000COL17.pdf . The exact-part web page timed out; the manufacturer family ordering table covers the unchanged MPN and value. No vendor PDF is committed.

Bound this screen to 5 mm from R96's old centre and 3 mm from U44. Preserve all 64-edge copper/groups and previously selected poses. Keep total new E1_ILM trace at most 5 mm, widths/clearance/vias unchanged and reconnect the resistor's ground to its entire old group. This does not change the setting resistance or authorize any higher current. A pose is not selected before lower independent opens, stable full DRC/replay, exact metadata and fault/source evidence. Current-limit accuracy/noise, ground-reference and assembly review remain open.

The 0.25 mm placement screen makes no complete candidate; the finer 0.10 mm screen finds zero legal courtyard/other-net-clearance poses inside both bounds. R96 remains at its accepted 64-edge position. The fixed-pose 4.81452 mm E1_ILM route is also excluded: it isolates U44.8, and both the short plane-bridge and local ground-path screens fail to restore that pad. No new current-setting route or component pose is selected; finite screens do not prove impossibility.

A second ignored screen may expand the distance from U44 to 5 mm while retaining the 5 mm maximum displacement from R96's old centre and the 5 mm total setting-trace bound. The original pose lies outside the first 3 mm IC-locality screen. All exact-part, prior-copper/group and validation limits remain unchanged; this expands only the ignored pose search.
