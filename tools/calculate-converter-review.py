#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Reproduce dated converter sensitivities; none is a qualified operating limit."""
import argparse
import bisect
import csv
import hashlib
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / 'hardware/coupon/rev-a/reference/vendor-datasheets'
CURVE = 'GRM219R60J476ME44_InProduction.csv'
CURVE_SHA = '79839e9d42e739c23f68490a2ea4248ca1c6cb45026c2a8897408973abaaa57e'
PDFS = {
    'tps631000.pdf': 'b52a4064a8c2cbb4c9dd97f366b398dedcb490ffc9d564245f297536a19b426b',
    'tps63020.pdf': 'd117773bb7370fd79377bc70ce987eec3469ea5979547a09df52fca5f95b2e69',
    'm_dfe252012p.pdf': 'ce259ba611fb3ea196baf60e2c7080a21cd897cdb662bf77552cc842c2b91c3e',
    'GRM187R61A226ME15-01A-EN.pdf': '8fc5a9d8e4f05c979eeca00354c982335d2b15552eb7ba5516924e3a9395acbb',
    'GRM219R60J476ME44-01A-EN.pdf': '97ac8bc37c063e920aa768521386524edb6a5d60cd0e3080f318ca567f75bafe',
    'GRM188R60J106ME47-61A-EN.pdf': 'f51cff8dad7a6983263ab35b5705f4d1d4b9977b1f03739c653381ba03d94ea8',
    'NTLJD3119C-D.PDF': '202122bd220e16138c458ac93bb737ab4fdb8a60d3a3722059636636f47d7aed',
    'sn74lvc1g04-2026-11-05.pdf': '5322c1ab3cd3bd3f7af9c9bfa1c6139dad799d0968d9eea3ee2d84648ffc2e9e',
    'sn74lvc1g08-2026-11-05.pdf': '30b963cc44233cf3ca35c891ff987c8323a2244ecc765e23296ec96ca4b42666',
}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def interpolate(points, voltage):
    """Interpolate one curve on its own axis; refuse extrapolation."""
    if len(points) < 2 or any(not math.isfinite(v) for row in points for v in row):
        raise ValueError('finite curve with two or more points required')
    xs = [row[0] for row in points]
    if any(a >= b for a, b in zip(xs, xs[1:])):
        raise ValueError('strictly increasing independent voltage axis required')
    if not math.isfinite(voltage) or not xs[0] <= voltage <= xs[-1]:
        raise ValueError('voltage outside measured curve')
    index = min(max(bisect.bisect_right(xs, voltage), 1), len(xs) - 1)
    x0, y0 = points[index - 1]
    x1, y1 = points[index]
    return y0 + (y1 - y0) * (voltage - x0) / (x1 - x0)


def curves(path):
    points = [[], []]
    for row in csv.reader(path.read_text().splitlines()):
        if not row or row[0].startswith('#') or row[0] == 'DC Bias[V]':
            continue
        for i, column in enumerate((0, 2)):
            if len(row) > column + 1 and row[column] and row[column + 1]:
                points[i].append((float(row[column]), float(row[column + 1])))
    return points


def feedback(top, bottom, temperature_shift_k=0):
    """Opposing 1% initial errors and 100 ppm/K TCR, multiplied explicitly."""
    low_r = .99 * (1 - .0001 * temperature_shift_k)
    high_r = 1.01 * (1 + .0001 * temperature_shift_k)
    return {
        'nominal_pwm_V': .5 * (1 + top / bottom),
        'static_low_V': .495 * (1 + top * low_r / (bottom * high_r)),
        'static_high_V': .505 * (1 + top * high_r / (bottom * low_r)),
        'temperature_shift_K_scenario': temperature_shift_k,
        'excludes': 'ripple, load/line dynamics, aging, self heating and combined manufacturer guarantee',
    }


def resistance(length_mm, width_mm, copper_um, temperature_c=20):
    """Uniform rectangular copper model; no ampacity or thermal solution."""
    if min(length_mm, width_mm, copper_um) <= 0:
        raise ValueError('positive dimensions required')
    return 1.72e-8 * length_mm * 1e-3 / (width_mm * 1e-3 * copper_um * 1e-6) * (1 + .00393 * (temperature_c - 20))


def boost_peak(vin, vout, iout, efficiency, frequency_hz, inductance_h):
    if not 0 < vin < vout or not 0 < efficiency <= 1 or min(iout, frequency_hz, inductance_h) <= 0:
        raise ValueError('positive boost-mode scenario required')
    duty = 1 - vin / vout
    average = iout / (efficiency * (1 - duty))
    ripple = vin * duty / (frequency_hz * inductance_h)
    return {'average_A': average, 'ripple_pp_A': ripple,
            'peak_A': average + ripple / 2,
            'minimum_A_CCM_model': average - ripple / 2,
            'CCM_nonnegative_current_condition': average >= ripple / 2,
            'mode_caveat': 'Fixed-frequency CCM approximation; PFM/DCM and current-limit behavior require separate analysis',
            'rms_A_triangular_CCM_model': math.sqrt(average ** 2 + ripple ** 2 / 12),
            'recommended_20percent_peak_headroom_A': 1.2 * (average + ripple / 2)}


def calculate(native):
    if sha(CACHE / CURVE) != CURVE_SHA:
        raise ValueError('owner curve identity mismatch')
    sources = {CURVE: CURVE_SHA}
    for name, expected in PDFS.items():
        actual = sha(CACHE / name)
        if actual != expected:
            raise ValueError('cached source identity mismatch: ' + name)
        sources[name] = actual
    c219, c187 = curves(CACHE / CURVE)
    app = feedback(511, 91)
    app_temp = feedback(511, 91, 60)
    led = feedback(1240, 180)
    led_temp = feedback(1240, 180, 60)
    led['power_save_static_low_V'] = led['static_low_V'] * 1.006
    led['power_save_static_high_V'] = led['static_high_V'] * 1.05
    led_temp['power_save_static_low_V'] = led_temp['static_low_V'] * 1.006
    led_temp['power_save_static_high_V'] = led_temp['static_high_V'] * 1.05
    bank_specs = [
        ('U36_input_SYS4.5', c187, 2, 4.5, 4.2),
        ('U36_input_SYS5.5_sensitivity', c187, 2, 5.5, 4.2),
        ('U36_output_rail_high_scenario', c219, 2, app_temp['static_high_V'], 10.4),
        ('U37_output_nominal_PWM', c187, 4, led['nominal_pwm_V'], None),
        ('U37_output_power_save_high_scenario', c187, 4, led_temp['power_save_static_high_V'], None),
    ]
    caps = []
    for name, curve, number, voltage, minimum in bank_specs:
        typical = number * interpolate(curve, voltage) * 1e6
        caps.append({'scenario': name, 'voltage_V': voltage, 'count': number,
                     'typical_curve_bank_uF_at_25C_AC0p5Vrms': typical,
                     'hypothetical_factor_0p8_times_0p85_times_0p9_uF': typical * .612,
                     'TI_effective_minimum_uF_if_explicit': minimum,
                     'qualified_combined_lower_bound': False})
    widths = []
    for thickness in (18, 35):
        for width in (.2, .4, .6, .8):
            for length in (2.4529975715, 3.215685425, 6.374987827):
                r = resistance(length, width, thickness, 80)
                widths.append({'length_mm': length, 'width_mm': width, 'copper_um_assumed': thickness,
                               'temperature_C_assumed': 80, 'resistance_ohm': r,
                               'drop_mV_at_0p9A': 900 * r, 'loss_mW_at_0p9A': 810 * r})
    coils = []
    for ref, vo, f, lmin, dcr, loads in (
        ('L1', app['nominal_pwm_V'], 1.8e6, .8e-6, .042, (.1, .3, .5)),
        ('L2', led_temp['power_save_static_high_V'], 2.2e6, 1.2e-6, .060, (.23302, .69906)),
    ):
        for load in loads:
            row = boost_peak(2.8, vo, load, .8, f, lmin)
            row.update({'reference': ref, 'VIN_V_assumed': 2.8, 'VOUT_V': vo, 'Iout_A_scenario': load,
                        'efficiency_assumed': .8, 'frequency_min_Hz': f, 'L_initial_min_H': lmin,
                        'DCR_max_at_20C_ohm': dcr, 'copper_loss_W_using_20C_DCR': row['rms_A_triangular_CCM_model'] ** 2 * dcr,
                        'qualified_operating_point': False})
            coils.append(row)
    vias = []
    for height in (.05, .10):
        for plating in (.01, .02):
            area = math.pi * plating * (.10 + plating) * 1e-6
            vias.append({'finished_hole_mm_assumed': .10, 'height_mm_assumed': height,
                         'plating_mm_assumed': plating,
                         'ideal_cylindrical_barrel_R20_ohm': 1.72e-8 * height * 1e-3 / area,
                         'excludes': 'taper, fill, interfaces, current crowding, fatigue and thermal qualification'})
    budget = []
    for app_load, led_load in ((.1, .23302), (.3, .23302), (.5, .23302), (.1, .69906)):
        power = app['nominal_pwm_V'] * app_load + led['nominal_pwm_V'] * led_load
        budget.append({'app_load_A_assumed': app_load, 'VLED_load_A_nominal_driver_scenario': led_load,
                       'VIN_V_assumed': 2.8, 'efficiency_assumed': .8,
                       'calculated_input_A_excluding_other_loads': power / (2.8 * .8),
                       'recorded_pack_discharge_A_not_confirmed_continuous': .9})
    assert native['board_sha256'] == '5e07fb866cc059de670e34102045d9dfd88c88f101355fcdbb27253c0ae26e43'
    rows = native['all_104_classified_findings']
    assert len(rows) == 104 and sum(r['actual_clearance_mm'] == .15 for r in rows) == 80
    assert all(not r['accepted_for_fabrication'] for r in rows)
    return {
        'SPDX-License-Identifier': 'CERN-OHL-S-2.0',
        'status': 'REVIEW_AND_SENSITIVITY_CALCULATIONS_ONLY_NOT_HARDWARE_QUALIFICATION',
        'date': '2026-11-05', 'sources_sha256': sources,
        'calculator_sha256': sha(Path(__file__)),
        'native_inventory': native,
        'feedback': {'U36_initial': app, 'U36_60K_TCR_scenario': app_temp,
                     'U37_initial': led, 'U37_60K_TCR_scenario': led_temp},
        'capacitor_bank_scenarios': caps,
        'U37_derived_2x22uF_times_0p8_times_0p5_table_endpoint_uF_NOT_published_minimum': 17.6,
        'inductor_scenarios': coils, 'copper_scenarios': widths, 'ideal_via_scenarios': vias,
        'power_budget_scenarios': budget,
        'unknowns': ['GRM188 combined effective C', 'GRM187/GRM219 combined bias-temperature-aging bound',
                     'actual L(I,T)', 'actual rail/load/transient envelope', 'finished copper and dielectric stack',
                     'microvia build and reliability', 'package mask/paste process', 'complete thermal model'],
        'source_circuit_or_rules_changed': False, 'fabrication_release_allowed': False,
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--native', type=Path, required=True)
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    report = calculate(json.loads(args.native.read_text()))
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + '\n')
    print('Reproduced converter review sensitivities; no electrical or fabrication approval')


if __name__ == '__main__':
    main()
