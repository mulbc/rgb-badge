<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Remaining routing: 38-open checkpoint

The zero-open goal remains **in progress**. The selected
[remaining-routing project](../../hardware/coupon/rev-a/staging/led-remaining-routing-trial-114mm.kicad_pro)
has **38 native and independently counted physical opens**, with the exact
unchanged **104 intrinsic DRC findings**. All 231 live pad groups in the
immutable 43-open switch source survive, as do all 227 groups and all 219
additions of the preceding 39-open checkpoint. This is unbuilt Coupon Rev A
CAD continuity, with no powered hardware/firmware measurement. Fabrication
remains prohibited.

[ADR 0091](../decisions/0091-zero-open-routing-study.md),
[ADR 0093](../decisions/0093-inherited-retired-copper-evidence.md),
[ADR 0094](../decisions/0094-tmp390-programming-resistor-locality.md),
[ADR 0096](../decisions/0096-tmp390-output-ground-plane-study.md),
[ADR 0098](../decisions/0098-remaining-enable-test-land-locality.md) and
[ADR 0099](../decisions/0099-local-permission-lead-replacement.md) bind the
[exact plan](../../mechanical/review/remaining-routing-plan.json),
[manifest](../../mechanical/review/remaining-routing-checkpoint.json) and
[native DRC](remaining-routing-drc-2026-11-07.json).

Selected PCB SHA:
`01fb2e8a1ac781172797d369df99ff3c834016453ffeaa3d76c224b525355031`.
The immutable 43-open parent is SHA
`b847f59f8a13a63d8db7a3c2ed2e7efc37239edc03c16fe12adc8b5758b4d524`.
Earlier remaining-routing checkpoints are preserved in Git:

| Opens | Commit | PCB SHA-256 |
|---|---|---|
| 39 | `772c83a` | `aab8f44a9ec3ae65aed4ee2500d52d57d4d3872c8428b8f50c765bfedd205a1e` |
| 40 | `fb5744c` | `7a36c24652fa22d18f583b729a0e79b6641e72686cb0f42299452f30f7304bee` |
| 41 | `6d30b28` | `2341f341e992da39431d3892daefe633a905a3737cd4cd276b2ba3a329ac91f1` |
| 42 | `de46325` | `844fd52387c41f6cfbbce1790e6a564a63d3285417b020769f91088d870ba4ca` |

## Selected continuity

The [U54/TP14 continuation](permission-output-locality-2026-11-07.md) replaces
three exact USB_RAW_LOGIC_READY B.Cu tracks with a shorter ordinary-width
lead, retaining both original outer endpoints and all four external contact
shapes. TP14 moves beside U54 and joins its numbered pin 3 through a 3.125 mm
ordinary-width B.Cu lead. The former test land is independently proved
isolated and free of nonzero preceding copper. Its exact 1.0 mm land, fields,
net, layer and orientation remain unchanged; no via is added.

Earlier joins remain: MCU USB U3.14–R46.1 and U3.13–R45.1, local
R90.1–U39.2 cold programming, and U39.4–U39.6 TEMP_OK. The
[TMP390 locality record](tmp390-locality-2026-11-07.md) describes the R90 move
and exact one-track return replacement. ADR 0096's five-track ground-plane
substitution retains all five boundary contacts and both endpoint disks in
one individually filled B.Cu ground component. The sensor itself stays fixed.

Relative to the 43-open parent, the ledger adds 198 ordinary 0.20 mm tracks
and twenty-five 0.30/0.10 mm adjacent outer microvias, and retires six original
GND tracks plus the three reviewed permission tracks. R90 and TP14 are the
only changed poses. Every other part/copper item and every captured net,
current/protection/default-disabled setting remains unchanged. No new central
transition, width exception or rule relaxation occurs.

The new permission lead calculates to 2.471699 mm, replacing 2.912742 mm.
Previously recorded added trace lengths remain 53.827927 mm USB_DP_MCU,
45.882612 mm USB_DN_MCU, 11.565362 mm +3V3_APP, 3.025000 mm +3V3_USB,
2.385000 mm TMP_COLD_SET, 2.330000 mm TEMP_OK and 5.770000 mm replacement
GND, excluding pad/via/plane travel. External USB data and CC/control nets
remain open. Geometry does not establish differential pairing, impedance,
skew, return quality, current capacity, voltage drop or functional operation.

## Validation and retirement evidence

- Exact part/field/local-pad/net/pose/profile/outline/zone and copper ledgers;
  483 footprints, 2,092 physical pads, all 231 parent groups and all 227 prior
  groups. Copper/net identity is rechecked after every refill.
- Three stable fills per generation and two independent byte-identical
  replays, matching the selected source and its 38 native/physical opens.
- Exact unchanged 104 native findings, with no waiver.
- Twenty-five isolated faults rejected. Seven new cases include actual TP14
  and permission-net disconnections, old permission-lead reinsertion, lost
  outer endpoint with a matching ledger, remote TP14, omitted boundary
  contact with otherwise matching copper, and injected old-site copper
  contact with a matching ledger. Endpoint/contact guards are reached
  independently of fingerprint mismatches.
- The source contract retains 465 common components and 1,718 logical pins;
  all 27 source-only workflow commands pass locally. No remote CI success is
  inferred. The native actual-copper endpoint fixture remains passed.
- Native B.Cu U54 permission/probe geometry inspected. The TI NAND pin table
  and unchanged DCU land drawing were rendered and visually rechecked.

The strict original three-via retirement proof is rerun on the **immutable
43-open parent**, preserving its groups, native count and exact original
warnings. Reinstating those vias into the selected source remains a separate
**rejected counterfactual**: refill reassigns the injected APP via at
(45.25,8.75) mm to USB_DN_MCU. Its 107 findings include two APP warnings and
one USB warning, not the same three original warnings. The actual source has
104 findings. Current GND and permission-track replacements have their own
explicit original-contact and endpoint evidence under ADRs 0094/0096/0099.

The [open-group inventory](../../mechanical/review/remaining-open-pad-groups.json)
records 38 opens across 28 nets with actual numbered pad memberships.
[Historical follow-up screens](remaining-routing-followup-2026-11-07.md)
include the unsuccessful fixed-copper test-land attempts; the coordinated
ADR 0099 change is the later selected result. Raw views, searches, replays,
fault logs and rejected boards remain ignored under the build directories.
Supplier/stack, 557 historical centre-via, electrical/thermal/process/fit,
probe access and independent Gate A holds remain open.
