"""
Task B1: Implement and Instrument Backtracking Search for Graph Colouring
Author: Rakshana V
Course: CSA06 Design and Analysis of Algorithms (CO5 Assignment 5)
"""

import time

class InstrumentedGraphColouring:
    def __init__(self, num_vertices, edges, m):
        self.n = num_vertices
        self.m = m
        self.adj = {i: set() for i in range(num_vertices)}
        for u, v in edges:
            self.adj[u].add(v)
            self.adj[v].add(u)
        self.reset_metrics()

    def reset_metrics(self):
        self.search_nodes_visited = 0
        self.candidate_assignments = 0
        self.rejected_branches = 0
        self.backtracks = 0
        self.max_search_depth = 0
        self.colours = [-1] * self.n

    def is_safe(self, vertex, colour):
        for neighbor in self.adj[vertex]:
            if self.colours[neighbor] == colour:
                return False
        return True

    def solve(self, heuristic="static"):
        self.reset_metrics()
        if self.n == 0:
            return True, []
        if self.m <= 0:
            return False, None

        if heuristic == "static":
            order = list(range(self.n))
            found = self._backtrack_static(0, order)
        elif heuristic == "degree_mrv":
            # Dynamic MRV (Minimum Remaining Values) with Degree tie-breaking
            found = self._backtrack_dynamic(0)
        else:
            raise ValueError("Unknown heuristic")

        return found, (list(self.colours) if found else None)

    def _backtrack_static(self, depth, order):
        self.search_nodes_visited += 1
        if depth > self.max_search_depth:
            self.max_search_depth = depth

        if depth == self.n:
            return True

        vertex = order[depth]
        for c in range(1, self.m + 1):
            self.candidate_assignments += 1
            if self.is_safe(vertex, c):
                self.colours[vertex] = c
                if self._backtrack_static(depth + 1, order):
                    return True
                # Undo operation
                self.colours[vertex] = -1
                self.backtracks += 1
            else:
                self.rejected_branches += 1

        return False

    def _select_next_vertex_mrv_degree(self):
        unassigned = [v for v in range(self.n) if self.colours[v] == -1]
        def score(v):
            used_neighbor_colours = {self.colours[nb] for nb in self.adj[v] if self.colours[nb] != -1}
            remaining_colours = self.m - len(used_neighbor_colours)
            unassigned_degree = sum(1 for nb in self.adj[v] if self.colours[nb] == -1)
            # Minimize remaining legal colours (MRV), maximize unassigned degree (Degree Heuristic)
            return (remaining_colours, -unassigned_degree, v)
        return min(unassigned, key=score)

    def _backtrack_dynamic(self, depth):
        self.search_nodes_visited += 1
        if depth > self.max_search_depth:
            self.max_search_depth = depth

        if depth == self.n:
            return True

        vertex = self._select_next_vertex_mrv_degree()
        for c in range(1, self.m + 1):
            self.candidate_assignments += 1
            if self.is_safe(vertex, c):
                self.colours[vertex] = c
                if self._backtrack_dynamic(depth + 1):
                    return True
                # Undo operation
                self.colours[vertex] = -1
                self.backtracks += 1
            else:
                self.rejected_branches += 1

        return False

    def get_metrics(self):
        return {
            "search_nodes": self.search_nodes_visited,
            "candidate_assignments": self.candidate_assignments,
            "rejected_branches": self.rejected_branches,
            "backtracks": self.backtracks,
            "max_depth": self.max_search_depth,
        }


def run_experiments():
    test_cases = [
        {
            "name": "Test 1: Colourable Graph (6-Vertex Cloud Service Network, m=3)",
            "n": 6,
            "edges": [(0, 1), (0, 2), (1, 2), (1, 3), (2, 4), (3, 4), (3, 5), (4, 5)],
            "m": 3,
            "purpose": "Verify correct valid assignment on a moderately constrained planar/wheel-like conflict graph."
        },
        {
            "name": "Test 2: Uncolourable Graph (K4 Clique embedded in 6 vertices, m=3)",
            "n": 6,
            "edges": [(0, 4), (1, 5), (2, 3), (2, 4), (2, 5), (3, 4), (3, 5), (4, 5)],
            "m": 3,
            "purpose": "Verify exhaustive pruning and false termination when chromatic number (4) > m (3), especially when clique appears late in static order."
        },
        {
            "name": "Test 3: Boundary Case A (Disconnected/Zero-Edge Graph, n=5, m=1)",
            "n": 5,
            "edges": [],
            "m": 1,
            "purpose": "Verify boundary condition where no conflicts exist and 1 server group suffices without backtracking."
        },
        {
            "name": "Test 4: Boundary Case B (m=0 Server Groups, n=3)",
            "n": 3,
            "edges": [(0, 1)],
            "m": 0,
            "purpose": "Verify immediate failure detection when zero server groups are available."
        },
        {
            "name": "Test 5: Star-Cycle Hybrid (8 vertices, m=3) - Ordering Impact",
            "n": 8,
            "edges": [(0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 0)],
            "m": 3,
            "purpose": "Compare static ordering (hub vertex 7 last) vs MRV+Degree heuristic (hub vertex 7 first) on an odd-wheel W7 (chromatic number 4, m=3)."
        }
    ]

    print("=" * 85)
    print("TASK B1: INSTRUMENTED GRAPH COLOURING - VALIDATION & HEURISTIC COMPARISON")
    print("=" * 85)

    for tc in test_cases:
        print(f"\n>>> {tc['name']}")
        print(f"    Purpose: {tc['purpose']}")
        solver = InstrumentedGraphColouring(tc["n"], tc["edges"], tc["m"])

        found_v1, sol_v1 = solver.solve(heuristic="static")
        m_v1 = solver.get_metrics()

        found_v2, sol_v2 = solver.solve(heuristic="degree_mrv")
        m_v2 = solver.get_metrics()

        print(f"    Result: Colourable = {found_v1} | V1 Colouring = {sol_v1} | V2 Colouring = {sol_v2}")
        print(f"    {'Metric':<24} | {'Version 1 (Static)':<18} | {'Version 2 (MRV+Deg)':<18}")
        print(f"    {'-'*24}-+-{'-'*18}-+-{'-'*18}")
        for key in ["search_nodes", "candidate_assignments", "rejected_branches", "backtracks", "max_depth"]:
            print(f"    {key:<24} | {m_v1[key]:<18} | {m_v2[key]:<18}")

if __name__ == "__main__":
    run_experiments()
