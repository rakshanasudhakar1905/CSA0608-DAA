import math
import random
def brute_force(points, counter):
    best = float("inf")
    pair = None
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            counter[0] += 1
            d = math.dist(points[i], points[j])
            if d < best:
                best, pair = d, (points[i], points[j])
    return best, pair
def closest_pair_dc(points):
    """Returns (minimum distance, pair, number of distance calculations)."""
    counter = [0]
    px = sorted(points)
    py = sorted(points, key=lambda p: p[1])
    def dist(p, q):
        counter[0] += 1
        return math.dist(p, q)
    def solve(x_sorted, y_sorted):
        n = len(x_sorted)
        if n <= 3:
            best, pair = float("inf"), None
            for i in range(n):
                for j in range(i + 1, n):
                    d = dist(x_sorted[i], x_sorted[j])
                    if d < best:
                        best, pair = d, (x_sorted[i], x_sorted[j])
            return best, pair
        mid = n // 2
        left_x, right_x = x_sorted[:mid], x_sorted[mid:]
        split_x = right_x[0][0]
        left_set = set(left_x)
        left_y = [p for p in y_sorted if p in left_set]
        right_y = [p for p in y_sorted if p not in left_set]
        d1, pair1 = solve(left_x, left_y)
        d2, pair2 = solve(right_x, right_y)
        if d1 < d2:
            best, pair = d1, pair1
        else:
            best, pair = d2, pair2
        strip = [p for p in y_sorted if abs(p[0] - split_x) < best]
        for i in range(len(strip)):
            # In y-sorted order, only the next at most 7 points need checking.
            for j in range(i + 1, min(i + 8, len(strip))):
                if strip[j][1] - strip[i][1] >= best:
                    break
                d = dist(strip[i], strip[j])
                if d < best:
                    best, pair = d, (strip[i], strip[j])
        return best, pair
    answer, pair = solve(px, py)
    return answer, pair, counter[0]
def main():
    print("Q5: BRUTE FORCE AND DIVIDE-AND-CONQUER CLOSEST PAIR")
    for n in (10, 50, 100, 300):
        random.seed(n)
        points = [(random.random() * 1000, random.random() * 1000) for _ in range(n)]
        c = [0]
        bdist, bpair = brute_force(points, c)
        ddist, dpair, dc_count = closest_pair_dc(points)
        print(f"n={n:3}: same_distance={math.isclose(bdist, ddist)}, "
              f"brute_distance_calculations={c[0]}, D&C_distance_calculations={dc_count}, "
              f"distance={ddist:.4f}")
if __name__ == "__main__":
    main()
