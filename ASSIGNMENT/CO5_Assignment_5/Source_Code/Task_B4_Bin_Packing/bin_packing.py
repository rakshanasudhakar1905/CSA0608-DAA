"""
Task B4: Bin Packing Under a Production Constraint (First-Fit Decreasing vs Exact)
Author: Rakshana V
Course: CSA06 Design and Analysis of Algorithms (CO5 Assignment 5)
"""

import time
import random

def first_fit_decreasing(workloads, capacity):
    """
    First-Fit Decreasing (FFD) Bin Packing Heuristic:
    1. Sort workloads in descending order of resource demand.
    2. Place each workload into the first active server with sufficient remaining capacity.
    3. Open a new server if no active server can accommodate the workload.
    Guarantee: FFD(I) <= (11/9) * OPT(I) + 6/9
    """
    t0 = time.perf_counter()
    # Keep track of (original_id, demand)
    indexed_workloads = sorted(enumerate(workloads, start=1), key=lambda x: x[1], reverse=True)
    servers = []  # Each entry: {"id": int, "items": list, "used": int, "remaining": int}
    comparisons = 0

    for w_id, demand in indexed_workloads:
        if demand > capacity or demand < 0:
            raise ValueError(f"Invalid workload demand {demand} for capacity {capacity}")
        placed = False
        for srv in servers:
            comparisons += 1
            if srv["remaining"] >= demand:
                srv["items"].append((w_id, demand))
                srv["used"] += demand
                srv["remaining"] -= demand
                placed = True
                break
        if not placed:
            servers.append({
                "id": len(servers) + 1,
                "items": [(w_id, demand)],
                "used": demand,
                "remaining": capacity - demand
            })

    elapsed_ms = (time.perf_counter() - t0) * 1000.0
    return servers, {"comparisons": comparisons, "time_ms": elapsed_ms}


def exact_bin_packing(workloads, capacity):
    """
    Exact Branch-and-Bound Bin Packing solver for small instances.
    """
    items = sorted(workloads, reverse=True)
    n = len(items)
    # Upper bound from FFD
    ffd_servers, _ = first_fit_decreasing(workloads, capacity)
    best_bins = len(ffd_servers)
    states = 0

    def backtrack(idx, bins):
        nonlocal best_bins, states
        states += 1
        if len(bins) >= best_bins:
            return
        if idx == n:
            best_bins = len(bins)
            return

        w = items[idx]
        seen_loads = set()
        for i in range(len(bins)):
            if bins[i] + w <= capacity and bins[i] not in seen_loads:
                seen_loads.add(bins[i])
                bins[i] += w
                backtrack(idx + 1, bins)
                bins[i] -= w

        # Open a new bin
        if len(bins) + 1 < best_bins:
            bins.append(w)
            backtrack(idx + 1, bins)
            bins.pop()

    backtrack(0, [])
    return best_bins, states


def run_b4_experiments():
    print("=" * 90)
    print("TASK B4: BIN PACKING UNDER A PRODUCTION CONSTRAINT (FIRST-FIT DECREASING)")
    print("=" * 90)

    # B4.1: Standard Cloud Workload Allocation (Capacity C = 100 vCPU units)
    capacity = 100
    workloads = [65, 45, 55, 35, 30, 25, 20, 15, 50, 40]
    servers, stats = first_fit_decreasing(workloads, capacity)

    print(f"\n--- B4.1: Production Workload Allocation (C = {capacity}, Workloads = {workloads}) ---")
    print(f"Total Servers Used: {len(servers)} | Comparisons: {stats['comparisons']} | Time: {stats['time_ms']:.4f} ms")
    for s in servers:
        items_str = ", ".join([f"W{wid}({dem})" for wid, dem in s["items"]])
        print(f"  Server {s['id']}: Assigned = [{items_str}] | Used = {s['used']}/{capacity} | Remaining = {s['remaining']}")

    # B4.2: Adversarial / Suboptimal Instance for FFD
    # Capacity C = 100. Items: {51, 28, 27, 26, 24, 22, 22} -> Sum = 200 (Exact = 2 bins: [51, 27, 22] and [28, 26, 24, 22])
    # FFD places 51+28=79 (rem 21), then 27, 26, 24 -> 99 (rem 1), then 22+22=44 -> 3 bins!
    adv_cap = 100
    adv_workloads = [51, 28, 27, 26, 24, 22, 22]
    adv_servers, _ = first_fit_decreasing(adv_workloads, adv_cap)
    opt_bins, exact_states = exact_bin_packing(adv_workloads, adv_cap)

    print(f"\n--- B4.2: Challenging Input for FFD (C = {adv_cap}, Workloads = {adv_workloads}) ---")
    print(f"Total Resource Demand = {sum(adv_workloads)} (Theoretical Lower Bound = {sum(adv_workloads)/adv_cap:.1f} servers)")
    print(f"Exact Minimum Servers : {opt_bins} (Bin 1: [51, 27, 22]=100, Bin 2: [28, 26, 24, 22]=100) | States = {exact_states}")
    print(f"FFD Servers Used      : {len(adv_servers)} (Suboptimal by +1 server due to greedy pairing of 51 + 28)")
    for s in adv_servers:
        items_str = ", ".join([f"W{wid}({dem})" for wid, dem in s["items"]])
        print(f"  Server {s['id']}: Assigned = [{items_str}] | Used = {s['used']}/{adv_cap} | Remaining = {s['remaining']}")

    # B4.3: Production-Scale Throughput Benchmark (5,000 workloads)
    random.seed(42)
    prod_workloads = [random.randint(5, 85) for _ in range(5000)]
    prod_servers, prod_stats = first_fit_decreasing(prod_workloads, 100)
    lower_bound = (sum(prod_workloads) + 99) // 100
    print(f"\n--- B4.3: Production Scale Stress Test (N = 5,000 Workloads, C = 100) ---")
    print(f"FFD Execution Time: {prod_stats['time_ms']:.2f} ms | Servers Allocated: {len(prod_servers)} | Theoretical Lower Bound: {lower_bound}")

if __name__ == "__main__":
    run_b4_experiments()
