<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0277: Front module access and exact private-leaf catalog

Date: 2026-11-24
Status: Accepted for bounded read-only complete-access discovery.

ADR0276 finds32 supported plane poses and28 PAIR05 poses with short
R10 power/gate options. Preserve all actual source parts/metadata/Cu.
Test real ordinary0.20 mm F ROW04 access, at most12 mm including the
package strap, to retained original through via642e420b-6171-523e-af5e-
ae5a512f8a23 at77.250,11.900. No new through via is permitted.
Test selector access from actual moved pin2 with at most12 mm conductor
and one additional supported0.30/0.10 mm F/In1 microvia on original
ROW_SEL_04 In1 bridge276689b1-ccd9-597c-a0d9-f3febe7e37c7 (80.2,15.0 to
84.85,15.0). The retained driver port is original In1/In2 via7c230c90-
28aa-5a4c-a462-1ff328f288fd at84.85,15.0. Every new conductor must clear
all source Cu, both moved packages and other proposed Cu; all source/new
holes apply with no unsupported source-hole exception. Write no PCB.

For source cataloguing only, record the exact bridge's typed signature
and original outside contacts before a temporary in-memory graph cut.
Require the cut to separate only original PAIR05.2 from the retained
R26.1/U2.7 driver group. Catalogue the entire source-side Cu component
plus the cut bridge, with exact typed declarations and original outside
contacts. Do not adopt or omit that full cohort before a separate bounded
replacement decision. Gate/row/R10 private source contacts are likewise
catalogued before any omission. Ground stubs may stay only if every
retained source conductor remains attached and full DRC adds no finding.

No partial module or lower count is selected. Full source groups/Cu,
exact104/replay/inverse/fault/source/visual and all part/electrical/return/
thermal/process/stack/fit/independent Gate A boundaries remain mandatory.
Fabrication remains prohibited.
