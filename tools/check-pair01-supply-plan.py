#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Portable frozen PAIR01 supply ledger and canonical circuit gate."""
import json,runpy
from collections import Counter
import routing_pair01_supply as policy

def main():
 plan=policy.load_plan();assert policy.sha(policy.OUTPUT)==policy.BOARD_SHA
 assert plan['expected_native_opens']==plan['expected_physical_opens']==23 and plan['expected_main_vled_pads']==38 and plan['expected_main_ground_pads']==197
 assert plan['poses']=={'PAIR01':dict(position_iu=[80000000,5200000],orientation_degrees=180,layer='F.Cu')}
 assert len(plan['retired_copper'])==len({r['uuid'] for r in plan['retired_copper']})==62
 oldpair=json.loads((policy.ROOT/'mechanical/review/pair01-front-ground-plan.json').read_text());r6=json.loads((policy.ROOT/'mechanical/review/r6-direct-bottom-plan.json').read_text())
 expected=oldpair['added_copper']+[r for r in r6['added_copper'] if r['signature'][:4]==['via','ROW_GATE_00',76600000,4300000] and r['signature'][4:6]==['F.Cu','In1.Cu']]
 assert plan['retired_copper']==expected
 assert len(plan['added_copper'])==len({r['uuid'] for r in plan['added_copper']})==27
 vias=[r for r in plan['added_copper'] if r['signature'][0]=='via'];assert len(vias)==5
 for r in vias:assert r['signature'][4:]==['F.Cu','In1.Cu',300000,100000] and r['via_type']==1
 assert plan['selector_route']['goal_witness_uuid']=='de96a271-92f1-5663-beaa-4f8a0e5658a4' and plan['selector_route']['additional_transitions']==3
 assert abs(plan['selector_route']['total_selector_conductor_mm']-4.099137802864838)<1e-12
 assert set(plan['source_retirement_contacts'])=={r['uuid'] for r in plan['retired_copper']}
 for ext,digest in policy.PROFILES.items():assert policy.sha(policy.OUTPUT.with_suffix(ext))==digest and policy.PARENT.with_suffix(ext).read_bytes()==policy.OUTPUT.with_suffix(ext).read_bytes()
 policy.serialized_ledger(policy.OUTPUT,plan)
 c=runpy.run_path(str(policy.ROOT/'tools/check-coupon-study-contract.py'));data=json.loads(c['CONTRACT'].read_text());c['validate_contract'](data);result=c['compare'](data,c['read_board'](policy.OUTPUT));assert result['historical_legacy_rse_assignments']==[]
 print('PAIR01 supply: frozen source/plan/board/profiles/raw Cu/canonical circuit pass; native gates remain separate')
if __name__=='__main__':main()
