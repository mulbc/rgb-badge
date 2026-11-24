<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0280: Preserve the supply plane with a real front row hop

Date: 2026-11-24
Status: Accepted for bounded RAM-only restoration discovery.

ADR0278's first native row path reaches the real ROW04 port but fails
full original-group preservation: its In1 trace splits VLED into34/6
pads (the six are PAIR01/02/03/04,R6,R11), with selector still pending.
Reject it. Selected source remains22 opens; no lower partial count is
adopted. The exact path and groups are row-plane-rejection.json.

Carry only the exact ADR0279 frozen cell and111-item source cohort.
Around the rejected path's maximum-y In1 section, test a real F-layer
hop between two native-clear path vertices,1.0..3.0 mm of original path
apart, with at least0.8 mm endpoint separation. Use two additional
supported0.30/0.10 mm F/In1 microvias (three row accesses overall, as
already allowed), ordinary0.20 mm direct/L F conductor, and at most
64 candidate pairs. No source Cu beyond the111-item catalogue retires.
Only proposed new row traces may be replaced by this hop. No invented
pad or temporary source-connection witness is allowed.

Require native source/new Cu and every source/mutual hole check, at most
12 mm total row conductor including package strap, and refill restoring
VLED40/GND197/full18-pad row/four-pad gate, all19256 retained attached
source Cu and every original group except the explicitly pending
three-pad selector. This is an unselected21-open partial state; only a
final20-open cell preserving all210 original groups may advance.
Write no PCB. All complete qualification/electrical/return/thermal/
trial-package/stack/process/fit/independent Gate A holds remain;
fabrication is prohibited.
