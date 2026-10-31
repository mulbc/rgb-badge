<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0073: C32 staggered ground-escape feasibility

Date: 2026-10-30
Status: Ignored feasibility only; no copper retirement selected.

The corrected 58-edge board leaves C32.2 isolated. A native 0.025 mm,
eight-direction local search reaches 7,797 B.Cu cells but no legal adjacent
microvia. Requiring a co-located B/In4/In3/In2 stack obscures a narrower first
step: fourteen reachable first-via sites are blocked only by original COL_03_B,
and twelve only by original COL_04_R. Subsequent vias need not share that first
site. These finite observations are not a proof of routing impossibility.

Removing either first obstruction alone reaches only In4. The next-layer
audit finds thirty-one sites in the COL_04_R vacancy obstructed only by
COL_01_G on In3. Permit ignored experiments replacing a subset of the following
exact original 0.20 mm segments, and no other copper:

- COL_03_B: (85.70, 10.75) to (83.50, 10.75) mm, In4.
- COL_04_R: (85.60, 10.30) to (83.20, 10.30) mm, In4.
- COL_01_G: (88.40, 10.65) to (82.95, 10.65) mm, In3.

Keep all original-layer endpoint and intermediate direct contacts connected on
their original layer (In4 or In3). Bound each replacement to its original x extent plus 1 mm at either end,
vertical excursion at most 1 mm, and total track length no greater than original
plus 2 mm. Use unchanged 0.20 mm tracks/clearance and 0.30/0.10 mm adjacent
microvias. An ignored local layered search may stagger successive adjacent
vias to avoid unrelated inner-layer tracks, retaining each intervening conductor.
The new C32 ground route is bounded to 12 mm of aggregate track length; no new
narrow neck is allowed. All other original/accepted copper, zones, parts,
poses, pad geometry/nets, current limits, protection, enable and firmware stay
fixed. No source via or power/USB track may retire.

Re-read TI TLC59581/82 Rev A pages 4–5: unchanged TLC59581RTQT U1 pins 12
(OUTG1), 19 (OUTB3) and 20 (OUTR4) are the relevant constant-current outputs. The official
PDF is cached locally, SHA-256
`c7a736e612dc1ff55057c1c4aa0409e26d401881e6ddb1c65f57fe4b8bfe2cfc`.
Source: https://www.ti.com/lit/ds/symlink/tlc59581.pdf . C32 retains the exact
GRM188R60J106ME47D library approved for source migration under ADR 0069; no
capacitor substitution, land change or electrical approval is implied.

Selection needs an exact independent source/contact/length catalog, complete
58-edge copper/group/pose retention outside these substitutions, lower native
and pad-cluster counts, unchanged full 104 findings, three stable fills,
deterministic replay, fault/source checks and original-orphan restoration.
Reject any split of an earlier supply, return, feedback or control group even
when the aggregate count decreases. The existing canonical source remains
unchanged until that whole gate passes.

This is geometric feasibility, not current capacity, return impedance, timing,
thermal/EMI or process qualification. Independent Gate A and all fabrication
holds remain open; the board is unbuilt.

## Bounded outcome, 2026-10-31

The [C32 study](../development/c32-ground-feasibility-2026-10-31.md) finds a
7.614823228 mm partial ground route after removing COL_04_R and COL_01_G, but
its 59 native/physical opens include two split original colour groups. Full
route and short-prefix restoration screens produce no acceptable transaction;
51 prefix site/order cases fail to restore all colours. No complete candidate
reaches full DRC/refill acceptance. These finite results do not prove routing
impossibility. The accepted 58-edge source remains unchanged, and no enumerated
source track is authorized to retire canonically.
