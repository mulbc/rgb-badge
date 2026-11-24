# SPDX-License-Identifier: Apache-2.0
"""Exact ADR 0090 geometric successor; hardware/process qualification is separate."""
from collections import Counter
import json
import math
from pathlib import Path
import runpy
import converter_checkpoint as base

ROOT=base.ROOT
PARENT=base.OUTPUT
PARENT_SHA='5e07fb866cc059de670e34102045d9dfd88c88f101355fcdbb27253c0ae26e43'
OUTPUT=ROOT/'hardware/coupon/rev-a/staging/led-u36-stage-routing-trial-114mm.kicad_pcb'
PLAN=ROOT/'mechanical/review/u36-stage-checkpoint-plan.json'
PLAN_SHA='533984854b6f607bfec29b0f90eac1113e2bc3b8159ae238a25230f67493e6b0'
sha=base.sha

WITNESSES={
 'FB':[('U36','8'),('R81','2'),('R82','1')],
 'EN_pulldown':[('U36','5'),('R83','1')],
 'VIN':[('U36','4'),('C40','1'),('C41','1')],
 'VOUT':[('U36','1'),('C42','1'),('C43','1'),('R81','1')],
 'GND':[('U36','7'),('U36','6'),('C40','2'),('C41','2'),('C42','2'),('C43','2'),('R82','2'),('R83','2')],
 'LX1':[('U36','3'),('L1','1')],'LX2':[('U36','2'),('L1','2')],
}


def load_plan():
    base.load_plan()
    assert sha(PARENT)==PARENT_SHA and sha(PLAN)==PLAN_SHA
    plan=json.loads(PLAN.read_text())
    assert plan['parent_sha256']==PARENT_SHA
    assert len(plan['poses'])==9 and len(plan['removed_copper'])==14 and len(plan['added_copper'])==47
    assert plan['native_opens']==plan['physical_opens']==47 and plan['intrinsic_findings']==104
    primary=[row for row in plan['primary_local_route_evidence'] if row['primary_local']]
    assert {(r['net'],tuple(r['source'])) for r in primary}=={('+SYS_APP_IN_DRAFT',('C40','1')),('+3V3_APP',('C43','1'))}
    assert all(r['routed'] and r['added_trace_length_mm']<=4 and r['added_vias']<=2 for r in primary)
    assert next(r for r in primary if r['net']=='+SYS_APP_IN_DRAFT')['added_vias']==0
    assert not plan['fabrication_release_allowed']
    return plan


def audit(path,plan=None,fill=True):
    import pcbnew as p
    plan=plan or load_plan();c=base.native_helpers()
    old,new=[p.LoadBoard(str(q)) for q in (PARENT,path)]
    inventory=lambda b:Counter(c['signature'](b,t) for t in b.GetTracks())
    before,after=inventory(old),inventory(new)
    assert before-after==Counter(map(tuple,plan['removed_copper'])),'Exact retirement cohort differs'
    assert after-before==Counter(map(tuple,plan['added_copper'])),'Exact new copper differs'
    for row in plan['added_copper']:
        if row[0]=='track':
            assert row[6] in ('B.Cu','In4.Cu') and row[7]==200000
        else:assert row[4:]==['In4.Cu','B.Cu',300000,100000]
    a={f.GetReference():f for f in old.GetFootprints()};b={f.GetReference():f for f in new.GetFootprints()}
    assert a.keys()==b.keys() and len(a)==483
    for ref,f in a.items():
        g=b[ref]
        assert f.GetFPIDAsString()==g.GetFPIDAsString() and f.GetLayer()==g.GetLayer(),'Part/layer changed'
        assert sorted((q.GetName(),q.GetText()) for q in f.GetFields())==sorted((q.GetName(),q.GetText()) for q in g.GetFields()),'Part identity changed'
        assert Counter(map(c['local_pad_signature'],f.Pads()))==Counter(map(c['local_pad_signature'],g.Pads())),'Pad geometry/net changed'
        row=plan['poses'].get(ref)
        actual=(g.GetPosition().x,g.GetPosition().y,g.GetOrientation().AsDegrees())
        expected=(f.GetPosition().x,f.GetPosition().y,f.GetOrientation().AsDegrees()) if row is None else (*row['position_iu'],row['angle_deg'])
        assert actual==expected,'Pose changed outside ledger: '+ref
    structure=runpy.run_path(str(ROOT/'tools/check-routing-progress-plan.py'))['immutable_board_structure']
    assert structure(PARENT)==structure(path),'Outline/stack/zones/setup/nets changed'
    for ext,key in [('.kicad_pro','source_project_sha256'),('.kicad_dru','source_rules_sha256')]:
        assert path.with_suffix(ext).read_bytes()==PARENT.with_suffix(ext).read_bytes()
        assert sha(path.with_suffix(ext))==plan[key]
    def pads(board):return{q.m_Uuid.AsString():q for f in board.GetFootprints() for q in f.Pads()}
    def cluster(board,q):return frozenset(z.m_Uuid.AsString() for z in board.GetConnectivity().GetConnectedItems(q) if isinstance(z,p.PAD))
    aa,bb=pads(old),pads(new);assert aa.keys()==bb.keys() and len(aa)==2092
    groups={cluster(old,q):key for key,q in aa.items() if q.GetNetname()};assert len(groups)==238
    for _ in range(3 if fill else 1):
        if fill:p.ZONE_FILLER(new).Fill(new.Zones());new.BuildConnectivity()
        assert all(group<=cluster(new,bb[key]) for group,key in groups.items()),'Old pad group split'
        assert new.GetConnectivity().GetUnconnectedCount(False)==47
    def pad(ref,n):
        rows=[q for q in b[ref].Pads() if q.GetNumber()==n];assert len(rows)==1
        return rows[0]
    for name,entries in WITNESSES.items():
        assert len({cluster(new,pad(*q)) for q in entries})==1,'Required local join missing: '+name
    # The switch and hardware display-permission interfaces remain separate.
    assert cluster(new,pad('SW2','3'))!=cluster(new,pad('U36','5'))
    assert pad('U36','6').GetNetname()=='GND'
    for ref in ('C40','C41','C42','C43','R81','R82','R83'):
        assert b[ref].GetField('MPN').GetText()==plan['poses'][ref]['mpn']
    distances={}
    for ref,pin_number,supply_max,return_max in [('C40','4',3,3.5),('C41','4',6,6),('C42','1',6,6),('C43','1',4,4)]:
        pos=lambda q:(q.GetPosition().x/1e6,q.GetPosition().y/1e6)
        supply=math.dist(pos(pad('U36',pin_number)),pos(pad(ref,'1')))
        back=math.dist(pos(pad('U36','7')),pos(pad(ref,'2')))
        assert supply<=supply_max and back<=return_max,'Coupled capacitor locality differs'
        distances[ref]={'supply_centre_distance_mm':supply,'return_centre_distance_mm':back}
    switching={}
    for pin_number,coil_number in [('3','1'),('2','2')]:
        rows=[r for r in plan['switching_routes'] if r[1]==pad('U36',pin_number).GetNetname()]
        assert len(rows)==2 and all(r in plan['added_copper'] and r[6:]==['B.Cu',200000] for r in rows)
        assert rows[0][2:4]==[pad('U36',pin_number).GetPosition().x,pad('U36',pin_number).GetPosition().y]
        assert rows[-1][4:6]==[pad('L1',coil_number).GetPosition().x,pad('L1',coil_number).GetPosition().y]
        length=sum(math.dist(r[2:4],r[4:6]) for r in rows)/1e6
        assert length<=5
        switching[pin_number]=length
    opens=runpy.run_path(str(ROOT/'tools/report-coupon-board-connectivity.py'))['open_edges_by_net'](path)
    assert opens['native_open_edges']==opens['pad_cluster_open_edges']==47
    return old,new,{'all_238_parent_groups_preserved':True,'native_opens':47,'physical_opens':47,
                    'all_local_pin_witnesses_passed':True,'capacitor_distances':distances,'switching_path_length_mm':switching,'switch_boundary_still_open':True,
                    'fabrication_release_allowed':False}
