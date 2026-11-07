<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Replacement power libraries: native review c054cb4

Status: **passed for first-author library rendering review** on 2026-09-15. No correction or repeat owner run is required for this checkpoint. This accepts the three libraries for schematic development, not the uncaptured power circuit or fabrication.

## Evidence

The owner ran KiCad 10.0.6 at `c054cb40642c67d8c6a034ccca88fc529a27aea5` and supplied the complete export ZIP and terminal transcript. The transcript ends with successful exports and no `git status --short` output. AppleDouble metadata was excluded from inspection.

| File | SHA-256 |
|---|---|
| `power-replacement-review-c054cb4.zip` | `8130a80713495c2cbb381d956e6612e4a258d0c1e00d636e7d072e892cb0d6d7` |
| `Pasted text(10).txt` | `adb2923b248c220744b48682fbf7098ce505ef31e7e1d9ab99672336ad02f021` |
| `coupon-erc.rpt` | `00523084a2eba06cfc967898344dd303dd3ed12d34b9e2f31100f5dffdf217ab` |
| `coupon-matrix.xml` | `2aa7dd622f8b8e2c53e3440ab7c92c00439e4c6cc973eadf112e76f470a3a618` |
| `coupon-schematic.pdf` | `7202e1b131e10a776216ca5ae6c3598807e8039235f7e43a3b4ccbbd50f7fe90` |

The bundle contains 32 symbol SVGs, 24 footprint SVGs in each of fabrication, copper, paste and mechanical views, two derived numbered LED SVGs, the ERC report, XML netlist and eight-page schematic PDF. The assistant rendered the three new symbols, their nine fabrication/copper/paste views and all eight schematic pages. Separate enlarged copper renders resolve the narrow RSE pads. Geometry was compared with the TI sources identified in the [replacement audit](../../hardware/coupon/rev-a/power-replacement-library-audit.md), including the RGT and both RSE stencil drawings.

## Results

- The supplied ERC report passes the strict report checker: zero errors and exactly the two allowed isolated `USB_D-` / `USB_D+` boundary warnings. These remain because the USB/input sheet is not captured. The recurring Fontconfig warning did not prevent export.
- The supplied XML passes the complete controller netlist checker: 356 PCB items and 1,360 logical pins. The three new ICs are correctly absent from this library-only checkpoint.
- The power-library source checker passes all pin and land-map checks, including the 35 replacement pins, narrower RSE middle lands, 0.05 mm corner radii and separated copper.
- BQ24074 shows distinct BAT pins 2/3, OUT pins 10/11, ground pin 8 and exposed-pad pin 17. CE has its inversion bubble. Reference, value and pin text are readable.
- BQ24392 preserves separate connector and host data pairs, GOOD_BAT, SW_OPEN, CHG_DET and active-low CHG_AL_N. TS3USB31E preserves the D/HSD pair distinction, active-low OE and explicit NC pin 7. No new symbol-heading collision was found.
- RGT copper shows sixteen separated perimeter lands and the central exposed pad; paste shows the smaller central aperture. The audited dimensions remain 1.68 mm copper and 1.55 mm paste, approximately 85% coverage. The external pin-one dot is correctly placed beside pad 1.
- RSE10 has four side pads per side, including two narrower middle pads per side, plus the top and bottom lands. Its fabrication body is correctly taller than it is wide. RSE8 has three side pads per side with narrower middle pads, plus the top and bottom lands. Copper and paste stay separate between all neighboring lands. Both external pin-one marks agree with the manufacturer orientation.
- Small perimeter pad numbers overlap body outlines in the combined fabrication exports. These views are useful for body/orientation inspection; the separate copper/paste views and audited source pad map provide the geometry and numbering evidence. No footprint geometry change is needed for this plotting limitation.
- All eight existing schematic pages retain readable layout with no new overlap or missing circuit block found. The root still explicitly identifies USB/input, charging and switched power as pending.

## Disposition

Close the replacement-library native-rendering blocker. The next implementation work is the VBUS-powered source-priority and level-translation circuit, followed by charger, gauge and switched-power capture. Keep the strict USB-closure gate failing until the real circuit and its remaining proof are complete.

After updating the blocker wording, all 15 power-design regression tests passed; `check-power-design.py --require-usb-closure` still returned 1 for the documented unfinished circuit. `git diff --check` passed. No KiCad source changed in this review-record commit.

The exact pack/NTC/timer qualification, auxiliary USB current budget and source transitions, charger thermal performance, shared stencil process, USB4505 cutout/stack-up qualification, PCB layout and independent Gate A review remain open. PR #8 remains draft. This review provides no purchasing or fabrication release.
