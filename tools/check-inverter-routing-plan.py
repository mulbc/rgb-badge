#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Portable exact inverter/clock routing source, ledger and circuit gate."""
import json
import math
import runpy
import routing_inverter as policy

def main():
 plan=policy.load_plan();assert policy.sha(policy.OUTPUT)==policy.BOARD_SHA
 assert plan['native_opens']==plan['physical_opens']==29 and plan['source_groups']==218
 assert plan['poses']=={'U48':{'position_iu':[110000000,28150000],'orientation_degrees':270},'C67':{'position_iu':[109450000,29950000],'orientation_degrees':180}}
 assert {r['uuid'] for r in plan['retired_copper']}=={'15606914-5a77-520f-891e-15e122b1afc8','0f1184fa-3b7b-5bbc-9b14-39fb0d58d95c'} and len(plan['added_copper'])==29
 assert len({r['uuid'] for r in plan['added_copper']})==29 and plan['source_retirement_contacts'] and plan['clock_pads']==[['U48','4'],['U49','7']]
 narrow=[]
 for row in plan['added_copper']:
  s=row['signature'];assert s[1] in ['+3V3_APP','GND','HEARTBEAT_FALL_CLK']
  if s[0]=='track':
   assert s[7] in [120000,200000]
   if s[7]==120000:
    assert s[1] in ['+3V3_APP','GND','HEARTBEAT_FALL_CLK'] and s[6]=='B.Cu';narrow.append(s)
  else:
   stack=['F.Cu','In1.Cu','In2.Cu','In3.Cu','In4.Cu','B.Cu'];assert abs(stack.index(s[4])-stack.index(s[5]))==1
   if set(s[4:6])=={'In2.Cu','In3.Cu'}:assert row['via_type']==3 and s[6:]==[500000,300000]
   else:assert row['via_type']==1 and s[6:]==[300000,100000]
 assert len(narrow)==3 and all(abs(math.dist(s[2:4],s[4:6])/1e6-.1)<1e-8 for s in narrow)
 for ext in ['.kicad_pro','.kicad_dru']:assert policy.PARENT.with_suffix(ext).read_bytes()==policy.OUTPUT.with_suffix(ext).read_bytes()
 c=runpy.run_path(str(policy.ROOT/'tools/check-coupon-study-contract.py'));data=json.loads(c['CONTRACT'].read_text());c['validate_contract'](data);result=c['compare'](data,c['read_board'](policy.OUTPUT));assert result['historical_legacy_rse_assignments']==[]
 print('Inverter routing: exact source/plan/board/profiles and canonical circuit pass; native continuity/DRC remain separate')
if __name__=='__main__':main()
