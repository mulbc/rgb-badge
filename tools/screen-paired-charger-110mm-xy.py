#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Reproduce a 110 mm first-fit screen with grouped USB/charger and paired rows.

This substitutes only courtyard boxes for the sixteen proposed DMC1229UFDB-7
row packages. It does not change the canonical schematic, netlist, BOM or PCB.
"""

import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import xml.etree.ElementTree as ET
from xml.sax.saxutils import escape


ROOT = Path(__file__).resolve().parents[1]
CLI = Path('/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli')
SOURCE = ROOT / 'hardware/coupon/rev-a/rgb-badge-coupon.kicad_sch'
JSON = ROOT / 'mechanical/review/paired-charger-110mm-xy.json'
SVG = ROOT / 'mechanical/review/paired-charger-110mm-xy.svg'
SPEC = importlib.util.spec_from_file_location('paired_fit', ROOT / 'tools/screen-current-lp452845-xy.py')
fit = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(fit)
WIDTH, HEIGHT = 110.0, 32.5

# These are reserved padded XY envelopes, not final solderable positions.
GROUPED = {
    'U45': (95.0, 13.25, 3.5, 3.5), 'U44': (95.0, 17.25, 3.5, 3.5),
    'C60': (99.0, 13.25, 3.0, 1.5), 'C61': (98.75, 15.25, 3.5, 1.5),
    'C62': (92.0, 15.25, 2.5, 1.5), 'C52': (99.0, 18.25, 2.5, 1.5),
    'C57': (92.0, 18.25, 2.5, 1.5), 'U41': (102.0, 23.0, 4.5, 4.5),
    'C56': (102.0, 28.0, 3.5, 1.5), 'R93': (106.75, 27.75, 2.0, 1.0),
    'C53': (98.0, 24.0, 3.5, 1.5), 'C54': (98.0, 26.0, 3.5, 1.5),
    'R92': (99.0, 28.0, 2.0, 1.0),
    'R99': (92.0, 11.25, 2.5, 1.5), 'R100': (92.0, 13.25, 2.5, 1.5),
    'R97': (92.0, 16.75, 2.5, 1.5), 'R98': (92.0, 20.0, 2.5, 1.5),
    'R96': (92.0, 21.75, 2.5, 1.5),
}


def render_svg(boxes, pack, sensor):
    scale = 10
    out = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="-10 -25 1140 370">',
           '<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->',
           '<title>110 mm paired-row and grouped-charger XY screen; no routing or fit approval</title>',
           '<rect x="-10" y="-25" width="1140" height="370" fill="white"/>',
           '<text x="0" y="-8" font-family="sans-serif" font-size="14">110 mm XY screen · provisional paired rows · grouped charger</text>',
           f'<rect x="0" y="0" width="{WIDTH*scale}" height="{HEIGHT*scale}" fill="#f4f7fa" stroke="#24364a"/>']
    def rect(box, colour, opacity, title):
        x0, y0, x1, y1 = box
        out.append(f'<rect x="{x0*scale:.2f}" y="{y0*scale:.2f}" width="{(x1-x0)*scale:.2f}" height="{(y1-y0)*scale:.2f}" fill="{colour}" fill-opacity="{opacity}" stroke="#344556" stroke-width="0.65"><title>{escape(title)}</title></rect>')
    rect(pack, '#e6a23c', .35, 'provisional battery body')
    rect(sensor, '#e6a23c', .28, 'battery temperature-sensor reservation')
    for ref, box in sorted(boxes.items()):
        if ref == 'J1': colour = '#8f54b5'
        elif ref in GROUPED: colour = '#178b72'
        elif ref.startswith('PAIR'): colour = '#d64c4c'
        else: colour = '#6b91b8'
        rect(box, colour, .65, ref)
        if ref in GROUPED or ref == 'J1' or ref.startswith('PAIR'):
            x0, y0, x1, y1 = box
            out.append(f'<text x="{(x0+x1)*5:.2f}" y="{(y0+y1)*5+2:.2f}" text-anchor="middle" font-family="sans-serif" font-size="6" fill="#182737" pointer-events="none">{escape(ref)}</text>')
    out.append('</svg>')
    SVG.write_text('\n'.join(out)+'\n')


def main():
    with tempfile.TemporaryDirectory(prefix='rgb-paired-charger-') as temp:
        xml = Path(temp) / 'coupon.xml'
        subprocess.run([str(CLI), 'sch', 'export', 'netlist', '--format', 'kicadxml',
                        '--output', str(xml), str(SOURCE)], check=True, capture_output=True)
        rear, counts = fit.space.component_inventory(xml)
        netlist = ET.parse(xml).getroot()
        netlist.find('./design/date').text = ''
        digest = hashlib.sha256(ET.tostring(netlist, encoding='utf-8')).hexdigest()
    fixed = fit.fixed_boxes(rear, right_shift=WIDTH-fit.BOARD_W)
    fixed.update({ref: fit.box(*box) for ref, box in GROUPED.items()})
    pack = fit.box(31.0, 2.0, 47.0, 28.5)
    sensor = fit.box(49.5, 12.25, 10.0, 8.0)
    for ref, box in fixed.items():
        assert not fit.overlap(box, pack) and not fit.overlap(box, sensor), ref
    default_order = fit.place(rear, 'dual-package candidate', 'area first', fixed,
                              pack, sensor, board_width=WIDTH)
    assert default_order['unplaced_refs'] == ['U50']
    result = fit.place(rear, 'dual-package candidate', 'area first', fixed,
                       pack, sensor, board_width=WIDTH, priority_refs=('U39', 'U50'))
    assert result['unplaced_count'] == 0
    assert len([ref for ref in result['boxes_mm'] if ref.startswith('PAIR')]) == 16
    narrow_fixed = fit.fixed_boxes(rear, right_shift=108.0-fit.BOARD_W)
    for ref in [name for name in narrow_fixed if name.startswith('U1-project-')]:
        narrow_fixed[ref] = tuple(value-2.0 if index % 2 == 0 else value
                                  for index, value in enumerate(narrow_fixed[ref]))
    narrow_fixed.update({ref: fit.box(box[0]-2.0, box[1], box[2], box[3])
                         for ref, box in GROUPED.items()})
    narrow_default = fit.place(rear, 'dual-package candidate', 'area first', narrow_fixed,
                               pack, sensor, board_width=108.0)
    narrow_priority = fit.place(rear, 'dual-package candidate', 'area first', narrow_fixed,
                                pack, sensor, board_width=108.0, priority_refs=('U39', 'U50'))
    report = {
        'SPDX-License-Identifier': 'CERN-OHL-S-2.0',
        'status': 'UNSELECTED_XY_FIRST_FIT_SCREEN_NOT_A_PCB_OR_110MM_CASE_APPROVAL',
        'source_netlist_sha256': digest,
        'board_mm': [WIDTH, HEIGHT],
        'source_coupon_items': sum(counts.values()),
        'candidate_row_packages': 16,
        'removed_canonical_row_transistors': 32,
        'paired_part': 'DMC1229UFDB-7',
        'priority_refs': ['U39', 'U50'],
        'pack_body_box_mm': list(pack),
        'sensor_reservation_box_mm': list(sensor),
        'grouped_fixed_boxes_mm': {ref: list(fixed[ref]) for ref in sorted(GROUPED)},
        'default_area_order_unplaced_refs': default_order['unplaced_refs'],
        'narrow_108mm_sensitivity': {
            'assumption': 'Shift the grouped USB/charger boxes and three projected drivers 2 mm left',
            'default_order_unplaced_refs': narrow_default['unplaced_refs'],
            'priority_order_unplaced_refs': narrow_priority['unplaced_refs'],
        },
        'placement': result,
        'limitations': [
            'The paired-row part remains unconnected; its numeric pin map and assembly process are unapproved.',
            'Courtyard boxes are not copper routes, thermal copper, via escapes or signal integrity.',
            'The USB4505 board cutout and 0.80 mm thickness guidance are not resolved.',
            'Battery insulation, enclosure height and wire exit are not represented.',
            'All five USB support resistors are grouped in XY but not electrically routed here.',
            'No full-size badge, fabrication files, or independent Gate A review exists.',
        ],
    }
    JSON.write_text(json.dumps(report, indent=2, sort_keys=True)+'\n')
    render_svg(result['boxes_mm'], pack, sensor)
    print(f"110 mm screen: {result['placed_boxes']} rear boxes, 16 candidate pairs, {result['unplaced_count']} misses")
    print(f'Wrote {JSON} and {SVG}')


if __name__ == '__main__':
    main()
