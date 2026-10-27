<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Routing continuation: 76 to 71 unconnected edges

Date: 2026-10-27. Status: unbuilt, unqualified source study; no hardware measurements or fabrication release. The 50-edge target remains open.

Native and independently counted physical-pad opens decrease **76 → 71**, with exactly **104 unchanged intrinsic DRC findings**. The selected transactions move R2 near U3 and complete LED_SIN through U1, join U31.2 on USB_CC2 with a verified ground restoration, and ground U38.2 and R31.2 through two enumerated local track replacements. Every previously completed physical pad group, every prior checkpoint's added copper, original zone definition, power parcel and exact DSF neck survives. Two original source tracks are replaced under [ADR 0053](../decisions/0053-enumerated-local-track-replacements.md); preservation claims therefore explicitly exclude these signatures rather than claiming that every original track remains.

## Exact changes

R2 moves from (62.250, 5.750) mm to (13.705, 30.795) mm, retaining 180° orientation, exact 100 kΩ value, MPN and pad/net data. Its LED_SIN pad joins U3.19, then the U1.26 inward escape completes the net. The source plan now records 34 passive poses; no IC, connector, inductor or row pair moves.

The USB_CC2 transaction confines horizontal In4 routing near U31 to avoid splitting application supply. A 1 mm In4 ground bridge with back-layer leads and adjacent microvias preserves the PAIR15 ground group. This is connectivity evidence, without USB/ESD/return qualification.

| Escape | Exact replaced source | Original → replacement track length, calculated | Original direct contacts checked |
|---|---|---:|---:|
| U38.2 GND | COL_09_R, In4, (82.6, 3.25) to (60.9, 3.25) mm | 21.7 → 22.9 mm | 2 |
| R31.2 GND | ROW_SEL_08, B, (51.4, 7.85) to (53.3, 7.85) mm | 1.9 → 2.6 mm | 10 |

The [exact catalog](../../mechanical/review/routing-progress-track-replacements.json) pins the two originals, all replacement and new-connection geometry, and all twelve original same-net pad/copper contacts. The first retains straight In4 tails and uses a local In3 bridge. The second retains a bounded back-layer detour. Independent native geometry checks require original endpoints and every direct interior junction to contact replacement copper on the original layer; a transitive net connection alone is insufficient. No source via, power-distribution track, USB track or third ordinary source track retires.

The board contains **483 footprints / 17,821 copper items**. Relative to the frozen 215-edge parent it retains **15,396 nonzero source items**, adds **1,623 tracks / 802 adjacent microvias**, replaces the two catalog tracks and retains the existing three orphan-via retirements and 116 neutral zero-length cleanups. Ordinary tracks/clearance remain 0.20 mm; the two previous 0.12 mm DSF necks, 0.30/0.10 mm microvias and 0.10 mm annulus remain unchanged. Parts, current/protection settings, firmware and fail-safe enable boundaries are unchanged.

## Validation

[Full DRC](led-routing-progress-71-drc-2026-10-27.json), [native checks](../../mechanical/review/routing-progress-71-native-check-2026-10-27.json), [orphan-restoration DRC](led-routing-progress-71-orphan-restoration-drc-2026-10-27.json), [remaining-net counts](../../mechanical/review/routing-progress-open-nets.json) and [validation fingerprints](../../mechanical/review/routing-progress-71-validation-2026-10-27.json) record the result. Three stable refills and two byte-identical PCB/project/rule replays pass. PCB SHA-256: `52f0bdba85a694bef00f36dbe01c3483876942a20cf732d51161800d2dcef2b8`.

The wrapper passes **30 isolated native guards**, canonical metadata checks and **256 LED checks**. The separate restored-orphan witness retains 71 opens/all groups and adds precisely the three expected dangling-via findings. Source-only CI passes **53 portable plan guards**, **21 canonical-source fault methods**, 14 distance tests, six path tests and seven clearance tests. New guards reject coordinated retirement of accepted 76-edge additions, undeclared original replacement/restoration, omitted catalog geometry/junction metadata, and missing original endpoint/interior contact evidence even with coordinated metadata edits. Run `./tools/check-routing-progress.sh`.

The [76-edge checkpoint](../../mechanical/review/routing-progress-76-checkpoint.json) freezes commit 42e16a1's integer plan. Its [historical remaining-net report](../../mechanical/review/routing-progress-76-open-nets-2026-10-27.json) preserves the previous count; old validation fingerprints describe the files at that commit.

## Further experiments and unresolved work

Repeated bounded original-width control searches, isolated passive moves and joint feedback placement searches produced no additional selected joins. A local Freerouting 2.5.0 experiment holds all existing copper fixed; its exchange-format count differs substantially from KiCad physical-pad connectivity. Tiny proposed stitches on already joined nets do not reduce native opens and are excluded. No router executable, exchange files or downloaded material is committed.

The owner-supplied Murata DFE252012P sheet lists both exact inductors and matches the footprint's recommended land geometry. [ADR 0054](../decisions/0054-local-converter-inductor-placement-study.md) permits ignored local-placement feasibility studies only. A 0.25 mm lattice within 5 mm of each fixed converter, at four orientations, finds no pose satisfying existing copper/pad clearance and back-courtyard separation. No inductor move or long switching-node route is selected; these finite bounds do not prove placement impossible. The supplied sheet's PDF metadata dates to 2016-04-22; it has no visible revision identifier. Local input SHA-256 is `ce259ba611fb3ea196baf60e2c7080a21cd897cdb662bf77552cc842c2b91c3e`. The vendor PDF stays outside the repository.

All remaining electrical, bypass/return, switching-loop, feedback, current/thermal, USB/display timing, RF, mechanical and HDI/assembly reviews remain open, alongside the C45 and SYS-distribution holds. Sixteen trial row pairs and two netless driver projections remain unqualified canonical exceptions. Independent Gate A is required before fabrication. A lower open count and unchanged intrinsic findings are source evidence, not a working-board claim.
