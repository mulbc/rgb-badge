#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Trace staged KiCad USB gates and compare their actual wiring to ADR 0011.

Includes a stable-state logic evaluator, not a SPICE/transient simulation. The
physical startup inhibit, detectors, charger and ILIM switch remain uncaptured.
"""

import argparse
from collections import defaultdict
from decimal import Decimal as D
from itertools import product
from pathlib import Path
import runpy
import sys

TOOLS=Path(__file__).resolve().parent
LIB=runpy.run_path(str(TOOLS/'check-power-libraries.py'))
CONTRACT=runpy.run_path(str(TOOLS/'check-usb-permission.py'))
parse,children,one,props=LIB['parse'],LIB['children'],LIB['one'],LIB['property_map']
PROJECT=LIB['PROJECT']
ROOT_UUID='207fb68e-2ddb-46bb-8712-eba2f8c5eef6'
SHEETS={
    'usb-conditioning.kicad_sch': ('05e96674-5624-545e-aef0-a1af37c3f4ba','1f02a509-ecc7-5fb6-8e3c-a47168ba29b3'),
    'usb-permission.kicad_sch': ('1bdb377e-db1a-5cbe-9422-f58828c0b6ba','a7d329d3-fad2-5879-8232-e18669c3e38f'),
}
INPUTS=('OUT1','OUT2','CHG_AL_N','CHG_DET','SW_OPEN','VBUS_VALID','LOGIC_READY','SWITCH_ON','ESP_RUNNING','USB_REQUEST')
GATES={
    'U10':('00',{'1':'OUT1','2':'OUT2','4':'ATTACHED'}),
    'U11':('04',{'2':'OUT1','4':'CC_HIGH'}),
    'U12':('04',{'2':'CHG_AL_N','4':'BC_ALLOWED'}),
    'U13':('04',{'2':'CHG_DET','4':'NOT_CHG_DET'}),
    'U14':('04',{'2':'SW_OPEN','4':'DATA_CLOSED'}),
    'U15':('08',{'1':'BC_ALLOWED','2':'CHG_DET','4':'BC_HIGH'}),
    'U16':('32',{'1':'CC_HIGH','2':'BC_HIGH','4':'SOURCE_HIGH'}),
    'U17':('11',{'1':'VBUS_VALID','3':'LOGIC_READY','6':'ATTACHED','4':'READY_ATTACHED'}),
    'U18':('08',{'1':'READY_ATTACHED','2':'SOURCE_HIGH','4':'HIGH_REQ'}),
    'U19':('11',{'1':'BC_ALLOWED','3':'NOT_CHG_DET','6':'DATA_CLOSED','4':'SDP'}),
    'U20':('11',{'1':'SWITCH_ON','3':'ESP_RUNNING','6':'USB_REQUEST','4':'APP_GRANT'}),
    'U21':('11',{'1':'READY_ATTACHED','3':'SDP','6':'APP_GRANT','4':'LOW_REQ'}),
    'U22':('32',{'1':'HIGH_REQ','2':'LOW_REQ','4':'RUN_REQ'}),
    'U23':('06',{'2':'RUN_REQ','4':'EN1_RAW_N'}),
}
PARTS={ref:(f'SN74LVC1G{code}DBVR',f'SN74LVC1G{code}DBVR',
            'rgb-badge-coupon:SOT23_TI_DBV0006A' if code=='11' else 'rgb-badge-coupon:SOT23_TI_DBV0005A')
       for ref,(code,_) in GATES.items()}
PARTS.update({f'U{i}':('SN74LVC2G17DBVR','SN74LVC2G17DBVR','rgb-badge-coupon:SOT23_TI_DBV0006A') for i in range(24,29)})
PARTS.update({f'C{i}':('GRM155R71C104KA88D','100n 16V X7R','rgb-badge-coupon:C_Murata_GRM15_0402') for i in range(10,29)})
for i,name in enumerate(INPUTS):
    up=name in ('OUT1','OUT2','CHG_AL_N','SW_OPEN')
    PARTS[f'R{60+i}']=('ERJ-2RKF1002X' if up else 'ERJ-2RKF1003X','10k 1%' if up else '100k 1%','rgb-badge-coupon:R_Panasonic_ERJ2_0402')
    PARTS[f'TP{20+i}']=('TestPoint_Pad',name,'rgb-badge-coupon:TestPoint_Pad_D1.0mm')
PARTS['R70']=('ERJ-2RKF1002X','10k 1%','rgb-badge-coupon:R_Panasonic_ERJ2_0402')
PARTS.update({ref:('TestPoint_Pad',value,'rgb-badge-coupon:TestPoint_Pad_D1.0mm') for ref,value in [('TP30','HIGH_REQ'),('TP31','EN1_RAW_N')]})


def require(ok, message):
    if not ok: raise ValueError(message)


def expected_connections():
    nets={}
    for ref,(code,pins) in GATES.items():
        nets.update({(ref,n):'USB_'+name for n,name in pins.items()})
        nets[ref,'2' if code=='11' else '3']='GND'
        nets[ref,'5']='+3V3_USB'
    for i in range(5):
        ref=f'U{24+i}';a,b=INPUTS[i*2:i*2+2]
        nets.update({(ref,n):name for n,name in {'1':'USB_RAW_'+a,'3':'USB_RAW_'+b,
                    '6':'USB_'+a,'4':'USB_'+b,'2':'GND','5':'+3V3_USB'}.items()})
    for i in range(10,29):
        nets[f'C{i}','1']='+3V3_USB';nets[f'C{i}','2']='GND'
    for i,name in enumerate(INPUTS):
        nets[f'R{60+i}','1']='USB_RAW_'+name
        nets[f'R{60+i}','2']='+3V3_USB' if name in ('OUT1','OUT2','CHG_AL_N','SW_OPEN') else 'GND'
        nets[f'TP{20+i}','1']='USB_RAW_'+name
    nets.update({('R70','1'):'+3V3_USB',('R70','2'):'USB_EN1_RAW_N',('TP30','1'):'USB_HIGH_REQ',('TP31','1'):'USB_EN1_RAW_N'})
    return nets


NO_CONNECTS={(ref,'1') for ref in ('U11','U12','U13','U14','U23')}


def expected_native_no_connects():
    return {(ref,pin):f'unconnected-({ref}-NC-Pad{pin})' for ref,pin in NO_CONNECTS}


def position(item):
    return tuple(map(D,one(item,'at','position')[1:3]))


def trace_sheet_set(project, sheets, parts, no_connects, flags):
    """Read canonical wires and labels; do not borrow the generator's net table."""
    LIB['check_libraries'](project)
    library={s[1]:s for s in children(parse(project/'symbols/rgb-badge-coupon.kicad_sym'),'symbol')}
    root=parse(project/'rgb-badge-coupon.kicad_sch')
    root_sheets=children(root,'sheet')
    require(one(root,'uuid','root')[1]==ROOT_UUID,'Unexpected permission root UUID')
    components,connections,nc=set(),{},set()
    for filename,(sheet_uuid,file_uuid) in sheets.items():
        targets=[s for s in root_sheets if props(s).get('Sheetfile')==filename]
        require(len(targets)==1 and one(targets[0],'uuid','sheet')[1]==sheet_uuid,'Permission sheet missing/duplicated or wrong UUID')
        source=parse(project/filename)
        require(one(source,'uuid','sheet')[1]==file_uuid,'Permission file UUID mismatch')
        for forbidden in ('sheet','bus','junction','label','hierarchical_label'):
            require(not children(source,forbidden),f'Unsupported permission source object: {forbidden}')
        cached={}
        for symbol in children(one(source,'lib_symbols','cache'),'symbol'):
            mpn=symbol[1].removeprefix('rgb-badge-coupon:')
            require(mpn in library and symbol==[symbol[0],symbol[1],*library[mpn][2:]],f'Stale permission symbol cache: {mpn}')
            require(symbol[1] not in cached,'Duplicate cached permission symbol')
            cached[symbol[1]]=symbol
        graph,labels=defaultdict(set),defaultdict(set)
        for wire in children(source,'wire'):
            pts=children(one(wire,'pts','wire'),'xy')
            require(len(pts)==2,'Expected two wire endpoints')
            a,b=[tuple(map(D,p[1:])) for p in pts]
            require(a!=b and a[1]==b[1],'Permission capture supports nonzero horizontal stubs only')
            require(b not in graph[a],'Duplicate wire')
            graph[a].add(b);graph[b].add(a)
        for label in children(source,'global_label'):
            p=position(label);labels[p].add(label[1])
            angle=one(label,'at','label')[3]
            valid={'0':('left',-1),'180':('right',1)}
            require(angle in valid,'Unsupported label angle')
            require(one(one(label,'effects','label'),'justify','label')[1]==valid[angle][0], 'Label justification mismatch')
            require(len(graph[p])==1 and all((other[0]-p[0])*valid[angle][1]>0 for other in graph[p]),'Wire runs through permission label')
        nc_points={position(p) for p in children(source,'no_connect')}
        require(len(nc_points)==len(children(source,'no_connect')),'Duplicate no-connect marker')
        consumed_nc,consumed_wire_points=set(),set()
        for symbol in children(source,'symbol'):
            p=props(symbol);ref=p['Reference'];virtual=ref in flags
            require(ref not in components,'Duplicate permission reference')
            components.add(ref)
            expected=('PWR_FLAG','PWR_FLAG','') if virtual else parts.get(ref)
            require(expected is not None,f'Unexpected permission component {ref}')
            mpn,value,fp=expected
            require(one(symbol,'lib_id',ref)[1]=='rgb-badge-coupon:'+mpn and p['Value']==value and p['Footprint']==fp,f'{ref}: MPN/value/footprint mismatch')
            require(p['MPN']==('' if virtual or ref.startswith('TP') else mpn),f'{ref}: MPN mismatch')
            require(one(symbol,'at',ref)[3]=='0' and not children(symbol,'mirror') and one(symbol,'unit',ref)[1]=='1',f'{ref}: unsupported orientation/unit')
            require(one(symbol,'on_board',ref)[1]==('no' if virtual else 'yes') and one(symbol,'dnp',ref)[1]=='no',f'{ref}: population flags mismatch')
            require(one(symbol,'in_bom',ref)[1]==('no' if virtual or ref.startswith('TP') else 'yes'),f'{ref}: BOM flag mismatch')
            instance=one(one(one(symbol,'instances',ref),'project',ref),'path',ref)
            require(instance[1]==f'/{ROOT_UUID}/{sheet_uuid}' and one(instance,'reference',ref)[1]==ref,f'{ref}: instance path mismatch')
            x,y=position(symbol)
            for number,pin in LIB['library_pins'](cached['rgb-badge-coupon:'+mpn]).items():
                px,py=position(pin);start=(x+px,y-py)
                pending=[start];visited=set();names=set()
                while pending:
                    point=pending.pop()
                    if point in visited:continue
                    visited.add(point);names.update(labels[point]);pending.extend(graph[point]-visited)
                if (ref,number) in no_connects:
                    require(start in nc_points and not names and not graph[start],f'{ref}.{number}: NC connected or missing')
                    nc.add((ref,number));consumed_nc.add(start)
                else:
                    require(start not in nc_points and len(names)==1 and bool(graph[start]),f'{ref}.{number}: expected one connected net')
                    name=names.pop()
                    if virtual:require(name==flags[ref],'Draft power flag assigned to wrong rail')
                    else:connections[ref,number]=name
                    consumed_wire_points.update(visited)
        require(consumed_nc==nc_points,'Orphan no-connect marker')
        require({p for p,edges in graph.items() if edges}<=consumed_wire_points,'Orphan permission wire')
    require(components==set(parts)|set(flags),'Permission population mismatch')
    require(nc==no_connects,'Permission no-connect set mismatch')
    return connections


def trace_sources(project=PROJECT):
    return trace_sheet_set(project, SHEETS, PARTS, NO_CONNECTS, {})


# Independent device truth functions, keyed by exact physical pin number.
FUNCTIONS={
    'SN74LVC1G00DBVR':(('1','2'),lambda a,b:not(a and b)),
    'SN74LVC1G04DBVR':(('2',),lambda a:not a),
    'SN74LVC1G06DBVR':(('2',),lambda a:not a),
    'SN74LVC1G08DBVR':(('1','2'),lambda a,b:a and b),
    'SN74LVC1G11DBVR':(('1','3','6'),lambda a,b,c:a and b and c),
    'SN74LVC1G32DBVR':(('1','2'),lambda a,b:a or b),
}


def evaluate(connections, bits):
    nets={'+3V3_USB':True,'GND':False}
    nets.update({'USB_RAW_'+name:bool(bit) for name,bit in zip(INPUTS,bits)})
    remaining=[]
    for ref,(mpn,_,_) in PARTS.items():
        if not ref.startswith('U'):continue
        if mpn=='SN74LVC2G17DBVR':
            remaining.extend([(ref,('1',),'6',lambda a:a),(ref,('3',),'4',lambda a:a)])
        else:
            pins,function=FUNCTIONS[mpn];remaining.append((ref,pins,'4',function))
    while remaining:
        progress=False
        for item in remaining[:]:
            ref,pins,out,function=item
            inputs=[connections[ref,p] for p in pins]
            if all(n in nets for n in inputs):
                target=connections[ref,out]
                require(target not in nets,f'Multiple drivers or driven input: {target}')
                nets[target]=bool(function(*(nets[n] for n in inputs)))
                remaining.remove(item);progress=True
        require(progress,'Logic cycle or undriven gate input')
    return nets


def check_logic(connections):
    for bits in product((0,1),repeat=10):
        actual=evaluate(connections,bits)
        expected=CONTRACT['permission'](**dict(zip(('out1','out2','chg_al_n','chg_det','sw_open'),bits[:5])),
              **dict(zip(('vbus_valid','logic_ready','switch_on','esp_running','usb_request'),map(bool,bits[5:]))))
        require(actual['USB_HIGH_REQ']==expected['boost'],f'Captured HIGH differs from contract for {bits}')
        if bits[5]:require(int(actual['USB_EN1_RAW_N'])==expected['en1'],f'Captured EN1 request differs from contract for {bits}')
        else:require(actual['USB_EN1_RAW_N'],'Missing VBUS permits captured RUN')
    return 1024


def check_sources(project=PROJECT):
    nets=trace_sources(project)
    require(nets==expected_connections(),'Permission source pin-to-net mismatch')
    check_logic(nets)
    return nets


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--project-dir',type=Path,default=PROJECT)
    args=p.parse_args()
    try:
        check_sources(args.project_dir)
        print('Captured USB logic source check passed: 61 PCB items, 176 pins including 5 NC; 1024 stable-state cases. Actuator/startup boundary remains open; not native ERC.')
    except (ValueError,KeyError,IndexError,OSError) as e:
        print(f'Permission capture check failed: {e}',file=sys.stderr);return 1
    return 0


if __name__=='__main__':sys.exit(main())
