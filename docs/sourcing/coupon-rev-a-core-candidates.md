<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Coupon Rev A core component candidates

Status: researched candidates for schematic capture; **not a frozen BOM and not authorization to buy or fabricate**

Research cut-off: 2026-09-14 for the selected charger/input sources; 2026-09-06 for other candidates

## How to read this record

An exact MPN in this document means that its public documentation, package and at least one traceable purchase route were found. It does not mean its symbol, footprint, thermal design, surrounding passives, availability or use in this circuit has passed Gate A. Stock counts and prices are intentionally not frozen here because they can change between research and quotation.

Before schematic capture, every selected part receives a project-local symbol and footprint checked against the linked manufacturer drawing. Before release, the assembler must quote the exact MPN and disclose its source; no equivalent or house substitution is allowed without written review.

## Core silicon and switching

| Function | Exact schematic candidate | Package / implementation note | Manufacturer evidence | Traceable sample source | State |
|---|---|---|---|---|---|
| MCU and BLE | `ESP32-S3-WROOM-1U-N16R8` | External-antenna module; 16 MB flash, 8 MB octal PSRAM | [Espressif module datasheet](https://documentation.espressif.com/esp32-s3-wroom-1_wroom-1u_datasheet_en.pdf) | [DigiKey](https://www.digikey.com/en/products/detail/espressif-systems/ESP32-S3-WROOM-1U-N16R8/16162641) | [Exact library and controller source captured](../../hardware/coupon/rev-a/controller-capture.md); [native review passed](../development/controller-review-d56e1aa.md) |
| 48-channel LED sink | `TLC59581RTQT` | 56-pin `RTQ` QFN, 8 × 8 mm; one on coupon, three on final badge | [TI datasheet](https://www.ti.com/lit/gpn/TLC59581) | [DigiKey](https://www.digikey.com/en/products/detail/texas-instruments/TLC59581RTQT/6571953) | [Driver captured](../../hardware/coupon/rev-a/driver-capture.md); provisional RTQ0056E footprint; confirm supplied E/G variant |
| Standalone charger / power path | `BQ24074RGTR` | 16-pin `RGT` VQFN, 3 × 3 mm; linear PowerPath with hardware standby/100/500/external modes | [TI datasheet](https://www.ti.com/lit/gpn/BQ24074) | [DigiKey](https://www.digikey.com/en/products/detail/texas-instruments/BQ24074RGTR/2047269) | Selected by ADR 0010; exact library, circuit and thermal review pending |
| Historical charger library | `BQ25616JRTWT` | 24-pin `RTW` WQFN, JEITA variant | [TI datasheet](https://www.ti.com/lit/gpn/BQ25616) | [DigiKey](https://www.digikey.com/en/products/detail/texas-instruments/BQ25616JRTWT/11570504) | Exact library/native render passed, but direct input topology rejected by ADR 0009; not selected for capture |
| BC1.2 detector / USB data switch | `BQ24392RSER` | 10-pin `RSE` UQFN, 2.05 × 1.55 mm; VBUS-powered | [TI datasheet](https://www.ti.com/lit/gpn/BQ24392) | [DigiKey](https://www.digikey.com/en/products/detail/texas-instruments/BQ24392RSER/3471183) | Selected by ADR 0010; exact library and level/priority circuit pending |
| Application USB data isolator | `TS3USB31ERSER` | 8-pin `RSE` UQFN, 1.5 × 1.5 mm; switched-rail power and partial-power-down isolation | [TI datasheet](https://www.ti.com/lit/gpn/TS3USB31E) | [DigiKey](https://www.digikey.com/en/products/detail/texas-instruments/TS3USB31ERSER/2071792) | Selected by ADR 0010; exact library and high-speed routing pending |
| USB-C CC detector | `TUSB320LAIRWBR` | 12-pin `RWB` X2QFN; fixed UFP, GPIO mode | [TI datasheet](https://www.ti.com/lit/gpn/TUSB320LAI) | [DigiKey](https://www.digikey.com/en/products/detail/texas-instruments/TUSB320LAIRWBR/5722618) | [Exact library/native render passed](../../hardware/coupon/rev-a/power-library-audit.md); current-state circuit review pending |
| USB-only 3.3 V rail | `TLV75533PDBVR` | 500 mA SOT-23-5 LDO from VBUS; powers CC detector and its logic while application rails are off | [TI datasheet](https://www.ti.com/lit/gpn/TLV755P) | [DigiKey](https://www.digikey.com/en/products/detail/texas-instruments/TLV75533PDBVR/9356541) | [Exact library/native render passed](../../hardware/coupon/rev-a/power-library-audit.md); circuit pending |
| CC-state inverter | `SN74LVC1G04DBVR` | SOT-23-5; same USB-only 3.3 V rail | [TI product and ordering page](https://www.ti.com/product/SN74LVC1G04/part-details/SN74LVC1G04DBVR) | [DigiKey](https://www.digikey.com/en/products/detail/texas-instruments/SN74LVC1G04DBVR/385716) | [Exact library/native render passed](../../hardware/coupon/rev-a/power-library-audit.md); circuit pending |
| 3.3 V application rail | `TPS631000DRLR` | 8-pin `DRL` SOT-5X3 buck-boost | [TI datasheet](https://www.ti.com/lit/gpn/TPS631000) | [DigiKey](https://www.digikey.com/en/products/detail/texas-instruments/TPS631000DRLR/15965499) | [Exact library/native render passed](../../hardware/coupon/rev-a/power-library-audit.md); passives pending |
| LED rail | `TPS63020DSJT` | 14-pin `DSJ` VSON adjustable buck-boost | [TI datasheet](https://www.ti.com/lit/gpn/TPS63020) | [DigiKey](https://www.digikey.com/en/products/detail/texas-instruments/TPS63020DSJT/2263063) | [Exact library/native render passed](../../hardware/coupon/rev-a/power-library-audit.md); passives and thermal layout pending |
| Fuel gauge | `MAX17048G+T10` | 8-pin 2 × 2 mm TDFN | [Analog Devices datasheet](https://www.analog.com/media/en/technical-documentation/data-sheets/MAX17048-MAX17049.pdf) | [DigiKey](https://www.digikey.com/en/products/detail/analog-devices-inc-maxim-integrated/MAX17048G-T10/3758921) | [Exact library/native render passed](../../hardware/coupon/rev-a/power-library-audit.md); cell model and circuit review pending |
| Battery-current monitor | `INA232AIDDFR` | 8-pin `DDF`; proposed `A0 = GND`, address `0x40` | [TI datasheet](https://www.ti.com/lit/gpn/INA232) | [DigiKey](https://www.digikey.com/en/products/detail/texas-instruments/INA232AIDDFR/17748453) | [Exact library/native render passed](../../hardware/coupon/rev-a/power-library-audit.md); shunt and circuit pending |
| Active-high row decoder | `74HC4514PW,118` | 24-pin TSSOP; `E = HIGH` forces every row output low | [Nexperia product page and datasheet](https://www.nexperia.com/product/74HC4514PW) | [DigiKey](https://www.digikey.com/en/products/detail/nexperia-usa-inc/74HC4514PW-118/1230453) | [Exact library and native render passed](../../hardware/coupon/rev-a/row-library-audit.md); [row source captured](../../hardware/coupon/rev-a/row-capture.md); native circuit review and quote-time availability pending |
| P-channel row switch | `DMP2066LSN-7` | SC-59; sixteen required | [Diodes Incorporated datasheet](https://www.diodes.com/datasheet/download/DMP2066LSN.pdf) | [DigiKey](https://www.digikey.com/en/products/detail/diodes-incorporated/DMP2066LSN-7/1964690) | Exact library/native render passed and row source captured; switching test required |
| N-channel gate pull-down / small switch | `2N7002K-7` | SOT-23; row level shift and candidate ILIM branch switch | [Diodes Incorporated product page](https://www.diodes.com/part/view/2N7002K) | [DigiKey](https://www.digikey.com/en/products/detail/diodes-incorporated/2N7002K-7/1934378) | Exact library/native render passed and row source captured; 3.3 V row use requires review and measurement |
| USB D+/D− and CC ESD | `TPD4E05U06DQAR` | Four 0.5 pF channels in 10-pin `DQA` USON; place at receptacle | [TI product and ordering page](https://www.ti.com/product/TPD4E05U06/part-details/TPD4E05U06DQAR) | [DigiKey](https://www.digikey.com/en/products/detail/texas-instruments/TPD4E05U06DQAR/3996774) | [Exact library/native render passed](../../hardware/coupon/rev-a/power-library-audit.md); routing and clamp review pending |

The driver draft selects `ERJ-2RKF3922X` (39.2 kΩ) for IREF and `GRM155R71C104KA88D` (100 nF) for local decoupling, plus four `ERJ-2RKF1003X` 100 kΩ input pull-downs. The row audit adds `ERJ-2RKF1001X` (1 kΩ) as the P-MOSFET source-to-gate pull-up and reuses the 100 kΩ part for logic defaults. The controller capture adds `ERJ-2RKF1002X`, `ERJ-2RKF22R0X`, `ERJ-2RKF4990X`, `GRM188R60J106ME47D`, active `GRM155C71A105KE11D` and `EVQP7J01P`; its record controls values and use. The VBUS protection device, fuse strategy, regulator inductors/capacitors, current shunt and remaining thermal/layout values remain open. They must not be inferred from this short list.

## Mechanical interfaces and RF

| Function | Exact candidate | Evidence | State |
|---|---|---|---|
| USB-C receptacle | `USB4505-03-0-A` by GCT; USB 2.0, mid-mount, 1.0 mm PCB offset, through-hole shell stakes | [GCT product page and drawings](https://gct.co/connector/usb4505), [DigiKey](https://www.digikey.com/en/products/detail/gct/USB4505-03-0-A/15283201) | [Draft library/native render passed](../development/usb-connector-review-bf1627c.md); cutout, stack-up/process and case model pending |
| Battery board header | `BM03B-ACHFKS-GACN-ETF` | [JST ACHF family](https://www.jst-mfg.com/product/detail_e.php?series=627), [DigiKey](https://www.digikey.com/en/products/detail/jst-sales-america-inc/BM03B-ACHFKS-GACN-ETF/5272484) | Interface candidate |
| Battery cable housing | `ACHFR-03V-H` with `SACHF-003GAC-P0.2` contacts and AWG 28 wire | [JST ACHF family](https://www.jst-mfg.com/product/detail_e.php?series=627), [DigiKey housing](https://www.digikey.com/en/products/detail/jst-sales-america-inc/ACHFR-03V-H/5272189) | Interface candidate; pack vendor must build and document harness |
| 2.4 GHz antenna | `FXP75.07.0045B` by Taoglas; 5.9 × 4.1 × 0.24 mm FPC, 45 mm cable, I-PEX MHF I / U.FL-compatible plug | [Current Taoglas datasheet](https://www.taoglas.com/datasheets/FXP75.07.0045B.pdf), [DigiKey](https://www.digikey.com/en/products/detail/taoglas-limited/FXP75-07-0045B/4503578) | Candidate; documentation conflict and installed RF validation required |

The proposed pack conductor order is battery positive, NTC and battery negative, with NTC in the centre. Do not assign connector pin numbers or order a harness until the exact mating-view drawing and pack-vendor drawing have been overlaid and independently polarity-checked.

The current Taoglas revision F datasheet specifies 0.84 dBi peak gain at 2.4 GHz, below Espressif's 2.33 dBi certification limit. Some distributor metadata still reports 2.5 dBi for the same MPN, apparently from older documentation. Gate A therefore requires confirmation of the supplied antenna revision and its controlled datasheet; Gate B still tests the installed antenna with the battery, body, case and magnets present.

`FXP840.07.0055B` is rejected for this design because its manufacturer currently specifies 2.5 dBi peak gain at 2.4 GHz, above the module datasheet's 2.33 dBi limit. Its convenient outline is not sufficient reason to inherit avoidable certification uncertainty.

## LED comparison selection

[ADR 0007](../decisions/0007-coupon-led-finalist-pair.md) locks Coupon Rev A to the first two parts below: eight 16-pixel columns of the 1010 Everlight and eight columns of the diffused 1515 QT Brightek. Exact footprints, optical bins and procurement lots remain Gate A work.

| Candidate | Package and optics | Electrical headline | Evidence | Role |
|---|---|---|---|---|
| `EAST10105RGBA0` by Everlight | 1.0 × 1.0 mm, clear, common anode | 5 mA test current; typical forward voltages 1.95/2.95/2.95 V R/G/B | [Datasheet copy at Mouser](https://www.mouser.com/datasheet/2/143/EAST10105RGBA0-1709851.pdf), [DigiKey](https://www.digikey.com/en/products/detail/everlight-electronics-co-ltd/EAST10105RGBA0/8510358) | Locked for columns 0–7 |
| `QBLP1515A-RGB2A` by QT Brightek | 1.55 × 1.50 mm, white diffused, common anode | 10 mA test current; typical forward voltages 2.0/2.8/2.8 V R/G/B | [Manufacturer datasheet](https://www.qt-brightek.com/datasheet/QBLP1515A-RGB2A.pdf), [DigiKey](https://www.digikey.com/en/products/detail/qt-brightek-qtb/QBLP1515A-RGB2A/29450018) | Locked for columns 8–15; exact pads with ADR 0008 checkerboard rotation |
| `EAST1616RGBA3` by Everlight | 1.6 × 1.6 mm, clear, common anode | 5 mA test current; typical forward voltages 1.95/2.8/2.8 V R/G/B | [Datasheet copy at Mouser](https://www.mouser.com/datasheet/2/143/EAST1616RGBA3-1594303.pdf), [DigiKey](https://www.digikey.com/en/products/detail/everlight-electronics-co-ltd/EAST1616RGBA3/8510359) | Not populated; retained alternative |

The selected pair compares the most promising end-product systems, including their real lens differences. It therefore does not isolate package size as the only variable. The assembler must confirm reel bin codes, moisture handling, tape orientation and no mixed optical lots.

The QBLP1515 recommended land pattern is nominally 2.00 mm wide, which cannot be repeated in one orientation on a 1.95 mm grid without copper overlap. [ADR 0008](../decisions/0008-qblp1515-checkerboard-placement.md) retains the exact pads and alternates component rotation by 0°/90°. The calculated 0.35 mm minimum copper clearance still requires PCB DRC and assembler DFM.

## Preliminary charge and USB-current calculations

These are datasheet calculations, not measurements and not reviewed release values.

### Battery charge current

The selected BQ24074 specifies `ICHG = KISET / RISET`, with `KISET` from 797 to 975 A·Ω over the stated conditions. For `RISET = 1.13 kΩ ±1%`:

| Result | Current |
|---|---:|
| Nominal using 890 A·Ω | 0.788 A |
| Calculated minimum including resistor tolerance | 0.698 A |
| Calculated maximum including resistor tolerance | 0.872 A |

This value is suitable only if the exact protected and terminated pack explicitly permits at least 0.872 A charging over the charger's allowed temperature range. Otherwise `RISET` increases. The NTC network is pack-dependent and remains open.

### Selected USB permission path

The TUSB320LAI has dead-battery `Rd` terminations, so a source can establish VBUS before the controller has VDD. After VBUS appears, the candidate TLV75533 rail powers the controller, pull-ups and inverter while the badge's application switch may remain off. The TUSB320LAI GPIO truth table is:

| `OUT1` | `OUT2` | Detected state |
|---:|---:|---|
| H | H | Unattached / default output state |
| H | L | Attached, default current |
| L | H | Attached, 1.5 A advertisement |
| L | L | Attached, 3.0 A advertisement |

Because the outputs are open drain, `OUT1` can participate directly in an active-low hardware grant for the 1.5 A and 3.0 A states. BQ24392 `CHG_DET` separately grants high current for positively classified charging sources. Its `GOOD_BAT` input stays high whenever VBUS is valid; using a low level as permanent OFF isolation would start its 30-minute nominal / 45-minute maximum Dead Battery Provision timer. The application-powered TS3USB31E instead supplies the hard-OFF data disconnect. A validated ESP32 USB-device-layer signal may select only the BQ24074's fixed 500 mA mode for an SDP after configuration and while unsuspended.

The passive BQ24074 state is standby (`EN2=1, EN1=1`). A 1.78 kΩ, 1% `ILIM` resistor defines only the hardware-qualified external mode:

| State | Calculated programmed range from `KILIM`, including 1% resistance tolerance |
|---|---:|
| Standby, unqualified source | No charger input path |
| Configured, unsuspended SDP | Fixed internal 450–500 mA limit |
| BC1.2 charging source or Type-C 1.5 A/3 A | 0.834–0.976 A external limit |

All limits cover total current entering BQ24074 `IN`, not arbitrary VBUS loads ahead of it. The USB-only LDO, both detectors, logic and status indicators need a separate budget. The exact priority logic must prevent the SDP grant from corrupting a simultaneous hardware high-current state. The TS3USB31E must place the detector-facing pair on its `D+/D-` pins covered by the published `Ioff` condition, place the ESP32 on `HSD+/HSD-`, and tie active-low `OE` to ground. The selected linear charger also requires thermal proof from a depleted-battery charge cycle.

The [power/input pre-capture record](../../hardware/coupon/rev-a/power-pre-capture.md) and [ADR 0010](../decisions/0010-source-qualified-off-charging.md) control these calculations and states.

The schematic must show this as a review block. It may not be copied into fabrication files merely because the resistor arithmetic is correct.

## Marketplace and assembler strategy

### Manufacturer-authorized and traceable sources

Use the manufacturer, DigiKey, Mouser, Farnell/Newark, Arrow or another authorized channel for prototype critical ICs, connectors and antennas. An assembler may procure them only when it identifies the exact MPN and traceable source on the quote. LCSC/JLCPCB stock can be used when the MPN and supply-chain evidence are acceptable; “compatible” search results are not acceptable substitutes.

### Alibaba

Alibaba is useful for finding a third turnkey PCBA quotation and, later, LED manufacturers willing to supply controlled optical bins. It is not evidence that a listing's description is electrically correct. Send every candidate supplier the identical release package and require written answers for:

- legal company and factory identity, actual assembly location and whether assembly is in-house;
- demonstrated 1010 LED, 0.4/0.5 mm-pitch QFN, fine-pitch USB-C and six-layer controlled-impedance capability;
- solder-paste inspection, AOI and X-ray coverage, moisture handling and polarity control;
- exact source and lot traceability for every critical line item;
- no substitutions without written approval;
- DFM findings, stencil approach, test plan, yield/rework policy and photos of comparable work;
- customer-consigned parts support when a critical item cannot be sourced traceably.

Do not choose a supplier by marketplace badge, years listed, unit price or claimed monthly capacity alone. Paid samples and platform payment protection reduce commercial risk but do not replace electrical evidence.

### AliExpress

AliExpress remains acceptable for development-only ESP32 boards, USB cables, jumper leads, optical diffuser samples, fixtures and inexpensive measurement accessories that will be cross-checked against trusted instruments. Do not source the final LiPo pack, charger, power converters, LED driver, USB connector, RF antenna or safety-critical protection parts there unless the storefront is demonstrably the manufacturer's authorized store and provides exact traceability. No current AliExpress listing is approved by this record.

## Gate A blockers carried forward

- Exact project-local LED footprints, pad numbering, polarity marks, tape orientation and controlled optical bins are checked against manufacturer documentation.
- Battery vendor supplies one exact protected-pack drawing, ratings, NTC curve, harness and safety documentation.
- Engineer resolves the complete USB-C/default-current/BC1.2/data topology and verifies that every current-limit state fails safely without application-firmware assistance.
- Converter calculations select inductors, capacitors, compensation/layout and worst-case thermal limits.
- Every symbol and footprint receives a two-person pin/pad/polarity check against controlled drawings.
- Schematic ERC and a preliminary placed/routed board pass review before fabrication.
