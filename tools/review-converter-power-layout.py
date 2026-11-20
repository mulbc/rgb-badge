#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Read-only native power-layout and intrinsic-clearance inventory; no approval."""
import argparse
from collections import Counter,defaultdict
import hashlib
import json
import math
from pathlib import Path
import re
import pcbnew as p

ROOT=Path(__file__).resolve().parents[1]
BOARD=ROOT/'hardware/coupon/rev-a/staging/led-converter-routing-trial-114mm.kicad_pcb'
DRC=ROOT/'docs/development/dual-converter-drc-2026-11-05.json'
BOARD_SHA='5e07fb866cc059de670e34102045d9dfd88c88f101355fcdbb27253c0ae26e43'


def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()


def review():
    assert sha(BOARD)==BOARD_SHA
    board=p.LoadBoard(str(BOARD));board.BuildConnectivity();parts={f.GetReference():f for f in board.GetFootprints()}
    def pads(ref,n):return [q for q in parts[ref].Pads() if q.GetNumber()==n]
    def pad(ref,n):
        rows=pads(ref,n);assert rows
        # Exposed-ground numbers can include narrow side lands. Use the main
        # exposed land for geometric/thermal distances, not arbitrary pad order.
        return max(rows,key=lambda q:q.GetSize().x*q.GetSize().y)
    def cluster(q):return frozenset(z.m_Uuid.AsString() for z in board.GetConnectivity().GetConnectedItems(q) if isinstance(z,p.PAD))
    def joined(a,b):return b.m_Uuid.AsString() in cluster(a)
    def point(q):return [q.GetPosition().x/1e6,q.GetPosition().y/1e6]
    def gap(a,b):
        x,y=a.GetBoundingBox(),b.GetBoundingBox()
        dx=max(x.GetX()-y.GetRight(),y.GetX()-x.GetRight(),0)
        dy=max(x.GetY()-y.GetBottom(),y.GetY()-x.GetBottom(),0)
        return math.hypot(dx,dy)/1e6
    def pair(a,b):
        return {'first':[a.GetParentFootprint().GetReference(),a.GetNumber()],
            'second':[b.GetParentFootprint().GetReference(),b.GetNumber()],
            'nets':[a.GetNetname(),b.GetNetname()],
            'centres_mm':[point(a),point(b)],'straight_centre_distance_mm':math.dist(point(a),point(b)),
            'aabb_edge_gap_lower_bound_mm':gap(a,b),'physically_connected':joined(a,b)}
    stage_specs={
      'U36':{'input':['C40','C41'],'output':['C42','C43'],'input_pin':'4','output_pin':'1','ground_pin':'7','feedback':['R81','R82'],'fb_pin':'8','enable':['R83','5']},
      'U37':{'input':['C44','C45'],'output':['C46','C47','C48','C49'],'input_pin':'10','output_pin':'4','ground_pin':'15','feedback':['R84','R85','R86'],'fb_pin':'3','enable':['R87','12']},
    }
    stages={}
    for ref,spec in stage_specs.items():
        f=parts[ref];caps={}
        for kind in ('input','output'):
            for cap in spec[kind]:
                caps[cap]={'function':kind,'mpn':parts[cap].GetField('MPN').GetText(),
                    'supply':pair(pad(ref,spec[kind+'_pin']),pad(cap,'1')),
                    'return':pair(pad(ref,spec['ground_pin']),pad(cap,'2'))}
        thermal=pad(ref,spec['ground_pin']);box=thermal.GetBoundingBox()
        near=[];under=[]
        for t in board.GetTracks():
            if not isinstance(t,p.PCB_VIA) or t.GetNetname()!='GND':continue
            distance=math.dist(point(thermal),[t.GetPosition().x/1e6,t.GetPosition().y/1e6])
            row={'position_mm':[t.GetPosition().x/1e6,t.GetPosition().y/1e6],
                'layers':[board.GetLayerName(t.TopLayer()),board.GetLayerName(t.BottomLayer())],
                'diameter_mm':t.GetWidth(t.TopLayer())/1e6,'drill_mm':t.GetDrillValue()/1e6,'centre_distance_mm':distance}
            if distance<=3:near.append(row)
            if box.Contains(t.GetPosition()):under.append(row)
        stages[ref]={'mpn':f.GetField('MPN').GetText(),'position_mm':[f.GetPosition().x/1e6,f.GetPosition().y/1e6],
            'capacitors':caps,'feedback_to_IC':[pair(pad(ref,spec['fb_pin']),pad(r,'1' if r in ('R82','R86') else '2')) for r in spec['feedback']],
            'feedback_chain':pair(pad('R81','2'),pad('R82','1')) if ref=='U36' else pair(pad('R85','2'),pad('R86','1')),
            'enable_to_pulldown':pair(pad(ref,spec['enable'][1]),pad(spec['enable'][0],'1')),
            'ground_pin_connected_to_main_ground':None,
            'ground_vias_within_3mm':sorted(near,key=lambda row:row['centre_distance_mm']),
            'ground_vias_under_ground_pad_aabb':under,
            'pins':[{'number':q.GetNumber(),'net':q.GetNetname(),'position_mm':point(q)} for q in f.Pads() if q.GetNumber()]}
    stages['U37']['VINA_bypass']={'supply':pair(pad('U37','1'),pad('C63','1')),'return':pair(pad('U37','2'),pad('C63','2'))}
    # Ground-return reference is a known capacitor-ground land, avoiding an
    # assumed pin function on an unrelated active device.
    for ref,spec in stage_specs.items():stages[ref]['ground_pin_connected_to_main_ground']=joined(pad(ref,spec['ground_pin']),pad('C46','2'))
    raw=json.loads(DRC.read_text());assert len(raw['violations'])==104
    uuid_pads={q.m_Uuid.AsString():q for f in board.GetFootprints() for q in f.Pads()}
    violations=[];groups=defaultdict(list)
    for v in raw['violations']:
        assert v['type']=='clearance' and v['severity']=='error' and len(v['items'])==2
        items=[uuid_pads[row['uuid']] for row in v['items']]
        refs={q.GetParentFootprint().GetReference() for q in items};assert len(refs)==1
        ref=next(iter(refs));assert ref.startswith('PAIR') or ref in ('U48','U52')
        actual=float(re.search(r'actual ([0-9.]+) mm',v['description']).group(1))
        record={'reference':ref,'footprint':parts[ref].GetFPIDAsString(),'actual_clearance_mm':actual,
            'required_clearance_mm':0.2,'pads':[{'number':q.GetNumber(),'uuid':q.m_Uuid.AsString(),
                'local_position_iu':[q.GetFPRelativePosition().x,q.GetFPRelativePosition().y],
                'size_iu':[q.GetSize().x,q.GetSize().y],'net':q.GetNetname()} for q in items],
            'classification':'INTERNAL_PACKAGE_LAND_SPACING_REQUIRES_MASK_PROCESS_AND_SCOPED_RULE_DISPOSITION',
            'accepted_for_fabrication':False}
        violations.append(record);groups[record['footprint']].append(record)
    drc_summary={fp:{'findings':len(rows),'references':sorted(set(row['reference'] for row in rows)),
        'gap_counts_mm':dict(Counter(str(row['actual_clearance_mm']) for row in rows))} for fp,rows in groups.items()}
    nets={}
    for name in ['APP_3V3_FB','APP_ON_SW_DRAFT','VLED_FB','VLED_FB_TOP_MID','VLED_ENABLE_DRAFT']:
        clusters={}
        for f in board.GetFootprints():
            for q in f.Pads():
                if q.GetNetname()==name:clusters.setdefault(cluster(q),[]).append([f.GetReference(),q.GetNumber()])
        nets[name]=list(clusters.values())
    width_counts=Counter((t.GetNetname(),board.GetLayerName(t.GetLayer()),t.GetWidth()) for t in board.GetTracks() if not isinstance(t,p.PCB_VIA) and t.GetNetname() in ['+SYS_APP_IN_DRAFT','+3V3_APP','VLED','Net-(U36-LX1)','Net-(U36-LX2)','Net-(L2-~-Pad1)','Net-(L2-~-Pad2)'])
    assert sha(BOARD)==BOARD_SHA
    return {'SPDX-License-Identifier':'CERN-OHL-S-2.0','status':'READ_ONLY_NATIVE_LAYOUT_INVENTORY_NOT_HARDWARE_OR_ELECTRICAL_APPROVAL',
        'board_sha256':BOARD_SHA,'native_opens':board.GetConnectivity().GetUnconnectedCount(False),'drc_sha256':sha(DRC),'tool_sha256':sha(Path(__file__)),'kicad_version':p.GetBuildVersion(),
        'stages':stages,'control_net_groups':nets,'intrinsic_drc_summary':drc_summary,'all_104_classified_findings':violations,
        'power_track_width_counts':[{'net':net,'layer':layer,'width_mm':width/1e6,'segments':n} for (net,layer,width),n in sorted(width_counts.items())],
        'stackup_copper_thickness_defined':'(stackup' in BOARD.read_text(),'total_board_thickness_mm':board.GetDesignSettings().GetBoardThickness()/1e6,
        'source_geometry_changed':False,'fabrication_release_allowed':False,'distance_interpretation':'Native CAD centres and conservative AABB lower bounds; not routed path length or loop inductance'}


def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--output',type=Path,required=True);args=ap.parse_args()
    out=args.output.resolve();assert (ROOT/'hardware/coupon/rev-a/build').resolve() in out.parents and out.suffix=='.json'
    out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(review(),indent=2,sort_keys=True)+'\n')
    print('Read-only converter geometry and all 104 package-internal findings inventoried')


if __name__=='__main__':main()
