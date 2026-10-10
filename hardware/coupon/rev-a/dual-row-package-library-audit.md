<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Unpopulated complementary row-MOSFET footprint audit

Status: **candidate footprint only**. [Proposed ADR 0020](../../../docs/decisions/0020-dual-row-mosfet-package-proposal.md) has not replaced the canonical 16 P-channel plus 16 N-channel row stages. There is no dual-device symbol, netlist assignment, BOM population, manufacturer assembly approval or independent Gate A disposition.

The exact candidate is Diodes Incorporated `DMC1229UFDB-7`, U-DFN2020-6 **Type B**. The controlled component source is [DS36128 Rev. 7-2, February 2020](https://www.diodes.com/datasheet/download/DMC1229UFDB.pdf), downloaded 2026-10-06 with SHA-256 `441380f483b7a88c204f521248f7822e57221e0bdedeaa1d29fdc505188cda18`. The separately linked [Type B package file](https://www.diodes.com/assets/Package-Files/U-DFN2020-6%20%28Type%20B%29.pdf), dated 2015-11-10, has SHA-256 `794c8246632b0238a139ba44bf7c496db736184db3faca5dce7f5bc3dab8b331` on this review date. It agrees with the component datasheet's suggested pad dimensions. Recheck the current manufacturer revision before final library approval.

The datasheet's **bottom view** labels the six small terminals and both exposed drains; its pin-one marker points to `S1`. Rotated into this project's footprint top-view convention with pin 1 at upper left, the candidate map is:

| Pad | N/P terminal | Footprint centre, mm |
|---:|---|---:|
| 1 | N source `S1` | (−0.65, −0.90) |
| 2 | N gate `G1` | (0, −0.90) |
| 3 | P drain `D2`, small + central land | (+0.65, −0.90), (+0.525, 0) |
| 4 | P source `S2` | (+0.65, +0.90) |
| 5 | P gate `G2` | (0, +0.90) |
| 6 | N drain `D1`, small + central land | (−0.65, +0.90), (−0.525, 0) |

The two lands numbered 3 and the two numbered 6 are intentionally duplicated copper/paste/mask pads, because each exposed drain island is the same named terminal as its small edge land. KiCad will connect duplicate pad numbers to the same net. The numeric sequence beyond the manufacturer's identified pin 1 follows the perimeter convention and the labelled bottom view; verify it independently against a manufacturer pin table/CAD or direct technical confirmation before a connected symbol is released. The package is **not** a shared-drain pair.

The [candidate KiCad footprint](footprints/rgb-badge-coupon.pretty/U-DFN2020-6_TypeB_Diodes_DMC1229UFDB.kicad_mod) transcribes the suggested `X=0.35`, `Y=0.50`, `X1=0.60`, `Y1=1.00`, `C=0.65`, `G=0.15`, `G1=0.45`, `X2=1.65` and `Y2=2.30 mm`. The six edge lands are 0.35 × 0.50 mm; the two central drain lands are 0.60 × 1.00 mm. Its 3.0 × 3.0 mm courtyard is a project assumption: the maximum 2.075 mm body leaves 0.4625 mm per side, and the 2.30 mm vertical land extent leaves 0.35 mm per side. That supports the previous **XY box arithmetic only**. Actual adjacent routing, copper heat spread and pick-and-place clearances still need layout/assembler review.

The footprint has one pin-one silkscreen dot and a chamfered fabrication outline. Manufacturer data gives no separate stencil ratio or solder-mask reduction; the candidate currently places full-size paste and default mask on each land. The 0.15 mm copper gap between an edge row and central pad leaves little margin for mask/paste processing. An assembler must review stencil, mask slivers, voiding and reflow before population. No `Edge.Cuts`, 3D model or under-battery placement is asserted.

`python3 tools/check-dual-row-candidate.py` checks the independent expected pad map, geometry, layers, marker and courtyard. `tools/check-kicad.sh` renders the candidate through native KiCad alongside the existing library and runs the unchanged coupon ERC/netlist. These checks establish file consistency and loadability, **not** the proposed row circuit's electrical suitability or production readiness.

Validation on 2026-10-06: the candidate check found all eight lands with the intended duplicate drain numbers, layers, marker and 3 × 3 mm courtyard. KiCad CLI 10.0.6 exported the raw footprint views and the full project without error; the unchanged coupon still reported **zero ERC violations, 410 PCB items and 1,537 logical pins**. The candidate copper SVG was visually inspected against the Type B suggested-land drawing. No board or thermal measurement exists, and the numeric pin sequence and assembler process remain open for independent review.
