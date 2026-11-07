<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Remaining routing: 41-open checkpoint

The zero-open goal remains **in progress**. The selected
[remaining-routing project](../../hardware/coupon/rev-a/staging/led-remaining-routing-trial-114mm.kicad_pro)
has **41 native and independently counted physical opens**, with the exact
unchanged **104 intrinsic DRC findings**. Every copper item and all 231 live
pad groups in the immutable 43-open switch source survive. The complete 230
pad groups and 83 additions from the preceding 42-open checkpoint also survive,
bound explicitly in the plan. This is unbuilt Coupon Rev A CAD continuity,
with no powered hardware/firmware measurement. Fabrication remains prohibited.

[ADR 0091](../decisions/0091-zero-open-routing-study.md),
[ADR 0093](../decisions/0093-inherited-retired-copper-evidence.md), the
[exact plan](../../mechanical/review/remaining-routing-plan.json),
[manifest](../../mechanical/review/remaining-routing-checkpoint.json) and
[native DRC](remaining-routing-drc-2026-11-07.json) bind the checkpoint. PCB SHA:
`2341f341e992da39431d3892daefe633a905a3737cd4cd276b2ba3a329ac91f1`.
The 43-open parent stays immutable. The preceding 42-open source is recorded
in commit `de46325`, SHA
`844fd52387c41f6cfbbce1790e6a564a63d3285417b020769f91088d870ba4ca`.

## Selected continuity

Both MCU-side USB paths now join: U3.14–R46.1 (USB_DP_MCU) and U3.13–R45.1
(USB_DN_MCU). The D− trial initially split APP/USB supply groups and isolated
an accepted USB-supply via. Explicit supply restoration and an actual-copper
endpoint route retain all existing live groups and original copper. No pad is
invented or deleted to obtain the result.

Relative to the 43-open parent, the ledger adds 183 ordinary 0.20 mm tracks
and twenty-five 0.30/0.10 mm adjacent outer microvias. No part moves, existing
copper retirement, new central transition, rule relaxation, circuit/net/current/
default-off or firmware changes occur. Added trace centre-line lengths are
53.827927 mm for USB_DP_MCU, 45.882612 mm for USB_DN_MCU, 11.565362 mm for
+3V3_APP and 3.025000 mm for +3V3_USB, excluding pad/via/plane travel.

External USB data and CC/control nets remain open. This geometry does not
establish differential pairing, impedance, skew, return quality or functional
USB operation. Supply-path current capacity, voltage drop and thermal review
remain unresolved.

## Validation and retirement evidence

- Exact copper/part/field/local-pad/net/pose/profile/outline/zone structure,
  all 231 parent groups, the complete 230-group previous checkpoint, 483
  footprints and 2,092 physical pads. Copper/net identity is rechecked after
  each refill, including detection of native net propagation.
- Three stable fills per generation, two independent byte-identical replays,
  and exact selected-board native/physical 41-open agreement.
- Exact unchanged 104 native findings on the selected board; no waiver.
- Ten isolated faults rejected, including actual D+/D− and APP/USB-supply
  disconnections, unsupported/smaller via, narrowing, changed converter
  default, deletion of prior switch copper and retired-via reinsertion.
- The source contract retains 465 common components and 1,718 logical pins.
  All 27 source-only workflow commands pass locally; results are recorded in
  the manifest without claiming remote CI success.
- Native bottom-copper views inspected at U3 and both series resistors.
  A native fixture proves that routing from an actual retained orphan-copper
  UUID changes native opens from one to zero with the same one pad and every
  original copper item; ordinary pad-only search leaves it untouched.

The strict original three-via retirement proof is rerun on the **immutable
43-open parent**, preserving its live groups, native count and exact three
original warnings. The manifest explicitly names this inherited basis.
Reinstating those retired vias into the current board is a separate **rejected
counterfactual**: refill reassigns the injected APP via at (45.25,8.75) mm to
USB_DN_MCU where the new route uses freed space. Its 107 findings include two
APP warnings and one USB warning, rather than the same three original warnings.
A local detour preserved actual connectivity but isolated that reinserted via.
Neither trial is selected or presented as the strict current-board proof.
The actual source has 104 findings, 41 native/physical opens and no additional
retirements. Raw experiments and observed identities are bound in the manifest.

Raw views, searches, replay/fault logs and the rejected restoration copy stay
ignored under `build/remaining-routing/` and `build/zero-open-routing/`.
Remaining opens are inventoried by net. The named successor may grow through
validated exact ledgers; the immutable 43-open source stays available. Supplier/
stack, 557 historical centre-via, part/electrical/process/fit and independent
Gate A holds remain open.
