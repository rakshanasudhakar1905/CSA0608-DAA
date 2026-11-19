"""
Task 2: Greedy vs Dynamic Programming (Fractional vs 0/1 Knapsack)
Course: CSA06 Design and Analysis of Algorithms - CO4 Assignment 4B
"""

from dataclasses import dataclass
from typing import List, Dict, Any

@dataclass
class Item:
    item_id: str
    weight: int
    value: int

    @property
    def ratio(self) -> float:
        return self.value / self.weight

def solve_fractional_knapsack_greedy(items: List[Item], capacity: int) -> Dict[str, Any]:
    ops = len(items) * max(1, len(items).bit_length())
    sorted_items = sorted(items, key=lambda x: x.ratio, reverse=True)
    rem_cap, total_value, selected, trace = capacity, 0.0, [], []

    for it in sorted_items:
        ops += 1
        if rem_cap == 0:
            trace.append(f"Skip {it.item_id}: Knapsack full.")
            continue
        if it.weight <= rem_cap:
            rem_cap -= it.weight
            total_value += it.value
            selected.append((it.item_id, 1.0, it.weight, float(it.value)))
            trace.append(f"Take 100% of {it.item_id} (W={it.weight}, V={it.value}, Ratio={it.ratio:.2f}) -> RemCap={rem_cap}")
        else:
            frac = rem_cap / it.weight
            val_taken = it.value * frac
            selected.append((it.item_id, round(frac, 4), rem_cap, round(val_taken, 2)))
            trace.append(f"Take {frac*100:.1f}% of {it.item_id} (W={rem_cap}/{it.weight}, V={val_taken:.2f}, Ratio={it.ratio:.2f}) -> RemCap=0")
            total_value += val_taken
            rem_cap = 0

    return {"total_value": round(total_value, 2), "selected": selected, "trace": trace, "ops": ops, "mem": len(items)}

def solve_01_knapsack_greedy_heuristic(items: List[Item], capacity: int) -> Dict[str, Any]:
    ops = len(items) * max(1, len(items).bit_length())
    sorted_items = sorted(items, key=lambda x: x.ratio, reverse=True)
    rem_cap, total_value, selected, trace = capacity, 0, [], []

    for it in sorted_items:
        ops += 1
        if it.weight <= rem_cap:
            rem_cap -= it.weight
            total_value += it.value
            selected.append((it.item_id, 1.0, it.weight, it.value))
            trace.append(f"COMMIT {it.item_id} (W={it.weight}, V={it.value}, Ratio={it.ratio:.2f}) -> RemCap={rem_cap}")
        else:
            trace.append(f"REJECT {it.item_id} (W={it.weight}, V={it.value}, Ratio={it.ratio:.2f}) -> Exceeds RemCap={rem_cap}")

    return {"total_value": total_value, "selected": selected, "trace": trace, "ops": ops, "mem": len(items)}

def solve_01_knapsack_dp(items: List[Item], capacity: int) -> Dict[str, Any]:
    n = len(items)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]
    ops = 0
    for i in range(1, n + 1):
        w_i, v_i = items[i - 1].weight, items[i - 1].value
        for w in range(capacity + 1):
            ops += 1
            dp[i][w] = max(dp[i - 1][w], dp[i - 1][w - w_i] + v_i) if w_i <= w else dp[i - 1][w]

    selected, w = [], capacity
    for i in range(n, 0, -1):
        ops += 1
        if dp[i][w] != dp[i - 1][w]:
            it = items[i - 1]
            selected.append((it.item_id, 1.0, it.weight, it.value))
            w -= it.weight
    selected.reverse()
    return {"total_value": dp[n][capacity], "selected": selected, "ops": ops, "mem": (n + 1) * (capacity + 1)}

if __name__ == "__main__":
    print("=== TASK 2.1: NORMAL CASE (CAPACITY = 50) ===")
    normal_items = [Item("PKG-1", 10, 60), Item("PKG-2", 20, 100), Item("PKG-3", 30, 120), Item("PKG-4", 15, 45)]
    res_frac = solve_fractional_knapsack_greedy(normal_items, 50)
    print(f"Fractional Greedy Total Value: {res_frac['total_value']}")
    for step in res_frac["trace"]:
        print("  ", step)
    print("Selected:", res_frac["selected"])

    print("\n=== TASK 2.2: ADVERSARIAL CASE BREAKING GREEDY (CAPACITY = 50) ===")
    adv_items = [Item("PKG-A", 10, 60), Item("PKG-B", 20, 100), Item("PKG-C", 30, 150)]
    g_01 = solve_01_knapsack_greedy_heuristic(adv_items, 50)
    dp_01 = solve_01_knapsack_dp(adv_items, 50)
    print(f"Greedy 0/1 Result = {g_01['total_value']} | Selected: {g_01['selected']}")
    for step in g_01["trace"]:
        print("  ", step)
    print(f"DP 0/1 Optimum    = {dp_01['total_value']} | Selected: {dp_01['selected']}")
    print(f"Suboptimality Gap = {dp_01['total_value'] - g_01['total_value']} (Greedy != DP Optimum)")

    print("\n=== TASK 2.3: ENGINEERING COMPARISON (N=20, W=500) ===")
    large_items = [Item(f"I{i}", (i % 15) + 5, ((i * 7) % 50) + 20) for i in range(1, 21)]
    g_large = solve_01_knapsack_greedy_heuristic(large_items, 500)
    dp_large = solve_01_knapsack_dp(large_items, 500)
    print(f"Greedy Heuristic -> Value: {g_large['total_value']} | Ops: {g_large['ops']} | Memory Cells: {g_large['mem']}")
    print(f"Exact DP         -> Value: {dp_large['total_value']} | Ops: {dp_large['ops']} | Memory Cells: {dp_large['mem']}")
