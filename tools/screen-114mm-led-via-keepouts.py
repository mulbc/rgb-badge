#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""First-fit rear-component screen with provisional 1010 LED via keepouts."""

import importlib.util
import json
from pathlib import Path
import re
import subprocess
import tempfile
import uuid
from collections import defaultdict

import pcbnew as pcb


ROOT = Path(__file__).resolve().parents[1]
SOURCE_BOARD = ROOT / 'hardware/coupon/rev-a/staging/paired-charger-placement-only-114mm.kicad_pcb'
OUTPUT_BOARD = ROOT / 'hardware/coupon/rev-a/staging/led-via-aware-placement-trial-114mm.kicad_pcb'
ROW_BOARD = ROOT / 'hardware/coupon/rev-a/staging/led-via-aware-row-escape-trial-114mm.kicad_pcb'
OUTPUT = ROOT / 'mechanical/review/led-via-aware-114mm-screen.json'
SPEC = importlib.util.spec_from_file_location(
    'paired_screen', ROOT / 'tools/screen-paired-charger-110mm-xy.py')
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
SCOPE = uuid.UUID('cb3dfeb7-0ae1-4949-b425-03bf6e205a70')
ROW_SCOPE = uuid.UUID('dfb3748c-b30c-4b77-9651-8fc4ef078dfc')
WIDTH = 114.0
LOCAL_BOXES = {
    'C32': (87.5, 9.5, 91.0, 11.5),
    'TP14': (33.0, 0.0, 35.0, 2.0),
    'C30': (96.0, 8.25, 98.5, 9.75),
    'TP10': (92.0, 30.0, 94.0, 32.0),
}


def screen_fit():
    board = pcb.LoadBoard(str(SOURCE_BOARD))
    parts = {part.GetReference(): part for part in board.GetFootprints()}
    assert len(parts) == 483
    with tempfile.TemporaryDirectory(prefix='rgb-led-via-screen-') as folder:
        xml = Path(folder) / 'coupon.xml'
        subprocess.run([str(screen.CLI), 'sch', 'export', 'netlist',
                        '--format', 'kicadxml', '--output', str(xml),
                        str(screen.SOURCE)], check=True, capture_output=True)
        rear, counts = fit.space.component_inventory(xml)
    assert sum(counts.values()) == 497
    fixed = fit.fixed_boxes(rear, right_shift=WIDTH-fit.BOARD_W)
    fixed.update({ref: fit.box(box[0]+WIDTH-screen.WIDTH, box[1], box[2], box[3])
                  for ref, box in screen.GROUPED.items()})
    fixed['TH1'] = fit.box(53.25, 15.25, 2.25, 1.75)
    fixed['U39'] = fit.box(56.0, 14.0, 3.25, 3.0)
    fixed.update(LOCAL_BOXES)
    sites = {}
    conflicts = {}
    for row in range(15):
        for column in range(7):
            ref = f'D{row*16+column+1}'
            led = parts[ref]
            assert led.GetValue() == 'EAST10105RGBA0'
            anodes = [pad for pad in led.Pads()
                      if pad.GetNumber() == '1' and pad.GetNetname() == f'ROW_{row:02d}_A']
            assert len(anodes) == 1, ref
            x = pcb.ToMM(anodes[0].GetPosition().x) + 0.55
            y = pcb.ToMM(anodes[0].GetPosition().y) + 1.4
            # 0.50 mm candidate copper plus 0.20 mm nominal clearance on each side.
            box = fit.box(x-0.45, y-0.45, 0.9, 0.9)
            name = f'VIA_KEEP_{row:02d}_{column:02d}'
            hits = [other for other, rect in fixed.items() if fit.overlap(box, rect)]
            if hits:
                conflicts[name] = {'center_mm': [round(x, 3), round(y, 3)],
                                   'fixed_refs': hits}
            else:
                fixed[name] = box
                sites[name] = [round(x, 3), round(y, 3)]
    nearby = {f'C{66+index}': f'U{47+index}' for index in range(9)}
    result = fit.place(rear, 'dual-package candidate', 'area first', fixed,
                       fit.box(31, 2, 47, 28.5), fit.box(49.5, 12.25, 10, 8),
                       board_width=WIDTH, priority_refs=('U50',),
                       nearby=nearby, near_gap_mm=3.0)
    return {
        'SPDX-License-Identifier': 'CERN-OHL-S-2.0',
        'status': 'ROUTE_AWARE_FIRST_FIT_SCREEN_NOT_A_ROUTED_PCB_OR_FAB_APPROVAL',
        'board_mm': [WIDTH, 32.5],
        'source_coupon_items': sum(counts.values()),
        'candidate_via_mm': {'diameter': 0.5, 'drill': 0.3},
        'candidate_sites': 105,
        'reserved_sites': sites,
        'fixed_site_conflicts': conflicts,
        'local_ldo_and_testpad_boxes_mm': {ref: list(box) for ref, box in LOCAL_BOXES.items()},
        'unplaced_refs': result['unplaced_refs'],
        'under_pack_small_parts': result['small_parts_placed_under_pack'],
        'placed_component_boxes_mm': {
            ref: box for ref, box in result['boxes_mm'].items()
            if not ref.startswith('VIA_KEEP_')},
        'limitations': [
            'Only 1010 row-anode via sites at rows 0..14 and columns 0..6 are reserved.',
            'Two candidate sites overlap the fixed TH1 sensor box and need alternate escapes.',
            'No colour-column routes, 1515 escapes, rear pad copper, inner trunks, RF or enclosure are fit-checked.',
            'Courtyard-first-fit order is not proof of native PCB DRC or assembly compatibility.',
        ],
    }


def generate_board(report):
    board = pcb.LoadBoard(str(SOURCE_BOARD))
    boxes = report['placed_component_boxes_mm']
    for part in board.GetFootprints():
        ref = part.GetReference()
        if ref.startswith('D') and ref[1:].isdigit():
            continue
        key = {'U1': 'U1-project-1',
               'PROJ_U1_2': 'U1-project-2',
               'PROJ_U1_3': 'U1-project-3'}.get(ref, ref)
        assert key in boxes, (ref, key)
        placement.align_courtyard(part, boxes[key])
        if ref == 'U38':
            pos = part.GetPosition()
            part.SetPosition(pcb.VECTOR2I(pos.x, pos.y+pcb.FromMM(0.1)))
    assert len(list(board.GetTracks())) == 0
    pcb.SaveBoard(str(OUTPUT_BOARD), board)
    contents = placement.sort_footprints(OUTPUT_BOARD.read_text())
    serial = iter(range(contents.count('(uuid "')))
    contents = re.sub(r'\(uuid "[0-9a-f-]{36}"\)',
                      lambda _: '(uuid "' + str(uuid.uuid5(SCOPE, str(next(serial)))) + '")',
                      contents)
    OUTPUT_BOARD.write_text(contents)


def generate_row_escape_board(report):
    board = pcb.LoadBoard(str(OUTPUT_BOARD))
    parts = {part.GetReference(): part for part in board.GetFootprints()}
    by_row = defaultdict(list)

    def add_track(start, end, net, layer=pcb.F_Cu):
        routing.add_segment(board, start, end, layer, net, width=0.2)

    def add_via(x, y, net):
        via = pcb.PCB_VIA(board)
        via.SetPosition(routing.point(x, y))
        via.SetViaType(pcb.VIATYPE_THROUGH)
        via.SetLayerPair(pcb.F_Cu, pcb.B_Cu)
        via.SetWidth(pcb.FromMM(0.5))
        via.SetDrill(pcb.FromMM(0.3))
        via.SetNet(net)
        board.Add(via)

    for name, (x, y) in sorted(report['reserved_sites'].items()):
        _, _, row_text, column_text = name.split('_')
        row, column = int(row_text), int(column_text)
        pads = [pad for pad in parts[f'D{row*16+column+1}'].Pads()
                if pad.GetNumber() == '1' and pad.GetNetname() == f'ROW_{row:02d}_A']
        assert len(pads) == 1
        pad = pads[0]
        py = pcb.ToMM(pad.GetPosition().y)
        add_via(x, y, pad.GetNet())
        add_track(pad.GetPosition(), routing.point(x, py), pad.GetNet())
        add_track(routing.point(x, py), routing.point(x, y), pad.GetNet())
        by_row[row].append((x, y, pad.GetNet()))
    assert len(by_row) == 15 and sum(map(len, by_row.values())) == 103
    for row, sites in sorted(by_row.items()):
        sites.sort()
        assert len({y for _, y, _ in sites}) == 1
        add_track(routing.point(sites[0][0], sites[0][1]),
                  routing.point(sites[-1][0], sites[-1][1]),
                  sites[0][2], pcb.In1_Cu)
    # The two vias under TH1 are omitted. These two same-row anodes share
    # the nearby column-4 via through short front-layer links.
    for column in (5, 6):
        pad = next(pad for pad in parts[f'D{7*16+column+1}'].Pads()
                   if pad.GetNumber() == '1' and pad.GetNetname() == 'ROW_07_A')
        x, y = pcb.ToMM(pad.GetPosition().x), pcb.ToMM(pad.GetPosition().y)
        add_track(pad.GetPosition(), routing.point(x+0.55, y), pad.GetNet())
        add_track(routing.point(x+0.55, y), routing.point(x+0.55, 16.25),
                  pad.GetNet())
    add_track(routing.point(51.15, 16.25), routing.point(55.05, 16.25),
              board.FindNet('ROW_07_A'))
    # The last row has no bottom inter-LED via site under the 0.5 mm edge
    # rule. A front-layer edge bus shares one offset via for all eight LEDs.
    bottom = board.FindNet('ROW_15_A')
    for column in range(8):
        pad = next(pad for pad in parts[f'D{15*16+column+1}'].Pads()
                   if pad.GetNumber() == '1' and pad.GetNetname() == 'ROW_15_A')
        x, y = pcb.ToMM(pad.GetPosition().x), pcb.ToMM(pad.GetPosition().y)
        add_track(pad.GetPosition(), routing.point(x+0.55, y), bottom)
        add_track(routing.point(x+0.55, y), routing.point(x+0.55, 31.85), bottom)
    add_track(routing.point(40.5, 31.85), routing.point(57.0, 31.85), bottom)
    add_track(routing.point(40.5, 31.7), routing.point(40.5, 31.85), bottom)
    add_via(40.5, 31.7, bottom)
    assert len(list(board.GetTracks())) == 348
    pcb.SaveBoard(str(ROW_BOARD), board)
    contents = placement.sort_footprints(ROW_BOARD.read_text())
    contents = routing.sorted_native_tracks(contents, expected=348)
    serial = iter(range(contents.count('(uuid "')))
    contents = re.sub(r'\(uuid "[0-9a-f-]{36}"\)',
                      lambda _: '(uuid "' + str(uuid.uuid5(ROW_SCOPE, str(next(serial)))) + '")',
                      contents)
    ROW_BOARD.write_text(contents)


if __name__ == '__main__':
    report = screen_fit()
    generate_board(report)
    generate_row_escape_board(report)
    OUTPUT.write_text(json.dumps(report, indent=2, sort_keys=True) + '\n')
    print(f"{OUTPUT}: {len(report['reserved_sites'])} via keepouts, "
          f"{len(report['fixed_site_conflicts'])} fixed conflicts, "
          f"{len(report['unplaced_refs'])} unplaced components")
    print(f'{OUTPUT_BOARD}: 483 footprints, no routes')
    print(f'{ROW_BOARD}: 244 segments, 104 provisional vias; 1010 row escapes only')
