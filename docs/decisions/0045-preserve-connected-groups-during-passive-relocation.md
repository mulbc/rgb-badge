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
