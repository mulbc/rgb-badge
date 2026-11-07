#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Native regression: legal pads outside the search grid can reach nearby cells."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys
import pcbnew as p

ROOT = Path(__file__).resolve().parents[1]
BUILD = ROOT/'hardware/coupon/rev-a/build/native-control-search/edge-endpoint-regression'


def main():
    BUILD.mkdir(parents=True,exist_ok=True)
    source=BUILD/'source.kicad_pcb'
    board=p.BOARD();board.SetCopperLayerCount(6)
    nets={}
    for code,name in enumerate(['DISPLAY_CLEAR_3','DISPLAY_ENABLE','GND'],1):
        net=p.NETINFO_ITEM(board,name,code);board.Add(net);nets[name]=net
    for ref,net,x,y in [('P1','DISPLAY_CLEAR_3',2,.65),('P2','DISPLAY_CLEAR_3',3,1.5),
                         ('P3','DISPLAY_ENABLE',4,31.85),('P4','DISPLAY_ENABLE',5,31),
                         ('G1','GND',10,10),('G2','GND',11,10)]:
        footprint=p.FOOTPRINT(board);footprint.SetReference(ref);footprint.SetLayer(p.B_Cu)
        footprint.SetPosition(p.VECTOR2I(p.FromMM(x),p.FromMM(y)))
        pad=p.PAD(footprint);pad.SetNumber('1');pad.SetAttribute(p.PAD_ATTRIB_SMD)
        pad.SetShape(p.PAD_SHAPE_RECT);pad.SetSize(p.VECTOR2I(p.FromMM(.6),p.FromMM(.17)))
        pad.SetPosition(footprint.GetPosition());layers=p.LSET();layers.AddLayer(p.B_Cu)
        pad.SetLayerSet(layers);pad.SetNetCode(nets[net].GetNetCode());footprint.Add(pad);board.Add(footprint)
    held=p.PCB_TRACK(board);held.SetStart(p.VECTOR2I(p.FromMM(10),p.FromMM(10)))
    held.SetEnd(p.VECTOR2I(p.FromMM(11),p.FromMM(10)));held.SetLayer(p.B_Cu)
    held.SetWidth(p.FromMM(.2));held.SetNetCode(nets['GND'].GetNetCode());board.Add(held)
    board.BuildConnectivity();assert board.GetConnectivity().GetUnconnectedCount(False)==2
    p.SaveBoard(str(source),board);digest=hashlib.sha256(source.read_bytes()).hexdigest()
    previous=None
    for label in ['first','replay']:
        output=BUILD/(label+'.kicad_pcb');report=BUILD/(label+'.json')
        subprocess.run([sys.executable,str(ROOT/'tools/search-native-control-routes.py'),
            '--source',str(source),'--output',str(output),'--report',str(report),
            '--native-grid','--heuristic','empty-grid','--max-nodes','10000',
            '--nets','DISPLAY_CLEAR_3','DISPLAY_ENABLE'],check=True)
        result=json.loads(report.read_text());assert result['open_edges']==0
        assert len(result['routes'])==2 and all(row['routed'] for row in result['routes'])
        assert result['source_sha256']==digest and hashlib.sha256(source.read_bytes()).hexdigest()==digest
        assert result['width_mm']==.2 and result['clearance_mm']==.2
        loaded=p.LoadBoard(str(output));tracks=list(loaded.GetTracks())
        assert loaded.GetConnectivity().GetUnconnectedCount(False)==0
        positions=lambda b: sorted((f.GetReference(),q.GetNumber(),q.GetPosition().x,q.GetPosition().y,q.GetNetname()) for f in b.GetFootprints() for q in f.Pads())
        assert positions(loaded)==positions(board),'Fixture pads moved or changed net'
        ground=[t for t in tracks if t.GetNetname()=='GND']
        assert len(ground)==1 and ground[0].GetStart()==held.GetStart() and ground[0].GetEnd()==held.GetEnd()
        for track in tracks:
            if isinstance(track,p.PCB_VIA):
                assert track.GetViaType()==p.VIATYPE_MICROVIA
                assert track.GetWidth(track.TopLayer())==300000 and track.GetDrillValue()==100000
                stack=list(loaded.GetEnabledLayers().CuStack())
                assert abs(stack.index(track.TopLayer())-stack.index(track.BottomLayer()))==1
            else:
                assert track.GetWidth()==200000 and track.GetStart()!=track.GetEnd()
        if previous is not None:assert output.read_bytes()==previous,'Fixture replay differs'
        previous=output.read_bytes()
    print('Native edge-endpoint regression passed: two boundary joins, source/ground retention and exact replay.')


if __name__=='__main__':
    main()
