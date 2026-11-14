#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Portable exact bypass/enable routing source, ledger and circuit gate."""
import json
import math
import runpy
import routing_enable as policy

def main():
 plan=policy.load_plan();assert policy.sha(policy.OUTPUT)==policy.BOARD_SHA
 assert plan['native_opens']==plan['physical_opens']==30 and plan['source_groups']==219
 assert plan['poses']=={'C71':{'position_iu':[102500000,6750000],'orientation_degrees':180}}
 assert {r['uuid'] for r in plan['retired_copper']}=={'cae1dd88-576d-5a0f-8616-ca4000e8c5d3','d9e75938-e0d3-5aca-8c05-4e7264aa3a24'} and len(plan['added_copper'])==88
 assert len({r['uuid'] for r in plan['added_copper']})==88 and plan['source_retirement_contacts'] and ['U52','2'] in plan['enable_pads']
 narrow=[]
 for row in plan['added_copper']:
  s=row['signature'];assert s[1] in ['+3V3_APP','GND','DISPLAY_ENABLE']
  if s[0]=='track':
   assert s[7] in [120000,200000]
   if s[7]==120000:
    assert s[1]=='DISPLAY_ENABLE' and s[6]=='B.Cu';narrow.append(s)
  else:
   stack=['F.Cu','In1.Cu','In2.Cu','In3.Cu','In4.Cu','B.Cu'];assert abs(stack.index(s[4])-stack.index(s[5]))==1
   if set(s[4:6])=={'In2.Cu','In3.Cu'}:assert row['via_type']==3 and s[6:]==[500000,300000]
   else:assert row['via_type']==1 and s[6:]==[300000,100000]
 assert len(narrow)==2 and .7363405<sum(math.dist(s[2:4],s[4:6])/1e6 for s in narrow)<.7363407
 for ext in ['.kicad_pro','.kicad_dru']:assert policy.PARENT.with_suffix(ext).read_bytes()==policy.OUTPUT.with_suffix(ext).read_bytes()
 c=runpy.run_path(str(policy.ROOT/'tools/check-coupon-study-contract.py'));data=json.loads(c['CONTRACT'].read_text());c['validate_contract'](data);result=c['compare'](data,c['read_board'](policy.OUTPUT));assert result['historical_legacy_rse_assignments']==[]
 print('Enable routing: exact source/plan/board/profiles and canonical circuit pass; native continuity/DRC remain separate')
if __name__=='__main__':main()
