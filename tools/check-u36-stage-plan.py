#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Portable fingerprints for the selected stage; native/electrical checks differ."""
import json
import u36_stage_checkpoint as policy


def main():
    plan=policy.load_plan()
    manifest=json.loads((policy.ROOT/'mechanical/review/u36-stage-checkpoint.json').read_text())
    assert policy.sha(policy.OUTPUT)==manifest['board_sha256']
    assert manifest['parent_sha256']==policy.PARENT_SHA and manifest['plan_sha256']==policy.PLAN_SHA
    assert manifest['native_opens']==manifest['physical_opens']==47
    assert manifest['intrinsic_findings']==104 and manifest['all_238_parent_groups_preserved']
    assert manifest['all_local_pin_witnesses_passed'] and manifest['stable_fill_and_replay_identical']
    assert manifest['original_orphan_restoration']['only_three_exact_original_orphan_warnings']
    assert len(manifest['isolated_fault_guards'])==5 and all(r['rejected'] for r in manifest['isolated_fault_guards'])
    for name,digest in manifest['tool_sha256'].items():assert policy.sha(policy.ROOT/name)==digest,name
    for ext,key in (('.kicad_pro','project_sha256'),('.kicad_dru','rules_sha256')):
        assert policy.sha(policy.OUTPUT.with_suffix(ext))==manifest[key]
        assert policy.OUTPUT.with_suffix(ext).read_bytes()==policy.PARENT.with_suffix(ext).read_bytes()
    assert not manifest['fabrication_release_allowed'] and not plan['fabrication_release_allowed']
    print('47-edge stage fingerprints passed; fabrication and power qualification remain separate.')


if __name__=='__main__':main()
