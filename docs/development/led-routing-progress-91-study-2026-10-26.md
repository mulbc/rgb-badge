<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Routing continuation: 94 to 91 unconnected edges

Historical checkpoint at commit 48cdb7a. Date: 2026-10-26. Status: unqualified native source study; no hardware measurements or fabrication release. The requested 50-edge target remains open.

The selected derivative reduces native and independently counted physical-pad opens **94 → 91**, with exactly **104 unchanged intrinsic DRC findings**. [ADR 0052](../decisions/0052-preserve-94-edge-routing-checkpoint.md) freezes the 94-edge plan: every accepted copper item, completed physical pad group, zone definition and both DSF supply-neck records survive, together with the earlier 100/150/215-edge contracts. No component moves, new necks, copper retirement or zone-definition changes are selected.

## Completed transactions

| Net | Result | Added signal tracks / microvias | Added signal length, calculated |
|---|---|---:|---:|
| MODE_BOOT_N | TP3 joins the existing button/U51/R44/U3 group; net now complete | 4 / 5 | 8.4531 mm |
| ROW_ENABLE_REQ_N | U3.12 joins the existing request/test-pad/interlock group; net now complete | 74 / 8 | 77.4571 mm |
| USB_RAW_OUT1 | U24.1 joins the R60/U31 group; TP20 remains open | 6 / 8 | 34.2162 mm |

Each transaction includes the necessary power-plane repair. Adding its signal alone split a previously completed supply group. Four exact 0.20 mm In2.Cu bridges and eight adjacent microvias restore those groups:

| Net | Zone layer / bridge layer | Start → end, mm | Calculated length |
|---|---|---|---:|
| VLED, mode test-pad transaction | In1 / In2 | (75.430294, 24.182101) → (76.030294, 24.982101) | 1.0000 mm |
| VLED, row-request transaction | In1 / In2 | (74.825, 26.5) → (75.825, 26.7) | 1.0198 mm |
| +3V3_USB, USB-control transaction | In3 / In2 | (25.55, 24.5) → (25.55, 25.5) | 1.0000 mm |
| +3V3_USB, USB-control transaction | In3 / In2 | (24.05, 13.975) → (25.05, 13.975) | 1.0000 mm |

Native checks preserve all previous ground and supply groups after refill. These bridges are routing-source continuity repairs, not current/thermal/transient or return-path qualification. Candidate display-enable outputs remain isolated from actual enable nets; no current/protection/firmware setting changes. The MODE_BOOT_N join is not a demonstrated programming or boot test.

The increment adds **88 tracks / 29 microvias** (117 copper items), retaining all 16,614 items of the 94-edge checkpoint. The resulting board has **483 footprints / 16,731 copper items**. Relative to the frozen 215-edge parent it retains 15,398 nonzero original items and adds **889 tracks / 444 microvias**, with the same **33 passive poses**, five original zones and four selected power parcels. All ordinary tracks/default netclass and clearance remain 0.20 mm, adjacent microvias 0.30/0.10 mm and minimum annulus 0.10 mm. The two previously selected 0.12 mm DSF supply necks and their exact project/custom-rule scope are unchanged.

## Validation and rejected exploration

[Full DRC](led-routing-progress-91-drc-2026-10-26.json), [native checks](../../mechanical/review/routing-progress-91-native-check-2026-10-26.json), [orphan-restoration DRC](led-routing-progress-91-orphan-restoration-drc-2026-10-26.json), [remaining-net counts](../../mechanical/review/routing-progress-open-nets-91-2026-10-26.json) and [validation fingerprints](../../mechanical/review/routing-progress-91-validation-2026-10-26.json) record the selected result. Three refill passes preserve every completed group and original copper net. Two independent replays produce identical PCB/project/custom-rule bytes; PCB SHA-256 is `ddd5560b11656ed8beb7f67bf24921ec346000db599461bd63e234044674e246`.

The full wrapper passes **22 isolated native guards**, all **256 LED placement checks**, canonical source/metadata checks and the independent 91-edge count. Restoring the same three previously retired orphan microvias preserves all selected groups and 91 opens, adding exactly their three dangling-via warnings to the 104 intrinsic findings. The source-only CI layout passes **35 portable plan guards**, **21 canonical-source fault methods**, and routing distance/path/clearance checks. New guards reject losing accepted 94-edge copper, pad groups or neck metadata, including a coordinated candidate/plan copper retirement. Run `./tools/check-routing-progress.sh`; the host-only `python3 tools/check-routing-progress-plan.py` checks fingerprints, immutable board/zone structure and scoped rules.

Larger address-line searches found paths that split VLED into additional islands; attempted local repairs did not preserve every old group. Supervisor and charger-gate paths left USB-logic supply pads disconnected and remain excluded. DSF ground escapes, rear ground-island stitches and additional passive poses produced no accepted lower-count candidate with the required preservation/DRC checks. Outer-layer searches also remain exploratory. Bounds are search limits, not proof that routing is impossible. Rejected boards remain ignored build output.

## Open gates

The board is unbuilt, incomplete and retains the 104 intrinsic findings. GND has 10 opens, VLED 8, application 3.3 V 1; gauge supply, USB and other control paths remain incomplete. Exact parts, values, metadata, pad geometry, numbered nets, schematic/BOM, current limits, protection, firmware and isolated enable boundaries are unchanged. Sixteen trial row pairs and two netless driver projections remain unqualified canonical exceptions. Bypass and converter locality, power/ground bridges, current/voltage-drop/transient/thermal behavior, timing/impedance/partial power, RF/fit and the HDI/assembly process require engineering review and physical evidence. Existing C45/SYS-distribution holds remain. Independent Gate A is mandatory before fabrication; no vendor PDFs or manufacturing files are released.
