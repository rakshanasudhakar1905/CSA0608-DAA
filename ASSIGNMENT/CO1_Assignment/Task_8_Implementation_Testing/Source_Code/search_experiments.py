from __future__ import annotations
import csv
import statistics
import sys
import time
from pathlib import Path
from typing import Optional

try:
    import matplotlib.pyplot as plt
except ImportError as exc:
    raise SystemExit(
        "matplotlib is required. Install with: python -m pip install matplotlib"
    ) from exc

ROOT = Path(__file__).resolve().parents[3]
OUTPUT_DIR = ROOT / "Report" / "Tables_and_Graphs"
SIZES = [1_000, 10_000, 100_000, 1_000_000]
REPEATS = 5


def linear_search(records: list[int], target: int) -> tuple[int, int]:
    """Return (index or -1, number of explicit key equality comparisons)."""
    comparisons = 0
    for i, value in enumerate(records):
        comparisons += 1
        if value == target:
            return i, comparisons
    return -1, comparisons


def recursive_binary_search(
    records: list[int], target: int, low: int = 0, high: Optional[int] = None
) -> tuple[int, int]:
    """Recursive binary search; returns (index or -1, explicit key comparisons)."""
    if high is None:
        high = len(records) - 1
    if low > high:
        return -1, 0

    mid = low + (high - low) // 2
    comparisons = 1  
    if records[mid] == target:
        return mid, comparisons

    comparisons += 1  
    if target < records[mid]:
        index, nested = recursive_binary_search(records, target, low, mid - 1)
    else:
        index, nested = recursive_binary_search(records, target, mid + 1, high)
    return index, comparisons + nested


def median_seconds(callable_, repeats: int = REPEATS) -> float:
    samples = []
    for _ in range(repeats):
        start = time.perf_counter()
        callable_()
        samples.append(time.perf_counter() - start)
    return statistics.median(samples)


def add_result(
    rows: list[dict],
    algorithm: str,
    n: int,
    case: str,
    preprocessing_seconds: float,
    search_seconds: float,
    comparisons: Optional[int],
    found: bool,
    correct: bool,
    extra_note: str = "",
) -> None:
    rows.append(
        {
            "algorithm": algorithm,
            "dataset_size": n,
            "test_case": case,
            "preprocessing_seconds": f"{preprocessing_seconds:.9f}",
            "search_seconds": f"{search_seconds:.9f}",
            "key_comparisons": "" if comparisons is None else comparisons,
            "explicit_lookup_operations": 1 if algorithm == "Hash Table" else "",
            "found": found,
            "correct": correct,
            "notes": extra_note,
        }
    )


def run() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    rows: list[dict] = []

    print(f"Python: {sys.version.split()[0]}")
    print(f"Output folder: {OUTPUT_DIR}")
    print(f"Timing repetitions per case: {REPEATS}")
    print()

    for n in SIZES:
        records = list(range(1_000_000, 1_000_000 + n))
        cases = [
            ("first", records[0], True),
            ("middle", records[n // 2], True),
            ("last", records[-1], True),
            ("absent", 9_999_999_999, False),
        ]

        linear_prep = 0.0
        for case, target, expected_found in cases:
            result, comparisons = linear_search(records, target)
            expected_index = records.index(target) if expected_found else -1
            correct = (result == expected_index) and ((result != -1) == expected_found)
            seconds = median_seconds(lambda r=records, t=target: linear_search(r, t))
            add_result(
                rows, "Linear Search", n, case, linear_prep, seconds,
                comparisons, result != -1, correct
            )

        sort_start = time.perf_counter()
        sorted_records = sorted(records, reverse=True)
        sorted_records.sort()
        binary_prep = time.perf_counter() - sort_start

        for case, target, expected_found in cases:
            result, comparisons = recursive_binary_search(sorted_records, target)
            expected_index = sorted_records.index(target) if expected_found else -1
            correct = (result == expected_index) and ((result != -1) == expected_found)
            seconds = median_seconds(
                lambda r=sorted_records, t=target: recursive_binary_search(r, t)
            )
            add_result(
                rows, "Recursive Binary Search", n, case, binary_prep,
                seconds, comparisons, result != -1, correct
            )

        hash_start = time.perf_counter()
        index = {key: key for key in records}
        hash_prep = time.perf_counter() - hash_start

        for case, target, expected_found in cases:
            result = index.get(target)
            found = target in index
            correct = (found == expected_found) and (
                (result == target) if expected_found else result is None
            )
            seconds = median_seconds(lambda h=index, t=target: h.get(t))
            add_result(
                rows, "Hash Table", n, case, hash_prep, seconds, None,
                found, correct,
                "Python dict internal equality/probe count not exposed; one get lookup timed."
            )

        print(f"Finished n={n:,}")

    csv_path = OUTPUT_DIR / "performance_results.csv"
    fieldnames = list(rows[0].keys())
    with csv_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    algorithms = ["Linear Search", "Recursive Binary Search", "Hash Table"]
    summary = {}
    for algorithm in algorithms:
        summary[algorithm] = []
        for n in SIZES:
            vals = [
                float(row["search_seconds"])
                for row in rows
                if row["algorithm"] == algorithm and row["dataset_size"] == n
            ]
            summary[algorithm].append(statistics.mean(vals))

    plt.figure(figsize=(9, 6))
    for algorithm in algorithms:
        plt.plot(SIZES, summary[algorithm], marker="o", label=algorithm)
    plt.xscale("log")
    plt.yscale("log")
    plt.xlabel("Number of student records (log scale)")
    plt.ylabel("Mean measured search time in seconds (log scale)")
    plt.title("Search Time vs Dataset Size")
    plt.grid(True, which="both", linestyle="--", alpha=0.35)
    plt.legend()
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "execution_time.png", dpi=160)
    plt.close()

    plt.figure(figsize=(9, 6))
    for algorithm in ["Linear Search", "Recursive Binary Search"]:
        means = []
        for n in SIZES:
            vals = [
                int(row["key_comparisons"])
                for row in rows
                if row["algorithm"] == algorithm
                and row["dataset_size"] == n
                and row["key_comparisons"] != ""
            ]
            means.append(statistics.mean(vals))
        plt.plot(SIZES, means, marker="o", label=algorithm)
    plt.xscale("log")
    plt.yscale("log")
    plt.xlabel("Number of student records (log scale)")
    plt.ylabel("Explicit key comparisons (log scale)")
    plt.title("Comparison Count vs Dataset Size")
    plt.grid(True, which="both", linestyle="--", alpha=0.35)
    plt.legend()
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "comparison_count.png", dpi=160)
    plt.close()

    plt.figure(figsize=(9, 6))
    for algorithm in algorithms:
        prep_values = []
        for n in SIZES:
            vals = [
                float(row["preprocessing_seconds"])
                for row in rows
                if row["algorithm"] == algorithm and row["dataset_size"] == n
            ]
            prep_values.append(max(vals) if vals else 0)
        plt.plot(SIZES, prep_values, marker="o", label=algorithm)
    plt.xscale("log")
    plt.yscale("symlog", linthresh=1e-7)
    plt.xlabel("Number of student records (log scale)")
    plt.ylabel("Preprocessing seconds (symlog scale)")
    plt.title("Preprocessing Time vs Dataset Size")
    plt.grid(True, which="both", linestyle="--", alpha=0.35)
    plt.legend()
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "preprocessing_time.png", dpi=160)
    plt.close()

    incorrect = [row for row in rows if row["correct"] is not True and row["correct"] != "True"]
    print()
    print(f"Saved: {csv_path}")
    print(f"Saved: {OUTPUT_DIR / 'execution_time.png'}")
    print(f"Saved: {OUTPUT_DIR / 'comparison_count.png'}")
    print(f"Saved: {OUTPUT_DIR / 'preprocessing_time.png'}")
    print(f"Total benchmark rows: {len(rows)}")
    print("Correctness: all tests passed." if not incorrect else f"WARNING: {len(incorrect)} incorrect rows.")

    print("\nMean search time by algorithm and dataset size (seconds):")
    for algorithm in algorithms:
        print(f"\n{algorithm}")
        for n, value in zip(SIZES, summary[algorithm]):
            print(f"  n={n:>7,}: {value:.9f}")
if __name__ == "__main__":
    run()
