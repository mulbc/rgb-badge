<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Application, USB-logic and VLED distribution studies

Status: **unbuilt source geometry with full native DRC evidence**. Three successive derivatives add supply copper to the [354-open local-control board](led-local-control-study-2026-10-20.md). Together they close **92 native connection edges**, leaving **262**. Each stage retains exactly the original **104 intrinsic footprint-clearance findings**; these remain unresolved and are not a clean fabrication DRC result.

| Stage | Added pour | Rail opens before → after | Total opens | Source output in main group |
|---|---|---:|---:|---|
| [Application](../../hardware/coupon/rev-a/staging/led-app-distribution-trial-114mm.kicad_pcb) | +3V3_APP, In4.Cu | 46 → 7 | 315 | U36, TPS631000 |
| [USB logic](../../hardware/coupon/rev-a/staging/led-usb-distribution-trial-114mm.kicad_pcb) | +3V3_USB, In3.Cu | 32 → 4 | 287 | U29, TPS70933 |
| [LED supply](../../hardware/coupon/rev-a/staging/led-vled-distribution-trial-114mm.kicad_pcb) | VLED, In1.Cu | 40 → 15 | 262 | U37, TPS63020 |

## Generation and acceptance

The [generator](../../tools/generate-supply-distribution-trial.py) uses a native effective-shape screen at 0.20 mm clearance to place direct adjacent-layer microvia stacks where possible, fills one new supply zone, then searches short routed escapes from the remaining rear pads to its main filled region. Six-layer search cells are 0.05 mm; tracks/clearance are 0.20 mm; provisional microvias are 0.30/0.10 mm. Search discovery is capped at 500,000 nodes per source. Via and planar steps have equal search cost, so this is not an optimization of HDI cost or electrical returns.

There are 37 accepted direct anchors plus five routed escapes in the application stage, 17 plus fifteen in the USB stage, and eight plus eighteen in VLED. These produce 86, 113 and 297 added tracks/vias respectively. Anchor counts are not connection-edge reductions: stacks may reach separate copper regions or already shared pad groups. The main application group includes the converter, ESP32 and TLC59581 supply pads. All three source outputs reach their respective main native groups, but none of the rails is completely connected.

All 483 footprints/pad maps and every original track/via survive. Ground and earlier supply pours are refilled around new copper. Their regions and areas change; the [saved-board checker](../../tools/check-supply-distribution-trial.py) requires **every non-target pad cluster to remain exactly unchanged** and forbids splitting an existing target cluster. In particular GND remains at 27 opens, and later stages preserve the application/USB connections already made. No net, part value, enable connection, firmware or current limit changes. Default-disabled VLED and candidate interlock boundaries are unchanged.

Evidence for each stage:

| Stage | Generation | Saved-board result | Native per-net report | Full native DRC |
|---|---|---|---|---|
| Application | [Manifest](../../mechanical/review/app-distribution-trial.json) | [Check](../../mechanical/review/app-distribution-check.json) | [Opens](../../mechanical/review/app-distribution-open-nets.json) | [JSON](led-app-distribution-drc-2026-10-20.json) |
| USB logic | [Manifest](../../mechanical/review/usb-distribution-trial.json) | [Check](../../mechanical/review/usb-distribution-check.json) | [Opens](../../mechanical/review/usb-distribution-open-nets.json) | [JSON](led-usb-distribution-drc-2026-10-20.json) |
| VLED | [Manifest](../../mechanical/review/vled-distribution-trial.json) | [Check](../../mechanical/review/vled-distribution-check.json) | [Opens](../../mechanical/review/vled-distribution-open-nets.json) | [JSON](led-vled-distribution-drc-2026-10-20.json) |

The reports identify KiCad 10.0.6, hashes, every attempt, source-connected groups and filled-zone geometry. Full native and pad-cluster edge counts reconcile at each stage. Every DRC finding's normalized type, severity, description and physical items match the baseline, not merely its count. The final VLED-stage LED check passes all 256 exact placements/rotations/pad maps/nets.

Second full generations are byte-identical:

- Application: `102fd0ce366b200481d7a2d7a388a3c9fbccc9cb84932a32cae0be12ae52a518`.
- USB logic: `b911e6e106d8494fe0b1f4cd17310b65f90e0c210333d7c5c163cb044db2a548`.
- VLED: `b6fde6e68dcba7f2ec012989f1d8d97cb71dea4efc4fd009f2951cfc7d61e5e7`.

Run `./tools/check-supply-distribution.sh app`, `usb` or `vled` for full saved-board acceptance; the default is `vled`. Generate with KiCad's bundled Python and `tools/generate-supply-distribution-trial.py --rail NAME`, in app → usb → vled order. Native DRC may require desktop access on macOS.

## Qualification and remaining work

This is a connectivity/clearance result, **not approval of supply delivery**. In particular, the widely separated converter/output capacitors still need coordinated local placement and loop routing under ADR 0017; a broad plane does not qualify bypass performance. No current-carrying capacity is assigned to the 0.20 mm escapes, microvia stacks or fragmented pours. Minimum copper thickness, voltage drop, peak/overlap/fault current, startup/transients, thermal rise and compact-board return paths require reviewed calculations and hardware qualification. This work raises no source, charge or LED current ceiling.

The final ground pour still has multiple physical regions and 27 pad-cluster opens. Remaining rail opens are explicit in the reports. Row anode nets also retain one isolated physical drain island per pair at this checkpoint, despite complete LED-to-perimeter-pad joins; these need local same-net ties. Eight gate pullups and the other controls remain incomplete. Broad power copper has no antenna/EMI/RF, thermal-relief or enclosure review. Mask/paste, selected HDI fabrication, canonical row-package/net reconciliation, pack/sensor fit, interlock behavior and independent Gate A remain open. No hardware revision, firmware revision, bench setup or measured result exists for these studies. They are never fabrication source.
