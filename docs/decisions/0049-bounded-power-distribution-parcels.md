<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0049: Bounded inner-layer power-distribution parcels

Date: 2026-10-23
Status: Accepted for explicitly recorded unqualified routing-study pours only.

## Context

The 122-edge checkpoint still has 22 opens across the existing SYS, protected-battery, USB input/output and charger-input nets. Existing inner-layer VLED and logic-supply pours cover regions with no corresponding load/anchor. Connecting those power pads with scattered long 0.20 mm tracks would leave current distribution and return paths unresolved. Bounded same-net parcels provide a distinct power-distribution study without changing circuit connectivity or current limits.

## Decision

Evaluate priority-10, 0.20 mm-clearance/minimum-thickness inner-layer rectangles, using full connections to internal vias and removal of unanchored islands. Retain every original zone definition. Record every selected rectangle in integer units, with exact net, layer and fill settings; replay and independent checks must match them exactly. Initial screen, millimetres:

- SYS on In1: left strip x 0.5–6/y 0.5–32; left upper blocks x 0.5–46.5/y 0.5–5.3 and x 0.5–49.5/y 0.5–3; bottom strip x 0.5–113.5/y 30.3–32; right strip x 110.8–113.5/y 0.5–32; converter VIN blocks x 102–113.5/y 5–7.5, x 90.7–113.5/y 0.5–1.3 and x 90.7–92.5/y 0.5–4.4.
- USB 5 V on In1: x 90–110.5/y 8–22 and x 90–95/y 21.5–26.
- Charger input on In1: x 99.3–100.7/y 18.5–24.5 and x 99.3–110.5/y 24–30.
- Protected battery on In4: left strip x 0.5–6/y 2.1–32; upper link x 0.5–28/y 2.1–3.3; bottom strip x 0.5–113.5/y 30.2–32; charger corner x 105–113.5/y 23.5–32.
- Raw VBUS on In3: x 104.7–113.5/y 12.5–30; x 90–113.5/y 24–30; x 96–105.5/y 14.2–16.2; x 96–100/y 11–16.2.

The selected inventory may be a smaller set or use explicitly recorded trimmed rectangles when native geometry rejects an initial boundary. Do not infer current capacity from filled area. Added escapes retain 0.20 mm tracks and 0.30/0.10 mm adjacent-layer microvias; keep all current, protection, physical-switch and enable-domain boundaries unchanged. Require lower actual native/physical-pad opens, preservation of every accepted 150-edge pad group, every non-retired original track and the exact 104 intrinsic DRC findings after refill. Reject parcels that isolate an earlier supply or return, produce a new finding or fail independent replay. Native orphan-via evidence and any separately authorized track-retirement evidence remain required.

## Remaining acceptance work

These are power-distribution source experiments, not proven supplies. Current-density/voltage-drop and thermal calculations require the actual finished copper and via process; converter input/output bypass locality, switching-loop area, Kelvin/return paths, source/switch limits, RF/mechanical fit, EMI and transient behavior remain engineering review work. No current setting is raised and no new load is enabled. Independent Gate A remains mandatory before fabrication; no fabrication outputs are released.

## Bounded continuation of the initial screen

The joint screen also evaluates a masked rear SYS perimeter strip at y 31.3–32 mm, connected to the In1 side parcels with original-size adjacent microvia stacks near x 5.4 and 112 mm. This avoids using a long In1 bottom parcel through the last LED row. Exact selected boundaries and any explicit VLED-preserving exclusions are recorded in the plan; no source zone is deleted. Selected support-capacitor moves remain subject to ADR 0045. A temporary keep-islands setting may expose potential copper for a stitch search, but every selected zone must restore remove-unanchored-islands before final refill/DRC. Every retained intermediate stitch must form real copper contact; final counts, all earlier pad groups and the exact intrinsic findings govern acceptance. Perimeter width and transitions remain unqualified for current/thermal/voltage-drop performance until the actual stack and load/source corners are reviewed.

## Selected outcome, 2026-10-25

The accepted 100-edge checkpoint selects four parcels: USB 5 V on In1, charger input on In3, and protected battery/raw VBUS on In4. The integer plan records their complete selected polygons and native definitions; the initial rectangles above are search history. The VBUS right edge is trimmed to x 110.5 mm to preserve the application-supply corridor. Every original zone definition remains exact. Independent native and portable checks reject added-zone boundary/net/fill changes and original-zone drift.

SYS pour variants are rejected because they split accepted VLED, USB-logic or ground groups. Selected SYS distribution instead uses 0.20 mm tracks with adjacent-layer microvia escapes and a perimeter crossing on In4 at y 31.8 mm, with outer sections on F.Cu. A three-item, original-width VLED bridge between R14.1 and R13.1 restores the earlier VLED group interrupted by the C40 escape stack. These long tracks and transitions remain unqualified for current, voltage drop, local bypass/return behavior and manufacturing; the unchanged hardware current limits are not a route-current rating. The complete selected copper inventory and every accepted 150-edge pad group must survive independent replay and native DRC.
