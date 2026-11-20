<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Routing continuation: 65 to 64 unconnected edges

Date: 2026-10-28. Unbuilt, unqualified source study; no hardware measurements or fabrication release. The 50-edge target remains open.

Native and independent physical-pad opens decrease **65 → 64**, retaining exactly **104 unchanged intrinsic DRC findings**. U39.6 on TEMP_OK now joins U40.1/R91.2. U39.4 remains open. Every accepted 65-edge copper item, physical pad group, 34 R/C poses and four test-land poses survives. The [65-edge integer plan](../../mechanical/review/routing-progress-65-checkpoint.json) freezes commit 67b69f2, including all previous exceptions.

## Exact transaction

Under [ADR 0053](../decisions/0053-enumerated-local-track-replacements.md), replace one original COL_02_R In4 segment, (77.9, 14.75)–(51.95, 14.75) mm. Its replacement calculates to 26.85 mm versus 25.95 mm. The [six-entry catalog](../../mechanical/review/routing-progress-track-replacements.json), SHA-256 `0f69fa50a68a19a2b897013b04a9986068c09c09694f518c344965e5a049dec4`, independently preserves all four direct source contacts on their original layer, bringing the catalog total to 27 contacts. No whole-chain or internal-vertex exception is selected.

The temperature connection adds a calculated 35.24147 mm of 0.20 mm trace. Its initial escape uses adjacent microvias at (56.935, 14.75) mm. The subsequent route avoids horizontal signal runs on the USB supply plane. Two application-supply bridges restore every old supply group after refill: a 1.0 mm In3 bridge between (34.868115, 11.899991) and (34.868115, 12.899991) mm, and a 1.2 mm B bridge between (41.055028, 15.284782) and (39.855028, 15.284782) mm. Each bridge uses two unchanged adjacent microvias. These restore prior connections; they do not establish a current rating.

An earlier bridge near (40.277891, 8.705954) mm failed the separate orphan-restoration gate by contacting a retired source-via site. It is excluded. The selected bridge passes the unchanged restoration requirement: all three restored vias remain dangling, with no other DRC or group difference.

Relative to the frozen 215-edge source, the board retains 15,392 nonzero copper items and adds **1,758 tracks / 834 microvias**. It contains **483 footprints / 17,984 copper items**. This transaction adds 98 tracks and 12 microvias while replacing one original track. The three orphan retirements, 116 neutral zero-length cleanups, five original zones, four selected parcels and two exact DSF necks remain unchanged. Ordinary track/clearance remains 0.20 mm; microvias remain 0.30/0.10 mm with a 0.10 mm annular floor. No component pose, exact MPN, footprint, pin/net assignment, current/protection/enable setting or firmware changes.

## Validation

[Full DRC](led-routing-progress-64-drc-2026-10-28.json), [native checks](../../mechanical/review/routing-progress-64-native-check-2026-10-28.json), [orphan-restoration DRC](led-routing-progress-64-orphan-restoration-drc-2026-10-28.json), [remaining-net counts](../../mechanical/review/routing-progress-64-open-nets-2026-10-28.json) and [validation fingerprints](../../mechanical/review/routing-progress-64-validation-2026-10-28.json) record the selected source. Three stable refills and two byte-identical PCB/project/custom-rule replays pass. Board SHA-256: `5b67c6618d8bbf1c945492c2c2ab96cf722edf7475799f2689d14be317c769ae`.

The gate passes **39 isolated native guards / 75 portable plan guards**, canonical metadata and **256 LED checks**. Source-only CI also passes 21 canonical faults, 14 distance tests, six path tests and seven clearance tests. New guards freeze the 65-edge copper/groups, component/test-land poses and earlier replacements; two native faults bypass catalog matching and independently reject omitted source contacts or a detached endpoint in the new temperature escape replacement. All prior source-contact and original-zone checks remain enforced.

## Excluded screens and remaining work

The joint R47/TP4 screen under [ADR 0055](../decisions/0055-localize-isolated-test-lands.md) produces no complete reconnection. The rear VLED rectangles/notches under [ADR 0056](../decisions/0056-bounded-rear-vled-distribution-study.md) either split ground or make no supply join; no new parcel is selected. The coordinated exchange screens under [ADR 0057](../decisions/0057-coordinated-colour-chain-fanout-study.md) make no selected connection. Native clock seeds retain an enclosed reachable pocket; additional row-select detours split earlier groups and remain excluded. The second temperature-output escape and subsequent U39 supply screen make no further accepted join. Finite searches do not prove routing impossible. Vendor PDFs, downloaded routing binaries, exchange files and failed probes remain outside Git.

The 50-edge target is unfinished. GND retains five opens, VLED eight, gauge supply three, plus incomplete controls, analogue settings, feedback, USB and converter paths. Temperature-inhibit latency/noise/return, supply voltage drop/current/thermal behavior, bypassing, timing/impedance, RF, probe/assembly/mechanical access and HDI process qualification remain open. The existing intrinsic findings, trial-package and C45/SYS holds remain. Independent Gate A is mandatory before fabrication; this source commit is not a manufacturing release.
