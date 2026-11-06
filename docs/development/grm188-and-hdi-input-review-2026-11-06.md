<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Supplied GRM188 reference sheet and proposed HDI stack

Date: 2026-11-06. Status: source verification and read-only proposal review.
No schematic, component value, board geometry, stack, rule or current limit is
changed. Independent Gate A and fabrication holds remain open.

## Manufacturer PDF

The owner supplied `GRM188R60J106ME47-61A-EN (2).pdf` from Downloads.
It is byte-identical to the already-cached June 14, 2026 Murata reference sheet:
SHA-256 `f51cff8dad7a6983263ab35b5705f4d1d4b9977b1f03739c653381ba03d94ea8`.
Both filenames are preserved in the ignored vendor-datasheet cache; its local
index records origin, date and hash. No vendor PDF or rendered page is committed.

Manufacturer authorship is confirmed. Page 2 nevertheless labels this a
reference sheet and requests the approval sheet before ordering. This distinction
does not invalidate the source; it preserves the manufacturer's stated scope.
Full relevant PDF pages 2, 3, 5, 12 and 13 were visually inspected.

| Owner-supplied claim | Manufacturer evidence / disposition |
|---|---|
| 10 µF, 6.3 V, 0603/1608, X5R | Confirmed p.2; initial capacitance tolerance is ±20%, measured under p.3 conditions (1 kHz, 0.5 Vrms, room temperature). |
| ±15% over −55 to +85°C | Confirmed p.2; p.3 temperature test explicitly uses **no DC bias**. It does not guarantee the same capacitance under operating DC bias. |
| Roughly 40–50% bias loss at 3.3 V, 70–80% near rating | Generic owner estimates, not exact GRM188 data in this PDF. Page 12's DC curve is explicitly an **example for X7R 0.1 µF / 50 V**, not this 10 µF X5R. Do not digitize it for C44/C45. |
| 5% capacitance loss per decade-hour | Page 13 has a generic illustrative X5R aging curve consistent with this sort of estimate, not a numerical guaranteed exact-part aging limit. An aging model also needs its reference time since de-aging, intended life and operating conditions. Keep 5%/decade as an assumption until supported for the exact part. |
| 1000 h at 85°C and 150% voltage, ±12.5% change | Substantially confirmed by p.5, with material qualifications below. |

The endurance test specifies maximum operating temperature ±3°C, 1000±12 h,
150% rated voltage (calculated 9.45 V), and a 50 mA maximum charge/discharge
current. It includes heat treatment at 150 +0/−10°C for one hour and
24±2 hours at room temperature **before and after** testing, before measurement.
Thus the ±12.5% acceptance criterion is not an in-circuit capacitance bound
while biased at 85°C, nor a persistent-aging guarantee after normal service.
The stress test does not increase the 6.3 V operating rating. Murata's
[aging explanation](https://www.murata.com/en-global/support/faqs/capacitor/ceramiccapacitor/char/0013)
also explains capacitance recovery after heating above the Curie temperature.

C44/C45 operate on SYS; 3.3 V bias alone does not cover their operating envelope.
The previous review's 4.5 V steady and higher-voltage sensitivity cases still
need exact GRM188 data and the actual SYS transient envelope. Manufacturer
SimSurfing data with voltage/temperature/AC-test conditions, aging reference
and a defensible combined lower-bound method remain missing. No prior
sensitivity is upgraded to a guaranteed minimum by this attachment.

## Proposed 1+4+1 stack: arithmetic and CAD compatibility

The stack dimensions are owner-supplied proposal inputs, not an identified
fabricator's controlled build. The deterministic
[native inventory and arithmetic](hdi-proposal-review-2026-11-06.json) is derived
from selected board SHA-256
`5e07fb866cc059de670e34102045d9dfd88c88f101355fcdbb27253c0ae26e43`.

| Check | Result / disposition |
|---|---|
| Six 35 µm copper layers | 0.210 mm total copper; retain as a proposed sensitivity, not a finished-copper guarantee. |
| Five dielectric entries | 0.076+0.100+0.710+0.100+0.076 = 1.062 mm. |
| Listed copper + dielectric total | **1.272 mm**, not 1.600 mm; **0.328 mm unaccounted for** before mask/finish. Clarify whether any vendor core dimension includes copper, to avoid double counting. |
| Algebraic central-dielectric correction | Holding all other entries fixed would require 1.038 mm instead of 0.710 mm. This is arithmetic only, **not a selected build**. |
| Selected CAD board thickness | 1.0 mm; no finished copper/dielectric stack is specified. |
| USB connector fit | Existing [USB4505 review](../../mechanical/usb-led-edge-screen-2026-09-26.md) cites a 0.80 mm recommended PCB. Existing 1.0 mm CAD and proposed 1.6 mm both need explicit connector/assembly review. |
| Outer via dielectric/hole estimate | 0.076/0.100 = 0.76. Confirm the fabricator's actual via-depth and hole-size conventions/tolerances; this ratio alone does not establish plating reliability. |
| Proposed 0.25/0.10 mm microvia annular ring | (0.25−0.10)/2 = **0.075 mm**; current 0.30/0.10 mm geometry gives **0.100 mm**, the ADR 0047 study floor. No pad reduction is adopted. |
| Proposed PTH at 1.6 mm / 0.2 mm hole | Nominal 8:1; drilled versus finished-hole definitions, plating and capability remain unspecified. |

The current CAD uses these spans (L1=F.Cu through L6=B.Cu):

| Span | Current microvia count | Supported by supplied outer-microvia scheme? |
|---|---:|---|
| L1–L2 | 909 | Nominal span yes; process/pad dimensions still differ |
| L2–L3 | 506 | No |
| L3–L4 | 557 | No |
| L4–L5 | 607 | No |
| L5–L6 | 705 | Nominal span yes; process/pad dimensions still differ |

There are **3,284 microvia objects, including 1,670 on inner-layer spans**, plus
16 through vias at 0.50/0.30 mm. Counts represent individual CAD via objects,
not independent holes, complete stacks or process cycles. The proposed buried
L2–L5 via does not reproduce separate L2–L3, L3–L4 or L4–L5 terminations.
Relabelling or extending them could join unrelated layers/nets and is prohibited.
A new topology needs rerouting and a full contact/net/clearance review.

The proposed L3–L4 dielectric is 0.710 mm. An existing 0.10 mm microvia across
that entry alone would imply about 7.1:1, rather than an outer laser via's
0.76 estimate. This directly demonstrates why the current adjacent-layer
microvia model cannot be mapped onto this build unchanged.
[NCAB's HDI description](https://www.ncabgroup.com/hdi-high-density-interconnect-pcb/)
distinguishes single versus multiple microvia build-up layers and recommends
aspect ratio below 0.8 for 100 µm copper-filled microvias. This is general
manufacturing guidance, not approval of this board or a selected supplier.

Assigning L2/L5 as ground planes also requires reviewing existing routing on
those layers; the current file has not reserved them as dedicated continuous
planes. A layer label alone cannot establish signal integrity or a return path.

## Consequence and next step

The original [complete-stage review](converter-power-layout-review-2026-11-05.md)
stands. U36 full-stage correction remains first in its layout queue. The
proposal adds an explicit **fabrication-topology decision** before selecting
further production-intended routing: either obtain a qualified build supporting
the required spans and thickness, or plan a bounded reroute for a simpler
fabricator-supported topology. Neither route is adopted here. Keep existing
geometry/currents/default-off/protection settings unchanged while investigating.

Request a controlled supplier build identifying finished thickness/tolerance,
copper by layer, pressed dielectrics/material, all allowed via spans, drilled
versus finished holes, capture/target pads, fill/cap, stack/stagger policy,
reliability acceptance and mask/assembly capabilities. Resolve connector/case fit
with that actual build. Generic reliability claims and the capacitor
manufacturer PDF cannot supply PCB-fabricator process approval.

Reproduce the read-only stack inventory:

```sh
/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/3.9/bin/python3 tools/review-hdi-stack-proposal.py --output hardware/coupon/rev-a/build/hdi-proposal-replay-2026-11-06.json
cmp docs/development/hdi-proposal-review-2026-11-06.json hardware/coupon/rev-a/build/hdi-proposal-replay-2026-11-06.json
python3 tools/check-converter-checkpoint-plan.py
```

Validation: source/cached PDF bytes and SHA agree; independent Decimal thickness
arithmetic and native span inventory agree; replay is byte-identical; selected
checkpoint fingerprints remain unchanged. This is no hardware test.
