<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0046: Retire displaced-passive orphan vias

Date: 2026-10-23
Status: Accepted for the unqualified routing continuation only.

## Context

ADR 0045's complete copper retention prevents accepting otherwise connected passive moves when a former pad's adjacent-layer via becomes connected on only one layer. Native KiCad reports `via_dangling`. Adding an unused copper loop or duplicate via would conceal the symptom without improving routing. A precise removal is preferable.

## Decision

Permit retirement of explicitly enumerated microvias from the accepted 150-edge inventory when passive displacement makes them orphaned. Keep their exact integer net, position, layer pair, diameter and drill in the replay plan. No ordinary nonzero track retirement, via resizing, net change or current-limit change is permitted. All non-retired source copper and every accepted 150-edge physical pad group must remain intact. All component and width constraints from ADR 0045 continue to apply.

Independently reconstruct a witness by restoring every retired via to the final selected PCB. Full native DRC of that witness must equal the unchanged 104 intrinsic findings plus precisely one `via_dangling` finding for each restored microvia, at its exact net/layer/position. Refilling and restoring the vias must preserve the final board's physical pad groups and edge count. The final selected PCB must retain exactly the 104 intrinsic findings. Reject any removal lacking this witness, any other new finding, and any loss of an earlier pad-group connection.

This exception supersedes complete via retention only for the exact audited orphan inventory. It does not permit deleting a live route or reducing return/current capacity to hit a connection count. Document selected removals and the restoration evidence separately from added copper. Native source checks are not hardware measurements; layout/current/thermal/process review and independent Gate A remain open. No fabrication files are released.
