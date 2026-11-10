<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

**Current checkpoint, 2026-11-10: 35 opens.** The [R11 ground-join record](r11-ground-join-2026-11-10.md) supersedes the earlier counts below, with all old groups and accepted additions retained. Zero-open and qualification work remain ongoing.

# Remaining routing: 36-open checkpoint

The zero-open goal remains **in progress**. The selected
[remaining-routing project](../../hardware/coupon/rev-a/staging/led-remaining-routing-trial-114mm.kicad_pro)
has **36 native and independently counted physical opens**, with the exact
unchanged **104 intrinsic DRC findings**. All 231 live pad groups in the
immutable 43-open switch source survive, as do all 225 groups and all 226
additions of the preceding 37-open checkpoint. This is unbuilt Coupon Rev A
CAD continuity, with no powered hardware/firmware measurement. Fabrication
remains prohibited.

[ADR 0091](../decisions/0091-zero-open-routing-study.md),
[ADR 0093](../decisions/0093-inherited-retired-copper-evidence.md),
[ADR 0094](../decisions/0094-tmp390-programming-resistor-locality.md),
[ADR 0096](../decisions/0096-tmp390-output-ground-plane-study.md),
[ADR 0098](../decisions/0098-remaining-enable-test-land-locality.md),
[ADR 0099](../decisions/0099-local-permission-lead-replacement.md),
[ADR 0101](../decisions/0101-native-pad-centre-escape-for-tp13.md) and
[ADR 0105](../decisions/0105-c32-contact-preserving-microplacement.md) bind the
[exact plan](../../mechanical/review/remaining-routing-plan.json),
[manifest](../../mechanical/review/remaining-routing-checkpoint.json) and
[native DRC](remaining-routing-drc-2026-11-07.json).

Selected PCB SHA:
`a24e9220226b77411ae8e8baea5cd629ce0fea8a97c377a708510d6791c2e439`.
The immutable 43-open parent is SHA
`b847f59f8a13a63d8db7a3c2ed2e7efc37239edc03c16fe12adc8b5758b4d524`.
Earlier remaining-routing checkpoints are preserved in Git:

| Opens | Commit | PCB SHA-256 |
|---|---|---|
| 37 | `e17fa35` | `ed6d3ff570f2481b47423d8375d9d4a40d756145cdd49e2c222bacc36edbfa57` |
| 38 | `d6a36e8` | `01fb2e8a1ac781172797d369df99ff3c834016453ffeaa3d76c224b525355031` |
| 39 | `772c83a` | `aab8f44a9ec3ae65aed4ee2500d52d57d4d3872c8428b8f50c765bfedd205a1e` |
| 40 | `fb5744c` | `7a36c24652fa22d18f583b729a0e79b6641e72686cb0f42299452f30f7304bee` |
| 41 | `6d30b28` | `2341f341e992da39431d3892daefe633a905a3737cd4cd276b2ba3a329ac91f1` |
| 42 | `de46325` | `844fd52387c41f6cfbbce1790e6a564a63d3285417b020769f91088d870ba4ca` |

## Selected continuity

The [C32 continuation](c32-microplacement-2026-11-09.md) shifts the exact
GRM188R60J106ME47D capacitor upward by 0.250 mm, retaining its original
supply contact and opening a filled B.Cu ground corridor. C32.2 joins the
main ground group without added or retired copper. The historical contact
inventory and an individual filled-component witness are independently
checked; all preceding groups and copper survive.

The earlier [native TP13 continuation](native-tp13-escape-2026-11-07.md) joins U55.7
through an exact pad-centre escape and 3.857541 mm ordinary In4.Cu lead,
with two adjacent 0.30/0.10 mm microvias and the unchanged relocated 1.0 mm
probe land. Every preceding copper item survives this additive step. The
exact (26.250,20.875) mm capture avoids rounding onto neighbouring pin
clearances; no general grid-search change is claimed.

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

Relative to the 43-open parent, the ledger adds 199 ordinary 0.20 mm tracks
and twenty-seven 0.30/0.10 mm adjacent outer microvias, and retires six original
GND tracks plus the three reviewed permission tracks. R90, TP14, TP13 and C32 are the
only changed poses. Every other part/copper item and every captured net,
current/protection/default-disabled setting remains unchanged. No new central
transition, width exception or rule relaxation occurs.

The new VLED_ENABLE_CANDIDATE lead calculates to 3.857541 mm.
The permission lead calculates to 2.471699 mm, replacing 2.912742 mm.
Previously recorded added trace lengths remain 53.827927 mm USB_DP_MCU,
45.882612 mm USB_DN_MCU, 11.565362 mm +3V3_APP, 3.025000 mm +3V3_USB,
2.385000 mm TMP_COLD_SET, 2.330000 mm TEMP_OK and 5.770000 mm replacement
GND, excluding pad/via/plane travel. External USB data and CC/control nets
remain open. Geometry does not establish differential pairing, impedance,
skew, return quality, current capacity, voltage drop or functional operation.

## Validation and retirement evidence

- Exact part/field/local-pad/net/pose/profile/outline/zone and copper ledgers;
  483 footprints, 2,092 physical pads, all 231 parent groups and all 225 prior
  groups. Copper/net identity is rechecked after every refill.
- Three stable fills per generation and two independent byte-identical
  replays, matching the selected source and its 36 native/physical opens.
- Exact unchanged 104 native findings, with no waiver.
- Thirty-six isolated faults rejected. ADR 0099 cases include actual TP14
  and permission-net disconnections, old permission-lead reinsertion, lost
  outer endpoint with a matching ledger, remote TP14, omitted boundary
  contact with otherwise matching copper, and injected old-site copper
  contact with a matching ledger. Endpoint/contact guards are reached
  independently of fingerprint mismatches. Five ADR 0101 cases additionally
  cover actual TP13 disconnection, rounded capture with a matching ledger,
  old-site contact with a matching ledger, remote TP13 and forged historical
  isolation. TP14 isolation is bound to the 39-open source; TP13 to the
  38-open source, independently of the advancing latest checkpoint. Six new
  C32 cases cover actual ground disconnection with a matching pose ledger,
  omitted contact data, excess displacement, forged historical source,
  omitted contact guard and silent packaging substitution.
- The source contract retains 465 common components and 1,718 logical pins;
  all 27 source-only workflow commands pass locally. No remote CI success is
  inferred. The native actual-copper endpoint fixture remains passed.
- Native before/after B.Cu C32 ground/supply geometry inspected; the
  calculated corridor respects the unchanged 0.250 mm zone minimum thickness.
  Earlier native B.Cu U54 permission/probe geometry and separate B.Cu/In4.Cu U55/TP13
  captures inspected. The exact TI NAND/AND pin tables and unchanged DCU land
  drawings were rendered and visually rechecked.

The strict original three-via retirement proof is rerun on the **immutable
43-open parent**, preserving its groups, native count and exact original
warnings. Reinstating those vias into the selected source remains a separate
**rejected counterfactual**: refill reassigns the injected APP via at
(45.25,8.75) mm to USB_DN_MCU. Its 107 findings include two APP warnings and
one USB warning, not the same three original warnings. The actual source has
104 findings. Current GND and permission-track replacements have their own
explicit original-contact and endpoint evidence under ADRs 0094/0096/0099.

The [open-group inventory](../../mechanical/review/remaining-open-pad-groups.json)
records 36 opens across 27 nets with actual numbered pad memberships.
[Historical follow-up screens](remaining-routing-followup-2026-11-07.md)
include the unsuccessful fixed-copper test-land attempts; the coordinated
ADR 0099 change is the later selected result. Raw views, searches, replays,
fault logs and rejected boards remain ignored under the build directories.
Supplier/stack, 557 historical centre-via, electrical/thermal/process/fit,
probe access and independent Gate A holds remain open.

The [2026-11-09 bounded follow-up](remaining-routing-followup-2026-11-09.md)
records exact-capture, ground, anchored-R8 and coordinated supply-restoration
trials on the historical 37-open basis. None is selected. ADR 0105 separately
selects the later C32-only 36-open successor; all qualification holds remain.
