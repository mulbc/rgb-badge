#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Portable exact row-two exchange, source ledger and circuit gate."""
import json
import runpy
import routing_row2 as policy

def main():
 plan=policy.load_plan();assert policy.sha(policy.OUTPUT)==policy.BOARD_SHA
 assert plan['native_opens']==plan['physical_opens']==28 and plan['source_groups']==217
 assert plan['poses']=={'R8':{'position_iu':[72575000,8000000],'orientation_degrees':90},'R37':{'position_iu':[72200000,9500000],'orientation_degrees':180}}
 assert len(plan['retired_copper'])==19 and len(plan['added_copper'])==4 and len(plan['external_selector_tracks'])==6 and len(plan['old_ground_tracks'])==4
 assert len({r['uuid'] for r in plan['retired_copper']})==19 and len({r['uuid'] for r in plan['added_copper']})==4
 for r in plan['retired_copper']:assert r['signature'][0:2]==['track','ROW_SEL_15'] and r['signature'][6:]==['B.Cu',200000] and r['via_type'] is None
 tracks=[];vias=[]
 for r in plan['added_copper']:
  s=r['signature']
  if s[0]=='track':assert s[7]==200000 and r['via_type'] is None;tracks.append(s)
  else:assert s[1]=='ROW_GATE_02' and s[4:]==['In4.Cu','B.Cu',300000,100000] and r['via_type']==1;vias.append(s)
 assert len(vias)==2 and {tuple(s[2:4]) for s in vias}=={(72575000,7500000),(74825000,7500000)}
 assert sorted(tracks)==sorted([['track','ROW_GATE_02',72575000,7500000,74825000,7500000,'In4.Cu',200000],['track','ROW_SEL_15',72700000,9500000,73550000,9049999,'B.Cu',200000]])
 for ext in ['.kicad_pro','.kicad_dru']:assert policy.PARENT.with_suffix(ext).read_bytes()==policy.OUTPUT.with_suffix(ext).read_bytes()
 c=runpy.run_path(str(policy.ROOT/'tools/check-coupon-study-contract.py'));data=json.loads(c['CONTRACT'].read_text());c['validate_contract'](data);result=c['compare'](data,c['read_board'](policy.OUTPUT));assert result['historical_legacy_rse_assignments']==[]
 print('Row-two exchange: exact source/plan/board/profiles and canonical circuit pass; native continuity/DRC remain separate')
if __name__=='__main__':main()
