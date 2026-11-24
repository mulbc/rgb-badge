<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Native pad-centre TP13 connection: selected 37-open checkpoint

The ADR 0101 successor joins exact U55.7 to TP13.1 at **37 native and
independently counted physical opens**, with the exact unchanged **104
intrinsic findings**. All 226 preceding live pad groups and 223 additions
survive, as do all 231 immutable 43-open parent groups. This additive step
retires or changes no preceding copper and leaves the window-permission lead
untouched. It is unbuilt Coupon Rev A CAD, with no powered hardware/firmware
measurement or fabrication permission.

## Geometry

TP13's unchanged 1.0 mm circular B.Cu land moves from
(82.501262,10.500001) mm to (23.250000,23.300000) mm, retaining its 180°
orientation, entire footprint, numbered net, fields and mask/paste definition.
An ordinary 0.20 mm In4.Cu diagonal joins it to U55.7, calculating to
**3.857541315 mm**, excluding via travel. The two new adjacent B.Cu/In4.Cu
microvias are exactly 0.30/0.10 mm at (26.250000,20.875000) mm and
(23.250000,23.300000) mm. No central or skipped span, rule change or
narrowing occurs.

The source capture's exact Y coordinate matters. On the unchanged 38-open
source, native foreign-copper checks find the exact 20.875 mm point clear.
The neighbouring 0.05 mm routing-grid levels fail: 20.850 mm interferes with
U55.8/+3V3_APP clearance, and 20.900 mm interferes with U55.6/VLED_WINDOW_OK.
The deterministic ledger retains the exact integer coordinates. Raw native
shape evidence is ignored at `build/remaining-routing/37-native-grid-witness.json`.
The existing generic grid-search implementation is unchanged.

The exact IC remains **SN74LVC2G08DCUR**. TI Rev. N SCES198N, December 2015,
PDF page 3 confirms pin 7 is output 1Y and pin 6 is input 2B. Its page 21
DCU0008A 4225266/A September 2014 example retains eight 0.85 × 0.30 mm lands,
0.50 mm pitch and 3.10 mm outer span, matching the existing local footprint.
Both pages were rendered and read visually. Current/window thresholds,
permission/default logic, protection, firmware and all other poses remain
unchanged by this step.

[TI manufacturer reference](https://www.ti.com/lit/ds/symlink/sn74lvc2g08.pdf),
ignored cached SHA:
`75dff6a7b9ba988865b776e0f7c5dd2855f13f64f05bfcda3b1baec886007199`.
Vendor PDF and rendered pages remain uncommitted.

## Validation and traceability

The preceding 38-open PCB is commit `d6a36e8`, SHA
`01fb2e8a1ac781172797d369df99ff3c834016453ffeaa3d76c224b525355031`.
The selected 37-open PCB SHA is
`ed6d3ff570f2481b47423d8375d9d4a40d756145cdd49e2c222bacc36edbfa57`.
Three stable fills per generation and two independent replays are identical.
Native/physical, exact DRC, all 27 source workflow commands, 30 isolated fault
guards and separate native B.Cu/In4.Cu visual review pass. The source contract
retains 465 common components and 1,718 logical pins; all 483 footprints and
2,092 physical pads survive.

Five new guards cover actual VLED-enable probe disconnection, rounded source
capture with a matching ledger, old-site TP13 copper contact with a matching
ledger, remote TP13 and forged historical isolation. The original isolation
bases are explicit: TP14 uses the 39-open source and TP13 the 38-open source.
An advancing checkpoint retains the earlier selected join rather than
incorrectly requiring that already-connected test land to be isolated again.
Conservative parent/current copper-superset checks still verify the recorded
old land shapes have no source-copper contact.

The bounded window-transfer experiment under ADR 0100 remains unselected:
its partial escape has 38 opens and one additional dangling-via warning, and
its fixed-TP13 searches do not establish a complete route. None of its copper
retirements or replacement vias enters this selected ledger.

Via-in-pad assembly/process, probe exposure/loading, signal/return, power/
thermal, controlled stack, 557 historical centre-via and fit qualification
remain open. Independent Gate A precedes fabrication. The zero-open goal is
still in progress.
