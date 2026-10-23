<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Native permission-circuit review: 6d9a08b

Reviewed 2026-09-17. Result: **first-author native electrical and rendering review passed** for the staged USB logic boundary. This is not a complete power-system review, bench evidence, or Gate A approval.

## Evidence

The owner supplied `permission-review-6d9a08b.zip` and its terminal transcript after running KiCad 10.0.6 on macOS/arm64 at `6d9a08bac0fe398e27003aedea8f0194a28fd699`. The reported working tree was clean. The archive contains native ERC, XML, a ten-page schematic PDF, 39 symbol SVGs and 25 footprint SVGs in each fabrication/copper/paste/mechanical view. AppleDouble metadata files are excluded from these counts.

| Artifact | SHA-256 |
|---|---|
| Uploaded ZIP | `d9abe52d3f284b938f5d48c23d52405b0d65d0fc5a55bd40b40e950735931d52` |
| coupon-schematic.pdf | `980ffcf8cdf23f19144e196cb93c2248ec37f5c6fea8a8fa53cf9492c240255f` |
| coupon-erc.rpt | `0c831589169d8d8bab92ce75a0619fe65fcc91a2b8cd2e9ac1ff008b8fd145ec` |
| Native XML netlist | `bd8e748f894bd5fab5d6fbd759c9a579d3e2fb986c80be34e1e72140dc93733c` |

The supplied ERC and XML were rechecked against the source at this commit. ERC has zero errors and exactly the two previously approved isolated USB_D-/USB_D+ boundary labels. Complete XML connectivity passes **417 PCB items / 1,536 physical/logical pins**, including explicit NC pins. This native evidence is separate from the host-only 1,024-state truth-table evaluation and synthetic CLI fixtures.

## Rendering inspection

The actual ten-page PDF was rendered and inspected: overview of all pages, with closer inspection of the root, driver, row, controller and two new USB logic pages. The new input-conditioning and permission sheets have readable gate groups, separate defaults/decoupling, outward-facing net labels and identifiable test boundaries. Enlarged title-block inspection confirmed that the long staged-boundary note fits within the border.

The seven new symbols were inspected: SN74LVC1G00DBVR, SN74LVC1G06DBVR, SN74LVC1G08DBVR, SN74LVC1G11DBVR, SN74LVC1G32DBVR, TPS3808G01DBVR and SN74LVC2G17DBVR. Numbered inputs/outputs, inversion bubbles, supply positions and heading clearance agree with the controlled library audit. The supervisor remains library-only.

Native DBV5 and DBV6 fabrication/copper/paste/mechanical views show the corrected tall nominal body, counter-clockwise pad numbers, separated copper lands, matching signal-paste apertures, pin-one marker and enclosing courtyard. These exports validate rendering and transcription; the dimension checks remain in the library checker. No new first-author rendering finding was identified.

## Remaining boundary

The result accepts the captured gate network and its libraries, not its uncaptured external circuit. Detectors, real USB-only supply, supervisors, switch/application inputs, startup/brownout inhibition, charger controls and ILIM boost switch still require capture and qualification. R70 is a raw logic-output pull-up, not proof of charger standby during power ramp. Full USB current/transition budgets, battery/NTC, thermal validation, layout and independent Gate A remain open. PR #8 stays draft while power capture is incomplete.
