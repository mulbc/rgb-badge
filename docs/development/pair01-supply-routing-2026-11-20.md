<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# PAIR01 supply continuation — 2026-11-20

Selected CAD checkpoint: **23 native and independently physical opens**.
All 212 previous pad groups and all 19,322 retained attached copper items
survive. Main VLED grows from37 to38 pads by joining PAIR01.4; main ground
remains197. ROW00A18, selector00 three and gate00 four pads remain connected.
The board is unbuilt and is not a fabrication release.

Only the existing trial `NTLJD3119CTBG_TRIAL_ONLY` PAIR01 moves, on F from
(76.100,4.300) mm /270° to (80.000,5.200) mm /180°. No flip, substitution,
field change or numbered-net change occurs. All other482 parts remain fixed.
The independent absolute pin transform is x'=84.300−y / y'=x−70.900 mm.
Manufacturer pin/package evidence remains the cached onsemi NTLJD3119C/D
Rev6, April2024, pages1/10; this routing does not approve the trial package.

The ordinary 0.20 mm F supply lead runs via (78.400,4.550),
(78.400,7.800) to the original actual main VLED port (79.100,7.800),
4.625 mm. Ground runs directly to original F ground (82.600,5.250).
The row output uses a body F/In1 access and a 5.700878 mm In1 lead to its
unchanged original port (74.700,2.599999). Gate uses a body F/In1 access
at (80.000,5.550) and reaches the retained R6 In1/In2 port (76.600,4.300).
Three ordinary package straps restore both physical drain pads and gate pins.

The selector's 4.099138 mm ordinary conductor uses three F/In1 0.30/0.10
microvias and reaches original In1 driver segment
`de96a271-92f1-5663-beaa-4f8a0e5658a4`. The retained driver group is
independently witnessed from R22.1/U2.11. No new centre or through via occurs.
Exactly62 obsolete leaves retire: all61 preceding PAIR01 front-ground additions
plus the single old R6 F/In1 gate access. The R6 In1/In2 access and every
original color/row copper item remain. Exactly27 new copper items attach;
the board contains19,349 items and no orphan copper.

Frozen plan: `mechanical/review/pair01-supply-routing-plan.json`.
Board SHA-256:
`9574949d6bd56caa6f79b9db78af3531b0150cfba1f110d727c829effcaf62b3`.
Validation evidence is local under
`hardware/coupon/rev-a/build/pair01-supply-routing/`:

- Four stable prototype fills; two independent three-fill replays produce
  identical bytes. Native/physical23 agree across211 groups on188 nets.
- Full raw serialized copper inventory and typed retired/new ledgers, exact
  483-part identity/fields/local pads, independent absolute pad transform,
  unchanged profiles and immutable board structure pass.
- All259 actual F courtyards pass. All source/new drill checks pass with one
  supported disjoint projected close pair; no unsupported hole is waived.
- Exactly104 original DRC findings remain. Only six intrinsic PAIR01 pad-pair
  clearances (twelve item occurrences) map through the independent same-face
  transform before inherited PAIR01/U48/U52 comparison. External findings
  cannot normalize. Separate checks fix every other part's identity/pose.
- Inverse restores the24-open source SHA
  `230b0c9f456837a0dd1b5e432497aa5223da95334ac2909ff8cd39d2edea804a`
  on all three fills, all212 groups equal, all nine integer filled-zone XORs
  empty and exact104 findings retained.
- All33 deliberate faults reject, with eight shared hole controls and two
  actual F courtyard controls. Four native controls disconnect the supply pad,
  supply conductor, gate conductor or final selector microvia. Added-via
  type/span/pad/drill faults reject. No new central via is part of this plan.
- All42 source-check commands pass. Native F/In1/In2/B views plus source F/In1
  comparisons are reviewed with exact image hashes.

ADRs0238–0242 record the preceding rejected access and bounded routing
studies. A failed sample is bounded evidence, not proof of impossibility.
The original direct ground lead is selected; ADR0241's rejected ground U
path and below-bus selector access are absent. No rejected color reroute is
adopted. The554 unsupported historical centre microvias remain held.

Zero opens and all current/default-off/protection, timing/return/thermal,
trial package, optical/fit, controlled-stack/process and independent Gate A
holds remain unfinished. Fabrication is prohibited.
