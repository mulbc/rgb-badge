<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0052: Preserve the accepted 94-edge routing checkpoint

Date: 2026-10-26
Status: Accepted for an unqualified continuation toward 50 opens.

Freeze the exact 94-edge integer plan at commit 759700b. In addition to the existing 100/150/215-edge contracts, retain every selected 94-edge copper item, completed physical pad group, power-zone definition and both selected DSF supply-neck records. Permit only additive original-width routing and separately verified R/C poses under ADR 0045, with the exact pad-neck scope of ADR 0051 unchanged. Do not retire more copper or change current/protection/enable boundaries, exact parts, pad maps, default widths, clearance or via dimensions.

A signal route and any necessary supply/ground repairs are one transaction: accept only if the final refilled board preserves all prior groups and source-copper nets, reduces native and independently counted physical-pad opens, and retains exactly the original 104 DRC findings. Require exact plan/profile/custom-rule fingerprints, byte-identical replay, orphan-restoration evidence, source/LED checks and fault guards. A lower ratsnest count does not establish bypass, return, current/transient, SI, fit or process quality. The board remains unbuilt and unqualified; independent Gate A precedes fabrication.

## Accepted 91-edge continuation, 2026-10-26

Commit 48cdb7a passes the independent 91-edge count, unchanged 104 findings, stable refill/replay and source/fault checks. Freeze its integer plan as an additional checkpoint and retain every selected copper item, completed pad group, power-zone definition and selected neck record. Apply the same transaction, dimension, exact-part, current/protection/enable and fabrication constraints above. Subsequent work must preserve the 91-edge joins as well as the earlier checkpoints; a search configuration change is not permission to change physical routing rules.
