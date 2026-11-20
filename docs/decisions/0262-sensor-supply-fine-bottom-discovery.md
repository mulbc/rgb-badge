<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0262: Sensor supply fine bottom discovery

Date: 2026-11-20
Status: Accepted for bounded read-only complete-join discovery.

ADR0261's original-grid complete gateway supply graph exhausts177 nodes;
356 proposed supported accesses fail Cu. Its exact gateway still preserves
all211 original groups,19343 retained original Cu, main GND197/VLED38/
USB32 and23 matching opens without orphans. No complete supply is selected.

Repeat only the same complete-gateway supply search with0.005 mm B steps
and0.025 mm In4 steps. Test the one permitted new supported B/In4 access
only at global0.025 mm coordinates reached by actual native-clear B edges.
No artificial pad, snap without a physical edge or changed clearance is
allowed. Keep actual-source/native merged-segment checks, full source/new
holes, the same ROI,≤100,000 nodes and≤12 mm complete physical conductor.
A1.5 heuristic weight may prioritize discovery; it implies no optimality.

Every found candidate must refill in RAM and preserve all211 old groups/
retained Cu, no orphans, GND197/VLED38, actual main USB33 including U39.5,
and22 matching native/physical opens. Reject and roll back a failed candidate
before continuing, proving base23 restoration. Write no PCB. All original
fixed gateway definitions, source, profiles, parts, current/threshold/default-
off/protection and bypass/thermal/return/stack/process/fit/Gate A holds remain
unchanged. A separate exact complete prototype and all successor gates are
required before selection; fabrication is prohibited.
