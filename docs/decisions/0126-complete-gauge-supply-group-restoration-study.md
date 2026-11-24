<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0126: Complete group restoration for the gauge supply route

Date: 2026-11-12
Status: Accepted for ignored coupled feasibility only; no successor selected.

Continue from selected 33-open source
`14f0c49582063bab84ea685a8cec798011eb4cd66389b085a3a47777180a13ce`.
ADR 0125's direct unweighted search finds a provisional U35 gauge-supply path
but rejects it after refill splits four original groups. Its exact rejected
snapshot is `95e972e4039b5e2f16d3e44600a89e2710a88dd5297dbdfb31eac6e0b499ff4b`.
The separate two-layer outer-route search exhausts its sampled graph after
384,131 expansions without a path. Neither result is selected progress or
proof of general infeasibility.

Permit ignored additive restoration on a copy of the exact rejected snapshot.
Restore every member of the original main GND group, VBUS_CONNECTOR including
TP32.1, +3V3_APP including R106.1, and protected battery including
C53.1/U41.2/U41.3. Restoring only a subset of an original group is insufficient.
No other old group may be split during restoration. Keep every selected-source
part, pose, local pad, net, copper item, rule/profile and zone/board outline.
The temporary off-grid U35 capture is not part of this snapshot or permission.

Use ordinary 0.20 mm tracks, supported adjacent 0.30/0.10 mm microvias,
0.50/0.30 mm In2/In3 buried transitions and optional complete 0.50/0.30 mm
F/B vias. Check actual pad/track shapes on every affected layer, all existing
holes, board edges and individually native-witnessed filled components.
Do not introduce another centre microvia, mixed-drill co-location warning,
narrower copper, source retirement, pin/net change or protection/current-limit
change. These are CAD continuity studies; power capacity and return quality
remain unqualified.

Final selection requires a frozen complete ledger from the immutable 33-open
source, the actual eight-terminal gauge group, every one of its 221 original
live groups, matching native/physical count below 33, exact unchanged 104
findings, stable independent replay/refills, source/fault checks and visual
review. A partial or pad-free count improvement cannot count as completion.
The selected source remains at 33 until all gates pass. Gauge bypass, current,
return/bus/rail-transition behaviour, controlled stack, 557 historical centre
vias, assembly/process/fit and independent Gate A remain open; no fabrication
or powered-operation qualification is authorized.

The ground-restoration trial rejoins all four newly split ground components
with no further old-group loss, and the input trial restores TP32 to its full
original VBUS group. Native/physical 34 opens and exact 104 findings remain
unselected while APP and battery groups are still split. Two short APP paths
are rejected because they re-isolate TP32.

A supported In3/In4 microvia at the exact existing R106 capture position
(94.453742,26.250001) mm, UUID `43706c45-94c7-5495-9470-8017b62f0841`,
retains the In4 footprint of the existing In4/B capture. Its new In3 contact
passes native copper/hole screening and refills retain all current groups.
It is an unfinished capture, not a selected join. Permit continuation on In3,
with candidate plane endpoints eroded inward 0.151 mm so a complete 0.30 mm
capture fits within its individually witnessed original filled component.
This search reservation adds no copper and relaxes no rule. Final complete
APP/VBUS/battery/GND retention and exact 104-finding acceptance remain mandatory.

## Bounded USB and ground repair after the four-layer battery bridge

The four-layer battery attempt (B/In4/In3/In2 only) preserves VLED and restores
the original protected-battery group, but is rejected for renewed GND and
USB-supply splits. Its exact J2-side snapshot is
`6860cf2077e689d1c66e80e046e1d82f46b7a16c775d64ff5aa7c2fd6c26aa7d`,
with 35 native/physical opens. USB groups contain 25, seven and the original
isolated U39 pad. No In1 copper is added in this battery attempt.

Extend ignored coupled restoration only to the exact original 32-pad
+3V3_USB group alongside GND. Preserve U39's separately counted supply open
unless its actual terminal is also connected and declared in a future ledger.
Restore every original source group, not only the listed witness pads. APP,
VBUS, battery, VLED and every other current pad group must remain intact during
these repairs. The six-layer descendant that loses VLED remains excluded.

Native read-only proxies identify clear supported In1/In2 0.30/0.10 mm
extensions at existing USB centre-capture positions (76.151904,30.849096) and
(76.951904,30.049096) mm; In3/In4 proxies there are blocked by retained gauge
or ground copper. A clear proxy is not a join or permission to alter VLED.
Prefer ordinary supported four-layer routing first. Any exact off-grid
extension must retain its old copper/drill footprints, clear all foreign
copper and holes, preserve every current group after refill and eliminate
all dangling findings in a completed successor. No original centre via may
be retyped or deleted. Final exact DRC, all 221 source groups, deterministic
replay, fault/source and visual gates remain unchanged.

## Reserve the original USB plane during alternative battery routing

The two ground repairs on the four-layer battery snapshot restore the original
main ground group, with 33 native/physical opens and exact original 104
findings. The original 32-pad USB supply remains split. In parallel with its
additive repair, permit an ignored alternative battery search from the clean
APP-restored source. Reserve the actual original native-witnessed USB In3
filled copper within the central x=57..79 mm strip against new battery copper.
This is an additional search restriction, not a new board keepout or a rule
relaxation. It does not retire any original or selected copper. Any resulting
path still requires actual battery/gauge groups, all 221 selected-source
groups, unchanged exact DRC and complete successor gates. Search exhaustion
or a bounded result is not general infeasibility.

The broad strip reservation exhausts its sampled graph in both directions.
A read-only native inventory shows that the old USB connection passes through
an In3 filled component ending at the retained In2/In3 capture
(76.151904,30.849096) mm, then through retained In2 copper to the separate right
component. The polygons' overlapping bounding boxes do not establish contact.
Permit the more focused alternative: reserve an ordinary 0.20 mm corridor
through the actual old filled component to that exact retained capture.
Derive its centreline on a 0.05 mm grid within a native 0.101 mm inward offset.
These proxy tracks exist only in search occupancy; never add them to the PCB
or count them as a new connection. All actual copper and final gates remain
unchanged.
