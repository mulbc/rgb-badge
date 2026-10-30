<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Routing checkpoint: 150 unconnected edges

Historical checkpoint, superseded by the [100-edge continuation](led-routing-progress-100-study-2026-10-25.md). The mutable routing derivative now contains that continuation; commit `8b3a74b98428f6d3aec3673065bcaf7bc337b70c` retains this 150-edge board, and the frozen 150-edge integer plan remains in `mechanical/review/routing-progress-150-checkpoint.json`.

Date: 2026-10-23. This is native source validation of an unbuilt, unqualified engineering study. No hardware was measured and no fabrication release is authorized.

The [current derivative](../../hardware/coupon/rev-a/staging/led-routing-progress-trial-114mm.kicad_pcb) reduces both the full native count and the independently counted physical-pad-cluster count from **215 to exactly 150**. Full KiCad 10.0.6 DRC retains the **exact same 104 existing findings**. The frozen native-control source remains available unchanged.

The selected plan adds **440 tracks and 212 adjacent-layer microvias**, retains all **15,401 nonzero source copper items**, and removes only the **116 exactly zero-length source tracks**. A separate native regression proves that removal alone leaves every original pad group exact and the original count at 215. The resulting board contains 16,053 copper items and 483 footprints.

Twelve audited passives move closer to their associated networks under [ADR 0044](../decisions/0044-localize-unrouted-study-passives.md). Their exact MPNs, fields, footprint-relative pad geometry, pin numbers and nets remain unchanged. Every prior physical pad group is preserved using pose-independent physical identities, including duplicated drain-pad numbers. All 256 LED positions, rotations and pad maps remain exact. Canonical comparison passes for 465 shared components and 1,718 logical pins; the existing trial row packages and two netless driver projections remain unselected exceptions.

## Selected dimensions and placements

Every selected added track is **0.20 mm**; other-net clearance remains **0.20 mm**, microvias remain **0.30/0.10 mm**, and minimum annular width remains **0.10 mm**. No narrower signal track is selected. [ADR 0043](../decisions/0043-bounded-signal-pad-escapes.md) records the rejected width/via studies. Added sensitive current/reference/feedback-setting copper stays within 5 mm total per net.

The [integer plan](../../mechanical/review/routing-progress-plan.json) is authoritative for exact poses and copper; coordinates below are native-source positions in millimetres.

| Part | Original x, y (mm) | Selected x, y (mm) | Original → selected angle (°) |
|---|---:|---:|---:|
| C51 | 69.75, 2.75 | 54.885, 17.75 | 180 → 0 |
| R109 | 69.75, 4.25 | 32.75, 6.75 | 180 → 180 |
| R3 | 47.25, 7.25 | 10.935, 30.7 | 180 → 0 |
| R38 | 69.75, 7.25 | 110.2125, 9.845 | 180 → -90 |
| R39 | 72.25, 7.25 | 112.2125, 9.345 | 180 → 180 |
| R5 | 54.75, 8.75 | 28.251262, 27.750001 | 180 → 180 |
| R63 | 67.25, 8.75 | 104.8, 12.825 | 180 → 180 |
| R70 | 72.25, 8.75 | 95.751262, 22.250001 | 180 → -90 |
| R8 | 47.25, 10.25 | 72.575, 9 | 180 → -90 |
| R88 | 69.75, 10.25 | 106.65, 18 | 180 → -90 |
| R89 | 72.25, 10.25 | 59.865, 15 | 180 → -90 |
| R97 | 97.25, 17.5 | 106.7, 14 | 180 → -90 |

## Validation and reproduction

- Full [native DRC](led-routing-progress-drc-2026-10-23.json), [independent geometry check](../../mechanical/review/routing-progress-native-check-2026-10-23.json) and [complete per-net open counts](../../mechanical/review/routing-progress-open-nets-2026-10-23.json) agree on 150 remaining edges.
- All 13 isolated native guard methods pass, covering exact cleanup neutrality, nonzero source-copper retention, selected and unexpected poses, duplicated physical lands, pad shape/net drift, detached routing, narrowed ground, skipped via layers, restored zero-length artifacts and MPN substitution.
- All ten portable plan guards pass. The source-only CI layout passes both old/new canonical checks, the plan/profile check, ten plan guards and 21 canonical-source fault methods. The workflow now includes the new board explicitly.
- Replaying twice produces the identical board SHA-256 `cd4c51dc74c6ef15d408e0ce004645c3077df6da15681378a6e48d11284d98f6`. The [manifest](../../mechanical/review/routing-progress-trial.json) pins the source, selected plan, project rules, generator and board. [Validation evidence](../../mechanical/review/routing-progress-validation-2026-10-23.json) pins checker/guard sources and reports.

From the repository root on the owner's KiCad installation:

```sh
/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/3.9/bin/python3 tools/generate-routing-progress-trial.py
./tools/check-routing-progress.sh
```

Searches evaluated group pairs and exact native endpoints, refilled zones after each proposal, and rejected plane splits or changed DRC findings. Local placement resolves passive-to-IC locality that long global detours could not. Selected connected route components are combined independently; counts from separate boards are never added together. The generator replays the selected integer geometry and poses without needing any local search candidates or manufacturer PDFs.

## Remaining work

The largest remaining groups are application input (12), ground (12), VLED (8), USB 5 V (7), connector VBUS (6), application 3.3 V (5) and switched gauge supply (5). The complete report lists all 150 edges. Supply/return current and thermal capacity, feedback/Kelvin paths, decoupling, signal timing/impedance, current-setting behavior, partial-power and interlock operation, HDI process/stack, assembly and enclosure fit remain unqualified. Values, current ceilings, firmware and isolated enable-domain net boundaries are unchanged. Independent Gate A is still required before fabrication. No manufacturer PDFs, local probes or manufacturing outputs are included.
