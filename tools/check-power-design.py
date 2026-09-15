#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Check the selected arithmetic and safety boundaries for Coupon Rev A power capture.

This is a deterministic design calculation, not a simulation, native KiCad ERC,
USB compliance test, battery qualification, thermal result, or fabrication approval.
"""

import argparse
from decimal import Decimal as D
import sys


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


def usb_capture_blockers():
    """Selected topology tasks not yet closed by calculation alone."""
    return (
        "Exact BQ24074RGTR, BQ24392RSER and TS3USB31ERSER libraries passed native review at c054cb4; the power circuit remains uncaptured.",
        "The VBUS-domain level translation and high-current-over-SDP priority logic are not captured.",
        "The detector/LDO/logic/status auxiliary-current budget and source transitions are not validated.",
        "The exact pack, NTC/timer network and BQ24074 linear thermal behavior remain unqualified.",
    )


TYPE_C_STATES = frozenset(("none", "default", "1.5A", "3A"))
BC12_STATES = frozenset(("none", "SDP", "CDP", "DCP", "dedicated", "unclassified"))
HIGH_TYPE_C = frozenset(("1.5A", "3A"))
HIGH_BC12 = frozenset(("CDP", "DCP", "dedicated"))


def selected_usb_state(*, switch_on, type_c, bc12, configured=False, suspended=False):
    """Resolve ADR 0010's logical product state.

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
        return {"mode": "usb500", "en2": 0, "en1": 1,
                "data_connected": True, "permission": "usb-stack",
                "good_bat": True, "app_data_isolator_powered": True}
    return {"mode": "standby", "en2": 1, "en1": 1,
            "data_connected": data_connected, "permission": "none",
            "good_bat": True, "app_data_isolator_powered": switch_on}


def results():
    charge_low, _, charge_high = bounded_ratio("797", "975", "1130", "0.01")
    charge = (charge_low, D("890") / D("1130"), charge_high)
    input_external = bounded_ratio("1500", "1720", "1780", "0.01")
    historical_input_default = bounded_ratio("459", "500", "1000", "0.01")
    historical_input_high = bounded_ratio("459", "500", parallel("1000", "665"), "0.01")
    rail_3v3 = divider("0.500", "511000", "91000")
    rail_vled = divider("0.500", "1240000", "180000")
    always_on_max = D("6.5") + D("5")
    return {
        "charge": charge,
        "input_external": input_external,
        "historical_input_default": historical_input_default,
        "historical_input_high": historical_input_high,
        "rail_3v3": rail_3v3,
        "rail_vled": rail_vled,
        "always_on_max_uA": always_on_max,
        "off_budget_remaining_uA": D("50") - always_on_max,
    }


def check():
    value = results()
    charge_min, charge_nom, charge_max = value["charge"]
    input_min, input_nom, input_max = value["input_external"]

    if not (D("0.698") < charge_min < D("0.699")):
        raise ValueError("BQ24074 minimum charge-current calculation changed")
    if not (D("0.787") < charge_nom < D("0.789")):
        raise ValueError("BQ24074 nominal charge-current calculation changed")
    if not (D("0.871") < charge_max < D("0.873")):
        raise ValueError("BQ24074 maximum charge-current calculation changed")
    if not (D("0.834") < input_min < D("0.835")):
        raise ValueError("BQ24074 minimum external input-current calculation changed")
    if not (D("0.904") < input_nom < D("0.905")):
        raise ValueError("BQ24074 nominal external input-current calculation changed")
    if not (D("0.976") < input_max < D("0.977")):
        raise ValueError("BQ24074 maximum external input-current calculation changed")
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
        print("Power pre-capture calculations passed:")
        print(f"- BQ24074 1.13-kohm charge setting: {value['charge'][0]:.3f} to {value['charge'][2]:.3f} A")
        print(f"- BQ24074 1.78-kohm external input setting: {value['input_external'][0]:.3f} to {value['input_external'][2]:.3f} A")
        print("- ADR 0010 source/switch/configuration/suspend and two-stage data-isolation truth table is internally consistent")
        print(f"- nominal rails: {value['rail_3v3']:.3f} V application and {value['rail_vled']:.3f} V LED")
        print(f"- BQ24074 plus hibernating MAX17048 maxima consume {value['always_on_max_uA']:.1f} uA of the 50-uA OFF budget")
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
