<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Captured interlock courtyard XY screen

Date: 2026-10-12. This is a calculation from native KiCad XML, **not** a PCB placement, route, enclosure fit or hardware measurement. The [machine result](review/captured-interlock-fit-2026-10-12.json) records the XML SHA-256 exported by KiCad 10.0.6 from the root-linked 20-page coupon source. It contains 497 PCB items, including all 31 new interlock IC/support/test-pad parts; 238 rear parts enter the screen. [The screen script](../tools/screen-captured-interlock-fit.py) reads project-local footprint courtyards and retains the prior LP452845 pack/sensor reservations. It compares the **canonical 32 separate row FETs** with the **proposed, unselected** dual row-package substitution.

| Trial PCB width | Canonical row FETs: unplaced boxes | Dual-package candidate: unplaced boxes |
|---:|---:|---:|
| 106 mm | 23 | 3 |
| 108 mm | 20 | 0 |
| 110 mm | 13 | 0 |

The present 32-FET row topology still misses 20 boxes at 108 mm and 13 at 110 mm, so merely increasing board width within the case target does not resolve this first-fit screen. The dual-package 108 mm trial is a useful target with the actual DSE/DRY/DSF/DCU courtyards, all eleven interlock resistors, nine bypass capacitors and both new 1 mm test pads counted. The first-fit algorithm does **not** constrain the bypass capacitors or divider resistors near their ICs, keep the comparator away from switching noise, reserve traces/vias/thermal copper, protect the antenna, check connector assembly access or include the case wall and USB opening. The dual row package has not been electrically or assembly qualified or changed in the schematic. Thus zero unplaced boxes at 108 mm is a coarse screen, not a board-width decision.

The machine result also records the courtyard-edge gap from each U47–U55 IC to its corresponding C66–C74 bypass capacitor. In the zero-miss 108 mm dual-package trial, these gaps range from **19.06 to 49.66 mm**. All nine capacitors fall under the pack reservation while their ICs scatter around the rear. This is direct evidence that the greedy solution is not a usable circuit placement; it does not impose an arbitrary electrical distance limit.

A second trial places each bypass capacitor immediately after its IC, restricting the courtyard-edge gap to **3 mm** as a deliberately chosen geometric test target. With the unselected dual row packages, this leaves three capacitors unplaced at 108 mm (`C67`, `C70`, `C71`) and one at 110 mm (`C67`). The other six/eight bypass capacitors do receive nearby nonoverlapping boxes. This greedy result is order dependent and excludes routing and the associated divider/logic locality; it neither proves the layout impossible nor approves the 110 mm outline. It shows why a grouped PCB placement must move the ICs and surrounding parts together.

Next physical step: build an actual grouped PCB placement with the selected battery envelope and both row-topology options, then review routing and the 110 × 35 × 11 mm enclosure section. Keep Gate A before fabrication.
