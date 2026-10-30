<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Routing continuation: 69 to 65 unconnected edges

Date: 2026-10-28. Unbuilt, unqualified source study; no hardware measurements or fabrication release. The 50-edge target remains open.

Native and independently counted physical-pad opens decrease **69 → 65** with exactly **104 unchanged intrinsic DRC findings**. Four previously isolated 1.0 mm digital/control test lands move beside their existing signals, each using one short 0.20 mm back-layer lead under [ADR 0055](../decisions/0055-localize-isolated-test-lands.md). All accepted 69-edge copper, completed groups, 34 R/C poses and earlier routing exceptions survive. The [69-edge integer plan](../../mechanical/review/routing-progress-69-checkpoint.json) freezes commit 9015215.

## Exact test-land changes

The [catalog](../../mechanical/review/routing-progress-testpad-placements.json) pins each original/selected integer pose, unchanged 180° orientation, numbered net, lead and joined source-pad witness. No land, mask/paste/layer attribute, footprint, part field, pin number or net changes. No manufacturer part is substituted: these existing PCB copper features retain their exact captured fields.

| Land / net | Old centre, mm | Selected centre, mm | Added lead, calculated |
|---|---|---|---:|
| TP1 / LED_SOUT | (74.001262, 1.000001) | (8.395, 30.795) | 2.095 mm |
| TP2 / ESP_EN | (84.501262, 10.500001) | (42.150, 14.590) | 1.545 mm |
| TP11 / SYS_I2C_SDA | (76.001262, 1.000001) | (44.250, 11.795) | 1.44638 mm |
| TP20 / USB_RAW_OUT1 | (86.501262, 10.500001) | (24.725, 29.815) | 1.545 mm |

SYS_I2C_SDA and USB_RAW_OUT1 now form single physical pad groups. LED_SOUT and ESP_EN each retain one other open. The independent verifier proves each selected land was isolated in the original source, remained isolated through 69 edges, and touched no accepted 69-edge nonzero copper. It also requires the exact short lead and joined source witness, retains all previous copper, and independently checks a real completed pad group. Moving an airwire label, deleting a land or changing a net cannot satisfy these checks.

The transaction adds **four tracks / no vias** and moves **four test lands**, separately from the unchanged **34 R/C poses**. The board contains **483 footprints / 17,875 copper items**, retains **15,393 nonzero source items**, and adds **1,660 tracks / 822 microvias** relative to the frozen 215-edge source. The same five original-track replacements, 23 direct-contact witnesses, three proved orphan-via retirements, 116 neutral zero-length cleanups, five original zones, four parcels and two exact DSF necks remain unchanged. Ordinary track/clearance is 0.20 mm; microvias are 0.30/0.10 mm, minimum annulus 0.10 mm, and only the two existing supply necks use 0.12 mm. Current/protection/enable settings, firmware, ICs, inductors and other component placements remain unchanged.

## Validation

[Full DRC](led-routing-progress-65-drc-2026-10-28.json), [native checks](../../mechanical/review/routing-progress-65-native-check-2026-10-28.json), [orphan-restoration DRC](led-routing-progress-65-orphan-restoration-drc-2026-10-28.json), [remaining-net counts](../../mechanical/review/routing-progress-65-open-nets-2026-10-28.json) and [validation fingerprints](../../mechanical/review/routing-progress-65-validation-2026-10-28.json) record the accepted source. Three stable refills and two byte-identical PCB/project/custom-rule replays pass. Board SHA-256: `a6a458a697d769ebba7c555f44d31dbe2c0945803847999e88116a399eb009e1`.

The complete gate passes **37 isolated native guards / 69 portable plan guards**, canonical metadata and **256 LED checks**. Source-only CI also passes 21 canonical fault methods, 14 distance tests, six path tests and seven clearance tests. New fault cases reject omitted/changed test-land metadata, unselected moves, land-size changes and coordinated lead removal. Independent native cases inject prior copper contact or bypass the catalog while leaving a land disconnected: both must fail. Restoring the same three orphan vias preserves all groups and 65 opens, adding only the expected three dangling-via findings. Run `./tools/check-routing-progress.sh`.

## Search-tool correction and excluded experiments

A native regression reproduced a search-boundary omission. The grid starts at y = 0.70 mm and ends at 31.80 mm, but valid existing lands can sit at 0.65/31.85 mm. The tool prematurely discarded those anchors before testing its existing 0.60 mm lead-probe reach. The correction admits only anchors within that same reach; candidate grid coordinates and native lead/via clearances remain checked. A two-net fixture retains two opens [before](../../mechanical/review/native-route-edge-endpoint-before-2026-10-28.json) and reaches zero [after](../../mechanical/review/native-route-edge-endpoint-after-2026-10-28.json), using identical source bytes, unchanged pads/ground copper and byte-identical replay. This is a synthetic fixture, not a zero-open coupon. Run `tools/test-native-route-edge-endpoints.py` with KiCad's Python. Six host path tests and fourteen distance tests pass.

Ignored 0.12 mm digital-control studies, including deeper two-million-node searches, do not produce another accepted board. A 95.6987 mm ROW_ENABLE_N_CANDIDATE route is below the prior 120 mm feasibility bound, but refill splits application and USB supply groups; attempted local bridges do not restore them all. Layer-locality restrictions likewise yield no accepted reduction. No broad digital-width exception, source rule relaxation or failed seed enters the selected source. Finite exhausted/bounded searches do not prove routing impossible.

Finer 0.10 mm placement screens find legal courtyard poses for TP4/TP13/TP14, but no completed short connection. These lands remain fixed. The manufacturer PDFs, routing exchange files, downloaded router and failed probes stay outside Git.

## Remaining engineering gates

The 50-edge target is unfinished. GND has five opens, VLED eight, gauge supply three, and remaining controls, analogue settings, feedback, USB and converter paths are incomplete. Probe access, enclosure exposure, fixture/assembly access, stub loading and signal quality require review at the new test locations. The board remains unbuilt with its intrinsic findings, trial-package exceptions and C45/SYS-distribution holds. Electrical, bypass/return, current/thermal, switching-loop, timing/impedance, interlock/partial-power, RF, mechanical and HDI/assembly qualification remain open. Independent Gate A is mandatory before fabrication; this source commit is not a manufacturing release.
