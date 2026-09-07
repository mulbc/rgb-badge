#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Check the matrix draft's source wiring or an actual KiCad XML netlist.

Source checking traces the simple unrotated LED/short-wire/global-label subset.
It is deliberately separate from KiCad's own connectivity engine and ERC.
"""

import argparse
from collections import Counter, defaultdict
from decimal import Decimal
from pathlib import Path
import runpy
import sys
import xml.etree.ElementTree as ET


AUDIT = runpy.run_path(str(Path(__file__).with_name('check-led-libraries.py')))
children = AUDIT['children']
one = AUDIT['only_child']
properties = AUDIT['property_map']
parse = AUDIT['parse_sexpr']
PARTS = AUDIT['PARTS']


def expected_matrix():
    components, connections = {}, {}
    for number in range(1, 257):
        row, column = divmod(number-1, 16)
        ref = f'D{number}'
        mpn = 'EAST10105RGBA0' if column < 8 else 'QBLP1515A-RGB2A'
        components[ref] = (mpn, PARTS[mpn]['footprint_property'])
        for function, pin in PARTS[mpn]['pins'].items():
            net = f'ROW_{row:02d}_A' if function == 'A' else f'COL_{column:02d}_{function[0]}'
            connections[(ref, pin)] = net
    return components, connections


def validate(components, connections):
    expected_components, expected_connections = expected_matrix()
    if components != expected_components:
        missing = sorted(set(expected_components) - set(components))
        extra = sorted(set(components) - set(expected_components))
        wrong = sorted(ref for ref in set(components) & set(expected_components) if components[ref] != expected_components[ref])
        raise ValueError(f'LED population/footprint mismatch; missing={missing}, extra={extra}, wrong={wrong}')
    if connections != expected_connections:
        mismatches = [
            f'{ref}.{pin}: expected {net}, found {connections.get((ref, pin))}'
            for (ref, pin), net in expected_connections.items()
            if connections.get((ref, pin)) != net
        ]
        extra = set(connections) - set(expected_connections)
        raise ValueError('LED connection mismatch: ' + '; '.join(mismatches[:8]) + (f'; extra pins={sorted(extra)}' if extra else ''))
    counts = Counter(connections.values())
    if len(counts) != 64 or set(counts.values()) != {16}:
        raise ValueError('Expected 16 row nets and 48 colour-column nets, with 16 LED pins per net')


def put_unique(mapping, key, value, context):
    if key in mapping:
        raise ValueError(f'Duplicate {context}: {key}')
    mapping[key] = value


def read_netlist(path):
    root = ET.parse(path).getroot()
    if root.tag != 'export':
        raise ValueError('Expected a KiCad XML netlist export')
    components, connections = {}, {}
    for component in root.findall('./components/comp'):
        if component.get('ref') in {'U1', 'R1', 'R2', 'R3', 'R4', 'R5', 'C1', '#FLG01', '#FLG02'}:
            continue  # Checked by check-coupon-driver.py, including complete population.
        put_unique(components, component.get('ref'), (component.findtext('value'), component.findtext('footprint')), 'component')
    for net in root.findall('./nets/net'):
        for node in net.findall('node'):
            if node.get('ref') in {'U1', 'R1', 'R2', 'R3', 'R4', 'R5', 'C1', '#FLG01', '#FLG02'}:
                continue
            put_unique(connections, (node.get('ref'), node.get('pin')), net.get('name'), 'netlist node')
    validate(components, connections)


def position(expression):
    at = one(expression, 'at', 'position')
    return Decimal(at[1]), Decimal(at[2])


def read_sources(project_dir):
    root = parse(project_dir / 'rgb-badge-coupon.kicad_sch')
    root_uuid = one(root, 'uuid', 'root')[1]
    sheets = children(root, 'sheet')
    if len(sheets) != 5 or children(root, 'symbol') or sum(properties(s)['Sheetfile'] == 'driver.kicad_sch' for s in sheets) != 1:
        raise ValueError('Expected four matrix sheets plus one driver sheet and no root components')
    library = {symbol[1]: symbol for symbol in children(parse(AUDIT['SYMBOL_LIBRARY']), 'symbol')}
    components, connections, all_uuids, sheet_files = {}, {}, set(), set()

    def check_uuids(expression):
        if expression[0] == 'uuid':
            if expression[1] in all_uuids:
                raise ValueError(f'Duplicate source UUID: {expression[1]}')
            all_uuids.add(expression[1])
        for child in expression[1:]:
            if isinstance(child, list):
                check_uuids(child)

    check_uuids(root)
    for sheet in sheets:
        filename = properties(sheet)['Sheetfile']
        if filename in sheet_files or Path(filename).name != filename:
            raise ValueError('Expected four distinct, project-local matrix sheets')
        sheet_files.add(filename)
        if filename == 'driver.kicad_sch':
            check_uuids(parse(project_dir / filename))
            continue  # Driver checker validates this sheet and its library.
        sheet_uuid = one(sheet, 'uuid', filename)[1]
        source = parse(project_dir / filename)
        check_uuids(source)
        if children(source, 'no_connect') or children(source, 'sheet') or children(source, 'bus') or children(source, 'label'):
            raise ValueError(f'{filename}: source check supports only the flat, global-label matrix draft')
        cache = one(source, 'lib_symbols', filename)
        cached = {}
        for symbol in children(cache, 'symbol'):
            mpn = symbol[1].removeprefix('rgb-badge-coupon:')
            if mpn not in library or symbol != [symbol[0], 'rgb-badge-coupon:' + mpn, *library[mpn][2:]]:
                raise ValueError(f'{filename}: embedded symbol differs from the controlled library')
            cached[symbol[1]] = symbol

        graph, labels = defaultdict(set), defaultdict(set)
        for wire in children(source, 'wire'):
            points = children(one(wire, 'pts', filename), 'xy')
            if len(points) != 2:
                raise ValueError('Expected a two-endpoint wire')
            a, b = [tuple(map(Decimal, point[1:])) for point in points]
            if a == b or (a[0] != b[0] and a[1] != b[1]):
                raise ValueError('Expected a non-zero axis-aligned wire')
            graph[a].add(b)
            graph[b].add(a)
        for label in children(source, 'global_label'):
            anchor = position(label)
            labels[anchor].add(label[1])
            angle = one(label, 'at', 'global label')[3]
            justification = one(one(label, 'effects', 'global label'), 'justify', 'global label')[1:]
            # In the actual KiCad PDF, angle 0 puts text to the right of its
            # anchor; angle 180 puts it to the left. The attached wire must
            # approach from the other side or it strikes through the text.
            valid = {'0': ('left', -1), '180': ('right', 1)}
            if angle not in valid or justification != [valid[angle][0]]:
                raise ValueError(f'{filename}: unsupported global-label orientation')
            neighbours = graph[anchor]
            if len(neighbours) != 1 or any(
                end[1] != anchor[1] or (end[0]-anchor[0])*valid[angle][1] <= 0
                for end in neighbours
            ):
                raise ValueError(f'{filename}: wire runs through global-label text: {label[1]}')

        for symbol in children(source, 'symbol'):
            props = properties(symbol)
            ref = props['Reference']
            put_unique(components, ref, (props['Value'], props['Footprint']), 'source component')
            if props['MPN'] != props['Value']:
                raise ValueError(f'{ref}: MPN differs from Value')
            if one(symbol, 'at', ref)[3] != '0' or children(symbol, 'mirror') or one(symbol, 'unit', ref)[1] != '1':
                raise ValueError(f'{ref}: source check supports only unrotated, unmirrored, single-unit LEDs')
            for field, value in [('in_bom', 'yes'), ('on_board', 'yes'), ('dnp', 'no')]:
                if one(symbol, field, ref)[1] != value:
                    raise ValueError(f'{ref}: unexpected {field}')
            number = int(ref.removeprefix('D'))
            row, column = divmod(number-1, 16)
            if props['Matrix Row'] != str(row) or props['Matrix Column'] != str(column):
                raise ValueError(f'{ref}: row/column metadata mismatch')
            instance = one(one(one(symbol, 'instances', ref), 'project', ref), 'path', ref)
            if instance[1] != f'/{root_uuid}/{sheet_uuid}' or one(instance, 'reference', ref)[1] != ref:
                raise ValueError(f'{ref}: hierarchy instance/reference mismatch')
            x, y = position(symbol)
            lib = cached[one(symbol, 'lib_id', ref)[1]]
            for unit in children(lib, 'symbol'):
                for pin in children(unit, 'pin'):
                    px, py = position(pin)
                    start = (x+px, y-py)
                    visited, pending, names = set(), [start], set()
                    while pending:
                        point = pending.pop()
                        if point in visited:
                            continue
                        visited.add(point)
                        names.update(labels[point])
                        pending.extend(graph[point] - visited)
                    pin_number = one(pin, 'number', ref)[1]
                    if len(names) != 1:
                        raise ValueError(f'{ref}.{pin_number}: expected one connected global net, found {sorted(names)}')
                    put_unique(connections, (ref, pin_number), names.pop(), 'source pin')
    validate(components, connections)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project-dir', type=Path, default=AUDIT['PROJECT_DIR'])
    parser.add_argument('--netlist', type=Path, help='Check KiCad XML instead of the source subset')
    args = parser.parse_args()
    try:
        if args.netlist:
            read_netlist(args.netlist)
            print('KiCad XML matrix connectivity check passed: 256 LEDs, 1024 pins, 16 row nets, 48 colour-column nets.')
        else:
            read_sources(args.project_dir)
            print('Matrix source connectivity check passed: 256 LEDs, 1024 pins, 16 row nets, 48 colour-column nets (not KiCad ERC).')
    except (OSError, ValueError, KeyError, IndexError, ET.ParseError) as error:
        print(f'Matrix check failed: {error}', file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
