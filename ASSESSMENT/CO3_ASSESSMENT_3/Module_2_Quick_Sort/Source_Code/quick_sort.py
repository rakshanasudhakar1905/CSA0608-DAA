def median_of_three_index(a, low, high):
    mid = (low + high) // 2
    candidates = [(a[low], low), (a[mid], mid), (a[high], high)]
    candidates.sort(key=lambda x: x[0])
    return candidates[1][1]
def partition(a, low, high, trace=False):
    pivot = a[high]
    i = low - 1
    for j in range(low, high):
        if a[j] <= pivot:
            i += 1
            a[i], a[j] = a[j], a[i]
    a[i + 1], a[high] = a[high], a[i + 1]
    p = i + 1
    if trace:
        print(f"Pivot={pivot}, partitioned={a[low:high+1]}, pivot_index={p}")
    return p
def quick_sort(a, low=0, high=None, trace=False):
    if high is None:
        high = len(a) - 1
    if low < high:
        pivot_index = median_of_three_index(a, low, high)
        a[pivot_index], a[high] = a[high], a[pivot_index]
        p = partition(a, low, high, trace)
        quick_sort(a, low, p - 1, trace)
        quick_sort(a, p + 1, high, trace)
    return a
if __name__ == "__main__":
    scores = [42, 17, 63, 8, 55, 29]
    print("Input :", scores)
    demo = scores[:]
    pivot = demo[0]
    smaller = [x for x in demo[1:] if x < pivot]
    greater = [x for x in demo[1:] if x >= pivot]
    print(f"First-pivot partition illustration: pivot={pivot}, "
          f"left={smaller}, right={greater}")
    print("Improved median-of-three Quick Sort:")
    print("Sorted:", quick_sort(scores, trace=True))
    nearly_sorted = list(range(1, 21))
    print("Nearly sorted sample:", quick_sort(nearly_sorted[:]))