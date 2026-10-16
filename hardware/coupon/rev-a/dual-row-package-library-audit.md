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

**2026-10-13 owner-supplied source check:** The owner supplied a local copy of DS36128 Rev. 7-2 (SHA-256 `441380f483b7a88c204f521248f7822e57221e0bdedeaa1d29fdc505188cda18`). Direct visual inspection of page 1 confirms the bottom-view pin-one arrow at `S1`, the separate `D1`/`D2` islands, and the labelled `G1`, `G2`, `S1`, `S2` terminals. Page 9 confirms the Type B outline and suggested-land dimensions transcribed below. The drawing does **not** print numbers 2–6, so this source check does not independently resolve their numeric sequence. Keep the candidate unconnected until that sequence is checked against another authoritative manufacturer source or an exact-part sample.

The [candidate KiCad footprint](footprints/rgb-badge-coupon.pretty/U-DFN2020-6_TypeB_Diodes_DMC1229UFDB.kicad_mod) transcribes the suggested `X=0.35`, `Y=0.50`, `X1=0.60`, `Y1=1.00`, `C=0.65`, `G=0.15`, `G1=0.45`, `X2=1.65` and `Y2=2.30 mm`. The six edge lands are 0.35 × 0.50 mm; the two central drain lands are 0.60 × 1.00 mm. Its 3.0 × 3.0 mm courtyard is a project assumption: the maximum 2.075 mm body leaves 0.4625 mm per side, and the 2.30 mm vertical land extent leaves 0.35 mm per side. That supports the previous **XY box arithmetic only**. Actual adjacent routing, copper heat spread and pick-and-place clearances still need layout/assembler review.

The footprint has one pin-one silkscreen dot and a chamfered fabrication outline. Manufacturer data gives no separate stencil ratio or solder-mask reduction; the candidate currently places full-size paste and default mask on each land. The 0.15 mm copper gap between an edge row and central pad leaves little margin for mask/paste processing. An assembler must review stencil, mask slivers, voiding and reflow before population. No `Edge.Cuts`, 3D model or under-battery placement is asserted.

The current coupon project netclass clearance is **0.20 mm**, greater than the manufacturer's **0.15 mm** suggested gap between each edge row and the drain land. Thus this footprint cannot be populated under the current global rule without a reviewed local exception or a different land pattern/package. Do not silently reduce the board-wide rule or claim DRC approval from this source audit.

As a manufacturing screen only, [JLCPCB's published capabilities](https://jlcpcb.com/capabilities/pcb-) list 0.15 mm minimum SMD pad-to-pad clearance for different nets and 0.10 mm minimum 1 oz trace/space; their 2 oz, two-layer trace/space figure is 0.16 mm and their 2 oz solder-mask bridge calls for 0.20 mm pad spacing. Thus a 1 oz, locally reviewed 0.15 mm rule is a plausible direction for this suggested land pattern, whereas 2 oz cannot be assumed to work. Exact stackup, solder mask, assembly process and a manufacturer design review remain open; these generic capability numbers are not approval of this footprint.

`python3 tools/check-dual-row-candidate.py` checks the independent expected pad map, geometry, layers, marker and courtyard. `tools/check-kicad.sh` renders the candidate through native KiCad alongside the existing library and runs the unchanged coupon ERC/netlist. These checks establish file consistency and loadability, **not** the proposed row circuit's electrical suitability or production readiness.

Validation on 2026-10-06: the candidate check found all eight lands with the intended duplicate drain numbers, layers, marker and 3 × 3 mm courtyard. KiCad CLI 10.0.6 exported the raw footprint views and the full project without error; the unchanged coupon still reported **zero ERC violations, 410 PCB items and 1,537 logical pins**. The candidate copper SVG was visually inspected against the Type B suggested-land drawing. No board or thermal measurement exists, and the numeric pin sequence and assembler process remain open for independent review.

## Separate onsemi numbered-pin candidate, 2026-10-14

The exact alternate is onsemi `NTLJD3119CTBG`, not a substitution for the Diodes part. The [manufacturer datasheet NTLJD3119C/D Rev. 6](https://www.onsemi.com/pdf/datasheet/ntljd3119c-d.pdf) downloaded for this audit has SHA-256 `12862a6e03c7ae750dd75e9f860c79ef859582fd147b97bdb973c5144990e997`. Its page-1 **top-view** diagram explicitly maps 1 = N source S1, 2 = N gate G1, 3 = P drain D2, 4 = P source S2, 5 = P gate G2, and 6 = N drain D1. Page 10 identifies WDFN6 CASE 506AN and a 2 × 2 mm body with 0.80 mm maximum height. The page-10 recommended mounting footprint is **solder-mask defined**.

The [separate candidate footprint](footprints/rgb-badge-coupon.pretty/WDFN6_2x2_onsemi_NTLJD3119C.kicad_mod) rotates the onsemi mounting drawing into KiCad's top view with pin 1 upper left. Six perimeter lands are 0.45 × 0.39 mm on two vertical columns (0.65 mm pitch); the two exposed-drain lands are 1.10 × 0.82 mm and duplicate pad numbers 6 (D1, upper) and 3 (D2, lower). Its 3 × 3 mm courtyard is a project assumption. The nearest nominal copper gaps are 0.15 mm from perimeter to exposed pad and 0.18 mm between the exposed pads, both below the current 0.20 mm board clearance rule. This alternate therefore **does not remove the fine-pitch process decision**. KiCad CLI 10.0.6 loaded and exported the footprint SVG, and the copper/marker/fabrication outline were visually inspected against both manufacturer pages.

Mask and paste in this first-author footprint still use KiCad's default pad openings. They do **not** implement onsemi's solder-mask-defined recommendation; the actual mask aperture, paste ratio and assembler process must be chosen before population. A [separate symbol and 16-row trial schematic](staging/onsemi-row-candidate/README.md) now exercise this exact pin map without changing the canonical row sheet or BOM. No populated board, mechanical-height fit or independent review exists. The explicit onsemi numeric map must never be used as proof of the Diodes map or as permission to populate one part on the other's footprint.
