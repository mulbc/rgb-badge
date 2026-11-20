<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0245: R9 expanded bottom discovery

Date: 2026-11-20
Status: Accepted for bounded read-only discovery.

ADR0244's17,324 local poses fail:17,300 courtyard,24 moved-pad clearance.
No clear pair of leads is inferred; source remains23 opens. Expand only the
read-only R9 placement/lead study to x=72.000–85.000 /y=2.000–16.000 mm,
0.100 mm lattice and four cardinal orientations. Retain all source copper,
actual B courtyard/pad/native clearance and witnessed PAIR04 supply/gate
ports. No PCB, source retirement, new via or other part move is permitted.

Keep ordinary0.20 mm supply conductor≤6 mm. Study gate conductor≤12 mm
instead of the first screen's3 mm, as a CAD discovery bound with exact
1 kΩ pull-up and unchanged current/default-off/protection. The longer lead
requires explicit timing/EMI/return review before engineering acceptance.
Try direct and the two orthogonal one-bend templates for each lead, requiring
mutual clearance and unchanged endpoint widths. A failed bounded screen
is not a proof of global impossibility. All old-group/retained-copper and full
exact104/inverse/replay/fault/visual gates precede any separately frozen
successor. All qualification and independent Gate A/fabrication holds persist.

Also sample the narrow inter-column corridor at x=77.500–78.000 /
y=7.000–13.000 mm with0.050 mm increments and the same four angles,
ports/lead templates/bounds. This includes intermediate x coordinates absent
from the0.100 mm grid; a coarse failure must not imply corridor exhaustion.
