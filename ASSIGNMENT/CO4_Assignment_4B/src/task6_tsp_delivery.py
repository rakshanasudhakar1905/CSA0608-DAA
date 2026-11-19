"""
Task 6: Last-Mile Delivery Route Optimisation (Held-Karp Bitmask DP for TSP)
Course: CSA06 Design and Analysis of Algorithms - CO4 Assignment 4B
"""

import time, itertools, tracemalloc
from typing import List, Tuple, Dict, Any

INF = float('inf')

def solve_tsp_dp(dist_matrix: List[List[int]], names: List[str]) -> Dict[str, Any]:
    n = len(dist_matrix)
    num_deliveries = n - 1
    num_subsets = 1 << num_deliveries
    dp = [[INF] * n for _ in range(num_subsets)]
    parent = [[-1] * n for _ in range(num_subsets)]
    states_evaluated = 0

    for j in range(1, n):
        mask = 1 << (j - 1)
        dp[mask][j] = dist_matrix[0][j]
        parent[mask][j] = 0
        states_evaluated += 1

    for mask in range(1, num_subsets):
        for j in range(1, n):
            if not (mask & (1 << (j - 1))):
                continue
            prev_mask = mask ^ (1 << (j - 1))
            if prev_mask == 0:
                continue
            for k in range(1, n):
                if prev_mask & (1 << (k - 1)):
                    states_evaluated += 1
                    new_cost = dp[prev_mask][k] + dist_matrix[k][j]
                    if new_cost < dp[mask][j]:
                        dp[mask][j] = new_cost
                        parent[mask][j] = k

    full_mask = num_subsets - 1
    min_tour_cost, last_node = INF, -1
    for j in range(1, n):
        states_evaluated += 1
        total = dp[full_mask][j] + dist_matrix[j][0]
        if total < min_tour_cost:
            min_tour_cost = total
            last_node = j

    rev_path, curr_mask, curr_node = [], full_mask, last_node
    while curr_node != 0 and curr_node != -1:
        rev_path.append(curr_node)
        prev_node = parent[curr_mask][curr_node]
        curr_mask ^= (1 << (curr_node - 1))
        curr_node = prev_node
    route_names = [names[0]] + [names[i] for i in reversed(rev_path)] + [names[0]]
    return {"min_cost": min_tour_cost, "route": route_names, "states_evaluated": states_evaluated, "dp_table_entries": num_subsets * n}

def solve_tsp_brute_force(dist_matrix: List[List[int]], names: List[str]) -> Tuple[int, List[str]]:
    n = len(dist_matrix)
    best_cost, best_perm = INF, None
    for perm in itertools.permutations(range(1, n)):
        cost = dist_matrix[0][perm[0]] + sum(dist_matrix[perm[i]][perm[i + 1]] for i in range(len(perm) - 1)) + dist_matrix[perm[-1]][0]
        if cost < best_cost:
            best_cost, best_perm = cost, perm
    return best_cost, [names[0]] + [names[i] for i in best_perm] + [names[0]]

if __name__ == "__main__":
    locations = ["Hub", "A", "B", "C", "D", "E", "F"]
    cost_matrix_6 = [
        [0,  12, 10, 19, 8,  15, 22],
        [12, 0,  9,  11, 14, 7,  16],
        [10, 9,  0,  8,  13, 18, 12],
        [19, 11, 8,  0,  10, 14, 9],
        [8,  14, 13, 10, 0,  11, 15],
        [15, 7,  18, 14, 11, 0,  6],
        [22, 16, 12, 9,  15, 6,  0]
    ]

    print("=== TASK 6.3: LAST-MILE DELIVERY ROUTE (HUB + 6 LOCATIONS) ===")
    res6 = solve_tsp_dp(cost_matrix_6, locations)
    print("Optimal Route:", " -> ".join(res6["route"]))
    print(f"Minimum Travel Cost = {res6['min_cost']} | States Evaluated = {res6['states_evaluated']}")

    print("\n=== TASK 6.4: INDEPENDENT VALIDATION (HUB + 4 LOCATIONS) ===")
    loc4, mat4 = locations[:5], [row[:5] for row in cost_matrix_6[:5]]
    dp4 = solve_tsp_dp(mat4, loc4)
    bf_cost, bf_route = solve_tsp_brute_force(mat4, loc4)
    print(f"Exhaustive Enumeration (4! = 24): Cost = {bf_cost} | Route = {' -> '.join(bf_route)}")
    print(f"Held-Karp Bitmask DP Result     : Cost = {dp4['min_cost']} | Route = {' -> '.join(dp4['route'])}")
    assert dp4["min_cost"] == bf_cost
    print("Validation Status: EXACT MATCH CONFIRMED.")

    print("\n=== TASK 6.5: STATE-SPACE GROWTH SCALING EXPERIMENT (n = 4 to 14) ===")
    print(f"{'Deliveries (n)':<15} | {'Subsets (2^n)':<14} | {'States Eval':<14} | {'Time (ms)':<12} | {'Peak Mem (KB)'}")
    print("-" * 76)
    for n_del in range(4, 15):
        size = n_del + 1
        synth_names = ["Hub"] + [f"L{i}" for i in range(1, size)]
        synth_mat = [[0 if i == j else ((i * 7 + j * 13) % 25) + 5 for j in range(size)] for i in range(size)]
        tracemalloc.start()
        t0 = time.perf_counter()
        r = solve_tsp_dp(synth_mat, synth_names)
        dt_ms = (time.perf_counter() - t0) * 1000
        _, peak_mem = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        print(f"{n_del:<15} | {1<<n_del:<14} | {r['states_evaluated']:<14} | {dt_ms:<12.3f} | {peak_mem/1024:.2f}")
