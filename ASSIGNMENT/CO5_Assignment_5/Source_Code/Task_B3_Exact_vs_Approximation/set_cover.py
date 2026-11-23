"""
Task B3: Exact vs Approximate Emergency Service Set Cover
Author: Rakshana V
Course: CSA06 Design and Analysis of Algorithms (CO5 Assignment 5)
"""

import time

class SetCoverSolver:
    def __init__(self, universe, subsets):
        self.universe = set(universe)
        self.subsets = [set(s) for s in subsets]

    def solve_exact(self):
        """
        Branch-and-bound exact algorithm that finds the minimum cardinality set cover.
        Tracks total search states explored and subset evaluations.
        """
        m = len(self.subsets)
        best_cover = None
        stats = {"search_states": 0, "pruned_branches": 0, "set_operations": 0}

        # Pre-sort subsets by descending size to find a tight upper bound quickly
        indexed_subsets = sorted(enumerate(self.subsets), key=lambda x: len(x[1]), reverse=True)

        def backtrack(idx, covered, chosen):
            nonlocal best_cover
            stats["search_states"] += 1

            if covered == self.universe:
                if best_cover is None or len(chosen) < len(best_cover):
                    best_cover = list(chosen)
                return

            # Pruning 1: Bound check (cannot improve upon best_cover)
            if best_cover is not None and len(chosen) >= len(best_cover) - 1:
                stats["pruned_branches"] += 1
                return

            # Pruning 2: No more subsets left
            if idx == m:
                return

            # Pruning 3: Even taking all remaining subsets cannot cover the universe
            remaining_union = set()
            for j in range(idx, m):
                remaining_union |= indexed_subsets[j][1]
                stats["set_operations"] += 1
            if not self.universe.issubset(covered | remaining_union):
                stats["pruned_branches"] += 1
                return

            orig_idx, sub = indexed_subsets[idx]
            new_covered = covered | sub
            stats["set_operations"] += 1

            # Branch 1: Include subset if it adds at least one new uncovered zone
            if len(new_covered) > len(covered):
                chosen.append(orig_idx)
                backtrack(idx + 1, new_covered, chosen)
                chosen.pop()

            # Branch 2: Exclude subset
            backtrack(idx + 1, covered, chosen)

        t0 = time.perf_counter()
        backtrack(0, set(), [])
        elapsed_ms = (time.perf_counter() - t0) * 1000.0
        stats["time_ms"] = elapsed_ms
        return sorted(best_cover) if best_cover is not None else None, stats

    def solve_greedy(self):
        """
        Greedy Set Cover approximation algorithm (O(ln n) approximation ratio).
        Repeatedly selects the centre covering the maximum number of uncovered zones.
        """
        uncovered = set(self.universe)
        selected = []
        used = [False] * len(self.subsets)
        stats = {"iterations": 0, "candidate_evaluations": 0, "set_operations": 0}

        t0 = time.perf_counter()
        while uncovered:
            stats["iterations"] += 1
            best_idx = -1
            best_gain = 0

            for i, sub in enumerate(self.subsets):
                if used[i]:
                    continue
                stats["candidate_evaluations"] += 1
                stats["set_operations"] += 1
                gain = len(sub & uncovered)
                if gain > best_gain:
                    best_gain = gain
                    best_idx = i

            if best_idx == -1 or best_gain == 0:
                return None, stats  # Infeasible

            used[best_idx] = True
            selected.append(best_idx)
            uncovered -= self.subsets[best_idx]
            stats["set_operations"] += 1

        elapsed_ms = (time.perf_counter() - t0) * 1000.0
        stats["time_ms"] = elapsed_ms
        return sorted(selected), stats


def run_b3_experiments():
    print("=" * 90)
    print("TASK B3: EXACT vs GREEDY EMERGENCY SERVICE SET COVER")
    print("=" * 90)

    # B3.1: Three Small Instances
    small_instances = [
        (
            "Instance 1 (6 Zones, 4 Centres - Exact == Greedy)",
            {"Z1", "Z2", "Z3", "Z4", "Z5", "Z6"},
            [
                {"Z1", "Z2", "Z3"},       # C0
                {"Z4", "Z5", "Z6"},       # C1
                {"Z1", "Z4"},             # C2
                {"Z2", "Z5"}              # C3
            ]
        ),
        (
            "Instance 2 (8 Zones, 5 Centres - Overlapping Districts, Exact == Greedy)",
            {f"Z{i}" for i in range(1, 9)},
            [
                {"Z1", "Z2", "Z3", "Z4"}, # C0
                {"Z3", "Z4", "Z5", "Z6"}, # C1
                {"Z5", "Z6", "Z7", "Z8"}, # C2
                {"Z1", "Z7"},             # C3
                {"Z2", "Z8"}              # C4
            ]
        ),
        (
            "Instance 3 (6 Zones, 3 Centres - Suboptimal Greedy Trap)",
            {"Z1", "Z2", "Z3", "Z4", "Z5", "Z6"},
            [
                {"Z1", "Z2", "Z3", "Z4"}, # C0 (covers 4, lures greedy)
                {"Z1", "Z2", "Z5"},       # C1 (part of optimal pair)
                {"Z3", "Z4", "Z6"}        # C2 (part of optimal pair)
            ]
        )
    ]

    print("\n--- B3.1: Correctness on Small Instances ---")
    for name, u, subs in small_instances:
        solver = SetCoverSolver(u, subs)
        exact_sol, _ = solver.solve_exact()
        greedy_sol, _ = solver.solve_greedy()
        print(f"{name}:")
        print(f"   Exact Size = {len(exact_sol)} {exact_sol} | Greedy Size = {len(greedy_sol)} {greedy_sol} | Same? {len(exact_sol) == len(greedy_sol)}")

    # B3.2: Dedicated Counterexample (14 Zones, 6 Centres; Optimal = 2, Greedy = 4)
    print("\n--- B3.2: Counterexample Construction (Optimal = 2, Greedy = 4) ---")
    u_ce = {f"Z{i}" for i in range(1, 15)}
    subs_ce = [
        {f"Z{i}" for i in range(1, 8)},       # C0: {Z1..Z7} (7 zones - Optimal 1)
        {f"Z{i}" for i in range(8, 15)},      # C1: {Z8..Z14} (7 zones - Optimal 2)
        {"Z1", "Z2", "Z3", "Z4", "Z8", "Z9", "Z10", "Z11"}, # C2: 8 zones (Greedy picks 1st!)
        {"Z5", "Z6", "Z12", "Z13"},           # C3: 4 remaining zones (Greedy picks 2nd!)
        {"Z7"},                               # C4: 1 remaining zone (Greedy picks 3rd!)
        {"Z14"}                               # C5: 1 remaining zone (Greedy picks 4th!)
    ]
    ce_solver = SetCoverSolver(u_ce, subs_ce)
    ex_ce, _ = ce_solver.solve_exact()
    gr_ce, _ = ce_solver.solve_greedy()
    print(f"Counterexample Universe: |U| = {len(u_ce)}, Candidate Centres = {len(subs_ce)}")
    print(f"Exact Optimal Cover : Size = {len(ex_ce)} -> Centres {ex_ce}")
    print(f"Greedy Approx Cover : Size = {len(gr_ce)} -> Centres {gr_ce} (GreedyCoverSize > OptimalCoverSize: {len(gr_ce)} > {len(ex_ce)})")

    # B3.3: Scalability Experiment across increasing problem sizes
    print("\n--- B3.3: Scalability Analysis (Increasing Zones & Candidate Centres) ---")
    scales = [
        (10, 8),
        (16, 12),
        (22, 16),
        (28, 20),
        (34, 24)
    ]
    print(f"{'Size (|U|, |S|)':<16} | {'Exact States':<14} | {'Exact Ops':<12} | {'Greedy Evals':<14} | {'Exact Cov':<10} | {'Greedy Cov':<10}")
    print("-" * 88)
    for num_z, num_c in scales:
        u_sc = {f"Z{i}" for i in range(1, num_z + 1)}
        subs_sc = []
        # Deterministic structured coverage generator
        block_size = max(2, num_z // 4)
        for c in range(num_c):
            start = (c * 3) % num_z
            s = {f"Z{((start + offset) % num_z) + 1}" for offset in range(block_size + (c % 3))}
            subs_sc.append(s)
        sc_solver = SetCoverSolver(u_sc, subs_sc)
        ex_s, ex_st = sc_solver.solve_exact()
        gr_s, gr_st = sc_solver.solve_greedy()
        print(f"({num_z:>2}, {num_c:>2})         | {ex_st['search_states']:<14} | {ex_st['set_operations']:<12} | "
              f"{gr_st['candidate_evaluations']:<14} | {len(ex_s):<10} | {len(gr_s):<10}")

if __name__ == "__main__":
    run_b3_experiments()
