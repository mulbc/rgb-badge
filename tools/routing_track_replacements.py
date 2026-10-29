# SPDX-License-Identifier: Apache-2.0
"""Exact ADR 0053 source-track substitutions; no general deletion exception."""
from collections import Counter
import hashlib
import json
import math
import runpy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT/'mechanical/review/routing-progress-track-replacements.json'
CATALOG_SHA256 = 'ce082f65a6e1b3636a13a6699e8e18925d73ef82067627cd17b1ba7c39d11343'


def catalog():
    assert hashlib.sha256(CATALOG.read_bytes()).hexdigest() == CATALOG_SHA256, 'Replacement catalog changed'
    return json.loads(CATALOG.read_text())['replacements']


def validate_plan(plan, required=False):
    if 'track_replacements' not in plan and not required:
        return Counter()
    entries = plan.get('track_replacements', [])
    assert entries == catalog(), 'Exact replacement catalog omitted or changed'
    retired = Counter(tuple(entry['original']) for entry in entries)
    assert all(n == 1 and row[0] == 'track' and row[1].startswith(('COL_', 'ROW_SEL_', 'ROW_GATE_')) and row[7] == 200000 for row,n in retired.items())
    added = Counter(map(tuple, plan['added_copper']))
    for entry in entries:
        rows = entry['replacement'] + entry['connection']
        assert not Counter(map(tuple, rows))-added, 'Reviewed replacement or connection copper missing'
        assert entry['junction_contacts'], 'Replacement junction inventory missing'
        for row in entry['replacement']:
            assert row[1] == entry['original'][1]
            assert (row[0] == 'track' and row[7] == 200000) or (row[0] == 'via' and row[6:] == [300000,100000])
    # ADRs 0062/0063 permit only these exact full-width colour transfers.
    transfers={
        'COL_10_R':['track','COL_10_R',83750000,1100000,70250000,1100000,'In4.Cu',200000],
        'COL_03_B':['track','COL_03_B',81700000,12100000,78300000,12100000,'In4.Cu',200000],
    }
    for entry in entries:
        net=entry['original'][1]
        if net not in transfers:
            continue
        original=transfers[net]
        assert entry['original']==original, 'Unreviewed colour-transfer original'
        tracks=[row for row in entry['replacement'] if row[0]=='track']
        assert sum(math.dist(row[2:4],row[4:6]) for row in tracks)<=math.dist(original[2:4],original[4:6])+2000000.01, 'Colour-transfer length bound exceeded'
        excursion=[row for row in tracks if row[6]!='In4.Cu']
        assert excursion, 'Colour-transfer excursion omitted'
        xs=[row[i] for row in excursion for i in (2,4)]
        assert max(xs)-min(xs)<=2000000, 'Colour-transfer interval too wide'
        assert all(min(original[2],original[4])<=row[i]<=max(original[2],original[4]) for row in tracks for i in (2,4)), 'Colour-transfer outside original extent'
        assert all(abs(row[i]-original[3])<=1000000 for row in tracks for i in (3,5)), 'Colour-transfer local region exceeded'
    return retired+runpy.run_path(str(ROOT/'tools/routing_source_chain.py'))['validate_plan'](plan)


def contacts(board, original, signature, physical_identity):
    """Direct source-layer contacts, including interior crossings, not a cluster query."""
    import pcbnew as p
    layer = original.GetLayer()
    shape = original.GetEffectiveShape(layer)
    result = []
    for item in list(board.GetTracks())+[q for f in board.GetFootprints() for q in f.Pads()]:
        if item.m_Uuid.AsString() == original.m_Uuid.AsString() or item.GetNetCode() != original.GetNetCode() or not item.IsOnLayer(layer):
            continue
        if isinstance(item,p.PCB_TRACK) and not isinstance(item,p.PCB_VIA) and item.GetStart() == item.GetEnd():
            continue  # Separately proved neutral source artifacts.
        if not shape.Collide(item.GetEffectiveShape(layer),0):
            continue
        key = ['pad',*physical_identity(item)] if isinstance(item,p.PAD) else ['copper',*signature(board,item)]
        result.append((json.loads(json.dumps(key)),item))
    return sorted(result,key=lambda row:repr(row[0]))


def verify_native(old, new, plan, signature, physical_identity):
    import pcbnew as p
    retired = validate_plan(plan,required=True)
    source = Counter(signature(old,t) for t in old.GetTracks())
    actual = Counter(signature(new,t) for t in new.GetTracks())
    assert not retired-source, 'Replacement original absent from frozen source'
    assert not any(actual[row] for row in retired), 'Replaced original restored'
    items = list(new.GetTracks())
    for entry in plan['track_replacements']:
        original = next(t for t in old.GetTracks() if signature(old,t) == tuple(entry['original']))
        witnesses = contacts(old,original,signature,physical_identity)
        assert [key for key,item in witnesses] == entry['junction_contacts'], 'Source junction inventory differs'
        wanted = Counter(map(tuple,entry['replacement']))
        replacement = []
        for t in items:
            key = signature(new,t)
            if wanted[key]:
                replacement.append(t);wanted[key]-=1
        assert not +wanted, 'Native replacement copper missing'
        layer = original.GetLayer()
        on_layer = [t for t in replacement if t.IsOnLayer(layer)]
        for point in [original.GetStart(),original.GetEnd()]:
            dot = p.SHAPE_CIRCLE(point,1)
            assert any(t.GetEffectiveShape(layer).Collide(dot,0) for t in on_layer), 'Original-layer endpoint detached'
        for key,item in witnesses:
            assert any(t.GetEffectiveShape(layer).Collide(item.GetEffectiveShape(layer),0) for t in on_layer), 'Original-layer junction detached'
    runpy.run_path(str(ROOT/'tools/routing_source_chain.py'))['verify_native'](old,new,plan,signature,physical_identity,contacts)
    return retired
