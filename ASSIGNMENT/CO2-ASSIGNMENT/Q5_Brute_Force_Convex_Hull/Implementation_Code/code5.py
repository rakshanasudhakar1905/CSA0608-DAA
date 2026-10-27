import time
import matplotlib.pyplot as plt
def cross_product(a, b, c):
    return ((b[0] - a[0]) * (c[1] - a[1])
            - (b[1] - a[1]) * (c[0] - a[0]))
def brute_force_convex_hull(points):
    n = len(points)
    hull_points = set()
    orientation_tests = 0
    start_time = time.perf_counter()
    if n < 3:
        return points, orientation_tests, time.perf_counter() - start_time
    for i in range(n):
        for j in range(i + 1, n):
            positive = False
            negative = False
            for k in range(n):
                if k == i or k == j:
                    continue
                value = cross_product(points[i], points[j], points[k])
                orientation_tests += 1
                if value > 0:
                    positive = True
                elif value < 0:
                    negative = True
                if positive and negative:
                    break
            if not (positive and negative):
                hull_points.add(points[i])
                hull_points.add(points[j])
    hull_points = list(hull_points)
    if len(hull_points) >= 3:
        center_x = sum(p[0] for p in hull_points) / len(hull_points)
        center_y = sum(p[1] for p in hull_points) / len(hull_points)
        hull_points.sort(
            key=lambda p: __import__("math").atan2(
                p[1] - center_y, p[0] - center_x
            )
        )
    elapsed_time = time.perf_counter() - start_time
    return hull_points, orientation_tests, elapsed_time
def display_hull(points, hull):
    plt.figure(figsize=(7, 5))
    x = [p[0] for p in points]
    y = [p[1] for p in points]
    plt.scatter(x, y, label="Input Points")
    if hull:
        hx = [p[0] for p in hull]
        hy = [p[1] for p in hull]
        if len(hull) >= 3:
            hx.append(hull[0][0])
            hy.append(hull[0][1])
        plt.plot(hx, hy, marker="o", label="Convex Hull")
    plt.title("Brute-Force Convex Hull")
    plt.xlabel("X-coordinate")
    plt.ylabel("Y-coordinate")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
def main():
    datasets = {
        "Small dataset": [
            (0, 0), (4, 0), (4, 4), (0, 4), (2, 2)
        ],
        "Medium dataset": [
            (0, 0), (5, 0), (6, 3), (3, 6),
            (0, 4), (2, 2), (3, 3), (4, 2)
        ],
        "Challenge dataset": [
            (0, 0), (6, 0), (7, 3), (4, 6),
            (0, 5), (2, 2), (3, 3), (5, 2),
            (2, 4), (3, 1)
        ]
    }
    for name, points in datasets.items():
        hull, tests, elapsed = brute_force_convex_hull(points)
        print("\nDataset:", name)
        print("Number of input points:", len(points))
        print("Input points:", points)
        print("Convex hull vertices:", hull)
        print("Orientation tests:", tests)
        print("Execution time:", format(elapsed, ".8f"), "seconds")
    points = datasets["Challenge dataset"]
    hull, _, _ = brute_force_convex_hull(points)
    display_hull(points, hull)
if __name__ == "__main__":
    main()