#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Add one provisional anchored In2.Cu GND pour to the candidate matrix."""

import hashlib
import importlib.util
import json
from pathlib import Path
import re
import uuid

import pcbnew as pcb


ROOT = Path(__file__).resolve().parents[1]
STAGING = ROOT / 'hardware/coupon/rev-a/staging'
SOURCE = STAGING / 'led-row-pulldown-complete-trial-114mm.kicad_pcb'
OUTPUT = STAGING / 'led-in2-ground-plane-trial-114mm.kicad_pcb'
REPORT = ROOT / 'mechanical/review/in2-ground-plane-trial.json'
SCOPE = uuid.UUID('c3618a76-f10a-445c-8ce0-d1fe7e64bef1')
ANCHOR = (34.25, 7.25)


def main():
    board = pcb.LoadBoard(str(SOURCE))
    assert len(list(board.GetFootprints())) == 483
    assert len(list(board.GetTracks())) == 11481
    assert len(list(board.Zones())) == 0
    ground = board.FindNet('GND')
    resistor = next(part for part in board.GetFootprints()
                    if part.GetReference() == 'R25')
    pad = next(pad for pad in resistor.Pads()
               if pad.GetNumber() == '2')
    assert pad.GetNetname() == 'GND'
    assert (pcb.ToMM(pad.GetPosition().x),
            pcb.ToMM(pad.GetPosition().y)) == ANCHOR
    position = pcb.VECTOR2I(*(pcb.FromMM(value) for value in ANCHOR))
    for top, bottom in ((pcb.In4_Cu, pcb.B_Cu),
                        (pcb.In3_Cu, pcb.In4_Cu),
                        (pcb.In2_Cu, pcb.In3_Cu)):
        via = pcb.PCB_VIA(board)
        via.SetPosition(position)
        via.SetViaType(pcb.VIATYPE_MICROVIA)
        via.SetLayerPair(top, bottom)
        via.SetWidth(pcb.FromMM(0.3))
        via.SetDrill(pcb.FromMM(0.1))
        via.SetNet(ground)
        board.Add(via)
    zone = pcb.ZONE(board)
    zone.SetLayer(pcb.In2_Cu)
    zone.SetNet(ground)
    zone.SetLocalClearance(pcb.FromMM(0.2))
    zone.SetThermalReliefGap(pcb.FromMM(0.2))
    zone.SetThermalReliefSpokeWidth(pcb.FromMM(0.2))
    zone.SetIslandRemovalMode(pcb.ISLAND_REMOVAL_MODE_ALWAYS)
    outline = zone.Outline()
    outline.NewOutline()
    for x, y in ((0.5, 0.5), (113.5, 0.5),
                 (113.5, 32.0), (0.5, 32.0)):
        outline.Append(pcb.FromMM(x), pcb.FromMM(y))
    board.Add(zone)
    pcb.ZONE_FILLER(board).Fill(board.Zones())
    fill = zone.GetFilledPolysList(pcb.In2_Cu)
    assert fill.OutlineCount() == 1
    pcb.SaveBoard(str(OUTPUT), board)
    spec = importlib.util.spec_from_file_location(
        'route_base', ROOT / 'tools/generate-paired-charger-114mm-routing.py')
    helper = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(helper)
    data = helper.sorted_native_tracks(
        OUTPUT.read_text(), expected=len(list(board.GetTracks())))
    sequence = iter(range(data.count('(uuid "')))
    data = re.sub(r'\(uuid "[0-9a-f-]{36}"\)',
                  lambda _: '(uuid "'+str(uuid.uuid5(SCOPE, str(next(sequence))))+'")',
                  data)
    OUTPUT.write_text(data)
    loaded = pcb.LoadBoard(str(OUTPUT))
    loaded_zone = next(iter(loaded.Zones()))
    polys = loaded_zone.GetFilledPolysList(pcb.In2_Cu)
    assert polys.OutlineCount() == 1
    area = polys.Area() / 1e12
    report = {
        'SPDX-License-Identifier': 'CERN-OHL-S-2.0',
        'status': 'UNQUALIFIED_GROUND_PLANE_STUDY',
        'source_sha256': hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
        'board_sha256': hashlib.sha256(OUTPUT.read_bytes()).hexdigest(),
        'ground_anchor_ref_pad': ['R25', '2'],
        'ground_anchor_mm': list(ANCHOR),
        'zone_layer': 'In2.Cu',
        'zone_outlines': polys.OutlineCount(),
        'zone_area_mm2': round(area, 3),
        'tracks_and_vias': len(list(loaded.GetTracks())),
        'open_edges': loaded.GetConnectivity().GetUnconnectedCount(False),
    }
    REPORT.write_text(json.dumps(report, indent=2, sort_keys=True)+'\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
