def subset_sums(values):
    sums = [0]
    for value in values:
        sums += [s + value for s in sums]
    return sums
def meet_in_middle_subset_sum(numbers, target):
    mid = len(numbers) // 2
    left_sums = subset_sums(numbers[:mid])
    right_sums = sorted(subset_sums(numbers[mid:]))
    for left in left_sums:
        needed = target - left
        lo, hi = 0, len(right_sums) - 1
        while lo <= hi:
            m = (lo + hi) // 2
            if right_sums[m] == needed:
                return True, len(left_sums), len(right_sums)
            if right_sums[m] < needed:
                lo = m + 1
            else:
                hi = m - 1
    return False, len(left_sums), len(right_sums)


def brute_force_subset_sum(numbers, target):
    n = len(numbers)
    for mask in range(1 << n):
        total = 0
        for i in range(n):
            if mask & (1 << i):
                total += numbers[i]
        if total == target:
            return True
    return False


def main():
    print("Q6B: MEET-IN-THE-MIDDLE SUBSET SUM")
    numbers = [3, 7, 2, 9, 5, 12, 4, 8, 6, 10, 11, 1, 13, 14]
    target = 26
    result, left_count, right_count = meet_in_middle_subset_sum(numbers, target)
    baseline = brute_force_subset_sum(numbers, target)
    print(f"Numbers={numbers}, target={target}")
    print(f"Meet-in-the-Middle={result}, left subsets={left_count}, right subsets={right_count}")
    print(f"Brute-force={baseline}, total subsets={2 ** len(numbers)}")


if __name__ == "__main__":
    main()
