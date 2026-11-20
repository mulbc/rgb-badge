#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Portable exact ordinary-routing source/ledger/circuit gate."""
import json
import runpy
import routing_ordinary as policy

def main():
 plan=policy.load_plan();assert policy.sha(policy.OUTPUT)==plan['expected_board_sha256']
 assert plan['native_opens']==plan['physical_opens']==31 and plan['source_groups']==220 and plan['poses']=={} and plan['retired_copper']==[]
 assert len(plan['added_copper'])==57 and len({r['uuid'] for r in plan['added_copper']})==57 and plan['allowed_nets']==['DISPLAY_CLEAR_OK'] and plan['original_contacts']
 assert plan['expected_terminal_groups']=={'DISPLAY_CLEAR_OK':[[['R108','1'],['U49','2'],['U52','4']],[['U50','2']]]}
 for row in plan['added_copper']:
  s=row['signature'];assert s[1]=='DISPLAY_CLEAR_OK'
  if s[0]=='track':assert s[7]==200000 and row['via_type'] is None
  else:
   stack=['F.Cu','In1.Cu','In2.Cu','In3.Cu','In4.Cu','B.Cu'];assert abs(stack.index(s[4])-stack.index(s[5]))==1
   if set(s[4:6])=={'In2.Cu','In3.Cu'}:assert row['via_type']==3 and s[6:]==[500000,300000]
   else:assert row['via_type']==1 and s[6:]==[300000,100000]
 for ext in ['.kicad_pro','.kicad_dru']:assert policy.PARENT.with_suffix(ext).read_bytes()==policy.OUTPUT.with_suffix(ext).read_bytes()
 c=runpy.run_path(str(policy.ROOT/'tools/check-coupon-study-contract.py'));data=json.loads(c['CONTRACT'].read_text());c['validate_contract'](data);result=c['compare'](data,c['read_board'](policy.OUTPUT));assert result['historical_legacy_rse_assignments']==[]
 print('Ordinary continuation: exact source/plan/board/profiles and canonical circuit pass; native continuity/DRC remain separate')
if __name__=='__main__':main()
