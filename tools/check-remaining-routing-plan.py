#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Portable exact fingerprints for the ongoing zero-open routing study."""
import json
import routing_remaining as policy

def main():
 plan=policy.load_plan();m=json.loads((policy.ROOT/'mechanical/review/remaining-routing-checkpoint.json').read_text())
 assert policy.sha(policy.OUTPUT)==m['board_sha256'] and m['parent_sha256']==policy.PARENT_SHA and m['plan_sha256']==policy.PLAN_SHA
 assert m['native_opens']==m['physical_opens']==plan['native_opens'] and m['intrinsic_findings']==104
 assert m['all_231_parent_groups_preserved'] and m['stable_fill_and_replay_identical']
 assert m['previous_checkpoint_preserved']['all_groups_and_added_copper_preserved']
 assert m['previous_checkpoint_preserved']['source_sha256']==plan['previous_checkpoint']['source_sha256']
 assert m['native_actual_copper_endpoint_fixture_passed']
 assert m['ground_plane_replacement_witness']['single_individual_bcu_ground_component']
 assert m['ground_plane_replacement_witness']['boundary_contact_count']==5 and m['ground_plane_replacement_witness']['both_endpoint_disks_touch']
 assert m['permission_lead_replacement_witness']['boundary_contact_count']==4
 assert m['permission_lead_replacement_witness']['both_outer_endpoints_retained'] and m['permission_lead_replacement_witness']['all_original_bcu_contacts_retained']
 assert m['permission_lead_replacement_witness']['tp14_previous_isolation_and_no_copper_contact']
 assert m['permission_lead_replacement_witness']['tp14_joined_pad']==['U54','3'] and m['permission_lead_replacement_witness']['tp14_lead_length_mm']<=5
 assert m['permission_lead_replacement_witness']['tp14_isolation_source_sha256']=='aab8f44a9ec3ae65aed4ee2500d52d57d4d3872c8428b8f50c765bfedd205a1e'
 assert m['native_testpad_escape_witness']['source_capture_iu']==[26250000,20875000]
 assert m['native_testpad_escape_witness']['prior_isolation_and_no_copper_contact'] and m['native_testpad_escape_witness']['joined_pad']==['U55','7']
 assert m['native_testpad_escape_witness']['trace_length_mm']<=5 and m['native_testpad_escape_witness']['new_vias']==2 and not m['native_testpad_escape_witness']['source_copper_retired']
 assert m['inherited_original_orphan_restoration']['only_three_exact_original_orphan_warnings']
 assert m['inherited_original_orphan_restoration']['basis']=='IMMUTABLE_43_OPEN_PARENT'
 assert m['inherited_original_orphan_restoration']['board_sha256']==policy.PARENT_SHA
 assert m['selected_retirement_probe']['source_unchanged'] and m['selected_retirement_probe']['status']=='REJECTED_COUNTERFACTUAL_NOT_SELECTED_SOURCE'
 assert m['capacitor_microplacement_witness']['original_direct_land_contacts_retained']
 assert m['capacitor_microplacement_witness']['contact_count']==1
 assert m['capacitor_microplacement_witness']['historical_ground_isolated']
 assert not m['capacitor_microplacement_witness']['historical_source_copper_retained']
 assert m['capacitor_microplacement_witness']['historical_source_copper_retained_except_reviewed_leaf']
 assert m['capacitor_microplacement_witness']['historical_approved_retired_copper']==[plan['r11_ground_replacement']['original_copper']]
 assert m['r11_ground_replacement_witness']['exact_original_leaf_retired'] and m['r11_ground_replacement_witness']['all_original_land_contacts_accounted_for']
 assert m['r11_ground_replacement_witness']['retained_ground_via_centres_reached']
 assert m['r11_ground_replacement_witness']['far_end_contacts_retained'] and m['r11_ground_replacement_witness']['actual_old_ground_endpoints_retained']
 assert m['r11_ground_replacement_witness']['shunt_ground_joined'] and m['r11_ground_replacement_witness']['main_ground_pad_count']>=196
 assert m['capacitor_microplacement_witness']['single_individual_bcu_ground_component']
 assert m['capacitor_microplacement_witness']['displacement_iu']==[0,-250000]
 assert m['capacitor_microplacement_witness']['source_sha256']=='ed6d3ff570f2481b47423d8375d9d4a40d756145cdd49e2c222bacc36edbfa57'
 assert len(m['isolated_fault_guards'])==44 and all(row['rejected'] for row in m['isolated_fault_guards'])
 for path,digest in m['tool_sha256'].items():assert policy.sha(policy.ROOT/path)==digest,path
 for ext,key in [('.kicad_pro','project_sha256'),('.kicad_dru','rules_sha256')]:
  assert policy.sha(policy.OUTPUT.with_suffix(ext))==m[key]
  assert policy.OUTPUT.with_suffix(ext).read_bytes()==policy.PARENT.with_suffix(ext).read_bytes()
 assert policy.sha(policy.ROOT/'docs/development/remaining-routing-drc-2026-11-07.json')==m['drc_sha256']
 assert not m['fabrication_release_allowed'] and m['goal_status']=='IN_PROGRESS_ZERO_OPEN_GOAL'
 print('Exact routing closure fingerprints passed:',m['native_opens'],'opens; zero-open goal ongoing, fabrication prohibited.')
if __name__=='__main__':main()
