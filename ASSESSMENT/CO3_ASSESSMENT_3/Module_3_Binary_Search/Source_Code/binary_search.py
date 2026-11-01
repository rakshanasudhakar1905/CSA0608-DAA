def first_timestamp_index(orders, target, trace=True):
    low, high = 0, len(orders) - 1
    answer = -1
    comparisons = 0
    while low <= high:
        mid = (low + high) // 2
        comparisons += 1
        if trace:
            print(f"low={low}, high={high}, mid={mid}, "
                  f"timestamp={orders[mid][0]}")
        if orders[mid][0] >= target:
            if orders[mid][0] == target:
                answer = mid
            high = mid - 1
        else:
            low = mid + 1
    if trace:
        print("Timestamp comparisons:", comparisons)
    return answer
if __name__ == "__main__":
    orders = [(101, "O4"), (102, "O2"), (102, "O5"),
              (103, "O6"), (105, "O1"), (105, "O3")]
    target = 102
    index = first_timestamp_index(orders, target)
    if index == -1:
        print(f"No order found at timestamp {target}")
    else:
        print(f"First order at timestamp {target}: {orders[index]}")
        i = index
        matches = []
        while i < len(orders) and orders[i][0] == target:
            matches.append(orders[i])
            i += 1
        print("All matching orders:", matches)