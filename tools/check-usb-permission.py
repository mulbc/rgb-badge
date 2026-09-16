#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Check the ADR 0011 permission contract against actual detector GPIO encodings.

Static Boolean analysis only. This is not a captured gate circuit, transient
simulation, supply-sequencing proof, USB compliance result or native KiCad check.
"""

from itertools import product


# TUSB320LAI SLLSEQ8D Table 3. 1 includes open-drain release with a valid pull-up.
TYPE_C_PINS = {
    "unattached": (1, 1), "default": (1, 0),
    "1.5A": (0, 1), "3A": (0, 0),
}
# BQ24392 SLIS146G Table 1, GOOD_BAT high: CHG_AL_N, CHG_DET, SW_OPEN.
BC12_PINS = {
    "none": (1, 0, 1), "SDP": (0, 0, 0), "CDP": (0, 1, 0),
    "DCP": (0, 1, 1), "dedicated": (0, 1, 1),
    "unclassified": (0, 0, 1),
}


def permission(*, out1, out2, chg_al_n, chg_det, sw_open,
               vbus_valid, logic_ready, switch_on, esp_running, usb_request):
    """Resolve stable inputs to standby / low ILIM / high ILIM.

    usb_request is the USB stack's configured-and-unsuspended grant, not an
    application preference. esp_running must clear on reset. logic_ready must
    eventually come from a qualified hardware power/reset circuit, not firmware.
    """
    for name, value in (("out1", out1), ("out2", out2), ("chg_al_n", chg_al_n),
                        ("chg_det", chg_det), ("sw_open", sw_open)):
        if type(value) is not int or value not in (0, 1):
            raise ValueError(f"{name} must be a resolved 0 or 1")
    for value in (vbus_valid, logic_ready, switch_on, esp_running, usb_request):
        if type(value) is not bool:
            raise ValueError("Power, reset and request inputs must be booleans")

    attached = not (out1 and out2)
    ready = vbus_valid and logic_ready and attached
    high = bool(ready and (not out1 or (not chg_al_n and chg_det)))
    sdp = not chg_al_n and not chg_det and not sw_open
    low = bool(ready and sdp and switch_on and esp_running and usb_request)
    run = high or low
    return {
        "mode": "input-asleep" if not vbus_valid else
                "external-high" if high else "external-low" if low else "standby",
        "en2": 1 if vbus_valid else None,
        "en1": int(not run) if vbus_valid else None,
        "boost": high,
    }


def check():
    count = 0
    for bits in product((0, 1), repeat=5):
        for flags in product((False, True), repeat=5):
            args = dict(zip(("out1", "out2", "chg_al_n", "chg_det", "sw_open"), bits))
            args.update(zip(("vbus_valid", "logic_ready", "switch_on", "esp_running", "usb_request"), flags))
            state = permission(**args)
            count += 1
            # Vary every firmware/application-domain condition together: none
            # may affect the resistor-boost output, even for inconsistent GPIOs.
            for field in ("switch_on", "esp_running", "usb_request"):
                changed = permission(**(args | {field: not args[field]}))
                if changed["boost"] != state["boost"]:
                    raise ValueError("Application state reached the high-current branch")
            if state["en2"] == 0:
                raise ValueError("Fixed USB100/USB500 mode became reachable")
            if not flags[0] or not flags[1] or bits[:2] == (1, 1):
                if state["boost"] or state["mode"] not in ("standby", "input-asleep"):
                    raise ValueError("Invalid supply or unattached source received permission")
    return count


if __name__ == "__main__":
    print(f"USB permission contract passed: {check()} GPIO/power/request combinations; abstract static contract, not physical startup/actuator qualification.")
