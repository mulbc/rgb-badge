# SPDX-License-Identifier: Apache-2.0
"""Independent brute-force and graph consistency checks for route heuristics."""
import importlib.util
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


if __name__ == '__main__':
    unittest.main()
