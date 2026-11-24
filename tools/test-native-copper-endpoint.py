#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Actual orphan-copper endpoint fixture; no temporary or deleted source pads."""
import hashlib,json,subprocess,sys
from pathlib import Path
import pcbnew as p
from routing_closure import signature
ROOT=Path(__file__).resolve().parents[1]
BUILD=ROOT/'hardware/coupon/rev-a/build/native-copper-endpoint'
def main():
 BUILD.mkdir(parents=True,exist_ok=True);b=p.BOARD();b.SetCopperLayerCount(6);net=p.NETINFO_ITEM(b,'OWN');b.Add(net)
 f=p.FOOTPRINT(b);f.SetReference('P1');f.SetLayer(p.B_Cu);f.SetPosition(p.VECTOR2I(6000000,5000000));q=p.PAD(f);q.SetNumber('1');q.SetSize(p.VECTOR2I(600000,600000));q.SetPosition(f.GetPosition());ls=p.LSET();ls.AddLayer(p.B_Cu);q.SetLayerSet(ls);q.SetAttribute(p.PAD_ATTRIB_SMD);q.SetNetCode(net.GetNetCode());f.Add(q);b.Add(f)
 v=p.PCB_VIA(b);v.SetPosition(p.VECTOR2I(5000000,5000000));v.SetViaType(p.VIATYPE_MICROVIA);v.SetLayerPair(p.In4_Cu,p.B_Cu);v.SetWidth(300000);v.SetDrill(100000);v.SetNetCode(net.GetNetCode());b.Add(v)
 for a,z in [((5000000,5000000),(4500000,5000000)),((4500000,5000000),(4500000,4500000)),((4500000,4500000),(5000000,4500000)),((5000000,4500000),(5000000,5000000))]:
  t=p.PCB_TRACK(b);t.SetStart(p.VECTOR2I(*a));t.SetEnd(p.VECTOR2I(*z));t.SetLayer(p.In4_Cu);t.SetWidth(200000);t.SetNetCode(net.GetNetCode());b.Add(t)
 b.BuildConnectivity();assert b.GetConnectivity().GetUnconnectedCount(False)==1
 assert not [x for x in b.GetConnectivity().GetConnectedItems(v) if isinstance(x,p.PAD)]
 original={t.m_Uuid.AsString():signature(b,t) for t in b.GetTracks()}
 src=BUILD/'source.kicad_pcb';p.SaveBoard(str(src),b);src.with_suffix('.kicad_pro').write_text('{}\n');src.with_suffix('.kicad_dru').write_text('(version 1)\n');before=hashlib.sha256(src.read_bytes()).hexdigest()
 for targeted in [False,True]:
  out=BUILD/('targeted.kicad_pcb' if targeted else 'normal.kicad_pcb');report=out.with_suffix('.json');cmd=[sys.executable,str(ROOT/'tools/search-routing-closure.py'),'--source',str(src),'--output',str(out),'--report',str(report),'--nets','OWN','--native-grid','--weight','1','--max-nodes','10000']
  if targeted:cmd+=['--source-copper-uuid',v.m_Uuid.AsString()]
  proc=subprocess.run(cmd,cwd=ROOT,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT);out.with_suffix('.log').write_text(proc.stdout);assert proc.returncode==0,proc.stdout
  z=p.LoadBoard(str(out));qq=[r for fp in z.GetFootprints() for r in fp.Pads()];assert len(qq)==1 and qq[0].m_Uuid.AsString()==q.m_Uuid.AsString();vv=next(t for t in z.GetTracks() if t.m_Uuid.AsString()==v.m_Uuid.AsString());assert vv.GetPosition()==v.GetPosition() and vv.GetViaType()==v.GetViaType()
  actual={t.m_Uuid.AsString():signature(z,t) for t in z.GetTracks()};assert all(actual.get(k)==v for k,v in original.items())
  assert qq[0].GetPosition()==q.GetPosition() and qq[0].GetSize()==q.GetSize() and qq[0].GetNetname()=='OWN'
  connected=any(x.m_Uuid.AsString()==q.m_Uuid.AsString() for x in z.GetConnectivity().GetConnectedItems(vv) if isinstance(x,p.PAD));assert connected==targeted
  result=json.loads(report.read_text())
  assert z.GetConnectivity().GetUnconnectedCount(False)==(0 if targeted else 1)
  if targeted:assert result['routes'][0]['routed']
  else:assert result['routes']==[]
 assert hashlib.sha256(src.read_bytes()).hexdigest()==before
 print('PASS native actual-copper endpoint joins orphan via without adding/deleting pads; normal pad-only search leaves it untouched')
if __name__=='__main__':main()
