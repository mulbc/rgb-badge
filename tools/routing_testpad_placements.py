# SPDX-License-Identifier: Apache-2.0
"""ADR 0055's exact isolated test-land poses; no general placement exception."""
from collections import Counter
import hashlib
import json
import math
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
CATALOG=ROOT/'mechanical/review/routing-progress-testpad-placements.json'
CATALOG_SHA256='e7d5b933844d6b19843c2dfdae954f47dcbd68a328b793bd9c595ee5ad977dfc'
FROZEN=ROOT/'mechanical/review/routing-progress-69-checkpoint.json'
FROZEN_SHA256='4afcfc21c9c28463a9b0a4d58a85fe82428ab5ae3b10b27347b9de1000473086'
NETS={'TP1':'LED_SOUT','TP2':'ESP_EN','TP4':'UART0_TX','TP11':'SYS_I2C_SDA',
      'TP13':'VLED_ENABLE_CANDIDATE','TP14':'ROW_ENABLE_N_CANDIDATE','TP20':'USB_RAW_OUT1'}


def catalog():
    assert hashlib.sha256(CATALOG.read_bytes()).hexdigest()==CATALOG_SHA256,'Testpad catalog changed'
    return json.loads(CATALOG.read_text())['testpads']


def validate_plan(plan,required=False):
    if 'testpad_placements' not in plan and not required:return []
    entries=plan.get('testpad_placements',[])
    assert entries==catalog(),'Exact testpad catalog omitted or changed'
    added=Counter(map(tuple,plan['added_copper']));seen=set()
    for entry in entries:
        ref=entry['reference'];assert ref in NETS and ref not in seen and entry['net']==NETS[ref]
        seen.add(ref)
        assert entry['old_angle_deg']==entry['new_angle_deg']
        for field in ['old_position_iu','new_position_iu']:
            assert len(entry[field])==2 and all(type(v) is int for v in entry[field])
        x,y=entry['new_position_iu'];assert 1250000<=x<=112750000 and 1250000<=y<=31250000
        assert entry['joined_source_group'] and all(row[0]!=ref for row in entry['joined_source_group'])
        assert not Counter(map(tuple,entry['connection']))-added,'Testpad lead missing'
        length=0
        for row in entry['connection']:
            assert len(row)==8 and row[0]=='track' and row[1]==entry['net'] and row[6]=='B.Cu' and row[7]==200000
            assert row[2:4]!=row[4:6]
            length+=math.hypot(row[2]-row[4],row[3]-row[5])
        assert length<=3000000,'Testpad lead exceeds 3 mm'
    return entries


def verify_native(old,new,plan,signature,physical_identity,physical_cluster):
    import pcbnew as p
    entries=validate_plan(plan,required=True)
    assert hashlib.sha256(FROZEN.read_bytes()).hexdigest()==FROZEN_SHA256
    prior=json.loads(FROZEN.read_text())
    retired=Counter(map(tuple,prior['retired_orphan_microvias']))
    retired.update(tuple(entry['original']) for entry in prior['track_replacements'])
    originals=[t for t in old.GetTracks() if not retired[signature(old,t)] and
               (isinstance(t,p.PCB_VIA) or t.GetStart()!=t.GetEnd())]
    needed=Counter(map(tuple,prior['added_copper']));added=[]
    for item in new.GetTracks():
        key=signature(new,item)
        if needed[key]:added.append(item);needed[key]-=1
    assert not +needed,'Frozen 69-edge additions missing'
    old_parts={f.GetReference():f for f in old.GetFootprints()}
    new_parts={f.GetReference():f for f in new.GetFootprints()}
    for entry in entries:
        ref=entry['reference'];before=list(old_parts[ref].Pads());after=list(new_parts[ref].Pads())
        assert len(before)==len(after)==1 and before[0].GetNumber()==after[0].GetNumber()=='1'
        pad,q=before[0],after[0]
        assert pad.GetNetname()==q.GetNetname()==entry['net']
        assert pad.GetSize()==q.GetSize()==p.VECTOR2I(1000000,1000000)
        assert pad.GetShape()==q.GetShape()==p.PAD_SHAPE_CIRCLE
        assert old_parts[ref].GetFPIDAsString()==new_parts[ref].GetFPIDAsString()=='rgb-badge-coupon:TestPoint_Pad_D1.0mm'
        assert old_parts[ref].GetLayer()==new_parts[ref].GetLayer()==p.B_Cu
        assert len(physical_cluster(old,pad))==1,'Testpad originally joined a source group'
        key=physical_identity(pad)
        for net,before_group,after_group in prior['physical_group_witnesses']:
            assert key not in set(map(tuple,after_group)) or len(after_group)==1,'Testpad already joined at 69 edges'
        shape=pad.GetEffectiveShape(p.B_Cu);box=pad.GetBoundingBox()
        for item in originals+added:
            if item.IsOnLayer(p.B_Cu) and box.Intersects(item.GetBoundingBox()):
                assert not shape.Collide(item.GetEffectiveShape(p.B_Cu),0),'Testpad originally contacted copper'
        group=physical_cluster(new,q)
        assert len(group)>1 and set(map(tuple,entry['joined_source_group']))<=group,'Testpad is not joined to its source witness'
    return len(entries)
