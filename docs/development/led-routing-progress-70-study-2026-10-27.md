<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Routing continuation: 71 to 70 unconnected edges

Date: 2026-10-27. Unbuilt, unqualified source study; no hardware measurements or fabrication release. The 50-edge target remains open.

The selected transaction grounds PAIR10.1 and reduces native/independent physical-pad opens **71 → 70**, retaining exactly **104 unchanged intrinsic DRC findings**. Every accepted 71-edge added copper item and completed physical group survives. The [71-edge plan](../../mechanical/review/routing-progress-71-checkpoint.json) freezes commit abf4f99 under ADR 0052. The two previous source replacements retain their exact geometry and contact evidence.

## Selected transaction

The third [catalog replacement](../../mechanical/review/routing-progress-track-replacements.json) is the original ROW_SEL_08 B.Cu segment (76.65, 18.70)–(81.25, 18.70) mm. It retains back-layer tails and diverts the local gap onto In1 through two chains of four adjacent microvias. Original and replacement track length both calculate to 4.6 mm; added vias and layer transitions still change electrical behavior and require review. All five direct original-layer pad/copper contacts and both original endpoints pass independent native geometric checks. The bounding box remains x = 76.65–81.25 mm, y = 18.70 mm; no broad row reroute is selected.

The ground connection uses a 0.70 mm back lead and 1.40 mm horizontal lead to (79.275, 18.650) mm, then three adjacent microvias to In2. The complete transaction adds **five tracks / eleven microvias** and replaces one original track, for a net fifteen copper items. No power-distribution bus, USB trace or source via is removed. GND opens fall **7 → 6**. All exact parts, 34 passive poses, widths, clearances, zones, power parcels, two DSF necks, current/protection settings, firmware and isolated enable boundaries remain unchanged.

The resulting board contains **483 footprints / 17,836 copper items**, retaining **15,395 nonzero original items** and adding **1,628 tracks / 813 microvias** relative to the frozen 215-edge source. There are now exactly three enumerated source-track replacements, with seventeen direct source-contact witnesses. Existing three orphan-via retirements and 116 neutral zero-length cleanups remain separately proved. Ordinary tracks/clearance are 0.20 mm, adjacent microvias 0.30/0.10 mm, annulus 0.10 mm, and only the previous two exact DSF necks are 0.12 mm.

## Validation evidence

[Full DRC](led-routing-progress-70-drc-2026-10-27.json), [native checks](../../mechanical/review/routing-progress-70-native-check-2026-10-27.json), [orphan-restoration DRC](led-routing-progress-70-orphan-restoration-drc-2026-10-27.json), [remaining-net report](../../mechanical/review/routing-progress-open-nets.json) and [validation fingerprints](../../mechanical/review/routing-progress-70-validation-2026-10-27.json) record the accepted source. Three stable fills and two byte-identical PCB/project/custom-rule replays pass. Board SHA-256: `be58a1ecd4060a5e3f8d29c040900a7ff65caacc0475b0fb36db5114f00bfedc`.

Acceptance passes **31 isolated native guards / 56 portable plan guards**, canonical source checks, **256 LED checks**, and the source-only CI layout's 21 canonical fault, 14 distance, six path and seven clearance tests. The new frozen-71 guards specifically remove an LED_SIN addition or its U1.26 join, including coordinated candidate/plan changes. The separate orphan restoration retains 70 opens/all groups and adds only the same three expected dangling-via warnings. Run `./tools/check-routing-progress.sh`. Final fingerprints record completed checks; do not infer success merely from a generated candidate.

## Rejected continuations and open gates

The two-obstruction screen samples a 0.10 mm lattice within 1.5 mm of remaining ground/supply pads and excludes power-bus, USB, via and accepted-addition retirements. It produces 87 geometric sites. Three-layer detours yield no accepted transaction. Six-layer adjacent-via search yields the PAIR10 transaction; other searched sites remain incomplete. Finite unsuccessful bounds do not prove routing impossible.

A targeted local Freerouting 2.5.0 search yields no additional control copper. A separate proposed VBUS divider branch shows 70 opens before refill but then splits an accepted +3V3_APP group and returns to 71; it is rejected. A bounded straight plane-bridge search cannot restore it. A lower pre-fill/router count never substitutes for physical-group retention and native checks. Local exchange files, binaries and unsuccessful probes remain ignored.

The [supplied Murata sheet recheck](../../hardware/coupon/rev-a/3v3-inductor-footprint-audit.md#owner-supplied-sheet-recheck-2026-10-27) confirms existing inductor lands; no local inductor move is selected. The vendor sheet stays outside Git.

The board remains unbuilt with 104 intrinsic findings. Electrical, bypass/return, switching-loop, current/thermal, timing/impedance, partial-power/interlock, RF, mechanical and HDI/assembly reviews remain open, alongside the C45 and SYS-distribution holds and trial package exceptions. Independent Gate A is required before fabrication. Neither this source commit nor its open count authorizes manufacturing.
