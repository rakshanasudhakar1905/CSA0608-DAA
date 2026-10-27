import time
def exhaustive_knapsack(weights, values, capacity):
    n = len(weights)
    best_value = 0
    best_subset = []
    subsets_examined = 0
    feasible_subsets = 0
    start_time = time.perf_counter()
    for mask in range(1 << n):
        subsets_examined += 1
        total_weight = 0
        total_value = 0
        selected_items = []
        for i in range(n):
            if mask & (1 << i):
                total_weight += weights[i]
                total_value += values[i]
                selected_items.append(i + 1)
        if total_weight <= capacity:
            feasible_subsets += 1
            if total_value > best_value:
                best_value = total_value
                best_subset = selected_items

    elapsed_time = time.perf_counter() - start_time
    return (
        best_subset,
        best_value,
        subsets_examined,
        feasible_subsets,
        elapsed_time
    )
def main():
    datasets = [
        {
            "name": "Small dataset",
            "weights": [2, 3, 4, 5],
            "values": [3, 4, 5, 6],
            "capacity": 8
        },
        {
            "name": "Medium dataset",
            "weights": [2, 3, 4, 5, 6, 7, 8, 9],
            "values": [3, 5, 6, 8, 9, 10, 12, 13],
            "capacity": 20
        },
        {
            "name": "Larger dataset",
            "weights": list(range(1, 16)),
            "values": [2 * i + 1 for i in range(1, 16)],
            "capacity": 40
        }
    ]
    for data in datasets:
        result = exhaustive_knapsack(
            data["weights"],
            data["values"],
            data["capacity"]
        )
        best_subset, best_value, examined, feasible, elapsed = result
        total_weight = sum(
            data["weights"][i - 1] for i in best_subset
        )
        print("\nDataset:", data["name"])
        print("Number of items:", len(data["weights"]))
        print("Weights:", data["weights"])
        print("Values:", data["values"])
        print("Capacity:", data["capacity"])
        print("Selected item numbers:", best_subset)
        print("Total weight:", total_weight)
        print("Maximum value:", best_value)
        print("Subsets examined:", examined)
        print("Expected subsets:", 2 ** len(data["weights"]))
        print("Feasible subsets:", feasible)
        print("Execution time:", format(elapsed, ".8f"), "seconds")
if __name__ == "__main__":
    main()