#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""ADR 0085 exact child-checkpoint policy; the parent routing gate is unchanged."""
from collections import Counter
import hashlib
import json
from pathlib import Path
import runpy

ROOT=Path(__file__).resolve().parents[1]
PARENT=ROOT/'hardware/coupon/rev-a/staging/led-routing-progress-trial-114mm.kicad_pcb'
OUTPUT=ROOT/'hardware/coupon/rev-a/staging/led-converter-routing-trial-114mm.kicad_pcb'
PLAN=ROOT/'mechanical/review/converter-routing-checkpoint-plan.json'
PLAN_SHA='2b5e0c59a0a86ac0e791fe7ed78d66b2e6a8252288686e8dceb59a675adac640'
VLED_PLAN=ROOT/'mechanical/review/converter-vled-52-checkpoint.json'
VLED_PLAN_SHA='f6879cf5bd8733a2031e512ff51a9cbd6d0e55ee0ccf918422df010aefc71b44'
PARENT_SHA='817241b48eee1ae6ccc6ff0a99bf89d6c373bde6b45cba687a71e2309115f3d4'


def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()


def load_plan(stage='dual'):
    path,digest=(VLED_PLAN,VLED_PLAN_SHA) if stage=='vled52' else (PLAN,PLAN_SHA)
    assert sha(path)==digest, 'Exact converter plan fingerprint differs'
    plan=json.loads(path.read_text());assert plan['parent_sha256']==PARENT_SHA
    for path,digest in plan['source_catalog_sha256'].items():assert sha(ROOT/path)==digest
    counts=(13,54,102,52) if stage=='vled52' else (15,65,134,50)
    poses,removed,added,opens=counts
    assert len(plan['poses'])==poses and len(plan['removed_copper'])==removed and len(plan['added_copper'])==added
    assert len(set(map(tuple,plan['removed_copper'])))==removed and len(set(map(tuple,plan['added_copper'])))==added
    assert (plan['native_opens'],plan['physical_opens'],plan['intrinsic_findings'])==(opens,opens,104)
    return plan


def native_helpers():return runpy.run_path(str(ROOT/'tools/check-routing-progress-trial.py'))


def audit_geometry(source,path,plan):
    import pcbnew as p
    assert sha(source)==PARENT_SHA, 'Exact corrected 58-edge parent required'
    c=native_helpers();old,new=(p.LoadBoard(str(x)) for x in (source,path))
    inv=lambda board:Counter(c['signature'](board,t) for t in board.GetTracks())
    before,after=inv(old),inv(new)
    removed=Counter(map(tuple,plan['removed_copper']));added=Counter(map(tuple,plan['added_copper']))
    assert before-after==removed, 'Exact converter retirement cohort differs'
    assert after-before==added, 'Exact converter additions differ'
    assert all(before[row]==1 for row in removed)
    original=inv(p.LoadBoard(str(c['SOURCE'])))
    assert sum((removed & original).values())==plan['removed_original_items']
    assert Counter(row['origin'] for row in plan['cleanup_ledger'])=={'frozen_215_source':plan['removed_original_items'],'accepted_addition':plan['removed_accepted_items']-2}
    for row in plan['cleanup_ledger']:
        assert row['origin']==('frozen_215_source' if original[tuple(row['signature'])] else 'accepted_addition')
    parts={f.GetReference():f for f in new.GetFootprints()}
    assert len(parts)==len(list(new.GetFootprints()))==len(list(old.GetFootprints()))==483
    for a in old.GetFootprints():
        ref=a.GetReference();b=parts[ref]
        assert a.GetFPIDAsString()==b.GetFPIDAsString() and a.GetLayer()==b.GetLayer(), 'Part identity/layer changed: '+ref
        assert Counter(map(c['local_pad_signature'],a.Pads()))==Counter(map(c['local_pad_signature'],b.Pads())), 'Part pad geometry/net changed: '+ref
        assert sorted((f.GetName(),f.GetText()) for f in a.GetFields())==sorted((f.GetName(),f.GetText()) for f in b.GetFields()), 'Part fields changed: '+ref
        pose=plan['poses'].get(ref)
        if pose:
            assert (a.GetPosition().x,a.GetPosition().y,a.GetOrientation().AsDegrees())==(*pose['old_position_iu'],pose['old_angle_deg'])
            expected=(*pose['new_position_iu'],pose['new_angle_deg'])
        else:expected=(a.GetPosition().x,a.GetPosition().y,a.GetOrientation().AsDegrees())
        assert (b.GetPosition().x,b.GetPosition().y,b.GetOrientation().AsDegrees())==expected, 'Unapproved pose: '+ref
    structure=runpy.run_path(str(ROOT/'tools/check-routing-progress-plan.py'))['immutable_board_structure']
    assert structure(source)==structure(path), 'Stack, zone, outline, net or setup changed'
    for ext in ('.kicad_pro','.kicad_dru'):assert source.with_suffix(ext).read_bytes()==path.with_suffix(ext).read_bytes()
    def pads(board):return {q.m_Uuid.AsString():q for f in board.GetFootprints() for q in f.Pads()}
    def cluster(board,q):return frozenset(z.m_Uuid.AsString() for z in board.GetConnectivity().GetConnectedItems(q) if isinstance(z,p.PAD))
    a,b=pads(old),pads(new);assert a.keys()==b.keys() and len(a)==2092
    groups={}
    for key,q in a.items():
        assert q.GetNumber()==b[key].GetNumber() and q.GetNetname()==b[key].GetNetname()
        if q.GetNetname():groups.setdefault(cluster(old,q),key)
    assert len(groups)==246
    for _ in range(3):
        p.ZONE_FILLER(new).Fill(new.Zones());new.BuildConnectivity()
        assert all(group<=cluster(new,b[key]) for group,key in groups.items()), 'Parent UUID pad group split'
        assert new.GetConnectivity().GetUnconnectedCount(False)==plan['native_opens']
    def named_pads(ref,num):
        rows=[q for q in parts[ref].Pads() if q.GetNumber()==num]
        assert rows and (len(rows)==1 or (ref,num)==('U37','15'))
        return rows
    witnesses={
      'LX1':[('L2','1'),('U37','8'),('U37','9')],
      'LX2':[('L2','2'),('U37','6'),('U37','7')],
      'FB':[('U37','3'),('R85','2'),('R86','1')],
      'FB_mid':[('R84','2'),('R85','1')],
      'enable':[('U37','12'),('R87','1')],
      'output':[('U37','4'),('U37','5'),('C46','1'),('C47','1'),('C48','1'),('C49','1'),('R84','1')],
      'input':[('U37','1'),('U37','10'),('U37','11'),('C44','1'),('C45','1'),('C63','1')],
      'return':[('C47','2'),('U37','2'),('U37','15')],
    }
    if plan['native_opens']==50:
        witnesses.update(app_LX1=[('L1','1'),('U36','3')],app_LX2=[('L1','2'),('U36','2')],app_input=[('U36','4'),('C63','1')],app_output=[('U36','1'),('U48','6')])
        import math
        for route in plan['app_switching_routes']:
            rows=route['tracks'];assert all(added[tuple(row)]==1 and row[-2:]==['B.Cu',200000] for row in rows)
            assert rows[0][2:4]==[named_pads('U36',route['ic_pin'])[0].GetPosition().x,named_pads('U36',route['ic_pin'])[0].GetPosition().y]
            assert rows[-1][4:6]==[named_pads('L1',route['coil_pad'])[0].GetPosition().x,named_pads('L1',route['coil_pad'])[0].GetPosition().y]
            assert all(a[4:6]==b[2:4] for a,b in zip(rows,rows[1:]))
            length=sum(math.dist(row[2:4],row[4:6]) for row in rows)/1e6
            assert abs(length-route['length_mm'])<1e-8 and length<=5
    for name,entries in witnesses.items():
        group=cluster(new,named_pads(*entries[0])[0])
        assert all(q.m_Uuid.AsString() in group for entry in entries for q in named_pads(*entry)), 'Required converter join absent: '+name
    # Preserve the exact retained UART interfaces, not merely an aggregate count.
    contacts=runpy.run_path(str(ROOT/'tools/routing_track_replacements.py'))['contacts']
    row=plan['uart_contacts'];item=next(t for t in old.GetTracks() if c['signature'](old,t)==tuple(row['signature']))
    assert [r for r,_ in contacts(old,item,c['signature'],c['physical_identity'])]==row['direct_contacts']
    opens=runpy.run_path(str(ROOT/'tools/report-coupon-board-connectivity.py'))['open_edges_by_net'](path)
    assert opens['native_open_edges']==opens['pad_cluster_open_edges']==plan['native_opens']
    return old,new,opens,witnesses
