<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0109: Bounded coordinated row-selector reroute at U38

Date: 2026-11-09
Status: Accepted for ignored exploration; no successor selected.

The ROW_SEL_03 back-layer trace separates U38's two ground lands, while
ROW_SEL_01 bounds its lower detour. Explore replacing these two traces
together within the interface recorded in
`mechanical/review/shunt-ground-reroute-interface-2026-11-09.json`, based on
selected source SHA-256
`a24e9220226b77411ae8e8baea5cd629ce0fea8a97c377a708510d6791c2e439`.
Only the 32 catalogued ordinary 0.20 mm B.Cu tracks may be retired. Preserve
the three exact outside fragments, boundary ports and protected PAIR02.2
contact. Confine changed copper to the recorded expanded rectangle. Add an
ordinary B.Cu ground connection between U38.3 and U38.2 if feasible.

Keep all parts, poses, vias, net identities, rules, zones, colour traces,
permission and protection settings unchanged. Preserve every preceding pad
group and accepted addition. No reduced width or clearance is authorized.
Exploration is confined to ignored build outputs. Selection requires a real
native/physical open reduction, unchanged exact 104 DRC findings, independent
interface/contact proof, deterministic replay, fault/source checks and visual
review. Source remains 36 opens until those gates pass. Electrical/process/fit
qualification and independent Gate A still precede fabrication.

The first two B.Cu routing orders failed: ROW_SEL_03 can detour below U38,
but ROW_SEL_00 prevents restoring ROW_SEL_01 in the remaining corridor.
Permit a second ignored variant retaining ROW_SEL_01 entirely and transferring
only the catalogued ROW_SEL_03 section to F.Cu. Use ordinary 0.20 mm tracks
and at most two 0.50/0.30 mm full-span through vias, screened on every copper
layer. Via centres and replacement tracks remain inside the same rectangle;
all other interface and acceptance requirements above still apply. This is
an explicit exception to the initial no-new-via exploration restriction,
not permission for unsupported central microvias or altered rules.

Outcome: GND→ROW_SEL_03→ROW_SEL_01 exhausts 1,305 row-01 nodes without
restoration. GND→ROW_SEL_01→ROW_SEL_03 restores row-01 in 8,689 nodes
but exhausts 7,567 row-03 nodes. The sampled through-via variant finds no
usable left or right capture. No variant is selected. ADR 0110 explores
the identified third-row obstruction explicitly.
