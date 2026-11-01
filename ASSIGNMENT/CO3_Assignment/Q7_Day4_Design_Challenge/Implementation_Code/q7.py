def brute_force_inversions(a):
    count = 0
    for i in range(len(a)):
        for j in range(i + 1, len(a)):
            if a[i] > a[j]:
                count += 1
    return count


def count_inversions_dc(a):
    """Returns (sorted array, inversion count, merge comparisons)."""
    comparisons = [0]

    def sort_count(values):
        if len(values) <= 1:
            return values, 0
        mid = len(values) // 2
        left, left_count = sort_count(values[:mid])
        right, right_count = sort_count(values[mid:])
        merged = []
        i = j = cross = 0
        while i < len(left) and j < len(right):
            comparisons[0] += 1
            if left[i] <= right[j]:
                merged.append(left[i]); i += 1
            else:
                merged.append(right[j])
                cross += len(left) - i
                j += 1
        merged.extend(left[i:])
        merged.extend(right[j:])
        return merged, left_count + right_count + cross

    sorted_a, count = sort_count(a)
    return sorted_a, count, comparisons[0]


def main():
    print("Q7: COUNTING INVERSIONS USING DIVIDE AND CONQUER")
    tests = [
        [2, 4, 1, 3, 5],
        [5, 4, 3, 2, 1],
        [1, 2, 3, 4, 5],
        [8, 3, 5, 1, 7, 2, 6, 4],
    ]
    for data in tests:
        baseline = brute_force_inversions(data)
        sorted_data, dc_count, comparisons = count_inversions_dc(data)
        print(f"Input={data}")
        print(f"Sorted={sorted_data}, brute_force={baseline}, D&C={dc_count}, "
              f"merge_comparisons={comparisons}, correct={baseline == dc_count}\n")


if __name__ == "__main__":
    main()
