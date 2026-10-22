<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Gauge IC data route with preserved pullup supplies

Status: **unbuilt noncanonical geometry study; fabrication prohibited**.

The [saved native-control derivative](../../hardware/coupon/rev-a/staging/led-native-control-trial-114mm.kicad_pcb)
now joins **MAX17048 U35.8** to the existing **R101.2 / TCA9517A U46.3** gauge
SDA group. Native and physical-pad open counts decrease **224 → 223**, and gauge
SDA has zero opens. Gauge SCL still needs U35.7. These are source connectivity
results; no bus operation or hardware measurement is claimed.

The [preceding reversed search](native-route-search-upgrade-2026-10-22.md)
reached the IC in 540,461 expansions but split the old application-supply group:
R42.1, R43.1, R44.1 and R79.1 disconnected from the main group. Direct and
pad-centred adjacent-layer supply bridge probes found no acceptable candidate.
The route remained rejected until the split itself was removed.

## Selected geometry

A bounded local probe examines native-clear In4-to-In3 microvia sites along the
new SDA column at x = 40.9 mm, y = 9.25–17.5 mm. Eighty-four via positions and
309 same-x In3 detours pass the foreign-net track/pad shape screen. Longer
clear detours are considered first; the first filled-zone transaction, from
**(40.9, 14.8) to (40.9, 15.8) mm on In3**, preserves every previous physical
pad group. Two adjacent-layer microvias join its ends to the remaining In4
column. Every source copper item remains; only newly proposed signal copper is
detoured. No supply copper is added and the exact prior supply-repair signatures
are unchanged. Complete native DRC then retains the exact original findings.

The accepted increment adds **128 tracks and ten adjacent-layer microvias** at
0.20 mm track width/clearance and 0.30/0.10 mm via diameter/drill. All 483
placements, pad assignments, 465 shared component identity fields and previous
physical pad groups survive. The cumulative replay plan adds **471 tracks and
48 microvias** to the frozen row-13 source: **15,013 total items, eleven joins**.
The integer [routing plan](../../mechanical/review/native-control-routing-plan.json)
and unchanged deterministic generator reproduce the accepted board without
rerunning the exploratory search. Two sequential generations are byte-identical.

Canonical schematic/BOM, exact parts, libraries, firmware, current limits and
isolated interlock boundaries are unchanged. This is routing of an existing net
under ADR 0030, with no material circuit decision or package adoption.

## Validation and remaining work

KiCad 10.0.6 full DRC retains exactly **104 intrinsic clearance findings**, with
no new normalized finding. Native and physical-pad counts agree at **223 opens**.
All **256 exact LED checks**, **19 isolated native guard cases**, **21 circuit/
metadata fault tests**, and a fresh complete canonical native XML comparison pass.
The source-only CI layout passes its 21 circuit, fourteen distance and six path/
CLI methods without vendor PDFs, native XML or KiCad.

The added fault case moves only the 1 mm detour back onto In4 while retaining
item counts. Gauge SDA remains connected, but all four application-supply pads
lose their main group; the physical-group checker must reject it. This exercises
the actual filled-zone failure rather than relying on total open counts alone.
These are native geometry/software checks, not independent electrical review.

GND, VLED, application 3.3 V and USB logic retain respectively **27, 14, 7 and 4
opens**. TP11, U35.7, R47.2/TP4.1, six gate terminals and remaining power/control/
USB routes are incomplete. Bus timing/LOW/leakage/transition behavior, return and
decoupling locality, current capacity, intrinsic footprint findings, HDI process,
mechanical fit, canonical row-package reconciliation and independent Gate A
remain unqualified/open. No fabrication output is released.

[Increment evidence](../../mechanical/review/native-control-gauge-ic-data-2026-10-22.json),
[current validation](../../mechanical/review/native-control-validation.json),
[native checker](../../mechanical/review/native-control-check.json),
[per-net opens](../../mechanical/review/native-control-open-nets.json),
[full DRC](led-native-control-drc-2026-10-21.json),
[reproduction](../../mechanical/review/native-control-reproduction.json).

Repeat with `./tools/check-native-control.sh` and
`./tools/check-coupon-study-contract.sh`.
Board SHA-256: `29d1f9cec25abc5ed199dd29b96c11338a646a2a95c4e6b49667e9a1b41bcf7e`.
