# SPDX-License-Identifier: Apache-2.0
"""Exact nearest-goal Manhattan distance for bounded routing searches.

Pass integer (grid_x, grid_y, layer_index * minimum_via_cost) points. When a
cardinal step costs at least one and adjacent-layer changes cost at least that
via cost, this is an admissible, consistent A* lower bound. It ignores obstacles
and does not establish clearance, connectivity or electrical qualification.
"""
from array import array


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


class EmptyGridGoals:
    """Exact empty-grid cost with layer-specific step costs and adjacent vias.

    ``None`` disables horizontal/vertical travel on a layer. Three separable
    min-plus transforms (via, planar, via) suffice: with no obstacles, an
    optimal path can do all planar travel on one cheapest visited layer.
    Goal points are (x, y, layer), queries use layer * width * height + cell.
    This is a lower bound for routing with additional obstacles, not a route.
    """
    def __init__(self, width, height, step_costs, via_cost, goals):
        costs = tuple(step_costs)
        if (any(type(x) is not int or x <= 0 for x in (width, height, via_cost)) or
                not costs or not any(x is not None for x in costs) or
                any(x is not None and (type(x) is not int or x <= 0) for x in costs)):
            raise ValueError('Positive grid dimensions/costs and a moving layer are required')
        infinity = 2**32-1
        bound = (width+height-2)*max(x for x in costs if x is not None)+2*(len(costs)-1)*via_cost
        if bound >= infinity:
            raise ValueError('Distance bound exceeds the uint32 field')
        goals = set(point(p) for p in goals)
        if not goals or any(not (0 <= x < width and 0 <= y < height and 0 <= layer < len(costs))
                            for x, y, layer in goals):
            raise ValueError('Nonempty in-grid goals are required')
        self._size = width*height
        self._count = self._size*len(costs)
        fields = [array('I', [infinity])*self._size for _ in costs]
        for x, y, layer in goals:
            fields[layer][y*width+x] = 0

        def vertical():
            for layers in (range(1, len(fields)), range(len(fields)-2, -1, -1)):
                direction = -1 if layers.step > 0 else 1
                for layer in layers:
                    current, adjacent = fields[layer], fields[layer+direction]
                    for i in range(self._size):
                        candidate = adjacent[i]+via_cost
                        if candidate < current[i]:
                            current[i] = candidate

        vertical()
        for field, cost in zip(fields, costs):
            if cost is None:
                continue
            for row in range(height):
                start, end = row*width, (row+1)*width
                for indices, delta in ((range(start+1, end), -1), (range(end-2, start-1, -1), 1)):
                    for i in indices:
                        candidate = field[i+delta]+cost
                        if candidate < field[i]:
                            field[i] = candidate
            for indices, delta in ((range(width, self._size), -width),
                                   (range(self._size-width-1, -1, -1), width)):
                for i in indices:
                    candidate = field[i+delta]+cost
                    if candidate < field[i]:
                        field[i] = candidate
        vertical()
        self._fields = fields
        self.storage_bytes = sum(len(f)*f.itemsize for f in fields)

    def distance(self, index):
        if type(index) is not int or not 0 <= index < self._count:
            raise ValueError('Query index is outside the grid')
        layer, cell = divmod(index, self._size)
        return self._fields[layer][cell]
