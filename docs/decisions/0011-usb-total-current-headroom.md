<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0011: Reserve current for USB detection and permission logic

**2026-09-17 current-budget finding:** resistor ranges below include initial tolerance only. The [temperature-drift counterexample](../../hardware/coupon/rev-a/usb-supervision-capture.md) exceeds the configured-SDP allocation for an ordinary 100 ppm/K candidate. Precision-part qualification or revised lower limits are required before programming-resistor capture; no substitution or current increase is approved.


**2026-09-17 amendment:** [ADR 0012](0012-programming-resistor-error-budget.md) selects exact 0.1%, 25 ppm/K parts and retains the ±1% interval below as a total qualified resistance envelope. Assembly/service drift remains a qualification requirement; the nominal values and current ceilings are unchanged.

- Status: Accepted design correction for capture; physical implementation and Gate A pending
- Date: 2026-09-15
- Amends: [ADR 0010](0010-source-qualified-off-charging.md), charger mode selection only

## Finding

The BQ24074 USB500 setting is specified as 450/475/500 mA minimum/typical/maximum into its IN pin. It does not limit detector, LDO, pull-up or status loads connected directly to VBUS. Selecting that mode for a configured 500 mA USB port leaves zero guaranteed headroom for those additional loads. Using the typical 475 mA value would conceal the issue. Even 1 microampere outside the charger breaks the worst-case 500 mA calculation.

The first-author native reviews accepted library transcriptions and the previously captured matrix/controller circuit. They did not approve this uncaptured power topology. The strict USB-closure gate remains blocked.

## Decision

Retain the selected BQ24074, BQ24392, TUSB320LAI and TS3USB31E. Replace normal USB500 operation with a lower resistor-programmed input limit. Keep BQ24074 EN2 high; select standby or external ILIM using EN1. A separate, hardware-only switch controls a parallel ILIM resistor. Firmware may request the low setting after valid USB configuration; it has no connection to the resistor-boost control.

- Base ILIM resistor: 3.65 kohm, 1%, permanently from ILIM to VSS.
- Boost branch: 3.48 kohm, 1%, in series with a normally-off switch to VSS. Only qualified source hardware may enable it.
- The ideal enabled resistance is 1.78149 kohm. This slightly lowers the previous 1.78 kohm setting's maximum; it does not increase authorized source or charge current.
- Keep the provisional 1.13 kohm ISET network and its exact-pack prerequisite unchanged.
- Do not populate the fixed USB100/USB500 mode-control paths in normal operation.

| Product state | EN2 | EN1 | Boost branch | Charger IN current calculation |
|---|---:|---:|---|---|
| Attached, not permitted / reset / SDP suspended | 1 | 1 | Off | Standby; separate standby/auxiliary budget applies |
| ON, configured and unsuspended SDP | 1 | 0 | Off | 0.361–0.476 A; 0.418 A typical-factor calculation |
| Hardware-qualified charging source or Type-C 1.5/3 A | 1 | 0 | On | 0.834–0.975 A; 0.904 A typical-factor calculation; ideal switch |
| No VBUS | Not evaluated | Not evaluated | Off | Charger input asleep |

The low calculation uses TI's **200–500 mA** KILIM factors 1330/1525/1720 A-ohm. The high calculation uses the **500 mA–1.5 A** factors 1500/1610/1720 A-ohm. Both include opposite 1% resistor tolerances. Do not use the high-range minimum factor for the low branch.

Allocate at most 20 mA to configured-state auxiliary VBUS loads and 2 mA to adverse programming-network effects. Together with the ideal low-branch maximum, this totals approximately 497.993 mA. These are design allocations, not measured or guaranteed load totals. Actual upper bounds must fit them before closure. The allocations do not apply to unconfigured or suspended operation; those require their own substantially smaller budget. Detector current figures printed only as typical values cannot establish worst-case compliance.

## Detector-to-control contract

TUSB320LAI is fixed UFP, GPIO mode. OUT1/OUT2 = 11 means unattached; 10 means attached default current; 01 means 1.5 A; 00 means 3 A. Thus OUT1 low qualifies the Type-C high-current branch, while either output low establishes attachment after the detector is operating normally.

BQ24392 CHG_DET alone is insufficient: require CHG_AL_N low **and** CHG_DET high for its high-current permission. For an SDP request, additionally require CHG_DET low and SW_OPEN low. A low-current non-data charger also produces CHG_AL_N low / CHG_DET low, but SW_OPEN remains high; it must not inherit a stale SDP request. GOOD_BAT remains high with valid VBUS as required by ADR 0010.

Use the following stable-signal equations. A released open-drain signal resolves high only with its correct-domain pull-up:

- `READY = VBUS_VALID AND LOGIC_READY`
- `ATTACHED = NOT (OUT1 AND OUT2)`
- `BC_HIGH = NOT CHG_AL_N AND CHG_DET`
- `HIGH = READY AND ATTACHED AND (NOT OUT1 OR BC_HIGH)`
- `SDP = NOT CHG_AL_N AND NOT CHG_DET AND NOT SW_OPEN`
- `LOW = READY AND ATTACHED AND SDP AND SWITCH_ON AND ESP_RUNNING AND USB_REQUEST`
- `BOOST = HIGH`
- `EN2 = 1`, `EN1 = NOT (HIGH OR LOW)` while the input domain is valid.

Hardware HIGH wins by enabling the boost branch regardless of application state. Firmware changes can only affect EN1 through LOW. The USB stack must clear USB_REQUEST on reset, detach and suspend; hardware also removes LOW on application OFF/reset, missing attachment or invalid detector supply. This does not make faulty firmware USB-compliant before configuration: the validated USB stack is still responsible for its grant.

## Physical circuit requirements for the next capture

1. EN2 and released EN1 must stay high while charger IN is valid, including the interval before the 3.3 V detection rail starts. A pull-up to an unpowered LDO output does not prove this. Select and verify the protected input-domain pull-ups and open-drain sink path against BQ24074's 1.4 V VIH, 0.4 V VIL and control-pin voltage limits.
2. LOGIC_READY must be implemented by a qualified hardware supply/reset condition. It is not a firmware flag or an assumption that every IC initializes simultaneously. Prevent the boost switch and EN1 sink from turning on during ramp, brownout and detector reset.
3. BQ24392 CHG_DET is a VBUS-level push-pull output; it must not be tied to an ordinary unprotected 3.3 V input. Audit voltage tolerance or level translation. Keep detector pull-ups out of the switched application domain and prevent backfeed into either unpowered rail.
4. The normally-off boost switch must have bounded off leakage and on resistance at the actual logic voltage and temperature. Positive on resistance lowers the ideal high limit; leakage into the nominally off branch can raise the low limit. The 2 mA allocation is not proof of either effect. Do not assume the existing row MOSFET is suitable from its threshold voltage alone.
5. Audit changes of HIGH while LOW is asserted. Returning from a high advertisement must remove the resistor branch promptly; steady-state Boolean tests do not bound switch turn-off time, rail capacitance or charger response. Leave required transition timing open until a real circuit and source specification are checked.
6. Sum every path drawing VBUS: charger IN, BQ24392, Type-C detector, LDO quiescent current, logic, pull-ups, status indicators, programming-switch errors and protection leakage. Resolve unconfigured/suspend current, inrush, and USB data backfeed separately.

Exact additional gate, supervisor, switch and resistor MPNs remain subject to source/package audit before KiCad capture. This ADR freezes the corrected contract and nominal resistor values, not an orderable BOM or fabricated circuit.

## Verification

`check-usb-permission.py` exhausts 1,024 resolved GPIO/power/request combinations. Tests cross-check manufacturer GPIO states against the product policy, reject unresolved inputs, and exercise stale requests, malformed BC1.2 status, attachment loss, application reset and Type-C advertisement reduction. Every application input is toggled to verify that none can change BOOST.

`check-power-design.py` retains the rejected USB500 budget counterexample, computes both ILIM factor ranges, checks resistor corners and confirms that the new ideal high ceiling does not exceed the old one. The strict USB-closure gate still fails. Native library review at c054cb4 remains valid because no symbol, footprint or schematic changed in this correction.

Host validation on 2026-09-15: 38 power-design/library tests, 13 new GPIO/budget tests and 17 shell-wrapper tests passed (68 total). The wrapper tests use a CLI stub, not KiCad. The standalone GPIO checker passed its 1,024 combinations, `git diff --check` passed, and `check-power-design.py --require-usb-closure` returned 1 for the remaining documented blockers. No new native run or bench measurement is claimed.

## Sources checked 2026-09-15

- [TI BQ2407x SLUS810N](https://www.ti.com/lit/ds/symlink/bq24074.pdf), Table 7-2, electrical characteristics IINmax/KILIM and EN logic levels, and section 9.3.4.1.
- [TI BQ24392 SLIS146G](https://www.ti.com/lit/ds/symlink/bq24392.pdf), pin functions and Tables 1–2; distinguishes CHG_AL_N, CHG_DET and SW_OPEN.
- [TI TUSB320LAI SLLSEQ8D](https://www.ti.com/lit/ds/symlink/tusb320lai.pdf), GPIO Table 3 and supply/control-pin limits.
