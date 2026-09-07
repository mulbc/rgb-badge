#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Audit the TLC59581 library, driver source and complete coupon XML contract.

Checks a deliberately restricted unrotated, endpoint-wire/global-label subset.
This is independent source verification, not native KiCad ERC or simulation.
"""
import argparse
from collections import defaultdict
from decimal import Decimal as D
from pathlib import Path
import runpy
import sys
import xml.etree.ElementTree as ET

MATRIX = runpy.run_path(str(Path(__file__).with_name('check-coupon-matrix.py')))
A = MATRIX['AUDIT']
parse, children, one, props = A['parse_sexpr'], A['children'], A['only_child'], A['property_map']
PROJECT = A['PROJECT_DIR']
FP = 'rgb-badge-coupon:QFN_TI_RTQ0056E_8x8mm_P0.5mm_EP5.7mm'
# Independent transcription in physical pin-number order, TI SLVSCZ9A pp.3-5.
PIN_NAMES = '''IREF OUTR14 OUTG14 OUTB14 OUTR15 OUTG15 OUTB15
OUTR0 OUTG0 OUTB0 OUTR1 OUTG1 OUTB1 OUTR2 OUTG2 OUTB2
OUTR3 OUTG3 OUTB3 OUTR4 OUTG4 OUTB4 OUTR5 OUTG5 OUTB5
SIN LAT SCLK GCLK OUTR6 OUTG6 OUTB6 OUTR7 OUTG7 OUTB7
OUTR8 OUTG8 OUTB8 OUTR9 OUTG9 OUTB9 SOUT VCC OUTR10
OUTG10 OUTB10 OUTR11 OUTG11 OUTB11 OUTR12 OUTG12 OUTB12
OUTR13 OUTG13 OUTB13 IREFGND GND_EP'''.split()
PARTS = {
    'U1': ('TLC59581RTQT', 'TLC59581RTQT', FP),
    'R1': ('ERJ-2RKF3922X', '39.2k 1%', 'rgb-badge-coupon:R_Panasonic_ERJ2_0402'),
    'C1': ('GRM155R71C104KA88D', '100n 16V X7R', 'rgb-badge-coupon:C_Murata_GRM15_0402'),
}
PARTS.update({f'R{i}': ('ERJ-2RKF1003X', '100k 1%', 'rgb-badge-coupon:R_Panasonic_ERJ2_0402') for i in range(2, 6)})
FLAGS = {'#FLG01': '+3V3_APP', '#FLG02': 'GND'}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def expected_connections():
    nets = {'IREF': 'LED_IREF', 'IREFGND': 'GND', 'GND_EP': 'GND', 'VCC': '+3V3_APP'}
    nets.update({n: 'LED_' + n for n in ('SIN', 'SCLK', 'LAT', 'GCLK', 'SOUT')})
    result = {}
    for n, name in enumerate(PIN_NAMES, 1):
        result['U1', str(n)] = f'COL_{int(name[4:]):02d}_{name[3]}' if name.startswith('OUT') else nets[name]
    result.update({('R1', '1'): 'LED_IREF', ('R1', '2'): 'GND', ('C1', '1'): '+3V3_APP', ('C1', '2'): 'GND'})
    for i, net in enumerate(('LED_SIN', 'LED_SCLK', 'LED_LAT', 'LED_GCLK'), 2):
        result[f'R{i}', '1'] = net
        result[f'R{i}', '2'] = 'GND'
    return result


def library_pins(symbol):
    result = {}
    for unit in children(symbol, 'symbol'):
        for pin in children(unit, 'pin'):
            MATRIX['put_unique'](result, one(pin, 'number', 'pin')[1], pin, 'library pin')
    return result


def check_libraries(project=PROJECT):
    lib = {s[1]: s for s in children(parse(project / 'symbols/rgb-badge-coupon.kicad_sym'), 'symbol')}
    for ref, (mpn, value, footprint) in PARTS.items():
        s = lib[mpn]
        require(props(s)['MPN'] == mpn and props(s)['Footprint'] == footprint, f'{ref}: library MPN/footprint mismatch')
        pins = library_pins(s)
        expected_names = dict(enumerate(PIN_NAMES, 1)) if ref == 'U1' else {1: '~', 2: '~'}
        require(set(pins) == set(map(str, expected_names)), f'{ref}: library pin count/number mismatch')
        for number, name in expected_names.items():
            pin = pins[str(number)]
            typ = 'open_collector' if name.startswith('OUT') else ('input' if name in {'SIN','SCLK','LAT','GCLK'} else ('output' if name == 'SOUT' else ('power_in' if name in {'VCC','GND_EP'} else 'passive')))
            require(one(pin, 'name', 'pin')[1] == name and pin[1] == typ, f'{ref}.{number}: manufacturer pin name/type mismatch')
        foot = parse(project / 'footprints/rgb-badge-coupon.pretty' / (footprint.split(':')[1] + '.kicad_mod'))
        pads = children(foot, 'pad')
        copper = {pad[1]: pad for pad in pads if 'F.Cu' in one(pad, 'layers', 'pad')[1:]}
        require(len(copper) == len(pins) and len(copper) == sum('F.Cu' in one(p,'layers','pad')[1:] for p in pads), f'{ref}: missing/duplicate copper pads')
        require(set(copper) == set(pins), f'{ref}: symbol/footprint pad-number mismatch')
        for number, pad in copper.items():
            n = int(number)
            if ref == 'U1':
                if n == 57:
                    x,y,w,h = 0,0,5.7,5.7
                elif n <= 14:
                    x,y,w,h = -3.9,-3.25+(n-1)*.5,.6,.24
                elif n <= 28:
                    x,y,w,h = -3.25+(n-15)*.5,3.9,.24,.6
                elif n <= 42:
                    x,y,w,h = 3.9,3.25-(n-29)*.5,.6,.24
                else:
                    x,y,w,h = 3.25-(n-43)*.5,-3.9,.24,.6
            else:
                x,y,w,h = (-1 if n == 1 else 1)*(.5 if ref.startswith('R') else .4),0,(.5 if ref.startswith('R') else .4),.5
            actual = one(pad,'at','pad')[1:] + one(pad,'size','pad')[1:]
            require(list(map(D, actual)) == list(map(lambda v:D(str(v)),(x,y,w,h))), f'{ref} pad {n}: position/size differs from audit')
            expected_layers = ['F.Cu','F.Mask'] if ref == 'U1' and n == 57 else ['F.Cu','F.Paste','F.Mask']
            require(one(pad,'layers','pad')[1:] == expected_layers and pad[2] == 'smd', f'{ref} pad {n}: copper/mask/paste mismatch')
        if ref == 'U1':
            windows = [pad for pad in pads if not pad[1]]
            expected = {(D(x),D(y)) for x in ('-2.025','-.675','.675','2.025') for y in ('-2.025','-.675','.675','2.025')}
            require(len(windows)==16 and {MATRIX['position'](p) for p in windows}==expected, 'Thermal paste window placement mismatch')
            for pad in windows:
                require(one(pad,'layers','paste')[1:]==['F.Paste'] and one(pad,'size','paste')[1:]==['1.15','1.15'], 'Thermal paste must be segmented, not full-pad paste')
            marker = one(foot, 'fp_circle', 'pin-1 mark')
            require(one(marker,'center','pin-1 mark')[1:]==['-4.55','-3.25'] and one(marker,'layer','pin-1 mark')[1]=='F.SilkS', 'Pin-1 silk mark mismatch')
    flag = lib['PWR_FLAG']; pins=library_pins(flag)
    require(set(pins)=={'1'} and pins['1'][1]=='power_out', 'Draft supply flag type mismatch')
    return lib


def check_sources(project=PROJECT):
    lib = check_libraries(project)
    root = parse(project/'rgb-badge-coupon.kicad_sch')
    sheets = [s for s in children(root,'sheet') if props(s)['Sheetfile']=='driver.kicad_sch']
    require(len(sheets)==1, 'Driver sheet missing/duplicated')
    instance_path = '/'+one(root,'uuid','root')[1]+'/'+one(sheets[0],'uuid','sheet')[1]
    source = parse(project/'driver.kicad_sch')
    for forbidden in ('no_connect','sheet','bus','label','junction'):
        require(not children(source,forbidden), f'Driver source subset does not support {forbidden}')
    cached = {}
    for s in children(one(source,'lib_symbols','driver'),'symbol'):
        name=s[1].removeprefix('rgb-badge-coupon:')
        require(name in lib and s==[s[0],'rgb-badge-coupon:'+name,*lib[name][2:]], 'Driver embedded library differs from controlled source')
        cached[s[1]]=s
    graph, labels = defaultdict(set), defaultdict(set)
    for wire in children(source,'wire'):
        points=children(one(wire,'pts','wire'),'xy'); require(len(points)==2,'Wire must have two endpoints')
        a,b=[tuple(map(D,point[1:])) for point in points]
        require(a[1]==b[1] and a!=b,'Driver subset requires nonzero horizontal wires')
        graph[a].add(b); graph[b].add(a)
    for label in children(source,'global_label'):
        pos=MATRIX['position'](label); angle=one(label,'at','label')[3]
        require(angle in {'0','180'}, 'Unsupported driver label angle')
        just=one(one(label,'effects','label'),'justify','label')[1:]
        direction=-1 if angle=='0' else 1
        require(just==(['left'] if angle=='0' else ['right']) and len(graph[pos])==1 and all((p[0]-pos[0])*direction>0 for p in graph[pos]),'Driver wire crosses label text')
        labels[pos].add(label[1])
    seen,connections=set(),{}
    for symbol in children(source,'symbol'):
        p=props(symbol); ref=p['Reference']; require(ref not in seen,'Duplicate driver reference'); seen.add(ref)
        virtual=ref in FLAGS
        require(ref in PARTS or virtual, f'Unexpected driver component {ref}')
        expected = ('PWR_FLAG','PWR_FLAG','') if virtual else PARTS[ref]
        require((p['MPN'],p['Value'],p['Footprint']) == (('' if virtual else expected[0]),expected[1],expected[2]),f'{ref}: wrong MPN/value/footprint')
        require(one(symbol,'lib_id',ref)[1]=='rgb-badge-coupon:'+expected[0], f'{ref}: wrong library ID')
        require(one(symbol,'at',ref)[3]=='0' and not children(symbol,'mirror') and one(symbol,'unit',ref)[1]=='1','Unsupported driver transform')
        require(one(symbol,'dnp',ref)[1]=='no' and all(one(symbol,k,ref)[1]==('no' if virtual else 'yes') for k in ['in_bom','on_board']), f'{ref}: unintended omission from assembly')
        path=one(one(one(symbol,'instances',ref),'project',ref),'path',ref)
        require(path[1]==instance_path and one(path,'reference',ref)[1]==ref,f'{ref}: incorrect hierarchy path')
        x,y=MATRIX['position'](symbol)
        for number,pin in library_pins(cached[one(symbol,'lib_id',ref)[1]]).items():
            px,py=MATRIX['position'](pin); pending=[(x+px,y-py)];visited=set();names=set()
            while pending:
                point=pending.pop()
                if point in visited:continue
                visited.add(point);names.update(labels[point]);pending.extend(graph[point]-visited)
            require(len(names)==1,f'{ref}.{number}: expected one connected global net')
            connections[ref,number]=names.pop()
    require(seen==set(PARTS)|set(FLAGS),'Driver population incomplete')
    expected=expected_connections() | {(ref,'1'):net for ref,net in FLAGS.items()}
    require(connections==expected,'Driver source pin-to-net mismatch (including IREF, ground and all columns)')


def check_netlist(path):
    root=ET.parse(path).getroot();require(root.tag=='export','Expected KiCad XML export')
    components, connections = {}, {}
    for comp in root.findall('./components/comp'):
        ref=comp.get('ref')
        MATRIX['put_unique'](components,ref,(comp.findtext('value'),comp.findtext('footprint') or ''),'XML component')
    for net in root.findall('./nets/net'):
        for node in net.findall('node'):
            MATRIX['put_unique'](connections,(node.get('ref'),node.get('pin')),net.get('name'),'XML node')
    # Virtual power flags are normally omitted by KiCad. If emitted, verify them.
    for ref,net in FLAGS.items():
        if ref in components:
            require(components.pop(ref)==('PWR_FLAG',''),f'{ref}: unexpected virtual component')
        if (ref,'1') in connections:
            require(connections.pop((ref,'1'))==net,f'{ref}: wrong declared boundary net')
    expected_components,expected_nets=MATRIX['expected_matrix']()
    expected_components.update({ref:(v,fp) for ref,(_,v,fp) in PARTS.items()})
    expected_nets.update(expected_connections())
    require(components==expected_components,'Complete coupon XML population/value/footprint mismatch')
    require(connections==expected_nets,'Complete coupon XML pin-to-net mismatch')


def current_calculation():
    # TI Equation 2 and Table 2 GAIN column, not its inconsistent ratio column.
    return D('1.209')*D('157.4')/D('39.2')


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project-dir',type=Path,default=PROJECT)
    parser.add_argument('--netlist',type=Path)
    args=parser.parse_args()
    try:
        if args.netlist:
            check_netlist(args.netlist)
            print('KiCad XML complete coupon check passed: 263 components, 1093 physical pins; matrix + driver/support.')
        else:
            check_sources(args.project_dir)
            print(f'Driver source/library checks passed: 57 IC pins, 48 outputs, IREF resistor, decoupling, logic defaults, thermal pad; nominal maximum {current_calculation():.3f} mA (not ERC).')
    except (OSError,ValueError,KeyError,IndexError,ET.ParseError) as e:
        print(f'Driver check failed: {e}',file=sys.stderr);return 1
    return 0

if __name__=='__main__':
    sys.exit(main())
