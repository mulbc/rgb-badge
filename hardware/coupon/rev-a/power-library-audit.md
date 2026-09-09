<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Coupon Rev A power-library audit

Status: first controlled charger, application-rail, USB-only logic, current-monitor and USB ESD libraries authored; native KiCad 10 render review and independent Gate A review pending; remaining power/input libraries are deliberately blocked or not yet transcribed

## Controlled parts

| Function | Exact part | Package / project footprint | Controlled source |
|---|---|---|---|
| Standalone charger and NVDC power path | `BQ25616JRTWT` | TI RTW0024A WQFN24, 4 × 4 mm, 0.5 mm pitch, exposed pad / `QFN_TI_RTW0024A_4x4mm_P0.5mm_EP2.7mm` | [TI BQ25616/BQ25616J datasheet](https://www.ti.com/lit/ds/symlink/bq25616.pdf), SLUSDF7A, revised 2022-02 |
| Switched application 3.3 V buck-boost | `TPS631000DRLR` | TI DRL0008A SOT-5X3, 0.5 mm pitch / `SOT5X3_TI_DRL0008A` | [TI TPS631000 datasheet](https://www.ti.com/lit/ds/symlink/tps631000.pdf), SLVSFH3C, revised 2026-08 |
| USB-only 3.3 V LDO | `TLV75533PDBVR` | TI DBV0005A SOT-23-5 / `SOT23_TI_DBV0005A` | [TI TLV755P datasheet](https://www.ti.com/lit/ds/symlink/tlv755p.pdf), SBVS320D, revised 2024-09 |
| USB-current-state inverter | `SN74LVC1G04DBVR` | TI DBV0005A SOT-23-5 / `SOT23_TI_DBV0005A` | [TI SN74LVC1G04 datasheet](https://www.ti.com/lit/ds/symlink/sn74lvc1g04.pdf), SCES214AF, revised 2025-10 |
| Battery-current monitor | `INA232AIDDFR` | TI DDF0008A SOT-23-THIN-8 / `SOT23_THIN_TI_DDF0008A` | [TI INA232 datasheet](https://www.ti.com/lit/ds/symlink/ina232.pdf), SBOSAA2, 2022-12 |
| Four-line USB data/CC ESD | `TPD4E05U06DQAR` | TI DQA0010A USON-10 / `USON_TI_DQA0010A` | [TI TPDxE05U06 datasheet](https://www.ti.com/lit/ds/symlink/tpd4e05u06.pdf), SLVSBO7O, revised 2024-08 |

The manufacturer PDFs downloaded for this transcription hashed as follows. A changed upstream file requires a fresh comparison rather than a blind hash update.

| Local source name | SHA-256 |
|---|---|
| `bq25616.pdf` | `db1c80794273f68d40f13969888a1da6abc08d4a1ea38b68af8b9a09d7c9834a` |
| `tps631000.pdf` | `b52a4064a8c2cbb4c9dd97f366b398dedcb490ffc9d564245f297536a19b426b` |
| `tlv755p.pdf` | `ee739b0fe51aea50d07b53d0acccad4a0ddeac5bb7aa932bed28dc631ec5305e` |
| `sn74lvc1g04.pdf` | `ac04a53de979125799e57ea5a6dff4138fe53e0eceebe45c31f57523669887d5` |
| `ina232.pdf` | `681ab74ffec4b3b19e30363ca9be52adc75fad089d3ddad59204ebfd52574153` |
| `tpd4e05u06.pdf` | `c167cf1e72a5473a4d2c59b6a3c0251498701da05b7785919b9ceaae3b3e02c6` |

These are candidate BOM lines, not procurement or fabrication approval. Production lots must use the exact MPN through an authorized distributor or traceable PCBA supply chain. Marketplace listings may be used only for replaceable development samples and must not silently substitute a package or suffix.

## Pin transcription

The `BQ25616JRTWT` symbol preserves all 24 perimeter pins plus the exposed ground pad:

| Pins | Signals |
|---|---|
| 1–4 | `VAC`, `ACDRV`, `D+`, `D-` |
| 5–8 | open-drain `STAT`, `OTG`, open-drain `PG`, `ILIM` |
| 9–12 | active-low `CE`, `ICHG`, `TS`, `VSET` |
| 13–18 | two `BAT`, two `SYS`, two `GND` |
| 19–24 | two `SW`, `BTST`, `REGN`, `PMID`, `VBUS` |
| 25 | exposed `GND_EP` |

The symbol shows `CE` with an inversion bubble and models `STAT`/`PG` as open-collector outputs. `D+` and `D-` remain bidirectional because the charger performs analog source detection. `SW` and `BTST` are intentionally passive switching nodes. Electrical types are ERC aids, not permission to omit the datasheet-required external network.

The `TPS631000DRLR` symbol maps pins 1–8 to `VOUT`, `LX2`, `LX1`, `VIN`, `EN`, `MODE`, `GND` and `FB`. Both `EN` and `MODE` are inputs that must never float in the later circuit.

The DBV symbols do not pretend their shared five-pin package has a shared function: `TLV75533PDBVR` maps `IN`, `GND`, `EN`, `NC`, `OUT`, while `SN74LVC1G04DBVR` maps `NC`, `A`, `GND`, inverted `Y`, `VCC`. `INA232AIDDFR` preserves `IN+`, `IN-`, `GND`, `VS`, `SCL`, `SDA`, `A0`, open-drain `ALERT`. `TPD4E05U06DQAR` preserves the datasheet's `D1+`, `D1-`, `GND`, `D2+`, `D2-`, four `NC` pins and second `GND`; unused ESD pins remain explicit so a later layout cannot mistake them for protected channels.

## Land-pattern transcription

The RTW footprint copies TI land-pattern drawing 4211120-3/D:

- 24 signal lands are 0.28 × 0.85 mm on 0.5 mm pitch, with the row centres at ±1.975 mm;
- exposed-pad copper and mask are 3.1 × 3.1 mm and assigned to pin 25;
- paste is four separate 1.1 × 1.1 mm apertures at `(±0.7, ±0.7)` mm, matching TI's example 66% area coverage;
- the package's optional nine 0.3 mm thermal vias are not embedded in the footprint. They belong in the PCB layout, where finished drill, annular ring and via fill/capping can be agreed with the assembler;
- courtyard and pin-1 marking are project review geometry, not dimensions copied into the copper pattern.

The DRL footprint copies TI drawing 4224486/G: eight 0.67 × 0.30 mm lands, left/right row centres at ±0.74 mm, and 0.5 mm vertical pitch. The project pin-1 marker sits outside the copper lands beside pad 1.

The shared DBV footprint copies TI drawing 4214839/K: five 1.10 × 0.60 mm lands, left/right row centres at ±1.30 mm, and 0.95 mm vertical pitch. The DDF footprint copies drawing 4222047/E: eight 1.05 × 0.45 mm lands with row centres at ±1.30 mm and 0.65 mm pitch.

The ESD footprint is specifically the base-suffix DQA0010A drawing 4220328/A used by `TPD4E05U06DQAR`, not the later `.B` orderable variant and its DQA0010B via-in-pad geometry. It uses ten 0.565 mm long lands at ±0.4175 mm row centres; signal/NC lands are 0.20 mm wide and ground pads 3/8 are 0.40 mm wide. Substituting a `.B`-suffixed device requires a new footprint and written review.

## Intentionally unresolved libraries

No unverified footprint is allowed merely to make the power sheet look complete:

- `USB4505-03-0-A`: GCT confirms the active 16-contact mid-mount product, but the exact downloadable PCB drawing was not retrievable in this environment. Connector shell stakes and contact numbering remain blocked on that controlled drawing.
- `MAX17048G+T10`: the electrical datasheet refers to separate Maxim drawings `21-0168` and `90-0065`; the exact land-pattern document must be obtained before authoring its TDFN footprint.
- `TUSB320LAIRWBR`: its tiny RWB X2QFN drawing is available, but the corner-land geometry and solder-mask clearances need their own focused transcription/review rather than a rectangular approximation.
- `TPS63020DSJT`: its DSJ exposed pad has side features, segmented stencil geometry and a thermal-via example. It remains a separate focused transcription.
- The latching slide switch, remaining converter/charger passives, battery connector and NTC network remain for the next library/capture increments. The switch and battery connector cannot be frozen before exact mechanical parts are selected.

## Automated and native review

`python3 tools/check-power-libraries.py` independently checks all six exact MPN properties, all 61 logical pins, five manufacturer land maps, the BQ exposed copper/paste split, the DQA ground-land distinction and pin-1 markers. `tools/check-kicad.sh` also requires KiCad 10 to load and export every controlled symbol and all three footprint views.

For the native render review, verify:

- BQ pins 1–6 run down the left package edge, 7–12 across the bottom, 13–18 up the right and 19–24 across the top when viewed from above;
- BQ pin 25 is one continuous central copper/mask land, while the paste-only view shows exactly four separated square apertures;
- the BQ symbol shows the `CE` inversion bubble plus open-drain `STAT` and `PG` outputs;
- TPS631000 pad 1 is upper-left, pins 1–4 run down the left, and pins 5–8 run up the right;
- DBV/DDF pads count counter-clockwise from upper-left; both DBV parts reuse identical copper without sharing their pin names;
- DQA pads 1–5 run down the left and 6–10 run up the right, with wider ground lands only at pins 3 and 8;
- no courtyard, body outline, value text or pin-1 marker touches a copper land.

A clean automated run is necessary but is not DRC, thermal analysis, USB compliance, assembler DFM, battery safety review or independent Gate A approval.
