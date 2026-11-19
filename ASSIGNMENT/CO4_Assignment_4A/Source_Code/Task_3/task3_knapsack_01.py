"""
Task 3: 0/1 Knapsack with Solution Reconstruction
Course: CSA06 Design and Analysis of Algorithms (CO4 - Assignment 4A)
"""

def knapsack_01(items, capacity):
    """
    Solves 0/1 Knapsack using bottom-up Dynamic Programming and reconstructs selected items.
    items: list of tuples (item_id, weight, value)
    capacity: integer vehicle capacity
    """
    n = len(items)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]

    # Build DP table
    for i in range(1, n + 1):
        item_id, w_i, v_i = items[i - 1]
        for w in range(capacity + 1):
            if w_i <= w:
                dp[i][w] = max(dp[i - 1][w], v_i + dp[i - 1][w - w_i])
            else:
                dp[i][w] = dp[i - 1][w]

    # Reconstruct selected items
    selected_items = []
    w_rem = capacity
    for i in range(n, 0, -1):
        if dp[i][w_rem] != dp[i - 1][w_rem]:
            item_id, w_i, v_i = items[i - 1]
            selected_items.append((item_id, w_i, v_i))
            w_rem -= w_i

    selected_items.reverse()
    return dp[n][capacity], selected_items, dp


if __name__ == "__main__":
    # Desk-Check Dataset from Assignment
    cargo_items = [
        ("P", 2, 12),
        ("Q", 3, 20),
        ("R", 4, 25),
        ("S", 5, 30)
    ]
    cap = 7
    opt_val, chosen, table = knapsack_01(cargo_items, cap)

    print("=== Test Case 1: Assignment Dataset (Capacity = 7) ===")
    header = "Item\Cap | " + " ".join(f"{w:>3}" for w in range(cap + 1))
    print(header)
    print("-" * len(header))
    labels = ["0 (None)"] + [f"{it[0]}({it[1]},{it[2]})" for it in cargo_items]
    for idx, row in enumerate(table):
        print(f"{labels[idx]:<9}| " + " ".join(f"{val:>3}" for val in row))

    print(f"\nOptimal Total Value: {opt_val}")
    print(f"Selected Items: {chosen}")

    # Test Case 2: Edge Case - All items heavier than capacity
    opt_val2, chosen2, _ = knapsack_01(cargo_items, 1)
    print("\n=== Test Case 2: Capacity Smaller Than All Items (Capacity = 1) ===")
    print(f"Optimal Total Value: {opt_val2}, Selected Items: {chosen2}")
