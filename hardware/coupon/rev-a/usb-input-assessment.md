<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# USB/input closure assessment

Status: direct BQ25616J ILIM-only proposal rejected under [ADR 0009](../../../docs/decisions/0009-usb-input-current-closure.md); replacement remains under evaluation. No new power circuit or component substitution is captured.

## State coverage required

| Source/state | Required design evidence |
|---|---|
| USB absent | No backfeed; application OFF drain below 50 uA including pack, gauge and disabled rails |
| Legacy USB 2.0 host, not configured | Total port draw fits the 100 mA startup allowance, including detector, LDO and indicators; no assumed 500 mA permission |
| Configured host | Any higher draw follows the permitted configuration; the application cannot override the hardware safety ceiling |
| Host suspend | Applicable USB suspend behavior covers the entire product, not only battery charging; resetting or absent firmware must not bypass it |
| BC1.2 charging source | Detection coexists with native data where supported; a charger-selected limit is not assumed to be clamped by an unrelated resistor |
| Type-C default advertisement | Do not equate default Rp with a completed USB configuration or a BC1.2 charging-port classification |
| Type-C 1.5 A / 3 A advertisement | Hardware may select a higher bounded limit only after valid attachment/classification; qualification must disappear on detach or reduced advertisement |
| Switch OFF, reset, depleted battery | Autonomous charging/source limits and stable startup must still work; no dependence on an ESP32 boot sequence for permission to draw more current |

The 100 mA row applies to the legacy USB 2.0 host state, not every Type-C or BC1.2 source. This table is a design coverage checklist, not a declaration of USB compliance.

## Candidate assessment

| Route | Evidence in its favor | Remaining concern / disposition |
|---|---|---|
| BQ25616J plus separate USB input control | Retains the audited charger and low standby draw | Additional circuitry must bound all system current, preserve source detection/data, handle suspend and avoid input-voltage/current-limit oscillation. No circuit selected. |
| BQ24166RGER | Standalone switching charger with pin-selected USB100 and other modes, NTC and power path | Its specified high-impedance battery drain reaches 55 uA under the listed conditions, exceeding the complete badge OFF budget in that mode. Other operating states would need independent characterization; do not accept it from USB-mode support alone. |
| LTC4088EDE#TRPBF | Standalone switching PowerPath with hardware 100/500/1000 mA classes and suspend modes; no charger D+/D- pins | Promising replacement, not selected. Check full port budget, reset/suspend qualification, voltage protection, thermistor and charge settings, efficiency and sourcing. Its 35 uA battery-drain maximum is specified at the listed datasheet conditions, not established here across the full temperature range. Adding the gauge's 5 uA leaves only 10 uA for all other OFF loads. |

The LTC4088 package is 4 × 3 mm and 0.75 mm nominal height. This is compatible with investigating it inside the existing envelope, not proof of final case fit. ADI lists the part in production. The existing BQ charge resistor and NTC network cannot be transferred to it without recalculation. Current-mode labels also do not include arbitrary extra loads connected directly to VBUS outside the charger.

Next selection gate: prove a complete hardware state table and full OFF/current budgets, then choose and audit exact libraries before drawing the power circuit. A bigger resistor on the BQ alone is not a valid fix outside its documented programming range.

Source verification for this increment: 79 host tests pass, including rejection of the historical resistor, rejection of an in-range setting that exceeds a host allowance, rejection of applying unknown-adapter bounds to BC1.2 states, and the explicit USB-closure failure. `--require-usb-closure` returns 1 intentionally for the current incomplete design. No KiCad source changed and no native rerun is requested.

## Connector drawing progress

The public GCT PDF at [USB4505 drawing](https://gct.co/files/drawings/usb4505.pdf) became readable through web text extraction on 2026-09-10. It identifies revision A2 dated 2023-12-18, the `03-0-A` ordering suffix and a component-side recommended layout for **0.80 mm PCB thickness**. This is a mechanical constraint to reconcile with the coupon stack-up.

The text identifies 16 contacts (A1/A4/A5/A6/A7/A8/A9/A12 and B1/B4/B5/B6/B7/B8/B9/B12), including two independent CC contacts, two USB data pairs and SBU contacts. It is insufficient to verify the drawn land/stake/cutout coordinate relationships. Direct PDF download still returned HTTP 403, and the web screenshot response provided no usable image in this environment. Therefore no footprint was inferred. The original PDF is still needed locally for visual dimension verification; the manufacturer drawing is not copied into the public repository.

## Source snapshots

| Primary document | SHA-256 of locally inspected PDF |
|---|---|
| [TI BQ25616/J SLUSDF7A](https://www.ti.com/lit/ds/symlink/bq25616.pdf) | `db1c80794273f68d40f13969888a1da6abc08d4a1ea38b68af8b9a09d7c9834a` |
| [TI BQ24165/166/167 SLUSAP4B](https://www.ti.com/lit/ds/symlink/bq24166.pdf) | `9435ba6f350cac8b67948f15aae807146c9156592b6ff54e1aea19e3dee70260` |
| [ADI LTC4088 Rev B](https://www.analog.com/media/en/technical-documentation/data-sheets/4088fb.pdf) | `30f0fbb435a3f7644000bffed2d71e7e85164e706e0184eb25087fc9157a90a2` |

Relevant sections: TI BQ25616/J pin functions and input-source/standalone/power-path descriptions; TI BQ24166 electrical characteristics and USB input table; LTC4088 electrical characteristics, Table 1 and PowerPath description. [ADI's product page](https://www.analog.com/en/products/ltc4088.html) supplied lifecycle/package context. These are document-based assessments, not measurements or final part availability quotes.
