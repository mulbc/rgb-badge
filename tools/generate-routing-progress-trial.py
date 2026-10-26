#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Replay the additive routing checkpoint on the frozen 215-edge study."""
import hashlib
from collections import Counter
import importlib.util
import json
from pathlib import Path
import re
import runpy
import uuid
import pcbnew as p

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT/'hardware/coupon/rev-a/staging/led-native-control-trial-114mm.kicad_pcb'
OUTPUT = ROOT/'hardware/coupon/rev-a/staging/led-routing-progress-trial-114mm.kicad_pcb'
PLAN = ROOT/'mechanical/review/routing-progress-plan.json'
SCOPE = uuid.UUID('7a6f7320-f5d9-4d64-a104-16efb7e933f0')


def main():
    plan = json.loads(PLAN.read_text())
    policy=runpy.run_path(str(ROOT/'tools/routing_pad_necks.py'))
    profile=policy['project_profile'](ROOT,plan)
    OUTPUT.with_suffix('.kicad_pro').write_text(json.dumps(profile,indent=2)+'\n')
    if plan.get('pad_necks'):
        OUTPUT.with_suffix('.kicad_dru').write_text(policy['native_rules']())
    else:
        OUTPUT.with_suffix('.kicad_dru').unlink(missing_ok=True)
    assert hashlib.sha256(SOURCE.read_bytes()).hexdigest() == plan['source_sha256']
    board = p.LoadBoard(str(SOURCE))
    parts = {f.GetReference(): f for f in board.GetFootprints()}
    for entry in plan['placements']:
        part = parts[entry['reference']]
        assert [part.GetPosition().x, part.GetPosition().y] == entry['old_position_iu']
        assert part.GetOrientation().AsDegrees() == entry['old_angle_deg']
        part.SetPosition(p.VECTOR2I(*entry['new_position_iu']))
        part.SetOrientationDegrees(entry['new_angle_deg'])
    removed = []
    source_items = list(board.GetTracks())
    retired_items = []
    orphan=Counter(map(tuple,plan.get('retired_orphan_microvias',[])))
    for item in source_items:
        if not isinstance(item, p.PCB_VIA) and item.GetStart() == item.GetEnd():
            removed.append([item.GetNetname(), item.GetStart().x, item.GetStart().y,
                            board.GetLayerName(item.GetLayer()), item.GetWidth()])
            retired_items.append(item)
            board.Remove(item)
        elif isinstance(item,p.PCB_VIA):
            key=('via',item.GetNetname(),item.GetPosition().x,item.GetPosition().y,
                 board.GetLayerName(item.TopLayer()),board.GetLayerName(item.BottomLayer()),
                 item.GetWidth(item.TopLayer()),item.GetDrillValue())
            if orphan[key]:
                orphan[key]-=1
                retired_items.append(item);board.Remove(item)
    assert sorted(removed) == plan['retired_zero_length_tracks'] and len(removed) == 116
    layers = {board.GetLayerName(x): x for x in board.GetEnabledLayers().CuStack()}
    for entry in plan['added_copper']:
        if entry[0] == 'track':
            _, net, ax, ay, bx, by, layer, width = entry
            item = p.PCB_TRACK(board)
            item.SetStart(p.VECTOR2I(ax, ay)); item.SetEnd(p.VECTOR2I(bx, by))
            item.SetLayer(layers[layer]); item.SetWidth(width)
            assert (ax, ay) != (bx, by)
        else:
            _, net, x, y, top, bottom, diameter, drill = entry
            assert entry[0] == 'via'
            item = p.PCB_VIA(board)
            item.SetPosition(p.VECTOR2I(x, y)); item.SetViaType(p.VIATYPE_MICROVIA)
            item.SetLayerPair(layers[top], layers[bottom])
            item.SetWidth(diameter); item.SetDrill(drill)
        item.SetNetCode(board.FindNet(net).GetNetCode()); board.Add(item)
    for entry in plan.get('power_zones',[]):
        zone = p.ZONE(board)
        zone.SetUuid(p.KIID(str(uuid.uuid5(SCOPE,'power-zone:'+entry['name']))))
        zone.SetZoneName(entry['name']);zone.SetLayer(layers[entry['layer']])
        zone.SetNetCode(board.FindNet(entry['net']).GetNetCode());zone.SetAssignedPriority(10)
        zone.SetLocalClearance(200000);zone.SetMinThickness(200000)
        zone.SetPadConnection(p.ZONE_CONNECTION_FULL)
        zone.SetIslandRemovalMode(p.ISLAND_REMOVAL_MODE_ALWAYS)
        zone.SetThermalReliefGap(200000);zone.SetThermalReliefSpokeWidth(200000)
        for outline in entry['polygons_iu']:
            poly=zone.Outline();index=poly.NewOutline()
            for x,y in outline['outer']:poly.Append(x,y,index)
            for hole in outline['holes']:
                hi=poly.NewHole(index)
                for x,y in hole:poly.Append(x,y,index,hi)
        board.Add(zone)
        assert zone.GetNetname()==entry['net']
    for fill_pass in range(3):
        board.BuildConnectivity()
        p.ZONE_FILLER(board).Fill(board.Zones())
        board.BuildConnectivity()
        print('Fill pass',fill_pass+1,'open edges',board.GetConnectivity().GetUnconnectedCount(False),flush=True)
    assert board.GetConnectivity().GetUnconnectedCount(False) == plan['open_edges']
    p.SaveBoard(str(OUTPUT), board)
    spec = importlib.util.spec_from_file_location('sort', ROOT/'tools/generate-paired-charger-114mm-routing.py')
    helper = importlib.util.module_from_spec(spec); spec.loader.exec_module(helper)
    data = helper.sorted_native_tracks(OUTPUT.read_text(), expected=len(list(board.GetTracks())))
    sequence = iter(range(data.count('(uuid "')))
    data = re.sub(r'\(uuid "[0-9a-f-]{36}"\)',
                  lambda _: '(uuid "'+str(uuid.uuid5(SCOPE, str(next(sequence))))+'")', data)
    OUTPUT.write_text(data)
    print(json.dumps(dict(board_sha256=hashlib.sha256(OUTPUT.read_bytes()).hexdigest(),
                         open_edges=plan['open_edges'], retired_zero_length_tracks=len(removed),
                         added_copper=len(plan['added_copper'])), sort_keys=True))


if __name__ == '__main__':
    main()
