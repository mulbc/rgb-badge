<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0236: R6 placement with a direct bottom supply lead

Date: 2026-11-20
Status: Accepted for bounded read-only pose/lead discovery only.

Use the unchanged selected 25-open source, retaining every original color
and row trace. All earlier color replacements and R6 placements remain
unselected. Inventory confirms actual main VLED B port PAIR02.4 at
(78.825,6.650) mm, original pad uuid 75480661-8dea-5444-ac43-3481bde8d9b8,
and its retained B tracks/via. Do not assume a power part or orientation from
via coordinates; use the actual source footprint and courtyard geometry.

Screen only exact R6 ERJ2RKF1001X on B over x=75.800–79.500 /
y=2.200–6.000 mm at 0.050 mm steps, orientations 0/90/180/270 degrees.
Keep every other part fixed. Prospectively retire only the six exact R6
supply items from ADR0119 and include the mandatory shortened shared In2
stem; no color/source via/other-net retirement is authorized.

Keep the previously clear complete gate transition fixed: lower supported
B/In4 + In3/In4 pair (76.650,4.550), direct ordinary In3 lead to mechanical
In2/In3 0.50/0.30 centre (77.100,4.350), ordinary In2 lead to supported
In1/In2 + F/In1 pair at actual PAIR01 gate body (76.600,4.300). Native
source/mutual Cu and every source/new drill pair must pass.

For each courtyard/pad-clear pose, screen ordinary 0.20 mm B pull-up supply
leads to the actual main PAIR02.4 port: direct, either single-corner Manhattan
path, or a three-segment path via x=79.350 mm. Screen gate B lead from actual
R6.2 to the fixed lower capture: direct or either single-corner Manhattan
path. Require all power/gate paths mutually clear of source/fixed/new Cu and
foreign pads; pull-up supply ≤8 mm, complete gate ≤12 mm. Keep zero-length
segments out of any final ledger. This permits wiring around an occupied
package without assuming its copper lands are clear. Actual R6 B courtyard
must clear every original B courtyard; no other part may move.

Write no PCB. A complete clear pose needs a frozen exact prototype plan,
all original 213 groups and attached retained Cu, matching 24-open counts,
exact104, replay/inverse/nine-zone equality, fault and visual checks before
selection. PAIR01.4 stays open. Current/protection/default-off, trial-package,
electrical/timing/return/thermal, optical/fit, stack/process and Gate A/fabrication
holds remain unchanged.
