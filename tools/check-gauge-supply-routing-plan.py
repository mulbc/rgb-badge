#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Portable exact-fingerprint and unchanged-circuit gate for ADR 0124."""
import json
import runpy
import routing_gauge_supply as policy
BOARD_SHA='14f0c49582063bab84ea685a8cec798011eb4cd66389b085a3a47777180a13ce'
def main():
    plan=policy.load_plan();assert policy.sha(policy.OUTPUT)==BOARD_SHA
    assert plan['native_opens']==plan['physical_opens']==33 and plan['poses']=={} and plan['retired_copper']==[]
    assert len(plan['added_copper'])==114 and len({r['uuid'] for r in plan['added_copper']})==114
    assert all(r['signature'][1]=='+BAT_GAUGE_SW' for r in plan['added_copper'])
    assert sum(r['signature'][0]=='via' for r in plan['added_copper'])==9
    assert plan['original_contacts'] and len(plan['target_pads'])==6
    assert plan['gauge_supply_device_group_still_open']==[['U35','2'],['U35','3']]
    for ext in ['.kicad_pro','.kicad_dru']:assert policy.PARENT.with_suffix(ext).read_bytes()==policy.OUTPUT.with_suffix(ext).read_bytes()
    c=runpy.run_path(str(policy.ROOT/'tools/check-coupon-study-contract.py'));data=json.loads(c['CONTRACT'].read_text());c['validate_contract'](data);result=c['compare'](data,c['read_board'](policy.OUTPUT));assert result['historical_legacy_rse_assignments']==[]
    print('Gauge supply: frozen source/plan/board/profiles and canonical circuit pass; native continuity/DRC remain separate')
if __name__=='__main__':main()
