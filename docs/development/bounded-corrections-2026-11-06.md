<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Bounded converter and stack corrections — 2026-11-06

The selected [U36 routing project](../../hardware/coupon/rev-a/staging/led-u36-stage-routing-trial-114mm.kicad_pro)
now has **47 native and physical open connections**, versus 50 in its immutable
parent, and the exact unchanged **104 intrinsic package-spacing findings**.
[ADR 0090](../decisions/0090-bounded-stack-and-complete-stage-corrections.md)
records the change. This is Coupon Rev A CAD geometry and calculation, not
built-hardware measurement. Firmware and all current/protection settings are
unchanged; no hardware/firmware bench revision or test setup exists.

Selected PCB SHA-256:
`e3036ccd84dee004425115617b409ff9c770b8cd7f75a529e178154b17cf5d53`.
The [exact plan](../../mechanical/review/u36-stage-checkpoint-plan.json),
[native validation manifest](../../mechanical/review/u36-stage-checkpoint.json)
and [native DRC report](u36-stage-drc-2026-11-06.json) bind source, poses, copper,
pad witnesses, source profiles, tools and rejection cases. All 238 immediate
parent pad groups survive, retaining the previously validated 246-group
58-edge history transitively.

## What changed

The complete nine-part stage moves together. U36 is at (110.00,17.25) mm,
−90° B.Cu; L1 at (110.25,14.35) mm, 180° B.Cu. Capacitor and divider fields,
land patterns, pin numbers and nets remain identical to the parent.

| Reference | New position (mm), angle | Supply / IC-ground return centre distances (mm) |
|---|---|---|
| C40, nearest input | (112.75,17.50), −90° | 2.012 / 3.014 |
| C41, second input | (112.75,14.50), 90° | 2.351 / 5.214 |
| C43, nearest output | (108.75,20.00), 180° | 3.519 / 2.800 |
| C42, second output | (111.00,12.00), 180° | 5.256 / 5.998 |
| R81 | (108.25,17.50), −90° | Divider upper resistor; VOUT and FB joined |
| R82 | (111.25,19.75), −90° | Divider lower resistor; FB and GND joined |
| R83 | (112.75,20.00), 0° | EN pull-down joined to U36.5 and GND |

Distances are native pad-centre geometry, not path length or loop inductance.
The first input capacitor has an explicit **1.793091 mm B.Cu trace path with
no vias**. Its bank partner adds a 1.166083 mm trace-only local join.
The nearest output capacitor has an explicit **2.784939 mm trace path with
two adjacent B.Cu–In4.Cu microvias**. These are added conductor lengths
between real land interfaces, excluding travel inside pads, via vertical
length and plane spreading. The raw routing transactions and length/via
bounds are included in the exact plan. Remaining bank members contribute
distributed capacitance; do not assume identical high-frequency contribution
or a manufacturer-guaranteed combined minimum.

Both LX paths stay via-free on B.Cu, 2.452998 and 2.238170 mm. The FB and EN
additions stay on B.Cu; MODE and every local ground return join main ground.
The three genuine physical merges are R81.1 into the output rail, U36.8 into
the R81/R82 divider, and U36.5 into its R83 pull-down. R81.1's previous
isolation is an additional finding beyond the earlier two-blocker summary.

The switch's SW2.3 contact remains separate from the local EN group. This
does not finish application switch operation or the remaining 47 circuit
opens. VLED hardware permission/defaults remain unchanged.

## Exact cleanup and validation

The final delta is **9 poses, 14 retirements, 47 additions**: 42 new tracks
and five outer-adjacent microvias, with no new centre-layer microvia.
Retirements are ten tracks and four vias. Six retired tracks are the old
four LX tracks plus two obsolete supply tails. The following eight-item
cleanup removes the old pad-free feedback component (three tracks/two vias),
one SYS tail and the two obsolete output-cap B.Cu–In4.Cu vias. The ledger
records exact source UUIDs/signatures before removal; all live groups and
new joins survive cleanup.

Before removing the pad-free FB island, native ratsnest reports 48 while
independent physical-pad counting reports 47. Afterwards both report 47.
That cleanup is **not counted as an additional circuit connection**.

Validation completed:

- Exact native identity/pose/pad/net/copper/profile/outline/zone/setup checks;
  483 footprints, 2,092 physical pads and all 238 parent groups retained.
- Three stable fills and two byte-identical deterministic replays.
- Independent native/physical 47-open count and the exact unchanged 104 DRC
  findings, with no new warning/error or footprint/courtyard/connector conflict.
- All VIN, VOUT, FB, pull-down, MODE/ground and numbered LX witnesses.
- Five isolated rejection fixtures: native FB disconnection, native EN/pull-down
  disconnection, remote C40, narrowed power copper and changed MODE net.
- Restoring the three historical orphan vias preserves every live pad group and
  47 opens; DRC adds only the same three exact dangling-via warnings.
- Native B.Cu/Fab/courtyard magnified view inspected, including the capacitor
  column and USB shield holes. Source-to-study and portable fingerprints pass.
- All 21 source-only workflow commands pass locally; their commands and exit
  statuses are recorded in the validation manifest.
- The corrected-stack checker rejects the current board as required; seven
  independent stack-policy unit cases pass.

Native evidence uses KiCad 10.0.6. Raw local trials, replay/fault logs and SVG/PNG
views remain ignored under `hardware/coupon/rev-a/build/u36-stage-*`.
The selected stage, manifest and source-check entry points are project-local;
vendor PDFs and unsigned manufacturing outputs are excluded.

## Corrected stack intent and remaining blocker

The [planning stack](../../manufacturing/planning/coupon-six-layer-stack.json)
replaces the inconsistent owner proposal with a **0.80 mm target** consistent
with the existing USB4505 recommendation. Four 76 µm build-up dielectrics,
six 35 µm copper layers and a 286 µm central dielectric total 800 µm before
mask/finish. Finished tolerance, mask allowance, materials, fill/cap, reliability
and supplier approval remain unspecified. This is not a fabrication drawing.

The proposed 2+2+2 topology permits outer adjacent microvias across L1–L2,
L2–L3, L4–L5 and L5–L6. The central L3–L4 transition is a proposed
0.50/0.30 mm mechanically drilled buried via, preserving the existing
0.10 mm annular-ring and 0.30 mm mechanical-hole floors. No global clearance
or package-pad rule is relaxed.

The [current eligibility inventory](../../mechanical/review/hdi-stack-eligibility-2026-11-06.json)
still rejects **557 centre-layer microvias**, and records the comparison CAD's
historical 1.0 mm general thickness and missing controlled explicit stack.
No actual stack adoption is claimed. The original 1+4+1 scheme would instead
leave 1,670 unsupported inner-layer transitions.

A literal 557-via expansion/retyping trial on the 50-edge parent produces
56 opens, changed cluster membership at 225 pads, six reported shorts and many
other DRC findings. It is rejected. This requires a real topology/routing
redesign under a confirmed supplier build, not a change of via labels.
The isolated trial and both 0.20/0.30 mm hole variants remain ignored.

## Rejected local alternatives and qualification boundary

The first nine-part placement overlapped USB shield keepouts. The screen was
corrected to include front-side through-hole lands when checking rear courtyards.
A tighter supply/return placement then allowed routes that cut narrow ground
returns; the per-transaction pad-group guard rejected them. Ground-spine
experiments on In4 and In3 cut VBUS/application/USB-only supply planes and
were also rejected. None of those failed copper changes is present in this
selected source. Rearranging the capacitor column resolves the local geometry
without changing those planes or introducing a new ground spine.

The layout improves local geometry; 0.20 mm power copper is still a study
parameter, not an ampacity rating. Exact combined C(V,T,age), source/load and
L(I,T), ripple/stability/startup, thermal performance, VLED power-save/window
compatibility, stack/mask/stencil/HDI process, procurement and enclosure fit
remain qualification work. The prior generic GRM188 bias/aging estimates are
not promoted to guaranteed part data. The source remains an unbuilt, incomplete
routing study; independent Gate A remains mandatory.

Reproduce the selected CAD source and checks from the repository root:

```sh
/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/3.9/bin/python3 tools/generate-u36-stage-checkpoint.py --output hardware/coupon/rev-a/build/u36-stage-replay/trial.kicad_pcb
cmp hardware/coupon/rev-a/staging/led-u36-stage-routing-trial-114mm.kicad_pcb hardware/coupon/rev-a/build/u36-stage-replay/trial.kicad_pcb
python3 tools/check-u36-stage-plan.py
/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/3.9/bin/python3 tools/check-u36-stage-checkpoint.py --check-orphans
/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/3.9/bin/python3 tools/test-u36-stage-checkpoint-guards.py
python3 tools/test-hdi-stack-policy.py
/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/3.9/bin/python3 tools/check-hdi-stack.py --output hardware/coupon/rev-a/build/hdi-eligibility.json --expect-ineligible
```

The last command is a regression assertion that this routing study remains
ineligible; omitting `--expect-ineligible` returns failure. It never grants
fabrication permission. Normal source-only CI and `tools/check-routing-progress.sh`
include the new selected checkpoint while preserving all parent gates.
