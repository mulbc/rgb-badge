#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Portable fingerprints for the selected converter study; not native/electrical proof."""
import json
from pathlib import Path
import converter_checkpoint as policy


def main():
    plan=policy.load_plan();manifest_path=policy.ROOT/'mechanical/review/converter-routing-checkpoint.json'
    manifest=json.loads(manifest_path.read_text())
    assert policy.sha(policy.PARENT)==policy.PARENT_SHA==manifest['parent_sha256']
    assert policy.sha(policy.OUTPUT)==manifest['board_sha256']
    assert manifest['plan_sha256']==policy.PLAN_SHA
    assert manifest['native_opens']==manifest['physical_opens']==plan['native_opens']
    assert manifest['intrinsic_findings']==104 and manifest['fabrication_release_allowed'] is False
    for name,digest in manifest['tool_sha256'].items():assert policy.sha(policy.ROOT/name)==digest, name
    for ext,key in [('.kicad_pro','project_sha256'),('.kicad_dru','rules_sha256')]:
        assert policy.OUTPUT.with_suffix(ext).read_bytes()==policy.PARENT.with_suffix(ext).read_bytes()
        assert policy.sha(policy.OUTPUT.with_suffix(ext))==manifest[key]
    assert manifest['all_246_parent_groups_preserved'] and manifest['original_orphan_restoration_passed']
    assert manifest['retired_original_items']==plan['removed_original_items']
    assert manifest['retired_accepted_items']==plan['removed_accepted_items']
    assert manifest['new_copper_items']==len(plan['added_copper'])
    print('Converter checkpoint fingerprints passed; native and electrical qualification are separate.')


if __name__=='__main__':main()
