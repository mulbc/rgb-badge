#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Native regression: pad-edge copper contacts escape intrinsic land gaps."""
from pathlib import Path
import hashlib
import importlib.util
import json
import shutil
import subprocess
import sys
import pcbnew as p

ROOT=Path(__file__).resolve().parents[1]
BUILD=ROOT/'hardware/coupon/rev-a/build/native-control-search/pad-contact-endpoint-regression'
CLI='/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli'


def main():
    BUILD.mkdir(parents=True,exist_ok=True)
    source=BUILD/'source.kicad_pcb';board=p.BOARD();board.SetCopperLayerCount(6)
    nets={}
    for code,name in enumerate(['DISPLAY_CLEAR_3','GUARD_A','GUARD_B','GND'],1):
        net=p.NETINFO_ITEM(board,name,code);board.Add(net);nets[name]=net
    for ref,net,x,y,w,h in [('P1','DISPLAY_CLEAR_3',2,2,.7,.2),('P2','DISPLAY_CLEAR_3',3.5,2,.5,.5),('N1','GUARD_A',2,1.45,.2,.7),('N2','GUARD_B',2,2.55,.2,.7),('G1','GND',4,4,.3,.3),('G2','GND',5,4,.3,.3)]:
        footprint=p.FOOTPRINT(board);footprint.SetReference(ref);footprint.SetLayer(p.B_Cu);footprint.SetAttributes(p.FP_SMD);footprint.Reference().SetVisible(False);footprint.Value().SetVisible(False)
        footprint.SetPosition(p.VECTOR2I(p.FromMM(x),p.FromMM(y)))
        pad=p.PAD(footprint);pad.SetNumber('1');pad.SetAttribute(p.PAD_ATTRIB_SMD);pad.SetShape(p.PAD_SHAPE_RECT)
        pad.SetSize(p.VECTOR2I(p.FromMM(w),p.FromMM(h)));pad.SetPosition(footprint.GetPosition())
        layers=p.LSET();layers.AddLayer(p.B_Cu);pad.SetLayerSet(layers);pad.SetNetCode(nets[net].GetNetCode());footprint.Add(pad);board.Add(footprint)
    corners=[(.5,.5),(6,.5),(6,5),(.5,5)]
    for a,z in zip(corners,corners[1:]+corners[:1]):
        edge=p.PCB_SHAPE(board);edge.SetShape(p.SHAPE_T_SEGMENT);edge.SetStart(p.VECTOR2I(*[p.FromMM(v) for v in a]));edge.SetEnd(p.VECTOR2I(*[p.FromMM(v) for v in z]));edge.SetLayer(p.Edge_Cuts);edge.SetWidth(p.FromMM(.05));board.Add(edge)
    held=p.PCB_TRACK(board);held.SetStart(p.VECTOR2I(p.FromMM(4),p.FromMM(4)));held.SetEnd(p.VECTOR2I(p.FromMM(5),p.FromMM(4)));held.SetLayer(p.B_Cu);held.SetWidth(200000);held.SetNetCode(nets['GND'].GetNetCode());board.Add(held)
    board.BuildConnectivity();assert board.GetConnectivity().GetUnconnectedCount(False)==1
    p.SaveBoard(str(source),board);digest=hashlib.sha256(source.read_bytes()).hexdigest()
    spec=importlib.util.spec_from_file_location('drc',ROOT/'tools/check-colour-fanout-trial.py');drc=importlib.util.module_from_spec(spec);spec.loader.exec_module(drc)
    profile=ROOT/'mechanical/review/routing-progress-100-project.json'
    def findings(path):
        shutil.copyfile(profile,path.with_suffix('.kicad_pro'));report=path.with_suffix('.drc.json')
        subprocess.run([CLI,'pcb','drc','--format','json','--output',str(report),str(path)],check=True)
        return drc.findings(report)
    baseline=findings(source);assert sum(baseline.values())==2;assert sum('"type": "clearance"' in row for row in baseline)==2
    previous=None
    for label in ['first','replay']:
        output=BUILD/(label+'.kicad_pcb');report=BUILD/(label+'.json')
        subprocess.run([sys.executable,str(ROOT/'tools/search-native-control-routes.py'),'--source',str(source),'--output',str(output),'--report',str(report),'--native-grid','--heuristic','empty-grid','--max-nodes','10000','--nets','DISPLAY_CLEAR_3'],check=True)
        result=json.loads(report.read_text());assert result['open_edges']==0, result['routes']
        assert result['source_sha256']==digest and hashlib.sha256(source.read_bytes()).hexdigest()==digest
        assert findings(output)==baseline, 'A new track inherited an intrinsic pad clearance violation'
        loaded=p.LoadBoard(str(output));assert loaded.GetConnectivity().GetUnconnectedCount(False)==0
        for track in loaded.GetTracks():
            if not isinstance(track,p.PCB_VIA):assert track.GetWidth()==200000 and track.GetStart()!=track.GetEnd()
        ground=[t for t in loaded.GetTracks() if t.GetNetname()=='GND'];assert len(ground)==1 and ground[0].GetStart()==held.GetStart() and ground[0].GetEnd()==held.GetEnd()
        identity=lambda b:sorted((f.GetReference(),q.GetNumber(),q.GetPosition().x,q.GetPosition().y,q.GetSize().x,q.GetSize().y,q.GetNetname()) for f in b.GetFootprints() for q in f.Pads())
        assert identity(loaded)==identity(board), 'Fixture pads changed'
        if previous is not None:assert output.read_bytes()==previous, 'Fixture replay differs'
        previous=output.read_bytes()
    print('Native pad-contact regression passed: one full-width join, unchanged two intrinsic clearances, fixed pads/source and exact replay.')


if __name__=='__main__':main()
