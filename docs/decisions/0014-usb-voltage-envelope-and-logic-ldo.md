<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0014: Correct the USB voltage envelope and widen logic-supply headroom

- Status: engineering decision implemented in the draft; native U29 review accepted at bad43fa; input-stage qualification pending
- Date: 2026-09-19
- Retains: ADR 0013 source-current policy, OFF charging, fixed current ceilings and independent Gate A
- Changes: USB-only U29 regulator and its enable connection; no change to the application regulator

## Evidence and decision

USB Type-C Release 2.5, section 4.4.2, explicitly allows 5.5 V at light loads. The earlier 4.8–5.25 V staged supply annotation was an assumption, not an adequate full-port design envelope. Use 5.5 V as the normal upper source boundary; derive the lower connector voltage separately from cable loss and current. Do not confuse the charging qualification threshold with the USB detach threshold.

The current TLV75533 input operating maximum is 5.5 V. That leaves no positive operating margin between the normal-source ceiling and an external overvoltage trip threshold. A nominal clamp value alone is insufficient. Select `TPS70933DBVR` for the USB-only logic supply to remove that narrow input-voltage constraint. This is an explicit draft substitution, not a procurement release. The TPS709A/B pinout variants are not interchangeable.

TPS709 accepts 2.7–30 V at IN, but this does NOT make the complete protected rail 30-V tolerant. Leave EN intentionally unconnected, as TI specifies for always-enabled operation; do not reproduce the former EN-to-IN wire. Reuse the independently compared DBV0005A footprint. Keep C30/C31 and C32 provisionally; output stability requires 1.5–47 µF effective capacitance for the 3.3 V variant and ESR within 0–0.2 ohm. C32 bias/temperature/aging qualification remains open. Output accuracy and start/stop behavior must be evaluated for this regulator, not inherited from TLV755.

No input-protection IC is selected by this ADR. `TPS259474ARPWR` is a candidate because protection and power-good could share one IC. Its DC threshold screening does not establish transient protection. Existing U34 and all other protected-rail components still constrain the complete rail. Charger mode-pin control remains separate work.

## Implementation and review scope

One new project-local symbol, no new footprint and no additional placed component. U29 changes MPN; pin 3 becomes an explicit intentional no-connect. Complete circuit remains 396 items / 1,492 logical pins, with one additional no-connect replacing one connected pin. Libraries become 47 symbols / 27 footprints.

The generator, independent expected source map and independently transcribed synthetic netlist all encode the changed enable connection. A fault test reconnecting EN to the input rail must fail. Batch the native U29 review with the next functional input-stage checkpoint; do not request a separate owner run solely for this substitution.

## Sources

- [USB-IF Type-C Release 2.5](https://www.usb.org/document-library/usb-type-cr-cable-and-connector-specification-release-25), section 4.4.2; downloaded PDF SHA-256 `6636cd61387a2f78b0fa96c8ea86ccc0f39ec59f98821cdb57b206d31445a328`.
- [TI TLV755P SBVS320D](https://www.ti.com/lit/ds/symlink/tlv755p.pdf), recommended conditions.
- [TI TPS709 SBVS186H](https://www.ti.com/lit/ds/symlink/tps709.pdf), sections 5, 6, 7.4 and 8.2.2.1; [library audit](../../hardware/coupon/rev-a/usb-input-protection-screening.md).
