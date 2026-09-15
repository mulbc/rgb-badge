<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# USB/input closure assessment

Status: direct BQ25616J ILIM-only proposal rejected under [ADR 0009](../../../docs/decisions/0009-usb-input-current-closure.md). [ADR 0010](../../../docs/decisions/0010-source-qualified-off-charging.md) selects BQ24074/BQ24392/TUSB320/TS3USB31E for the next capture; replacement libraries pass host audits; native rendering review, priority logic, thermal proof and the complete power sheet remain pending.

## State coverage required

| Source/state | Required design evidence |
|---|---|
| USB absent | No backfeed; application OFF drain below 50 uA including pack, gauge and disabled rails |
| Legacy USB 2.0 host, not configured | Application runs from the battery; charger remains in standby and takes no system power from VBUS beyond the VBUS-only detection/logic budget |
| Configured SDP | Validated USB-device-layer grant selects the charger's fixed 500 mA input ceiling; it cannot select external ILIM |
| SDP suspend | Grant clears and charger returns to standby; reset and absent firmware are already standby |
| BC1.2 charging source | Detection coexists with native data where supported; a charger-selected limit is not assumed to be clamped by an unrelated resistor |
| Type-C default advertisement | Do not equate default Rp with a completed USB configuration or a BC1.2 charging-port classification |
| Type-C 1.5 A / 3 A advertisement | Hardware may select a higher bounded limit only after valid attachment/classification; qualification must disappear on detach or reduced advertisement |
| Switch OFF, reset, depleted battery | SDP/default/unclassified sources remain standby; hardware-qualified BC1.2 charging or Type-C 1.5 A/3 A sources charge without an ESP32 boot sequence |

The selected normal state table does not use the BQ24074's 100 mA mode. The battery-powered ESP32 can enumerate while VBUS remains limited to the detector/logic budget, and standby is more conservative than consuming the historical pre-configuration allowance. This table is a design coverage checklist, not a declaration of USB compliance.

## Candidate assessment

| Route | Evidence in its favor | Remaining concern / disposition |
|---|---|---|
| BQ25616J plus separate USB input control | Retains the audited charger and low standby draw | Rejected for this coupon. Additional circuitry would still need to override its complete input path and coexist with native data; the direct ILIM route does not do so. |
| BQ24166RGER | Standalone switching charger with pin-selected USB100 and other modes, NTC and power path | Its specified high-impedance battery drain reaches 55 uA under the listed conditions, exceeding the complete badge OFF budget in that mode. Other operating states would need independent characterization; do not accept it from USB-mode support alone. |
| LTC4088EDE#TRPBF | Standalone switching PowerPath with hardware 100/500/1000 mA classes and suspend modes; no charger D+/D- pins | Not selected. Its 35 uA battery-drain maximum plus the gauge's 5 uA leaves only 10 uA for all other OFF loads. |
| `BQ24074RGTR` + `BQ24392RSER` + `TUSB320LAIRWBR` + `TS3USB31ERSER` | Hardware standby/100/500/external modes; low charger battery sleep current; BC1.2 detection; switched-rail data isolation; independent Type-C 1.5 A/3 A permission | **Selected for capture by ADR 0010.** Requires native library review, VBUS-domain level/priority logic, full auxiliary-current budget, linear-charger thermal validation and exact pack qualification. |

The BQ24074 is a 3 × 3 mm, 16-pin VQFN. Its no-input BAT-pin sleep current is 6.5 uA maximum at the stated 85°C condition. With a 1.13 kohm, 1% ISET resistor, the calculated fast-charge range is 0.698–0.872 A. With a 1.78 kohm, 1% ILIM resistor, the external-mode input range is 0.834–0.976 A. Both include the published factor extremes and opposite resistor tolerance. The exact pack must permit the charge-current maximum; all VBUS-only auxiliary loads must fit under the input limit.

This improved OFF budget comes with linear dissipation. At 5 V, 0.8 A and a 3.0 V battery, the first-order charger loss is approximately 1.6 W before system-load terms. TI's thermal model and copper recommendations are not proof of acceptable enclosure temperature. Gate A reviews the layout calculation; the coupon logs charge current, die regulation behavior and case temperature from depleted through full charge.

## Selected permission logic

`TUSB320LAIRWBR` GPIO `OUT1` is high for unattached/default and low for attached 1.5 A/3 A. `BQ24392RSER` `CHG_DET` is high for CDP/DCP and its supported dedicated-charger classifications. Those signals form hardware high-current permission. The ESP32 may request the independent 500 mA mode only for an attached SDP after native USB configuration and while unsuspended.

| High-current permission | Valid SDP grant | BQ24074 `EN2,EN1` | Result |
|---:|---:|---|---|
| 0 | 0 | `1,1` | Standby |
| 0 | 1 | `0,1` | Fixed USB500 ceiling |
| 1 | X | `1,0` | External ILIM ceiling; hardware priority |

Both mode inputs require external pull-ups to the VBUS-only logic rail because the BQ24074's internal pull-downs select USB100, not standby. Loss of a detector, reset or absent firmware must release those pull-down controls and restore `1,1`. BQ24392 `GOOD_BAT` stays high while VBUS is valid to avoid its 30-minute nominal / 45-minute maximum Dead Battery Provision timeout. A second `TS3USB31ERSER`, powered only by switched `+3V3_APP`, isolates the ESP32 data pins while OFF and prevents detector-side signals from back-powering the application. The detector-facing pair uses the switch's `D+/D-` pins covered by the published zero-VCC `Ioff` condition, the ESP32 uses `HSD+/HSD-`, and active-low `OE` is tied to ground. Exact gates/transistors and output-level translation are deferred to the audited-library/capture increment.

Next capture gate: complete native rendering review of the exact BQ24074/BQ24392/TS3USB31E symbols and footprints, select the level-safe priority logic, prove the complete VBUS auxiliary-current budget and encode the state table in the schematic checker. A bigger resistor on the old BQ25616J remains an invalid fix.

The deterministic checker covers all permission-state combinations, resistor extremes and conservative reset/detach defaults. `--require-usb-closure` still returns 1 intentionally until the selected topology is captured. No KiCad source changes in this decision increment, so no native rerun is requested.

## Connector drawing progress

The public GCT PDF at [USB4505 drawing](https://gct.co/files/drawings/usb4505.pdf) became readable through web text extraction on 2026-09-10. It identifies revision A2 dated 2023-12-18, the `03-0-A` ordering suffix and a component-side recommended layout for **0.80 mm PCB thickness**. This is a mechanical constraint to reconcile with the coupon stack-up.

The owner subsequently supplied the original PDF and both pages were visually inspected. The [connector drawing and candidate-library review](usb-connector-audit.md) preserves the 16-contact/12-land mapping, shell-slot coordinates and unresolved cutout reliefs. The recovered symbol, footprint, checker and fault tests pass host validation, and the owner-generated KiCad 10.0.6 exports passed first-author native rendering review at `bf1627c`. The manufacturer drawing is not redistributed. Cutout/process qualification and the selected input circuit's capture remain open.

## Source snapshots

| Primary document | SHA-256 of locally inspected PDF |
|---|---|
| Owner-supplied [GCT USB4505 A2](https://gct.co/files/drawings/usb4505.pdf) | `b1ea604d8e579ee60bf3db78fc55a300bc107cb3bdb3ac3e6c881955898b52ad` |
| [TI BQ25616/J SLUSDF7A](https://www.ti.com/lit/ds/symlink/bq25616.pdf) | `db1c80794273f68d40f13969888a1da6abc08d4a1ea38b68af8b9a09d7c9834a` |
| [TI BQ24165/166/167 SLUSAP4B](https://www.ti.com/lit/ds/symlink/bq24166.pdf) | `9435ba6f350cac8b67948f15aae807146c9156592b6ff54e1aea19e3dee70260` |
| [ADI LTC4088 Rev B](https://www.analog.com/media/en/technical-documentation/data-sheets/4088fb.pdf) | `30f0fbb435a3f7644000bffed2d71e7e85164e706e0184eb25087fc9157a90a2` |

Additional selected-topology sources inspected online on 2026-09-14: [TI BQ2407x SLUS810N](https://www.ti.com/lit/ds/symlink/bq24074.pdf), [TI BQ24392 SLIS146G](https://www.ti.com/lit/ds/symlink/bq24392.pdf), [TI TUSB320LAI SLLSEQ8D](https://www.ti.com/lit/ds/symlink/tusb320lai.pdf), [TI TS3USB31E](https://www.ti.com/lit/ds/symlink/ts3usb31e.pdf), and the [USB-IF Type-C Release 2.5 page](https://usb.org/document-library/usb-type-cr-cable-and-connector-specification-release-25). TI marks all three exact new ICs active. On the inspection date, DigiKey showed 2,842 `BQ24392RSER` with a nine-week standard lead time while Mouser showed 72; this concentration is a sourcing watch item, not purchase authorization. TS3USB31ERSER had more than 20,000 at DigiKey and more than 1,800 at Mouser.

Relevant historical sections: TI BQ25616/J pin functions and input-source/standalone/power-path descriptions; TI BQ24166 electrical characteristics and USB input table; LTC4088 electrical characteristics, Table 1 and PowerPath description. Selected-topology sections: BQ24074 EN1/EN2, quiescent current, programming factors, PowerPath, NTC/timer and thermal guidance; BQ24392 detection/GPIO/data switch; TUSB320 GPIO current states and dead-battery behavior. These are document-based assessments, not measurements or final availability quotes.
