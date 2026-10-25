<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0048: Local display-track detours for pad escapes

Date: 2026-10-23
Status: Evaluated locally; no display-track replacement selected in the 100-edge checkpoint.

## Context

At the 122-edge local checkpoint, bounded coincident and staggered via searches leave isolated ground and supply pads enclosed by earlier display copper. Passive moves cannot resolve every enclosure while preserving existing groups. A narrower signal probe does not remove an obstruction on a different net. Earlier R28/R29/R2/R36/R86 studies already demonstrate that exact local display-track replacement can open a return path, provided every earlier group and the full native findings are preserved.

## Decision

Permit replacement of explicitly recorded 0.20 mm straight `COL_*` or `ROW_*` display segments that obstruct an audited ground/supply pad escape. Retain their exact source signatures and replacement geometry. Keep original endpoints and unchanged straight tails where possible; use a bounded alternate-layer bridge around the obstruction, with 0.20 mm tracks, 0.20 mm clearance and 0.30/0.10 mm adjacent-layer microvias. Record original and replacement lengths and layers. No ordinary-track deletion without a selected replacement, package/net/value/pin-map change, current-limit increase or interlock connection is permitted.

The independent verifier must retain every other original nonzero track, require both original endpoints to remain contacted by same-net copper on the original layer, preserve all accepted 150-edge physical pad groups and validate exact integer retirements/additions. Source/selected comparison and fault guards must reject undeclared removal or restoration of a replaced original. Refill and full native DRC must retain precisely the original 104 intrinsic findings, and both native and independently counted physical-pad edges must decrease. ADR 0046's separate orphan-via restoration proof remains required.

This is a local routing replacement, not power/return-path, signal-integrity, thermal or manufacturing qualification. Added via transitions and detours require independent Gate A engineering review before fabrication. No fabrication files are released.

## Selected outcome, 2026-10-25

The local U38 ground/COL_09_R detour candidate is excluded. The accepted 100-edge checkpoint retains every ordinary nonzero frozen-source track and all accepted 150-edge tracks. Only the separately witnessed three orphan microvias in ADR 0046 retire.
