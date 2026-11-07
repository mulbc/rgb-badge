# SPDX-License-Identifier: Apache-2.0
import importlib.util
from pathlib import Path
import unittest
spec=importlib.util.spec_from_file_location('convex',Path(__file__).resolve().parents[1]/'convex_geometry.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

class ConvexGeometry(unittest.TestCase):
    def test_disjoint_diagonal_polygons_can_have_overlapping_boxes(self):
        a=[(0,2),(2,0),(4,2),(2,4)];b=[(3,5),(5,3),(7,5),(5,7)]
        self.assertFalse(m.intersects(a,b));self.assertFalse(m.intersects(b,a))
    def test_containment_crossing_and_edge_touch_are_obstructions(self):
        a=[(0,0),(10,0),(10,10),(0,10)]
        for b in [[(2,2),(3,2),(3,3),(2,3)],[(8,-2),(12,2),(8,6),(4,2)],[(10,2),(12,2),(12,4),(10,4)]]:
            with self.subTest(polygon=b):self.assertTrue(m.intersects(a,b))
    def test_clockwise_order_and_large_translation_preserve_result(self):
        a=[(0,0),(4,0),(4,4),(0,4)];b=[(5,0),(9,0),(9,4),(5,4)]
        offset=lambda q:[(x+100000000,y+100000000) for x,y in q]
        self.assertFalse(m.intersects(offset(a[::-1]),offset(b)))
    def test_degenerate_or_concave_inputs_are_rejected(self):
        for q in [[(0,0),(1,0),(2,0)],[(0,0),(2,0),(1,1),(2,2),(0,2)],[(0,0),(0,0),(1,1)],[(0,3),(3,3),(1,0),(2,5),(4,0)]]:
            with self.subTest(polygon=q),self.assertRaises(AssertionError):m.intersects(q,[(0,0),(2,0),(0,2)])

if __name__=='__main__':unittest.main()
