<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0268: Fixed PAIR03 additive supply discovery

Date: 2026-11-20
Status: Accepted for bounded read-only route discovery.

Independently search from actual selected23-open PAIR03.4 to actual main
VLED38 conductors on B/In4/In3, without moving any part or retiring any
copper. Keep ordinary0.20 mm tracks and at most two supported0.30/0.10 mm
microvias monotonically B/In4 then In4/In3. Use0.025 mm grid,
x70..88/y3..13 mm, at most25 mm conductor/400000 expanded states and1.5
weighted heuristic. Require native source Cu/hole and mutual-via hole
clearance. Existing PAIR03 trial package/MPN acceptance remains held.
A full result must refill to22 native/physical opens, main VLED39,
GND197/USB32 and retain all211 prior groups/all19349 attached source Cu
with no orphans before separate full successor qualification. Write no
PCB. All electrical/current/return/bypass/thermal/process/stack/fit and
independent Gate A holds persist; fabrication is prohibited.
