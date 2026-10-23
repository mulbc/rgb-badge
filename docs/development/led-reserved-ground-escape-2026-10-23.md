<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Reserve a local ground escape and screen exact grid geometry

Status: **unbuilt noncanonical routing study; fabrication prohibited**.

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
