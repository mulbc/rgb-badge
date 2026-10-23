<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Reserve a local ground escape and screen exact grid geometry

Status: **unbuilt noncanonical routing study; fabrication prohibited**.

The subsequent [R36 continuation](led-r36-ground-study-2026-10-23.md) resolves the previously rejected branch cleanup and leaves **216 opens / 23 GND opens / 104 intrinsic findings**. The R2 and probe sections below retain their historical 217-open checkpoint.

## R2 driver-control ground

R2 (`ERJ2RKF1003X`, 100 kΩ ±1%) pulls LED_SIN low; pad 2 at
**(61.75, 5.75) mm** now connects to the existing In2 ground group through a
rear lead to **(61.55, 6.20) mm** and three adjacent B–In4–In3–In2 microvias.
Native and physical-pad opens decrease **218 → 217**, GND **25 → 24**.
All previous pad groups, including R28/R29 and every colour-column group, survive.

The original COL_07_R In4 segment from **(81.4, 6.05) to (56.45, 6.05) mm**
blocks the ground stack. Inline In4/In3 signal transitions are themselves
blocked by ROW_02_A on In3. The selected replacement retains outer In4 stubs,
uses short In4 offsets from y = 6.05 to 6.30 mm at x = **62.1 and 60.2 mm**,
and two adjacent In4/In3 signal microvias. Its In3 detour runs through
**(62.1, 6.30), (62.1, 6.70), (60.2, 6.70), (60.2, 6.30) mm**.
The complete increment adds eight tracks/five microvias and removes that single
original colour track. The prior row-select exception is unchanged: **14,492
of 14,494 original items remain exact**, with two explicitly reviewed removals.

Generator and independent checker pin both original removals separately and
hash all added GND, ROW_SEL_04, COL_07_R and supply-repair geometry. No other
source removal or restoration of either obstructing source track is permitted.
Cumulative plan: **934 tracks / 77 microvias**, seventeen joins and **15,503
items**. Full native DRC retains exactly the same 104 intrinsic findings;
28 isolated guard cases, 256 LED checks, fresh 21-case canonical comparison
and source-only CI pass. Two generations are byte-identical. New faults detach
only R2's ground stack while proving R28/R29 remain joined, detach the colour
replacement without changing counts, and restore its obstructing original track.

Bounded same-layer/inline probes for R2 and inline/offset probes for R36/R86
find no accepted route. These local failures do not prove other routes impossible.
R36/R86 remain unchanged. Sources rechecked: TI TLC59581 SLVSCZ9A pin tables
(OUTR7 pin 33, SIN pin 26), Everlight EAST10105RGBA0 DSE-0014497 and QT Brightek
QBLP1515A-RGB2A version 1.0. Existing component/pad/footprint contracts are retained;
PDFs are excluded from Git. R1's IREF network and every current setting are unchanged.

This is existing-net routing, with no material circuit decision, exact-part,
firmware, pad/net, placement, current-limit or isolated enable-boundary change.
There are no hardware measurements. Returns, impedance, signal integrity,
HDI/process/fit, the 217 remaining opens and 104 intrinsic findings still need
engineering work and independent Gate A. Fabrication remains prohibited.
[Increment evidence](../../mechanical/review/native-control-r2-ground-escape-2026-10-23.json).
Current PCB SHA-256: `a1f742cd395079eb8360483a912c69890bd4f5f2ebbf17201bbd5ddf74f23f98`.

The following R29/R28 sections are historical checkpoints. Their linked rolling
reports now describe the 217-open R2 continuation above.


## Further ground probes after R2

The accepted R2 board remains **217 opens / 24 GND opens / 104 intrinsic
findings**. Its pushed commit `b85cf46` passes all ten GitHub checks.
An exact native B.Cu A* probe enumerates 84 nearby source/main-ground pad pairs
and searches eighteen endpoint-clear pairs on a 0.05 mm grid, with a 2.5 mm
per-axis bounding margin and 8 mm maximum pair distance. All eighteen searches
exhaust, totaling 4,426 expansions; no copper is accepted.

R36 asymmetric In3 and fixed-transition In1 detours find no clear candidate.
A bounded In3/In1 search using adjacent microvia stacks across In2, with no
planar In2 signal steps, exhausts at 1,216 nodes. In3 segments are blocked by
ROW_03_A/ROW_GATE_01 even where both endpoint vias are clear.

A broader local six-layer COL_06_G replacement reaches U1.31 in 381,583
expansions, retaining prior pad groups and giving **216 opens**, but full DRC
adds one dangling original In3/In4 via at (61.9, 7.25) mm (**105 findings**).
Removing exactly that obsolete via preserves all pad groups but exposes the
old 0.95 mm In3 track end, still **105 findings**. Both candidates are rejected;
none of their tracks, vias or original-source removals enter the replay plan.
The reversed global search reaches its 400,001-node bound without a route.
A future proposal would need exact obsolete-branch cleanup and complete native
acceptance; these bounded failures do not prove other routes impossible.

[Follow-up search, rejection and GitHub evidence](../../mechanical/review/native-ground-followup-2026-10-23.json).
No hardware was measured, no rule/current limit or firmware changed, and Gate A
remains open. All local candidate copper remains excluded from Git.

## R29 extension

The preceding continuation extends the reserved row-select detour to ground R29.2
at **(44.25, 7.25) mm** while retaining R28 and every previous physical pad group.
Native/physical-pad opens decrease **219 → 218**, and GND **26 → 25**. A
same-layer extension has no native-clear candidate in the bounded probe. The
selected In3 route runs through **(40.5, 7.25), (40.5, 7.75), (44.8, 7.75),
(44.8, 7.25) mm**, with two adjacent In4/In3 signal microvias at its ends.
Three B–In4–In3–In2 microvias at R29.2 connect its ground pad without a rear lead.

Four previously added row-select track signatures are superseded by four new
ones; the left outer stub is geometrically identical. No additional original
source item is removed: the exact one-segment source exception and 14,493 retained
original items are unchanged. The plan/checker update their exact row/GND copper
hashes. The cumulative plan has **926 tracks / 72 microvias**, one original
removal, sixteen joins and **15,491 items**. Full DRC retains exactly 104 findings,
all **25 native guards**, 256 LED checks and fresh 21-case canonical comparison
pass; replay is byte-identical. The new fault case withdraws only R29's three
GND vias, proves R28 still connected, and requires rejection.

No current, exact part, pad/net, firmware or isolated display-enable boundary is
changed. Return/impedance/loop/HDI/process/fit qualification and Gate A remain open.
[Extension evidence](../../mechanical/review/native-control-r29-ground-escape-2026-10-23.json).
R29 checkpoint PCB SHA-256: `c90db60ca8cec219eeb5379766f537083a829c7c3ba6e404a13a1870ddd9c5b0`.

The following sections record the preceding **219-open R28 checkpoint**. Their
exact identities remain in its increment record; linked rolling native reports
now describe the 218-open extension above.


The [saved derivative](../../hardware/coupon/rev-a/staging/led-native-control-trial-114mm.kicad_pcb)
connects R28 pad 2 to the existing main In2 GND region, reducing native/physical-pad
opens **220 → 219** and GND **27 → 26**. No board or return impedance was measured.
All 483 footprints, pad assignments, component identities and previous physical
pad groups survive. VLED/application 3.3 V/USB logic remain at 14/7/4 opens.

## Find and remove the actual obstruction

A read-only audit of the 220-open source checks 31 unjoined rear GND pads against
0.05 mm candidate sites within ±1 mm in each axis. Twelve pads have clear rear
leads, but none has a clear B–In4–In3–In2 stack into the main ground polygon.
The retained audit lists the least-obstructed sites and exact blocking source
UUIDs/nets/layers/segments. This is a bounded short-lead screen, not a proof that
other placements, paths or return structures are impossible.

For R28.2 at (41.75, 7.25) mm, the via site (41.85, 7.20) mm is blocked by exactly
one ROW_SEL_04 track on In4 from (38.6, 7.25) to (54.0, 7.25) mm. The selected
replacement retains the two outer stubs and detours the middle through
**(40.5, 7.25), (40.5, 6.25), (42.3, 6.25), (42.3, 7.25) mm**, all on In4.
A short rear lead plus three adjacent-layer microvias joins R28.2 to ground.
A separate In3 detour also passed the geometric screen/full DRC but needed two
more signal microvias; it is not selected.

This deliberately replaces **one** source track; it does not claim to preserve
all source copper. The remaining **14,493** frozen row-13 items remain exact.
The generator and independent checker pin the removed segment independently,
require five exact replacement tracks and four exact GND items by integer
signatures/hashes, and reject every other source removal or restoration of the
obstructing segment. ROW_SEL_04 retains its exact prior pad group. All old supply
groups and fixed application/USB repair signatures survive.

The increment removes one track and adds six tracks/three microvias, giving
**15,486 total items**. The cumulative plan adds **926 tracks/67 microvias** with
one removal and fifteen claimed joins. Track width/clearance remain 0.20 mm;
microvias remain 0.30/0.10 mm between adjacent layers. Current capacity, return
locality, copper thickness and the HDI process remain unqualified. No current
limit, part, pad/net assignment, firmware, schematic/BOM or isolated display-enable
boundary changes. Routing an existing net makes no new circuit decision.

## Optional exact-geometry search fallback

`tools/search-native-control-routes.py --native-grid` can now screen grid cells
excluded by the conservative raster against exact native pad/track shapes.
It checks both endpoints and the complete segment whenever either endpoint is
masked. Clear endpoints alone cannot authorize an obstructed step. Native via
checks, the ban on planar In2 steps, zone refill, old-group guards, source/code
fingerprints and ignored-build-only outputs remain in force. Caches belong to
one net/immutable copper transaction and are discarded before the next attempt;
reports retain only counters rather than accumulating geometry caches.

Default mode is unchanged: the retained 225-open application-data fixture is
byte-identical to its earlier default result. With the new option, that fixture
joins U46.6/R79.2/U3.10 with **59 tracks/four microvias (63 items versus 69)**,
52,601 expansions and exactly the same 104 native findings. Two optional-mode
runs are byte-identical. This fixture is local evidence, not a replacement of
the accepted application's existing route or a performance guarantee. Independent
native checks preserve its source copper, 483 placements and every old pad group.

On the current turn's 220-open source, reverse TP11 search reaches 300,001
expansions while forward TP11 exhausts at 1,892. Reset exhausts at 90 versus
58 in the earlier coarse-only screen. Small fine-pitch endpoints remain blocked.
These results show why more search alone does not close the remaining geometry.
The mode-route In1 stack probe and in-board short ground bridges also find no
accepted candidate. Initial off-board bridge probes are rejected and excluded.

Seven new host tests cover disabled-mode behavior, callback avoidance, a blocked
segment with clear endpoints, blocked endpoints, positive/negative/symmetric
caching, transaction isolation and all 168 directed edges of an independent
7×7 analytic-obstacle graph. Host and KiCad Python 3.9 pass; source-only CI now
includes these alongside the existing 21 circuit, fourteen distance and six path
methods. The accepted ground escape is replayed from its reviewed integer plan,
not discovered by this optional search.

## Acceptance and remaining work

Full KiCad 10.0.6 DRC retains the exact normalized multiset of **104 intrinsic
findings**, with no added finding. Native and physical-pad counts agree at 219.
All **256 LED checks, 24 isolated native guards and 21 circuit/metadata tests**
pass, including a fresh complete canonical native XML comparison. New native
fault cases detach ground, detach the row replacement without changing item
counts, and restore the obstructing original source segment. Generation repeats
byte-identically. These are source/geometry checks, not powered-board tests.

GND still has 26 opens, TP11 and the transmit test-pad leg remain open, and six
gate terminals plus remaining power/control/USB routes are incomplete. Remaining
returns, decoupling, current capacity, sequencing/fault behavior, footprint/process
findings, RF, fit, canonical row-package adoption and independent Gate A remain
unqualified/open. No fabrication files are released.

[Ground obstruction audit](../../mechanical/review/native-ground-escape-audit-2026-10-23.json),
[increment/tool evidence](../../mechanical/review/native-control-ground-escape-2026-10-23.json),
[current validation](../../mechanical/review/native-control-validation.json),
[native checker](../../mechanical/review/native-control-check.json),
[per-net opens](../../mechanical/review/native-control-open-nets.json),
[full DRC](led-native-control-drc-2026-10-21.json).

Repeat native acceptance with `./tools/check-native-control.sh` and fresh circuit
comparison with `./tools/check-coupon-study-contract.sh`.
Board SHA-256: `1ddc1f914b714c9ed37fa81e200254bef2dcd842f20794a145c362d508f8d83e`.
