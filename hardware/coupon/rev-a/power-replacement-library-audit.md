<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Selected power replacement libraries

Status: first-author source/drawing transcription and host checks pass; native KiCad rendering review is pending. These three libraries implement the part choices in ADR 0010. They are not instantiated in the schematic and are not fabrication approval.

## Sources inspected on 2026-09-15

| Part | Pin source | Land/stencil source |
|---|---|---|
| BQ24074RGTR | [TI SLUS810N](https://www.ti.com/lit/ds/symlink/bq24074.pdf), October 2021, Table 7-1 | Embedded RGT0016C drawing 4222419/E, July 2025, PDF pages 50-52 |
| BQ24392RSER | [TI SLIS146G](https://www.ti.com/lit/ds/symlink/bq24392.pdf), September 2017, pin functions | [MPQF186D](https://www.ti.com/lit/pdf/MPQF186D), RSE0010A; drawing sheets identify 4220307/A, March 2020 |
| TS3USB31ERSER | [TI SCDS256A](https://www.ti.com/lit/ds/symlink/ts3usb31e.pdf), September 2016, pin functions | [MPQF207E](https://www.ti.com/lit/pdf/MPQF207E), RSE0008A; drawing sheets identify 4220323/B, March 2018 |

The download identifier revision and the revision printed on each drawing sheet are deliberately distinguished. BQ24074's older pin-view caption still names RGT0016B, while the current comparison table and appended package drawing specify RGT0016C. This footprint transcribes the appended C land pattern; confirm the supplied lot/package with the assembler before Gate A closure.

| Download | SHA-256 |
|---|---|
| bq24074.pdf | 3c8a0a906dc305bccc4eb5f83f27a9df7d8db441ee304e204650f5e7b43c4e56 |
| bq24392.pdf | 7931cb7602a38537ca4ea296999e502f02a0a4fbfe38cf82bf5971ebae1a0fb4 |
| MPQF186D | 523624138802702cae87ae5f918d05107b8259c7626d1ee741bbd61a41183bbb |
| ts3usb31e.pdf | b33c728a099c9f32d3acae56125b13bb88bad6f8925ddf32be69a3bd8908d940 |
| MPQF207E | a0c14d6741c72681f20f827f2d873e210e10124f2f38626cb1e38eb6876b91d9 |

## Pin transcription

| Part | Numbered signals |
|---|---|
| BQ24074RGTR | 1 TS; 2 BAT; 3 BAT; 4 active-low CE; 5 EN2; 6 EN1; 7 open-drain PGOOD; 8 VSS; 9 open-drain CHG; 10 OUT; 11 OUT; 12 ILIM; 13 IN; 14 TMR; 15 ITERM; 16 ISET; project pad 17 VSS_EP |
| BQ24392RSER | 1 open-drain SW_OPEN; 2 DM_HOST; 3 DP_HOST; 4 active-low open-drain CHG_AL_N; 5 GOOD_BAT; 6 GND; 7 DP_CON; 8 DM_CON; 9 VBUS; 10 push-pull CHG_DET |
| TS3USB31ERSER | 1 active-low OE; 2 HSD+; 3 D+; 4 GND; 5 D-; 6 HSD-; 7 NC; 8 VCC |

The charger exposed pad must connect to VSS and cannot replace perimeter pin 8 as the primary ground connection. The BAT pins use the existing project battery-boundary power-input convention; ISET is bidirectional because it also reports charge current. Electrical types are ERC aids, not a substitute for the external circuitry.

The BQ24392 GOOD_BAT input stays high while VBUS is valid under ADR 0010. TS3USB31E is powered only from the switched application rail, with OE low; put the detector-facing pair on D+/D- because those are the pins explicitly covered by zero-VCC Ioff. Keep its NC pin explicit for later disposition.

## Geometry

All coordinates are millimetres in the top-view KiCad footprint, with positive Y down. Pin numbers run counter-clockwise.

| Pattern | Signal copper and paste | Body and exposed land |
|---|---|---|
| RGT0016C | 16 lands, 0.60 long by 0.24 wide; 0.50 pitch; rows centred at ±1.40. Pins 1-4 left, 5-8 bottom, 9-12 right, 13-16 top. | 3 × 3 body; pad 17 copper/mask 1.68 × 1.68; separate paste-only opening 1.55 × 1.55, approximately 85% area |
| RSE0010A | Pins 1/4/6/9: 0.55 × 0.25; middle pins 2/3/7/8: 0.55 × 0.20. Left/right centres ±0.675, vertical pitch 0.50. End pins 5/10: 0.30 × 0.60 at (0, ±0.90). | X width 1.50, Y height 2.00; no exposed pad |
| RSE0008A | Pins 1/3/5/7: 0.55 × 0.25; middle pins 2/6: 0.55 × 0.20. Left/right centres ±0.675, vertical pitch 0.50. End pins 4/8: 0.30 × 0.60 at (0, ±0.65). | 1.50 × 1.50; no exposed pad |

All pad corners use radius 0.05. KiCad's roundrect ratio is radius divided by the shorter full pad dimension, not by its half-width. The masks use an explicit 0.05 expansion, within the drawings' preferred NSMD 0.07 maximum. No pad-level paste overrides are allowed. Project courtyards provide at least 0.25 clearance from pad/body extents; external silk pin-one dots avoid lands. Optional thermal vias are not embedded and remain a PCB/assembler decision. TI's RGT stencil example uses 0.125 thickness while both RSE examples use 0.10; the eventual shared stencil needs assembler DFM review.

## Recovery findings

The interrupted, unpublished local commit c671fc4 was unavailable after the workspace reset. Recovery from published 00e3712 and the conversation record caught three first-author transcription errors before any native export or board fabrication:

- The RSE drafts widened every side pad to 0.25; the manufacturer uses 0.20 for the middle pads.
- The drafts doubled the intended corner radii through an incorrect roundrect-ratio conversion.
- The RSE0010A fabrication body had its X/Y dimensions swapped.

All three are corrected here, with regression tests. The footprint geometry guard now checks corner radii, body/courtyard axes, explicit mask expansion and prohibited paste overrides in addition to pin numbers, sizes, coordinates, layer assignments and copper separation.

## Native review required

Host evidence on 2026-09-15: all 99 tests passed with `python3 -m unittest discover -s tools/tests -p 'test_*.py' -v`. The power-state subset was rerun after updating its blocker wording and passed all 15 tests. The wrapper uses a test-only CLI stub here; no new native KiCad result is claimed.

Run the repository's check-kicad.sh with a fresh output directory and upload the complete ZIP. It must export 32 symbols and 24 footprints per raw view, preserve the existing 356-item/1,360-logical-pin native netlist contract, and pass the strict staged ERC gate. Library-only additions do not change the eight schematic pages or resolve the temporary USB boundary.

The assistant will inspect the three new symbols and fabrication/copper/paste views against the drawings: distinct charger BAT/OUT pins; inversion bubbles on CE, CHG_AL_N and OE; smaller central RGT paste aperture; correct pin-one orientation; narrower RSE middle pads; and the tall RSE0010A body. Do not mark this review passed from host checks or stub exports. Power capture, source-priority logic, auxiliary-current budget, pack/NTC, thermal validation, PCB layout and independent Gate A remain open.
