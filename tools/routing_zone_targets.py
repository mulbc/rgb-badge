# SPDX-License-Identifier: Apache-2.0
"""Filled-plane components with an actual copper witness in the anchor group.

A zone object can contain disconnected filled islands. Its pointer alone is
never a connectivity witness. Return only individual filled polygons which
physically touch native copper reached from the requested pad. New routes must
still pass a refill and the independent native pad-group join check.
"""
def connected_polygons(board,pad):
 import pcbnew as p
 actual={q.m_Uuid.AsString():q for q in list(board.GetTracks())+[q for f in board.GetFootprints() for q in f.Pads()]}
 items=[actual[q.m_Uuid.AsString()] for q in board.GetConnectivity().GetConnectedItems(pad) if q.m_Uuid.AsString() in actual]+[pad]
 result=[]
 for zone in board.Zones():
  if zone.GetNetCode()!=pad.GetNetCode():continue
  layer=zone.GetLayer();filled=zone.GetFilledPolysList(layer)
  copper=[q for q in items if q.IsOnLayer(layer)]
  for i in range(filled.OutlineCount()):
   unit=filled.UnitSet(i);box=unit.BBox()
   witness=next((q for q in copper if box.Intersects(q.GetBoundingBox()) and unit.Collide(q.GetEffectiveShape(layer),0)),None)
   if witness is not None:result.append((layer,unit,zone.m_Uuid.AsString(),i,witness.m_Uuid.AsString()))
 return result
