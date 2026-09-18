#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Check the selected arithmetic and safety boundaries for Coupon Rev A power capture.

This is a deterministic design calculation, not a simulation, native KiCad ERC,
USB compliance test, battery qualification, thermal result, or fabrication approval.
"""

import argparse
from decimal import Decimal as D
from pathlib import Path
import runpy
import sys

PRECISION=runpy.run_path(str(Path(__file__).with_name('check-programming-resistors.py')))


def bounded_ratio(constant_min, constant_max, resistance, tolerance):
    """Return minimum/midpoint/maximum current for I = K/R.

    The midpoint is not necessarily the manufacturer's typical value.
    """
    k_min, k_max = D(constant_min), D(constant_max)
    resistor, tol = D(resistance), D(tolerance)
    return (
        k_min / (resistor * (D(1) + tol)),
        ((k_min + k_max) / D(2)) / resistor,
        k_max / (resistor * (D(1) - tol)),
    )


def parallel(a, b):
    a, b = D(a), D(b)
    return a * b / (a + b)


def divider(vfb, upper, lower):
    return D(vfb) * (D(1) + D(upper) / D(lower))


def validate_bq_unknown_input(resistance, source_limit, *, classification="unknown"):
    """Preserve the rejected BQ25616J calculation for regression history.

    SLUSDF7A sections 7 and 9.3.5: nominal setting must be 0.5--3.2 A.
    KILIM min/typ/max is 459/478/500 A-ohm. Only unknown-adapter mode
    uses this resistor; its bounds do not apply to BC1.2-classified sources.
    """
    resistance, source_limit = D(resistance), D(source_limit)
    if resistance <= 0 or source_limit <= 0:
        raise ValueError("Resistance and permitted source current must be positive")
    if classification != "unknown":
        raise ValueError("ILIM resistor does not bound a BC1.2-classified source")
    nominal = D("478") / resistance
    if not D("0.5") <= nominal <= D("3.2"):
        raise ValueError("Nominal ILIM setting is outside the documented 0.5--3.2 A range")
    low, _, high = bounded_ratio("459", "500", resistance, "0.01")
    if high > source_limit:
        raise ValueError("Worst-case ILIM exceeds the permitted source current")
    return low, nominal, high


def actuator_supply_screen(*, local_drop_v="0", fall_slew_v_per_us="0",
                           response_us="0"):
    """Conditional voltage margins, NOT a qualified transient or timing model.

    BQ24074 SLUS810N §8.5: UVLO rising 3.2–3.4 V, hysteresis
    0.2–0.3 V. ADG4612 Rev.0 Table5: VDD minimum 2.7 V;
    Table3: the 17-ohm maximum is characterized at VDD=4.5 V.
    All inputs are assumed bounds to explore, not measured design values.
    """
    drop, slew, delay = map(D, (local_drop_v, fall_slew_v_per_us, response_us))
    if any(not x.is_finite() or x < 0 for x in (drop, slew, delay)):
        raise ValueError("Supply-screen bounds must be finite and nonnegative")
    earliest_rise = D("3.2")
    lowest_fall = earliest_rise - D("0.3")
    loss = drop + slew * delay
    return {
        "charger_rise_min_v": earliest_rise,
        "charger_fall_min_v": lowest_fall,
        "rise_static_margin_v": earliest_rise - drop - D("2.7"),
        "fall_remaining_margin_v": lowest_fall - D("2.7") - loss,
        "ron_supply_gap_at_fall_v": D("4.5") - lowest_fall,
    }


def usb_capture_blockers():
    """Selected topology tasks not yet closed by calculation alone."""
    return (
        "Exact BQ24074RGTR, BQ24392RSER and TS3USB31ERSER libraries passed native review at c054cb4; the charger/power path remains uncaptured.",
        "ADR 0011 logic, USB detectors/data path and USB LDO are captured; protected input, VBUS qualification, hardware-only ILIM boost and physical startup inhibition remain uncaptured.",
        "The detector/LDO/logic/status auxiliary-current budget and source transitions are not validated. Shared-rail actuator UVLO arithmetic is conditional, not startup/brownout closure.",
        "ADR 0012 selects precision programming resistors and retains ±1% total error; their assembly/service drift allocation and actuator leakage still require qualification. The historical 100-ppm/K temperature counterexample remains rejected.",
        "The exact pack, NTC/timer network and BQ24074 linear thermal behavior remain unqualified.",
    )


TYPE_C_STATES = frozenset(("none", "default", "1.5A", "3A"))
BC12_STATES = frozenset(("none", "SDP", "CDP", "DCP", "dedicated", "unclassified"))
HIGH_TYPE_C = frozenset(("1.5A", "3A"))
HIGH_BC12 = frozenset(("CDP", "DCP", "dedicated"))


def selected_usb_state(*, switch_on, type_c, bc12, configured=False, suspended=False):
    """Resolve ADR 0010 policy with ADR 0011's current-budget correction.

    This proves the intended truth table, not transistor/gate implementation,
    USB compliance, detector accuracy, or firmware behavior.
    """
    if not isinstance(switch_on, bool) or not isinstance(configured, bool) or not isinstance(suspended, bool):
        raise ValueError("Switch, configured and suspended inputs must be booleans")
    if type_c not in TYPE_C_STATES:
        raise ValueError(f"Unsupported Type-C state: {type_c}")
    if bc12 not in BC12_STATES:
        raise ValueError(f"Unsupported BC1.2 state: {bc12}")
    if type_c == "none":
        if bc12 != "none" or configured or suspended:
            raise ValueError("USB protocol state cannot exist without an attached source")
        return {"mode": "input-asleep", "en2": None, "en1": None,
                "data_connected": False, "permission": "none",
                "good_bat": False, "app_data_isolator_powered": switch_on}

    data_connected = switch_on and bc12 in ("SDP", "CDP")
    if type_c in HIGH_TYPE_C:
        return {"mode": "external-ilim", "en2": 1, "en1": 0,
                "data_connected": data_connected, "permission": "type-c-hardware",
                "good_bat": True, "app_data_isolator_powered": switch_on}
    if bc12 in HIGH_BC12:
        return {"mode": "external-ilim", "en2": 1, "en1": 0,
                "data_connected": data_connected, "permission": "bc1.2-hardware",
                "good_bat": True, "app_data_isolator_powered": switch_on}
    if switch_on and bc12 == "SDP" and configured and not suspended:
        return {"mode": "external-low", "en2": 1, "en1": 0,
                "data_connected": True, "permission": "usb-stack",
                "good_bat": True, "app_data_isolator_powered": True}
    return {"mode": "standby", "en2": 1, "en1": 1,
            "data_connected": data_connected, "permission": "none",
            "good_bat": True, "app_data_isolator_powered": switch_on}


def selected_input_bounds(*, boost=False, switch_resistance_max="0"):
    """Ideal-switch resistor limits, optionally including ON resistance.

    Switch leakage, transient effects and auxiliary loads are NOT included.
    Exact switch qualification must bound those before circuit closure.
    """
    if type(boost) is not bool:
        raise ValueError("boost must be a boolean")
    ron = D(switch_resistance_max)
    if not ron.is_finite() or ron < 0:
        raise ValueError("Switch resistance must be finite and nonnegative")
    # ADR 0012: total qualified resistance envelope, not initial tolerance.
    base, branch, tolerance = D("3650"), D("3480"), PRECISION['TOTAL_ERROR']
    if not boost:
        low, _, high = bounded_ratio("1330", "1720", str(base), str(tolerance))
        return low, D("1525") / base, high
    r_min = parallel(base * (1 - tolerance), branch * (1 - tolerance))
    r_max = parallel(base * (1 + tolerance), branch * (1 + tolerance) + ron)
    # Only use TI's 500 mA--1.5 A factor row while the whole result stays there.
    if D("1500") / r_max < D("0.5"):
        raise ValueError("Switch resistance moves the high branch outside the factor range")
    return D("1500") / r_max, D("1610") / parallel(base, branch), D("1720") / r_min


def total_usb_current(charger_max, auxiliary_max, programming_allowance="0"):
    values = tuple(map(D, (charger_max, auxiliary_max, programming_allowance)))
    if any(not v.is_finite() or v < 0 for v in values):
        raise ValueError("Current budgets must be finite and nonnegative")
    return sum(values)


def results():
    charge_low, _, charge_high = bounded_ratio("797", "975", "1130", PRECISION['TOTAL_ERROR'])
    charge = (charge_low, D("890") / D("1130"), charge_high)
    input_external = selected_input_bounds(boost=True)
    input_sdp = selected_input_bounds()
    historical_input_default = bounded_ratio("459", "500", "1000", "0.01")
    historical_input_high = bounded_ratio("459", "500", parallel("1000", "665"), "0.01")
    rail_3v3 = divider("0.500", "511000", "91000")
    rail_vled = divider("0.500", "1240000", "180000")
    always_on_max = D("6.5") + D("5")
    return {
        "charge": charge,
        "input_external": input_external,
        "input_sdp": input_sdp,
        "historical_fixed_usb500_max": D("0.5"),
        "historical_single_resistor_high": bounded_ratio("1500", "1720", "1780", "0.01"),
        "configured_sdp_allocated_total": total_usb_current(input_sdp[2], "0.020", "0.002"),
        # Counterexample for the ordinary ERJ2RK candidate, not a selected MPN.
        "sdp_temperature_counterexample": total_usb_current(
            D('1720')/(D('3650')*D('.99')*D('.9935')), '.020', '.002'),
        "historical_input_default": historical_input_default,
        "historical_input_high": historical_input_high,
        "rail_3v3": rail_3v3,
        "rail_vled": rail_vled,
        "always_on_max_uA": always_on_max,
        "off_budget_remaining_uA": D("50") - always_on_max,
    }


def check():
    PRECISION['check_budget']()
    value = results()
    charge_min, charge_nom, charge_max = value["charge"]
    input_min, input_nom, input_max = value["input_external"]

    if not (D("0.698") < charge_min < D("0.699")):
        raise ValueError("BQ24074 minimum charge-current calculation changed")
    if not (D("0.787") < charge_nom < D("0.789")):
        raise ValueError("BQ24074 nominal charge-current calculation changed")
    if not (D("0.871") < charge_max < D("0.873")):
        raise ValueError("BQ24074 maximum charge-current calculation changed")
    if not (D("0.833") < input_min < D("0.834")):
        raise ValueError("BQ24074 minimum external input-current calculation changed")
    if not (D("0.903") < input_nom < D("0.904")):
        raise ValueError("BQ24074 nominal external input-current calculation changed")
    if not (D("0.975") < input_max < D("0.976")):
        raise ValueError("BQ24074 maximum external input-current calculation changed")
    if input_max > value["historical_single_resistor_high"][2]:
        raise ValueError("Hardware boost increased the previous high-current maximum")
    if not D("0.497") < value["configured_sdp_allocated_total"] < D("0.5"):
        raise ValueError("Configured SDP allocation no longer fits 500 mA")
    if value['sdp_temperature_counterexample']<=D('.5'):
        raise ValueError('Lost the resistor-temperature budget counterexample')
    if not (D("3.307") < value["rail_3v3"] < D("3.309")):
        raise ValueError("TPS631000 3.3-V divider calculation changed")
    if not (D("3.944") < value["rail_vled"] < D("3.945")):
        raise ValueError("TPS63020 VLED divider calculation changed")
    if value["off_budget_remaining_uA"] != D("38.5"):
        raise ValueError("Always-on IC current budget changed")

    for switch_on in (False, True):
        for type_c in TYPE_C_STATES - {"none"}:
            for bc12 in BC12_STATES:
                for configured in (False, True):
                    for suspended in (False, True):
                        state = selected_usb_state(switch_on=switch_on, type_c=type_c, bc12=bc12,
                                                   configured=configured, suspended=suspended)
                        if not switch_on and state["data_connected"]:
                            raise ValueError("USB data connected while switch is OFF")
                        if not switch_on and state["app_data_isolator_powered"]:
                            raise ValueError("Application USB isolator powered while switch is OFF")
                        if not state["good_bat"]:
                            raise ValueError("BQ24392 GOOD_BAT low while VBUS is valid")
                        if state["data_connected"] and not state["app_data_isolator_powered"]:
                            raise ValueError("USB data connected through an unpowered application isolator")
                        if state["mode"] == "external-ilim" and state["permission"] == "usb-stack":
                            raise ValueError("Firmware grant selected external high-current mode")
    return value


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--require-usb-closure", action="store_true",
                        help="Fail while USB/input circuit blockers remain; arithmetic success is insufficient")
    args = parser.parse_args()
    try:
        value = check()
        supply = actuator_supply_screen()
        print("Power pre-capture calculations passed:")
        print('- ADR 0012 current bounds use ±1% TOTAL resistance error; selected parts are 0.1%, 25 ppm/K, with assembly/service allocation still requiring qualification')
        print(f"- BQ24074 1.13-kohm charge setting: {value['charge'][0]:.3f} to {value['charge'][2]:.3f} A")
        print(f"- ADR 0011 low ILIM (3.65 kohm): {value['input_sdp'][0]:.3f} to {value['input_sdp'][2]:.3f} A")
        print(f"- hardware boost (3.65 || 3.48 kohm): {value['input_external'][0]:.3f} to {value['input_external'][2]:.3f} A, ideal switch")
        print(f"- configured SDP allocation: {value['configured_sdp_allocated_total']:.3f} A including 20 mA auxiliary + 2 mA programming allowances (not qualified loads)")
        print(f"- 100-ppm/K resistor candidate at temperature: {value['sdp_temperature_counterexample']:.6f} A with those allocations; exceeds 500 mA, so the earlier tolerance-only margin is NOT closure")
        print("- ADR 0010/0011 source/switch/configuration/suspend and two-stage data-isolation truth table is internally consistent")
        print(f"- nominal rails: {value['rail_3v3']:.3f} V application and {value['rail_vled']:.3f} V LED")
        print(f"- BQ24074 plus hibernating MAX17048 maxima consume {value['always_on_max_uA']:.1f} uA of the 50-uA OFF budget")
        print(f"- candidate shared-rail static UVLO margin: {supply['fall_remaining_margin_v']:.3f} V; zero-drop/zero-delay assumption only, NOT transient closure")
        print("- exact libraries/logic, auxiliary loads, battery/NTC, thermal behavior and layout still require review")
        blockers = usb_capture_blockers()
        print("USB/input capture remains BLOCKED:")
        for finding in blockers:
            print(f"- {finding}")
        if args.require_usb_closure and blockers:
            return 1
    except (ArithmeticError, ValueError) as error:
        print(f"Power pre-capture check failed: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
