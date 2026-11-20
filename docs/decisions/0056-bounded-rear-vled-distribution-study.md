<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0056: Bounded rear-layer VLED distribution study

Date: 2026-10-28
Status: Authorized for ignored feasibility experiments; no canonical VLED parcel selected.

Eight VLED physical-pad joins remain open at the 65-edge checkpoint. Repeated original-width lead/microvia searches cannot reach every pad through the dense control/display copper. ADR 0049 demonstrates explicitly bounded power parcels, but its selected four parcels exclude VLED. This decision permits an ignored masked rear-layer VLED distribution screen, without deleting or changing any original zone or earlier parcel.

Initially evaluate a priority-10 rectangle on B.Cu, x = 75.0–84.0 mm and y = 0.5–32.0 mm, spanning the row-pair supply region. Exact trimmed rectangles or a smaller explicitly recorded union may be explored if native fill partitions prior returns. Use 0.20 mm other-net clearance and minimum copper thickness, full same-net connections, and removal of unanchored islands. Keep every 65-edge track/via, source zone definition, selected parcel, component pose/field/pin/net, test land and DSF neck unchanged. No current, voltage, protection, charge, hardware-limit, firmware or fail-safe enable setting changes are authorized.

Before selecting any parcel, require lower native/independent pad opens, every earlier physical group after three stable refills and exactly the existing 104 full intrinsic DRC findings. Reject any parcel that partitions ground, supply, feedback or control connections, or introduces a new finding. Record exact integer polygons, net/layer/priority/fill parameters and independently enforced replay metadata/fault guards. A new native zone is not permission to redraw or suppress an old zone. Existing orphan restoration and exact original-track replacement proofs remain required.

This is a power-distribution feasibility study, not a current/thermal rating. The captured 39.2 kΩ IREF setting gives a calculated nominal 233.02 mA active white-row load under the existing driver model; it is not a guaranteed worst-case limit. No calculation here raises that setting. Finished copper/via process, voltage drop, thermal behavior, local bypass/return, row switching/EMI, mask/assembly and mechanical access require engineering review. New outer copper remains under the existing mask configuration; no mask opening is added by this screen. Independent Gate A precedes fabrication. No manufacturing output is authorized.

## Ground-preserving per-row screen

The broad rear rectangles partition existing ground groups and are rejected. Investigate smaller per-row rectangles/notched outlines within x = 74.3–80.0 mm and the two partner supply-pad heights ±0.45 mm. An upper-edge notch may leave the partner ground pad and its route to the surrounding original ground plane outside the new VLED copper. All clearance/minimum-thickness/fill parameters, prior-copper/group retention and full native gates above remain unchanged. Native fill, not polygon area, must prove both the intended supply join and every previous return. No parcel is selected merely because its outline reaches both pads.

## Recorded outcome

The four broad rear rectangles retain 68 opens and split previous ground groups; all are rejected. The per-row/notched screen either preserves old groups without making the intended VLED join or loses a ground group. The final retained candidate stays at 65 opens with no new parcel selected. Canonical zone definitions remain unchanged. The failed polygons and generated copper remain in the ignored build tree; these finite screens do not prove a rear supply solution impossible.
