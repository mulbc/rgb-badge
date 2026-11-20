<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0044: Localize unrouted study passives

Date: 2026-10-23
Status: Accepted for an unqualified routing derivative only.

## Context

The first-fit board places several sense, pull-up and bypass parts far from the IC pins they serve. Bounded searches leave short setting networks unrouted because their existing physical separation exceeds the routing-length budget. Adding long detours would not resolve the locality problem. A native audit identifies 22 resistors/capacitors with at least one isolated pad and no direct contact to any nonzero copper in the frozen 215-edge source. This includes USB series resistors, which are excluded from the automatic relocation screen.

## Decision

A separate routing derivative may relocate selected resistors and capacitors from that audited inventory, keeping exact MPN, footprint, pin numbers, relative pad geometry, polarity and nets. Record every original and selected pose in integer units. Do not relocate ICs, thermal sensors, connectors, USB differential series resistors or row MOSFET pairs under this decision. Do not change values, current settings, circuit topology, protection features or enable-domain separation.

Retain every nonzero track and via in the frozen source. Preserve all earlier physical pad groups using pose-independent physical identities (reference, numbered pad, exact footprint-relative pad coordinates), including duplicated pad numbers. Require actual native and physical-pad edge reductions, native courtyard/clearance checks and the exact unchanged 104 intrinsic DRC findings after zone refill. Reject moves that split an existing plane group or cannot reconnect the moved passive to its former group. Keep the selected tracks at 0.20 mm, other-net clearance at 0.20 mm and adjacent-layer microvias at 0.30/0.10 mm, as recorded in ADR 0043. Added current/reference/feedback-setting copper shall remain within 5 mm total per sensitive net.

## Remaining review

This improves source placement and routing only. Feedback/Kelvin return choice, decoupling effectiveness, current/thermal capacity, controlled impedance, manufacturing process/stack, stencil and interlock behavior remain engineering acceptance work. Independent Gate A review remains mandatory before fabrication. No manufacturing outputs are released by this decision.
