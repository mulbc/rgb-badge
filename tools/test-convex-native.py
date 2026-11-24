#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Cross-check placement SAT against KiCad polygon collision; not board approval."""
import argparse
import hashlib
import json
import math
from pathlib import Path
import random
import pcbnew as p
from convex_geometry import intersects

ROOT=Path(__file__).resolve().parents[1]


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output',type=Path,default=ROOT/'hardware/coupon/rev-a/build/converter-locality-59/convex-native-oracle.json')
    args=ap.parse_args();output=args.output.resolve()
    assert ROOT/'hardware/coupon/rev-a/build' in output.parents and output.suffix=='.json'
    rng=random.Random(5469)
    for _ in range(2000):
        polygons=[]
        for _ in range(2):
            x=rng.randrange(-10000,10001);y=rng.randrange(-10000,10001)
            w=rng.randrange(1000,6000);h=rng.randrange(1000,6000);angle=rng.random()*6.28
            polygons.append([(x+round(dx*math.cos(angle)-dy*math.sin(angle)),
                              y+round(dx*math.sin(angle)+dy*math.cos(angle)))
                             for dx,dy in [(-w,-h),(w,-h),(w,h),(-w,h)]])
        natives=[]
        for points in polygons:
            poly=p.SHAPE_POLY_SET();index=poly.NewOutline()
            for x,y in points:poly.Append(x,y,index)
            natives.append(poly)
        assert bool(natives[0].Collide(natives[1],0))==intersects(*polygons), 'Native polygon oracle differs'
    result={'SPDX-License-Identifier':'CERN-OHL-S-2.0','status':'DETERMINISTIC_NATIVE_POLYGON_COMPARISON_NOT_HARDWARE_MEASUREMENTS',
            'kicad_version':p.GetBuildVersion(),'seed':5469,'convex_rectangle_pairs':2000,'all_results_match':True,
            'touching_policy':'Conservatively classify exact touching as obstructed; explicit host fixture',
            'tool_sha256':{str(path.relative_to(ROOT)):hashlib.sha256(path.read_bytes()).hexdigest()
                           for path in [Path(__file__),ROOT/'tools/convex_geometry.py']}}
    output.parent.mkdir(parents=True,exist_ok=True);output.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print('Convex predicate: 2000 deterministic native fixtures passed.')

if __name__=='__main__':main()
