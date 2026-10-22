#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Check a mixed-source PCB against the canonical circuit, never release it.

Native XML is needed only to refresh the source-pinned canonical snapshot.
Ordinary checks use controlled source parsers and the existing circuit contract.
"""
import argparse
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path
import runpy
import sys
import tempfile
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / 'hardware/coupon/rev-a'
BOARD = PROJECT / 'staging/led-native-control-trial-114mm.kicad_pcb'
CONTRACT = ROOT / 'mechanical/review/coupon-canonical-net-contract.json'
CHECK = runpy.run_path(str(ROOT / 'tools/check-coupon-controller.py'))
A = CHECK['A']


def require(test, message):
    if not test:
        raise ValueError(message)


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def write(path, value):
    Path(path).write_text(json.dumps(value, indent=2, sort_keys=True, allow_nan=False)+'\n')


def source_paths():
    return sorted(list(PROJECT.glob('*.kicad_sch')) +
                  list((PROJECT/'symbols').glob('*.kicad_sym')) +
                  list((PROJECT/'footprints/rgb-badge-coupon.pretty').glob('*.kicad_mod')))


def refresh(netlist):
    require(Path(netlist).stat().st_mtime_ns >= max(p.stat().st_mtime_ns for p in source_paths()),
            'Native XML predates canonical source; export it again before refreshing')
    CHECK['check_netlist'](netlist)
    xml = ET.parse(netlist).getroot()
    parts = {}
    for c in xml.findall('./components/comp'):
        ref = c.get('ref')
        if ref.startswith('#'):
            continue
        require(ref not in parts, 'Duplicate native reference: '+ref)
        fields = {q.get('name'): q.text or '' for q in c.findall('./fields/field')}
        parts[ref] = dict(value=c.findtext('value'), footprint=c.findtext('footprint'),
                          mpn=fields.get('MPN', ''), manufacturer=fields.get('Manufacturer', ''), pins={})
    for net in xml.findall('./nets/net'):
        for node in net.findall('node'):
            ref, pin = node.get('ref'), node.get('pin')
            if ref.startswith('#'):
                continue
            require(pin not in parts[ref]['pins'], 'Duplicate native pin: '+ref+'.'+pin)
            parts[ref]['pins'][pin] = dict(native_net=net.get('name'),
                no_connect='no_connect' in node.get('pintype', ''))
    return {'SPDX-License-Identifier':'CERN-OHL-S-2.0', 'schema_version':1,
            'status':'CANONICAL_SOURCE_SNAPSHOT_NOT_A_FABRICATION_BOM',
            'native_export_tool':xml.findtext('./design/tool'),
            'source_sha256':{str(p.relative_to(ROOT)):sha(p) for p in source_paths()},
            'components':parts}


def validate_contract(data):
    require(type(data.get('schema_version')) is int and data['schema_version'] == 1,
            'Unsupported canonical contract schema')
    actual = {str(p.relative_to(ROOT)):sha(p) for p in source_paths()}
    require(data['source_sha256'] == actual, 'Canonical source drift: refresh from a checked fresh native XML export')
    # Check exact part identity directly from placed canonical source properties.
    placed = {}
    for path in PROJECT.glob('*.kicad_sch'):
        for symbol in A['children'](A['parse_sexpr'](path), 'symbol'):
            fields = A['property_map'](symbol)
            ref = fields['Reference']
            if ref.startswith('#'):
                continue
            require(ref not in placed, 'Duplicate canonical source reference: '+ref)
            placed[ref] = dict(value=fields['Value'], footprint=fields['Footprint'],
                              mpn=fields.get('MPN', ''), manufacturer=fields.get('Manufacturer', ''))
    require(set(placed) == set(data['components']), 'Canonical snapshot population differs from placed source')
    xml = ET.Element('export')
    components, nets = ET.SubElement(xml, 'components'), ET.SubElement(xml, 'nets')
    grouped = defaultdict(list)
    for ref, part in data['components'].items():
        require({k:part[k] for k in placed[ref]} == placed[ref], 'Canonical part identity differs: '+ref)
        c = ET.SubElement(components, 'comp', ref=ref)
        ET.SubElement(c, 'value').text = part['value']
        ET.SubElement(c, 'footprint').text = part['footprint']
        for pin, entry in part['pins'].items():
            require(type(entry['no_connect']) is bool and
                    entry['no_connect'] == entry['native_net'].startswith('unconnected-('),
                    'Invalid no-connect classification: '+ref+'.'+pin)
            grouped[entry['native_net']].append((ref, pin))
    for name, nodes in grouped.items():
        n = ET.SubElement(nets, 'net', name=name)
        for ref, pin in nodes:
            ET.SubElement(n, 'node', ref=ref, pin=pin)
    # This is model-side verification of the snapshot, not a fresh native run.
    with tempfile.TemporaryDirectory(prefix='rgb-contract-') as folder:
        path = Path(folder)/'contract.xml'
        ET.ElementTree(xml).write(path)
        CHECK['check_netlist'](path)


def read_board(path):
    board = A['parse_sexpr'](path)
    require(board[0] == 'kicad_pcb', 'Expected native KiCad PCB source')
    result = {}
    for f in A['children'](board, 'footprint'):
        fields = A['property_map'](f)
        ref = fields['Reference']
        require(ref not in result, 'Duplicate PCB reference: '+ref)
        pads = []
        for q in A['children'](f, 'pad'):
            nets = A['children'](q, 'net')
            require(len(nets) <= 1, 'Duplicate PCB pad-net declaration: '+ref)
            layers = A['only_child'](q, 'layers', ref+' pad layers')[1:]
            pads.append(dict(number=q[1], net=nets[0][-1] if nets else '',
                             copper=any(l.endswith('.Cu') for l in layers)))
        result[ref] = dict(value=fields['Value'], footprint=f[1],
                          mpn=fields.get('MPN', ''), manufacturer=fields.get('Manufacturer', ''), pads=pads)
    return result


def compare(data, board):
    canonical = data['components']
    rows = {f'Q{i}' for i in range(1,33)}
    pairs = {f'PAIR{i:02d}' for i in range(1,17)}
    projected = {'PROJ_U1_2', 'PROJ_U1_3'}
    require(set(canonical)-set(board) == rows, 'Unexpected missing canonical components')
    require(set(board)-set(canonical) == pairs | projected, 'Unexpected PCB-only components')
    counts = Counter()
    missing_mpn = []
    for ref in sorted(set(canonical) & set(board)):
        expected, actual = canonical[ref], board[ref]
        for key in ('value', 'footprint'):
            require(expected[key] == actual[key], 'PCB '+key+' differs: '+ref)
        require(not actual['mpn'] or actual['mpn'] == expected['mpn'], 'PCB exact MPN differs: '+ref)
        require(not actual['manufacturer'] or actual['manufacturer'] == expected['manufacturer'],
                'PCB manufacturer differs: '+ref)
        if not actual['mpn']:
            missing_mpn.append(ref)
        seen = set()
        for pad in actual['pads']:
            number, net = pad['number'], pad['net']
            if number in expected['pins']:
                entry = expected['pins'][number]
                require(pad['copper'], 'Electrical pin lost its copper: '+ref+'.'+number)
                require(net == ('' if entry['no_connect'] else entry['native_net']),
                        'PCB pad net differs: '+ref+'.'+number)
                seen.add(number)
                counts['matched_physical_electrical_pads'] += 1
            else:
                mechanical = (ref == 'J2' and number == 'MP')
                require(not net and (mechanical or (not number and not pad['copper'])),
                        'Unexpected electrical/mechanical pad: '+ref+'.'+number)
                counts['netless_mechanical_pads' if mechanical else 'non_copper_apertures'] += 1
        require(seen == set(expected['pins']), 'PCB logical pin population differs: '+ref)
        counts['matched_components'] += 1
        counts['matched_logical_pins'] += len(seen)
    for row in range(16):
        ref = f'PAIR{row+1:02d}'
        part = board[ref]
        require(part['value'] == 'NTLJD3119CTBG_TRIAL_ONLY' and
                part['footprint'] == 'rgb-badge-coupon:WDFN6_2x2_onsemi_NTLJD3119C' and
                (not part['mpn'] or part['mpn'] == 'NTLJD3119CTBG'), 'Trial pair identity differs: '+ref)
        p, n = canonical[f'Q{row+1}']['pins'], canonical[f'Q{row+17}']['pins']
        require(p['1']['native_net'] == n['3']['native_net'], 'Canonical row gate contract differs')
        expected = {'1':n['2'], '2':n['1'], '3':p['3'], '4':p['2'], '5':p['1'], '6':n['3']}
        copper = [q for q in part['pads'] if q['copper']]
        require(Counter(q['number'] for q in copper) == Counter({'1':1,'2':1,'3':2,'4':1,'5':1,'6':2}),
                'Trial physical drain/pin population differs: '+ref)
        for q in copper:
            require(q['net'] == expected[q['number']]['native_net'], 'Trial pair pad net differs: '+ref+'.'+q['number'])
        require(all(not q['net'] for q in part['pads'] if not q['copper']), 'Non-copper trial pad has a net')
    for ref in projected:
        part = board[ref]
        require(part['value'] == 'PROJECTED_DRIVER_GEOMETRY_ONLY' and
                part['footprint'] == 'rgb-badge-coupon:QFN_TI_RTQ0056E_8x8mm_P0.5mm_EP5.7mm' and
                not part['mpn'] and
                all(not q['net'] for q in part['pads']), 'Projected geometry became a circuit item: '+ref)
    return {'SPDX-License-Identifier':'CERN-OHL-S-2.0',
            'status':'CHECKED_WITH_DOCUMENTED_STUDY_EXCEPTIONS', 'fabrication_release_allowed':False,
            'canonical_components':len(canonical), 'study_footprints':len(board), **dict(counts),
            'trial_pairs_with_checked_logical_pin_maps':16, 'netless_projected_drivers':2,
            'absent_canonical_row_devices':sorted(rows), 'pcb_references_missing_exact_mpn_fields':missing_mpn,
            'limitations':['Trial row pairs have not replaced the canonical schematic/BOM',
                           'Projected final-driver footprints are netless geometry only',
                           'PCB exact MPN fields remain absent where listed; canonical MPNs are not inferred as PCB approval',
                           'This checks logical source assignment, not physical connectivity, DRC, electrical behavior or independent Gate A']}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--refresh-contract', action='store_true')
    ap.add_argument('--netlist', type=Path)
    ap.add_argument('--contract', type=Path, default=CONTRACT)
    ap.add_argument('--board', type=Path, default=BOARD)
    ap.add_argument('--report', type=Path)
    args = ap.parse_args()
    try:
        if args.refresh_contract:
            require(args.netlist is not None, 'A fresh checked native XML export is required to refresh the snapshot')
            data = refresh(args.netlist)
            validate_contract(data)
            write(args.contract, data)
        else:
            data = json.loads(args.contract.read_text())
            validate_contract(data)
            if args.netlist:
                require(refresh(args.netlist) == data, 'Fresh native XML differs from the source-pinned snapshot')
        result = compare(data, read_board(args.board))
        result.update(board_sha256=sha(args.board), canonical_contract_sha256=sha(args.contract),
                      checker_sha256=sha(__file__), native_xml_verified_this_run=args.netlist is not None)
        if args.report:
            write(args.report, result)
        print(f"Study contract passed: {result['matched_components']} common components, "
              f"{result['matched_logical_pins']} logical pins; known study exceptions retained; fabrication prohibited.")
    except (ValueError, KeyError, OSError, ET.ParseError) as error:
        print('Study contract failed: '+str(error), file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
