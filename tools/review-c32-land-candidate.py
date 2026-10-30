#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Generate an ignored C32-only land trial; never replace the accepted board."""
from collections import Counter
from pathlib import Path
import argparse
import hashlib
import importlib.util
import json
import math
import shutil
import subprocess
import typing

if not hasattr(typing,'TypeAlias'):
    typing.TypeAlias=object  # KiCad's bundled Python 3.9.
import pcbnew as p

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'hardware/coupon/rev-a/staging/led-routing-progress-trial-114mm.kicad_pcb'
BUILD=ROOT/'hardware/coupon/rev-a/build'
LIBRARY=ROOT/'hardware/coupon/rev-a/staging/library-candidates.pretty'
NAME='C_Murata_GRM188R60J106ME47_0603'
CLI='/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli'


def module(name,file):
    spec=importlib.util.spec_from_file_location(name,ROOT/'tools'/file)
    result=importlib.util.module_from_spec(spec);spec.loader.exec_module(result)
    return result


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,default=BUILD/'c32-land-review/candidate.kicad_pcb')
    args=parser.parse_args();out=args.output.resolve()
    if BUILD.resolve() not in out.parents or out.suffix!='.kicad_pcb':
        parser.error('Output must be a PCB inside the ignored Rev A build directory')
    out.parent.mkdir(parents=True,exist_ok=True)
    c=module('c32_source','check-routing-progress-trial.py')
    check=module('c32_land','check-c32-land-candidate.py')
    check.validate(check.A['parse_sexpr'](LIBRARY/(NAME+'.kicad_mod')))
    digest=hashlib.sha256(SOURCE.read_bytes()).hexdigest()
    old=p.LoadBoard(str(SOURCE));b=p.LoadBoard(str(SOURCE))
    required=Counter(c.signature(old,t) for t in old.GetTracks())
    parts={f.GetReference():f for f in b.GetFootprints()};f=parts['C32']
    assert f.GetFPIDAsString()=='rgb-badge-coupon:C_Murata_GRM18_0603'
    assert f.GetField('MPN').GetText()=='GRM188R60J106ME47D'
    for q in f.Pads():
        assert q.GetNumber() in ['1','2'] and q.GetSize()==p.VECTOR2I(900000,900000)
        assert q.GetFPRelativePosition()==p.VECTOR2I(-800000 if q.GetNumber()=='1' else 800000,0)
        q.SetSize(p.VECTOR2I(650000,700000))
        q.SetFPRelativePosition(p.VECTOR2I(-675000 if q.GetNumber()=='1' else 675000,0))
    centre=f.GetPosition();angle=f.GetOrientation().AsRadians()
    u=(math.cos(angle),math.sin(angle));v=(-u[1],u[0])
    def scaled(point):
        dx,dy=point.x-centre.x,point.y-centre.y
        x=(dx*u[0]+dy*u[1])*1.25/1.5;y=dx*v[0]+dy*v[1]
        return p.VECTOR2I(centre.x+round(x*u[0]+y*v[0]),centre.y+round(x*u[1]+y*v[1]))
    for item in f.GraphicalItems():
        if item.GetLayer()==p.B_CrtYd:
            item.SetStart(scaled(item.GetStart()));item.SetEnd(scaled(item.GetEnd()))
    f.SetFPIDAsString('rgb-badge-coupon-c32-study:'+NAME)
    def identity(q):
        if q.GetParentFootprint().GetReference()=='C32':
            return ('C32',q.GetNumber(),-800000 if q.GetNumber()=='1' else 800000,0)
        return c.physical_identity(q)
    def cluster(board,q):
        return frozenset(identity(z) for z in board.GetConnectivity().GetConnectedItems(q) if isinstance(z,p.PAD))
    prior={}
    for fp in old.GetFootprints():
        other=parts[fp.GetReference()]
        assert fp.GetPosition()==other.GetPosition() and fp.GetOrientation().AsDegrees()==other.GetOrientation().AsDegrees()
        assert sorted((z.GetName(),z.GetText()) for z in fp.GetFields())==sorted((z.GetName(),z.GetText()) for z in other.GetFields())
        if fp.GetReference()!='C32':
            assert fp.GetFPIDAsString()==other.GetFPIDAsString()
            assert Counter(c.local_pad_signature(q) for q in fp.Pads())==Counter(c.local_pad_signature(q) for q in other.Pads())
        for q in fp.Pads():
            if q.GetNetname():prior.setdefault(cluster(old,q),identity(q))
    lookup={identity(q):q for fp in b.GetFootprints() for q in fp.Pads()}
    opens=old.GetConnectivity().GetUnconnectedCount(False)
    for _ in range(3):
        p.ZONE_FILLER(b).Fill(b.Zones());b.BuildConnectivity()
        assert required==Counter(c.signature(b,t) for t in b.GetTracks())
        assert b.GetConnectivity().GetUnconnectedCount(False)==opens
        assert all(g<=cluster(b,lookup[key]) for g,key in prior.items())
    for q in f.Pads():
        assert q.GetSize()==p.VECTOR2I(650000,700000) and q.GetShape()==p.PAD_SHAPE_RECT
        assert q.GetFPRelativePosition()==p.VECTOR2I(-675000 if q.GetNumber()=='1' else 675000,0)
        assert q.GetNetname()==('+3V3_USB' if q.GetNumber()=='1' else 'GND')
    p.SaveBoard(str(out),b)
    for ext in ['.kicad_pro','.kicad_dru']:shutil.copyfile(SOURCE.with_suffix(ext),out.with_suffix(ext))
    table='(fp_lib_table\n'
    for alias,path in [('rgb-badge-coupon',ROOT/'hardware/coupon/rev-a/footprints/rgb-badge-coupon.pretty'),('rgb-badge-coupon-c32-study',LIBRARY)]:
        table+='  (lib (name "'+alias+'")(type "KiCad")(uri "'+str(path)+'")(options "")(descr "Project-local land review"))\n'
    (out.parent/'fp-lib-table').write_text(table+')\n')
    drc=out.with_suffix('.drc.json')
    subprocess.run([CLI,'pcb','drc','--format','json','--output',str(drc),str(out)],check=True)
    d=module('c32_drc','check-colour-fanout-trial.py')
    assert d.findings(drc)==d.findings(ROOT/'docs/development/led-native-control-drc-2026-10-21.json')
    assert hashlib.sha256(SOURCE.read_bytes()).hexdigest()==digest
    report={'SPDX-License-Identifier':'CERN-OHL-S-2.0','status':'UNSELECTED_EXACT_C32_LAND_REVIEW_NOT_HARDWARE_MEASUREMENTS',
            'fabrication_release_allowed':False,'source_sha256':digest,'candidate_board_sha256':hashlib.sha256(out.read_bytes()).hexdigest(),
            'project_sha256':hashlib.sha256(SOURCE.with_suffix('.kicad_pro').read_bytes()).hexdigest(),
            'custom_rules_sha256':hashlib.sha256(SOURCE.with_suffix('.kicad_dru').read_bytes()).hexdigest(),
            'candidate_footprint_sha256':hashlib.sha256((LIBRARY/(NAME+'.kicad_mod')).read_bytes()).hexdigest(),
            'native_open_edges':opens,'unchanged_intrinsic_findings':104,'all_source_copper_retained':True,
            'all_prior_pad_groups_preserved':True,'all_component_poses_and_fields_preserved':True,'stable_refill_passes':3,
            'identity_mapping':'Only corrected C32 numbered pads map back to their explicitly checked legacy +/-0.8 mm reference identities',
            'drc_sha256':hashlib.sha256(drc.read_bytes()).hexdigest(),'kicad_version':p.GetBuildVersion()}
    out.with_suffix('.review.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
    print(json.dumps(report,sort_keys=True))


if __name__=='__main__':main()
