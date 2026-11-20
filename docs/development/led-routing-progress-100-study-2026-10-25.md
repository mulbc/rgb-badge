<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Routing checkpoint: 100 unconnected edges

Historical 100-edge snapshot at commit `91090c8`; superseded by the [94-edge continuation](led-routing-progress-94-study-2026-10-26.md). Its frozen integer checkpoint, dated DRC and archived net report retain the original evidence; current derivative paths now contain the newer board.

Date: 2026-10-25. Native source checks of an unbuilt, unqualified study; no hardware measurements or fabrication release.

The [routing derivative](../../hardware/coupon/rev-a/staging/led-routing-progress-trial-114mm.kicad_pcb) reaches **100 native and independently counted physical-pad-cluster opens**, down from the accepted 150-edge checkpoint and the frozen 215-edge source. Full KiCad 10.0.6 DRC retains exactly the original **104 intrinsic findings**. Every accepted 150-edge physical pad group remains joined, including repeated logical drain-pad numbers.

The selected inventory adds **679 tracks and 396 adjacent-layer microvias**, retains **15,398 original nonzero copper items**, and contains **16,473 copper items / 483 footprints**. All ordinary nonzero source tracks and accepted 150-edge tracks remain exact. The original 116 zero-length artifacts remain retired; three displaced-passive orphan microvias also retire under ADR 0046. Restoring those exact three vias independently preserves every selected pad group and the 100-edge count, with precisely three additional `via_dangling` findings and no other DRC difference ([raw restoration DRC](led-routing-progress-orphan-restoration-drc-2026-10-25.json)).

## Selected routing and placement

All added tracks and other-net clearance remain **0.20 mm**. Microvias remain **0.30/0.10 mm**, adjacent layers only, with the original 0.10 mm annular-width floor. No narrower track, reduced project floor, ordinary-track replacement, part/value/net change, current-limit change or enable-domain connection is selected. Sensitive setting/reference/feedback additions remain within 5 mm total per net.

[ADR 0045](../decisions/0045-preserve-connected-groups-during-passive-relocation.md) governs the 31 exact R/C poses below; USB differential series resistors R45/R46 and all other component classes remain fixed. [ADR 0046](../decisions/0046-retire-displaced-passive-orphan-vias.md) requires the orphan restoration witness. Narrower digital tracks and a COL_09_R replacement evaluated in ADRs 0047/0048 are excluded.

[ADR 0049](../decisions/0049-bounded-power-distribution-parcels.md) records four selected bounded parcels: USB 5 V on In1, charger input on In3, protected battery and raw VBUS on In4. All five original zone definitions remain exact. The VBUS right edge is trimmed to x 110.5 mm to retain the application-supply corridor. Exact polygons, holes, net/layer/priority/fill settings and every selected copper item are pinned in the [integer plan](../../mechanical/review/routing-progress-plan.json). The independent verifier checks both native zone geometry and complete source definitions.

SYS pours that split old VLED, USB-logic or ground groups are rejected. The selected SYS distribution uses ordinary-width escapes and a perimeter crossing; a three-item R14.1–R13.1 VLED bridge preserves the earlier VLED group. A rejected C45 site overlapped a retired via and failed restoration evidence. Its selected replacement at (5, 30.5) preserves the count and satisfies that evidence. This placement and the long supply distribution remain **bypass-locality, current-density, voltage-drop, return-path and transient-review holds**; connectivity is not supply qualification.

| Part | Original x, y (mm) | Selected x, y (mm) | Original → selected angle (°) |
|---|---:|---:|---:|
| C30 | 97.25, 9 | 107.295, 16 | 180 → 180 |
| C31 | 49.75, 2.75 | 103.495, 17.5 | 180 → 180 |
| C39 | 59.75, 2.75 | 19.745, 2.65 | 180 → -90 |
| C4 | 62.25, 2.75 | 97.77, 17.875 | 180 → 180 |
| C40 | 36.75, 1 | 39.75, 4 | 180 → 180 |
| C44 | 43.75, 1 | 36.75, 1 | 180 → 180 |
| C45 | 47.25, 1 | 5, 30.5 | 180 → 0 |
| C5 | 64.75, 2.75 | 41.75, 13.045 | 180 → 180 |
| C50 | 67.25, 2.75 | 56.885, 19.295 | 180 → 180 |
| C51 | 69.75, 2.75 | 54.885, 17.75 | 180 → 0 |
| C64 | 39.75, 4.25 | 50.25, 2.705 | 180 → 90 |
| R103 | 54.75, 4.25 | 31.195, 17.825 | 180 → -90 |
| R105 | 59.75, 4.25 | 21.395, 28.7 | 180 → 180 |
| R106 | 62.25, 4.25 | 93.9537, 26.25 | 180 → 180 |
| R107 | 64.75, 4.25 | 21.3, 21.35 | 180 → 0 |
| R108 | 67.25, 4.25 | 109.825, 22.005 | 180 → -90 |
| R109 | 69.75, 4.25 | 32.75, 6.75 | 180 → 180 |
| R3 | 47.25, 7.25 | 10.935, 30.7 | 180 → 0 |
| R38 | 69.75, 7.25 | 110.213, 9.845 | 180 → -90 |
| R39 | 72.25, 7.25 | 112.213, 9.345 | 180 → 180 |
| R42 | 39.75, 8.75 | 108.487, 9.345 | 180 → 180 |
| R44 | 44.75, 8.75 | 1.55, 30.795 | 180 → 180 |
| R5 | 54.75, 8.75 | 28.2513, 27.75 | 180 → 180 |
| R60 | 59.75, 8.75 | 25.225, 28.27 | 180 → 0 |
| R63 | 67.25, 8.75 | 104.8, 12.825 | 180 → 180 |
| R70 | 72.25, 8.75 | 95.7513, 22.25 | 180 → -90 |
| R78 | 42.25, 10.25 | 88.0463, 22 | 180 → -90 |
| R8 | 47.25, 10.25 | 72.575, 9 | 180 → -90 |
| R88 | 69.75, 10.25 | 106.65, 18 | 180 → -90 |
| R89 | 72.25, 10.25 | 59.865, 15 | 180 → -90 |
| R97 | 97.25, 17.5 | 106.7, 14 | 180 → -90 |

## Validation and reproduction

The [native check](../../mechanical/review/routing-progress-native-check-2026-10-25.json), [full DRC](led-routing-progress-drc-2026-10-25.json), [complete remaining-net counts](../../mechanical/review/routing-progress-open-nets-2026-10-25.json) and [validation fingerprints](../../mechanical/review/routing-progress-validation-2026-10-25.json) record the selected result. The [manifest](../../mechanical/review/routing-progress-trial.json) pins the board, project, plan and generator. Two replays produce identical board SHA-256 `3a16b0d69a0d831a99485aa6d2011d2b01f8d0f1a306a3f1a43f3d078235eddd`. Native source checks cover 19 isolated native guard methods, 19 portable plan methods, all 256 LED placements and the exact metadata/pin assignments of 465 shared canonical components / 1,718 logical pins. The source-only CI layout includes 21 canonical-source fault methods and routing-search tests.

Run `./tools/check-routing-progress.sh` from the repository root on the owner's KiCad installation. `python3 tools/check-routing-progress-plan.py` runs the portable plan/profile check. The wrapper also restores the three orphan vias into ignored review output, verifies their exact additional findings, and runs each native fault in a separate process. Refill and source inventory checks reject silent track-net relabelling during native merges.

## Open findings and release boundary

The board is incomplete at 100 opens and retains the 104 intrinsic findings. Exact component metadata is preserved, but the sixteen trial row packages and two netless driver projections remain unqualified canonical exceptions. All electrical behavior, input/protection/charging limits, bypass and converter loops, current/voltage-drop/thermal/SI/HDI process, RF and mechanical fit require engineering review and physical validation. Current limits, firmware and isolated enable boundaries are unchanged. Independent Gate A remains mandatory before fabrication; no manufacturing artifacts are released.
