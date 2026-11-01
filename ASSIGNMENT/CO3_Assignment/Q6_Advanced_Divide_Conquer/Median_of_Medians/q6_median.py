def insertion_sort(a):
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        while j >= 0 and a[j] > key:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = key
    return a
def median_of_medians(a):
    if len(a) <= 5:
        s = insertion_sort(a[:])
        return s[len(s) // 2]
    medians = []
    for i in range(0, len(a), 5):
        group = insertion_sort(a[i:i + 5])
        medians.append(group[len(group) // 2])
    return median_of_medians(medians)
def select_mom(a, k, stats):
    """One-based k-th smallest element."""
    stats["partitions"] += 1
    if len(a) <= 5:
        return sorted(a)[k - 1]
    pivot = median_of_medians(a)
    lows = [x for x in a if x < pivot]
    equals = [x for x in a if x == pivot]
    highs = [x for x in a if x > pivot]
    if k <= len(lows):
        return select_mom(lows, k, stats)
    if k <= len(lows) + len(equals):
        return pivot
    return select_mom(highs, k - len(lows) - len(equals), stats)
def quickselect(a, k, pivot_mode="last", stats=None):
    if stats is None:
        stats = {"partitions": 0}
    stats["partitions"] += 1
    if len(a) <= 1:
        return a[0]
    pivot = a[-1] if pivot_mode == "last" else a[len(a)//2]
    lows = [x for x in a if x < pivot]
    equals = [x for x in a if x == pivot]
    highs = [x for x in a if x > pivot]
    if k <= len(lows):
        return quickselect(lows, k, pivot_mode, stats)
    if k <= len(lows) + len(equals):
        return pivot
    return quickselect(highs, k-len(lows)-len(equals), pivot_mode, stats)
def main():
    print("Q6A: MEDIAN OF MEDIANS AND QUICKSELECT")
    data = list(range(1, 101))
    k = 50
    s = {"partitions": 0}
    result = select_mom(data, k, s)
    print(f"Median of Medians: k={k}, result={result}, partitions={s['partitions']}")
    for mode in ("last", "middle"):
        q = {"partitions": 0}
        value = quickselect(data, k, mode, q)
        print(f"QuickSelect pivot={mode}: result={value}, partitions={q['partitions']}")
if __name__ == "__main__":
    main()
