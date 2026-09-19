#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Check the staged USB interface, exact passive additions and complete pin map.

Source connectivity is not native ERC, USB compliance or transient simulation.
The protected 5 V input is a deliberately unclosed power boundary.
"""

import argparse
from decimal import Decimal as D
from pathlib import Path
import runpy
import sys

TOOLS=Path(__file__).resolve().parent
TRACE=runpy.run_path(str(TOOLS/'check-coupon-permission.py'))
LIB=TRACE['LIB']
parse,children,one,props=LIB['parse'],LIB['children'],LIB['one'],LIB['property_map']
PROJECT=LIB['PROJECT']
require=TRACE['require']
SHEETS={'usb-interface.kicad_sch':('271a5e22-dd9f-53e5-be76-9ea876726439','4cd06246-fee3-58d0-a7b6-a6b2526af0d3')}
PARTS={
    'J1':('USB4505-03-0-A','USB4505-03-0-A','USB_C_GCT_USB4505-03-0-A_MidMount'),
    'U29':('TLV75533PDBVR','TLV75533PDBVR','SOT23_TI_DBV0005A'),
    'U31':('TUSB320LAIRWBR','TUSB320LAIRWBR','X2QFN_TI_RWB0012A_1.6x1.6mm_P0.4mm'),
    'U32':('TS3USB31ERSER','TS3USB31ERSER','UQFN_TI_RSE0008A_1.5x1.5mm_P0.5mm'),
    'U33':('TPD4E05U06DQAR','TPD4E05U06DQAR','USON_TI_DQA0010A'),
    'R71':('ERJ-2RKF8873X','887k 1%','R_Panasonic_ERJ2_0402'),
    'C32':('GRM188R60J106ME47D','10u 6.3V X5R','C_Murata_GRM18_0603'),
}
PARTS.update({f'C{i}':('GRM155C71A105KE11D','1u 10V X7S','C_Murata_GRM15_0402') for i in (30,31)})
PARTS.update({f'C{i}':('GRM155R71C104KA88D','100n 16V X7R','C_Murata_GRM15_0402') for i in (36,37)})
PARTS.update({ref:('TestPoint_Pad',value,'TestPoint_Pad_D1.0mm') for ref,value in [('TP32','VBUS_CONNECTOR'),('TP33','5V_USB_BOUNDARY')]})
PARTS={ref:(mpn,value,'rgb-badge-coupon:'+fp) for ref,(mpn,value,fp) in PARTS.items()}


def expected_connections():
    # Independent transcription from pin tables and capture contract.
    maps={
        'J1':{'A1_B12':'GND','A4_B9':'VBUS_CONNECTOR','B8':None,'A5':'USB_CC1',
              'B7':'USB_CONN_DM','A6':'USB_CONN_DP','A7':'USB_CONN_DM','B6':'USB_CONN_DP',
              'A8':None,'B5':'USB_CC2','B4_A9':'VBUS_CONNECTOR','B1_A12':'GND','S1':'GND'},
        'U29':{1:'+5V_USB',2:'GND',3:'+5V_USB',5:'+3V3_USB'},
        'U31':{1:'USB_CC1',2:'USB_CC2',3:'GND',4:'USB_VBUS_DET',7:'USB_RAW_OUT1',8:'USB_RAW_OUT2',10:'GND',11:'GND',12:'+3V3_USB'},
        'U32':{1:'GND',2:'USB_D+',3:'USB_CONN_DP',4:'GND',5:'USB_CONN_DM',6:'USB_D-',8:'+3V3_APP'},
        'U33':{1:'USB_CONN_DP',2:'USB_CONN_DM',3:'GND',4:'USB_CC1',5:'USB_CC2',8:'GND'},
        'R71':{1:'VBUS_CONNECTOR',2:'USB_VBUS_DET'},
        'TP32':{1:'VBUS_CONNECTOR'},'TP33':{1:'+5V_USB'},
    }
    for ref,net in [('C30','+5V_USB'),('C31','+5V_USB'),('C32','+3V3_USB'),

                    ('C36','+3V3_USB'),('C37','+3V3_APP')]:maps[ref]={1:net,2:'GND'}
    return {(ref,str(pin)):net for ref,pins in maps.items() for pin,net in pins.items() if net is not None}


NC_NAMES={('J1','B8'):'SBU2',('J1','A8'):'SBU1',('U29','4'):'NC',
          ('U31','5'):'ADDR',('U31','6'):'INT_N/OUT3',('U31','9'):'ID',('U32','7'):'NC',
          **{('U33',str(p)):'NC' for p in (6,7,9,10)}}


def expected_native_no_connects():
    return {(ref,pin):f'unconnected-({ref}-{name}-Pad{pin})' for (ref,pin),name in NC_NAMES.items()}


def check_added_libraries(project=PROJECT):
    symbols={s[1]:s for s in children(parse(project/'symbols/rgb-badge-coupon.kicad_sym'),'symbol')}
    for mpn in ('ERJ-2RKF8873X','ERJ-2RCF2R20X'):
        p=props(symbols[mpn])
        require(p.get('MPN')==mpn and p.get('Value')==mpn and p.get('Manufacturer')=='Panasonic','USB resistor identity mismatch')
        require(p.get('Footprint')=='rgb-badge-coupon:R_Panasonic_ERJ2_0402','USB resistor footprint mismatch')
        require(p.get('Datasheet')=='https://industrial.panasonic.com/cdbs/www-data/pdf/RDA0000/AOA0000C304.pdf','USB resistor source mismatch')
        pins=LIB['library_pins'](symbols[mpn])
        require(set(pins)=={'1','2'} and all(p[1:3]==['passive','line'] and one(p,'name','pin')[1]=='~' for p in pins.values()),'USB resistor pin map mismatch')
        # Inherit only the already audited geometry, never the old MPN.
        def normalized(s):
            import json
            return json.dumps(s).replace(mpn,'ERJ-2RKF1003X')
        require(normalized(symbols[mpn])==normalized(symbols['ERJ-2RKF1003X']),'Unexpected USB resistor symbol geometry')
    # TUSB320 R_VBUS specification: 855..920 kohm. Include 1% tolerance
    # and ±100 ppm/K over the detector's -40..85 C range (25 C reference).
    lo=D(887)*(1-D('.01'))*(1-D('.0001')*65)
    hi=D(887)*(1+D('.01'))*(1+D('.0001')*65)
    require(D(855)<=lo<=hi<=D(920),'VBUS detect resistor outside TI interval')
    return lo,hi


def check_sources(project=PROJECT):
    check_added_libraries(project)
    runpy.run_path(str(TOOLS/'check-usb-connector.py'))['check_libraries'](project)
    actual=TRACE['trace_sheet_set'](project,SHEETS,PARTS,set(NC_NAMES),{'#FLG05':'+5V_USB'})
    require(actual==expected_connections(),'USB interface pin-to-net mismatch')
    # The logic supply must have a real source, without the old parallel flag.
    conditioning=parse(project/'usb-conditioning.kicad_sch')
    require(not any(props(s).get('Reference')=='#FLG04' for s in children(conditioning,'symbol')),'Old USB logic supply flag still present')
    return actual


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--project-dir',type=Path,default=PROJECT)
    args=p.parse_args()
    try:
        check_sources(args.project_dir)
        print('USB interface source checks passed: 13 PCB items / 62 pins; connector, ESD, detectors, switched data, USB LDO. Protected input remains staged; not native ERC.')
    except (OSError,ValueError,KeyError,IndexError) as e:
        print(f'USB interface check failed: {e}',file=sys.stderr);return 1
    return 0


if __name__=='__main__':sys.exit(main())
