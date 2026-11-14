# SPDX-License-Identifier: Apache-2.0
"""Optional exact-shape fallback for a conservative, immutable search grid.

Callbacks belong to one net and one unchanged copper state. Create a new screen
after each attempted join; cached geometry decisions must never cross a refill
or copper mutation. This does not screen zones or replace complete native DRC.
"""


class GridClearance:
    def __init__(self, coarse, point_clear, edge_clear, enabled=False):
        self.coarse = coarse
        self.point_clear = point_clear
        self.edge_clear = edge_clear
        self.enabled = enabled
        self.points = {}
        self.edges = {}

    def node(self, index):
        if self.coarse(index):
            return True
        if not self.enabled:
            return False
        if index not in self.points:
            self.points[index] = bool(self.point_clear(index))
        return self.points[index]

    def step(self, first, second):
        if self.coarse(first) and self.coarse(second):
            return True
        if not self.enabled or not self.node(first) or not self.node(second):
            return False
        key = tuple(sorted((first, second)))
        if key not in self.edges:
            self.edges[key] = bool(self.edge_clear(*key))
        return self.edges[key]

    def statistics(self):
        return dict(native_point_queries=len(self.points),
                    native_clear_masked_points=sum(self.points.values()),
                    native_edge_queries=len(self.edges),
                    native_clear_masked_edges=sum(self.edges.values()))
