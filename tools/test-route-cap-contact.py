#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Native geometry/connectivity fixture for a narrow-to-wide round-cap join."""
import pcbnew as p
from routing_contact_endpoints import end_cap_points

def main():
 b=p.BOARD();own=p.NETINFO_ITEM(b,'OWN');other=p.NETINFO_ITEM(b,'OTHER');b.Add(own);b.Add(other)
 def track(a,z,width,net):
  t=p.PCB_TRACK(b);t.SetStart(p.VECTOR2I(*a));t.SetEnd(p.VECTOR2I(*z));t.SetWidth(width);t.SetLayer(p.B_Cu);t.SetNetCode(net.GetNetCode());b.Add(t);return t
 def pad(x):
  f=p.FOOTPRINT(b);f.SetReference('P'+str(x));f.SetPosition(p.VECTOR2I(x,2000000));q=p.PAD(f);q.SetNumber('1');q.SetSize(p.VECTOR2I(100000,100000));q.SetPosition(f.GetPosition());layers=p.LSET();layers.AddLayer(p.B_Cu);q.SetLayerSet(layers);q.SetAttribute(p.PAD_ATTRIB_SMD);q.SetNetCode(own.GetNetCode());f.Add(q);b.Add(f);return q
 a,z=pad(1000000),pad(3000000)
 stem=track((1000000,2000000),(2000000,2000000),120000,own)
 neighbour=track((1500000,2350000),(2000000,2350000),120000,other)
 blocked=track((2000000,2000000),(3000000,2000000),200000,own)
 assert blocked.GetEffectiveShape(p.B_Cu).Collide(neighbour.GetEffectiveShape(p.B_Cu),200000)
 b.Remove(blocked)
 endpoint=end_cap_points((1000000,2000000),(2000000,2000000),120000,200000)[1]
 joined=track(endpoint,(3000000,2000000),200000,own)
 assert joined.GetEffectiveShape(p.B_Cu).Collide(stem.GetEffectiveShape(p.B_Cu),0)
 assert not joined.GetEffectiveShape(p.B_Cu).Collide(neighbour.GetEffectiveShape(p.B_Cu),200000)
 b.BuildConnectivity()
 assert z.m_Uuid.AsString() in {q.m_Uuid.AsString() for q in b.GetConnectivity().GetConnectedItems(a) if isinstance(q,p.PAD)}
 # A 10 um gap beyond the combined cap radii must lose the native join.
 joined.SetStart(p.VECTOR2I(2170000,2000000));b.BuildConnectivity()
 assert not joined.GetEffectiveShape(p.B_Cu).Collide(stem.GetEffectiveShape(p.B_Cu),0)
 assert z.m_Uuid.AsString() not in {q.m_Uuid.AsString() for q in b.GetConnectivity().GetConnectedItems(a) if isinstance(q,p.PAD)}
 print('PASS native cap overlap joins, adjacent clearance and separated-cap disconnection')
if __name__=='__main__':main()
