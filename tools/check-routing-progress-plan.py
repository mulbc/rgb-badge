#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Check portable routing checkpoint fingerprints and integer rule exceptions."""
import hashlib
from collections import Counter
import json
import math
import runpy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLAN = ROOT/'mechanical/review/routing-progress-plan.json'
MANIFEST = ROOT/'mechanical/review/routing-progress-trial.json'
SOURCE = ROOT/'hardware/coupon/rev-a/staging/led-native-control-trial-114mm.kicad_pcb'
OUTPUT = ROOT/'hardware/coupon/rev-a/staging/led-routing-progress-trial-114mm.kicad_pcb'
LAYERS = ['F.Cu','In1.Cu','In2.Cu','In3.Cu','In4.Cu','B.Cu']


def validate_prior_checkpoint(plan):
    """Preserve the accepted 150-edge copper and every subsequent pad join."""
    path=ROOT/'mechanical/review/routing-progress-150-checkpoint.json'
    prior=json.loads(path.read_text())
    assert hashlib.sha256(path.read_bytes()).hexdigest() == 'f2a8891fd42127c4cda64024ec4f43aed1ffd4ac2263b30acde4c6ed8c992dcf'
    assert prior['open_edges']==150 and prior['source_sha256']==plan['source_sha256']
    assert prior['retired_zero_length_tracks']==plan['retired_zero_length_tracks']
    retired=Counter(map(tuple,plan.get('retired_orphan_microvias',[])))
    assert not Counter(map(tuple,prior['added_copper']))-Counter(map(tuple,plan['added_copper']))-retired, 'Accepted 150-edge copper changed'
    current=[(net,set(map(tuple,after))) for net,before,after in plan['physical_group_witnesses']]
    for net,before,after in prior['physical_group_witnesses']:
        group=set(map(tuple,after))
        assert any(name==net and group<=joined for name,joined in current), ('Accepted 150-edge pad group split',net)


def validate_100_checkpoint(plan):
    """Never lose a completed 100-edge connection or change its selected copper."""
    path=ROOT/'mechanical/review/routing-progress-100-checkpoint.json'
    assert hashlib.sha256(path.read_bytes()).hexdigest()=='3b855dd65d133f5e09248447b3fd6782ef509515ea5e94b40d317a999533c889'
    prior=json.loads(path.read_text())
    assert prior['open_edges']==100 and prior['source_sha256']==plan['source_sha256']
    assert not Counter(map(tuple,prior['added_copper']))-Counter(map(tuple,plan['added_copper'])), 'Accepted 100-edge copper changed'
    assert prior['retired_orphan_microvias']==plan['retired_orphan_microvias'], 'Orphan inventory changed beyond the accepted proof'
    assert prior['power_zones']==plan['power_zones'], 'Accepted power-zone definitions changed'
    current=[(net,set(map(tuple,after))) for net,before,after in plan['physical_group_witnesses']]
    for net,before,after in prior['physical_group_witnesses']:
        group=set(map(tuple,after))
        assert any(name==net and group<=joined for name,joined in current), ('Accepted 100-edge pad group split',net)


def validate(plan, manifest):
    runpy.run_path(str(ROOT/'tools/routing_pad_necks.py'))['validate_necks'](plan)
    assert plan['source_sha256'] == manifest['source_sha256'] == 'da3c3e093acef457ce2d0ebe73b57fd5006b9139a57b7fe8acfcd77e612dc246'
    assert plan['open_edges'] == manifest['native_open_edges'] <= 100
    assert sum(plan['open_edges_by_net'].values()) == plan['open_edges']
    assert manifest['fabrication_release_allowed'] is False
    retired=plan.get('retired_orphan_microvias',[])
    assert len(set(map(tuple,retired)))==len(retired)
    for row in retired:
        assert len(row)==8 and row[0]=='via', 'Only witnessed orphan microvias may retire'
        _,net,x,y,top,bottom,diameter,drill=row
        assert all(type(v) is int for v in (x,y,diameter,drill))
        assert abs(LAYERS.index(top)-LAYERS.index(bottom))==1
        assert (diameter,drill)==(300000,100000)
    zones=plan.get('power_zones',[])
    assert len({z['name'] for z in zones})==len(zones), 'Duplicate power-zone name'
    for z in zones:
        assert z['name'].startswith('ADR0049-')
        assert z['net'] in {'+5V_USB','CHARGER_IN_DRAFT','+SYS_APP_IN_DRAFT','+BAT_PROTECTED_DRAFT','VBUS_CONNECTOR'}
        assert z['layer'] in {'In1.Cu','In3.Cu','In4.Cu','B.Cu'}
        assert z['polygons_iu'] and z['definition'][0]=='zone'
        for polygon in z['polygons_iu']:
            for chain in [polygon['outer']]+polygon['holes']:
                assert len(chain)>=3
                assert all(len(xy)==2 and all(type(v) is int for v in xy) and 500000<=xy[0]<=113500000 and 500000<=xy[1]<=32000000 for xy in chain), 'Power parcel outside bounded study'
    refs=set()
    for pose in plan['placements']:
        ref=pose['reference']
        assert ref.startswith(('R','C')) and ref[1:].isdigit() and ref not in {'R45','R46'} and ref not in refs
        refs.add(pose['reference'])
        assert len(pose['old_position_iu'])==len(pose['new_position_iu'])==2
        assert all(type(x) is int for x in pose['old_position_iu']+pose['new_position_iu'])
    assert len(plan['retired_zero_length_tracks']) == 116
    assert all(len(row)==5 and all(type(x) is int for x in (row[1],row[2],row[4]))
               for row in plan['retired_zero_length_tracks'])
    critical={'APP_3V3_FB','VLED_FB','VLED_FB_TOP_MID','LED_IREF','CHARGER_ILIM','CHARGER_ISET','E0_ILM','E1_ILM','E0_DVDT','E1_DVDT','TMP_COLD_SET','TMP_HOT_SET','USB_LOGIC_CT'}
    sensitive={}
    for row in plan['added_copper']:
        assert len(row)==8 and row[0] in {'track','via'}
        if row[0]=='track':
            _,net,ax,ay,bx,by,layer,width=row
            assert all(type(x) is int for x in (ax,ay,bx,by,width))
            assert (ax,ay)!=(bx,by) and layer in LAYERS and width in {120000,200000}
            length=math.hypot(bx-ax,by-ay)/1e6
            if net in critical:sensitive[net]=sensitive.get(net,0)+length
        else:
            _,net,x,y,top,bottom,diameter,drill=row
            assert all(type(v) is int for v in (x,y,diameter,drill))
            assert abs(LAYERS.index(top)-LAYERS.index(bottom))==1
            assert (diameter,drill)==(300000,100000)
    assert all(length<=5.00001 for length in sensitive.values()), 'Setting route exceeds 5 mm'


def immutable_board_structure(path, include_zones=True):
    # The canonical parser uses newer host typing; keep native KiCad 3.9 compatible.
    import subprocess,sys,shutil
    if sys.version_info<(3,10):
        code="import json,runpy,sys;print(json.dumps(runpy.run_path(sys.argv[1])['parse_sexpr'](__import__('pathlib').Path(sys.argv[2]))))"
        tree=json.loads(subprocess.check_output([shutil.which('python3'), '-c',code,str(ROOT/'tools/check-led-libraries.py'),str(path)],text=True))
    else:tree=runpy.run_path(str(ROOT/'tools/check-led-libraries.py'))['parse_sexpr'](path)
    def normalized(value):
        if not isinstance(value,list):return value
        return [normalized(child) for child in value if not (isinstance(child,list) and child and child[0] in {'uuid','filled_polygon','fill_segments'})]
    retained={'general','paper','layers','setup','net','zone','gr_line','gr_rect','gr_arc','gr_poly','gr_circle'}
    return sorted((normalized(node) for node in tree[1:] if isinstance(node,list) and node and node[0] in retained and (include_zones or node[0]!='zone')),key=repr)


def validate_zone_structure(source, output, plan):
    assert immutable_board_structure(source,False)==immutable_board_structure(output,False), 'Stack, board outline or source nets changed'
    original=[n for n in immutable_board_structure(source) if n[0]=='zone']
    actual=[n for n in immutable_board_structure(output) if n[0]=='zone']
    selected=[z['definition'] for z in plan.get('power_zones',[])]
    assert Counter(map(repr,actual))==Counter(map(repr,original+selected)), 'Original or selected zone definition changed'


def validate_profile(plan,manifest):
    pro=json.loads(OUTPUT.with_suffix('.kicad_pro').read_text())
    policy=runpy.run_path(str(ROOT/'tools/routing_pad_necks.py'))
    assert pro==policy['project_profile'](ROOT,plan), 'Unreviewed project-rule change'
    rules=OUTPUT.with_suffix('.kicad_dru')
    if plan.get('pad_necks'):
        assert rules.read_text()==policy['native_rules']()
        assert hashlib.sha256(rules.read_bytes()).hexdigest()==manifest['custom_rules_sha256']
        assert manifest['pad_necks']==len(plan['pad_necks'])
    else:
        assert not rules.exists(), 'Unexpected native custom rules'
    assert pro['board']['design_settings']['rules']['min_via_annular_width']==.1
    assert len(pro['net_settings']['classes'])==1
    assert pro['net_settings']['classes'][0]['clearance']==.2
    assert pro['net_settings']['classes'][0]['track_width']==.2
    assert pro['net_settings']['classes'][0]['microvia_diameter']==.3
    assert pro['net_settings']['classes'][0]['microvia_drill']==.1


def main():
    plan=json.loads(PLAN.read_text());manifest=json.loads(MANIFEST.read_text())
    validate(plan,manifest)
    validate_prior_checkpoint(plan)
    validate_100_checkpoint(plan)
    for path,key in [(SOURCE,'source_sha256'),(OUTPUT,'board_sha256'),(PLAN,'plan_sha256'),
                     (OUTPUT.with_suffix('.kicad_pro'),'project_sha256'),
                     (ROOT/'tools/generate-routing-progress-trial.py','generator_sha256')]:
        assert hashlib.sha256(path.read_bytes()).hexdigest()==manifest[key], (key,'Fingerprint changed')
    validate_zone_structure(SOURCE,OUTPUT,plan)
    validate_profile(plan,manifest)
    print('Routing progress: integer plan and fingerprints passed; native connectivity and DRC require the native checker.')


if __name__=='__main__':main()
