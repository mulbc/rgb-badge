<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0074: Local VLED switching-node feasibility at the packing seed

Date: 2026-10-31
Status: Ignored geometry experiments only; no canonical pose or routing selected.

ADR 0072 identifies one courtyard/pad-clear rigid VLED pose but does not route
its switching nodes. Its thirteen-part move breaks old external groups. Test
the actual local switching paths before treating that packing seed as useful.

Permit ignored comparisons at the recorded seed: U37 TPS63020DSJT centre
(45.50, 17.50) mm, 0°, and L2 DFE252012P-1R5M=P2 centre (49.55, 17.50) mm,
−90°, both on B.Cu. Compare moving only those two footprints with applying all
thirteen exact poses already recorded under ADR 0072. For the two-part case,
recheck every other actual fixed courtyard/pad rather than assuming the earlier
thirteen-part exclusions still apply. Preserve all parts, local pad shapes/nets,
metadata, existing copper and zone definitions. No source stub may retire.

First test six 0.20 mm B.Cu segments from the mirrored historical local routing:
join U37.6/7 to L2.2 and U37.8/9 to L2.1. Bound aggregate track length on each
switching net to 5 mm. If direct segments are obstructed, a separately recorded
finite B.Cu-only 0.025 mm search may retain that same width, clearance and length
bound. No new switching-node via or width exception is included. Keep current,
voltage, protection, pull-down, display-enable and firmware settings unchanged.

TI TPS63020 Rev I page 4 confirms the duplicated switching pins and identifies
pin 2 as control ground; grounded PS/SYNC pin 13 is a mode input, not a substitute
for the control-ground pin. Section 10 still requires nearby passives and
short/wide power and ground paths. Murata's supplied exact DFE252012P sheet
supports the unchanged nonpolar inductor land. These references are cached
and hash-identified locally; no vendor material is committed.

Record native obstacle checks, exact poses/tracks, calculated lengths, three
fills, native/pad-cluster counts and all prior-group losses. Full DRC must
distinguish existing transformed intrinsic pad findings from new findings; never
claim the canonical unchanged-DRC gate passed for this relocated study.

The supplied 2021 capacitor catalogue does not approve the remaining shared
lands, order codes or effective capacitance. Existing passives remain
unqualified in the two-part comparison. A local switching join or a lower count
alone cannot select a power stage. Canonical adoption requires exact pose,
contact/rework and power-path policies, every prior external group restored,
native/physical counts, full DRC, stable replay, independent fault/source and
orphan evidence. Electrical/current/thermal/EMI, bypass/return, assembly/process/
fit qualification and independent Gate A remain open. Fabrication is prohibited.

## Observed outcome

The [native local switching study](../development/vled-local-switching-feasibility-2026-10-31.md)
finds two directly clear 3.215685425 mm B.Cu paths, with six total ordinary-width
tracks and no new vias. Pair/stage counts are 63/72 native versus 61/69 physical,
with two/three prior groups split and 110/118 full findings. The 104 intrinsic
clearance identities remain accounted for, but vacated copper is dangling.
Stable fills, byte-identical PCB replays, an independent six-track/pad-group
inventory and three real CLI output/source guards pass. No source selection or
obsolete-copper retirement follows from this local feasibility result.
