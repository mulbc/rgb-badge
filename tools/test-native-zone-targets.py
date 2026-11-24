#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Verify plane-target membership against actual disconnected ground groups."""
from pathlib import Path
import pcbnew as p
from routing_zone_targets import connected_polygons
ROOT=Path(__file__).resolve().parents[1]

def main():
 source=ROOT/'hardware/coupon/rev-a/staging/led-routing-closure-trial-114mm.kicad_pcb'
 b=p.LoadBoard(str(source));pad=next(q for q in b.FindFootprintByReference('J1').Pads() if q.GetNumber()=='A1_B12')
 group={q.m_Uuid.AsString() for q in b.GetConnectivity().GetConnectedItems(pad) if isinstance(q,p.PAD)}
 isolated=[q for f in b.GetFootprints() for q in f.Pads() if q.GetNetname()=='GND' and q.m_Uuid.AsString() not in group]
 assert isolated,'Fixture must retain genuinely disconnected same-net pads'
 regions=connected_polygons(b,pad);assert regions
 actual={q.m_Uuid.AsString():q for q in list(b.GetTracks())+[q for f in b.GetFootprints() for q in f.Pads()]}
 reached={q.m_Uuid.AsString() for q in b.GetConnectivity().GetConnectedItems(pad)}
 for layer,unit,zone,i,witness in regions:
  assert witness in reached and actual[witness].IsOnLayer(layer)
  assert unit.Collide(actual[witness].GetEffectiveShape(layer),0)
  for q in isolated:
   assert not (q.IsOnLayer(layer) and unit.Collide(q.GetEffectiveShape(layer),0)),'Unconnected same-net pad incorrectly included in a plane target'
 print('PASS',len(regions),'copper-witnessed polygons exclude all',len(isolated),'isolated same-net pads')
if __name__=='__main__':main()
