<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Coupon Rev A row-selector capture

Status: source capture and independent connectivity checks pass; native KiCad 10.0.6 ERC/XML/PDF review pending; not a fabrication release

## Scope

`rows.kicad_sch` adds the complete 1-of-16 high-side row-selection chain to the reviewed matrix and TLC59581 driver. The root now has six child sheets and seven pages. Controller GPIOs and the real VLED/3.3 V power circuits remain explicit global-label boundaries.

| References | Exact part / value | Function |
|---|---|---|
| U2 | `74HC4514PW,118` | Active-high 4-to-16 decoder; pin 23 `E` is active-low enable |
| Q1–Q16 | `DMP2066LSN-7` | P-channel high-side switches for rows 00–15 |
| Q17–Q32 | `2N7002K-7` | N-channel P-gate pull-down/level shifters for rows 00–15 |
| R6–R21 | `ERJ-2RKF1001X`, 1 kΩ ±1% | P-gate pull-ups to VLED |
| R22–R37 | `ERJ-2RKF1003X`, 100 kΩ ±1% | N-gate pull-downs |
| R38–R41 | `ERJ-2RKF1003X`, 100 kΩ ±1% | A0–A3 default-low pull-downs |
| R42 | `ERJ-2RKF1003X`, 100 kΩ ±1% | `ROW_ENABLE_N` default-high pull-up |
| C2 | `GRM155R71C104KA88D`, 100 nF, 16 V, X7R | U2 local decoupling |
| #FLG03 | virtual `PWR_FLAG` | Draft declaration that a future circuit supplies VLED |

Exact symbol, pin, footprint and controlled-datasheet evidence is in the [row library audit](row-library-audit.md) and [native library review](../../../docs/development/row-library-review-0c71860.md). These are candidate BOM lines, not purchasing authorization. Critical semiconductor lots require the exact MPN and traceable sourcing; Alibaba turnkey suppliers may quote them but may not substitute them. AliExpress remains development-only for these parts.

## Electrical contract

For row `nn`:

| Node | Required connections |
|---|---|
| `ROW_SEL_nn` | U2 `Qn`, Q(17+n) gate, R(22+n) pin 1 |
| `ROW_GATE_nn` | Q(1+n) gate, Q(17+n) drain, R(6+n) pin 2 |
| `ROW_nn_A` | Q(1+n) drain and all sixteen LED common anodes in row `nn` |
| VLED | every Q1–Q16 source and every R6–R21 pin 1 |
| GND | every Q17–Q32 source and every R22–R41 pin 2 |

U2 uses `ROW_A0` through `ROW_A3` in binary order. `LE` is tied high so the address path is transparent. `ROW_ENABLE_N` drives active-low pin 23: high forces all sixteen outputs low; low selects exactly one active-high output. U2 and C2 use `+3V3_APP`; C2 returns to GND.

References deliberately preserve a mechanical one-to-one pattern: row `n` uses P-MOS Q(1+n), N-MOS Q(17+n), 1 kΩ R(6+n), and 100 kΩ R(22+n). The checker rejects a correct-looking but swapped output, row, stage or physical pin.

## Default state and sequencing limits

With 3.3 V established and the controller high-impedance, R42 holds decoder enable high, R38–R41 hold the address at zero, every decoder output is low, R22–R37 hold every N-MOS gate low, and R6–R21 pull every P-MOS gate up to its source. All rows are therefore commanded off.

That statement is conditional; it is not a complete startup interlock. During rail ramp, power-down or an unpowered decoder, semiconductor states may be indeterminate. #FLG03 only prevents a false ERC missing-driver result. The future power sheet must inhibit the VLED converter in hardware until the application rail and control state are valid, and must remove VLED when the latching switch is off. Firmware must then use this break-before-make sequence:

1. drive `ROW_ENABLE_N` high;
2. wait for the selected P-MOS to turn off and row capacitance to discharge;
3. update `ROW_A0..A3`;
4. wait for decoder/address settling;
5. drive `ROW_ENABLE_N` low for the next row interval.

Dead-time values are not selected from schematic appearance. Gate B must measure U2 output timing, N/P-MOS edges, simultaneous-row overlap, row-anode discharge and visible low-gray ghosting. A watchdog/fault path must blank rows and disable VLED; firmware cannot replace the hardware-off default.

## Calculated loading and open device question

At the provisional 3.9 V VLED, one active stage draws approximately `3.9 V / 1 kΩ = 3.9 mA` through its P-gate pull-up, or about 15.2 mW. Only one row may be active. An asserted 3.3 V decoder output also loads its 100 kΩ N-gate pull-down by about 33 µA. These are nominal calculations, not measurements or guaranteed limits.

The `DMP2066LSN-7` has characterized low-voltage P-channel drive, but the `2N7002K-7` only guarantees RDS(on) at 5 V and 10 V. Here it sinks roughly 3.9 mA, not row current, but its drain-low voltage and switching edges at 3.3 V remain an explicit Gate A acceptance/replacement decision and Gate B measurement. The decoder land pattern remains IPC-derived because Nexperia does not publish a recommended board land pattern; it requires independent comparison and assembler DFM.

## Automated validation

`python3 tools/check-coupon-rows.py` checks the controlled libraries, root hierarchy, embedded-library equality, exact references/values/footprints, every default resistor and all row-sheet pin-to-net assignments. With `--netlist`, it checks the complete KiCad XML population: 335 PCB items and 1,290 physical pins across matrix, driver/support and row selectors. The wrapper now uses this comprehensive XML contract after ERC.

Thirty-seven regression tests pass, including injected decoder-output swaps, row-drain swaps, a missing pull-up, an enable pull-up moved to ground, duplicate pins, source-label changes, wrong values and missing hierarchy. `generate-coupon-rows.py` deterministically reproduces the initial row sheet only into a new directory; the canonical KiCad source remains editable and must never be overwritten by regeneration.

Source validation is not native KiCad parsing, ERC, DRC, simulation, drawing review, assembler DFM or measurement. The next required evidence is an owner KiCad 10.0.6 run.

## macOS validation

Close KiCad, then run from the repository root after the branch is published:

```bash
git fetch origin
git switch coupon-row-capture-rev-a
git pull --ff-only
git rev-parse --short HEAD

review_dir="hardware/coupon/rev-a/build/row-capture-review-$(git rev-parse --short HEAD)"
RGB_BADGE_KICAD_CHECK_OUTPUT="$review_dir" ./tools/check-kicad.sh
git status --short
```

If and only if the check succeeds, package the new directory:

```bash
ditto -c -k --keepParent "$review_dir" "$review_dir.zip"
open -R "$review_dir.zip"
```

Upload the ZIP and complete terminal output. Do not save the schematic in the GUI or disable an ERC/checker finding. The PDF should have seven pages. On page 7 confirm U2 and its five default resistors/decoupler are readable; all sixteen stages exist; each P-MOS source reaches VLED and drain reaches the matching `ROW_nn_A`; each P-gate uses the matching 1 kΩ pull-up and N-MOS drain; and no labels or fields collide badly enough to make a stage ambiguous.

## Next increment

After native acceptance, capture the ESP32-S3, programming/test interfaces and control defaults. The later power increment must replace #FLG01–#FLG03 with real sources and implement hardware VLED inhibition before any fabrication review.
