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
 assert m['original_orphan_restoration']['only_three_exact_original_orphan_warnings']
 assert len(m['isolated_fault_guards'])==7 and all(row['rejected'] for row in m['isolated_fault_guards'])
 for path,digest in m['tool_sha256'].items():assert policy.sha(policy.ROOT/path)==digest,path
 for ext,key in [('.kicad_pro','project_sha256'),('.kicad_dru','rules_sha256')]:
  assert policy.sha(policy.OUTPUT.with_suffix(ext))==m[key]
  assert policy.OUTPUT.with_suffix(ext).read_bytes()==policy.PARENT.with_suffix(ext).read_bytes()
 assert policy.sha(policy.ROOT/'docs/development/remaining-routing-drc-2026-11-07.json')==m['drc_sha256']
 assert not m['fabrication_release_allowed'] and m['goal_status']=='IN_PROGRESS_ZERO_OPEN_GOAL'
 print('Exact routing closure fingerprints passed:',m['native_opens'],'opens; zero-open goal ongoing, fabrication prohibited.')
if __name__=='__main__':main()
