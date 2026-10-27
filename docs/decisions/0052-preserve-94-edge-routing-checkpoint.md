<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0052: Preserve the accepted 94-edge routing checkpoint

Date: 2026-10-26
Status: Accepted for an unqualified continuation toward 50 opens.

Freeze the exact 94-edge integer plan at commit 759700b. In addition to the existing 100/150/215-edge contracts, retain every selected 94-edge copper item, completed physical pad group, power-zone definition and both selected DSF supply-neck records. Permit only additive original-width routing and separately verified R/C poses under ADR 0045, with the exact pad-neck scope of ADR 0051 unchanged. Do not retire more copper or change current/protection/enable boundaries, exact parts, pad maps, default widths, clearance or via dimensions.

A signal route and any necessary supply/ground repairs are one transaction: accept only if the final refilled board preserves all prior groups and source-copper nets, reduces native and independently counted physical-pad opens, and retains exactly the original 104 DRC findings. Require exact plan/profile/custom-rule fingerprints, byte-identical replay, orphan-restoration evidence, source/LED checks and fault guards. A lower ratsnest count does not establish bypass, return, current/transient, SI, fit or process quality. The board remains unbuilt and unqualified; independent Gate A precedes fabrication.

## Accepted 91-edge continuation, 2026-10-26

Commit 48cdb7a passes the independent 91-edge count, unchanged 104 findings, stable refill/replay and source/fault checks. Freeze its integer plan as an additional checkpoint and retain every selected copper item, completed pad group, power-zone definition and selected neck record. Apply the same transaction, dimension, exact-part, current/protection/enable and fabrication constraints above. Subsequent work must preserve the 91-edge joins as well as the earlier checkpoints; a search configuration change is not permission to change physical routing rules.

## Accepted 84-edge continuation, 2026-10-26

Commit e095f3b passes the independent 84-edge count, unchanged 104 findings, stable replay and source/fault checks. Freeze its integer plan as an additional checkpoint. Retain every selected copper item, completed pad group, power-zone definition and selected neck record under the same constraints. Additional exact pin escapes already enumerated by ADR 0051 may be selected only with complete native connections, exact metadata and unchanged full DRC; dangling seeds are never accepted.

## Accepted 82-edge continuation, 2026-10-27

Commit 88fdcbe passed the independent 82-edge count, unchanged 104 findings, stable replay and source/fault checks. Freeze its integer plan as an additional checkpoint, including the completed address nets and C67 ground join. Retain every selected copper item, completed physical pad group, power-zone definition and existing neck record under the same additive routing constraints. New USB or LED routes require the same unchanged native DRC and preservation evidence; connectivity does not qualify differential impedance, stubs, skew, reference returns or timing. Fabrication and independent Gate A requirements remain unchanged.

## Accepted 76-edge checkpoint and enumerated exception, 2026-10-27

Freeze the accepted 42e16a1 76-edge plan and all its completed physical groups, added copper, original zones, parcels and neck records. [ADR 0053](0053-enumerated-local-track-replacements.md) permits exactly two catalogued original-source track replacements in the 71-edge continuation, with independent original-layer endpoint and direct interior contact proof. This is the sole exception to the original-source copper freeze above. Every earlier checkpoint's added copper, all previous physical groups and every other original item remain protected; no general deletion or rerouting permission is granted.

## Accepted 71-edge checkpoint, 2026-10-27

Freeze abf4f99's integer plan and every completed group/addition. ADR 0053's exact third source replacement permits the 70-edge PAIR10 ground transaction only after full native/replay/fault proof. Every earlier addition and all other original copper remain protected. Current/protection/enable and fabrication constraints remain unchanged.
