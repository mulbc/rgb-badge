<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Ground-return island routing on the combined board

Status: **unbuilt geometry study, full native DRC checked**. This derivative retains the [validated ground escapes](led-ground-escape-study-2026-10-20.md), adds solid rear GND copper and four targeted ground joins, and reduces full native open edges from **383 to 366**. GND opens fall from **44 to 27**. The remaining 104 intrinsic footprint-clearance findings are unchanged; this is not a clean fabrication DRC result.

## Changes and checks

The [deterministic generator](../../tools/generate-ground-return-trial.py) retains all 483 component placements/pads and all 13,262 source tracks/vias. A B.Cu GND zone with 0.20 mm clearance and full pad connections first reduces opens to 370. It fills 44 polygons with 2394.471 mm² total copper. The original In2.Cu zone remains six polygons totalling 2886.218 mm².

The generator then searches for short ground connections from disconnected rear polygons or a pad's actual copper face to the **main** In2 ground region. It adds 22 tracks/vias in four routes: the PAIR02/03/04 ground cluster, PAIR05 ground, and both front-side J1 GND lands. The front J1 lands use F.Cu–In1.Cu–In2.Cu stacks; they cannot be assumed connected to a rear pour merely because their XY positions overlap it. The search uses 0.05 mm cells, 0.20 mm traces and the existing provisional 0.30/0.10 mm adjacent-layer microvias. A via transition costs eight planar steps; this is a geometric search preference, not an electrical or process optimization.

Evidence:

- [Generation manifest](../../mechanical/review/ground-return-trial.json): source/output SHA-256, native version, each disconnected pad group, seed and search counts, selected endpoints and zone areas.
- [Saved-board checker](../../tools/check-ground-return-trial.py) and [result](../../mechanical/review/ground-return-check.json): all original tracks retained; identical placements/pad assignments and all non-ground pad clusters; 22 ground-only additions; zero added-copper/foreign-shape conflicts at 0.20 mm; each claimed join reaches the actual C1 main ground cluster.
- [Full native DRC](led-ground-return-drc-2026-10-20.json): KiCad 10.0.6, exactly the baseline 104 intrinsic findings and 366 open connections. Its complete normalized finding set matches the validated source, not merely its count.
- [Native per-net report](../../mechanical/review/ground-return-open-nets.json): pad-cluster and full native counts both reconcile to 366. Leading remaining nets are +3V3_APP (46), VLED (41), +3V3_USB (32), GND (27) and +SYS_APP_IN_DRAFT (12).
- All 256 exact LED placements, rotations, pad maps and nets pass. A second complete generation is byte-identical: board SHA-256 `874798c1eccab2e89e98d961236077a4f8f1148f4a9ff93ba7171992dcbdb8bc`.

Repeat full acceptance from the repository root with `./tools/check-ground-return.sh`, using desktop access if macOS registration fails in a sandbox. It retains raw checks under the ignored coupon build directory. Extra In3/In4 ground-pour probes gave no connectivity improvement and are not included. Two direct-stack probe routes did not join the main network; those are also excluded.

## Remaining work

The 27 GND opens still include row-pair source pads, select-pulldown grounds, other passives and U48/U52/U38. Several rear islands have no 0.20 mm grid escape or 0.30 mm via site at the present placement; the manifest distinguishes zero seed cells from exhausted searches. Coordinate placement/route changes rather than assuming a plane completes them. Nine gate pullups, supply distribution and the other control nets are still open.

Full pad connections have **no soldering/thermal-relief approval**. The broad pours have no RF/antenna, switching-loop, return-current, EMI, thermal or current-capacity review. Stack-up, adjacent-layer microvias/via-in-pad, mask/paste, canonical row-pair selection and net synchronization, sensor/battery/case fit, interlock behavior and independent Gate A remain open. No hardware revision, firmware revision, bench setup or measured hardware result exists for this study. It is never fabrication source.
