<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Routing continuation: 100 to 94 unconnected edges

Historical 94-edge snapshot at commit `759700b`, superseded by the [91-edge continuation](led-routing-progress-91-study-2026-10-26.md). Its frozen integer checkpoint and dated evidence remain available; current derivative paths now contain the newer board.

Date: 2026-10-26. Status: unqualified native source study, not a hardware measurement or fabrication release. The requested 50-edge target has not been reached.

The selected derivative reduces native and independently counted physical-pad opens **100 → 94**. Full KiCad 10.0.6 DRC retains exactly the **104 unchanged intrinsic findings**. Every completed 100/150/215-edge physical pad group survives. All selected 100-edge copper and all ordinary nonzero parent tracks remain exact; no further orphan retirement or zone change is selected. [ADR 0050](../decisions/0050-preserve-100-edge-routing-checkpoint.md) freezes the accepted 100-edge integer plan and project profile.

## Selected changes

Three application-supply connections, one +5V connection, one ground connection and one mode-button connection close. Remaining counts include GND 10, VLED 8, application 3.3 V 1, gauge supply 3 and unfinished USB/control paths. [The complete net report](../../mechanical/review/routing-progress-open-nets-94-2026-10-26.json) records all 94 edges.

U48.6 and U52.6 now escape their fixed DSF lands through two explicitly enumerated straight B.Cu necks, respectively **0.55 mm and 0.65 mm long / 0.12 mm wide**. [ADR 0051](../decisions/0051-bounded-dsf-pad-necks.md) records the current manufacturer drawings, calculated neighbour clearance and illustrative DC sensitivity. These exceptions apply only to the exact numbered pins, nets, fixed pad centres, layer, outward direction and bounded lengths. They do not narrow supply distribution or raise a current setting. Ordinary selected tracks/default netclass remain 0.20 mm; clearance remains 0.20 mm, adjacent-layer microvias 0.30/0.10 mm and minimum annulus 0.10 mm. The absolute project track floor alone becomes 0.12 mm; exact native custom rules and independent integer checks constrain its use. No signal seed neck is selected.

C55 and C71 shared an isolated ground group. Moving either alone split that group. A joint placement/routing transaction joins both capacitors to existing supply and ground copper while preserving their previous relationship and every other completed group. A more remote 95-edge pose was superseded by the selected poses near the associated circuit areas:

| Part | Previous centre, mm | Selected centre, mm | Native angle |
|---|---|---|---|
| C55 | 72.25, 2.75 | 100.25, 12.755 | 180 → 0° |
| C71 | 71.75, 0.75 | 68.1, 3.295 | 180 → 90° |

These positions and DC connectivity do not establish bypass-loop quality. U52 ground remains open, and supply/bypass/return qualification remains required.

The mode-button/U51 group joins the existing R44/U3 MODE_BOOT_N group using original-width routing. Its initial path cut the USB-logic supply zone. An exact **1.1314 mm In2.Cu / 0.20 mm** supply bridge with two adjacent In2/In3 microvias restores that old group. Its endpoints are (76.951904, 30.049096) and (76.151904, 30.849096) mm. All old supply and ground groups survive after refill. TP3's mode-button test-pad leg remains open. This is neither a programming demonstration nor return/current/impedance qualification.

The resulting board has **483 footprints / 16,614 copper items**. Relative to the frozen 215-edge parent it retains 15,398 nonzero original items and adds **801 tracks / 415 adjacent microvias**, with **33** exact passive poses. The increment beyond the accepted 100-edge checkpoint adds 122 tracks / 19 microvias and moves two capacitors. The original five zone definitions and four accepted power parcels remain exact. The previously proved 116 zero-length artifact and three orphan-via retirements are unchanged.

## Rejected exploration

Short original-width paths and single-passive localization made no accepted progress. Larger forward/reverse native-grid searches reached their bounds or produced routes that split established supply/ground groups. A research search avoiding horizontal In4/In2 routing found the selected mode-button path, with its USB-supply repair required as one transaction. Courtyard proximity alone never qualified a route.

A separate MODE_BOOT_N test-pad path needed application and battery supply repairs. Combining it with the selected mode-button path split the application supply and changed DRC; it is excluded. A shorter test-pad tail split VLED and is excluded. Other DSF neck seeds failed preservation or left a dangling via and are excluded. Search bounds are exploration limits, not proof that no route exists. Rejected boards remain ignored build output.

## Verification and replay

[Native checks](../../mechanical/review/routing-progress-native-check-2026-10-26.json), [full DRC](led-routing-progress-drc-2026-10-26.json), [orphan-restoration DRC](led-routing-progress-orphan-restoration-drc-2026-10-26.json) and [validation fingerprints](../../mechanical/review/routing-progress-validation-2026-10-26.json) record the selected checkpoint. The [manifest](../../mechanical/review/routing-progress-trial.json) pins the PCB, project, custom rules, integer plan and generator. Two independent replays produce identical PCB/project/custom-rule bytes; PCB SHA-256 is `bddfeef9e0296489319ba9433343ad597189b1e5ba78ef0cf6132e4eaa8c6ea2`.

The full wrapper checks 21 isolated native fault methods, all 256 LED placements, the canonical contract and the independent 94-edge count. Restoring the same three orphan vias preserves all selected groups and 94 opens, adding exactly their three dangling-via warnings to the 104 intrinsic findings. The source-only CI layout passes 31 portable plan guards, 21 canonical-source fault methods and the routing distance/path/clearance tests. Guards reject losing an accepted 100-edge join/copper item, undeclared narrow tracks, wrong-pin/net/layer/direction/length necks and coordinated candidate/plan neck edits. The complete project profile must equal the frozen 100-edge profile except for its reviewed absolute track floor.

Reproduce with `./tools/check-routing-progress.sh`. Generate with KiCad's bundled Python and `tools/generate-routing-progress-trial.py`; the generator replays from the frozen 215-edge source and writes the exact project/custom rules. The host-only `python3 tools/check-routing-progress-plan.py` checks fingerprints, integer exceptions, frozen checkpoints, zones and rules.

## Remaining gates

The board is unbuilt, incomplete and retains the 104 intrinsic findings. Sixteen trial NTLJD3119CTBG row pairs and two netless driver projections remain unqualified canonical exceptions. Exact MPNs, metadata, values, relative pad geometry, pin numbers/nets, schematic/BOM, firmware, current limits, protection and isolated enable boundaries are unchanged. Bypass and converter locality, all supply/return bridges and current capacity, voltage drop, transients, SI/timing, partial power, RF/fit and the sequential-lamination/assembly process require review and physical evidence. C45 and the earlier long SYS distribution retain their existing holds. Independent Gate A remains mandatory before fabrication; no manufacturing files or vendor PDFs are released.
