#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Check the frozen arithmetic and safety boundaries for Coupon Rev A power capture.

This is a deterministic design calculation, not a simulation, native KiCad ERC,
USB compliance test, battery qualification, thermal result, or fabrication approval.
"""

from decimal import Decimal as D
import sys


def bounded_ratio(constant_min, constant_max, resistance, tolerance):
    """Return minimum/nominal/maximum current for I = K/R."""
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
    try:
        value = check()
        print("Power pre-capture calculations passed:")
        print(f"- BQ25616J 806-ohm charge setting: {value['charge'][0]:.3f} to {value['charge'][2]:.3f} A")
        print(f"- candidate unknown-adapter ILIM states: {value['input_default'][0]:.3f} to {value['input_default'][2]:.3f} A and {value['input_high'][0]:.3f} to {value['input_high'][2]:.3f} A")
        print(f"- nominal rails: {value['rail_3v3']:.3f} V application and {value['rail_vled']:.3f} V LED")
        print(f"- BQ25616J plus hibernating MAX17048 maxima consume {value['always_on_max_uA']:.0f} uA of the 50-uA OFF budget")
        print("- USB default-current, battery/NTC, tolerances, thermal behavior and layout still require review")
    except (ArithmeticError, ValueError) as error:
        print(f"Power pre-capture check failed: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
