#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Portable fingerprint/circuit gate; native geometry remains a separate check."""
from collections import Counter
import json
import math
import runpy
import routing_usb_en1 as policy

BOARD_SHA='92f942e46281475cbdadf6e9a0ad7a0d531e38c3032f85a4206bbf9e9bc1fccd'


def main():
    plan=policy.load_plan()
    assert policy.sha(policy.OUTPUT)==BOARD_SHA
    assert plan['native_opens']==plan['physical_opens']==34
    assert set(plan['poses'])=={'R70','TP31'}
    assert plan['poses']['R70']['position_iu']==[10550000,6500000] and plan['poses']['R70']['angle_deg']%360==270
    assert plan['poses']['TP31']['position_iu']==[11900000,7750000] and plan['poses']['TP31']['angle_deg']%360==180
    assert len(plan['retired_copper'])==3 and {r['uuid'] for r in plan['retired_copper']}==policy.RETIRED
    assert len(plan['added_copper'])==11 and len({r['uuid'] for r in plan['added_copper']})==11
    assert set(plan['original_contacts'])==policy.RETIRED
    rows=Counter()
    assert {r['role'] for r in plan['branches']}=={'supply','output','test'}
    for branch in plan['branches']:
        points=branch['points_iu']
        assert all(type(q) is int for point in points for q in point)
        assert sum(math.dist(a,b) for a,b in zip(points,points[1:]))<=16000000
        for (x,y),(a,b) in zip(points,points[1:]):rows[('track',branch['net'],x,y,a,b,'B.Cu',200000)]+=1
    assert rows==Counter(tuple(r['signature']) for r in plan['added_copper'])
    for ext in ['.kicad_pro','.kicad_dru']:
        assert policy.PARENT.with_suffix(ext).read_bytes()==policy.OUTPUT.with_suffix(ext).read_bytes()
    c=runpy.run_path(str(policy.ROOT/'tools/check-coupon-study-contract.py'))
    data=json.loads(c['CONTRACT'].read_text());c['validate_contract'](data)
    result=c['compare'](data,c['read_board'](policy.OUTPUT))
    assert result['historical_legacy_rse_assignments']==[]
    print('USB EN1: exact source/plan/profile fingerprints and canonical circuit passed; native/physical continuity and DRC require the native gate')


if __name__=='__main__':main()
