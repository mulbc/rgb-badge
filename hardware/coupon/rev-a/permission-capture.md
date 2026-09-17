<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Staged USB permission circuit capture

Date: 2026-09-16. Status: canonical KiCad source and host validation; [native KiCad ERC/XML/render review passed at 6d9a08b](../../../docs/development/permission-review-6d9a08b.md). This is a circuit increment, not completion of the power section or USB-current qualification.

## Subsequent integration

The [USB interface increment](usb-interface-capture.md) now connects the five detector outputs and supplies +3V3_USB from U29. #FLG04 is removed. The [logic-rail supervisor](usb-supervision-capture.md) now drives LOGIC_READY; four inputs and both actuator outputs remain staged. The ten-page counts and boundary description below record the reviewed `6d9a08b` checkpoint; current coupon totals are eleven pages, 443 items / 1,636 logical pins.

## What was connected at 6d9a08b

Two new sheets implement the stable-signal equations of ADR 0011 using real, numbered IC pins. `usb-conditioning.kicad_sch` provides five dual Schmitt buffers, ten default resistors, decoupling and ten input test pads. `usb-permission.kicad_sch` contains fourteen gates, decoupling, two output test pads and a pull-up for the raw open-drain logic output. Added population: **61 PCB items / 176 physical pins, including five explicit NCs**. Complete coupon source: **417 PCB items / 1,536 physical pins, on ten schematic pages**. Power flags are virtual source assumptions and are excluded from PCB counts.

The external raw inputs terminate at test pads. They are **not yet connected** to the Type-C detector, BC1.2 detector, supply supervisors, slide switch or controller GPIO. The two outputs similarly terminate at test pads; they are not charger or ILIM connections. There is no implicit connection between `USB_RAW_ESP_RUNNING` and the existing controller's `ESP_EN`.

| Boundary net suffix (`USB_RAW_…`) | Default resistor | Buffer pin → output pin | Conditioned net |
|---|---|---|---|
| OUT1 | R60, 10k to +3V3_USB | U24.1 → U24.6 | USB_OUT1 |
| OUT2 | R61, 10k to +3V3_USB | U24.3 → U24.4 | USB_OUT2 |
| CHG_AL_N | R62, 10k to +3V3_USB | U25.1 → U25.6 | USB_CHG_AL_N |
| CHG_DET | R63, 100k to GND | U25.3 → U25.4 | USB_CHG_DET |
| SW_OPEN | R64, 10k to +3V3_USB | U26.1 → U26.6 | USB_SW_OPEN |
| VBUS_VALID | R65, 100k to GND | U26.3 → U26.4 | USB_VBUS_VALID |
| LOGIC_READY | R66, 100k to GND | U27.1 → U27.6 | USB_LOGIC_READY |
| SWITCH_ON | R67, 100k to GND | U27.3 → U27.4 | USB_SWITCH_ON |
| ESP_RUNNING | R68, 100k to GND | U28.1 → U28.6 | USB_ESP_RUNNING |
| USB_REQUEST | R69, 100k to GND | U28.3 → U28.4 | USB_USB_REQUEST |

Each buffer is exact `SN74LVC2G17DBVR`. Its inputs accept slow transitions with hysteresis and tolerate up to 5.5 V under the stated operating conditions. Ordinary LVC gates have input transition-rate limits; routing RC/reset and resistor-pulled detector signals directly into them would leave that constraint unresolved. Conditioning all ten inputs keeps the captured logic interface consistent. Schmitt conditioning does not guarantee valid outputs during an invalid supply ramp.

U10 establishes attachment; U11–U16 establish a hardware-qualified high-current source. U17 combines both supply-valid inputs and attachment. U18 generates `USB_HIGH_REQ`. U19 recognizes the SDP/data condition, U20 combines application state and USB-stack grant, and U21 generates the low-current request. U22 combines high/low requests; U23 provides the inverted open-drain `USB_EN1_RAW_N` output. The application inputs reach only the low branch. Unattached or invalid-supply input states remove both requests in the stable-state model.

## Intentional unresolved boundaries

1. `#FLG04` is an explicit **draft +3V3_USB source assumption**, alongside the older coupon power flags. It does not represent a connected USB LDO. All nineteen new ICs have one local 100 nF / 16 V X7R capacitor; placement is still pending.
2. R70 pulls `USB_EN1_RAW_N` up to +3V3_USB solely to make the open-drain logic output reviewable. It is **not** the charger's mode-input pull-up and cannot satisfy ADR 0011's startup requirement. Actual charger EN1/EN2 need input-domain defaults and a separately qualified inhibition path.
3. `USB_HIGH_REQ` is a logical request, not a populated parallel ILIM switch. The boost switch, leakage/resistance proof and analog power sequencing remain pending. Application firmware has no route into HIGH in this captured logic.
4. The supervisor library remains uncaptured. Both valid signals must eventually come from hardware, with a reviewed release delay and a physical path that prevents startup/brownout glitches from reaching the charger. Neither default resistors nor Schmitt inputs replace that proof.
5. Raw CHG_DET must be bounded to the buffer's 5.5 V operating limit. Direct exposure to a faulty or unprotected USB input is not approved. The future connection to ESP_EN must account for R68 loading of the existing reset RC, rather than silently changing reset timing/thresholds.
6. Default resistors are selected for this staged interface, not a closed whole-port budget. Include their source-state currents, buffer input leakage, Ioff, non-rail input supply current, detector loads and the LDO in configured, unconfigured and suspend budgets. Do not substitute the buffers' 10 µA static ICC headline for a complete worst-case current budget.

## Source and verification

The added [TI SN74LVC2G17 datasheet](https://www.ti.com/lit/ds/symlink/sn74lvc2g17.pdf), SCES381N (2015-01), was downloaded on 2026-09-16 with SHA-256 `624dbe55679d2fed4123b0d7708cd0d295efcc78de395e71a0caf5cd13cbc216`. Its page-3 pin table, DBV6 outline/land drawings on PDF pages 30–31 and ordering table were checked. The shared footprint matches 4214840/G (08/2024), already audited for the AND3/supervisor. Physical pins are 1=1A, 2=GND, 3=2A, 4=2Y, 5=VCC, 6=1Y. This adds one exact symbol and no new footprint. Other IC sources and hashes are in the [permission-library audit](permission-library-audit.md).

`generate-coupon-permission.py --output NEW_DIRECTORY` deterministically regenerates both sheets and refuses an existing output directory. Canonical schematic files remain authoritative. `check-coupon-permission.py` independently traces their wires, compares caches to the controlled libraries, checks component/MPN/footprint/population metadata, rejects missing/orphan wiring and NCs, then evaluates the actual connected gates against the independent ADR 0011 contract for all **1,024** input states.

Fault tests prove that a firmware-to-HIGH route, bypassed supply-valid input, bypassed SDP data condition, bypassed application grant and loss of autonomous OFF charging fail the logic comparison. Separate source/XML mutations reject missed pins, wrong resistors, missing decoupling, wrong NCs and altered connections. The complete XML checker now includes every new component and pin instead of silently ignoring the added sheets. The synthetic exporter fixture remains test-only, never native evidence.

## Native checkpoint completed

Host validation on 2026-09-16: all **120** tests passed, including six new capture tests with multiple source, logic and XML fault cases. The canonical-source 1,024-case logic evaluation, controlled-library check, unchanged matrix/row/controller source checks and whitespace check passed. The strict USB-closure gate still exits 1, as required for the remaining uncaptured physical boundaries. No new native result or bench measurement is claimed.

Run `tools/check-kicad.sh` under KiCad 10.0.6. It must load/export **39 symbols**, **25 footprints per raw view**, produce the ten-page schematic PDF, pass the complete **417-item / 1,536-pin** XML check, and pass the unchanged strict staged ERC policy (only the old USB_D−/USB_D+ isolated-label pair is temporarily permitted). New warnings are not automatically exempted. Review both new sheets plus the Schmitt symbol and previously added permission-library exports. Also inspect the corrected DBV5/DBV6 fabrication outlines.

The source/logic checks do not prove native connectivity, rendered readability, transient behavior or hardware performance. Keep PR #8 draft, the strict USB-closure gate blocked, and fabrication behind Gate A.

The owner supplied the requested native exports at `6d9a08b`. ERC/XML and first-author rendered review passed; see the [evidence record](../../../docs/development/permission-review-6d9a08b.md). The instructions above describe that completed checkpoint, not a request to repeat it.
