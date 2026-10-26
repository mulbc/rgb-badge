# SPDX-License-Identifier: Apache-2.0
"""ADR 0051's exact fixed DSF pin escapes; no bus-width exception."""
import hashlib
import json
# ref, pin: net, x/y in KiCad integer units, outward x direction.
PADS = {
    ('U48','2'): ('DISPLAY_HEARTBEAT',64650000,1000000,1),
    ('U48','3'): ('GND',64650000,1350000,1),
    ('U48','4'): ('HEARTBEAT_FALL_CLK',63850000,1350000,-1),
    ('U48','6'): ('+3V3_APP',63850000,650000,-1),
    ('U52','1'): ('DISPLAY_CLEAR_3',69650000,650000,1),
    ('U52','2'): ('DISPLAY_ENABLE',69650000,1000000,1),
    ('U52','3'): ('GND',69650000,1350000,1),
    ('U52','4'): ('DISPLAY_CLEAR_OK',68850000,1350000,-1),
    ('U52','6'): ('+3V3_APP',68850000,650000,-1),
}


def validate_necks(plan):
    entries=plan.get('pad_necks',[]);seen=set();selected=[]
    for entry in entries:
        key=(entry['reference'],entry['pin'])
        assert key in PADS and key not in seen, 'Unreviewed or duplicate neck pin'
        seen.add(key);net,x,y,direction=PADS[key];row=entry['track']
        assert len(row)==8 and row[0]=='track' and row[1]==net and row[6]=='B.Cu' and row[7]==120000
        assert all(type(v) is int for v in row[2:6])
        a,b=tuple(row[2:4]),tuple(row[4:6])
        assert (x,y) in (a,b), 'Neck does not start at the exact fixed pad centre'
        end=b if a==(x,y) else a
        assert end[1]==y and 500000<=(end[0]-x)*direction<=700000, 'Neck is bent, reversed or too long'
        assert row in plan['added_copper'];selected.append(tuple(row))
    actual=[tuple(row) for row in plan['added_copper'] if row[0]=='track' and row[7]!=200000]
    assert sorted(actual)==sorted(selected), 'Narrow copper is outside the exact neck inventory'
    return len(entries)


def native_rules():
    text='# SPDX-License-Identifier: CERN-OHL-S-2.0\n(version 1)\n(rule "Default original track floor" (constraint track_width (min 0.20mm)))\n'
    for ref in ['U48','U52']:
        nets=sorted({row[0] for key,row in PADS.items() if key[0]==ref})
        net_clause=' || '.join("A.NetName == '%s'"%net for net in nets)
        condition="A.Layer == 'B.Cu' && A.intersectsCourtyard('%s') && (%s)"%(ref,net_clause)
        text+='(rule "'+ref+' bounded DSF neck"\n (condition "'+condition+'")\n (constraint track_width (min 0.12mm)))\n'
    return text


def project_profile(root,plan):
    """Change only the absolute track floor from the frozen accepted profile."""
    path=root/'mechanical/review/routing-progress-100-project.json'
    assert hashlib.sha256(path.read_bytes()).hexdigest()=='773c27e94eee531af324b2e2d14cd59d76c7b7c9ef43acb4e9f260a2264326b1'
    profile=json.loads(path.read_text())
    if validate_necks(plan):
        profile['board']['design_settings']['rules']['min_track_width']=.12
    return profile
