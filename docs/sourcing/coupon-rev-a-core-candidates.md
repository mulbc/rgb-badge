<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Coupon Rev A core component candidates

Status: researched candidates for schematic capture; **not a frozen BOM and not authorization to buy or fabricate**

Research cut-off: 2026-09-06

## How to read this record

An exact MPN in this document means that its public documentation, package and at least one traceable purchase route were found. It does not mean its symbol, footprint, thermal design, surrounding passives, availability or use in this circuit has passed Gate A. Stock counts and prices are intentionally not frozen here because they can change between research and quotation.

Before schematic capture, every selected part receives a project-local symbol and footprint checked against the linked manufacturer drawing. Before release, the assembler must quote the exact MPN and disclose its source; no equivalent or house substitution is allowed without written review.

## Core silicon and switching

| Function | Exact schematic candidate | Package / implementation note | Manufacturer evidence | Traceable sample source | State |
|---|---|---|---|---|---|
| MCU and BLE | `ESP32-S3-WROOM-1U-N16R8` | External-antenna module; 16 MB flash, 8 MB PSRAM | [Espressif module datasheet](https://documentation.espressif.com/esp32-s3-wroom-1_wroom-1u_datasheet_en.pdf) | [DigiKey](https://www.digikey.com/en/products/detail/espressif-systems/ESP32-S3-WROOM-1U-N16R8/16162641) | Selected for draft |
| 48-channel LED sink | `TLC59581RTQT` | 56-pin `RTQ` QFN, 8 × 8 mm; one on coupon, three on final badge | [TI datasheet](https://www.ti.com/lit/gpn/TLC59581) | [DigiKey](https://www.digikey.com/en/products/detail/texas-instruments/TLC59581RTQT/6571953) | [Driver captured](../../hardware/coupon/rev-a/driver-capture.md); provisional RTQ0056E footprint; confirm supplied E/G variant |
| Standalone charger / power path | `BQ25616JRTWT` | 24-pin `RTW` WQFN, JEITA variant | [TI datasheet](https://www.ti.com/lit/gpn/BQ25616) | [DigiKey](https://www.digikey.com/en/products/detail/texas-instruments/BQ25616JRTWT/11570504) | Selected for draft; USB-current circuit unresolved |
| USB-C CC detector | `TUSB320LAIRWBR` | 12-pin `RWB` X2QFN; fixed UFP, GPIO mode | [TI datasheet](https://www.ti.com/lit/gpn/TUSB320LAI) | [DigiKey](https://www.digikey.com/en/products/detail/texas-instruments/TUSB320LAIRWBR/5722618) | Selected for draft; Gate A review required |
| USB-only 3.3 V rail | `TLV75533PDBVR` | 500 mA SOT-23-5 LDO from VBUS; powers CC detector and its logic while application rails are off | [TI datasheet](https://www.ti.com/lit/gpn/TLV755P) | [DigiKey](https://www.digikey.com/en/products/detail/texas-instruments/TLV75533PDBVR/9356541) | Circuit candidate |
| CC-state inverter | `SN74LVC1G04DBVR` | SOT-23-5; same USB-only 3.3 V rail | [TI product and ordering page](https://www.ti.com/product/SN74LVC1G04/part-details/SN74LVC1G04DBVR) | [DigiKey](https://www.digikey.com/en/products/detail/texas-instruments/SN74LVC1G04DBVR/385716) | Circuit candidate |
| 3.3 V application rail | `TPS631000DRLR` | 8-pin `DRL` SOT-5X3 buck-boost | [TI datasheet](https://www.ti.com/lit/gpn/TPS631000) | [DigiKey](https://www.digikey.com/en/products/detail/texas-instruments/TPS631000DRLR/15965499) | Selected for draft; passives open |
| LED rail | `TPS63020DSJT` | 14-pin `DSJ` VSON adjustable buck-boost | [TI datasheet](https://www.ti.com/lit/gpn/TPS63020) | [DigiKey](https://www.digikey.com/en/products/detail/texas-instruments/TPS63020DSJT/2263063) | Selected for draft; passives and voltage open |
| Fuel gauge | `MAX17048G+T10` | 8-pin 2 × 2 mm TDFN | [Analog Devices datasheet](https://www.analog.com/media/en/technical-documentation/data-sheets/MAX17048-MAX17049.pdf) | [DigiKey](https://www.digikey.com/en/products/detail/analog-devices-inc-maxim-integrated/MAX17048G-T10/3758921) | Selected for draft |
| Battery-current monitor | `INA232AIDDFR` | 8-pin `DDF`; proposed `A0 = GND`, address `0x40` | [TI datasheet](https://www.ti.com/lit/gpn/INA232) | [DigiKey](https://www.digikey.com/en/products/detail/texas-instruments/INA232AIDDFR/17748453) | Selected for draft; shunt open |
| Active-high row decoder | `74HC4514PW,118` | 24-pin TSSOP; `E = HIGH` forces every row output low | [Nexperia product page and datasheet](https://www.nexperia.com/product/74HC4514PW) | [DigiKey](https://www.digikey.com/en/products/detail/nexperia-usa-inc/74HC4514PW-118/1230453) | [Exact library audited](../../hardware/coupon/rev-a/row-library-audit.md); native render and quote-time availability pending |
| P-channel row switch | `DMP2066LSN-7` | SC-59; sixteen required | [Diodes Incorporated datasheet](https://www.diodes.com/datasheet/download/DMP2066LSN.pdf) | [DigiKey](https://www.digikey.com/en/products/detail/diodes-incorporated/DMP2066LSN-7/1964690) | Exact library audited; switching test required |
| N-channel gate pull-down / small switch | `2N7002K-7` | SOT-23; row level shift and candidate ILIM branch switch | [Diodes Incorporated product page](https://www.diodes.com/part/view/2N7002K) | [DigiKey](https://www.digikey.com/en/products/detail/diodes-incorporated/2N7002K-7/1934378) | Exact library audited; 3.3 V row use requires review and measurement |
| USB D+/D− and CC ESD | `TPD4E05U06DQAR` | Four 0.5 pF channels in 10-pin `DQA` USON; place at receptacle | [TI product and ordering page](https://www.ti.com/product/TPD4E05U06/part-details/TPD4E05U06DQAR) | [DigiKey](https://www.digikey.com/en/products/detail/texas-instruments/TPD4E05U06DQAR/3996774) | Candidate; routing and clamp review required |

The driver draft now selects `ERJ-2RKF3922X` (39.2 kΩ) for IREF and `GRM155R71C104KA88D` (100 nF) for local decoupling, plus four `ERJ-2RKF1003X` 100 kΩ input pull-downs. The row audit adds `ERJ-2RKF1001X` (1 kΩ) as the P-MOSFET source-to-gate pull-up and reuses the 100 kΩ part for logic defaults. The VBUS protection device, fuse strategy, regulator inductors/capacitors, current shunt and remaining thermal/layout values remain open. They must not be inferred from this short list.

## Mechanical interfaces and RF

| Function | Exact candidate | Evidence | State |
|---|---|---|---|
| USB-C receptacle | `USB4505-03-0-A` by GCT; USB 2.0, mid-mount, 1.0 mm PCB offset, through-hole shell stakes | [GCT product page and drawings](https://gct.co/connector/usb4505), [DigiKey](https://www.digikey.com/en/products/detail/gct/USB4505-03-0-A/15283201) | Selected for draft; case and PCB-edge model required |
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

The BQ25616J specifies `ICHG = KICHG / RICHG`, with `KICHG` from 639 to 715 A·Ω over the stated conditions. For `RICHG = 806 Ω ±1%`:

| Result | Current |
|---|---:|
| Nominal using 677 A·Ω | 0.840 A |
| Calculated minimum including resistor tolerance | 0.785 A |
| Calculated maximum including resistor tolerance | 0.896 A |

This value is suitable only if the exact protected and terminated pack explicitly permits at least 0.90 A charging over the charger's allowed temperature range. Otherwise `RICHG` increases. `VSET` and the JEITA/NTC network are also pack-dependent and remain open.

### Provisional Type-C advertisement path

The TUSB320LAI has dead-battery `Rd` terminations, so a source can establish VBUS before the controller has VDD. After VBUS appears, the candidate TLV75533 rail powers the controller, pull-ups and inverter while the badge's application switch may remain off. The TUSB320LAI GPIO truth table is:

| `OUT1` | `OUT2` | Detected state |
|---:|---:|---|
| H | H | Unattached / default output state |
| H | L | Attached, default current |
| L | H | Attached, 1.5 A advertisement |
| L | L | Attached, 3.0 A advertisement |

Because the outputs are open drain, `OUT1` pulled up to the USB-only 3.3 V rail and then inverted can turn on an N-MOSFET only for the 1.5 A and 3.0 A states. A gate pull-down keeps that MOSFET off with USB absent.

A preliminary BQ25616J `ILIM` network uses 1.00 kΩ as the passive branch and 665 Ω in parallel only for the higher-advertisement states:

| State | Effective resistance | Calculated programmed range from `KILIM`, including 1% resistance tolerance |
|---|---:|---:|
| Passive/default | 1.00 kΩ | 0.454–0.505 A |
| 1.5 A or 3.0 A advertised | 399.4 Ω nominal | 1.138–1.265 A |

This is deliberately below a 1.5 A advertisement even at the calculated maximum. It is **not approved** because all of the following remain unresolved:

1. The exact USB 2.0/default-current behaviour before and after enumeration, especially while the badge is switched off and cannot enumerate.
2. Whether the charger's D+/D− pins can remain isolated while meeting the intended A-to-C, C-to-C, SDP, CDP and dedicated-charger behaviours, or whether a reviewed BC1.2/data-multiplexer solution is required.
3. The 1.00 kΩ passive setting's tolerance at the nominal 500 mA boundary.
4. TUSB320LAI VDD ramp, pull-up sequencing, detach behaviour and stale advertisement states.
5. Dynamic stability when the display operates while the charger reaches input-current or input-voltage regulation.

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
