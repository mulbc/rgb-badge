<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0091: Close remaining circuit opens in the routing study

Date: 2026-11-06
Status: Accepted for the first 44-open CAD continuation; zero-open goal ongoing.

## Decision

The owner explicitly requests a goal of zero open connections. Continue from the
immutable ADR 0090 47-open PCB, SHA-256
`e3036ccd84dee004425115617b409ff9c770b8cd7f75a529e178154b17cf5d53`.
Zero means both native ratsnest and independently counted physical pad clusters,
without deleting pads, changing nets, bridging distinct permission boundaries or
counting removal of pad-free copper as a circuit join.

Preserve component identities, exact local pads, schematic circuits, current
limits, default-disabled LED permissions, outline, existing live pad groups and
all accepted local converter geometry. Start with additive ordinary 0.20 mm
routing and unchanged rules. Existing exact narrow-neck exceptions do not grant
general narrowing permission. Any necessary copper replacement or placement
change requires a recorded exact ledger and preserved live contacts before
selection. Search trials remain ignored until their full validation passes.

Do not introduce further unsupported central microvias. New adjacent outer
microvias use existing 0.30/0.10 mm geometry. Any new central transition must
use the provisional 0.50/0.30 mm buried-via planning geometry and be screened
across its complete span; it remains unqualified manufacturing intent. Do not
retype the 557 historical centre microvias in place. Routing does not adopt a
supplier stack or change the historical comparison thickness.

Refill zones after each proposed join and reject transactions that split an
existing pad group. Native DRC must retain the exact existing 104 intrinsic
findings without additions. Final selection requires exact source/geometry
ledgers, stable fills and deterministic replay, source contracts, native and
physical connectivity, and isolated rejection checks. USB continuity does not
establish impedance, skew, return-path or signal-integrity qualification.

The goal does not authorize fabrication or electrical claims. All supplier,
power-copper/current, effective-capacitance, thermal, protection, USB/HDI,
mechanical and independent Gate A qualifications remain separate holds.

## First selected continuation

The [implementation record](../development/routing-closure-2026-11-06.md) selects
44 native/physical opens with exact unchanged 104 findings, all 235 parent
groups, one R1 pose, no retirements and 46 ordinary copper additions. It joins
timing, IREF and ILIM; the LED current resistor moves close to U1 with an
explicit local return. Stable replay, native/source/orphan/fault and visual
checks pass. Rejected DSF/temperature/colour trials are absent from the ledger.
The zero-open objective and fabrication/qualification holds remain open.
