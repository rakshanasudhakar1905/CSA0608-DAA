import random
import time
def selection_sort(data):
    arr = data.copy()
    comparisons = 0
    swaps = 0
    start = time.perf_counter()
    for i in range(len(arr)):
        min_index = i
        for j in range(i + 1, len(arr)):
            comparisons += 1
            if arr[j] < arr[min_index]:
                min_index = j
        if min_index != i:
            arr[i], arr[min_index] = arr[min_index], arr[i]
            swaps += 1
    elapsed = time.perf_counter() - start
    return arr, comparisons, swaps, elapsed
def bubble_sort(data):
    arr = data.copy()
    comparisons = 0
    swaps = 0
    start = time.perf_counter()
    for i in range(len(arr)):
        swapped = False
        for j in range(len(arr) - i - 1):
            comparisons += 1
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swaps += 1
                swapped = True
        if not swapped:
            break
    elapsed = time.perf_counter() - start
    return arr, comparisons, swaps, elapsed
def insertion_sort(data):
    arr = data.copy()
    comparisons = 0
    movements = 0
    start = time.perf_counter()
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0:
            comparisons += 1
            if arr[j] > key:
                arr[j + 1] = arr[j]
                movements += 1
                j -= 1
            else:
                break
        arr[j + 1] = key
        movements += 1
    elapsed = time.perf_counter() - start
    return arr, comparisons, movements, elapsed
random.seed(42)
data_sets = {
    "Already Sorted": list(range(1, 101)),
    "Reverse Sorted": list(range(100, 0, -1)),
    "Random Data": random.sample(range(1, 1001), 100)
}
nearly_sorted = list(range(1, 101))
for _ in range(5):
    i = random.randrange(100)
    j = random.randrange(100)
    nearly_sorted[i], nearly_sorted[j] = (
        nearly_sorted[j], nearly_sorted[i]
    )
data_sets["Approximately 95% Ordered"] = nearly_sorted
algorithms = [
    ("Selection Sort", selection_sort),
    ("Bubble Sort", bubble_sort),
    ("Insertion Sort", insertion_sort)
]
for data_name, data in data_sets.items():
    print("\n" + "=" * 60)
    print("DATASET:", data_name)
    print("Input size:", len(data))
    print("=" * 60)
    for algorithm_name, algorithm in algorithms:
        result, comparisons, movements, elapsed = algorithm(data)
        print("\nAlgorithm:", algorithm_name)
        print("Comparisons:", comparisons)
        print("Swaps/Movements:", movements)
        print(f"Execution time: {elapsed:.8f} seconds")
        print("Correctly sorted:", result == sorted(data))