# SPDX-License-Identifier: Apache-2.0
"""Exact ADR 0047 digital-width exception; no general narrowing permission."""
from collections import Counter
import hashlib
import json
import math
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
CATALOG=ROOT/'mechanical/review/routing-progress-digital-width.json'
CATALOG_SHA256='f7537d0eaaccceba289105f9d95557d26d7de794a96937ef489b8c97f2d7501c'
LAYERS=['F.Cu','In1.Cu','In2.Cu','In3.Cu','In4.Cu','B.Cu']
NETS=['USB_RAW_OUT2','UART0_TX','LED_SOUT']


def catalog():
    assert hashlib.sha256(CATALOG.read_bytes()).hexdigest()==CATALOG_SHA256, 'Digital-width catalog changed'
    return json.loads(CATALOG.read_text())


def validate_plan(plan,required=False):
    if 'digital_width' not in plan and not required:return Counter()
    entry=plan.get('digital_width')
    assert entry==catalog(), 'Exact digital-width catalog omitted or changed'
    assert entry['nets']==NETS and entry['track_width_iu']==120000
    assert entry['maximum_narrow_length_per_net_iu']==120000000
    assert entry['joined_pads']=={'USB_RAW_OUT2':[['U24','3'],['R61','1'],['U31','8']],'UART0_TX':[['R47','2'],['TP4','1']],'LED_SOUT':[['U1','42'],['U3','22'],['TP1','1']]}
    rows=entry['added_copper'];assert len(rows)==len(set(map(tuple,rows)))
    narrow=Counter();lengths=Counter()
    for row in rows:
        assert len(row)==8 and row[1] in NETS, 'Net outside digital-width scope'
        if row[0]=='track':
            assert row[7]==120000 and row[6] in LAYERS
            assert all(type(x) is int for x in row[2:6]) and row[2:4]!=row[4:6]
            narrow[tuple(row)]+=1;lengths[row[1]]+=math.dist(row[2:4],row[4:6])
        else:
            assert row[0]=='via' and row[6:]==[300000,100000]
            assert all(type(x) is int for x in row[2:4])
            assert abs(LAYERS.index(row[4])-LAYERS.index(row[5]))==1
    assert all(length<=120000001 for length in lengths.values()), 'Digital-width length bound exceeded'
    added=Counter(map(tuple,plan['added_copper']))
    assert not Counter(map(tuple,rows))-added, 'Reviewed digital copper missing'
    actual=Counter(tuple(row) for row in plan['added_copper'] if row[0]=='track' and row[1] in NETS and row[7]!=200000)
    assert actual==narrow, 'Unreviewed narrow digital copper'
    return narrow


def native_rule(plan):
    if 'digital_width' not in plan:return ''
    validate_plan(plan,required=True)
    return ''.join('\n(rule "ADR0047 exact ' + net + ' width"\n (condition "A.NetName == \'' + net + '\'")\n (constraint track_width (min 0.12mm)))\n' for net in NETS)


def verify_native(board,plan,signature,physical_cluster):
    wanted=validate_plan(plan)
    if not wanted:return 0
    actual=Counter(signature(board,t) for t in board.GetTracks())
    assert not wanted-actual, 'Native digital copper missing'
    for net in NETS:
        pads={(part.GetReference(),pad.GetNumber()):pad
              for part in board.GetFootprints() for pad in part.Pads() if pad.GetNetname()==net}
        expected=set(map(tuple,catalog()['joined_pads'][net]))
        assert set(pads)==expected, 'Digital source pin inventory differs'
        groups={physical_cluster(board,pad) for pad in pads.values()}
        assert len(groups)==1, 'Digital status source pads are not joined: '+net
    return sum(wanted.values())
