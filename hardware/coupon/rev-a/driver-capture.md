<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Coupon Rev A TLC59581 driver capture

Status: native KiCad 10.0.6 ERC, complete exported connectivity and six-page drawing review passed at `8e95eb0`. The earlier isolated-label warning is resolved. Not a fabrication release.

## Scope and component choices

`driver.kicad_sch` adds U1, six local support components and one bare PCB test pad to the previously reviewed matrix. The root now has five child sheets and six pages total. The four matrix sheets are unchanged from `63afa77`.

| Reference | Exact MPN | Draft function |
|---|---|---|
| U1 | `TLC59581RTQT` | 48 sinks, one per colour/column; 3.3 V application supply |
| R1 | `ERJ-2RKF3922X` (Panasonic web spelling `ERJ2RKF3922X`) | 39.2 kΩ, ±1%, ±100 ppm/K, 0402; IREF to IREFGND/GND |
| R2–R5 | `ERJ-2RKF1003X` | 100 kΩ, ±1%, 0402; SIN/SCLK/LAT/GCLK pull-downs |
| C1 | `GRM155R71C104KA88D` | 100 nF, ±10%, 16 V, X7R, 0402; VCC decoupling |
| TP1 | No MPN: PCB copper feature, excluded from BOM | 1 mm exposed copper probe pad on `LED_SOUT` |

These are draft exact-part selections, not an approved purchase BOM. TI's [part page](https://www.ti.com/product/TLC59581/part-details/TLC59581RTQT), [Panasonic's exact resistor page](https://industrial.panasonic.com/ww/products/pt/general-purpose-chip-resistors/models/ERJ2RKF3922X) [the pull-down resistor page](https://industrial.panasonic.com/ww/products/pt/general-purpose-chip-resistors/models/ERJ2RKF1003X), and Murata's reference sheet below document the parts. Obtain critical silicon through an authorized distributor or traceable assembler sourcing. Alibaba turnkey quotes must identify the same MPN and supplied package drawing; a marketplace listing alone does not settle the E/G distinction below. Existing AliExpress sourcing for case hardware/test leads remains applicable.

No row switches, inhibit circuit, controller, VLED regulator or power source are captured in this increment. It cannot operate as a display.

## Controlled documents

Retrieved 2026-09-07. Manufacturer PDFs are referenced by hash and are not redistributed.

| Document | Identity / inspected material | SHA-256 |
|---|---|---|
| [TI TLC59581 datasheet](https://www.ti.com/lit/gpn/TLC59581) | SLVSCZ9A, November 2015; electrical pp.3–9, 17–21; appended RTQ0056E/G drawings | `c7a736e612dc1ff55057c1c4aa0409e26d401881e6ddb1c65f57fe4b8bfe2cfc` |
| [Panasonic ERJ series](https://industrial.panasonic.com/cdbs/www-data/pdf/RDA0000/AOA0000C304.pdf) | ERJ-2R dimensions, rating and part-number scheme | `78825b819853a63f57cc18214f321d2f1da9dc205a7e58af7db18ae73563e378` |
| [Panasonic land patterns](https://industrial.panasonic.com/cdbs/www-data/pdf/RDM0000/DMM0000COL17.pdf) | 24-Dec-2025; p.1 rectangular 1005/0402 row | `fc707b230cce91d464bc3aaf1ed614fa5b412f40cbe7df7cab1541d2c164a882` |
| [Murata reference sheet](https://pim.murata.com/asset/pim4/ceramicCapacitorSMD/GRM155R71C104KA88-01A-EN_PDF_CERAMICCAPACITORSMD) | GRM155R71C104KA88-01A, 17-Jun-2026; p.2 exact specification; p.27 reflow lands | `530d3a4bf8e67af48379d3d027c23f87d1433a5c59abc51d313dada0d9e4b031` |

Both LED PDFs were retrieved again and match the hashes in the [LED audit](footprints/led-audit.md). Their ratings and power/temperature restrictions apply independently of the driver's nominal setting.

## Pin map

The table is transcribed from TI's pin-function table and top-view drawing. `OUTRn`, `OUTGn`, `OUTBn` connect to `COL_nn_R`, `COL_nn_G`, `COL_nn_B` respectively. The output numbering wraps around the package; it is not a simple sequence beginning at pin 1.

| Column n | OUTRn pin | OUTGn pin | OUTBn pin |
|---|---:|---:|---:|
| 00 | 8 | 9 | 10 |
| 01 | 11 | 12 | 13 |
| 02 | 14 | 15 | 16 |
| 03 | 17 | 18 | 19 |
| 04 | 20 | 21 | 22 |
| 05 | 23 | 24 | 25 |
| 06 | 30 | 31 | 32 |
| 07 | 33 | 34 | 35 |
| 08 | 36 | 37 | 38 |
| 09 | 39 | 40 | 41 |
| 10 | 44 | 45 | 46 |
| 11 | 47 | 48 | 49 |
| 12 | 50 | 51 | 52 |
| 13 | 53 | 54 | 55 |
| 14 | 2 | 3 | 4 |
| 15 | 5 | 6 | 7 |

| U1 pin | Function | Net / intent |
|---:|---|---|
| 1 | IREF | `LED_IREF`; R1 returns to pin 56 via a quiet ground route |
| 26 | SIN | `LED_SIN`, future controller data output |
| 27 | LAT | `LED_LAT`, future latch/command signal |
| 28 | SCLK | `LED_SCLK`, future serial clock |
| 29 | GCLK | `LED_GCLK`, future grayscale clock |
| 42 | SOUT | `LED_SOUT`, TP1 diagnostic probe pad and future controller readback input |
| 43 | VCC | `+3V3_APP`; C1 close to this pin and GND plane |
| 56 | IREFGND | `GND`; route R1 return here before joining noisy power return |
| 57 | GND_EP | Exposed pad, mandatory power ground and thermal connection |

Symbol pin 57 represents the physical exposed pad numbered 57 in TI's mechanical drawing. It is not an extra lead or an optional NC. The 48 sinks use KiCad's `open_collector` electrical type; VCC and the exposed power-ground pad use `power_in`. IREF/IREFGND are passive analog terminals. SOUT is an output; the four logic controls are inputs.

## Current calculation and its limits

Initial R1 is **39.2 kΩ ±1%**, below TI's suggested 60 kΩ noise-immunity ceiling. The draft uses TI Equation 2 and the numeric **GAIN** column of Table 2:

`I_nominal(mA) = 1.209 V × GAIN(BC) / R_IREF(kΩ) × CC/511`

| Calculated condition | Current per enabled colour channel |
|---|---:|
| Maximum register settings: BC=7, CC=511 | 4.8545 mA nominal |
| Same settings; resistor tolerance only | 4.8064–4.9035 mA |
| BC=4, CC=511 | 3.1397 mA nominal |
| Power-on register values BC=4, CC=256, if subsequently enabled | 1.5729 mA nominal |
| BC=0, CC=511 | 0.6292 mA nominal; below the advertised 1 mA accuracy range |

The outputs themselves power up off; the register-value calculation is not a claim that they illuminate at power-up. Lower current settings need coupon characterization; do not assume the published accuracy at sub-mA settings. Brightness remains a fixed user choice during playback; this does not introduce automatic dimming.

At maximum nominal settings, one active 16-pixel white row draws `48 × 4.8545 mA = 233.02 mA` from VLED, excluding driver logic consumption. One LED die averages at most `0.3034 mA` with ideal 1:16 scanning before PWM and blanking. R1 nominal dissipation is only `37.29 µW`. These are calculations, not measurements or complete power/thermal budgets.

**This is not a guaranteed 4.85 mA ceiling.** TI gives VIREF=1.19–1.228 V under the stated 6.2 kΩ / BC=0 / CC=129 test condition, and its current-error figures also have specific test conditions; resistor tolerance alone does not bound the actual current across temperature, supply and output voltage. R1 TCR adds up to 0.6% resistance change over a 60 K shift. The gain-ratio column also contains apparent errors (BC=2 and BC=3), and Table 1's 7.41 kΩ / 25 mA example differs from Equation 2 with the printed VIREF/gain. Use the stated equation consistently for this draft; confirm the discrepancy with TI or independent review and measure current before qualifying a limit.

The selected current is close to, and slightly below, the plan's provisional 5 mA red-channel assumption. It is not permission to increase the hardware limit later. Everlight's blue die has a particularly restrictive 20 mW power rating at 25°C; its printed DC and pulse-current ratings also need conservative interpretation. For illustration, 4.855 mA × 3.4 V is about 16.5 mW before tolerance and temperature derating. Gate A must evaluate worst-case LED current/power and temperature; Gate B must measure optical output, regulation and thermal behavior. Do not use a 1:16 average to waive the instantaneous ratings or stalled-row case.

## Footprint and layout audit

All coordinates use KiCad's top view: +X right, +Y down.

### U1: provisional RTQ0056E

TI appends **two** RTQ variants to the same datasheet. E uses a 5.7 mm nominal exposed pad; G uses 5.6 mm. The public generic RTQ package view does not identify the supplied lot's variant. The schematic selects a clearly named **E-only provisional footprint**; it does not claim to support both variants automatically.

Transcription follows **RTQ0056E, 4224191/A, 03/2018**, PDF pages 27–29:

- Body: nominal 8 × 8 mm; manufacturer body maximum 8.15 mm; height maximum 1.0 mm.
- Leads: 56 at 0.5 mm pitch, each copper land 0.60 × 0.24 mm, with 0.05 mm corner radius. Opposing land centre lines are 7.8 mm apart.
- Left pins 1–14: X=−3.9; Y=−3.25…+3.25. Bottom pins 15–28: Y=+3.9; X=−3.25…+3.25. Right pins 29–42 and top pins 43–56 run in the reverse coordinate direction.
- Exposed copper pad 57: 5.7 × 5.7 mm at the origin, with mask opening and **no full-size paste aperture**.
- Paste: 16 rounded 1.15 × 1.15 mm apertures, centres at X/Y=−2.025, −0.675, +0.675, +2.025 mm. About 65% exposed-pad paste coverage, following TI's 0.125 mm stencil example.
- Courtyard: ±4.45 mm, allowing 0.25 mm beyond the outer lead lands. Fabrication outline has a pin-1 chamfer; silk has a pin-1 dot outside copper.
- Thermal vias are **not yet placed**. PCB layout must connect pad 57 solidly to ground with the reviewed heat-spreading/via arrangement; assembler must approve via fill/tenting and paste/mask settings.

Before layout release or ordering, obtain the supplier's lot/package drawing and either confirm E or audit and select a separate G footprint. Do not silently resize this pad or substitute the package drawing. Gate A covers this open item.

### R1–R5 and C1

The resistors and capacitor are nonpolar two-terminal parts, with pin 1 left and pin 2 right for consistent schematic/PCB references.

| Footprint | Body | Chosen land geometry | Manufacturer range checked |
|---|---|---|---|
| Panasonic ERJ2 0402 | 1.0 × 0.5 mm | 0.50 × 0.50 mm pads, centres X=±0.50 mm | Gap a=0.50 mm, outside span b=1.50 mm, width c=0.50 mm; within Panasonic's a=0.5–0.6, b=1.4–1.6, c=0.4–0.6 |
| Murata GRM15 0402 | 1.0 × 0.5 mm | 0.40 × 0.50 mm pads, centres X=±0.40 mm | Gap a=0.40 mm, each land b=0.40 mm, width c=0.50 mm; within Murata's reflow ranges a=0.3–0.5, b=0.35–0.45, c=0.4–0.6 |

Each footprint has individual copper/paste/mask lands and a 2.0 × 1.0 mm courtyard. Paste, mask and placement remain subject to assembler DFM. C1 is local high-frequency decoupling; it does not replace the regulator output capacitors or VLED bulk capacitance.

### TP1: readback probe pad

`TestPoint_Pad_D1.0mm` is a project-defined PCB feature, not a purchased component. Pad 1 is a 1.0 mm diameter SMD circle at (0, 0), on F.Cu and F.Mask, with no F.Paste aperture and excluded from assembly position files; its circular courtyard is 1.5 mm diameter. The symbol is passive, included on the board and excluded from the BOM, with an intentionally empty MPN. This adds physical probe access to U1 pin 42 without an assembled header. PCB layout must keep the pad accessible and the SOUT route short. The controller readback connection is still to be captured.

## Incomplete interfaces and ERC meaning

Two explicit **draft boundary PWR_FLAG symbols** declare `+3V3_APP` and `GND` as externally supplied for this circuit increment. They are virtual, excluded from the PCB/BOM, and labelled as assumptions on the sheet. A future successful ERC run verifies the captured circuit under those assumptions; it cannot prove a working power source. Remove/reconcile these flags when the actual source and return are captured. Do not change ERC severities or add blanket exclusions to hide a failure.

No TLC59581 /OE pin exists. The future row-inhibit and VLED-enable circuits must independently keep LEDs off during boot, reset, faults and programming. Unconnected controller-side signal labels are interfaces awaiting capture, not a completed startup design. R2–R5 pull SIN/SCLK/LAT/GCLK low while the controller is absent or high impedance. At 3.3 V each loads an asserted high by about 33 µA. The ±1 µA leakage specification explicitly covers SIN/SCLK, giving about 0.101 V with a worst-tolerance 100 kΩ resistor; verify LAT/GCLK behavior and all reset/power-sequencing states during review and bring-up. Pull-downs neither supply a clock nor guarantee row/VLED inhibition. Add any required signal conditioning during controller capture. The shared 3.3 V logic rail avoids a 5 V logic-level mismatch, but power sequencing and signal integrity remain future checks.

## Validation status

- All 57 U1 pins, all six support components, TP1 probe connection, current value, 48 column assignments, pad numbering/geometry, paste segmentation and pin-1 marker pass source checks.
- The matrix check retains all 1,024 LED pin assignments. A separate complete-coupon XML check requires all 264 PCB items (263 components plus TP1) and 1,094 physical pin assignments, including U1 exposed ground; it rejects missing or extra components and pins.
- 27 local regression tests pass, including deliberate output swaps, missing U1, missing exposed-pad connection, IREF shorts, a resistor decade error, mirrored pad placement, unsegmented thermal paste and a missing SOUT probe connection.
- Source-coordinate previews of the new sheet and footprint were inspected for gross placement errors. These use a simple independent drawing tool and are **not native KiCad render evidence**.
- Owner KiCad 10.0.6 at `8e95eb0` passed ERC and complete native XML validation. The uploaded XML was checked again in the authoring environment; all six PDF pages and corrected library SVGs passed first-author visual review. Native evidence is recorded below. No circuit changes were required after this run.

## Native evidence at `55706f0` and correction

Owner run on 2026-09-08, KiCad 10.0.6 on macOS. The supplied `driver-review-55706f0.zip` has SHA-256 `2f40c7388ebe4d47bf7be9a7d53aee5acbe753c97ff2470635ff607ddd78dbd2`; its `coupon-erc.rpt` has SHA-256 `14e4194be595ae9300ffd45771425f84a31de6fb90e650c7b6cc7e46703b6ff1`.

ERC reported **0 errors and 1 warning**, `isolated_pin_label`, for `LED_SOUT` at (99.06, 116.84) mm. Only U1 pin 42 was on that labelled net; the controller readback input has not yet been captured. The wrapper correctly stopped at ERC, so this archive contains no exported XML or schematic PDF. The Fontconfig message is separate from this electrical warning.

The correction connects TP1 pin 1 to `LED_SOUT`, retaining both diagnostic access and the future controller interface. ERC severity and exclusions are unchanged. A regression first failed for the missing TP1 connection; it now passes and rejects removal of that connection from the synthetic complete netlist. This is source/fixture evidence, not a substitute for a native ERC rerun.

The uploaded native driver/support symbol SVGs and QFN/resistor/capacitor footprint views were inspected on a white background. U1 labels are legible; copper views show separate perimeter lands and the QFN paste view shows the intended 4 × 4 thermal aperture array. The combined fabrication view overlays the body outline on some pad numbers, so it is not sufficient on its own to read every QFN number; use the source pin/pad audit alongside the separate copper view. Support symbols showed visible placeholder pin names, the flag's pin text overlapped its body, and the capacitor value crowded the plates. The correction hides those non-informative pin names (and the virtual flag pin number) and increases capacitor field spacing, consistently in the library and cached schematic. Pin number/type/net contracts are unchanged by those presentation edits. Symbol visibility syntax follows [KiCad's format documentation](https://dev-docs.kicad.org/en/file-formats/sexpr-intro/index.html#_symbols).

The corrected symbol SVGs, new TP1 footprint, ERC, native XML and complete schematic PDF were reviewed in the subsequent `8e95eb0` run below. No hardware has been built or measured.

## Native acceptance at `8e95eb0`

Owner run on 2026-09-08, KiCad 10.0.6 on macOS arm64, source commit `8e95eb0e5106a4431a567d05cac70f105eff25a2`. Terminal output reports successful library exports, zero ERC violations, both native XML checks passing and a complete PDF export; `git status --short` showed no changes. Reviewed upload: `driver-review-8e95eb0.zip`.

| Evidence | SHA-256 |
|---|---|
| Uploaded ZIP | `c661b9238ffd99e4f8cdc19b42b71eb982e5c28f37261c396876dfdcd1e70035` |
| `coupon-erc.rpt` | `1e5ab931d35611653e118ec80ef19bbd101ebe36e323abd42264c6360d175aa3` |
| `coupon-matrix.xml` | `3dcffc155412eb5c784a0592a48ce2a415cc9606e032a516731b2dc6d2ef9563` |
| `coupon-schematic.pdf` | `3933f22e17387447f8fc6816eda5b794af77f755cc3a7ccae20e82989803e0bc` |

The report contains **0 errors, 0 warnings, 0 ERC messages**. Its four ignored check categories are unchanged from the prior run: global-label uniqueness, four-way junctions, SPICE models and footprint filters. In particular, `isolated_pin_label` was not disabled. The draft power-boundary assumptions still apply.

Both validators were rerun against the actual uploaded XML and passed: 256 LEDs / 1,024 LED pins, and 264 PCB items / 1,094 total physical pins. This confirms that TP1 remains in the electrical netlist despite being excluded from the purchase BOM.

First-author visual review used Poppler-rendered pages and white-background renders of the native SVG exports:

- Page 1: five child-sheet boxes, filenames and project status fit within the border and title block.
- Pages 2–5: all four 64-LED matrices retain separated symbol, reference and net-label placement; page numbering and revision fields fit. Their historical matrix-only title-block note still mentions driver capture as pending; the root and driver page carry the current circuit scope. This stale note is cosmetic and should be refreshed with the next schematic increment.
- Page 6: all U1 output labels, IREF return, decoupling, four logic pull-downs, TP1, exposed-ground connection and explicit draft supply flags are legible without overlapping wiring or notes.
- Corrected resistor/capacitor/flag SVGs: placeholder names no longer obscure symbol graphics, and the capacitor value clears the plates. TP1's symbol and numbered pad are readable.
- TP1 footprint: a single round copper pad; its paste export is intentionally blank. The combined fabrication view places the reference close to the courtyard, so final PCB reference placement remains a layout task. The prior QFN combined-view pad-number limitation remains as recorded above; native copper/paste views and the controlled pin/pad audit are the applicable geometry evidence.

Disposition: driver capture passes this source-design milestone and is eligible to merge. The acceptance commit changes documentation only; KiCad sources, libraries and validation tools remain exactly those checked at `8e95eb0`. No further owner rerun is required for this documentation update. Independent Gate A review, package-variant confirmation, current/thermal qualification and all uncaptured circuitry remain open before fabrication.

## macOS validation

Close KiCad. From the repository root:

```bash
git fetch origin
git switch coupon-driver-rev-a
git pull --ff-only
git rev-parse --short HEAD
review_dir="hardware/coupon/rev-a/build/driver-review-$(git rev-parse --short HEAD)"
RGB_BADGE_KICAD_CHECK_OUTPUT="$review_dir" ./tools/check-kicad.sh
git status --short
```

If the check succeeds, package it:

```bash
ditto -c -k --keepParent "$review_dir" "$review_dir.zip"
open -R "$review_dir.zip"
```

Upload the ZIP and terminal output. The output directory must be new. Despite its historical name, `coupon-matrix.xml` now contains the complete captured circuit; both matrix and driver validators check it. The PDF has six pages. The new paste view should show 16 separate apertures over the thermal pad. If the check fails, share the complete output; do not disable a check to obtain a pass.

## Next increment

The row decoder and all level-shifted MOSFET stages are now in the separate [row-capture increment](row-capture.md). After its native review, capture the controller and power circuits, replace draft supply assumptions, and complete the timing/current/thermal and Gate A checks before fabrication.
