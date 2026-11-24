<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# U54 permission lead and TP14: selected 38-open checkpoint

The selected ADR 0099 successor joins U54.3 to TP14 without moving U54 or
changing any part, net, field, current limit or permission setting. It has
**38 native and independently counted physical opens** and the exact unchanged
**104 intrinsic findings**. It preserves all 227 live groups and 219 additions
of the preceding 39-open checkpoint, plus all 231 immutable 43-open groups.
This is unbuilt Coupon Rev A CAD, with no hardware/firmware measurement.
Three stable fills, identical independent replays, all 27 source-only workflow
commands, exact native DRC, 25 rejection guards and native visual review pass.
The main checkpoint manifest binds the evidence.

## Exact change

The isolated 1.0 mm circular TP14 land moves from (34.001262,1.000001) mm to
(93.500000,22.000000) mm, retaining its 180° B.Cu orientation and entire
footprint/pad/mask/paste/field definition. Its ordinary 0.20 mm B.Cu lead is
(94.250,19.625)–(93.500,19.625)–(93.500,22.000) mm, totaling **3.125 mm**.
That is within ADR 0098's 5 mm study bound. Probe access, loading and fit
remain unqualified, rather than inferred from this geometric bound.

Three old ordinary-width USB_RAW_LOGIC_READY B.Cu tracks are replaced:

- (93.500,18.950)–(92.900,18.350) mm
- (93.500,19.600)–(93.500,18.950) mm
- (92.500,20.600)–(93.500,19.600) mm

The new path is (92.900,18.350)–(92.900,20.350)–(92.500,20.600) mm,
calculating to 2.471699 mm rather than 2.912742 mm. Both original outer
endpoints and **all four actual external B.Cu contact shapes** remain
connected to the new lead. Overlapping prefix contacts are inventoried rather
than reduced to an assumed two-endpoint list. All other copper survives;
there are no new vias or circuit/net/rule/outline/zone-definition changes.

This local replacement opens the formerly obstructed U54 output exit. It does
not bypass the USB-ready condition or change its source/sinks. The native
checks independently rederive the boundary inventory and verify retained
item identity, layer and direct shape contact after every refill.

## Part and source evidence

The unchanged exact IC is TI **SN74LVC2G00DCUR**. The manufacturer Rev. N
SCES193N pin table/top-view DCU map on PDF page 3 confirms pin 3 is gate-2
output 2Y; the existing input/output nets and gate type remain unchanged.
The appended DCU0008A 4225266/A September 2014 land example on PDF page 21
retains eight 0.85 × 0.30 mm lands, 0.50 mm pitch and 3.10 mm outer span,
matching the existing local footprint. Both pages were rendered and read
visually. No manufacturer component is added for the copper test land.

[TI manufacturer reference](https://www.ti.com/lit/ds/symlink/sn74lvc2g00.pdf),
ignored cache SHA:
`e15782a519f712eed3d794da178f8ca94af402b7960e71ae5ce192729a74a564`.
Vendor PDF/rendered pages remain local and uncommitted.

The preceding 39-open source is preserved in commit `772c83a`, SHA
`aab8f44a9ec3ae65aed4ee2500d52d57d4d3872c8428b8f50c765bfedd205a1e`.
The new deterministic PCB SHA is
`01fb2e8a1ac781172797d369df99ff3c834016453ffeaa3d76c224b525355031`.
The exact plan and native audit bind the old/new copper, numbered join,
original isolation and no-copper-contact proof. A native bottom-copper view
is local at `build/remaining-routing/38-permission.png`.

The zero-open goal remains ongoing. Electrical/thermal/USB/stack/process/fit,
557 historical centre-microvia and independent Gate A holds remain open;
fabrication is prohibited.
