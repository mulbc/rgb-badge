#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Portable exact front-side R11 relocation ledger and circuit contract."""
import json,runpy
import routing_r11_front as policy

def main():
 plan=policy.load_plan();assert policy.sha(policy.OUTPUT)==policy.BOARD_SHA
 assert plan['source_groups']==215 and plan['source_copper']==19381 and plan['native_opens']==plan['physical_opens']==26
 assert plan['poses']=={'R11':{'position_iu':[78850000,9100000],'orientation_degrees':180,'layer':'F.Cu','flip':'top-bottom'}} and plan['exact_mpn']=={'R11':'ERJ2RKF1001X'}
 assert len(plan['retired_copper'])==len({r['uuid'] for r in plan['retired_copper']})==25 and sum(r['via_type'] is not None for r in plan['retired_copper'])==5
 assert len(plan['added_copper'])==1 and plan['added_copper'][0]['signature']==['track','ROW_GATE_05',78350000,9100000,78300000,10800000,'F.Cu',200000] and plan['added_copper'][0]['via_type'] is None
 assert plan['new_supply_copper_mm']==0 and plan['expected_main_vled_pads']==37 and abs(plan['new_gate_length_mm']-1.7007351351694948)<1e-12
 assert plan['supply_source_uuid']=='9e97b5ce-a21b-5767-80bb-e30b1564a12d' and set(plan['source_retirement_contacts'])=={r['uuid'] for r in plan['retired_copper']}
 for ext,digest in policy.PROFILES.items():assert policy.sha(policy.OUTPUT.with_suffix(ext))==digest and policy.PARENT.with_suffix(ext).read_bytes()==policy.OUTPUT.with_suffix(ext).read_bytes()
 c=runpy.run_path(str(policy.ROOT/'tools/check-coupon-study-contract.py'));data=json.loads(c['CONTRACT'].read_text());c['validate_contract'](data);result=c['compare'](data,c['read_board'](policy.OUTPUT));assert result['historical_legacy_rse_assignments']==[]
 print('R11 front: exact source/plan/board/profiles and canonical circuit pass; native gates remain separate')
if __name__=='__main__':main()
