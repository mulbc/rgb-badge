<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Routing continuation: 91 to 84 unconnected edges

Historical checkpoint at commit e095f3b. Date: 2026-10-26. Status: unqualified native source study; no hardware measurements or fabrication release. The requested 50-edge target remains open.

The selected derivative reduces native and independently counted physical-pad opens **91 → 84**, retaining exactly **104 unchanged intrinsic DRC findings**. The [91-edge checkpoint](../../mechanical/review/routing-progress-91-checkpoint.json) is frozen under [ADR 0052](../decisions/0052-preserve-94-edge-routing-checkpoint.md). Every selected copper item, completed physical pad group, zone definition and both DSF neck records survive, together with the earlier 94/100/150/215-edge contracts. No component moves, additional necks, copper retirement or zone-definition changes are selected.

## Completed transactions

| Net | Result | Added signal tracks / microvias | Added signal length, calculated |
|---|---|---:|---:|
| APP_SUPERVISOR_OK | U51.1 joins the existing supervisor group; complete | 66 / 30 | 130.3544 mm |
| CHARGER_GATE_EN | TP35 joins the existing charger-gate control group; complete | 20 / 31 | 83.1513 mm |
| ROW_A0 | Address group complete | 78 / 35 | 129.9315 mm |
| ROW_A2 | U2.21 joins R40.1/U3.6; complete | 89 / 21 | 110.6445 mm |
| ROW_A3 | U2.22 joins R41.1/U3.7; complete | 45 / 31 | 115.6403 mm |
| USB_OUT1 | U24.6 joins the existing USB control group; complete | 72 / 32 | 142.6262 mm |
| USB_RAW_OUT2 | U24.3 joins R61.1; U31.8 remains open | 13 / 16 | 82.0710 mm |

Ground repairs are part of the corresponding signal transactions. The increment adds 4 original-width 0.20 mm ground tracks and 8 adjacent 0.30/0.10 mm microvias, restoring ground groups and the original via stranded by these signals:

| Bridge layer | Start → end, mm | Calculated length |
|---|---|---:|
| In4.Cu | (2.514142, 28.202801) → (2.714142, 27.602801) | 0.6325 mm |
| In4.Cu | (53.231457, 23.886500) → (53.231457, 22.886500) | 1.0000 mm |
| In3.Cu | (73.886187, 30.796399) → (72.686187, 30.796399) | 1.2000 mm |
| In1.Cu | (99.350000, 6.800000) → (98.350000, 6.800000) | 1.0000 mm |

Three filled-zone passes preserve every previous physical pad group and copper net. These continuity repairs do not qualify current, ground impedance, bypass placement, return paths or transient behavior. The address/control routes have substantial lengths and layer transitions; timing, edge quality, parasitics and process capability remain review and measurement work. Candidate display-enable outputs remain isolated from actual enables. No current/protection/firmware setting changes.

The increment adds **387 tracks / 204 microvias** (591 copper items), retaining all 16,731 items of the 91-edge checkpoint. The resulting board has **483 footprints / 17,322 copper items**. Relative to the frozen 215-edge parent it retains 15,398 nonzero original items and adds **1,276 tracks / 648 microvias**, with the same 33 passive poses, five original zone definitions and four selected power parcels. Ordinary tracks/default netclass and clearance remain 0.20 mm, adjacent microvias 0.30/0.10 mm and minimum annulus 0.10 mm. The two prior 0.12 mm DSF supply necks and exact project/custom-rule scope are unchanged.

## Validation and rejected exploration

[Full DRC](led-routing-progress-84-drc-2026-10-26.json), [native checks](../../mechanical/review/routing-progress-84-native-check-2026-10-26.json), [orphan-restoration DRC](led-routing-progress-84-orphan-restoration-drc-2026-10-26.json), [remaining-net counts](../../mechanical/review/routing-progress-open-nets-84-2026-10-26.json) and [validation fingerprints](../../mechanical/review/routing-progress-84-validation-2026-10-26.json) record the selected result. Two independent replays produce identical PCB/project/custom-rule bytes. PCB SHA-256: `1d4882c4105605a9b2608383643512112c411d11d0c2065035100752203edc14`.

The complete wrapper passes **23 isolated native guards**, all **256 LED checks**, canonical source/metadata checks and the independent 84-edge count. Restoring the same three retired orphan microvias preserves all selected groups and 84 opens, adding exactly their three dangling-via warnings to the 104 intrinsic findings. Source-only CI passes **38 portable plan guards**, **21 canonical-source fault methods**, 14 distance tests, six path tests and seven clearance tests. New guards reject loss of accepted 91-edge copper or completed groups, including coordinated candidate/plan copper retirement. Run `./tools/check-routing-progress.sh`.

Local search used a coarser search lattice and changed layer costs while retaining exact native shapes, physical widths and clearances. A later search excluded horizontal signal steps on In1 to avoid LED-supply splits. Every selected path is represented by exact integer copper in the deterministic plan; search settings do not relax physical rules. Pure outer-layer searches exhausted their configured graph without accepted joins. Other address/control trials split completed ground or supply groups and were rejected unless repaired and fully rechecked. Independently combining one USB trial with an address trial produced two real crossing/short findings and was rejected; the selected USB route was searched afresh against the address copper. An 84-edge trial initially stranded an accepted ground microvia at (99.35, 6.8) mm. A 1 mm In1.Cu ground bridge to (98.35, 6.8) mm with two adjacent In1/In2 microvias restores it; the original via is retained. Additional ground stitching, row-gate searches and local UART repairs yielded no selected lower-count board. The remaining address-line trial splits USB-logic and battery-supply groups and remains excluded. Search bounds do not prove routing impossible. Exploratory scripts/boards remain ignored local output.

## Open gates

The board is unbuilt, incomplete and retains the 104 intrinsic findings. GND has 10 opens, VLED eight, application 3.3 V one; gauge supply, USB and other controls remain incomplete. Parts, values, metadata, pad geometry, numbered nets, schematic/BOM, current limits, protection, firmware and isolated enable boundaries are unchanged. Sixteen trial row pairs and two netless driver projections remain unqualified canonical exceptions. Existing C45/SYS-distribution holds remain. Supply/bypass/return quality, current/voltage-drop/transient/thermal behavior, timing/impedance/partial power, RF/fit and HDI/assembly process require engineering review and physical evidence. Independent Gate A is mandatory before fabrication. No vendor PDFs or manufacturing files are released.
