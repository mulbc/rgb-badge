#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Read-only native inventory of the exact 58-edge converter floorplan.

Distances are straight pad-centre geometry, not routed path lengths, electrical
acceptance or pad-edge lower bounds. Direct contacts exclude filled zones.
"""
import argparse
import hashlib
import json
import math
from pathlib import Path
import pcbnew as p

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT/'hardware/coupon/rev-a/staging/led-routing-progress-trial-114mm.kicad_pcb'
SOURCE_SHA256 = '3451177253a021d8706ff818696212afabf539a108f15ef9e5d6921e46435acc'
BUILD = ROOT/'hardware/coupon/rev-a/build'
STAGES = {
    '3V3': dict(ic='U36', refs=['U36','L1','C40','C41','C42','C43','R81','R82','R83']),
    'VLED': dict(ic='U37', refs=['U37','L2','C44','C45','C46','C47','C48','C49','C63','R84','R85','R86','R87']),
}


def xy(point):
    return [point.x, point.y]


def pair_distance(a, b):
    return math.dist(xy(a.GetPosition()), xy(b.GetPosition()))/1e6


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--source', type=Path, default=SOURCE)
    ap.add_argument('--output', type=Path, default=BUILD/'converter-floorplan-58/inventory.json')
    args = ap.parse_args()
    source, output = args.source.resolve(), args.output.resolve()
    assert BUILD.resolve() in output.parents and output.suffix == '.json'
    assert hashlib.sha256(source.read_bytes()).hexdigest() == SOURCE_SHA256, 'Exact 58-edge source required'
    board = p.LoadBoard(str(source))
    parts = {f.GetReference(): f for f in board.GetFootprints()}
    tracks = [t for t in board.GetTracks() if isinstance(t,p.PCB_VIA) or t.GetStart()!=t.GetEnd()]
    assert parts['U36'].GetField('MPN').GetText() == 'TPS631000DRLR'
    assert parts['U37'].GetField('MPN').GetText() == 'TPS63020DSJT'
    assert parts['L1'].GetField('MPN').GetText() == 'DFE252012P-1R0M=P2'
    assert parts['L2'].GetField('MPN').GetText() == 'DFE252012P-1R5M=P2'
    results = {}
    for stage, config in STAGES.items():
        ic = parts[config['ic']]
        target_pads = list(ic.Pads())
        rows = {}
        for ref in config['refs']:
            fp = parts[ref]
            assert fp.GetLayer() == p.B_Cu
            pads = []
            for pad in fp.Pads():
                shape = pad.GetEffectiveShape(p.B_Cu)
                own = []
                other = []
                for item in tracks:
                    if not pad.IsOnLayer(p.B_Cu) or not item.IsOnLayer(p.B_Cu):
                        continue
                    box = pad.GetBoundingBox()
                    if not box.Intersects(item.GetBoundingBox()):
                        continue
                    if not shape.Collide(item.GetEffectiveShape(p.B_Cu),0):
                        continue
                    row = dict(uuid=item.m_Uuid.AsString(),net=item.GetNetname(),
                               kind='via' if isinstance(item,p.PCB_VIA) else 'track')
                    (own if pad.GetNetCode()==item.GetNetCode() else other).append(row)
                targets = [q for q in target_pads if q.GetNetname()==pad.GetNetname() and q.GetNetname()]
                nearest = min(targets,key=lambda q:pair_distance(pad,q)) if targets else None
                pads.append(dict(number=pad.GetNumber(),net=pad.GetNetname(),on_back_copper=pad.IsOnLayer(p.B_Cu),position_iu=xy(pad.GetPosition()),
                                 relative_position_iu=xy(pad.GetFPRelativePosition()),size_iu=xy(pad.GetSize()),
                                 same_net_direct_copper=sorted(own,key=lambda r:r['uuid']),
                                 other_net_direct_copper=sorted(other,key=lambda r:r['uuid']),
                                 nearest_same_net_ic_pad=None if nearest is None else dict(
                                     number=nearest.GetNumber(),position_iu=xy(nearest.GetPosition()),
                                     centre_distance_mm=pair_distance(pad,nearest))))
            rows[ref] = dict(mpn=fp.GetField('MPN').GetText(),footprint=fp.GetFPIDAsString(),
                             position_iu=xy(fp.GetPosition()),angle_deg=fp.GetOrientation().AsDegrees(),
                             pads=sorted(pads,key=lambda q:(q['number'],q['relative_position_iu'])))
        refs_with_contact = [ref for ref,row in rows.items() if any(q['same_net_direct_copper'] for q in row['pads'])]
        results[stage] = dict(ic=config['ic'],parts=rows,parts_with_direct_nonzero_copper=refs_with_contact,
                             direct_contact_pad_count=sum(bool(q['same_net_direct_copper']) for row in rows.values() for q in row['pads']))
    report = dict(status='READ_ONLY_CONVERTER_FLOORPLAN_INVENTORY_NOT_LAYOUT_ACCEPTANCE',
                  source_sha256=SOURCE_SHA256,kicad_version=p.GetBuildVersion(),results=results,
                  source_unchanged=hashlib.sha256(source.read_bytes()).hexdigest()==SOURCE_SHA256,
                  limitations=['Pad-centre distances are not route lengths or pad-edge path lower bounds',
                               'Direct nonzero copper contacts exclude filled zones and other pads',
                               'No component move, trace replacement or electrical setting selected',
                               'Not a power, assembly, process, EMI, thermal or hardware qualification'],
                  fabrication_release_allowed=False)
    report['SPDX-License-Identifier'] = 'CERN-OHL-S-2.0'
    report['tool_sha256'] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
    for stage,result in results.items():
        print(stage,'parts with direct nonzero copper:',','.join(result['parts_with_direct_nonzero_copper']))
        for ref,row in result['parts'].items():
            if ref==result['ic']: continue
            values=[(q['number'],q['net'],round(q['nearest_same_net_ic_pad']['centre_distance_mm'],3))
                    for q in row['pads'] if q['nearest_same_net_ic_pad']]
            print(ref, values)


if __name__ == '__main__':
    main()
