<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# R6 direct bottom continuation — 2026-11-20

Selected CAD checkpoint: **24 native and independently physical opens**.
The R6 pull-up reaches both its original main VLED group and the four-pad
ROW_GATE_00 group. All 213 previous groups and all retained attached copper
remain intact. The board is unbuilt and is not a fabrication release.

Exact Panasonic ERJ2RKF1001X R6 moves on B from (57.250,8.750) mm / 180°
to (77.750,5.600) mm / 90°. All numbered pad nets, fields, identities and
local package geometry remain unchanged. Independent absolute pin transform:
x'=86.500−y / y'=x−51.650 mm. No other footprint moves.

The new 1.207529 mm B supply lead reaches the actual original connected
PAIR02.4 pad at (78.825,6.650). The 2.224775 mm gate conductor reaches the
existing front PAIR01 gate body through four supported 0.30/0.10 mm adjacent
microvias and one mechanical buried 0.50/0.30 mm In2/In3 centre. No new
power via or through via is added. Supported access topology does not qualify
fabricator stack, filling/capping or assembly capability.

Exactly six old R6 supply items retire. The shared In2 stem retains its exact
remainder from (58.750,9.713636) to (58.750,14.050), including the original
607bd79b-bb37-5fc4-8a76-ed1e127f247c junction and every other source contact.
All original color and row copper remains unchanged. Earlier color-detour and
placement alternatives are unselected; their exact evidence digests and
bounded outcomes are in `mechanical/review/r6-placement-continuation.json`.

The 23,100-pose native screen finds 1,043 complete direct-supply placements.
The selected pose has the shortest combined supply/gate lead of the sampled
successful candidates. Exact frozen plan:
`mechanical/review/r6-direct-bottom-plan.json`. Board SHA-256:
`230b0c9f456837a0dd1b5e432497aa5223da95334ac2909ff8cd39d2edea804a`.

Validation evidence under `hardware/coupon/rev-a/build/r6-direct-bottom-routing/`:

- 212 physical groups on 188 nets; all 213 source groups preserved, main
  GND197, main VLED37 and full ROW_GATE_00 four-pad group connected.
- All 19,374 retained original Cu and all ten new items attached, zero orphans;
  complete raw serialized Cu, exact 483-part fields/pads and source-contact
  inventory, profiles/rules and immutable board structure checked.
- All 224 actual B courtyards and full new/source holes pass, including two
  aligned supported access pairs and four close projected disjoint span pairs.
- Exact original104 DRC findings; only the inherited exact PAIR01/U48/U52
  intrinsic transformations apply. No new external finding is waived.
- Four stable prototype refills and two independent three-refill replays
  produce identical board bytes.
- Full inverse restores source SHA-256
  `ec0bf7fc842f3dd4f9210e7667925cffc388d3d82906e44c5bde4e10f428ee88`
  on all three fills, with all 213 source groups equal and all nine integer
  filled-zone XORs empty; inverse original104 is exact.
- All 33 deliberate faults rejected, eight shared drill controls and two B
  courtyard controls pass. Four controls prove actual native disconnections
  after moving the supply pad or removing supply, gate or centre. Four
  additional controls reject wrong centre type/span/pad/drill geometry.
- All 41 source workflow commands pass. Native F/B/In2/In3/In4 and old B/In2
  region exports are visually reviewed with exact image digests recorded.

The portable checker pins the actual KiCad 10.0.6 buried-via enum value (3);
the native checker uses its named constant. The wrong-layer control changes
the B lead to F, so it cannot pass by reassigning the existing layer.

Retiring the old R6 central microvia reduces the remaining unsupported
historical centre count from 555 to 554. Every remaining one stays held.
PAIR01.4 and all other outstanding opens remain explicit. The zero-open goal,
current/default-off/protection requirements and all electrical/timing/return/
thermal, trial package, optical/fit, stack/process and independent Gate A
holds remain unfinished; fabrication is prohibited.
