<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0018: Complete power architecture proposal

- Date: 2026-10-05
- Status: **Proposed for engineering review; not accepted for electrical capture**
- Baseline: `0764245`, `coupon-power-rev-a`
- Scope: USB protection/permission, charger, protected pack, physical OFF, gauge, application and LED supplies
- Retains: ADRs 0013–0017 product policy, current ceilings, NTC/timer safeguards and independent Gate A

## Recommendation

Use one protected USB domain for detection and a second reverse-blocking power switch for charger permission. Keep the BQ24074 in fixed external-current mode behind that switch. Retain the switched MAX17048 and isolate its I²C segment with a dual-supply buffer, with the gauge on the low-offset A side. Reduce the proposed charge setting to approximately 357 mA nominal / 396 mA maximum, conditional on the eventual exact pack. Keep the two existing buck-boost converters and add a hardware display-arm/reset boundary.

The [complete proposal](../design/power-architecture-2026-10-05.md) is the review artifact. It gives a connected block topology, operating/transition states, calculations, alternatives, capture holds and validation plan. The topology intentionally spends an additional USB power-switch footprint to avoid exposing the detector rail directly to connector faults and avoid making BQ24074 mode-pin startup the source-permission mechanism. This is a proposed trade-off, not a claim of lower part count.

## Consequences and acceptance boundary

The proposed second input switch and gauge buffer are material changes. No canonical schematic, BOM, pin map or accepted current setting changes in this proposal. The [requirements addendum](../requirements.md#power-architecture-proposal-verification-addendum) records the checks that must be incorporated before implementation; it does not silently supersede the existing accepted requirements.

If accepted for capture, amend ADR 0013's physical standby implementation to permit an electrically disconnected charger input, amend ADR 0015's direct gauge bus to the buffered connection, and supersede ADR 0012's 1.13 kΩ ISET population with an exact audited lower-current part. The gauge remains physically off and post-ON SOC remains provisional. All proposed new part libraries need manufacturer pin/package audit.

The owner confirmed on 2026-10-05 that no battery supplier reply or alternate pack selection is available. Pack-specific charge voltage/current, NTC, timer, connector and minimum capacity therefore remain real dependencies. Do not label the proposal electrically closed or fabricate from it.

2026-10-06 placement follow-on: the [tight VLED XY trial](../../mechanical/dual-row-package-screen-2026-10-06.md) fits its converter cluster and all sixteen proposed row-package boxes when the `INA232AIDDFR` current-monitor IC box is omitted from that deterministic first-fit pass. [ADR 0021](0021-external-battery-current-measurement.md) independently accepts external inline battery-current measurement and removes the on-board monitor/shunt from capture, without changing current or charger safeguards. A complete routed-board fit is still unproven.

2026-10-07 current-coordinate follow-on: [proposed ADR 0022](0022-lower-fixed-usb-input-limit-proposal.md) screens dropping the 3.48 kΩ parallel ILIM branch and using the existing 3.65 kΩ resistor alone. This would lower the calculated charger input maximum from 0.975 A to 0.476 A and remove the present DC overlap with a published eFuse breaker test point. It does not select a new circuit or close input transient, permission, pack or thermal holds.

2026-10-07 permission follow-on: the [charger pin-boundary review](../design/charger-permission-boundary-2026-10-07.md) states the proposed E1/AUP/supervisor connections and default-off source states together. It identifies BQ24074 `EN2` sourcing, fault voltage and timing as the immediate unresolved pin-level connection. The existing permission test outputs remain disconnected from charger control.

## Review disposition required

Resolve the six numbered capture holds in the proposal as one engineering review. In particular, do not approve a Boolean permission table as evidence of analog startup behavior, or the buffer's power-up sequencing statement as a numerical bound on power-down injection. A simpler replacement is welcome if it satisfies the same source, OFF and transient contracts with traceable evidence.
