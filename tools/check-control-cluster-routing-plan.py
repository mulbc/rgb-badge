#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Portable frozen source/ledger/circuit gate; native checks remain mandatory."""
import json
import math
import runpy
import routing_control_cluster as policy

def main():
 plan=policy.load_plan();assert policy.sha(policy.OUTPUT)==policy.BOARD_SHA
 assert plan['native_opens']==plan['physical_opens']==32 and plan['source_groups']==221 and plan['net_count']==188
 assert plan['poses']=={'U52':{'position_iu':[103200000,5275000],'orientation_degrees':90},'C71':{'position_iu':[103000000,6750000],'orientation_degrees':180}}
 assert len(plan['retired_copper'])==11 and len(plan['added_copper'])==59
 retired={r['uuid'] for r in plan['retired_copper']};assert len(retired)==11 and plan['source_retirement_contacts'].keys()==retired
 assert len({r['uuid'] for r in plan['added_copper']})==59
 narrow=[];vias=[]
 for row in plan['added_copper']:
  s=row['signature']
  if s[0]=='track':
   assert s[7] in [120000,200000]
   if s[7]==120000:
    assert s[1] in ['+3V3_APP','GND','DISPLAY_CLEAR_3'] and s[6]=='B.Cu' and math.dist(s[2:4],s[4:6])<=750000;narrow.append(row)
  else:
   vias.append(row);span=set(s[4:6])
   if span=={'In2.Cu','In3.Cu'}:assert row['via_type']==3 and s[6:]==[500000,300000]
   else:assert span in [{'B.Cu','In4.Cu'},{'In4.Cu','In3.Cu'},{'In2.Cu','In1.Cu'}] and row['via_type']==1 and s[6:]==[300000,100000]
 assert len(narrow)==3 and len(vias)==12
 for ext in ['.kicad_pro','.kicad_dru']:assert policy.PARENT.with_suffix(ext).read_bytes()==policy.OUTPUT.with_suffix(ext).read_bytes()
 c=runpy.run_path(str(policy.ROOT/'tools/check-coupon-study-contract.py'));data=json.loads(c['CONTRACT'].read_text());c['validate_contract'](data);result=c['compare'](data,c['read_board'](policy.OUTPUT));assert result['historical_legacy_rse_assignments']==[]
 print('Control cluster: exact source/plan/board/profiles and canonical circuit pass; native continuity/DRC remain separate')
if __name__=='__main__':main()
