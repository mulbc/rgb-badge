<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0267: Three-layer seeded sensor supply discovery

Date: 2026-11-20
Status: Accepted for bounded read-only route discovery.

ADR0266 exhausts145182 nodes,58103 capture positions and1618 clear
B/In4 captures without an actual main-supply join. Carry the same exact
source-preserving gateway and real escape. Permit a second supported
0.30/0.10 mm In3/In4 microvia and ordinary0.20 mm In3 routing, keeping
x49..65/y9..21.5 mm,20 mm total conductor and400000-state bound.
Search monotonically B to In4 to In3. Targets are actual main USB32
conductors on those layers. Every proposed capture must clear source
copper and holes; the two captures must also pass the full mutual/source
hole audit, including the exact supported adjacent aligned-stack case.
No centre microvia, new through via, width, clearance or profile change.
Require actual filled22 opens/USB33 and every prior group/retained Cu
with no orphans before separate full successor qualification. Write no
PCB. All electrical/bypass/return/thermal/process/stack/fit and independent
Gate A holds remain. Fabrication is prohibited.
