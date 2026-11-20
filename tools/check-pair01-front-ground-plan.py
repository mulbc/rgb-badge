#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Portable frozen PAIR01 front ground ledger and canonical circuit gate."""
import json,runpy
from collections import Counter
import routing_pair01_front_ground as policy

def main():
 plan=policy.load_plan();assert policy.sha(policy.OUTPUT)==policy.BOARD_SHA
 assert plan['expected_native_opens']==plan['expected_physical_opens']==25
 assert plan['poses']=={'PAIR01':dict(position_iu=[76100000,4300000],orientation_degrees=270,layer='F.Cu',flip='top-bottom')}
 assert len(plan['retired_copper'])==len({r['uuid'] for r in plan['retired_copper']})==38 and Counter(r['signature'][1] for r in plan['retired_copper'])=={'ROW_SEL_00':32,'ROW_00_A':4,'ROW_GATE_00':2}
 assert len(plan['added_copper'])==len({r['uuid'] for r in plan['added_copper']})==61 and all(r['signature'][1]!='VLED' for r in plan['added_copper'])
 vias=[r for r in plan['added_copper'] if r['signature'][0]=='via'];assert len(vias)==2 and {tuple(r['signature']) for r in vias}=={('via','GND',76750000,3375000,'F.Cu','In1.Cu',300000,100000),('via','ROW_SEL_00',76100000,3375000,'F.Cu','In1.Cu',300000,100000)} and all(r['via_type']==1 for r in vias)
 assert set(plan['source_retirement_contacts'])=={r['uuid'] for r in plan['retired_copper']}
 for ext,digest in policy.PROFILES.items():assert policy.sha(policy.OUTPUT.with_suffix(ext))==digest and policy.PARENT.with_suffix(ext).read_bytes()==policy.OUTPUT.with_suffix(ext).read_bytes()
 policy.serialized_ledger(policy.OUTPUT,plan)
 c=runpy.run_path(str(policy.ROOT/'tools/check-coupon-study-contract.py'));data=json.loads(c['CONTRACT'].read_text());c['validate_contract'](data);result=c['compare'](data,c['read_board'](policy.OUTPUT));assert result['historical_legacy_rse_assignments']==[]
 print('PAIR01 front ground: frozen source/plan/board/profiles/raw copper/canonical circuit pass; native gates remain separate')
if __name__=='__main__':main()
