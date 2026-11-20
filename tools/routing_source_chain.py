# SPDX-License-Identifier: Apache-2.0
"""ADR 0061's exact original UART chain; no general source retirement."""
from collections import Counter
import hashlib
import json
import math
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
CATALOG=ROOT/'mechanical/review/routing-progress-source-chain.json'
CATALOG_SHA256='31c298d7c17971ad5b20634b99c7dccbc86d24a55be92142651a2fef148e7e5e'
ORIGINAL=[['track', 'UART0_TX_RAW', 51350000, 9000000, 51400000, 9000000, 'In4.Cu', 200000], ['track', 'UART0_TX_RAW', 51400000, 8950000, 51450000, 8950000, 'In4.Cu', 200000], ['track', 'UART0_TX_RAW', 51400000, 9000000, 51400000, 8950000, 'In4.Cu', 200000], ['track', 'UART0_TX_RAW', 51450000, 8900000, 51600000, 8900000, 'In4.Cu', 200000], ['track', 'UART0_TX_RAW', 51450000, 8950000, 51450000, 8900000, 'In4.Cu', 200000], ['track', 'UART0_TX_RAW', 51600000, 8850000, 52350000, 8850000, 'In4.Cu', 200000], ['track', 'UART0_TX_RAW', 51600000, 8900000, 51600000, 8850000, 'In4.Cu', 200000]]
INTERFACES=[(51350000,9000000),(52350000,8850000)]


def catalog():
    assert hashlib.sha256(CATALOG.read_bytes()).hexdigest()==CATALOG_SHA256, 'Source-chain catalog changed'
    return json.loads(CATALOG.read_text())


def validate_plan(plan,required=False):
    if 'source_chain_replacement' not in plan and not required:return Counter()
    entry=plan.get('source_chain_replacement')
    assert entry==catalog(), 'Exact source-chain catalog omitted or changed'
    assert entry['original']==ORIGINAL, 'Source-chain original inventory differs'
    assert entry['net']=='UART0_TX_RAW' and entry['layer']=='In4.Cu'
    assert entry['maximum_extra_trace_length_iu']==4000000
    rows=entry['replacement']
    assert len(rows)==33 and len(set(map(tuple,rows)))==33
    for row in rows:
        assert row[:2]==['track','UART0_TX_RAW'] and row[6:]==['In4.Cu',200000], 'Source-chain width/net/layer changed'
        assert all(type(x) is int for x in row[2:6]) and row[2:4]!=row[4:6]
        assert all(500000<=x<=113500000 for x in [row[2],row[4]]) and all(500000<=y<=32000000 for y in [row[3],row[5]])
    length=sum(math.dist(row[2:4],row[4:6]) for row in rows)
    original_length=sum(math.dist(row[2:4],row[4:6]) for row in ORIGINAL)
    assert length<=original_length+4000001, 'Source-chain length bound exceeded'
    assert not Counter(map(tuple,rows))-Counter(map(tuple,plan['added_copper'])), 'Source-chain replacement copper missing'
    assert not Counter(map(tuple,ORIGINAL))&Counter(map(tuple,plan['added_copper'])), 'Source-chain original restored'
    return Counter(map(tuple,ORIGINAL))


def verify_native(old,new,plan,signature,physical_identity,contacts):
    import pcbnew as p
    retired=validate_plan(plan)
    if not retired:return retired
    entry=plan['source_chain_replacement'];source=list(old.GetTracks());actual=list(new.GetTracks());actual_inventory=Counter(signature(new,t) for t in actual)
    assert not retired-Counter(signature(old,t) for t in source), 'Source-chain original absent from source'
    assert not retired&actual_inventory, 'Source-chain original restored'
    external={}
    for row in retired:
        original=next(t for t in source if signature(old,t)==row)
        for key,item in contacts(old,original,signature,physical_identity):
            if key[0]=='copper' and tuple(key[1:]) in retired:continue
            external[repr(key)]=(key,item)
    witnesses=sorted(external.values(),key=lambda pair:repr(pair[0]))
    assert [key for key,_ in witnesses]==entry['external_contacts'], 'Source-chain external contact inventory differs'
    wanted=Counter(map(tuple,entry['replacement']));replacement=[]
    for item in actual:
        row=signature(new,item)
        if wanted[row]:replacement.append(item);wanted[row]-=1
    assert not +wanted, 'Native source-chain replacement missing'
    for point in INTERFACES:
        dot=p.SHAPE_CIRCLE(p.VECTOR2I(*point),1)
        assert any(t.GetEffectiveShape(p.In4_Cu).Collide(dot,0) for t in replacement), 'Source-chain interface detached'
    for _,item in witnesses:
        assert any(t.GetEffectiveShape(p.In4_Cu).Collide(item.GetEffectiveShape(p.In4_Cu),0) for t in replacement), 'Source-chain external contact detached'
    return retired
