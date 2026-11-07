<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Zero-open routing goal: first selected continuation

The owner's zero-open goal remains **in progress**. The selected
[routing project](../../hardware/coupon/rev-a/staging/led-routing-closure-trial-114mm.kicad_pro)
has **44 native and independently counted physical open connections**, down
from the immutable ADR 0090 parent at 47. Native DRC retains the exact existing
104 intrinsic findings, with no additions. This is an unbuilt Coupon Rev A CAD
routing study, not electrical, thermal, manufacturing or hardware validation.
No firmware revision or powered test setup is involved.

[ADR 0091](../decisions/0091-zero-open-routing-study.md), the
[exact plan](../../mechanical/review/routing-closure-plan.json),
[validation manifest](../../mechanical/review/routing-closure-checkpoint.json)
and [native DRC](routing-closure-drc-2026-11-06.json) bind the geometry and evidence.
Selected PCB SHA-256:
`d961cf435d1ea8ff63454d580953edae26f16330c46768c84db3cfa88fbd41aa`.

## Selected changes

All original copper survives. Forty ordinary 0.20 mm tracks and six
0.30/0.10 mm outer-adjacent microvias are added. No new central microvia,
rule relaxation, circuit/net change or current-setting change is selected.
All 235 parent physical pad groups, all 483 footprints and all 2,092 physical
pads survive. U36/U37 and their accepted local switching/capacitor/feedback
geometry remain unchanged.

Three genuine joins close:

| Circuit | Verified pin witnesses | Added conductor length |
|---|---|---|
| USB logic timing | R77.2–U34.4 | 20.115754 mm, two outer-layer transitions at each end |
| LED current programming | R1.1–U1.1 | 4.550000 mm on B.Cu |
| E1 ILIM programming | R96.1–U44.9 | 5.147549 mm, two B.Cu–In4.Cu microvias |

Lengths are sums of added trace centre lines, excluding pad travel, via depth
and plane spreading. They are CAD geometry, not impedance or ampacity results.
The original timing route uses four adjacent outer microvias, never a central
transition.

R1's exact MPN, value, pads and nets are unchanged. Its pose moves from
(44.75,4.25) mm, 180° B.Cu to (91.75,3.25) mm, 90° B.Cu. The manufacturer's
TLC59581 layout guidance places the current-setting resistor close to IREF and
IREFGND. The new pad-centre distances to U1.1/U1.56 are 2.412986/2.592778 mm.
Three additional B.Cu ground segments total 4.35 mm and explicitly join R1.2 to
U1.56 while preserving main ground. This improves the old remote placement;
noise/current accuracy and quiet-return behaviour remain unqualified.
The exact cached vendor sheet is unchanged; no vendor content is redistributed.

The first ILIM route cut U44.8's ground connection after refill. Moving its
IC-side via from (99.35,18.80) to (99.30,18.70) mm and retaining exact land
interfaces preserves ground. The rejected version is not selected.

## Validation

- Exact native copper/pose/field/local-pad/net/project/rule/outline/zone/setup
  checks, all parent groups and all four explicit local pin witnesses.
- Three stable fills and two byte-identical deterministic replays at the SHA
  above; exact selected-source native/physical 44-open count.
- Exact unchanged 104 intrinsic DRC findings. Restoring the original three
  orphan vias preserves all live groups and adds only their same three warnings.
- Seven isolated fault cases pass: native timing/IREF/ILIM disconnections,
  remote R1, unreviewed narrowing, changed converter MODE net and deletion of
  previously accepted converter copper.
- Source-to-study component contract and portable fingerprint checks pass.
  All 23 source-only workflow commands pass locally; commands and exit statuses
  are recorded in the manifest.
- Native magnified SVG view of the moved resistor inspected. Generated views,
  rejected trials and raw replay/fault logs remain ignored in the build tree.

The reusable search now also samples legitimate overlapping round-cap contact
positions. Its native fixture proves actual pad connectivity, adjacent 0.20 mm
clearance, and loss of connectivity with a separated cap. This is search
coverage, not a new width exception or a claimed additional circuit join.

## Continuing work and rejected trials

Remaining counts and exact net names are in the manifest's `by_net` inventory.
The queue still includes ground/VLED islands, gauge supply, switch EN, row gates,
interlock controls, temperature controls, clocks and USB data. Same-net opens
must close without bridging distinct intentional permission nets. VLED and row
hardware defaults and every source/charge/LED/regulator limit stay unchanged.

Finite additive control/power searches leave many pins trapped by existing
colour and row-select copper. Five attempted catalogue-position DSF necks
collide with existing copper; they are rejected, not added to the selected
source. No general narrow routing is authorized. A small TMP390 pose screen
finds only its existing position within ±2 mm after courtyard/copper checks.
Simple same-layer and adjacent-layer colour-detour trials at the cold-threshold
escape have not preserved all contacts and clearance. No such retirement,
part move or threshold change is selected.

The search's plane-target extension treats each filled polygon separately and
requires a native connected-copper contact witness. A zone object's identity
alone cannot prove that a disconnected filled island belongs to main ground.
Exploratory plane-target results still require the normal per-join refill,
full old-group preservation, actual anchor-pad join and full DRC before selection.
A native fixture verifies that all 83 accepted main-ground polygons exclude
the four genuinely isolated same-net pads. No plane-target join is included
in this 44-open checkpoint.

The historical 557 incompatible central microvias, unconfirmed controlled
stack/thickness, power/thermal/effective-capacitance/USB/assembly/fit
qualification and independent Gate A still prohibit fabrication. Closing
remaining opens will not independently resolve those holds.

## Reproduction

Run from the repository root:

```sh
python3 tools/check-routing-closure-plan.py
python3 tools/check-coupon-study-contract.py --board hardware/coupon/rev-a/staging/led-routing-closure-trial-114mm.kicad_pcb
/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/3.9/bin/python3 tools/generate-routing-closure.py --output hardware/coupon/rev-a/build/routing-closure/replay.kicad_pcb
cmp hardware/coupon/rev-a/staging/led-routing-closure-trial-114mm.kicad_pcb hardware/coupon/rev-a/build/routing-closure/replay.kicad_pcb
/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/3.9/bin/python3 tools/check-routing-closure.py --check-orphans
/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/3.9/bin/python3 tools/test-routing-closure-guards.py
/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/3.9/bin/python3 tools/test-route-cap-contact.py
```

The exact plan is the authoritative replay; running heuristic search again is
not required to regenerate or validate this checkpoint.
