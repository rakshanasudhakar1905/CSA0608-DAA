import random
import math
import time
def closest_pair(points):
    n = len(points)
    if n < 2:
        return None, None, 0, 0, 0.0
    min_distance = float("inf")
    closest_points = None
    pairs_examined = 0
    distance_calculations = 0
    start = time.perf_counter()
    for i in range(n):
        for j in range(i + 1, n):
            pairs_examined += 1
            x1, y1 = points[i]
            x2, y2 = points[j]
            distance_calculations += 1
            distance = math.sqrt(
                (x2 - x1) ** 2 + (y2 - y1) ** 2
            )
            if distance < min_distance:
                min_distance = distance
                closest_points = (points[i], points[j])
    elapsed = time.perf_counter() - start
    return (
        closest_points,
        min_distance,
        pairs_examined,
        distance_calculations,
        elapsed
    )
random.seed(42)
for size in [5, 10, 20, 50, 100]:
    points = [
        (random.randint(0, 1000), random.randint(0, 1000))
        for _ in range(size)
    ]
    (
        pair,
        distance,
        pairs,
        calculations,
        elapsed
    ) = closest_pair(points)
    expected_pairs = size * (size - 1) // 2
    print("\n" + "=" * 50)
    print("NUMBER OF POINTS:", size)
    print("=" * 50)
    print("Closest pair:", pair)
    print("Minimum distance:", round(distance, 4))
    print("Pairs examined:", pairs)
    print("Expected pairs:", expected_pairs)
    print("Distance calculations:", calculations)
    print(f"Execution time: {elapsed:.8f} seconds")