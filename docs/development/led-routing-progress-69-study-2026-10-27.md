<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Routing continuation: 70 to 69 unconnected edges

Historical checkpoint at commit 9015215; see the [65-edge continuation](led-routing-progress-65-study-2026-10-28.md). Validation fingerprints describe files at that commit.

Date: 2026-10-27. Unbuilt, unqualified source study; no hardware measurements or fabrication release. The 50-edge target remains open.

The selected transaction grounds TH1.2 and reduces native/independent physical-pad opens **70 → 69**, retaining exactly **104 unchanged intrinsic DRC findings**. Every accepted 70-edge added copper item and physical pad group survives. The [70-edge integer plan](../../mechanical/review/routing-progress-70-checkpoint.json) freezes commit 7c19554 under ADR 0052. All earlier source replacements and physical connections remain exact.

## Selected local replacements

The additional two [catalog entries](../../mechanical/review/routing-progress-track-replacements.json) preserve each original endpoint and all direct same-net pad/copper contacts on its original layer. All other source copper remains protected.

| Source track | Source → replacement track length, calculated | Replacement bounds, mm | Direct contacts |
|---|---:|---|---:|
| ROW_GATE_09, In2, (54.2, 12.6)–(54.2, 19.9) | 7.3 → 7.5 mm | x 54.2–54.3, y 12.6–19.9 | 4 |
| ROW_SEL_05, In4, (53.35, 15.75)–(55.15, 15.75) | 1.8 → 7.4 mm | x 52.65–55.50, y 14.50–15.75 | 2 |

The gate track stays on In2 with a small local offset. The row-select path uses six adjacent microvias and a bounded local bridge; the added 5.6 mm and its layer transitions remain return/timing review items. A 0.4123 mm calculated back-layer ground lead runs from TH1.2 at (53.950, 16.125) mm to (53.850, 15.725) mm, then three adjacent microvias join In2 ground. Solving the gate replacement before row-select avoids a blocked search that occurs in the opposite order. The complete transaction adds **28 tracks / nine microvias**, replaces two original tracks and adds 35 net copper items. GND opens fall **6 → 5**. No sensor value, pad map, NTC qualification circuit, current/protection/enable setting, firmware or component placement changes.

The board contains **483 footprints / 17,871 copper items**, retains **15,393 nonzero source items** and adds **1,656 tracks / 822 adjacent microvias** relative to the frozen 215-edge source. Exactly five source tracks are replaced, with **23 direct-contact witnesses**. Existing three orphan-via retirements, 116 neutral zero-length cleanups, 34 R/C poses, five original zones, four power parcels and two DSF necks remain unchanged. Ordinary tracks/clearance are 0.20 mm, microvias 0.30/0.10 mm and annulus 0.10 mm; only the two previous exact DSF necks are 0.12 mm.

## Validation

[Full DRC](led-routing-progress-69-drc-2026-10-27.json), [native checks](../../mechanical/review/routing-progress-69-native-check-2026-10-27.json), [orphan-restoration DRC](led-routing-progress-69-orphan-restoration-drc-2026-10-27.json), [remaining-net counts](../../mechanical/review/routing-progress-69-open-nets-2026-10-27.json) and [validation fingerprints](../../mechanical/review/routing-progress-69-validation-2026-10-27.json) record this checkpoint. Three stable refills and two identical PCB/project/custom-rule replays pass. Board SHA-256: `8a763a39aa0089c8c3d2c110e0a73f46a7b17cc905ea1ce6734417a0ea65c8c9`.

Acceptance passes **31 isolated native / 59 portable plan guards**, canonical metadata and **256 LED checks**, plus source-only CI's 21 canonical-source fault methods, 14 distance tests, six path tests and seven clearance tests. The new frozen-70 checks reject losing prior copper or the PAIR10 ground group. Exact catalog fingerprints and independent original-contact checks protect all five source replacements. The separate restored-orphan witness retains all groups and 69 opens while adding only the same three expected dangling-via findings. Final validation fingerprints record the completed checks. Run `./tools/check-routing-progress.sh`.

Further U39 supply and U38 ground transactions do not produce a selected reduction while retaining all previous groups and copper. Unsuccessful finite bounds do not establish impossibility. Router exchange artifacts, vendor files and failed probes remain local ignored output. The supplied Murata sheet matches existing inductor lands; no inductor move or broad switching-node route is selected.

The unbuilt board retains its 104 intrinsic findings, trial-package exceptions, C45/SYS-distribution holds and incomplete electrical, bypass/return, current/thermal, switching-loop, timing/impedance, interlock/partial-power, RF, mechanical and HDI/assembly qualification. Independent Gate A precedes fabrication. Source connectivity does not establish working hardware or authorize manufacturing.
