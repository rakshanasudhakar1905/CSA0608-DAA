"""
Task B2: Engineer an Adversarial Input (Same Size n=10, m=3, Very Different Search)
Author: Rakshana V
Course: CSA06 Design and Analysis of Algorithms (CO5 Assignment 5)
"""

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Task_B1_Graph_Colouring")))
from graph_colouring import InstrumentedGraphColouring

def run_adversarial_experiment():
    n = 10
    m = 3

    # Graph A (Easy Instance): Bipartite / Tree-like hierarchical dependency structure (n=10, edges=12, m=3)
    # Chromatic number = 2 <= 3. Almost every greedy choice succeeds immediately without dead-ends.
    edges_a = [
        (0, 1), (0, 2), (1, 3), (1, 4), (2, 5), (2, 6),
        (3, 7), (4, 8), (5, 9), (6, 7), (8, 9), (0, 9)
    ]

    # Graph B (Adversarial Hard Instance): n=10, m=3
    # Vertices 0..5 form a sparsely connected 3-colourable chain/tree prefix that creates 3 * 2^5 = 96 valid partial assignments,
    # while vertices 6, 7, 8, 9 form an uncolourable K4 clique at the deepest recursion levels (depth 6..9),
    # joined sparsely to earlier vertices so static ordering explores all 96 prefix paths before hitting the K4 contradiction!
    edges_b = [
        # Sparse 3-colourable prefix (vertices 0..5)
        (0, 1), (1, 2), (2, 3), (3, 4), (4, 5),
        # Bridge edges to late clique
        (4, 6), (5, 7),
        # Uncolourable K4 clique placed at the end of static vertex order (vertices 6, 7, 8, 9)
        (6, 7), (6, 8), (6, 9), (7, 8), (7, 9), (8, 9)
    ]

    print("=" * 85)
    print(f"TASK B2: ADVERSARIAL INPUT ENGINEERING (n = {n} vertices, m = {m} server groups)")
    print("=" * 85)

    for label, edges in [("Graph A (Easy Hierarchical Instance)", edges_a),
                         ("Graph B (Adversarial Late-Clique Instance)", edges_b)]:
        print(f"\n>>> {label} | |V| = {n}, |E| = {len(edges)}, m = {m}")
        solver = InstrumentedGraphColouring(n, edges, m)

        found_v1, sol_v1 = solver.solve(heuristic="static")
        m_v1 = solver.get_metrics()

        found_v2, sol_v2 = solver.solve(heuristic="degree_mrv")
        m_v2 = solver.get_metrics()

        print(f"    Colourable: {found_v1}")
        print(f"    [Static Order]   Nodes={m_v1['search_nodes']}, Candidates={m_v1['candidate_assignments']}, "
              f"Rejected={m_v1['rejected_branches']}, Backtracks={m_v1['backtracks']}, MaxDepth={m_v1['max_depth']}")
        print(f"    [MRV+Deg Order]  Nodes={m_v2['search_nodes']}, Candidates={m_v2['candidate_assignments']}, "
              f"Rejected={m_v2['rejected_branches']}, Backtracks={m_v2['backtracks']}, MaxDepth={m_v2['max_depth']}")

if __name__ == "__main__":
    run_adversarial_experiment()
