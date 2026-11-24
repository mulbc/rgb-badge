#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Portable source/fingerprint gate for the exact corrected RSE checkpoint."""
from collections import Counter
import hashlib
import json
from pathlib import Path
import runpy

ROOT=Path(__file__).resolve().parents[1]
PLAN=ROOT/'mechanical/review/rse-pin-migration-plan.json'
BOARD=ROOT/'hardware/coupon/rev-a/staging/led-rse-corrected-routing-trial-114mm.kicad_pcb'
PARENT=ROOT/'hardware/coupon/rev-a/staging/led-remaining-routing-trial-114mm.kicad_pcb'
PLAN_SHA='ca2a86c6678f237fdfbfc29c7c9bbf9426083f1d25fde777268564ecb5777157'
BOARD_SHA='3967bb66e89e0005f6859ce78a766b4536d06883b76fce130e75a6fdeefaf96e'
PARENT_SHA='da3764ddf5c8c615529340c33c92974cff3fd036b937b5e4a53c408e0b141637'


def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    assert sha(PLAN)==PLAN_SHA and sha(BOARD)==BOARD_SHA and sha(PARENT)==PARENT_SHA
    plan=json.loads(PLAN.read_text())
    assert plan['source_sha256']==PARENT_SHA
    assert plan['native_opens']==plan['physical_opens']==35 and plan['source_semantic_groups']==223
    assert plan['fabrication_release_allowed'] is False
    assert len(plan['added_copper'])==73 and len(plan['retired_copper'])==8
    ids=[r['uuid'] for key in ('added_copper','retired_copper') for r in plan[key]]
    assert len(ids)==len(set(ids))
    layers=['F.Cu','In1.Cu','In2.Cu','In3.Cu','In4.Cu','B.Cu']
    for entry in plan['added_copper']:
        row=entry['signature'];assert row[1] in {'+3V3_APP','DISPLAY_CLEAR_OK','DISPLAY_ARM_CLK','ARM_LATCH'}
        if row[0]=='track':
            assert len(row)==8 and row[-1]==200000 and row[2:4]!=row[4:6]
            assert all(type(q) is int for q in row[2:6])
        else:
            assert row[0]=='via' and len(row)==8 and row[-2:]==[300000,100000]
            assert abs(layers.index(row[4])-layers.index(row[5]))==1
            assert set(row[4:6])!={'In2.Cu','In3.Cu'}
    for ext in ('.kicad_pro','.kicad_dru'):
        assert BOARD.with_suffix(ext).read_bytes()==PARENT.with_suffix(ext).read_bytes()
    c=runpy.run_path(str(ROOT/'tools/check-coupon-study-contract.py'))
    data=json.loads(c['CONTRACT'].read_text());c['validate_contract'](data)
    current=c['compare'](data,c['read_board'](BOARD))
    assert current['historical_legacy_rse_assignments']==[]
    old=c['compare'](data,c['read_board'](PARENT),legacy_rse_study=True)
    assert old['historical_legacy_rse_assignments']==['U49','U50']
    print('Corrected RSE checkpoint: exact source/plan/profile fingerprints, canonical pins and explicit historical boundary passed; native checks remain separate')


if __name__=='__main__':main()
