def merge_sort(a, counter):
    if len(a) <= 1:
        return a
    mid = len(a) // 2
    left = merge_sort(a[:mid], counter)
    right = merge_sort(a[mid:], counter)
    merged = []
    i = j = 0
    while i < len(left) and j < len(right):
        counter[0] += 1
        if left[i] <= right[j]:
            merged.append(left[i]); i += 1
        else:
            merged.append(right[j]); j += 1
    return merged + left[i:] + right[j:]
def quick_sort(a, pivot_strategy="first"):
    stats = {"comparisons": 0, "max_depth": 0, "partitions": []}
    def sort(values, depth):
        stats["max_depth"] = max(stats["max_depth"], depth)
        if len(values) <= 1:
            return values
        pivot = values[0] if pivot_strategy == "first" else values[len(values)//2]
        left, equal, right = [], [], []
        for x in values:
            stats["comparisons"] += 1
            if x < pivot:
                left.append(x)
            elif x > pivot:
                right.append(x)
            else:
                equal.append(x)
        stats["partitions"].append((len(left), len(equal), len(right)))
        return sort(left, depth + 1) + equal + sort(right, depth + 1)
    return sort(a, 1), stats
def main():
    print("Q2: MERGE SORT AND QUICK SORT")
    for label, data in [
        ("random-like", [23, 5, 17, 9, 31, 2, 14, 8, 27, 11]),
        ("sorted", list(range(1, 16))),
        ("reverse", list(range(15, 0, -1))),
    ]:
        mc = [0]
        ms = merge_sort(data, mc)
        print(f"\n{label}: MergeSort comparisons={mc[0]}, result={ms}")
        for pivot in ("first", "middle"):
            qs, st = quick_sort(data, pivot)
            print(f"QuickSort pivot={pivot}: comparisons={st['comparisons']}, "
                  f"max_depth={st['max_depth']}, first_partitions={st['partitions'][:5]}, "
                  f"result={qs}")
if __name__ == "__main__":
    main()
