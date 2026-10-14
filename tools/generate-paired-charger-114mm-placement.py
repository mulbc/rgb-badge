#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Generate a net-incomplete 114 mm paired-row placement study, never fabrication data."""

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
SOURCE = STAGING / 'full-coupon-placement-trial-120mm.kicad_pcb'
OUTPUT = STAGING / 'paired-charger-placement-only-114mm.kicad_pcb'
TOPOLOGY_REPORT = ROOT / 'mechanical/review/paired-charger-114mm-topology.json'
LIBRARY = ROOT / 'hardware/coupon/rev-a/footprints/rgb-badge-coupon.pretty'
CLI = Path('/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli')
SCOPE = uuid.UUID('0dc6c48a-c42b-5a94-a660-f45ee8030204')
WIDTH, HEIGHT = 114.0, 32.5


def candidate_boxes():
    spec = importlib.util.spec_from_file_location(
        'paired_charger_screen', ROOT / 'tools/screen-paired-charger-110mm-xy.py')
    screen = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(screen)
    fit = screen.fit
    with tempfile.TemporaryDirectory(prefix='rgb-114-placement-') as folder:
        xml = Path(folder) / 'coupon.xml'
        subprocess.run([str(CLI), 'sch', 'export', 'netlist', '--format', 'kicadxml',
                        '--output', str(xml), str(screen.SOURCE)], check=True,
                       capture_output=True)
        rear, counts = fit.space.component_inventory(xml)
    assert sum(counts.values()) == 497
    extra = WIDTH - screen.WIDTH
    fixed = fit.fixed_boxes(rear, right_shift=WIDTH-fit.BOARD_W)
    fixed.update({ref: fit.box(box[0]+extra, box[1], box[2], box[3])
                  for ref, box in screen.GROUPED.items()})
    # Unlike the older free first-fit screen, reserve actual battery-facing
    # positions for both independent temperature devices in the central box.
    fixed['TH1'] = fit.box(53.25, 15.25, 2.25, 1.75)
    fixed['U39'] = fit.box(56.0, 14.0, 3.25, 3.0)
    near = {f'C{66+i}': f'U{47+i}' for i in range(9)}
    pack, sensor = fit.box(31, 2, 47, 28.5), fit.box(49.5, 12.25, 10, 8)
    comparisons = {}
    for topology in ('canonical 32 separate row FETs', 'dual-package candidate'):
        for nearby in (False, True):
            result = fit.place(rear, topology, 'area first', fixed, pack, sensor,
                               board_width=WIDTH, priority_refs=('U50',),
                               nearby=near if nearby else None, near_gap_mm=3.0)
            comparisons[f'{topology}; bypass_local={nearby}'] = {
                'unplaced_refs': result['unplaced_refs'],
                'under_pack_small_parts': result['small_parts_placed_under_pack'],
            }
            if topology == 'dual-package candidate' and nearby:
                placed = result
    TOPOLOGY_REPORT.write_text(json.dumps({
        'SPDX-License-Identifier': 'CERN-OHL-S-2.0',
        'status': 'GREEDY_XY_SCREEN_NOT_ELECTRICAL_OR_CASE_FIT',
        'board_mm': [WIDTH, HEIGHT],
        'source_coupon_items': sum(counts.values()),
        'battery_body_box_mm': list(pack),
        'sensor_reservation_box_mm': list(sensor),
        'fixed_sensor_boxes_mm': {ref: list(fixed[ref]) for ref in ('TH1', 'U39')},
        'priority_refs': ['U50'],
        'trial_bypass_courtyard_gap_limit_mm': 3.0,
        'comparisons': comparisons,
        'limitations': [
            'Placement order can change the miss count; zero misses do not prove routability.',
            'Paired row package numeric pin map and 0.15 mm land-gap process are unapproved.',
            'Under-pack parts require insulation, height, swelling and thermal qualification.',
            'No case, USB cutout, current-rated copper, RF keepout or fabrication review is represented.',
        ],
    }, indent=2, sort_keys=True) + '\n')
    assert placed['unplaced_count'] == 0 and placed['placed_boxes'] == 227
    return placed['boxes_mm']


def align_courtyard(part, rect):
    layer = pcb.F_CrtYd if part.GetLayer() == pcb.F_Cu else pcb.B_CrtYd
    bounds = part.GetCourtyard(layer).BBox()
    current_x = bounds.GetX() + bounds.GetWidth() // 2
    current_y = bounds.GetY() + bounds.GetHeight() // 2
    target_x = pcb.FromMM((rect[0]+rect[2])/2)
    target_y = pcb.FromMM((rect[1]+rect[3])/2)
    origin = part.GetPosition()
    part.SetPosition(pcb.VECTOR2I(origin.x+target_x-current_x,
                                  origin.y+target_y-current_y))


def sort_footprints(contents):
    starts = [match.start() for match in re.finditer(r'\n\t\(footprint(?=\s)', contents)]
    assert len(starts) == 483
    blocks = []
    for start in starts:
        depth = 0
        quoted = escaped = False
        for pos in range(start + 2, len(contents)):
            char = contents[pos]
            if quoted:
                if escaped:
                    escaped = False
                elif char == '\\':
                    escaped = True
                elif char == '"':
                    quoted = False
            elif char == '"':
                quoted = True
            elif char == '(':
                depth += 1
            elif char == ')':
                depth -= 1
                if depth == 0:
                    blocks.append((start, pos+1, contents[start:pos+1]))
                    break
        else:
            raise ValueError('Unclosed footprint in native board export')
    assert all(not contents[a[1]:b[0]].strip() for a, b in zip(blocks, blocks[1:]))
    def reference(block):
        match = re.search(r'\(property "Reference" "([^"]+)"', block)
        assert match
        return match.group(1)
    ordered = sorted((block[2] for block in blocks), key=reference)
    return contents[:blocks[0][0]] + ''.join(ordered) + contents[blocks[-1][1]:]


def generate():
    boxes = candidate_boxes()
    board = pcb.LoadBoard(str(SOURCE))
    for item in list(board.GetTracks()):
        board.Delete(item)
    for item in list(board.GetDrawings()):
        if item.GetLayer() == pcb.Edge_Cuts:
            board.Delete(item)
    corners = [(0, 0), (WIDTH, 0), (WIDTH, HEIGHT), (0, HEIGHT)]
    for start, end in zip(corners, corners[1:] + corners[:1]):
        edge = pcb.PCB_SHAPE(board)
        edge.SetShape(pcb.S_SEGMENT)
        edge.SetStart(pcb.VECTOR2I(pcb.FromMM(start[0]), pcb.FromMM(start[1])))
        edge.SetEnd(pcb.VECTOR2I(pcb.FromMM(end[0]), pcb.FromMM(end[1])))
        edge.SetLayer(pcb.Edge_Cuts)
        edge.SetWidth(pcb.FromMM(0.05))
        board.Add(edge)
    originals = list(board.GetFootprints())
    driver = next(part for part in originals if part.GetReference() == 'U1')
    for part in originals:
        ref = part.GetReference()
        if ref.startswith('Q') and ref[1:].isdigit():
            board.Delete(part)
        elif ref.startswith('D') and ref[1:].isdigit():
            pos = part.GetPosition()
            part.SetPosition(pcb.VECTOR2I(pos.x-pcb.FromMM(3), pos.y))
        else:
            align_courtyard(part, boxes['U1-project-1' if ref == 'U1' else ref])
            if ref == 'U38':  # Keep pad 3 at least 0.5 mm from the top board edge.
                pos = part.GetPosition()
                part.SetPosition(pcb.VECTOR2I(pos.x, pos.y+pcb.FromMM(0.1)))
    for index in range(1, 17):
        part = pcb.FootprintLoad(str(LIBRARY),
                                 'U-DFN2020-6_TypeB_Diodes_DMC1229UFDB')
        part.SetFPID(pcb.LIB_ID('rgb-badge-coupon',
                                'U-DFN2020-6_TypeB_Diodes_DMC1229UFDB'))
        part.SetReference(f'PAIR{index:02d}')
        part.SetValue('DMC1229UFDB-7_GEOMETRY_ONLY')
        part.Reference().SetVisible(False)
        part.Value().SetVisible(False)
        board.Add(part)
        part.Flip(pcb.VECTOR2I(0, 0), False)
        align_courtyard(part, boxes[f'PAIR{index:02d}'])
    for index in (2, 3):
        part = pcb.FootprintLoad(str(LIBRARY), driver.GetFPID().GetLibItemName())
        part.SetFPID(driver.GetFPID())
        part.SetReference(f'PROJ_U1_{index}')
        part.SetValue('PROJECTED_DRIVER_GEOMETRY_ONLY')
        part.Reference().SetVisible(False)
        part.Value().SetVisible(False)
        board.Add(part)
        part.Flip(pcb.VECTOR2I(0, 0), False)
        align_courtyard(part, boxes[f'U1-project-{index}'])
    assert len(list(board.GetFootprints())) == 483
    assert not list(board.GetTracks())
    pcb.SaveBoard(str(OUTPUT), board)
    contents = sort_footprints(OUTPUT.read_text())
    # pcbnew assigns random UUIDs to the new geometry. Replace every UUID in
    # stable serialization order so repeated study exports are byte identical.
    serial = iter(range(contents.count('(uuid "')))
    contents = re.sub(r'\(uuid "[0-9a-f-]{36}"\)',
                      lambda _: '(uuid "' + str(uuid.uuid5(SCOPE, str(next(serial)))) + '")',
                      contents)
    OUTPUT.write_text(contents)
    print(f'{OUTPUT}: 483 footprints, no tracks; 16 row pairs and 2 drivers are netless geometry')


if __name__ == '__main__':
    generate()
