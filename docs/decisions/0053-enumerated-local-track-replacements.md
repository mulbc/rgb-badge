<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0053: Enumerated local track replacements for blocked escapes

Date: 2026-10-27
Status: Accepted for the unqualified 69-edge continuation; exactly five catalog replacements selected.

## Context

The accepted 76-edge study and additive continuation preserve all previous copper. Original display and row-control tracks can surround an unconnected pin on the back and adjacent inner layers. Repeated original-width searches and audited passive moves cannot escape every such enclosure. ADR 0048 permits bounded display detours, but ADR 0052 subsequently prohibits additional retirement. This decision permits a narrowly verified exception to that exact-copper freeze while retaining its electrical connectivity requirements.

## Decision

Investigate explicitly enumerated replacements of straight 0.20 mm `COL_*` or `ROW_*` tracks obstructing a ground/supply or low-speed control-pin escape. Keep the original endpoints and every intermediate same-net pad, via, endpoint and crossing junction connected on its original layer. Prefer unchanged straight tails and a short adjacent-layer bridge around the obstruction. Retain the source signature, affected gap, exact replacement signatures, junction inventory and calculated length/layer changes. Keep all other copper unchanged. Do not remove source vias, power-distribution tracks or USB differential tracks, or alter any component, pin map, net, zone, current setting, protection or enable boundary. Existing independently verified R/C moves remain allowed under ADR 0045.

Tracks remain 0.20 mm except the existing exact ADR 0051 neck policy; clearance remains 0.20 mm, adjacent microvias 0.30/0.10 mm and annular floor 0.10 mm. A local replacement may not become a broad display reroute. Keep the added detour within a documented local bounding box and record each source segment and straight tail, including a longer source segment when only its small central gap is diverted.

## Selection gate

Experiments stay ignored until a complete replacement-and-new-connection transaction passes all of the following:

- Every previously completed physical pad group, including the accepted 76-edge USB groups, survives three stable refills.
- Native and independent physical-pad opens decrease, and full native DRC retains exactly the same 104 intrinsic findings.
- An independent checker verifies an exact reviewed replacement catalog, source signatures, original-layer endpoint/interior junction contacts, replacement dimensions, all other copper and original zone definitions. Undeclared removal, coordinated plan/candidate retirement, original restoration and omitted junctions must fail fault guards.
- Deterministic replay, exact manifest fingerprints, the existing separate orphan-via restoration proof, canonical component metadata and all LED/source checks pass.

Selection is limited to the two signatures recorded below; every other frozen-checkpoint constraint remains in force.

## Limits

This is an unbuilt routing study. A completed physical group does not qualify return impedance, current capacity, transient behavior, differential routing, switching loops, timing, thermal or HDI/assembly quality. No current limit increases or fabrication release are authorized. Independent Gate A and all existing electrical, package-adoption and enclosure holds remain required.

## Selected 71-edge continuation

The [catalog](../../mechanical/review/routing-progress-track-replacements.json), SHA-256 `0db842ca826c7f567448e4dbff3d6ec2e84eaecf7cc692568b63431f63845acf`, selects only the COL_09_R In4 segment (82.6, 3.25)–(60.9, 3.25) mm and ROW_SEL_08 B segment (51.4, 7.85)–(53.3, 7.85) mm. Calculated replacement track lengths are 22.9 versus 21.7 mm and 2.6 versus 1.9 mm. They permit U38.2 and R31.2 ground escapes. Exact catalog geometry and twelve original direct same-net contacts are checked independently, including contacts inside the source segment. Original endpoints and those contacts must touch replacement copper on their original layer.

The [71-edge evidence](../development/led-routing-progress-71-study-2026-10-27.md) records unchanged 104 intrinsic findings, three stable refills, two identical replays, 30 native/53 portable guards, canonical/LED checks and separate orphan restoration. Every prior physical pad group and checkpoint's added copper survives; every other original nonzero copper item is retained subject to the existing three orphan-via exception. The accepted 76-edge plan at 42e16a1 is frozen independently. Only these two original source signatures are exempted from ADR 0052's exact-copper freeze. No additional inductor move or narrow route is selected.

## 70-edge candidate selection gate

A further exact source ROW_SEL_08 B segment, (76.65, 18.70)–(81.25, 18.70) mm, can be replaced locally to ground PAIR10.1. Its original-layer endpoint and direct-contact proof passes in an ignored 70-edge candidate with unchanged full DRC. Extend the catalog only to this third signature, protect all accepted 71-edge additions/groups with a frozen checkpoint, and require the complete replay/native/fault/source gate before accepting this continuation. No other copper or geometry exception is permitted.

The 70-edge continuation passes three stable refills, byte-identical replays, 31 native/56 portable guards, full unchanged DRC and independent physical-pad counts, canonical/LED and separate orphan-restoration checks. Its selected catalog SHA-256 is `3b9403539212c786e301e82df479b64daf5ea8c3e8fd2c61e33a9fcacf49a24b`. The new 4.6 mm replacement preserves five direct contacts, bringing the total to seventeen. See [70-edge evidence](../development/led-routing-progress-70-study-2026-10-27.md). Exactly the third signature above is selected; all other freezes remain in force.

## 69-edge candidate selection gate

The TH1.2 ground transaction requires exactly two further original tracks: ROW_GATE_09 on In2, (54.2, 12.6)–(54.2, 19.9) mm, and ROW_SEL_05 on In4, (53.35, 15.75)–(55.15, 15.75) mm. The ignored 69-edge candidate preserves their four/two direct contacts and endpoints, all earlier groups and the full intrinsic DRC. Calculated replacement track lengths are 7.5 versus 7.3 mm and 7.4 versus 1.8 mm; layer/via changes remain timing/return review items. Pin only these two additional catalog entries, freeze the accepted 70-edge plan, and require full stable replay/native/fault/source proof before selection. No power bus, source via, package/current/enable boundary changes are authorized.

The selected 69-edge continuation passes full unchanged DRC, independent pad counts, three stable fills, two byte-identical replays, 31 native/59 portable guards, canonical/LED checks and separate orphan restoration. Catalog SHA-256: `917746d45be4c9387b766c87fa1cc31a27b1476b4aca3f10e3d988d2e4edf4c4`. All five replacements preserve 23 direct source contacts. See [69-edge evidence](../development/led-routing-progress-69-study-2026-10-27.md). Only the two extra signatures above are selected; all 70-edge additions/groups remain frozen and all other source copper remains protected.
