<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Remaining routing: 40-open checkpoint

The zero-open goal remains **in progress**. The selected
[remaining-routing project](../../hardware/coupon/rev-a/staging/led-remaining-routing-trial-114mm.kicad_pro)
has **40 native and independently counted physical opens**, with the exact
unchanged **104 intrinsic DRC findings**. All 231 live pad groups in the immutable 43-open switch source survive.
One exact GND return is replaced under ADR 0094, retaining every original
contact and all other copper. The complete 229 pad groups and 208 additions
from the preceding 41-open checkpoint also survive,
bound explicitly in the plan. This is unbuilt Coupon Rev A CAD continuity,
with no powered hardware/firmware measurement. Fabrication remains prohibited.

[ADR 0091](../decisions/0091-zero-open-routing-study.md),
[ADR 0093](../decisions/0093-inherited-retired-copper-evidence.md),
[ADR 0094](../decisions/0094-tmp390-programming-resistor-locality.md), the
[exact plan](../../mechanical/review/remaining-routing-plan.json),
[manifest](../../mechanical/review/remaining-routing-checkpoint.json) and
[native DRC](remaining-routing-drc-2026-11-07.json) bind the checkpoint. PCB SHA:
`7a36c24652fa22d18f583b729a0e79b6641e72686cb0f42299452f30f7304bee`.
The 43-open parent stays immutable. The preceding 41-open source is recorded in commit `6d30b28`, SHA
`2341f341e992da39431d3892daefe633a905a3737cd4cd276b2ba3a329ac91f1`.
The earlier 42-open source is recorded
in commit `de46325`, SHA
`844fd52387c41f6cfbbce1790e6a564a63d3285417b020769f91088d870ba4ca`.

## Selected continuity

Both MCU-side USB paths now join: U3.14–R46.1 (USB_DP_MCU) and U3.13–R45.1
(USB_DN_MCU). The D− trial initially split APP/USB supply groups and isolated
an accepted USB-supply via. Explicit supply restoration and an actual-copper
endpoint route retained all existing live groups in that USB continuation. No pad is
invented or deleted to obtain the result.

The [TMP390 locality continuation](tmp390-locality-2026-11-07.md) additionally
joins R90.1–U39.2, keeping the 14 kΩ part and sensor position fixed.
Relative to the 43-open parent, the ledger adds 191 ordinary 0.20 mm tracks
and twenty-five 0.30/0.10 mm adjacent outer microvias. R90 moves locally and
one GND track is replaced; all other poses/copper,
source circuits/current/default-off settings and firmware stay unchanged.
No new central transition or rule relaxation occurs. Added trace centre-line lengths are
53.827927 mm for USB_DP_MCU, 45.882612 mm for USB_DN_MCU, 11.565362 mm for
+3V3_APP, 3.025000 mm for +3V3_USB, 2.385000 mm for TMP_COLD_SET and
5.770000 mm of replacement GND copper, excluding pad/via/plane travel. The
retired original GND track is 1.500000 mm.

External USB data and CC/control nets remain open. This geometry does not
establish differential pairing, impedance, skew, return quality or functional
USB operation. Supply-path current capacity, voltage drop and thermal review
remain unresolved.

## Validation and retirement evidence

- Exact copper/part/field/local-pad/net/pose/profile/outline/zone structure,
  all 231 parent groups, the complete 229-group previous checkpoint, 483
  footprints and 2,092 physical pads. Copper/net identity is rechecked after
  each refill, including detection of native net propagation.
- Three stable fills per generation, two independent byte-identical replays,
  and exact selected-board native/physical 40-open agreement.
- Exact unchanged 104 native findings on the selected board; no waiver.
- Fifteen isolated faults rejected, including actual D+/D− and APP/USB-supply
  disconnections, unsupported/smaller via, narrowing, changed converter
  default, deletion of prior switch copper, retired-via reinsertion, cold-pin
  disconnection, remote/retuned R90, old-return
  reinsertion and independent return-endpoint loss with a matching ledger.
- The source contract retains 465 common components and 1,718 logical pins.
  All 27 source-only workflow commands pass locally; results are recorded in
  the manifest without claiming remote CI success.
- Native bottom-copper views inspected at U3, both series resistors and the
  local TMP390/R89/R90 return geometry.
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
The actual source has 104 findings and 40 native/physical opens. Its single
GND retirement has its own original-contact and endpoint proof under ADR 0094.
Raw experiments and observed identities are bound in the manifest.

Raw views, searches, replay/fault logs and the rejected restoration copy stay
ignored under `build/remaining-routing/` and `build/zero-open-routing/`.
Remaining opens are inventoried by net. The named successor may grow through
validated exact ledgers; the immutable 43-open source stays available. Supplier/
stack, 557 historical centre-via, part/electrical/process/fit and independent
Gate A holds remain open.
