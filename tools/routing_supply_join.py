# SPDX-License-Identifier: Apache-2.0
"""Exact ADR 0070 additive gauge supply join; no electrical-limit exception."""
from collections import Counter
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
CATALOG=ROOT/'mechanical/review/routing-progress-gauge-supply-join.json'
CATALOG_SHA256='8adfc892c893cf0d8de0b5806e1e8c17fb36d2b4b2eac5896991ec023212ba3d'
REQUIRED={('SW2','7'),('C39','1'),('U46','1')}


def catalog():
    assert hashlib.sha256(CATALOG.read_bytes()).hexdigest()==CATALOG_SHA256, 'Gauge supply catalog changed'
    return json.loads(CATALOG.read_text())


def validate_plan(plan,required=False):
    if 'gauge_supply_join' not in plan and not required:return Counter()
    entry=plan.get('gauge_supply_join')
    assert entry==catalog(), 'Gauge supply catalog omitted or changed'
    assert entry['net']=='+BAT_GAUGE_SW' and set(map(tuple,entry['required_joined_pads']))==REQUIRED
    assert entry['track_width_iu']==200000 and entry['microvia_diameter_drill_iu']==[300000,100000]
    wanted=Counter(map(tuple,entry['added_copper']))
    assert sum(wanted.values())==14 and all(n==1 for n in wanted.values())
    assert sum(row[0]=='track' for row in wanted)==13
    for row in wanted:
        assert len(row)==8 and row[1]=='+BAT_GAUGE_SW'
        if row[0]=='track':assert row[7]==200000 and row[6] in ('B.Cu','In4.Cu') and row[2:4]!=row[4:6]
        else:assert row[0]=='via' and row[4:]==('In4.Cu','B.Cu',300000,100000)
    assert not wanted-Counter(map(tuple,plan['added_copper'])), 'Exact gauge supply copper missing'
    return wanted


def verify_join(board,physical_cluster):
    pads={}
    for ref,pin in sorted(REQUIRED):
        part=board.FindFootprintByReference(ref)
        assert part is not None, 'Gauge source component missing'
        matches=[q for q in part.Pads() if q.GetNumber()==pin]
        assert len(matches)==1, 'Gauge source pad missing or duplicated'
        pads[(ref,pin)]=matches[0]
    assert set(pads)==REQUIRED and all(q.GetNetname()=='+BAT_GAUGE_SW' for q in pads.values()), 'Gauge source pins differ'
    assert len({physical_cluster(board,q) for q in pads.values()})==1, 'Gauge switch supply not joined'


def verify_native(board,plan,signature,physical_cluster):
    wanted=validate_plan(plan,required=True)
    assert not wanted-Counter(signature(board,t) for t in board.GetTracks()), 'Native gauge supply copper missing'
    verify_join(board,physical_cluster)
    return sum(wanted.values())
