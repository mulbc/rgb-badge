#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Portable PAIR03 additive ledger and unchanged canonical circuit gate."""
import runpy
import json
import routing_pair03_supply as policy

def main():
 plan=policy.load_plan();assert policy.sha(policy.OUTPUT)==policy.BOARD_SHA
 assert plan['expected_native_opens']==plan['expected_physical_opens']==22 and plan['expected_main_vled_pads']==39 and plan['expected_main_ground_pads']==197
 rows=plan['added_copper'];assert len(rows)==len({r['uuid'] for r in rows})==18
 vias=[r for r in rows if r['signature'][0]=='via'];assert len(vias)==1 and vias[0]['signature']==['via','VLED',77800000,10075000,'In4.Cu','B.Cu',300000,100000] and vias[0]['via_type']==1
 tracks=[r for r in rows if r['signature'][0]=='track'];assert len(tracks)==17
 assert all(r['signature'][1]=='VLED' and r['signature'][6] in ['B.Cu','In4.Cu'] and r['signature'][7]==200000 and r['via_type'] is None for r in tracks)
 assert plan['route']['goal_witness_uuid']=='85ad9ca5-5c6b-5aa4-a068-b51753571be9'
 policy.serialized_ledger(policy.OUTPUT,plan);assert policy.fixed_structure(policy.PARENT)==policy.fixed_structure(policy.OUTPUT)
 for ext,digest in policy.PROFILES.items():assert policy.sha(policy.OUTPUT.with_suffix(ext))==digest and policy.PARENT.with_suffix(ext).read_bytes()==policy.OUTPUT.with_suffix(ext).read_bytes()
 c=runpy.run_path(str(policy.ROOT/'tools/check-coupon-study-contract.py'));data=json.loads(c['CONTRACT'].read_text());c['validate_contract'](data);result=c['compare'](data,c['read_board'](policy.OUTPUT));assert result['historical_legacy_rse_assignments']==[]
 print('PAIR03 supply: frozen source/plan/profiles, exact additive raw Cu, all fixed declarations and canonical circuit pass; native gates remain separate')
if __name__=='__main__':main()
