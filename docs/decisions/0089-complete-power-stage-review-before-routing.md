<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0089: Complete power-stage review before further routing

Date: 2026-11-05
Status: Accepted for review, calculation and bounded correction planning only.

## Context

ADR 0088 closes the local converter switching-node routing goal at 50 opens.
That count does not establish a usable power circuit. The
[complete-stage review](../development/converter-power-layout-review-2026-11-05.md)
finds disconnected U36 feedback and enable pull-down, remote U36 capacitors,
unqualified power copper/returns and a VLED power-save/window compatibility risk.
All 104 clearance findings are internal pad pairs in two package families.

## Decision

Prioritize complete converter stages and their default-off/protection interfaces
over reducing the remaining open count. Preserve the selected board, circuit
values, exact MPNs, protection/current limits, fabrication hold and independent
Gate A requirement during this review. Record reproducible native measurements,
explicit sensitivity assumptions, every intrinsic finding and a function-based
routing queue. Calculations are not bench measurements or qualified limits.

The next geometry experiment shall address U36, L1, C40–C43 and R81–R83 as one
nine-part stage, with explicit upstream-switch interfaces. Moving only the coil
and IC is insufficient. A later bounded implementation ADR/contact ledger must
define allowed poses, copper retirement, additions and acceptance before any
canonical geometry change. Do not maintain a remote feedback divider merely to
preserve an incidental pair pose.

Reconcile U37 power-save voltage with the interlock window, effective capacitance,
quiet control returns, exposed-pad heat spreading and source/load envelope.
Keep its draft enable held low. Do not bridge hardware permission boundaries
or change thresholds, mode, parts or currents as part of this review.

Retain global 0.20 mm clearance. Package-internal findings require manufacturer
land/mask/paste and fabricator/assembler disposition. Any future exception shall
identify exact physical pad pairs and frozen geometry; it shall not grant
pad-to-track, via, foreign-pad or whole-net clearance reductions. No existing
finding is waived or accepted for fabrication by this decision.

## Acceptance and consequences

Deliver the linked review, source identities, all-104 native inventory,
reproducible calculations/tests, bounded correction queue and explicit unresolved
inputs. Keep the selected source SHA and 50/104 checkpoint unchanged. Finish this
review goal independently of later layout implementation or manufacturer replies.
Finished copper/HDI specifications, combined capacitor/inductor data, complete
load budget and independent review remain prerequisites to qualification.
