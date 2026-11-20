<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# USB permission logic: exact candidate libraries

Date: 2026-09-16. Status: manufacturer pin/package transcription, host checks and native rendering at `6d9a08b` complete; full electrical qualification pending. These libraries support ADR 0011, without changing its current limits or granting USB closure. The gate circuit is now captured; TPS3808 remains library-only.

## Controlled pin maps

Follow-on capture: [permission-capture.md](permission-capture.md) now connects the LVC gates in two staged sheets and adds the audited `SN74LVC2G17DBVR` dual Schmitt buffer. The TPS3808 supervisor remains library-only. The earlier library-only status and validation counts below are historical; native review now applies to the combined circuit checkpoint.

The table lists physical pin numbers in top-view package order. `Y` on the 1G06 and `RESET` on the TPS3808 are open-drain outputs, represented by KiCad's `open_collector` electrical type. NC is passive and must receive a no-connect marker when captured. Active-low inputs/outputs have inversion bubbles.

| Exact MPN | Intended use | Pins 1 → 6 | Footprint |
|---|---|---|---|
| SN74LVC1G00DBVR | NAND2 for attachment detection | A, B, GND, Y (inverted), VCC | SOT23_TI_DBV0005A |
| SN74LVC1G06DBVR | Open-drain inverter candidate for charger EN1 sink | NC, A, GND, Y (inverted, open drain), VCC | SOT23_TI_DBV0005A |
| SN74LVC1G08DBVR | AND2 qualification | A, B, GND, Y, VCC | SOT23_TI_DBV0005A |
| SN74LVC1G11DBVR | AND3 qualification | A, GND, B, Y, VCC, C | SOT23_TI_DBV0006A |
| SN74LVC1G32DBVR | OR2 source/request combination | A, B, GND, Y, VCC | SOT23_TI_DBV0005A |
| TPS3808G01DBVR | Adjustable supply supervisor candidate | RESET (inverted, open drain), GND, MR (inverted), CT, SENSE, VDD | SOT23_TI_DBV0006A |

The AND3 ground is **pin 2**, not the AND2's pin 3. The TPS3808 DBV map differs from the DRV/WSON map; no exposed pad exists on the selected DBV package. The existing SN74LVC1G04DBVR remains the push-pull inverter. Exact base MPNs appear in the source ordering tables; added `.A`, `.B`, E4/G4 and other suffixes are not automatically accepted substitutes.

## Package drawings and correction

DBV0006A drawing **4214840/G, 08/2024** appears in both the AND3 and supervisor sources. Copper/paste lands are 1.1 × 0.6 mm, corner radius 0.05 mm, with column centers x = ±1.3 mm and row centers y = −0.95, 0, +0.95 mm. Pins 1/2/3 run down the left; 4/5/6 run up the right. The new footprint explicitly uses 0.05 mm non-solder-mask-defined expansion and zero paste offset/ratio. The source's example stencil is 0.125 mm thick; final assembler stencil/process approval remains separate.

DBV0005A drawing **4214839/K, 08/2024** has the same lands, with no right-middle pad and pin 5 at the upper right. The earlier footprint's F.Fab rectangle was 2.9 × 3.2 mm rather than the nominal plastic-body envelope. This increment corrects **both** DBV footprints to a nominal 1.6 × 2.9 mm F.Fab body. Existing DBV5 copper/paste lands and pin numbering do not change. The rectangular courtyard is now 4.3 × 3.6 mm: at least 0.25 mm outside the 3.05 mm maximum body length and existing land extents. Pin-1 silk stays upper-left. Mask/process settings of the earlier DBV5 footprint are unchanged; final board/assembler rules must qualify them.

This is a newly found drawing issue in previously reviewed source, not a claim that the older native review checked this corrected outline. The new DBV5/DBV6 drawings and six symbols require native rendering at the next combined capture checkpoint.

## Circuit constraints retained for capture

- LVC input tolerance permits a correctly bounded BQ24392 CHG_DET signal to reach the 3.3 V logic without a conventional VCC-clamp path. Input and open-drain output operating limits still require a protected USB rail at or below 5.5 V; the charger's wider input range does not protect these devices.
- Partial-power-down Ioff ratings at VCC = 0 are not a guarantee of output logic during every intermediate supply voltage. Neither the supervisor library nor a Boolean READY signal proves that EN1 and the resistor boost remain inactive during ramp/brownout.
- TPS3808G01 has a nominal 0.405 V SENSE threshold, ±2% negative-going threshold accuracy over its full stated temperature range, up to 3% hysteresis and ±25 nA SENSE current at the threshold. Divider tolerances and both rising/falling thresholds must be calculated before capture; no divider is selected here.
- The supervisor's power-up-reset rating is conditional on load and supply rise time. Below its valid operating region, RESET cannot be assumed to enforce the whole circuit. Its 90-kohm typical internal MR pull-up is also not a precision external timing element.
- Evaluate supply supervision from the protected input domain so inhibition can precede the USB LDO's startup. Determine reset-release delay, detector initialization time and the physical inhibition path together. A default pull-down alone on a potentially driven gate output is insufficient proof.
- The parallel ILIM switch remains unselected. It needs bounded leakage and on resistance, and verified behavior with its supply absent. Do not repurpose the row 2N7002K solely from its threshold voltage; do not assume a precision analog switch's fail-safe logic input implies powered-off analog isolation.

These are capture constraints, not newly waived requirements. Complete VBUS current budgets, unconfigured/suspend behavior, transition timing, protection, thermal behavior and exact pack qualification remain open.

## Source record

Official PDFs downloaded and compared on 2026-09-16. Package, pin and ordering tables are the controlling source; these hashes identify the bytes reviewed, not a permanent guarantee that a live URL will remain unchanged.

| Source | Revision | SHA-256 |
|---|---|---|
| [SN74LVC1G00](https://www.ti.com/lit/ds/symlink/sn74lvc1g00.pdf) | SCES212AC, 2026-08 | `1264f79853e6119b66d60fe54f1f6e87995c12c00138bd820981fe68febb1063` |
| [SN74LVC1G06](https://www.ti.com/lit/ds/symlink/sn74lvc1g06.pdf) | SCES295AB, 2025-10 | `44dbca33c92d677ed71f99c2d1a2eb28f12d6fdb512e13fdf485444a3a42b4a4` |
| [SN74LVC1G08](https://www.ti.com/lit/ds/symlink/sn74lvc1g08.pdf) | SCES217AA, 2026-08 | `30b963cc44233cf3ca35c891ff987c8323a2244ecc765e23296ec96ca4b42666` |
| [SN74LVC1G11](https://www.ti.com/lit/ds/symlink/sn74lvc1g11.pdf) | SCES487I, 2024-11 | `ffd953703273b43844eae23cfbf31cfc801a3b9443f2c863d49dde62f5a9232b` |
| [SN74LVC1G32](https://www.ti.com/lit/ds/symlink/sn74lvc1g32.pdf) | SCES219W, 2026-08 | `b64786a568abe6a715c6f15dbc8ab1ffde3ad1017a1128a98931200e12c4c416` |
| [TPS3808](https://www.ti.com/lit/ds/symlink/tps3808.pdf) | SBVS050N, 2026-08 | `74d889c0f68af88032f1633c26381817cc03e10d9fd3b4c177a044ad3ed86eed` |

Pin tables: first five sources page 3; TPS3808 pages 4–5. DBV6 outline/land/stencil: AND3 PDF pages 21–23 and supervisor pages 36–38. DBV5 outline/land: NAND2 PDF pages 40–41. Source drawings were rendered and visually inspected. This does not substitute for inspecting KiCad's exports of our new source.

## Checks

`check-power-libraries.py` now audits the 32 added pins, output electrical types/inversions, DBV6 pads/mask/paste and both nominal body/courtyard outlines. Mutation tests reject the wrong AND3 ground number, swapped supervisor function, push-pull substitution for the open-drain inverter, incorrect logic polarity, duplicate right-side pad placement, wrong radius, mask/paste changes and recurrence of the oversized body drawing. `check-kicad.sh` requires all six additional native symbol exports and the DBV6 footprint exports. Wrapper tests use a stub and are not native ERC or rendering evidence.

Validation on 2026-09-16: all 114 host tests passed, including the 25 power-library and 17 wrapper tests. The 1,024-case permission contract, controller source check and `git diff --check` passed. The strict `check-power-design.py --require-usb-closure` gate still returns 1 for the recorded uncaptured/unqualified circuit. No KiCad CLI is available in this workspace; no new native ERC, render or bench result is claimed. Native export review is deferred to the next combined capture checkpoint, with no owner action needed for this increment.

## Native rendering evidence

The combined circuit/library exports at `6d9a08b` passed [first-author native review](../../../docs/development/permission-review-6d9a08b.md) on 2026-09-17, including all seven added symbols and corrected DBV5/DBV6 views. TPS3808 remains a library candidate; this does not qualify a supervisor circuit.
