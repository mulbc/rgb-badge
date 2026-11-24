<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0264: Sensor contact tangent discovery

Date: 2026-11-20
Status: Accepted for bounded read-only native escape discovery.

ADR0263 exhausts25,434 nodes and7,160 Cu-blocked access candidates without
a join. The exact gateway remains source-preserving at23 opens. Test actual
short B polylines around existing contact geometry independently of the grid;
no physical width, clearance, hole, source or part rule changes are allowed.

Derive the actual moved U39.6 land's lower-left bounding-box corner and the
left endpoint of retained TEMP_OK B track203518a7-2610-5416-a454-e94881e1a8e7.
The land's bounding rectangle is conservative for its rounded corners. Offset
that corner by new-wire halfwidth+original0.20 mm clearance, and the retained
track endpoint by both halfwidths+original clearance. Add only0.00010,
0.00025 or0.00050 mm geometric guard for numerical rounding, not a process
qualification. Form circumscribed tangent polylines using1/3/5 degree angular
steps; every final integer-coordinate segment must pass exact native Cu.

Connect from actual U39.5 to each existing-grid waypoint
(56.400,14.750),(56.350,14.750),(56.400,14.725),(56.350,14.725),
(56.300,14.750),(56.250,14.725),(56.250,14.750), only with real ordinary
0.20 mm B segments. These are routing waypoints, not pads or net witnesses.
A clear partial escape must refill in RAM with all211 old groups,19343
retained source Cu, GND197/VLED38/USB32 and23 matching opens/no orphans.
A failed fill rolls back before another candidate. Write no PCB.

Any later coarse supply search must carry the exact real escape conductor
and its full physical length; only a source-witnessed full USB33/22-open
join may progress to a separately frozen prototype. Full source/identity/
contacts/hole/DRC104/replay/inverse/fault/visual and electrical/bypass/thermal/
return/current/default-off/protection/process/stack/fit/Gate A holds persist.
Fabrication remains prohibited.
