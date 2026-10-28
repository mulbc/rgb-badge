<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0047: Scoped 0.12 mm digital-signal routing study

Date: 2026-10-23
Status: Exact USB_RAW_OUT2 inventory selected at 63 edges; other digital-width studies remain unselected.

## Context and source review

Original-width placement and routing probes reach a 122-edge candidate. Some remaining logic lands cannot accept a 0.20 mm centred escape with 0.20 mm other-net clearance. ADR 0043 records the DSF0006A geometry: 0.17 mm lands on 0.35 mm pitch give a calculated 0.165 mm trace-to-neighbour clearance for 0.20 mm copper, versus 0.205 mm for 0.12 mm copper. The intrinsic land gaps remain explicit existing DRC findings.

Rechecked 2026-10-23: [TI SN74LVC1G04 Rev. AF with DSF0006A drawing](https://www.ti.com/lit/ds/symlink/sn74lvc1g04.pdf), [the project package audit](../../hardware/coupon/rev-a/display-interlock-library-audit.md), and [JLCPCB capabilities](https://jlcpcb.com/capabilities/Capabilities). Published HDI 3 mil trace/space is smaller than 0.12 mm (4.72 mil). It supports a geometry study; it does not select or qualify a manufacturer, copper thickness, complete sequential-lamination stack, stencil or assembly process.

## Evaluated approach

The local candidate evaluated 0.12 mm added tracks on an explicit digital-control allowlist. Selection would require pinning that inventory and the enforcing native rules in replay evidence. Default routing remains 0.20 mm. Keep all power, ground, analogue current/reference/feedback/timer and USB differential/CC tracks at their original widths. Keep 0.20 mm other-net clearance, 0.30/0.10 mm adjacent-layer microvias and the 0.10 mm annular-width floor. No current-limit, value, net, pin map, protection or enable-domain change is allowed.

Set the study project's absolute track floor to 0.12 mm and add explicit native rules enforcing at least 0.20 mm on every non-allowlisted net. Independently verify every narrower integer track against the allowlist and require at most 120 mm aggregate added 0.12 mm copper per digital net. The separate sensitive-setting total remains 5 mm. Retain all earlier copper except the independently witnessed orphan-via inventory in ADR 0046. Preserve every accepted 150-edge physical pad group after refill and require exactly the same 104 intrinsic DRC findings. Pin the rules/profile and selected narrow-track inventory in replay evidence.

## Calculated screen and remaining review

Illustrative DC calculation, not a finished-copper specification or measured board result: copper resistivity 1.724e-8 ohm metre at 20 C, 0.12 mm width and an assumed 18 micrometre finished thickness give 0.798 ohm per 100 mm. At an illustrative 24 mA this is 19.2 mV and 0.460 mW per 100 mm at 20 C. This does not establish ampacity or bound output-current transients. The 24 mA example corresponds to the cited inverter's listed output-drive magnitude; it is not a new current setting or a guarantee for every component on the allowlist.

Longer routed digital traces still require actual stack/copper qualification, return-path and signal-integrity review, I2C rise-time checks, reset/boot timing, gate/interlock timing and physical validation. No completed electrical behavior, safety, fabrication approval or Gate A closure follows from fewer open edges.

## Selected outcome, 2026-10-25

The accepted 100-edge checkpoint selects no narrower tracks or reduced track floor. All added tracks remain 0.20 mm and the original 0.20 mm project floor remains enforced. Local narrower candidates are excluded from the selected PCB, plan and release evidence.

## 64-edge follow-up feasibility, 2026-10-28

The separately profiled signal-spacing screen of ADR 0058 makes no accepted join. Repeat this existing 0.12 mm digital-width study on the ignored ADR 0060 ground-rework board, preserving 0.20 mm clearance. Explicitly pin the new focus list and 120 mm per-net bound. Retain the two already selected exact ADR 0051 supply necks as unchanged exceptions; no other power/ground/setting/USB differential or CC copper may narrow. Source MPNs, pads, current limits and enable/protection boundaries stay fixed. Ground-retirement policy and the digital-width policy must both pass independently before any combined canonical selection. Existing accepted source remains 64 edges at its original ordinary width and clearance.

## Exact USB status candidate gate, 2026-10-28

The successful USB_RAW_OUT2 route is independently transferred to the unchanged accepted 64-edge copper. It needs none of the experimental ground retirements or smaller clearances. Select only its exact 13 × 0.12 mm tracks (13.21546 mm calculated total) and three 0.30/0.10 mm adjacent microvias after the full acceptance gate. Retain every 64-edge copper item, pose, group, zone, replacement and both supply necks. The native default floor remains 0.20 mm; an exact USB_RAW_OUT2-only width rule and an independent pinned copper catalog must reject every other narrow addition. Keep the 120 mm hard bound, original clearance and all current/enable/protection settings unchanged.

Rechecked TI TUSB320LAI Rev. D (https://www.ti.com/lit/ds/symlink/tusb320lai.pdf) and SN74LVC2G17 Rev. N (https://www.ti.com/lit/ds/symlink/sn74lvc2g17.pdf). U31.8 is the GPIO-mode open-drain OUT2 signal, U24.3 is the Schmitt input, and the unchanged R61 is a 10 kΩ pull-up to their USB-only 3.3 V supply. This route carries a logic status, not USB data/CC or charging power. No MPN, package, pin map, mode or resistance changes. Illustrative DC calculation with 18 µm copper at 20 °C gives about 0.1055 Ω for the new trace; the nominal 3.3 V / 10 kΩ pull-up case gives about 34.8 µV drop. This is not a finished-copper, noise/timing, partial-power or hardware-current qualification.

A native check caught one candidate via at 0.1953 mm clearance. Moving only new signal copper by (−0.050, +0.025) mm restores the full unchanged 104-finding baseline. The coarse via-footprint check assumed a 0.20 mm track and is corrected to account for the actual trial width; six host regressions include the previous failure. Independent native rules remain authoritative. Canonical selection still requires exact replay, frozen 64-edge preservation, native/physical 63 opens, unchanged orphan restoration, full fault/source/LED evidence and recorded engineering holds. No ground retirement or 0.15/0.18 mm spacing rule is selected.

## Selected outcome at 63 edges

The exact USB_RAW_OUT2-only inventory passes all required gates: 63 native/physical opens, unchanged 104 full findings, all frozen 64-edge copper/groups/poses, three stable refills, byte-identical regeneration, 43 native/87 portable faults, canonical/source/256 LED checks and unchanged three-orphan restoration. The [63-edge study](../development/led-routing-progress-63-study-2026-10-28.md) records hashes and review holds. No ADR 0058 spacing or ADR 0059/0060 ground retirement is selected. The 50-edge target and independent Gate A remain open.
