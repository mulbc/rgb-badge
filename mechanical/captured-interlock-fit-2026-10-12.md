<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Captured interlock courtyard XY screen

Date: 2026-10-12. This is a calculation from native KiCad XML, **not** a PCB placement, route, enclosure fit or hardware measurement. The [machine result](review/captured-interlock-fit-2026-10-12.json) records the XML SHA-256 exported by KiCad 10.0.6 from the root-linked 20-page coupon source. It contains 497 PCB items, including all 31 new interlock IC/support/test-pad parts; 238 rear parts enter the screen. [The screen script](../tools/screen-captured-interlock-fit.py) reads project-local footprint courtyards and retains the prior LP452845 pack/sensor reservations. It compares the **canonical 32 separate row FETs** with the **proposed, unselected** dual row-package substitution.

| Trial PCB width | Canonical row FETs: unplaced boxes | Dual-package candidate: unplaced boxes |
|---:|---:|---:|
| 106 mm | 23 | 3 |
| 108 mm | 20 | 0 |
| 110 mm | 13 | 0 |

The present 32-FET row topology still misses 20 boxes at 108 mm and 13 at 110 mm, so merely increasing board width within the case target does not resolve this first-fit screen. The dual-package 108 mm trial is a useful target with the actual DSE/DRY/DSF/DCU courtyards, all eleven interlock resistors, nine bypass capacitors and both new 1 mm test pads counted. The first-fit algorithm does **not** constrain the bypass capacitors or divider resistors near their ICs, keep the comparator away from switching noise, reserve traces/vias/thermal copper, protect the antenna, check connector assembly access or include the case wall and USB opening. The dual row package has not been electrically or assembly qualified or changed in the schematic. Thus zero unplaced boxes at 108 mm is a coarse screen, not a board-width decision.

Next physical step: build an actual grouped PCB placement with the selected battery envelope and both row-topology options, then review routing and the 110 × 35 × 11 mm enclosure section. Keep Gate A before fabrication.
