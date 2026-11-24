#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Portable frozen R6 direct-supply ledger and canonical circuit gate."""
import json,runpy
from collections import Counter
import routing_r6_direct_bottom as policy

def main():
 plan=policy.load_plan();assert policy.sha(policy.OUTPUT)==policy.BOARD_SHA
 assert plan['expected_native_opens']==plan['expected_physical_opens']==24 and plan['expected_main_vled_pads']==37 and plan['expected_main_ground_pads']==197
 assert plan['poses']=={'R6':dict(position_iu=[77750000,5600000],orientation_degrees=90,layer='B.Cu')}
 assert len(plan['retired_copper'])==len({r['uuid'] for r in plan['retired_copper']})==6 and {r['signature'][1] for r in plan['retired_copper']}=={'VLED'}
 assert len(plan['added_copper'])==len({r['uuid'] for r in plan['added_copper']})==10
 vias=[r for r in plan['added_copper'] if r['signature'][0]=='via'];assert len(vias)==5 and Counter(tuple(r['signature'][4:6]) for r in vias)=={('F.Cu','In1.Cu'):1,('In1.Cu','In2.Cu'):1,('In2.Cu','In3.Cu'):1,('In3.Cu','In4.Cu'):1,('In4.Cu','B.Cu'):1}
 for r in vias:
  assert r['signature'][1]=='ROW_GATE_00'
  if r['signature'][4:6]==['In2.Cu','In3.Cu']:assert r['signature'][6:]==[500000,300000] and r['via_type']==3
  else:assert r['signature'][6:]==[300000,100000] and r['via_type']==1
 assert plan['supply_source_pad_uuid']=='75480661-8dea-5444-ac43-3481bde8d9b8' and abs(plan['new_supply_length_mm']-1.2075284675733322)<1e-12 and abs(plan['new_gate_length_mm']-2.224774058770734)<1e-12
 assert set(plan['source_retirement_contacts'])=={r['uuid'] for r in plan['retired_copper']}
 for ext,digest in policy.PROFILES.items():assert policy.sha(policy.OUTPUT.with_suffix(ext))==digest and policy.PARENT.with_suffix(ext).read_bytes()==policy.OUTPUT.with_suffix(ext).read_bytes()
 policy.serialized_ledger(policy.OUTPUT,plan)
 c=runpy.run_path(str(policy.ROOT/'tools/check-coupon-study-contract.py'));data=json.loads(c['CONTRACT'].read_text());c['validate_contract'](data);result=c['compare'](data,c['read_board'](policy.OUTPUT));assert result['historical_legacy_rse_assignments']==[]
 print('R6 direct bottom: frozen source/plan/board/profiles/raw Cu/canonical circuit pass; native gates remain separate')
if __name__=='__main__':main()
