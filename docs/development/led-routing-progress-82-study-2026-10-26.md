<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Routing continuation: 84 to 82 unconnected edges

Historical checkpoint at 88fdcbe; superseded by the [76-edge continuation](led-routing-progress-76-study-2026-10-27.md). Validation fingerprints describe the files at that commit.

Date: 2026-10-26. Status: unqualified native source study; no hardware measurements or fabrication release. The requested 50-edge target remains open.

The selected derivative reduces native and independently counted physical-pad opens **84 → 82**, retaining exactly **104 unchanged intrinsic DRC findings**. The [84-edge checkpoint](../../mechanical/review/routing-progress-84-checkpoint.json) is additionally frozen under [ADR 0052](../decisions/0052-preserve-94-edge-routing-checkpoint.md). Every selected copper item, completed physical pad group, zone definition and both prior DSF neck records survive, together with all earlier 91/94/100/150/215-edge contracts.

## Completed transactions

| Transaction | Result | Added tracks / adjacent microvias | Added track length, calculated |
|---|---|---:|---:|
| ROW_A1 signal | U3.5 joins R39.1/U2.3; all four address nets now form single physical pad groups | 69 / 44 | 128.9522 mm |
| Address-route ground restoration | Restores the main GND group plus the PAIR15 ground fragment split by the signal | 6 / 4 | 11.6582 mm |
| C67/U48 ground | The pre-existing C67.2/U48.3 ground island joins the main ground group | 27 / 0 | 7.4075 mm |

The main ground restoration uses four B.Cu leads and a 7.1 mm In4.Cu bridge from (74.2, 10.2) to (67.1, 10.2) mm, with two adjacent B/In4 microvias. The separate PAIR15 repair is a 1 mm In4.Cu bridge from (76.799653, 29.399500) to (77.599653, 29.999500) mm, with two adjacent B/In4 microvias. The C67/U48 connection is entirely on B.Cu. These source continuity checks do not qualify ground impedance, local bypass behavior, current, transient response or timing. The long address route and its layer transitions remain explicit SI/process review work.

The increment adds **102 tracks / 48 microvias** (150 copper items), retaining all 17,322 items of the 84-edge checkpoint. The resulting board has **483 footprints / 17,472 copper items**. Relative to the frozen 215-edge parent it retains 15,398 nonzero original items and adds **1,378 tracks / 696 microvias**. No component moves, additional necks, power/supply routes, copper retirement or zone-definition changes are selected. The same 33 passive poses, five original zones, four power parcels and two exact 0.12 mm supply necks remain. Ordinary tracks/default netclass and clearance stay 0.20 mm, microvias 0.30/0.10 mm and minimum annulus 0.10 mm. Parts, fields, pad geometry, numbered nets, current/protection settings, firmware and isolated enable boundaries remain unchanged.

## Validation and rejected exploration

[Full DRC](led-routing-progress-82-drc-2026-10-26.json), [native checks](../../mechanical/review/routing-progress-82-native-check-2026-10-26.json), [orphan-restoration DRC](led-routing-progress-82-orphan-restoration-drc-2026-10-26.json), [remaining-net counts](../../mechanical/review/routing-progress-82-open-nets-2026-10-26.json) and [validation fingerprints](../../mechanical/review/routing-progress-82-validation-2026-10-26.json) record the result. Three refills preserve every old copper net and completed physical group. Two independent replays produce identical PCB/project/custom-rule bytes. PCB SHA-256: `14cd20aca2d1f803c8de9f1d0a60afce85d1991e68e637c2fa9e21fca97b4bb1`.

The complete wrapper passes **24 isolated native guards**, all **256 LED checks**, canonical source/metadata checks and the independent 82-edge count. Restoring the same three previously retired orphan vias preserves all selected groups and 82 opens, adding exactly their three dangling-via warnings to the 104 intrinsic findings. Source-only CI passes **41 portable plan guards**, **21 canonical-source fault methods**, 14 distance tests, six path tests and seven clearance tests. New guards reject loss of accepted 84-edge copper or completed groups, including coordinated candidate/plan copper retirement. Run `./tools/check-routing-progress.sh`.

A finer 0.05 mm search lattice finds the C67/U48 ground path missed by the preceding 0.10 mm trial. Exact native shape screening and all physical dimensions remain unchanged. Separate 0.025 mm bounded NTC/resistor ground trials do not add an accepted connection. Original-width row-gate searches, attempted resistor relocations and ground stitches also yield no selected improvement. Search bounds do not prove routing impossible.

The [TI inverter Rev. AF](https://www.ti.com/lit/ds/symlink/sn74lvc1g04.pdf) and [AND-gate Rev. AA](https://www.ti.com/lit/ds/symlink/sn74lvc1g08.pdf) pin tables and DSF land data were rechecked against [ADR 0051](../decisions/0051-bounded-dsf-pad-necks.md). Three legal signal-neck seeds and ground-neck trials fail to produce complete accepted routes; none is selected. Intermediate dangling seeds remain ignored output. Neighboring seed interactions and the upper-edge search boundary were investigated without relaxing dimensions or expanding neck scope.

An earlier 83-edge candidate restores address continuity using 121.7658 mm of additional battery routing and 29.7123 mm of USB-logic supply routing. That candidate and its supply detours remain excluded. The selected address search excludes horizontal signal steps on the LED and battery distribution layers; it retains all prior supply groups after its ground repairs. A separate trial excluding every power layer exhausts its configured graph. Every selected integer copper item is replayed independently; exploratory scripts/boards remain ignored local output.

## Open gates

GND still has nine opens, VLED eight and application 3.3 V one. Gauge supply, USB, other controls, display paths and remaining row-gate connections are incomplete. The board is unbuilt and retains the 104 intrinsic findings. Sixteen trial row pairs and two netless driver projections remain unqualified canonical exceptions. Existing C45/SYS-distribution holds remain. Bypass/return quality, supply/ground current and voltage drop, transients/thermal behavior, signal timing/impedance, partial-power/interlock operation, RF/fit and HDI/assembly process require engineering review and physical evidence. Independent Gate A remains mandatory before fabrication. No vendor PDFs or manufacturing files are released.
