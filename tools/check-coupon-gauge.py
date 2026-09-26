#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Check staged MAX17048 source connections; native KiCad ERC remains required."""

from collections import defaultdict
from decimal import Decimal
from pathlib import Path
import argparse
import runpy
import sys


TOOLS = Path(__file__).resolve().parent
LED = runpy.run_path(str(TOOLS / 'check-led-libraries.py'))
parse, children, one, props = LED['parse_sexpr'], LED['children'], LED['only_child'], LED['property_map']
PROJECT = TOOLS.parent / 'hardware/coupon/rev-a'
SHEET_UUID = 'a3481745-5e2e-5d38-a0e5-19e861e87d30'
FILE_UUID = '0e9b0552-544c-5c4e-83ac-90b44a40a47a'
PARTS = {
    'U35': ('MAX17048G+T10', 'MAX17048G+T10', 'rgb-badge-coupon:TDFN_Maxim_T822-3_2x2mm_P0.5mm_EP0.7x1.38mm'),
    'R79': ('ERJ-2RKF2201X', '2.2k 1%', 'rgb-badge-coupon:R_Panasonic_ERJ2_0402'),
    'R80': ('ERJ-2RKF2201X', '2.2k 1%', 'rgb-badge-coupon:R_Panasonic_ERJ2_0402'),
    'C39': ('GRM155R71C104KA88D', '100n 16V X7R', 'rgb-badge-coupon:C_Murata_GRM15_0402'),
    '#FLG06': ('PWR_FLAG', 'PWR_FLAG', ''),
}
CONNECTIONS = {
    ('U35','1'): 'GND', ('U35','2'): '+BAT_GAUGE_SW', ('U35','3'): '+BAT_GAUGE_SW',
    ('U35','4'): 'GND', ('U35','6'): 'GND', ('U35','7'): 'SYS_I2C_SCL',
    ('U35','8'): 'SYS_I2C_SDA', ('U35','9'): 'GND',
    ('R79','1'): '+3V3_APP', ('R79','2'): 'SYS_I2C_SDA',
    ('R80','1'): '+3V3_APP', ('R80','2'): 'SYS_I2C_SCL',
    ('C39','1'): '+BAT_GAUGE_SW', ('C39','2'): 'GND',
    ('#FLG06','1'): '+BAT_GAUGE_SW',
}


def require(ok, message):
    if not ok:
        raise ValueError(message)


def pos(item):
    at = one(item, 'at', 'position')
    return Decimal(at[1]), Decimal(at[2])


def library_pins(symbol):
    return {one(pin, 'number', 'pin')[1]: pin for unit in children(symbol, 'symbol') for pin in children(unit, 'pin')}


def check_sources(project=PROJECT):
    root = parse(project / 'rgb-badge-coupon.kicad_sch')
    sheet = [s for s in children(root, 'sheet') if props(s).get('Sheetfile') == 'gauge.kicad_sch']
    require(len(sheet) == 1 and one(sheet[0], 'uuid', 'gauge sheet')[1] == SHEET_UUID, 'Missing or changed gauge sheet')
    require(not children(root, 'symbol'), 'Unexpected root symbol')
    path = f'/{one(root,"uuid","root")[1]}/{SHEET_UUID}'
    source = parse(project / 'gauge.kicad_sch')
    require(one(source, 'uuid', 'gauge source')[1] == FILE_UUID, 'Unexpected gauge file UUID')
    for forbidden in ('sheet','bus','label','junction'):
        require(not children(source, forbidden), 'Unexpected gauge structure: ' + forbidden)
    controlled = {s[1]: s for s in children(parse(project / 'symbols/rgb-badge-coupon.kicad_sym'), 'symbol')}
    cached = {}
    for sym in children(one(source, 'lib_symbols', 'gauge'), 'symbol'):
        name = sym[1].removeprefix('rgb-badge-coupon:')
        require(name in controlled and sym == ['symbol', 'rgb-badge-coupon:' + name, *controlled[name][2:]], 'Gauge cached symbol mismatch: '+name)
        cached[sym[1]] = sym
    require(set(cached) == {'rgb-badge-coupon:' + p[0] for p in PARTS.values()}, 'Gauge symbol cache differs from expected')
    graph, labels = defaultdict(set), defaultdict(set)
    for wire in children(source, 'wire'):
        points = children(one(wire, 'pts', 'wire'), 'xy')
        require(len(points) == 2, 'Unsupported gauge wire')
        a,b = (tuple(Decimal(v) for v in point[1:]) for point in points)
        require(a != b and (a[0] == b[0] or a[1] == b[1]), 'Gauge wire must be straight and nonzero')
        graph[a].add(b);graph[b].add(a)
    for label in children(source, 'global_label'):
        position = pos(label)
        labels[position].add(label[1])
        angle = one(label, 'at', 'label')[3]
        require(angle in ('0','180') and len(graph[position]) == 1, 'Unexpected gauge label position or angle')
        require(one(one(label,'effects','label'),'justify','label')[1] == {'0':'left','180':'right'}[angle], 'Gauge label orientation mismatch')
    nc = {pos(marker) for marker in children(source, 'no_connect')}
    require(len(nc) == 1, 'Exactly one gauge no-connect expected')
    found, connections = set(), {}
    for sym in children(source,'symbol'):
        p = props(sym); ref=p['Reference']
        require(ref in PARTS and ref not in found, 'Unexpected or duplicate gauge reference: '+ref)
        found.add(ref)
        mpn,value,footprint=PARTS[ref]
        require((p['MPN'],p['Value'],p['Footprint']) == (('' if ref.startswith('#') else mpn),value,footprint), 'Gauge part metadata mismatch: '+ref)
        require(one(sym,'lib_id',ref)[1]=='rgb-badge-coupon:'+mpn, 'Gauge library ID mismatch: '+ref)
        require(one(sym,'at',ref)[3]=='0' and not children(sym,'mirror') and one(sym,'unit',ref)[1]=='1', 'Unsupported gauge symbol orientation')
        require(one(sym,'in_bom',ref)[1]==('no' if ref.startswith('#') else 'yes') and one(sym,'on_board',ref)[1]==('no' if ref.startswith('#') else 'yes'), 'Gauge BOM/board state mismatch')
        inst=one(one(one(sym,'instances',ref),'project',ref),'path',ref)
        require(inst[1]==path and one(inst,'reference',ref)[1]==ref,'Gauge instance hierarchy mismatch')
        x,y=pos(sym)
        for number,pin in library_pins(cached[one(sym,'lib_id',ref)[1]]).items():
            dx,dy=pos(pin);start=(x+dx,y-dy)
            todo,visited,names=[start],set(),set()
            while todo:
                node=todo.pop()
                if node in visited:continue
                visited.add(node);names.update(labels[node]);todo.extend(graph[node]-visited)
            if (ref,number)==('U35','5'):
                require(start in nc and not names,'Gauge alert must be explicitly no-connected')
            else:
                require(start not in nc and len(names)==1,'Gauge pin not on exactly one net: '+ref+'.'+number)
                connections[ref,number]=names.pop()
    require(found==set(PARTS) and connections==CONNECTIONS,'Gauge population or net map differs from expected')
    # The PWR_FLAG declares a missing source, not a physical ON/OFF switch.
    return connections


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project-dir',type=Path,default=PROJECT)
    args=parser.parse_args()
    try:
        check_sources(args.project_dir)
        print('Staged gauge source check passed: 5 symbols, 14 connected pins, one explicit NC (not native ERC or switch capture).')
        return 0
    except (ValueError,OSError,KeyError,IndexError) as error:
        print('Gauge check failed: '+str(error),file=sys.stderr)
        return 1


if __name__=='__main__':
    sys.exit(main())
