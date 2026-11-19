
import random
import time
import csv
import os
import statistics
import matplotlib.pyplot as plt

from linear_search import linear_search
import binary_search
from hash_search import build_hash_table, hash_search

SIZES = [1000, 10000, 100000, 1000000]
REPEATS = 5

os.makedirs("results", exist_ok=True)

results = []

for n in SIZES:

    print("\nTesting dataset:", n)
    records = [
        {"reg_no": i, "name": f"Student{i}"}
        for i in range(1, n + 1)
    ]

    random.shuffle(records)

    target = n // 2

    linear_times = []
    linear_counts = []

    for _ in range(REPEATS):
        start = time.perf_counter()

        result, count = linear_search(records, target)

        elapsed = time.perf_counter() - start

        assert result is not None
        assert result["reg_no"] == target

        linear_times.append(elapsed)
        linear_counts.append(count)

    linear_time = statistics.median(linear_times)

    start = time.perf_counter()

    sorted_records = sorted(
        records, key=lambda x: x["reg_no"]
    )

    sort_time = time.perf_counter() - start

    binary_times = []
    binary_counts = []

    for _ in range(REPEATS):

        binary_search.comparisons = 0

        start = time.perf_counter()

        result = binary_search.recursive_binary_search(
            sorted_records,
            0,
            len(sorted_records) - 1,
            target
        )

        elapsed = time.perf_counter() - start

        assert result is not None
        assert result["reg_no"] == target

        binary_times.append(elapsed)
        binary_counts.append(binary_search.comparisons)

    binary_time = statistics.median(binary_times)

    start = time.perf_counter()

    hash_table = build_hash_table(records)

    build_time = time.perf_counter() - start

    hash_times = []

    for _ in range(REPEATS):

        start = time.perf_counter()

        result = hash_search(hash_table, target)

        elapsed = time.perf_counter() - start

        assert result is not None
        assert result["reg_no"] == target

        hash_times.append(elapsed)

    hash_time = statistics.median(hash_times)

    row = {
        "Records": n,
        "Linear_Search_Time": linear_time,
        "Linear_Comparisons": statistics.median(linear_counts),
        "Binary_Sort_Time": sort_time,
        "Binary_Search_Time": binary_time,
        "Binary_Comparisons": statistics.median(binary_counts),
        "Hash_Build_Time": build_time,
        "Hash_Search_Time": hash_time
    }

    results.append(row)

    print("Linear Search:", linear_time)
    print("Linear Comparisons:", row["Linear_Comparisons"])

    print("Binary Sorting:", sort_time)
    print("Binary Search:", binary_time)
    print("Binary Comparisons:", row["Binary_Comparisons"])

    print("Hash Construction:", build_time)
    print("Hash Search:", hash_time)

with open(
    "results/performance_results.csv",
    "w",
    newline=""
) as file:

    writer = csv.DictWriter(
        file,
        fieldnames=results[0].keys()
    )

    writer.writeheader()
    writer.writerows(results)


sizes = [r["Records"] for r in results]

plt.figure(figsize=(9, 5))

plt.plot(
    sizes,
    [r["Linear_Search_Time"] for r in results],
    marker="o",
    label="Linear Search"
)

plt.plot(
    sizes,
    [r["Binary_Search_Time"] for r in results],
    marker="o",
    label="Binary Search"
)

plt.plot(
    sizes,
    [r["Hash_Search_Time"] for r in results],
    marker="o",
    label="Hash Search"
)

plt.xscale("log")
plt.yscale("log")
plt.xlabel("Number of Records")
plt.ylabel("Search Time (Seconds)")
plt.title("Searching Algorithm Performance")
plt.legend()
plt.grid(True)

plt.savefig("results/search_time.png")
plt.show()


plt.figure(figsize=(9, 5))

plt.plot(
    sizes,
    [r["Linear_Comparisons"] for r in results],
    marker="o",
    label="Linear Search"
)

plt.plot(
    sizes,
    [r["Binary_Comparisons"] for r in results],
    marker="o",
    label="Binary Search"
)

plt.xscale("log")
plt.yscale("log")
plt.xlabel("Number of Records")
plt.ylabel("Number of Comparisons")
plt.title("Comparison Count Analysis")
plt.legend()
plt.grid(True)

plt.savefig("results/comparison_count.png")
plt.show()

print("\nAll experiments completed successfully.")
print("CSV and graphs saved inside results folder.")
