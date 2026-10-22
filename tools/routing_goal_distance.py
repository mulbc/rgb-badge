# SPDX-License-Identifier: Apache-2.0
"""Exact nearest-goal Manhattan distance for bounded routing searches.

Pass integer (grid_x, grid_y, layer_index * minimum_via_cost) points. When a
cardinal step costs at least one and adjacent-layer changes cost at least that
via cost, this is an admissible, consistent A* lower bound. It ignores obstacles
and does not establish clearance, connectivity or electrical qualification.
"""


def point(value):
    result = tuple(value)
    if len(result) != 3 or any(type(x) is not int for x in result):
        raise ValueError('Expected three integer coordinates')
    return result


class ManhattanGoals:
    """Balanced spatial index; query values exactly equal a brute-force minimum."""

    def __init__(self, goals):
        points = sorted(set(point(p) for p in goals))
        if not points:
            raise ValueError('At least one goal is required')
        self._tree = self._build(points)

    @classmethod
    def _build(cls, points):
        low = tuple(min(p[d] for p in points) for d in range(3))
        high = tuple(max(p[d] for p in points) for d in range(3))
        axis = max(range(3), key=lambda d: high[d]-low[d])
        points.sort(key=lambda p: p[axis])
        mid = len(points)//2
        return (points[mid], low, high,
                cls._build(points[:mid]) if mid else None,
                cls._build(points[mid+1:]) if mid+1 < len(points) else None)

    @staticmethod
    def _bound(pt, node):
        return sum(max(lo-x, 0, x-hi) for x, lo, hi in zip(pt, node[1], node[2]))

    @classmethod
    def _nearest(cls, pt, node, best):
        if cls._bound(pt, node) >= best:
            return best
        best = min(best, sum(abs(x-y) for x, y in zip(pt, node[0])))
        children = [n for n in node[3:] if n]
        children.sort(key=lambda n: cls._bound(pt, n))
        for child in children:
            best = cls._nearest(pt, child, best)
        return best

    def distance(self, query):
        pt = point(query)
        # An actual goal gives a finite upper bound, with no arbitrary cap.
        best = sum(abs(x-y) for x, y in zip(pt, self._tree[0]))
        return self._nearest(pt, self._tree, best)
