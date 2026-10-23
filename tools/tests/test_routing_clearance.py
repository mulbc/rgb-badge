# SPDX-License-Identifier: Apache-2.0
"""Geometry/caching contracts without a native KiCad dependency."""
from collections import deque
import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location('clearance',
    Path(__file__).resolve().parents[1]/'routing_clearance.py')
c = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c)


class RoutingClearance(unittest.TestCase):
    def test_default_never_overrides_the_conservative_mask(self):
        def forbidden(*args):
            self.fail('Native callback called in default mode')
        screen = c.GridClearance(lambda i: i != 2, forbidden, forbidden)
        self.assertTrue(screen.step(0, 1))
        self.assertFalse(screen.node(2))
        self.assertFalse(screen.step(1, 2))
        self.assertEqual(screen.statistics()['native_point_queries'], 0)

    def test_coarse_clear_points_need_no_native_callbacks(self):
        def forbidden(*args):
            self.fail('Unnecessary native callback')
        screen = c.GridClearance(lambda i: True, forbidden, forbidden, True)
        self.assertTrue(screen.node(2))
        self.assertTrue(screen.step(1, 2))

    def test_clear_endpoints_do_not_make_a_clear_segment(self):
        # A segment through a disk can collide despite clear endpoints.
        screen = c.GridClearance(lambda i: False, lambda i: i in (0, 2),
                                 lambda a, b: False, True)
        self.assertTrue(screen.node(0))
        self.assertTrue(screen.node(2))
        self.assertFalse(screen.step(0, 2))

    def test_blocked_endpoint_prevents_an_edge_query(self):
        def forbidden(*args):
            self.fail('Edge query with a blocked endpoint')
        screen = c.GridClearance(lambda i: False, lambda i: i != 1, forbidden, True)
        self.assertFalse(screen.step(0, 1))
        self.assertFalse(screen.step(1, 0))

    def test_positive_and_negative_cache_entries_and_reverse_edges(self):
        points, edges = [], []
        def point(i):
            points.append(i)
            return i != 3
        def edge(a, b):
            edges.append((a, b))
            return (a, b) == (0, 1)
        screen = c.GridClearance(lambda i: False, point, edge, True)
        for _ in range(3):
            self.assertTrue(screen.step(0, 1))
            self.assertTrue(screen.step(1, 0))
            self.assertFalse(screen.step(0, 2))
            self.assertFalse(screen.step(2, 0))
            self.assertFalse(screen.node(3))
        self.assertEqual(sorted(points), [0, 1, 2, 3])
        self.assertEqual(edges, [(0, 1), (0, 2)])
        self.assertEqual(screen.statistics(), dict(native_point_queries=4,
            native_clear_masked_points=3, native_edge_queries=2, native_clear_masked_edges=1))

    def test_net_or_copper_changes_require_fresh_instances(self):
        old = c.GridClearance(lambda i: False, lambda i: True, lambda a, b: True, True)
        new = c.GridClearance(lambda i: False, lambda i: False, lambda a, b: False, True)
        self.assertTrue(old.step(0, 1))
        self.assertFalse(new.step(0, 1))

    def test_full_grid_matches_independent_geometric_edges(self):
        # Inflated coarse mask excludes a whole column; the actual obstacle is
        # one disk. Compare every graph edge against analytic segment distance.
        width = 7
        def point(i):
            return i % width, i // width
        def exact(a, b):
            ax, ay = point(a); bx, by = point(b)
            dx, dy = bx-ax, by-ay
            ratio = min(1, max(0, ((3-ax)*dx+(3-ay)*dy)/(dx*dx+dy*dy))) if dx or dy else 0
            return (ax+ratio*dx-3)**2+(ay+ratio*dy-3)**2 > .6**2
        screen = c.GridClearance(lambda i: i % width != 3,
            lambda i: exact(i, i), exact, True)
        graph = {}
        for a in range(width*width):
            x, y = point(a)
            graph[a] = []
            for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                if 0 <= x+dx < width and 0 <= y+dy < width:
                    b = a+dx+dy*width
                    self.assertEqual(screen.step(a, b), exact(a, b), (a, b))
                    if screen.step(a, b):
                        graph[a].append(b)
        seen, queue = {0}, deque([0])
        while queue:
            for b in graph[queue.popleft()]:
                if b not in seen:
                    seen.add(b); queue.append(b)
        self.assertEqual(len(seen), 48)
        self.assertNotIn(3+3*width, seen)


if __name__ == '__main__':
    unittest.main()
