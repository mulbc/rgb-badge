<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0093: Inherit retired-copper evidence from its immutable source

Date: 2026-11-07
Status: Accepted for remaining-routing validation; no fabrication permission.

## Context

The 41-open USB_DN_MCU candidate retains every 43-open and 42-open copper
item and every prior live pad group, with 41 native/physical opens and the
exact unchanged 104 intrinsic findings. The three retired APP microvias are
absent from the immutable 43-open source. Its strict restoration proof already
records identical live pad groups and the same three original warnings.

The new D− path uses freed In4.Cu space near (45.25,8.75) mm. Reinstating the
old APP via in a counterfactual copy causes KiCad refill to reassign that
injected via to USB_DN_MCU. A local detour preserves actual 41-open connectivity
and 104 findings but leaves the reinserted via isolated, increasing the
counterfactual native count. Neither trial passes the previous strict
selected-board restoration contract. These are rejected counterfactuals;
they must not be described as the same three original warnings passing.

## Decision

Keep the exact three-via retirement proof on the unchanged immutable 43-open
parent and rerun it as a required gate. The remaining successor authorizes
**no additional retirements**: retain every parent copper item, all 231 parent
pad groups, the complete 230-group 42-open checkpoint inventory, and explicit
new USB witnesses. The exact ledger, native/physical agreement, stable fills
and replay, source contract, fault tests and exact unchanged 104 findings
remain mandatory for the selected board. No finding is waived or filtered
from the actual selected source.

Continue running a separately labelled selected-board restoration experiment.
Report actual injected-via net changes, open counts, group preservation and
DRC findings; never accept its output as source. It is diagnostic evidence,
not a selected-board pass criterion after reuse of retired space. The manifest
must explicitly identify the immutable-parent basis of the retirement proof.

After every native refill, recheck the exact copper/net inventory to detect
silent net propagation. Add a rejected retired-via reinsertion fault and
retain the actual-copper endpoint fixture, which repairs retained isolated
copper without inventing/deleting pads. Hardware safety/default-off/current
settings, source net assignments and all electrical/process/fit/Gate A holds
remain unchanged. CAD continuity is not electrical or fabrication validation.
