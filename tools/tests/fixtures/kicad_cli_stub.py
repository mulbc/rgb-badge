#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Test-only CLI stub. Its output is not a KiCad render or ERC result."""

import os
from pathlib import Path
import sys
import xml.etree.ElementTree as ET


def fabrication_svg():
    # Minimal KiCad-shaped text structure for wrapper/overlay tests. The paths
    # are deliberately dummy strokes, not a real LED footprint or digit font.
    groups = "".join(
        f'<g style="fill:none;stroke:#000000;stroke-width:0.012500;stroke-linecap:round">'
        f'<g class="stroked-text"><desc>{number}</desc>'
        f'<path d="M{x} {y} L{x + 0.1} {y + 0.15}"/></g></g>'
        for number, x, y in ((1, 1.3, 0.4), (2, 1.3, 1.3), (3, 0.4, 1.3), (4, 0.4, 0.4))
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
        root = coupon_netlist()
        if os.environ.get('RGB_BADGE_TEST_BAD_MATRIX') == '1':
            root.find('./nets/net/node').set('pin', '99')
        if os.environ.get('RGB_BADGE_TEST_BAD_DRIVER') == '1':
            root.find("./nets/net/node[@ref='U1'][@pin='57']").set('pin','58')
        output.write_bytes(ET.tostring(root))
        return 0
    elif args[:3] == ["sch", "export", "pdf"]:
        assert '--black-and-white' in args
        if os.environ.get('RGB_BADGE_TEST_FAIL') == 'pdf':
            return 7
        output.write_text('Stub only: not a PDF or KiCad render.\n')
        return 0
    elif args[:3] == ["sym", "export", "svg"]:
        names = [n + "_unit1.svg" for n in ("EAST10105RGBA0", "QBLP1515A-RGB2A", "TLC59581RTQT", "ERJ-2RKF3922X", "ERJ-2RKF1003X", "GRM155R71C104KA88D", "PWR_FLAG", "TestPoint_Pad", "74HC4514PW,118", "DMP2066LSN-7", "2N7002K-7", "ERJ-2RKF1001X")]
    elif args[:3] == ["fp", "export", "svg"]:
        layers = args[args.index("--layers") + 1]
        if output.name == "fabrication":
            assert layers == "F.Fab,F.SilkS,F.CrtYd", "Fabrication view must exclude solid pad layers"
            assert "--sketch-pads-on-fab-layers" in args
        elif output.name == "copper":
            assert layers == "F.Cu", "Copper view must exclude non-copper outlines"
            assert "--sketch-pads-on-fab-layers" not in args
        elif output.name == "paste":
            assert layers == "F.Paste"
        else:
            raise AssertionError(f"Unexpected footprint export destination: {output}")
        stage = output.name
        names = [n + ".svg" for n in ("LED_Everlight_EAST10105RGBA0", "LED_QTBrightek_QBLP1515A-RGB2A", "QFN_TI_RTQ0056E_8x8mm_P0.5mm_EP5.7mm", "R_Panasonic_ERJ2_0402", "C_Murata_GRM15_0402", "TestPoint_Pad_D1.0mm", "TSSOP_Nexperia_SOT355-1_24", "SC59_Diodes_DMP2066LSN", "SOT23_Diodes_2N7002K")]
    elif args[:2] == ["sch", "erc"]:
        assert "--severity-all" in args and "--exit-code-violations" in args
        if os.environ.get("RGB_BADGE_TEST_FAIL") == stage:
            return 5
        output.write_text("Stub only: no real ERC was run.\n", encoding="utf-8")
        return 0
    else:
        raise AssertionError(f"Unexpected command: {args}")

    if os.environ.get("RGB_BADGE_TEST_FAIL") == stage:
        return 7
    for name in names:
        file = output / name
        if "QFN_TI" in name and stage == "paste" and os.environ.get("RGB_BADGE_TEST_MISSING_PASTE") == "1":
            continue
        # Always exercise a missing/empty export of the second copper part.
        target = stage == "copper" and "QTBrightek" in name
        if target and os.environ.get("RGB_BADGE_TEST_MISSING") == "1":
            continue
        svg = '<svg xmlns="http://www.w3.org/2000/svg"><desc>Test stub, not a KiCad render</desc></svg>\n'
        if stage == "fabrication":
            svg = fabrication_svg()
            if os.environ.get("RGB_BADGE_TEST_BAD_LABELS") == "1":
                svg = svg.replace('<desc>4</desc>', '<desc>3</desc>')
        if target and os.environ.get("RGB_BADGE_TEST_EMPTY") == "1":
            svg = ""
        file.write_text(svg, encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
