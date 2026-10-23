#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Check portable routing checkpoint fingerprints and integer rule exceptions."""
import hashlib
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


def validate(plan, manifest):
    assert plan['source_sha256'] == manifest['source_sha256'] == 'da3c3e093acef457ce2d0ebe73b57fd5006b9139a57b7fe8acfcd77e612dc246'
    assert plan['open_edges'] == manifest['native_open_edges'] <= 150
    assert sum(plan['open_edges_by_net'].values()) == plan['open_edges']
    assert manifest['fabrication_release_allowed'] is False
    refs=set()
    allowed_moves={'C51','C55','C71','R109','R3','R38','R39','R5','R63','R70','R71','R8','R81','R84','R85','R87','R88','R89','R97','R99'}
    for pose in plan['placements']:
        assert pose['reference'] in allowed_moves and pose['reference'] not in refs
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
            assert (ax,ay)!=(bx,by) and layer in LAYERS and width == 200000
            length=math.hypot(bx-ax,by-ay)/1e6
            if net in critical:sensitive[net]=sensitive.get(net,0)+length
        else:
            _,net,x,y,top,bottom,diameter,drill=row
            assert all(type(v) is int for v in (x,y,diameter,drill))
            assert abs(LAYERS.index(top)-LAYERS.index(bottom))==1
            assert (diameter,drill)==(300000,100000)
    assert all(length<=5.00001 for length in sensitive.values()), 'Setting route exceeds 5 mm'


def immutable_board_structure(path):
    parser=runpy.run_path(str(ROOT/'tools/check-led-libraries.py'))['parse_sexpr']
    tree=parser(path)
    def normalized(value):
        if not isinstance(value,list):return value
        return [normalized(child) for child in value if not (isinstance(child,list) and child and child[0] in {'uuid','filled_polygon','fill_segments'})]
    retained={'general','paper','layers','setup','net','zone','gr_line','gr_rect','gr_arc','gr_poly','gr_circle'}
    return sorted((normalized(node) for node in tree[1:] if isinstance(node,list) and node and node[0] in retained),key=repr)


def main():
    plan=json.loads(PLAN.read_text());manifest=json.loads(MANIFEST.read_text())
    validate(plan,manifest)
    for path,key in [(SOURCE,'source_sha256'),(OUTPUT,'board_sha256'),(PLAN,'plan_sha256'),
                     (OUTPUT.with_suffix('.kicad_pro'),'project_sha256'),
                     (ROOT/'tools/generate-routing-progress-trial.py','generator_sha256')]:
        assert hashlib.sha256(path.read_bytes()).hexdigest()==manifest[key], (key,'Fingerprint changed')
    assert immutable_board_structure(SOURCE)==immutable_board_structure(OUTPUT), 'Zone definitions, stack, board outline or source nets changed'
    pro=json.loads(OUTPUT.with_suffix('.kicad_pro').read_text())
    assert pro['board']['design_settings']['rules']['min_track_width']==.2
    assert pro['board']['design_settings']['rules']['min_via_annular_width']==.1
    assert len(pro['net_settings']['classes'])==1
    assert pro['net_settings']['classes'][0]['clearance']==.2
    assert pro['net_settings']['classes'][0]['track_width']==.2
    assert pro['net_settings']['classes'][0]['microvia_diameter']==.3
    assert pro['net_settings']['classes'][0]['microvia_drill']==.1
    print('Routing progress: integer plan and fingerprints passed; native connectivity and DRC require the native checker.')


if __name__=='__main__':main()
