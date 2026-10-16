#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Reproduce ADR 0018 proposal arithmetic, NOT circuit or hardware validation.

Manufacturer constants: BQ24074 SLUS810N; TPS25947 SLVSFC9C;
TCA9517A SCPS245E. Load, efficiency and thermal inputs are scenarios.
Run from any directory; stdout is deterministic JSON. No files are modified.
"""
from decimal import Decimal as D
from itertools import product
import json
from pathlib import Path
import runpy


def report():
    protection = runpy.run_path(str(Path(__file__).with_name('check-input-protection.py')))
    charge_min = D(797) / (D(2490) * D('1.01'))
    charge_typ = D(890) / D(2490)
    charge_max = D(975) / (D(2490) * D('.99'))
    ilim_r = D(3650) * D(3480) / D(7130)
    ilim_min = D(1500) / (ilim_r * D('1.01'))
    ilim_max = D(1720) / (ilim_r * D('.99'))
    lower_ilim_r = D(3650)
    lower_ilim_min = D(1330) / (lower_ilim_r * D('1.01'))
    lower_ilim_max = D(1720) / (lower_ilim_r * D('.99'))
    fuse_rows = [(D('6650'), D('.425'), D('.575')),
                 (D('3320'), D('.850'), D('1.150')),
                 (D('1650'), D('1.800'), D('2.200'))]
    thermal = []
    for cell_v, sys_a, theta in product(map(D, ('3.0', '3.4')), map(D, ('0', '.4')), map(D, ('44.5', '70'))):
        loss = (D('5.5') - cell_v) * charge_max + (D('5.5') - D('4.4')) * sys_a
        thermal.append(dict(cell_v=cell_v, sys_a=sys_a, theta_c_per_w=theta,
                            loss_w=loss, open_loop_junction_c=D(40) + theta * loss))
    states = []
    for voltage_valid, logic_ready, advertised_high, switch_on in product((False, True), repeat=4):
        permit = voltage_valid and logic_ready and advertised_high
        states.append(dict(voltage_valid=voltage_valid, logic_ready=logic_ready,
                           advertised_high=advertised_high, switch_on=switch_on,
                           charger_input_permitted=permit,
                           application_requested=switch_on,
                           gauge_requested=switch_on))
    ov = protection['divider_bounds']('38300', '10000', ('1.183', '1.223'), ('-.0000001', '.0000001'), '.01')
    recovery = protection['divider_bounds']('38300', '10000', ('1.076', '1.116'), ('-.0000001', '.0000001'), '.01')
    energy = D('.9') * D('3.7') * D('.85')
    buffer_power = D('3.3') * D('.005') / D('.85')
    en_pullup_min = D(220000) * D('.99')
    en_pullup_max = D(220000) * D('1.01')
    en_pulldown_min = D(1000000) * D('.99')
    hypothetical_en_sink = D('.0000009')
    en_high_screen = (D('3.0') / en_pullup_max - hypothetical_en_sink) / (1 / en_pullup_max + 1 / en_pulldown_min)
    en2_feed_min = (D('4.35') - D('2.519')) / D('10100')
    en2_fault_feed_max = (D('28') - D('2.481')) / D('9900')
    return {
        'SPDX-License-Identifier': 'CERN-OHL-S-2.0',
        'status': 'PROPOSAL_ONLY_NOT_CAPTURED_NOT_SIMULATED_NOT_MEASURED',
        'baseline_commit': '0764245',
        'charge_setting': {'numerical_resistance_ohm': 2490, 'exact_mpn_selected': False,
                           'total_resistance_error_fraction': D('.01'),
                           'min_a': charge_min, 'typ_a': charge_typ, 'max_a': charge_max,
                           '900mah_ideal_80percent_min_minutes_at_max_a': D('.72') / charge_max * 60,
                           '900mah_ideal_full_min_minutes_at_max_a': D('.9') / charge_max * 60},
        'unchanged_charger_input_limit_a': [ilim_min, ilim_max],
        'qualified_source_arithmetic_headroom_a': D('1.5') - ilim_max,
        'lower_fixed_input_limit_screen': {
            'status': 'PROPOSED_DC_SCREEN_NOT_SELECTED',
            'retained_exact_resistor_mpn': 'ERA2AEB3651X',
            'remove_parallel_branch_mpn_if_accepted': 'ERA2AEB3481X',
            'total_resistance_error_fraction_assumed': D('.01'),
            'calculated_bq24074_limit_min_a': lower_ilim_min,
            'calculated_bq24074_limit_max_a': lower_ilim_max,
            'tps259474_published_3k32_min_threshold_a': D('.850'),
            'dc_gap_to_published_nominal_rilm_test_point_a': D('.850') - lower_ilim_max,
            'normal_1v5_source_arithmetic_headroom_a': D('1.5') - lower_ilim_max,
            'charge_current_proposal_max_a': charge_max,
            'charger_input_min_below_charge_proposal_max': lower_ilim_min < charge_max,
            'efuse_resistor_tolerance_transient_or_fault_proven': False,
        },
        'published_efuse_threshold_rows': [
            {'resistance_ohm': resistance, 'minimum_a': minimum, 'maximum_a': maximum,
             'minimum_exceeds_charger_input_corner': minimum > ilim_max,
             'maximum_at_or_below_1v5_source_a': maximum <= D('1.5')}
            for resistance, minimum, maximum in fuse_rows],
        'ovlo_38k3_10k_screen_v': {'rising': ov, 'falling': recovery},
        'thermal_scenarios': thermal,
        'runtime_scenarios': {'usable_nominal_energy_wh': energy,
                              'baseline_hours': energy / D('.45'),
                              'buffer_5ma_85percent_efficiency_extra_w': buffer_power,
                              'with_buffer_hours': energy / (D('.45') + buffer_power),
                              'required_nominal_mah_for_six_hours_with_buffer':
                              6 * (D('.45') + buffer_power) / (D('3.7') * D('.85')) * 1000},
        'gauge_bus_screen': {'pullup_nominal_ohm': 2200,
                             'assumed_resistance_factor': D('1.023'),
                             '300ns_max_modeled_capacitance_pf': D('300e-9') / (D('.8473') * 2200 * D('1.023')) * D('1e12'),
                             '4v23_pullup_current_a_conservative': D('4.23') / (2200 * D('.977'))},
        'permission_candidate_static_screen': {
            'gate': 'SN74AUP1G125DBVR', 'rail_v': '3.3V_USB',
            'pullup_nominal_ohm': 220000, 'pulldown_nominal_ohm': 1000000,
            'resistor_total_error_fraction_assumed': D('.01'),
            'pullup_current_at_0v8_rail_a': D('.8') / en_pullup_min,
            'pullup_current_at_3v6_rail_a': D('3.6') / en_pullup_min,
            'hypothetical_combined_en_sink_a': hypothetical_en_sink,
            'minimum_en_high_at_3v_rail_v': en_high_screen,
            'leakage_and_transients_proven': False},
        'charger_en2_local_clamp_screen': {
            'status': 'PROPOSED_DC_SCREEN_ISOLATED_KICAD_CANDIDATE_ONLY',
            'shunt_exact_mpn': 'LM4040A25IDBZT',
            'series_resistor_exact_mpn': 'ERJ2RKF1002X',
            'minimum_feed_at_bq_operating_input_a': en2_feed_min,
            'assumed_en2_load_at_clamp_a': D('.000020'),
            'minimum_shunt_after_assumed_load_a': en2_feed_min - D('.000020'),
            'lm4040_full_range_minimum_cathode_current_a': D('.000080'),
            'fault_28v_max_feed_a': en2_fault_feed_max,
            'fault_28v_resistor_power_w': (D('28') - D('2.481')) ** 2 / D('9900'),
            'en2_load_at_2v5_manufacturer_bounded': False,
            'startup_and_fault_waveforms_proven': False,
        },
        'off_current_allocations_ua': {'charger_reference_limit': D('6.5'), 'pack_protection_target': 10,
                                      'disabled_converters_target': 10, 'other_paths_target': 10,
                                      'unspent_margin_to_50': D('13.5'), 'compliance_established': False},
        'stable_intent_states': states,
        'unresolved': ['Exact protected NTC pack and connector', 'USB fault and enable transient bounds',
                       'eFuse current/inrush coordination', 'Gauge buffer power-down and LOW-level bounds',
                       'Hardware display interlock circuit', 'Thermal, runtime and mechanical qualification'],
    }


if __name__ == '__main__':
    print(json.dumps(report(), default=lambda value: str(value) if isinstance(value, D) else value, indent=2))
