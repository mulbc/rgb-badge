#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Check the frozen arithmetic and safety boundaries for Coupon Rev A power capture.

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
    """Check one steady-state ILIM setting, not a complete USB power circuit.

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
    """Known unresolved circuit findings; never inferred closed from arithmetic."""
    return (
        "The historical 1 kohm ILIM setting is nominally 478 mA, below the documented programming range.",
        "The direct ILIM network cannot provide a USB 2.0 host's 100 mA pre-configuration state.",
        "ILIM is not an override for BC1.2 detection; CE disables charging, not all system input current.",
        "Source classification, suspend, attach/detach and total port-current budgets lack a validated circuit.",
    )


def results():
    charge = bounded_ratio("639", "715", "806", "0.01")
    input_default = bounded_ratio("459", "500", "1000", "0.01")
    input_high = bounded_ratio("459", "500", parallel("1000", "665"), "0.01")
    rail_3v3 = divider("0.500", "511000", "91000")
    rail_vled = divider("0.500", "1240000", "180000")
    always_on_max = D("15") + D("5")
    return {
        "charge": charge,
        "input_default": input_default,
        "input_high": input_high,
        "rail_3v3": rail_3v3,
        "rail_vled": rail_vled,
        "always_on_max_uA": always_on_max,
        "off_budget_remaining_uA": D("50") - always_on_max,
    }


def check():
    value = results()
    charge_min, charge_nom, charge_max = value["charge"]
    default_min, _, default_max = value["input_default"]
    high_min, _, high_max = value["input_high"]

    if not (D("0.784") < charge_min < D("0.786")):
        raise ValueError("BQ25616J minimum charge-current calculation changed")
    if not (D("0.839") < charge_nom < D("0.841")):
        raise ValueError("BQ25616J nominal charge-current calculation changed")
    if not (D("0.895") < charge_max < D("0.897")):
        raise ValueError("BQ25616J maximum charge-current calculation changed")
    if not (D("0.454") < default_min < D("0.455") and D("0.505") < default_max < D("0.506")):
        raise ValueError("BQ25616J default ILIM calculation changed")
    if not (D("1.137") < high_min < D("1.139") and D("1.264") < high_max < D("1.266")):
        raise ValueError("BQ25616J high-advertisement ILIM calculation changed")
    if not (D("3.307") < value["rail_3v3"] < D("3.309")):
        raise ValueError("TPS631000 3.3-V divider calculation changed")
    if not (D("3.944") < value["rail_vled"] < D("3.945")):
        raise ValueError("TPS63020 VLED divider calculation changed")
    if value["off_budget_remaining_uA"] != D("30"):
        raise ValueError("Always-on IC current budget changed")
    return value


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--require-usb-closure", action="store_true",
                        help="Fail while USB/input circuit blockers remain; arithmetic success is insufficient")
    args = parser.parse_args()
    try:
        value = check()
        print("Power pre-capture calculations passed:")
        print(f"- BQ25616J 806-ohm charge setting: {value['charge'][0]:.3f} to {value['charge'][2]:.3f} A")
        print(f"- historical, unaccepted ILIM arithmetic: {value['input_default'][0]:.3f} to {value['input_default'][2]:.3f} A and {value['input_high'][0]:.3f} to {value['input_high'][2]:.3f} A")
        print(f"- nominal rails: {value['rail_3v3']:.3f} V application and {value['rail_vled']:.3f} V LED")
        print(f"- BQ25616J plus hibernating MAX17048 maxima consume {value['always_on_max_uA']:.0f} uA of the 50-uA OFF budget")
        print("- USB default-current, battery/NTC, tolerances, thermal behavior and layout still require review")
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
