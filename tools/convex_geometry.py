# SPDX-License-Identifier: Apache-2.0
"""Exact integer convex-polygon screening for unselected placement experiments."""


def bounds(points):
    return (min(x for x,y in points),min(y for x,y in points),
            max(x for x,y in points),max(y for x,y in points))


def convex(points):
    if len(points)<3 or len(set(points))!=len(points):return False
    side=None
    for a,b in zip(points,points[1:]+points[:1]):
        values=[(b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0]) for c in points]
        positive=any(x>0 for x in values);negative=any(x<0 for x in values)
        if positive and negative:return False
        current=1 if positive else -1 if negative else None
        if current is not None:
            if side is not None and side!=current:return False
            side=current
    return side is not None



def intersects(first,second):
    """SAT for two convex polygons; touching counts as an obstruction."""
    assert convex(first) and convex(second), 'Convex nondegenerate polygons required'
    for points in (first,second):
        for a,b in zip(points,points[1:]+points[:1]):
            nx,ny=a[1]-b[1],b[0]-a[0]
            p=[x*nx+y*ny for x,y in first];q=[x*nx+y*ny for x,y in second]
            if max(p)<min(q) or max(q)<min(p):return False
    return True
