<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0132: Use the existing exact U52 signal-neck allowance

Date: 2026-11-14
Status: Accepted for ignored exact-escape feasibility; no successor selected.

The immutable selected source remains 33 native/physical opens. The exact
unchanged source rule file already permits 0.12 mm B.Cu tracks intersecting
U52's courtyard on DISPLAY_CLEAR_3 (and its listed sibling pins). This is the
existing package-specific exception, not permission for general narrowing.
Its original power/ground leaves are also 0.12 mm; ADR 0130's supply-leaf width
was corrected accordingly. No native rule/profile change is authorized.

From ADR 0129's interface-restored prototype, add only one exact 0.12 mm B.Cu
signal neck from unchanged U52.1 at (69.65,0.65) to (70.10,0.65) mm, length
0.450 mm, entirely within its existing courtyard. Retain every source item
outside the exact already-recorded three MODE_BOOT_N retirements. No U52/C71
move, capacitor change or additional source retirement is authorized.

The DSF pin pitch is 0.35 mm and native land width across the row is 0.17 mm.
The calculated centreline-to-adjacent-land clearance for a 0.12 mm straight
neck is 0.35−0.17/2−0.12/2 = 0.205 mm; this is a geometry calculation, not a
waiver or manufacturing qualification. Verify actual native shapes, including
all no-net/mechanical pads, against the unchanged 0.20 mm clearance rule.
Use ordinary 0.20 mm copper after that exact local neck and only the existing
supported adjacent/central/full-span planning via geometries. Reject any prior
group loss, new finding or unlisted narrow copper.

The neck alone is not a new terminal connection. Final selection requires the
actual U51.4–U52.1 join, all 221 original live groups, matching native/physical
count below 33, all original 104 finding payloads unchanged, frozen exact
retirement/neck/ordinary-addition ledger, independent stable replay/refills,
fault/source and visual checks. Parts/poses/pins/nets, limits, protection and
default-off behaviour remain unchanged. All electrical/stack/process/fit and
independent Gate A holds remain; fabrication is prohibited.
