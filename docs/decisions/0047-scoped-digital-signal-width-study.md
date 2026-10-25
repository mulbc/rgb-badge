<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0047: Scoped 0.12 mm digital-signal routing study

Date: 2026-10-23
Status: Evaluated locally; not selected in the 100-edge checkpoint.

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
