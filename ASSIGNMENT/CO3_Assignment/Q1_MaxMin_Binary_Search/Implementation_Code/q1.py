def max_min_dc(a, counter):
    if len(a) == 1:
        return a[0], a[0]
    if len(a) == 2:
        counter[0] += 1
        return (a[0], a[1]) if a[0] < a[1] else (a[1], a[0])
    mid = len(a) // 2
    mn1, mx1 = max_min_dc(a[:mid], counter)
    mn2, mx2 = max_min_dc(a[mid:], counter)
    counter[0] += 2
    return min(mn1, mn2), max(mx1, mx2)
def independent_max_min(a, counter):
    mn = mx = a[0]
    for x in a[1:]:
        counter[0] += 1
        if x < mn:
            mn = x
    for x in a[1:]:
        counter[0] += 1
        if x > mx:
            mx = x
    return mn, mx
def binary_search(a, target):
    low, high, comparisons = 0, len(a) - 1, 0
    while low <= high:
        mid = (low + high) // 2
        comparisons += 1
        if a[mid] == target:
            return mid, comparisons
        comparisons += 1
        if target < a[mid]:
            high = mid - 1
        else:
            low = mid + 1
    return -1, comparisons
def main():
    print("Q1: MAXIMUM, MINIMUM AND BINARY SEARCH")
    for n in (10, 100, 1000, 10000):
        data = list(range(n, 0, -1))
        c1 = [0]; c2 = [0]
        r1 = max_min_dc(data, c1)
        r2 = independent_max_min(data, c2)
        print(f"n={n:5} D&C={r1}, comparisons={c1[0]}, "
              f"independent={r2}, comparisons={c2[0]}")
    a = list(range(0, 100, 2))
    for target in (42, 43):
        idx, count = binary_search(a, target)
        print(f"Binary search target={target}: index={idx}, comparisons={count}")
if __name__ == "__main__":
    main()