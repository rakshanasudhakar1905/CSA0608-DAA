import time
def brute_force_search(text, pattern):
    comparisons = 0
    positions = []
    start = time.perf_counter()
    if pattern == "":
        return positions, comparisons, time.perf_counter() - start
    n = len(text)
    m = len(pattern)
    for i in range(n - m + 1):
        j = 0
        while j < m:
            comparisons += 1
            if text[i + j] != pattern[j]:
                break
            j += 1
        if j == m:
            positions.append(i)
    elapsed = time.perf_counter() - start
    return positions, comparisons, elapsed
test_cases = [
    (
        "Early Match",
        "ALGORITHM DESIGN AND ANALYSIS",
        "ALGO"
    ),
    (
        "Match Near the End",
        "A" * 1000 + "XYZ",
        "XYZ"
    ),
    (
        "Repeated Prefix Challenge",
        "A" * 1000 + "B",
        "A" * 20 + "C"
    ),
    (
        "Pattern Not Found",
        "COMPUTER SCIENCE",
        "PYTHON"
    )
]
for name, text, pattern in test_cases:
    positions, comparisons, elapsed = brute_force_search(text, pattern)
    print("\n" + "=" * 55)
    print("TEST CASE:", name)
    print("=" * 55)
    print("Text length:", len(text))
    print("Pattern:", pattern)
    print("Pattern length:", len(pattern))
    print("Match positions:", positions)
    print("Character comparisons:", comparisons)
    print(f"Execution time: {elapsed:.8f} seconds")
    if positions:
        print("Pattern found.")
    else:
        print("Pattern not found.")