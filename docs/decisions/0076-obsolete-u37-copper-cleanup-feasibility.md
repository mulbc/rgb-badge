<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0076: Obsolete U37 copper cleanup feasibility

Date: 2026-11-01
Status: Ignored bounded simulation only; no canonical retirement selected.

The ADR 0075 supply-restored pair trial preserves all 246 accepted pad groups
and has 56 physical-pad opens but 58 native opens. Its full DRC has the existing
104 intrinsic clearances plus three dangling tracks and three dangling vias at
the vacated U37 site. Read-only contact inventory shows that these items include
both original source copper and previously accepted additions. The SYS tie also
contacts another old via, so a blanket seven-item orphan assumption is invalid.

Permit an ignored cleanup simulation on the restored trial SHA-256
`6396e747b1ef3f32b987a6f35ca129005551f31b57c64a4bc6deb708584bc3fc`. Only an item that is
present in the exact accepted 58-edge inventory, newly reported as dangling by
full native DRC, and wholly within x = 91.5–96.0 mm, y = 0.5–5.0 mm may be
removed from the private trial. Eligible nets are only +SYS_APP_IN_DRAFT, VLED
and the two Net-(L2-~-Pad1/Pad2) switching nets. Use a maximum of eight native
DRC/refill rounds and thirty removed items. Inventory each exact signature,
origin (215-edge source or accepted addition), UUID and direct contacts before
removal. Do not remove new switching/supply routes, ground copper, zones, any
component/pad, or an item crossing the local boundary. Report unresolved findings
outside scope rather than extending deletion automatically.

Keep every prior physical pad group, all poses/local geometry/metadata, all
remaining copper, zone definitions, dimensions and electrical settings. After
each round require unchanged intrinsic clearance identities and all old groups;
abort/retain the preceding ignored state on a split or new geometric finding.
The intended source profile remains unchanged. No field/firmware/current,
protection, enable, capacitor or power-path qualification change is included.

This bounded experiment may discover the exact obsolete stack/branch cohort.
Canonical retirement needs a separate independently enforced exact catalog,
frozen 58-edge presence/origin proof, original/current contact treatment,
retention of every other accepted item and old group, full DRC/pose policy,
deterministic replay and fault/source/original-orphan evidence. Removing an
item from a private simulation does not authorize its removal from source.
All power-stage, part/order-code, electrical/thermal/EMI, return/process/assembly/
fit and independent Gate A holds remain; fabrication remains prohibited.

## Exact leaf-branch continuation

The bounded simulation stops after 21 removals with two out-of-window SYS
F.Cu branches still dangling. Native contact inventories show that each now
contacts only the shared F.Cu SYS bus from (84.00, 31.80) to (104.55, 31.80) mm.
In the frozen 58-edge board each additionally contacts its own now-vacated
F.Cu/In1.Cu via; neither is present in the original 215-edge source. Permit
private removal of exactly these two accepted-addition signatures, and no
other out-of-window item, from round-6 SHA-256
`1cad971cb183a331a0801808234ec7eeafeb35534dfb5c5104aa05a942a069ff`:

- SYS, F.Cu, 0.20 mm: (92.25, 3.65) → (92.25, 31.80) mm.
- SYS, F.Cu, 0.20 mm: (94.25, 0.85) → (94.25, 31.80) mm.

Keep the shared bus and every other remaining copper item, all prior pad
groups, poses, exact parts, zones and settings. Recheck both frozen/current
contact sets and unchanged full intrinsic DRC before and after removal.
This exact extension remains ignored feasibility, with no canonical retirement
or electrical qualification granted. Record three stable fills and independent
physical/native counts.

## Recorded result

The [native evidence](../development/vled-supply-cleanup-feasibility-2026-11-01.md)
records complete prior-group restoration and exact cleanup at 56 native/physical
opens / 104 intrinsic findings. Replays/fills, independent audit, eight fault
cases and original-orphan restoration pass. This remains an ignored experiment;
no canonical pose or copper retirement is selected.
