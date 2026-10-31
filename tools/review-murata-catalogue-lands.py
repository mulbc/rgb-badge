#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Read-only comparison with the supplied 2021 catalogue, not part approval."""
import argparse
from decimal import Decimal as D
import hashlib
import json
from pathlib import Path
import runpy

ROOT = Path(__file__).resolve().parents[1]
HELPERS = runpy.run_path(str(ROOT/'tools/check-led-libraries.py'))
PARSE, CHILDREN = HELPERS['parse_sexpr'], HELPERS['children']
FOOTPRINTS = ROOT/'hardware/coupon/rev-a/footprints/rgb-badge-coupon.pretty'
CATALOGUE_SHA256 = '40827b0048b9af98017b011f5497ee063e5c4382c2d9eef3d95b5e8141530bb4'
ROWS = {
    '18_within_0.10': {'a':('0.6','0.8'),'b':('0.6','0.7'),'c':('0.6','0.8')},
    '18_0.15_or_0.20': {'a':('0.7','0.9'),'b':('0.7','0.8'),'c':('0.8','1.0')},
    '21_within_0.10': {'a':('1.2','1.2'),'b':('0.6','0.6'),'c':('1.25','1.25')},
    '21_0.15': {'a':('1.2','1.2'),'b':('0.6','0.8'),'c':('1.2','1.4')},
    '21_0.20': {'a':('1.0','1.4'),'b':('0.6','0.8'),'c':('1.2','1.4')},
}


def one(node, name):
    result = CHILDREN(node,name)
    assert len(result)==1, 'Expected one '+name
    return result[0]


def dimensions(fp):
    pads = sorted(CHILDREN(fp,'pad'),key=lambda pad:pad[1])
    assert [pad[1] for pad in pads]==['1','2']
    sizes = [tuple(map(D,one(pad,'size')[1:3])) for pad in pads]
    assert sizes[0]==sizes[1] and all(v>0 for v in sizes[0])
    positions = [tuple(map(D,one(pad,'at')[1:3])) for pad in pads]
    assert positions[0][1]==positions[1][1]==0 and positions[0][0]==-positions[1][0]<0
    assert all(len(one(pad,'at'))==3 or D(one(pad,'at')[3])==0 for pad in pads)
    length,width = sizes[0]
    gap = positions[1][0]-positions[0][0]-length
    assert gap>0
    return {'a':gap,'b':length,'c':width}


def mismatches(measured,row):
    return [name for name in ('a','b','c') if not D(row[name][0])<=measured[name]<=D(row[name][1])]


def report():
    parts = json.loads((ROOT/'mechanical/review/coupon-canonical-net-contract.json').read_text())['components']
    records = {}
    for identity,footprint,code,page in [
        ('GRM187R61A226ME15','C_Murata_GRM18_0603','18',107),
        ('GRM219R60J476ME44','C_Murata_GRM21_0805','21',109)]:
        path = FOOTPRINTS/(footprint+'.kicad_mod')
        measured = dimensions(PARSE(path))
        rows = {name:dict(ranges_mm={key:list(bounds) for key,bounds in row.items()},
                          out_of_range_dimensions=mismatches(measured,row))
                for name,row in ROWS.items() if name.startswith(code+'_')}
        refs = sorted(ref for ref,part in parts.items() if part['mpn']==identity)
        assert refs and all(parts[ref]['footprint']=='rgb-badge-coupon:'+footprint for ref in refs)
        records[identity] = dict(source_identity_is_provisional_without_packaging_code=True,
            references=refs,footprint=footprint,footprint_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
            catalogue_part_list_page=page,measured_mm={key:str(value) for key,value in measured.items()},
            catalogue_family_rows=rows,matches_any_listed_family_row=any(not row['out_of_range_dimensions'] for row in rows.values()),
            current_exact_part_drawing_approved=False)
    return {'SPDX-License-Identifier':'CERN-OHL-S-2.0',
        'status':'SUPPLIED_2021_CATALOGUE_GEOMETRY_FINDINGS_NO_SOURCE_MIGRATION',
        'catalogue_sha256':CATALOGUE_SHA256,
        'supplied_filenames':['490_Chip_Multilayer_CAT2021_MLCC.pdf','Chip_Multilayer_CAT2021_MLCC.pdf'],
        'supplied_files_are_byte_identical':True,'catalogue_visible_date':'2021-01-18',
        'catalogue_part_specification_cutoff':'2020-11','catalogue_page_count':287,
        'diagram_page':277,'reflow_table_page':278,
        'dimension_definitions':{'a':'inner copper gap','b':'one copper land length','c':'transverse copper land width'},
        'parts':records,'source_geometry_changed':False,'fabrication_release_allowed':False,
        'limitations':['Generic historical catalogue; current exact-part approval is not established',
            'Body-tolerance row and orderable packaging code require exact-part verification',
            'No shared land shrink, substitution or capacitor derating approval follows',
            'Assembly/process, electrical and independent Gate A holds remain open']}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output',type=Path)
    ap.add_argument('--verify-report',type=Path)
    ap.add_argument('--vendor-pdf',type=Path)
    args = ap.parse_args()
    if args.vendor_pdf:
        assert hashlib.sha256(args.vendor_pdf.read_bytes()).hexdigest()==CATALOGUE_SHA256, 'Wrong catalogue bytes'
    result = report()
    if args.verify_report:
        assert json.loads(args.verify_report.read_text())==result, 'Recorded catalogue comparison differs'
    if args.output:
        output = args.output.resolve()
        assert (ROOT/'hardware/coupon/rev-a/build').resolve() in output.parents and output.suffix=='.json'
        output.parent.mkdir(parents=True,exist_ok=True)
        output.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    for identity,row in result['parts'].items():
        print(identity,row['measured_mm'],'matches listed family row:',row['matches_any_listed_family_row'])
    print('Read-only catalogue comparison; exact-part drawing and order-code approval remain open.')


if __name__=='__main__': main()
