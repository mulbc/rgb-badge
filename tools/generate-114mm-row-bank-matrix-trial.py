#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Screen and place ordered candidate row-pair banks in a matrix trial."""

import importlib.util
import json
from pathlib import Path
import re
import subprocess
import tempfile
import uuid

import pcbnew as pcb


ROOT = Path(__file__).resolve().parents[1]
STAGING = ROOT / 'hardware/coupon/rev-a/staging'
SOURCE = STAGING / 'led-qt-uniform-2p2-matrix-trial-114mm.kicad_pcb'
OUTPUT = STAGING / 'led-qt-uniform-2p2-row-bank-onsemi-trial-114mm.kicad_pcb'
REPORT = ROOT / 'mechanical/review/row-bank-114mm-screen.json'
LIBRARY = ROOT / 'hardware/coupon/rev-a/footprints/rgb-badge-coupon.pretty'
NAME = 'WDFN6_2x2_onsemi_NTLJD3119C'
SCOPE = uuid.UUID('24765360-974a-4ccb-9c64-232f7d38771b')
SPEC = importlib.util.spec_from_file_location(
    'via_screen', ROOT / 'tools/screen-114mm-led-via-keepouts.py')
screen = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(screen)
fit = screen.fit
PLACEMENT_SPEC = importlib.util.spec_from_file_location(
    'base_placement', ROOT / 'tools/generate-paired-charger-114mm-placement.py')
placement = importlib.util.module_from_spec(PLACEMENT_SPEC)
PLACEMENT_SPEC.loader.exec_module(placement)
ROUTING_SPEC = importlib.util.spec_from_file_location(
    'base_routing', ROOT / 'tools/generate-paired-charger-114mm-routing.py')
routing = importlib.util.module_from_spec(ROUTING_SPEC)
ROUTING_SPEC.loader.exec_module(routing)


def screen_boxes():
    with tempfile.TemporaryDirectory(prefix='rgb-row-bank-') as folder:
        xml = Path(folder) / 'coupon.xml'
        subprocess.run([str(screen.screen.CLI), 'sch', 'export', 'netlist',
                        '--format', 'kicadxml', '--output', str(xml),
                        str(screen.screen.SOURCE)], check=True, capture_output=True)
        rear, counts = fit.space.component_inventory(xml)
    assert sum(counts.values()) == 497
    fixed = fit.fixed_boxes(rear, right_shift=114-fit.BOARD_W)
    fixed.update({ref: fit.box(box[0]+114-screen.screen.WIDTH,
                               box[1], box[2], box[3])
                  for ref, box in screen.screen.GROUPED.items()})
    fixed['TH1'] = fit.box(53.25, 15.25, 2.25, 1.75)
    fixed['U39'] = fit.box(56, 14, 3.25, 3)
    fixed.update(screen.LOCAL_BOXES)
    # Two ordered eight-pair banks, adjacent to the matrix edge. Their rear
    # height and battery/cover spacing remain subject to mechanical review.
    for index in range(16):
        slot, bank = divmod(index, 2)
        x = 74.0 if bank == 0 else 78.0
        y = 2.0+3.75*slot if bank == 0 else 4.25+3.5*slot
        fixed[f'PAIR{index+1:02d}'] = fit.box(x, y, 3.5, 3.5)
    near = {f'C{66+i}': f'U{47+i}' for i in range(9)}
    result = fit.place(rear, 'dual-package candidate', 'area first', fixed,
                       fit.box(31, 2, 47, 28.5), fit.box(49.5, 12.25, 10, 8),
                       board_width=114, priority_refs=('U50',),
                       nearby=near, near_gap_mm=3.0)
    assert result['unplaced_count'] == 0 and result['placed_boxes'] == 227
    REPORT.write_text(json.dumps({
        'SPDX-License-Identifier': 'CERN-OHL-S-2.0',
        'status': 'UNSELECTED_FIRST_FIT_ROW_BANK_SCREEN',
        'board_mm': [114, 32.5],
        'source_coupon_items': sum(counts.values()),
        'row_pair_boxes_mm': {ref: list(fixed[ref]) for ref in fixed
                              if ref.startswith('PAIR')},
        'placed_component_boxes_mm': result['boxes_mm'],
        'unplaced_refs': result['unplaced_refs'],
        'limitations': [
            'QT 2.2 mm pitch and onsemi row pair are unselected candidates.',
            'This XY screen omits routed rear copper and cell/enclosure heights.',
            'The ordered row-bank fanout, power and driver connections are open.',
        ],
    }, indent=2, sort_keys=True) + '\n')
    return result['boxes_mm']


def generate():
    boxes = screen_boxes()
    board = pcb.LoadBoard(str(SOURCE))
    parts = {part.GetReference(): part for part in board.GetFootprints()}
    assert len(parts) == 483 and len(list(board.GetTracks())) == 2416
    for ref, part in parts.items():
        if ref.startswith('D') and ref[1:].isdigit() and int(ref[1:]) <= 256:
            continue
        if ref.startswith('PAIR'):
            continue
        key = {'U1': 'U1-project-1',
               'PROJ_U1_2': 'U1-project-2',
               'PROJ_U1_3': 'U1-project-3'}.get(ref, ref)
        assert key in boxes, (ref, key)
        placement.align_courtyard(part, boxes[key])
        if ref == 'U38':
            pos = part.GetPosition()
            part.SetPosition(pcb.VECTOR2I(pos.x, pos.y+pcb.FromMM(0.1)))
    for index in range(1, 17):
        ref = f'PAIR{index:02d}'
        old = parts[ref]
        assert old.GetValue() == 'DMC1229UFDB-7_GEOMETRY_ONLY'
        position, angle, flipped = (old.GetPosition(),
                                    old.GetOrientationDegrees(), old.IsFlipped())
        board.Delete(old)
        part = pcb.FootprintLoad(str(LIBRARY), NAME)
        part.SetFPID(pcb.LIB_ID('rgb-badge-coupon', NAME))
        part.SetReference(ref)
        part.SetValue('NTLJD3119CTBG_TRIAL_ONLY')
        part.Reference().SetVisible(False)
        part.Value().SetVisible(False)
        board.Add(part)
        part.SetPosition(position)
        if flipped:
            part.Flip(position, False)
        part.SetOrientationDegrees(angle)
        placement.align_courtyard(part, boxes[ref])
        nets = {'1': 'GND', '2': f'ROW_SEL_{index-1:02d}',
                '3': f'ROW_{index-1:02d}_A', '4': 'VLED',
                '5': f'ROW_GATE_{index-1:02d}',
                '6': f'ROW_GATE_{index-1:02d}'}
        for pad in part.Pads():
            pad.SetNet(board.FindNet(nets[pad.GetNumber()]))
    parts = {part.GetReference(): part for part in board.GetFootprints()}
    for index in range(16):
        part = parts[f'PAIR{index+1:02d}']
        pad = next(pad for pad in part.Pads()
                   if pad.GetNumber() == '3' and
                   pad.GetPosition().x > part.GetPosition().x)
        assert pad.GetNetname() == f'ROW_{index:02d}_A'
        via_x = 77.25 if index % 2 == 0 else 81.25
        escape = pcb.VECTOR2I(pcb.FromMM(via_x), pad.GetPosition().y)
        rear = pcb.PCB_TRACK(board)
        rear.SetStart(pad.GetPosition())
        rear.SetEnd(escape)
        rear.SetWidth(pcb.FromMM(0.2))
        rear.SetLayer(pcb.B_Cu)
        rear.SetNet(pad.GetNet())
        rear.SetUuid(pcb.KIID(str(uuid.uuid5(SCOPE, f'row-{index:02d}-rear'))))
        board.Add(rear)
        via = pcb.PCB_VIA(board)
        via.SetPosition(escape)
        via.SetViaType(pcb.VIATYPE_THROUGH)
        via.SetLayerPair(pcb.F_Cu, pcb.B_Cu)
        via.SetWidth(pcb.FromMM(0.5))
        via.SetDrill(pcb.FromMM(0.3))
        via.SetNet(pad.GetNet())
        via.SetUuid(pcb.KIID(str(uuid.uuid5(SCOPE, f'row-{index:02d}-via'))))
        board.Add(via)
        inner = pcb.PCB_TRACK(board)
        inner.SetStart(pcb.VECTOR2I(
            pcb.FromMM(74.7), pcb.FromMM(2.6+1.95*index)))
        inner.SetEnd(escape)
        inner.SetWidth(pcb.FromMM(0.2))
        inner.SetLayer(pcb.In3_Cu)
        inner.SetNet(pad.GetNet())
        inner.SetUuid(pcb.KIID(str(uuid.uuid5(SCOPE, f'row-{index:02d}-inner'))))
        board.Add(inner)
    # One complete colour-driver path checks that matrix breakout, the new
    # bank vias and the driver land can coexist on the proposed stack-up.
    led = next(pad for pad in parts['D9'].Pads()
               if pad.GetNumber() == '4')
    driver = next(pad for pad in parts['U1'].Pads()
                  if pad.GetNumber() == '36')
    assert led.GetNetname() == driver.GetNetname() == 'COL_08_R'
    colour_net = led.GetNet()
    transition = pcb.VECTOR2I(led.GetPosition().x, pcb.FromMM(0.65))
    front_inner = pcb.PCB_TRACK(board)
    front_inner.SetStart(led.GetPosition())
    front_inner.SetEnd(transition)
    front_inner.SetWidth(pcb.FromMM(0.2))
    front_inner.SetLayer(pcb.In1_Cu)
    front_inner.SetNet(colour_net)
    front_inner.SetUuid(pcb.KIID(str(uuid.uuid5(SCOPE, 'COL_08_R/In1'))))
    board.Add(front_inner)
    for layer_index, (top, bottom) in enumerate((
            (pcb.In1_Cu, pcb.In2_Cu),
            (pcb.In2_Cu, pcb.In3_Cu),
            (pcb.In3_Cu, pcb.In4_Cu))):
        microvia = pcb.PCB_VIA(board)
        microvia.SetPosition(transition)
        microvia.SetViaType(pcb.VIATYPE_MICROVIA)
        microvia.SetLayerPair(top, bottom)
        microvia.SetWidth(pcb.FromMM(0.3))
        microvia.SetDrill(pcb.FromMM(0.1))
        microvia.SetNet(colour_net)
        microvia.SetUuid(pcb.KIID(str(uuid.uuid5(
            SCOPE, f'COL_08_R/transition-{layer_index}'))))
        board.Add(microvia)
    colour_trunk = pcb.PCB_TRACK(board)
    colour_trunk.SetStart(transition)
    colour_trunk.SetEnd(driver.GetPosition())
    colour_trunk.SetWidth(pcb.FromMM(0.2))
    colour_trunk.SetLayer(pcb.In4_Cu)
    colour_trunk.SetNet(colour_net)
    colour_trunk.SetUuid(pcb.KIID(str(uuid.uuid5(SCOPE, 'COL_08_R/In4'))))
    board.Add(colour_trunk)
    driver_via = pcb.PCB_VIA(board)
    driver_via.SetPosition(driver.GetPosition())
    driver_via.SetViaType(pcb.VIATYPE_MICROVIA)
    driver_via.SetLayerPair(pcb.In4_Cu, pcb.B_Cu)
    driver_via.SetWidth(pcb.FromMM(0.3))
    driver_via.SetDrill(pcb.FromMM(0.1))
    driver_via.SetNet(colour_net)
    driver_via.SetUuid(pcb.KIID(str(uuid.uuid5(SCOPE, 'COL_08_R/driver'))))
    board.Add(driver_via)
    assert len(list(board.GetFootprints())) == 483
    assert len(list(board.GetTracks())) == 2470
    assert pcb.SaveBoard(str(OUTPUT), board)
    contents = placement.sort_footprints(OUTPUT.read_text())
    contents = routing.sorted_native_tracks(contents, expected=2470)
    serial = iter(range(contents.count('(uuid "')))
    contents = re.sub(r'\(uuid "[0-9a-f-]{36}"\)',
                      lambda _: '(uuid "' + str(uuid.uuid5(SCOPE, str(next(serial)))) + '")',
                      contents)
    OUTPUT.write_text(contents)
    loaded = pcb.LoadBoard(str(OUTPUT))
    assert loaded.GetConnectivity().GetUnconnectedCount(False) == 645
    print(f'{OUTPUT}: 483 footprints, 16 joined row pairs, '
          'one colour-driver join, 645 open edges')


if __name__ == '__main__':
    generate()
