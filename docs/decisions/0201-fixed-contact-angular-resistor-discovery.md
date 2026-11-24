<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0201: Fixed-contact angular resistor discovery

Date: 2026-11-16
Status: Accepted for read-only native geometry discovery only.

The two ADR0200 poses preserve all 216 groups and exact104, but a clear pose
does not establish a supply feed. Extend ADR0199 discovery for exact R21/R11
only to 15-degree orientation samples about their unchanged connected pad-2
centres. Keep R71, all other parts and every original copper item fixed.
Preserve exact part/local-pad/net identities, source-edge/courtyard/copper
rules and every old direct and filled pad-2 contact at each pose.

At a clear pose, screen an optional supported 0.30/0.10 mm B/In4 capture
centred on supply pad 1 and optional aligned In3/In4 access. Check actual
foreign/no-net source copper, the proposed moved footprint's own foreign pad
and full-board hole policy. A main-supply contact requires actual retained
main-group copper or an individually witnessed source filled unit on an
actual capture layer; no invented zone anchor. Write no PCB. No new source
retirement, smaller width/hole, unsupported centre via, value/current limit
or qualification hold change. Any useful pose requires separate exact
complete-prototype scope and all original-group/native/physical/exact104/
source/replay/inverse/contact/hole/fault/visual gates before selection.
