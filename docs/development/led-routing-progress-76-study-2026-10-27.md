<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Routing continuation: 82 to 76 unconnected edges

Historical checkpoint at commit 42e16a1; see the [71-edge continuation](led-routing-progress-71-study-2026-10-27.md). Validation fingerprints describe the files at that commit.

Date: 2026-10-27. Status: unqualified native source study, without hardware measurements or fabrication release. The requested 50-edge target remains open.

The selected derivative reduces native and independently counted physical-pad opens **82 → 76**, preserving exactly **104 unchanged intrinsic DRC findings**. The [82-edge integer plan](../../mechanical/review/routing-progress-82-checkpoint.json) at 88fdcbe is additionally frozen under [ADR 0052](../decisions/0052-preserve-94-edge-routing-checkpoint.md). Every accepted copper item, completed physical pad group, power-zone definition and both exact DSF neck records survive, together with the earlier 84/91/94/100/150/215-edge contracts.

## Selected USB connectivity transactions

| Net | Physical result | Added tracks / adjacent microvias | Added track length, calculated |
|---|---|---:|---:|
| USB_CONN_DP | J1.A6/B6, U32.3 and U33.1 form one physical group | 13 / 12 | 18.2644 mm |
| USB_CONN_DM | J1.A7/B7, U32.5 and U33.2 form one physical group | 34 / 12 | 24.0728 mm |

Each net previously had four disconnected physical pad groups. Joining the duplicated connector contacts reduces opens by two; four local connector/protection/switch joins reduce another four. No ground or supply repairs are needed for this increment. The table gives aggregate added track length per branched net, not matched pin-to-pin electrical length or a USB skew measurement. Differential impedance, coupled routing, branch/stub lengths, skew, reference-plane continuity and ESD return behavior remain explicit unresolved layout holds. Downstream USB_D+/USB_D- and USB_DN_MCU/USB_DP_MCU remain disconnected. The data path is not complete or electrically qualified.

The [TI TS3USB31E Rev. A](https://www.ti.com/lit/ds/symlink/ts3usb31e.pdf) pin table identifies connector-facing D+ and D− on pins 3/5 and the other data ports on 2/6. The [TPD4E05U06 Rev. O](https://www.ti.com/lit/ds/symlink/tpd4e05u06.pdf) identifies D1+/D1− on 1/2 and ground on 3/8. The selected source retains the captured exact MPNs, pin maps and packages. TI requires matched, controlled USB routing and connector-local ESD protection; these connectivity probes do not establish compliance with those layout requirements. Package/land geometry is unchanged from the recorded library reviews.

The increment adds **47 tracks / 24 adjacent-layer microvias**, retaining all **17,472** items of the accepted 82-edge checkpoint. The resulting board has **483 footprints / 17,543 copper items**. Relative to the frozen 215-edge parent, it retains 15,398 nonzero source copper items and adds **1,425 tracks / 720 microvias**. The same 33 passive poses, five original zone definitions, four power parcels and two selected 0.12 mm supply necks remain unchanged. Ordinary tracks/default netclass and other-net clearance remain 0.20 mm; microvias remain 0.30/0.10 mm and minimum annulus 0.10 mm. No component move, new neck, source-copper retirement, current/protection setting, firmware or isolated enable-boundary change is selected.

## Validation and exploration

[Full DRC](led-routing-progress-76-drc-2026-10-27.json), [native checks](../../mechanical/review/routing-progress-76-native-check-2026-10-27.json), [orphan-restoration DRC](led-routing-progress-76-orphan-restoration-drc-2026-10-27.json), [remaining-net counts](../../mechanical/review/routing-progress-76-open-nets-2026-10-27.json) and [validation fingerprints](../../mechanical/review/routing-progress-76-validation-2026-10-27.json) record the selected result. Three stable refills preserve every earlier group and copper net; two independent replays yield byte-identical PCB/project/custom-rule files. PCB SHA-256: `febed76efdf661dadde856be3f621bffb226685a0755f980e52fa4a6a36f2d31`.

The complete wrapper passes **25 isolated native guards**, **256 LED checks**, canonical source/metadata checks and the independent 76-edge count. Restoring the three previously proved orphan vias preserves all selected groups and 76 opens, adding precisely three dangling-via warnings to the 104 intrinsic findings. Source-only CI passes **44 portable plan guards**, **21 canonical-source fault methods**, 14 distance tests, six path tests and seven clearance tests. New guards reject removal of accepted 82-edge copper, including coordinated candidate/plan retirement, and loss of its completed pad groups. Run `./tools/check-routing-progress.sh`.

Bounded ground-neck searches, including a 0.025 mm local lattice, do not produce another selected join. Original-width ground/control resistor and capacitor relocation screens likewise add no accepted pose. Straight original-width CC-pin escapes permit a candidate route, but its refill splits previously connected ground and application-supply groups; it is rejected. Excluding horizontal routing on the application-supply layer yields no accepted CC join. LED control searches and legal ordinary-width escape seeds also produce no selected reduction. None of these search bounds proves routing impossible. All unsuccessful boards, seed traces and exploratory scripts remain ignored local output.

## Remaining gates

GND still has nine opens, VLED eight, gauge supply three and each 3.3 V rail one. Display/LED controls, remaining row gates, feedback and other USB paths are unfinished. All four address nets and the C67/U48 ground join remain complete. The [historical 82-edge report](../../mechanical/review/routing-progress-82-open-nets-2026-10-26.json) retains the preceding per-net count.

The board remains unbuilt with the 104 intrinsic findings. Sixteen trial row pairs and two netless driver projections remain explicit unqualified canonical exceptions. C45 and SYS-distribution holds remain. Supply/bypass/return behavior, switching loops, current/voltage drop/transients/thermal behavior, USB/display timing and impedance, partial-power/interlock behavior, RF, enclosure fit and HDI/assembly process require engineering review and physical evidence. Independent Gate A remains mandatory before fabrication. No vendor PDFs, unsigned manufacturing files or local build output are released.
