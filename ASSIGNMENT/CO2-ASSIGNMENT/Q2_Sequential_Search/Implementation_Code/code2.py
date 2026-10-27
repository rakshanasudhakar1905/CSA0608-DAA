import time
def sequential_search(data, target):
    comparisons = 0
    start = time.perf_counter()
    for index, value in enumerate(data):
        comparisons += 1
        if value == target:
            elapsed = time.perf_counter() - start
            return index, comparisons, elapsed
    elapsed = time.perf_counter() - start
    return -1, comparisons, elapsed
sizes = [10, 100, 1000, 10000]
for size in sizes:
    data = list(range(1, size + 1))
    test_cases = [
        ("First element", data[0]),
        ("Middle element", data[size // 2]),
        ("Last element", data[-1]),
        ("Target absent", size + 1)
    ]
    print("\n" + "=" * 50)
    print("LIST SIZE:", size)
    print("=" * 50)
    for case_name, target in test_cases:
        index, comparisons, elapsed = sequential_search(data, target)
        print("\nTest case:", case_name)
        print("Target:", target)
        if index != -1:
            print("Target found at index:", index)
        else:
            print("Target not found")
        print("Comparisons:", comparisons)
        print(f"Execution time: {elapsed:.8f} seconds")