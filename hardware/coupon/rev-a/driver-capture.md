<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Coupon Rev A TLC59581 driver capture

Status: first-author source/library audit complete; native KiCad 10.0.6 ERC, XML and rendering review pending. Not a fabrication release.

## Scope and component choices

`driver.kicad_sch` adds U1 and six local support components to the previously reviewed matrix. The root now has five child sheets and six pages total. The four matrix sheets are unchanged from `63afa77`.

| Reference | Exact MPN | Draft function |
|---|---|---|
| U1 | `TLC59581RTQT` | 48 sinks, one per colour/column; 3.3 V application supply |
| R1 | `ERJ-2RKF3922X` (Panasonic web spelling `ERJ2RKF3922X`) | 39.2 kΩ, ±1%, ±100 ppm/K, 0402; IREF to IREFGND/GND |
| R2–R5 | `ERJ-2RKF1003X` | 100 kΩ, ±1%, 0402; SIN/SCLK/LAT/GCLK pull-downs |
| C1 | `GRM155R71C104KA88D` | 100 nF, ±10%, 16 V, X7R, 0402; VCC decoupling |

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
| 42 | SOUT | `LED_SOUT`, future controller readback input; retain for diagnostic readback |
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

## Incomplete interfaces and ERC meaning

Two explicit **draft boundary PWR_FLAG symbols** declare `+3V3_APP` and `GND` as externally supplied for this circuit increment. They are virtual, excluded from the PCB/BOM, and labelled as assumptions on the sheet. A future successful ERC run verifies the captured circuit under those assumptions; it cannot prove a working power source. Remove/reconcile these flags when the actual source and return are captured. Do not change ERC severities or add blanket exclusions to hide a failure.

No TLC59581 /OE pin exists. The future row-inhibit and VLED-enable circuits must independently keep LEDs off during boot, reset, faults and programming. Unconnected controller-side signal labels are interfaces awaiting capture, not a completed startup design. R2–R5 pull SIN/SCLK/LAT/GCLK low while the controller is absent or high impedance. At 3.3 V each loads an asserted high by about 33 µA. The ±1 µA leakage specification explicitly covers SIN/SCLK, giving about 0.101 V with a worst-tolerance 100 kΩ resistor; verify LAT/GCLK behavior and all reset/power-sequencing states during review and bring-up. Pull-downs neither supply a clock nor guarantee row/VLED inhibition. Add any required signal conditioning during controller capture. The shared 3.3 V logic rail avoids a 5 V logic-level mismatch, but power sequencing and signal integrity remain future checks.

## Validation status

- All 57 U1 pins, all six support components, current value, 48 column assignments, pad numbering/geometry, paste segmentation and pin-1 marker pass source checks.
- The matrix check retains all 1,024 LED pin assignments. A separate complete-coupon XML check requires all 263 physical components and 1,093 physical pin assignments, including U1 exposed ground; it rejects missing or extra components and pins.
- 26 local regression tests pass, including deliberate output swaps, missing U1, missing exposed-pad connection, IREF shorts, a resistor decade error, mirrored pad placement and unsegmented thermal paste.
- Source-coordinate previews of the new sheet and footprint were inspected for gross placement errors. These use a simple independent drawing tool and are **not native KiCad render evidence**.
- No KiCad executable is available in the authoring environment. Native ERC, actual XML connectivity and all six PDF pages/new library SVGs still require the owner's KiCad 10.0.6 run. Keep this PR in draft until those results have been inspected.

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

After native driver review, capture the row decoder, level-shifted MOSFET stages and hardware inhibit/default-off behavior. Then capture the controller and power circuits, replace draft supply assumptions, and complete the timing/current/thermal and Gate A checks before fabrication.
