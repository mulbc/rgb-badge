#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Portable exact R21 relocation ledger and canonical circuit contract."""
import json
import runpy
import routing_r21 as policy

def main():
 plan=policy.load_plan();assert policy.sha(policy.OUTPUT)==policy.BOARD_SHA
 assert plan['source_groups']==216 and plan['source_copper']==19381 and plan['native_opens']==plan['physical_opens']==27
 assert plan['poses']=={'R21':{'position_iu':[59300000,5600000],'orientation_degrees':0}} and plan['exact_mpn']=={'R21':'ERJ2RKF1001X'}
 assert len(plan['retired_copper'])==len({r['uuid'] for r in plan['retired_copper']})==2
 assert len(plan['added_copper'])==len({r['uuid'] for r in plan['added_copper']})==2
 assert sorted(r['signature'] for r in plan['retired_copper'])==sorted([['track','ROW_GATE_15',66750000,5000000,56750000,5000000,'B.Cu',200000],['track','ROW_GATE_15',66750000,5750000,66750000,5000000,'B.Cu',200000]])
 assert sorted(r['signature'] for r in plan['added_copper'])==sorted([['track','ROW_GATE_15',59800000,5600000,59800000,5000000,'B.Cu',200000],['track','ROW_GATE_15',59800000,5000000,56750000,5000000,'B.Cu',200000]])
 assert all(r['via_type'] is None for r in plan['added_copper']+plan['retired_copper'])
 assert len(plan['supply_source_contacts'])==3 and plan['new_supply_copper_mm']==0
 assert plan['expected_main_vled_pads']==36 and plan['new_gate_length_mm']==3.65 and plan['original_gate_length_mm']==10.75
 assert plan['external_gate_via_uuid']=='cb9294d1-c465-51d9-8d7a-b4344a70b4fc'
 assert set(plan['source_retirement_contacts'])=={r['uuid'] for r in plan['retired_copper']}
 for ext,digest in policy.PROFILES.items():assert policy.sha(policy.OUTPUT.with_suffix(ext))==digest and policy.PARENT.with_suffix(ext).read_bytes()==policy.OUTPUT.with_suffix(ext).read_bytes()
 c=runpy.run_path(str(policy.ROOT/'tools/check-coupon-study-contract.py'));data=json.loads(c['CONTRACT'].read_text());c['validate_contract'](data);result=c['compare'](data,c['read_board'](policy.OUTPUT));assert result['historical_legacy_rse_assignments']==[]
 print('R21: exact source/plan/board/profiles and canonical circuit pass; native continuity/DRC remain separate')

if __name__=='__main__':main()
