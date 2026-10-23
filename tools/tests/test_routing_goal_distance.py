# SPDX-License-Identifier: Apache-2.0
"""Independent brute-force and graph consistency checks for route heuristics."""
import importlib.util
import heapq
from pathlib import Path
import random
import unittest

spec = importlib.util.spec_from_file_location('distance', Path(__file__).resolve().parents[1]/'routing_goal_distance.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


def brute(goals, query):
    return min(sum(abs(a-b) for a, b in zip(goal, query)) for goal in goals)


class RoutingGoalDistance(unittest.TestCase):
    def test_bounding_rectangle_does_not_hide_distance_to_actual_copper(self):
        goals = [(0, 0, 0), (100, 100, 0)]
        self.assertEqual(m.ManhattanGoals(goals).distance((50, 50, 0)), 100)

    def test_every_goal_is_zero_including_duplicate_inputs(self):
        goals = [(0, 0, 0), (3, -4, 20), (3, -4, 20), (100, 19, 100)]
        index = m.ManhattanGoals(iter(goals))
        for goal in goals:
            self.assertEqual(index.distance(goal), 0)

    def test_seeded_sparse_and_dense_sets_match_brute_force(self):
        rng = random.Random(20261022)
        for size in (1, 2, 3, 16, 127, 512):
            goals = [(rng.randrange(-1200, 1201), rng.randrange(-400, 401), rng.randrange(6)*20)
                     for _ in range(size)]
            index = m.ManhattanGoals(goals)
            for _ in range(150):
                q = (rng.randrange(-1500, 1501), rng.randrange(-600, 601), rng.randrange(6)*20)
                self.assertEqual(index.distance(q), brute(goals, q))

    def test_layer_and_cardinal_neighbor_consistency(self):
        goals = [(0, 0, 100), (15, 10, 0), (3, 9, 40)]
        index = m.ManhattanGoals(goals)
        for x in range(-2, 18):
            for y in range(-2, 13):
                for layer in range(6):
                    current = (x, y, layer*20)
                    neighbors = [((x+1, y, layer*20), 1), ((x, y+1, layer*20), 1)]
                    if layer < 5:
                        neighbors.append(((x, y, (layer+1)*20), 20))
                    for other, cost in neighbors:
                        self.assertLessEqual(abs(index.distance(current)-index.distance(other)), cost)

    def test_unbounded_python_integers_have_no_distance_cap(self):
        goals = [(10**30, -10**40, 0), (-10**35, 10**39, 100)]
        q = (-10**45, -10**42, -10**30)
        self.assertEqual(m.ManhattanGoals(goals).distance(q), brute(goals, q))

    def test_invalid_empty_and_noninteger_coordinates_are_rejected(self):
        with self.assertRaises(ValueError):
            m.ManhattanGoals([])
        for q in [(0, 0), (0, 0, 0, 0), (0.0, 0, 0), (True, 0, 0), ('0', 0, 0)]:
            with self.subTest(point=q):
                with self.assertRaises(ValueError):
                    m.ManhattanGoals([q])
                with self.assertRaises(ValueError):
                    m.ManhattanGoals([(0, 0, 0)]).distance(q)

    def test_goal_order_cannot_change_distance(self):
        goals = [(x, y, z) for x in (-20, 0, 20) for y in (-4, 1, 9) for z in (0, 20, 80)]
        indexes = [m.ManhattanGoals(goals), m.ManhattanGoals(reversed(goals))]
        for q in [(x, 5-x, 40) for x in range(-30, 31)]:
            self.assertEqual(indexes[0].distance(q), indexes[1].distance(q))


def graph_distances(width, height, costs, via, goals):
    """Independent shortest-path oracle over explicit empty-grid graph edges."""
    distances = {g: 0 for g in goals}
    queue = [(0, g) for g in goals]
    heapq.heapify(queue)
    while queue:
        cost, node = heapq.heappop(queue)
        if distances[node] != cost:
            continue
        x, y, layer = node
        edges = []
        if costs[layer] is not None:
            edges += [((a, b, layer), costs[layer]) for a, b in
                      [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
                      if 0 <= a < width and 0 <= b < height]
        edges += [((x, y, other), via) for other in (layer-1, layer+1) if 0 <= other < len(costs)]
        for other, step in edges:
            candidate = cost+step
            if candidate < distances.get(other, float('inf')):
                distances[other] = candidate
                heapq.heappush(queue, (candidate, other))
    return distances


class EmptyGridDistance(unittest.TestCase):
    def test_complete_fields_match_independent_dijkstra(self):
        rng = random.Random(20261023)
        for width, height in [(1, 1), (1, 7), (7, 1), (4, 5), (7, 6)]:
            for costs in [(5, 1), (5, 1, 1, None, 1, 1), (None, 3, None), (7,)]:
                goals = {(rng.randrange(width), rng.randrange(height), rng.randrange(len(costs)))
                         for _ in range(4)}
                field = m.EmptyGridGoals(width, height, costs, 20, goals)
                oracle = graph_distances(width, height, costs, 20, goals)
                for (x, y, layer), expected in oracle.items():
                    self.assertEqual(field.distance(layer*width*height+y*width+x), expected)
                self.assertEqual(field.storage_bytes, width*height*len(costs)*4)

    def test_rear_travel_can_be_cheaper_than_a_round_trip_to_an_inner_layer(self):
        field = m.EmptyGridGoals(30, 1, (5, 1), 20, [(0, 0, 0)])
        self.assertEqual(field.distance(1), 5)
        self.assertEqual(field.distance(10), 50)
        self.assertEqual(field.distance(11), 51)
        self.assertEqual(field.distance(29), 69)

    def test_disabled_plane_requires_a_vertical_detour_for_planar_travel(self):
        field = m.EmptyGridGoals(4, 1, (1, None, 1), 20, [(0, 0, 1)])
        self.assertEqual(field.distance(4), 0)
        self.assertEqual(field.distance(5), 41)
        self.assertEqual(field.distance(7), 43)

    def test_stronger_field_never_underestimates_the_old_lower_bound(self):
        goals = [(0, 0, 0), (3, 2, 3)]
        field = m.EmptyGridGoals(5, 4, (5, 1, None, 1), 20, goals)
        old = m.ManhattanGoals((x, y, layer*20) for x, y, layer in goals)
        for layer in range(4):
            for y in range(4):
                for x in range(5):
                    self.assertGreaterEqual(field.distance(layer*20+y*5+x), old.distance((x, y, layer*20)))

    def test_duplicate_goal_order_does_not_change_the_field(self):
        goals = [(1, 2, 0), (4, 1, 2), (1, 2, 0)]
        a = m.EmptyGridGoals(6, 4, (5, None, 1), 7, iter(goals))
        b = m.EmptyGridGoals(6, 4, (5, None, 1), 7, reversed(goals))
        self.assertEqual([a.distance(i) for i in range(72)], [b.distance(i) for i in range(72)])

    def test_invalid_grid_cost_goal_and_query_inputs_are_rejected(self):
        for args in [(0, 2, (1,), 20, [(0, 0, 0)]), (2, True, (1,), 20, [(0, 0, 0)]),
                     (2, 2, (), 20, [(0, 0, 0)]), (2, 2, (None,), 20, [(0, 0, 0)]),
                     (2, 2, (0,), 20, [(0, 0, 0)]), (2, 2, (1,), 0, [(0, 0, 0)]),
                     (2, 2, (1.0,), 20, [(0, 0, 0)]), (2, 2, (1,), 20, []),
                     (2, 2, (1,), 20, [(2, 0, 0)]), (2, 2, (1,), 20, [(0, 0, 1)])]:
            with self.subTest(args=args), self.assertRaises(ValueError):
                m.EmptyGridGoals(*args)
        field = m.EmptyGridGoals(2, 2, (1,), 20, [(0, 0, 0)])
        for index in (-1, 4, 0.0, True):
            with self.subTest(index=index), self.assertRaises(ValueError):
                field.distance(index)

    def test_uint32_cost_overflow_is_rejected_before_allocation(self):
        with self.assertRaisesRegex(ValueError, 'uint32'):
            m.EmptyGridGoals(2, 2, (2**32,), 20, [(0, 0, 0)])


if __name__ == '__main__':
    unittest.main()
