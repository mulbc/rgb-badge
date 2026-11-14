<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0072: Coordinated converter floorplan feasibility

Date: 2026-10-30
Status: Ignored feasibility only; no canonical pose or copper rework selected.

ADR 0054's fixed-converter inductor screen selects no sampled pose. A read-only
inventory of the accepted 58-edge source also finds long capacitor/feedback
separations and direct nonzero copper at every converter-stage component except
L1/L2. Moving those components without reconnecting their existing contacts
would lose accepted work. A short inductor route alone cannot qualify a stage.

Permit an ignored, read-only coordinated placement screen using the thirteen
current exact VLED footprints U37/L2/C44–C49/C63/R84–R87, arranged according to
the historical standalone VLED layout template, with historical C50 mapped to
current C63 by function. Use current exact footprints, pads, nets and MPNs;
the old template supplies poses only. Mirror that front-side template onto the
current back side, then sample rigid translations on a 0.5 mm grid and four
90° rotations inside the unchanged 114 × 32.5 mm board.

Exclude only those thirteen current component courtyards from fixed-component
obstructions. Retain every current track/via, other component and zone. Check
the full translated courtyard polygons and internal courtyard separation before
any native other-net pad/copper/edge screen. Touching courtyards are obstructed.
This is a finite packing screen, not approval of the old template's power or
feedback layout. Record source/template/tool hashes, sampled bounds, obstruction
counts, exact surviving poses and source-byte retention. Write raw outputs only
under ignored build storage. Do not route or save a replacement canonical PCB.

No part substitution, land change, current/voltage adjustment, protection,
enable or firmware change is authorized by this experiment. A future accepted
floorplan requires a separately specified exact copper-rework/contact policy,
reconnected old groups, suitable power-path geometry, native and independent
connectivity, full DRC, replay/fault/source evidence and updated requirements.
Moving an IC also requires distinguishing transformed intrinsic footprint
findings from newly introduced findings; do not relax the existing DRC gate.

TI TPS631000 Rev C §7.4 and TPS63020 Rev I §10 still govern short/wide power
paths, nearby passives, feedback separation and ground returns. Effective
capacitance, current, thermal, EMI, mechanical/assembly/process qualification
and independent Gate A remain open. The unbuilt board is fabrication-prohibited.

See the [floorplan inventory and packing report](../development/converter-floorplan-58-2026-10-30.md).

## Bounded result

The 60,456-pose screen has one preliminary survivor. An independent native
all-pairs check confirms its courtyard/pad clearance, but the ignored unrouted
witness has 76 native opens, 73 pad-cluster opens, 53 split-pad witnesses and
14 new dangling findings after three fills. All 104 intrinsic clearance
descriptions/pad UUIDs remain accounted for. No pose or copper rework is
selected; the canonical source remains the accepted 58-edge checkpoint.
