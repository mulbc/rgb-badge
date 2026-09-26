#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Test-only CLI stub. Its output is not a KiCad render or ERC result."""

import os
from pathlib import Path
import sys
import xml.etree.ElementTree as ET


def fabrication_svg(profile="led"):
    # Minimal KiCad-shaped text structure for wrapper/overlay tests. The paths
    # are deliberately dummy strokes, not a real LED footprint or digit font.
    groups = "".join(
        f'<g style="fill:none;stroke:#000000;stroke-width:0.012500;stroke-linecap:round">'
        f'<g class="stroked-text"><desc>{number}</desc>'
        f'<path d="M{x} {y} L{x + 0.1} {y + 0.15}"/></g></g>'
        for number, x, y in (
            ((1, 1.3, 0.4), (2, 1.3, 1.3), (3, 0.4, 1.3), (4, 0.4, 0.4))
            if profile == "led" else
            tuple((n, n / 10, copy / 10) for n in range(1, 11)
                  for copy in range(2 if n in (1, 4, 7, 10) else 1))
        )
    )
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" width="2.000000mm" '
        'height="2.000000mm" viewBox="0.000000 0.000000 2.000000 2.000000">'
        '<title>Stub only, not a KiCad render</title>' + groups + '</svg>\n'
    )


def matrix_netlist():
    # Synthetic fixture, not an export from KiCad. The validator has separate
    # fault-injection tests; this fixture exercises wrapper command plumbing.
    root = ET.Element('export')
    components = ET.SubElement(root, 'components')
    nets = {}
    for number in range(1, 257):
        row, column = divmod(number-1, 16)
        ref = f'D{number}'
        if column < 8:
            mpn, footprint = 'EAST10105RGBA0', 'LED_Everlight_EAST10105RGBA0'
            pins = {'A': '1', 'R': '2', 'G': '4', 'B': '3'}
        else:
            mpn, footprint = 'QBLP1515A-RGB2A', 'LED_QTBrightek_QBLP1515A-RGB2A'
            pins = {'A': '1', 'R': '4', 'G': '3', 'B': '2'}
        comp = ET.SubElement(components, 'comp', ref=ref)
        ET.SubElement(comp, 'value').text = mpn
        ET.SubElement(comp, 'footprint').text = 'rgb-badge-coupon:' + footprint
        for function, pin in pins.items():
            net = f'ROW_{row:02d}_A' if function == 'A' else f'COL_{column:02d}_{function}'
            nets.setdefault(net, []).append((ref, pin))
    net_root = ET.SubElement(root, 'nets')
    for name, nodes in sorted(nets.items()):
        net = ET.SubElement(net_root, 'net', name=name)
        for ref, pin in nodes:
            ET.SubElement(net, 'node', ref=ref, pin=pin)
    return root


def coupon_netlist():
    root = matrix_netlist()
    components = root.find('components')
    for ref, value, footprint in [
        ('U1','TLC59581RTQT','QFN_TI_RTQ0056E_8x8mm_P0.5mm_EP5.7mm'),
        ('R1','39.2k 1%','R_Panasonic_ERJ2_0402'),
        ('C1','100n 16V X7R','C_Murata_GRM15_0402'),
        ('TP1','LED_SOUT','TestPoint_Pad_D1.0mm'),
        *[(f'R{i}', '100k 1%', 'R_Panasonic_ERJ2_0402') for i in range(2,6)],
    ]:
        comp=ET.SubElement(components,'comp',ref=ref)
        ET.SubElement(comp,'value').text=value
        ET.SubElement(comp,'footprint').text='rgb-badge-coupon:'+footprint
    nets={n.get('name'):n for n in root.findall('./nets/net')}
    # Test fixture transcription, not a native exporter or production checker.
    triples=[(8,9,10),(11,12,13),(14,15,16),(17,18,19),(20,21,22),(23,24,25),(30,31,32),(33,34,35),(36,37,38),(39,40,41),(44,45,46),(47,48,49),(50,51,52),(53,54,55),(2,3,4),(5,6,7)]
    extra=[]
    for col,group in enumerate(triples):
        for color,pin in zip('RGB',group):extra.append(('U1',str(pin),f'COL_{col:02d}_{color}'))
    extra += [('U1',str(pin),net) for pin,net in [(1,'LED_IREF'),(26,'LED_SIN'),(27,'LED_LAT'),(28,'LED_SCLK'),(29,'LED_GCLK'),(42,'LED_SOUT'),(43,'+3V3_APP'),(56,'GND'),(57,'GND')]]
    extra += [('R1','1','LED_IREF'),('R1','2','GND'),('C1','1','+3V3_APP'),('C1','2','GND')]
    for i,net in enumerate(('LED_SIN','LED_SCLK','LED_LAT','LED_GCLK'),2):
        extra += [(f'R{i}','1',net),(f'R{i}','2','GND')]
    extra.append(('TP1','1','LED_SOUT'))
    for ref,pin,name in extra:
        if name not in nets:nets[name]=ET.SubElement(root.find('nets'),'net',name=name)
        ET.SubElement(nets[name],'node',ref=ref,pin=pin)
    return root


def complete_coupon_netlist():
    """Synthetic matrix + driver + row fixture; never native KiCad evidence."""
    root = coupon_netlist()
    components = root.find('components')
    parts = [
        ('U2', '74HC4514PW,118', 'TSSOP_Nexperia_SOT355-1_24'),
        ('C2', '100n 16V X7R', 'C_Murata_GRM15_0402'),
        *[(f'Q{i + 1}', 'DMP2066LSN-7', 'SC59_Diodes_DMP2066LSN') for i in range(16)],
        *[(f'Q{i + 17}', '2N7002K-7', 'SOT23_Diodes_2N7002K') for i in range(16)],
        *[(f'R{i + 6}', '1k 1%', 'R_Panasonic_ERJ2_0402') for i in range(16)],
        *[(f'R{i + 22}', '100k 1%', 'R_Panasonic_ERJ2_0402') for i in range(16)],
        *[(f'R{i + 38}', '100k 1%', 'R_Panasonic_ERJ2_0402') for i in range(4)],
        ('R42', '100k 1%', 'R_Panasonic_ERJ2_0402'),
    ]
    for ref, value, footprint in parts:
        comp = ET.SubElement(components, 'comp', ref=ref)
        ET.SubElement(comp, 'value').text = value
        ET.SubElement(comp, 'footprint').text = 'rgb-badge-coupon:' + footprint
    nets = {net.get('name'): net for net in root.findall('./nets/net')}

    def add(ref, pin, name):
        if name not in nets:
            nets[name] = ET.SubElement(root.find('nets'), 'net', name=name)
        net = nets[name]
        ET.SubElement(net, 'node', ref=ref, pin=str(pin))

    decoder = {
        1: '+3V3_APP', 2: 'ROW_A0', 3: 'ROW_A1', 4: 'ROW_SEL_07',
        5: 'ROW_SEL_06', 6: 'ROW_SEL_05', 7: 'ROW_SEL_04', 8: 'ROW_SEL_03',
        9: 'ROW_SEL_01', 10: 'ROW_SEL_02', 11: 'ROW_SEL_00', 12: 'GND',
        13: 'ROW_SEL_13', 14: 'ROW_SEL_12', 15: 'ROW_SEL_15', 16: 'ROW_SEL_14',
        17: 'ROW_SEL_09', 18: 'ROW_SEL_08', 19: 'ROW_SEL_11', 20: 'ROW_SEL_10',
        21: 'ROW_A2', 22: 'ROW_A3', 23: 'ROW_ENABLE_N', 24: '+3V3_APP',
    }
    for pin, net in decoder.items():
        add('U2', pin, net)
    add('C2', 1, '+3V3_APP'); add('C2', 2, 'GND')
    for i in range(16):
        row = f'{i:02d}'
        for ref, pin, net in [
            (f'Q{i + 1}', 1, f'ROW_GATE_{row}'), (f'Q{i + 1}', 2, 'VLED'),
            (f'Q{i + 1}', 3, f'ROW_{row}_A'), (f'Q{i + 17}', 1, f'ROW_SEL_{row}'),
            (f'Q{i + 17}', 2, 'GND'), (f'Q{i + 17}', 3, f'ROW_GATE_{row}'),
            (f'R{i + 6}', 1, 'VLED'), (f'R{i + 6}', 2, f'ROW_GATE_{row}'),
            (f'R{i + 22}', 1, f'ROW_SEL_{row}'), (f'R{i + 22}', 2, 'GND'),
        ]:
            add(ref, pin, net)
    for i in range(4):
        add(f'R{i + 38}', 1, f'ROW_A{i}'); add(f'R{i + 38}', 2, 'GND')
    add('R42', 1, '+3V3_APP'); add('R42', 2, 'ROW_ENABLE_N')
    return root


def legacy_controller_coupon_netlist():
    """Synthetic complete coupon including the controller; never native evidence."""
    root = complete_coupon_netlist()
    components = root.find('components')
    parts = [
        ('U3', 'ESP32-S3-WROOM-1U-N16R8', 'ESP32-S3-WROOM-1U'),
        ('C3', '10u 6.3V X5R', 'C_Murata_GRM18_0603'),
        ('C4', '100n 16V X7R', 'C_Murata_GRM15_0402'),
        ('C5', '1u 10V X7S', 'C_Murata_GRM15_0402'),
        ('R43', '10k 1%', 'R_Panasonic_ERJ2_0402'),
        ('R44', '10k 1%', 'R_Panasonic_ERJ2_0402'),
        ('R45', '22R 1%', 'R_Panasonic_ERJ2_0402'),
        ('R46', '22R 1%', 'R_Panasonic_ERJ2_0402'),
        ('R47', '499R 1%', 'R_Panasonic_ERJ2_0402'),
        ('SW1', 'EVQP7J01P', 'SW_Panasonic_EVQP7J01P'),
        *[(f'TP{i}', 'TestPoint_Pad', 'TestPoint_Pad_D1.0mm') for i in range(2, 13)],
    ]
    for ref, value, footprint in parts:
        comp = ET.SubElement(components, 'comp', ref=ref)
        ET.SubElement(comp, 'value').text = value
        ET.SubElement(comp, 'footprint').text = 'rgb-badge-coupon:' + footprint
    nets = {net.get('name'): net for net in root.findall('./nets/net')}

    def add(ref, pin, name):
        if name not in nets:
            nets[name] = ET.SubElement(root.find('nets'), 'net', name=name)
        ET.SubElement(nets[name], 'node', ref=ref, pin=str(pin))

    module = {
        1: 'GND', 2: '+3V3_APP', 3: 'ESP_EN', 4: 'ROW_A0', 5: 'ROW_A1',
        6: 'ROW_A2', 7: 'ROW_A3', 10: 'SYS_I2C_SDA', 11: 'SYS_I2C_SCL',
        12: 'ROW_ENABLE_N', 13: 'USB_DN_MCU', 14: 'USB_DP_MCU',
        17: 'DISPLAY_ENABLE', 18: 'LED_LAT', 19: 'LED_SIN', 20: 'LED_SCLK',
        21: 'LED_GCLK', 22: 'LED_SOUT', 27: 'MODE_BOOT_N', 36: 'UART0_RX',
        37: 'UART0_TX_RAW', 40: 'GND', 41: 'GND',
    }
    for pin, net in module.items(): add('U3', pin, net)
    # KiCad's native XML exporter includes explicitly no-connected pins as
    # one-node nets. Keep this fixture aligned with the captured native export.
    unused_module_pins = {
        8: 'GPIO15', 9: 'GPIO16', 15: 'GPIO3', 16: 'GPIO46', 23: 'GPIO21',
        24: 'GPIO47', 25: 'GPIO48', 26: 'GPIO45', 28: 'GPIO35/PSRAM',
        29: 'GPIO36/PSRAM', 30: 'GPIO37/PSRAM', 31: 'GPIO38', 32: 'GPIO39',
        33: 'GPIO40', 34: 'GPIO41', 35: 'GPIO42', 38: 'GPIO2', 39: 'GPIO1',
    }
    for pin, name in unused_module_pins.items():
        add('U3', pin, f'unconnected-(U3-{name}-Pad{pin})')
    for ref, left, right in (
        ('C3', '+3V3_APP', 'GND'), ('C4', '+3V3_APP', 'GND'), ('C5', 'ESP_EN', 'GND'),
        ('R43', '+3V3_APP', 'ESP_EN'), ('R44', '+3V3_APP', 'MODE_BOOT_N'),
        ('R45', 'USB_DN_MCU', 'USB_D-'), ('R46', 'USB_DP_MCU', 'USB_D+'),
        ('R47', 'UART0_TX_RAW', 'UART0_TX'), ('SW1', 'MODE_BOOT_N', 'GND'),
    ):
        add(ref, 1, left); add(ref, 2, right)
    for i, net in enumerate(('ESP_EN', 'MODE_BOOT_N', 'UART0_TX', 'UART0_RX', 'LED_GCLK',
                             'ROW_ENABLE_N', '+3V3_APP', 'GND', 'DISPLAY_ENABLE',
                             'SYS_I2C_SDA', 'SYS_I2C_SCL'), 2):
        add(f'TP{i}', 1, net)
    return root


def permission_coupon_netlist():
    """Independent synthetic full-coupon fixture including staged USB gates."""
    root = legacy_controller_coupon_netlist()
    components = root.find('components')
    nets = {n.get('name'): n for n in root.findall('./nets/net')}

    def add(ref, pin, name):
        if name not in nets:
            nets[name] = ET.SubElement(root.find('nets'), 'net', name=name)
        ET.SubElement(nets[name], 'node', ref=ref, pin=str(pin))

    def part(ref, value, footprint):
        comp = ET.SubElement(components, 'comp', ref=ref)
        ET.SubElement(comp, 'value').text = value
        ET.SubElement(comp, 'footprint').text = 'rgb-badge-coupon:' + footprint

    gate_map = [
        (11,'04',[(2,'OUT1'),(4,'CC_HIGH')]),
        (17,'11',[(1,'VBUS_VALID'),(3,'LOGIC_READY'),(6,'CC_HIGH'),(4,'CHARGE_REQ')]),
        (23,'06',[(2,'CHARGE_REQ'),(4,'EN1_RAW_N')]),
    ]
    for number,code,pins in gate_map:
        ref = f'U{number}'
        part(ref,f'SN74LVC1G{code}DBVR','SOT23_TI_DBV0006A' if code=='11' else 'SOT23_TI_DBV0005A')
        for pin,net in pins:add(ref,pin,'USB_'+net)
        add(ref,2 if code=='11' else 3,'GND');add(ref,5,'+3V3_USB')
        if code in ('04','06'):add(ref,1,f'unconnected-({ref}-NC-Pad1)')
    raw = ['OUT1','OUT2','VBUS_VALID','LOGIC_READY']
    for i in range(2):
        ref = f'U{24+i}'
        part(ref,'SN74LVC2G17DBVR','SOT23_TI_DBV0006A')
        for pin,name in [(1,'USB_RAW_'+raw[2*i]),(3,'USB_RAW_'+raw[2*i+1]),
                         (6,'USB_'+raw[2*i]),(4,'USB_'+raw[2*i+1]),(2,'GND'),(5,'+3V3_USB')]:add(ref,pin,name)
    for i in (11,17,23,24,25):
        part(f'C{i}','100n 16V X7R','C_Murata_GRM15_0402')
        add(f'C{i}',1,'+3V3_USB');add(f'C{i}',2,'GND')
    for i,name in enumerate(raw):
        up = i in (0,1)
        part(f'R{60+i}','10k 1%' if up else '100k 1%','R_Panasonic_ERJ2_0402')
        add(f'R{60+i}',1,'USB_RAW_'+name);add(f'R{60+i}',2,'+3V3_USB' if up else 'GND')
        part(f'TP{20+i}',name,'TestPoint_Pad_D1.0mm');add(f'TP{20+i}',1,'USB_OUT2' if i==1 else 'USB_RAW_'+name)
    part('R70','10k 1%','R_Panasonic_ERJ2_0402');add('R70',1,'+3V3_USB');add('R70',2,'USB_EN1_RAW_N')
    for ref,name in [('TP30','CHARGE_REQ'),('TP31','EN1_RAW_N')]:
        part(ref,name,'TestPoint_Pad_D1.0mm');add(ref,1,'USB_'+name)
    part('U34','TPS3808G01DBVR','SOT23_TI_DBV0006A')
    for pin,net in [(1,'USB_RAW_LOGIC_READY'),(2,'GND'),(3,'+5V_USB'),(4,'USB_LOGIC_CT'),(5,'USB_LOGIC_SENSE'),(6,'+5V_USB')]:
        add('U34',pin,net)
    part('C38','100n 16V X7R','C_Murata_GRM15_0402');add('C38',1,'+5V_USB');add('C38',2,'GND')
    for ref,value,a,b in [('R75','620k 1%','+3V3_USB','USB_LOGIC_SENSE'),
                         ('R76','100k 1%','USB_LOGIC_SENSE','GND'),
                         ('R77','100k 1%','+5V_USB','USB_LOGIC_CT'),
                         ('R78','10k 1%','+3V3_USB','USB_RAW_LOGIC_READY')]:
        part(ref,value,'R_Panasonic_ERJ2_0402');add(ref,1,a);add(ref,2,b)
    return root


def controller_coupon_netlist():
    """Test-only USB capture fixture, transcribed separately from the checker."""
    root=permission_coupon_netlist()
    nets={n.get('name'):n for n in root.findall('./nets/net')}
    def add(ref,pin,name):
        if name not in nets:nets[name]=ET.SubElement(root.find('nets'),'net',name=name)
        ET.SubElement(nets[name],'node',ref=ref,pin=str(pin))
    def part(ref,value,footprint,pins):
        comp=ET.SubElement(root.find('components'),'comp',ref=ref)
        ET.SubElement(comp,'value').text=value
        ET.SubElement(comp,'footprint').text='rgb-badge-coupon:'+footprint
        for p,n in pins.items():add(ref,p,n)
    part('J1','USB4505-03-0-A','USB_C_GCT_USB4505-03-0-A_MidMount',{
        'A1_B12':'GND','A4_B9':'VBUS_CONNECTOR','B8':'unconnected-(J1-SBU2-PadB8)',
        'A5':'USB_CC1','B7':'USB_CONN_DM','A6':'USB_CONN_DP','A7':'USB_CONN_DM','B6':'USB_CONN_DP',
        'A8':'unconnected-(J1-SBU1-PadA8)','B5':'USB_CC2','B4_A9':'VBUS_CONNECTOR','B1_A12':'GND','S1':'GND'})
    part('U29','TPS70933DBVR','SOT23_TI_DBV0005A',{
        1:'+5V_USB',2:'GND',3:'unconnected-(U29-EN-Pad3)',4:'unconnected-(U29-NC-Pad4)',5:'+3V3_USB'})
    part('U31','TUSB320LAIRWBR','X2QFN_TI_RWB0012A_1.6x1.6mm_P0.4mm',{
        1:'USB_CC1',2:'USB_CC2',3:'GND',4:'USB_VBUS_DET',5:'unconnected-(U31-ADDR-Pad5)',
        6:'unconnected-(U31-INT_N/OUT3-Pad6)',7:'USB_RAW_OUT1',8:'USB_RAW_OUT2',
        9:'unconnected-(U31-ID-Pad9)',10:'GND',11:'GND',12:'+3V3_USB'})
    part('U32','TS3USB31ERSER','UQFN_TI_RSE0008A_1.5x1.5mm_P0.5mm',{
        1:'GND',2:'USB_D+',3:'USB_CONN_DP',4:'GND',5:'USB_CONN_DM',6:'USB_D-',7:'unconnected-(U32-NC-Pad7)',8:'+3V3_APP'})
    part('U33','TPD4E05U06DQAR','USON_TI_DQA0010A',{
        1:'USB_CONN_DP',2:'USB_CONN_DM',3:'GND',4:'USB_CC1',5:'USB_CC2',6:'unconnected-(U33-NC-Pad6)',
        7:'unconnected-(U33-NC-Pad7)',8:'GND',9:'unconnected-(U33-NC-Pad9)',10:'unconnected-(U33-NC-Pad10)'})
    for ref,a,b,v in [('R71','VBUS_CONNECTOR','USB_VBUS_DET','887k 1%')]:
        part(ref,v,'R_Panasonic_ERJ2_0402',{1:a,2:b})
    for ref,rail in [('C30','+5V_USB'),('C31','+5V_USB')]:
        part(ref,'1u 10V X7S','C_Murata_GRM15_0402',{1:rail,2:'GND'})
    part('C32','10u 6.3V X5R','C_Murata_GRM18_0603',{1:'+3V3_USB',2:'GND'})
    for ref,rail in [('C36','+3V3_USB'),('C37','+3V3_APP')]:
        part(ref,'100n 16V X7R','C_Murata_GRM15_0402',{1:rail,2:'GND'})
    for ref,value,net in [('TP32','VBUS_CONNECTOR','VBUS_CONNECTOR'),('TP33','5V_USB_BOUNDARY','+5V_USB')]:
        part(ref,value,'TestPoint_Pad_D1.0mm',{1:net})
    return root


def main():
    args = sys.argv[1:]
    if args == ["version"]:
        print(os.environ.get("RGB_BADGE_TEST_VERSION", "10.0.6"))
        return 0

    output = Path(args[args.index("--output") + 1])
    stage = "/".join(args[:2])
    if args[:3] == ["sch", "export", "netlist"]:
        assert args[args.index('--format') + 1] == 'kicadxml'
        if os.environ.get('RGB_BADGE_TEST_FAIL') == 'netlist':
            return 7
        root = controller_coupon_netlist()
        if os.environ.get('RGB_BADGE_TEST_BAD_MATRIX') == '1':
            root.find('./nets/net/node').set('pin', '99')
        if os.environ.get('RGB_BADGE_TEST_BAD_DRIVER') == '1':
            root.find("./nets/net/node[@ref='U1'][@pin='57']").set('pin','58')
        if os.environ.get('RGB_BADGE_TEST_BAD_ROWS') == '1':
            root.find("./nets/net/node[@ref='U2'][@pin='23']").set('pin', '24')
        if os.environ.get('RGB_BADGE_TEST_BAD_CONTROLLER') == '1':
            root.find("./nets/net/node[@ref='U3'][@pin='27']").set('pin', '26')
        output.write_bytes(ET.tostring(root))
        return 0
    elif args[:3] == ["sch", "export", "pdf"]:
        assert '--black-and-white' in args
        if os.environ.get('RGB_BADGE_TEST_FAIL') == 'pdf':
            return 7
        output.write_text('Stub only: not a PDF or KiCad render.\n')
        return 0
    elif args[:3] == ["sym", "export", "svg"]:
        names = [n + "_unit1.svg" for n in ("EAST10105RGBA0", "QBLP1515A-RGB2A", "TLC59581RTQT", "ERJ-2RKF3922X", "ERJ-2RKF1003X", "GRM155R71C104KA88D", "PWR_FLAG", "TestPoint_Pad", "74HC4514PW,118", "DMP2066LSN-7", "2N7002K-7", "ERJ-2RKF1001X", "ESP32-S3-WROOM-1U-N16R8", "ERJ-2RKF1002X", "ERJ-2RKF22R0X", "ERJ-2RKF4990X", "GRM155C71A105KE11D", "GRM188R60J106ME47D", "EVQP7J01P", "BQ24074RGTR", "BQ24392RSER", "TS3USB31ERSER", "BQ25616JRTWT", "TPS631000DRLR", "TPS70933DBVR", "TLV75533PDBVR", "SN74LVC1G04DBVR", "INA232AIDDFR", "TPD4E05U06DQAR", "TUSB320LAIRWBR", "TPS63020DSJT", "MAX17048G+T10", "SN74LVC1G00DBVR", "SN74LVC1G06DBVR", "SN74LVC1G08DBVR", "SN74LVC1G11DBVR", "SN74LVC1G32DBVR", "TPS3808G01DBVR", "SN74LVC2G17DBVR", "ERJ-2RKF8873X", "ERJ-2RCF2R20X")]
        names.append("ERJ-2RKF2201X_unit1.svg")
    elif args[:3] == ["fp", "export", "svg"]:
        # Added independently of the source parser: exercise wrapper requirements.
        layers = args[args.index("--layers") + 1]
        if output.name == "fabrication":
            assert layers == "F.Fab,F.SilkS,F.CrtYd", "Fabrication view must exclude solid pad layers"
            assert "--sketch-pads-on-fab-layers" in args
        elif output.name == "copper":
            assert layers == "F.Cu", "Copper view must exclude non-copper outlines"
            assert "--sketch-pads-on-fab-layers" not in args
        elif output.name == "paste":
            assert layers == "F.Paste"
        elif output.name == "mechanical":
            assert layers == "F.Fab,Dwgs.User"
        else:
            raise AssertionError(f"Unexpected footprint export destination: {output}")
        stage = output.name
        names = [n + ".svg" for n in ("LED_Everlight_EAST10105RGBA0", "LED_QTBrightek_QBLP1515A-RGB2A", "QFN_TI_RTQ0056E_8x8mm_P0.5mm_EP5.7mm", "R_Panasonic_ERJ2_0402", "C_Murata_GRM15_0402", "TestPoint_Pad_D1.0mm", "TSSOP_Nexperia_SOT355-1_24", "SC59_Diodes_DMP2066LSN", "SOT23_Diodes_2N7002K", "ESP32-S3-WROOM-1U", "C_Murata_GRM18_0603", "SW_Panasonic_EVQP7J01P", "VQFN_TI_RGT0016C_3x3mm_P0.5mm_EP1.68mm", "UQFN_TI_RSE0010A_2x1.5mm_P0.5mm", "UQFN_TI_RSE0008A_1.5x1.5mm_P0.5mm", "QFN_TI_RTW0024A_4x4mm_P0.5mm_EP2.7mm", "SOT5X3_TI_DRL0008A", "SOT23_TI_DBV0005A", "SOT23_THIN_TI_DDF0008A", "USON_TI_DQA0010A", "X2QFN_TI_RWB0012A_1.6x1.6mm_P0.4mm", "VSON_TI_DSJ0014_4x3mm_P0.5mm_EP2.85x1.58mm", "TDFN_Maxim_T822-3_2x2mm_P0.5mm_EP0.7x1.38mm", "SOT23_TI_DBV0006A")]
    elif args[:2] == ["sch", "erc"]:
        assert "--severity-all" in args and "--exit-code-violations" not in args
        if os.environ.get("RGB_BADGE_TEST_FAIL") == stage:
            return 5
        if os.environ.get("RGB_BADGE_TEST_UNEXPECTED_ERC") == "1":
            records = """[isolated_pin_label]: Label connected to only one pin
    ; warning
    @(10.00 mm, 20.00 mm): Global Label 'UNEXPECTED'
"""
            summary = " ** ERC messages: 1  Errors 0  Warnings 1\n"
        elif os.environ.get("RGB_BADGE_TEST_USB_BOUNDARY_ERC") == "1":
            records = """[isolated_pin_label]: Label connected to only one pin
    ; warning
    @(350.52 mm, 66.04 mm): Global Label 'USB_D-'
[isolated_pin_label]: Label connected to only one pin
    ; warning
    @(350.52 mm, 81.28 mm): Global Label 'USB_D+'
"""
            summary = " ** ERC messages: 2  Errors 0  Warnings 2\n"
        else:
            records = ""
            summary = " ** ERC messages: 0  Errors 0  Warnings 0\n"
        output.write_text("ERC report (stub fixture)\n***** Sheet /\n" + records + summary, encoding="utf-8")
        return 0
    else:
        raise AssertionError(f"Unexpected command: {args}")

    if os.environ.get("RGB_BADGE_TEST_FAIL") == stage:
        return 7
    if stage == "sym/export":
        names.extend(n + "_unit1.svg" for n in ("TPS259472ARPWR", "TPS259474ARPWR", "USB4505-03-0-A", "ERJ-2RKF6203X", "ERA2AEB3651X", "ERA2AEB3481X", "ERA2AEB1131X", "ADG4612BCPZ-REEL7"))
    elif stage in ("fabrication", "copper", "paste", "mechanical"):
        if not (stage == "mechanical" and
                os.environ.get("RGB_BADGE_TEST_MISSING_USB_CONNECTOR") == "1"):
            names.append("USB_C_GCT_USB4505-03-0-A_MidMount.svg")
    if stage in ("fabrication", "copper", "paste", "mechanical"):
        names.extend(("VQFN_TI_RPW0010A_2x2mm_HotRod.svg", "R_Panasonic_ERA2_0402.svg", "LFCSP_ADI_CP16_22_3x3mm_P0.5mm_EP1.75mm.svg"))
    for name in names:
        if name == os.environ.get("RGB_BADGE_TEST_MISSING_NAMED"):
            continue
        file = output / name
        if "QFN_TI_RTQ0056E" in name and stage == "paste" and os.environ.get("RGB_BADGE_TEST_MISSING_PASTE") == "1":
            continue
        # Always exercise a missing/empty export of the second copper part.
        target = stage == "copper" and "QTBrightek" in name
        if target and os.environ.get("RGB_BADGE_TEST_MISSING") == "1":
            continue
        svg = '<svg xmlns="http://www.w3.org/2000/svg"><desc>Test stub, not a KiCad render</desc></svg>\n'
        if stage == "fabrication":
            svg = fabrication_svg("rpw" if "RPW0010A" in name else "led")
            if os.environ.get("RGB_BADGE_TEST_BAD_LABELS") == "1":
                svg = svg.replace('<desc>4</desc>', '<desc>3</desc>')
        if target and os.environ.get("RGB_BADGE_TEST_EMPTY") == "1":
            svg = ""
        file.write_text(svg, encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
