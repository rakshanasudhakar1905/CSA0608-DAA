import time
def exhaustive_knapsack(weights, values, capacity):
    n = len(weights)
    best_value = 0
    best_items = []
    subsets_checked = 0
    start = time.perf_counter()
    for mask in range(1 << n):
        subsets_checked += 1
        total_weight = 0
        total_value = 0
        selected = []
        for i in range(n):
            if mask & (1 << i):
                total_weight += weights[i]
                total_value += values[i]
                selected.append(i + 1)
        if total_weight <= capacity and total_value > best_value:
            best_value = total_value
            best_items = selected
    elapsed = time.perf_counter() - start
    return best_value, best_items, subsets_checked, elapsed
def dynamic_programming_knapsack(weights, values, capacity):
    n = len(weights)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]
    states_processed = 0
    start = time.perf_counter()
    for i in range(1, n + 1):
        weight = weights[i - 1]
        value = values[i - 1]
        for w in range(capacity + 1):
            states_processed += 1
            dp[i][w] = dp[i - 1][w]
            if weight <= w:
                dp[i][w] = max(
                    dp[i][w],
                    value + dp[i - 1][w - weight]
                )
    best_value = dp[n][capacity]
    selected_items = []
    remaining_capacity = capacity
    for i in range(n, 0, -1):
        if dp[i][remaining_capacity] != dp[i - 1][remaining_capacity]:
            selected_items.append(i)
            remaining_capacity -= weights[i - 1]
    selected_items.reverse()
    elapsed = time.perf_counter() - start
    return best_value, selected_items, states_processed, elapsed
def main():
    datasets = [
        {
            "name": "Small dataset",
            "weights": [2, 3, 4, 5, 6],
            "values": [3, 4, 5, 8, 9],
            "capacity": 10
        },
        {
            "name": "Medium dataset",
            "weights": [2, 5, 3, 7, 4, 6, 8, 3, 5, 4],
            "values": [6, 10, 7, 14, 8, 12, 15, 6, 11, 9],
            "capacity": 20
        },
        {
            "name": "Larger dataset",
            "weights": [2, 5, 3, 7, 4, 6, 8, 3, 5, 4,
                        9, 2, 6, 7, 3, 8, 4, 5],
            "values": [6, 10, 7, 14, 8, 12, 15, 6, 11, 9,
                       17, 5, 13, 14, 7, 16, 8, 10],
            "capacity": 35
        }
    ]
    for data in datasets:
        weights = data["weights"]
        values = data["values"]
        capacity = data["capacity"]
        brute = exhaustive_knapsack(weights, values, capacity)
        dynamic = dynamic_programming_knapsack(
            weights, values, capacity
        )
        brute_value, brute_items, subsets, brute_time = brute
        dp_value, dp_items, states, dp_time = dynamic
        print("\n" + "=" * 48)
        print("Dataset:", data["name"])
        print("Number of items:", len(weights))
        print("Capacity:", capacity)
        print("\nEXHAUSTIVE SEARCH")
        print("Maximum value:", brute_value)
        print("Selected items:", brute_items)
        print("Subsets examined:", subsets)
        print("Execution time:", format(brute_time, ".8f"), "seconds")
        print("\nDYNAMIC PROGRAMMING")
        print("Maximum value:", dp_value)
        print("Selected items:", dp_items)
        print("DP states processed:", states)
        print("Execution time:", format(dp_time, ".8f"), "seconds")
        print("\nCOMPARISON")
        print("Same optimal value:", brute_value == dp_value)
        print("Subsets vs DP states:", subsets, "vs", states)
        if brute_time > 0 and dp_time > 0:
            print(
                "Measured speedup:",
                format(brute_time / dp_time, ".2f"),
                "times"
            )
        if brute_value != dp_value:
            print("WARNING: Results do not match!")
if __name__ == "__main__":
    main()