#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Check exact-MPN population and pin nets of the unlinked 3V3 candidate."""

from collections import defaultdict
from decimal import Decimal
from pathlib import Path
import argparse
import runpy
import sys


TOOLS = Path(__file__).resolve().parent
GEN = runpy.run_path(str(TOOLS / 'generate-coupon-3v3.py'))
LIB = runpy.run_path(str(TOOLS / 'check-led-libraries.py'))
parse, children, one, props = LIB['parse_sexpr'], LIB['children'], LIB['only_child'], LIB['property_map']
PROJECT = TOOLS.parent / 'hardware/coupon/rev-a'
EXPECTED = {
    ('U36','1'):'+3V3_APP', ('U36','2'):'LX2', ('U36','3'):'LX1',
    ('U36','4'):'+SYS_APP_IN_DRAFT', ('U36','5'):'APP_ON_SW_DRAFT',
    ('U36','6'):'GND', ('U36','7'):'GND', ('U36','8'):'APP_3V3_FB',
    ('L1','1'):'LX1', ('L1','2'):'LX2',
    ('C40','1'):'+SYS_APP_IN_DRAFT', ('C40','2'):'GND',
    ('C41','1'):'+SYS_APP_IN_DRAFT', ('C41','2'):'GND',
    ('C42','1'):'+3V3_APP', ('C42','2'):'GND',
    ('C43','1'):'+3V3_APP', ('C43','2'):'GND',
    ('R81','1'):'+3V3_APP', ('R81','2'):'APP_3V3_FB',
    ('R82','1'):'APP_3V3_FB', ('R82','2'):'GND',
    ('R83','1'):'APP_ON_SW_DRAFT', ('R83','2'):'GND',
}


def require(ok, reason):
    if not ok:
        raise ValueError(reason)


def at(item):
    expr = one(item, 'at', 'position')
    return Decimal(expr[1]), Decimal(expr[2])


def check(project=PROJECT):
    require(not (project / 'rgb-badge-coupon.kicad_sch').read_text().find('"3v3-converter.kicad_sch"') >= 0,
            'The candidate was linked into the root without source/switch integration')
    sheet = parse(project / 'staging/3v3-converter.kicad_sch')
    require(one(sheet, 'uuid', 'file')[1] == GEN['FILE_UUID'], 'Unexpected file UUID')
    require(not any(children(sheet, key) for key in ('sheet','bus','label','junction','no_connect')),
            'Unexpected schematic structure')
    library = {s[1]:s for s in children(parse(project / 'symbols/rgb-badge-coupon.kicad_sym'), 'symbol')}
    cached = {s[1]:s for s in children(one(sheet,'lib_symbols','cache'),'symbol')}
    used = {f'rgb-badge-coupon:{data[0]}' for data in GEN['PARTS'].values()}
    require(set(cached) == used, 'Cached library set changed')
    for name, symbol in cached.items():
        mpn=name.removeprefix('rgb-badge-coupon:')
        require(symbol == ['symbol',name,*library[mpn][2:]], 'Cached symbol mismatch: '+mpn)
    graph, labels = defaultdict(set), defaultdict(set)
    for line in children(sheet,'wire'):
        pts = children(one(line,'pts','wire'),'xy')
        require(len(pts)==2, 'Unexpected wire geometry')
        a,b = (tuple(Decimal(v) for v in point[1:]) for point in pts)
        require(a != b and (a[0]==b[0] or a[1]==b[1]), 'Diagonal or zero-length wire')
        graph[a].add(b); graph[b].add(a)
    for label in children(sheet,'global_label'):
        position=at(label)
        labels[position].add(label[1])
        require(len(graph[position])==1, 'Label must terminate a wire')
    physical={}
    refs=set()
    for sym in children(sheet,'symbol'):
        meta=props(sym); ref=meta['Reference']
        require(ref in GEN['PARTS'] and ref not in refs,'Unexpected/duplicate reference: '+ref)
        refs.add(ref)
        mpn,value,fp,maker,link,pin_count=GEN['PARTS'][ref]
        require((meta['MPN'],meta['Value'],meta['Footprint'],meta['Manufacturer'],meta['Datasheet']) ==
                (mpn,value,'rgb-badge-coupon:'+fp,maker,link),'Part metadata mismatch: '+ref)
        require(one(sym,'lib_id',ref)[1]=='rgb-badge-coupon:'+mpn and one(sym,'at',ref)[3]=='0' and not children(sym,'mirror'),
                'Unsupported part orientation: '+ref)
        pins={one(pin,'number',ref)[1]:pin for unit in children(cached['rgb-badge-coupon:'+mpn],'symbol')
              for pin in children(unit,'pin')}
        require(set(pins)=={str(n) for n in range(1,pin_count+1)},'Cached pin count changed: '+ref)
        x,y=at(sym)
        for n,pin in pins.items():
            dx,dy=at(pin)
            physical[ref,n]=(x+dx,y-dy)
    require(refs==set(GEN['PARTS']),'Population differs from expected')
    connected={}
    for pair, start in physical.items():
        pending=[start]; visited=set(); names=set()
        while pending:
            node=pending.pop()
            if node in visited: continue
            visited.add(node); names.update(labels[node]); pending.extend(graph[node]-visited)
        require(start in graph,'Unwired pin: '+str(pair))
        if pair in {('U36','2'),('L1','2'),('U36','3'),('L1','1')}:
            require(not names,'LX node must stay local: '+str(pair))
            connected[pair]='LX2' if pair in {('U36','2'),('L1','2')} else 'LX1'
            require({p for p, location in physical.items() if location in visited} ==
                    ({('U36','2'),('L1','2')} if connected[pair]=='LX2' else {('U36','3'),('L1','1')}),
                    'Switch node pair changed: '+str(pair))
        else:
            require(len(names)==1,'Pin must have one labelled net: '+str(pair))
            connected[pair]=names.pop()
    require(connected==EXPECTED,'Pin-to-net map changed')
    return connected


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project-dir',type=Path,default=PROJECT)
    args=parser.parse_args()
    try:
        check(args.project_dir)
        print('Unlinked 3V3 candidate source check passed: 9 exact-MPN items, 24 pins, two local LX nodes; no native ERC.')
        return 0
    except (ValueError,KeyError,IndexError,OSError) as error:
        print('3V3 candidate check failed: '+str(error),file=sys.stderr)
        return 1


if __name__=='__main__':
    sys.exit(main())
