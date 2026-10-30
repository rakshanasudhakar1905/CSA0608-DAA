"""Production-oriented SentinelOps alert-triage algorithms.

Public outputs:
- sort_alerts mutates and returns the input list, with stable descending severity.
- build_blocklist_index + is_blocked_indexed support repeated O(1)-average lookups.
- find_signature_kmp returns all (including overlapping) match positions.
- closest_logins_divide_conquer returns (pair, Euclidean distance); fewer than 2 => (None, None).
"""
import math


def sort_alerts(alerts):
    """Stable in-place Timsort by descending severity; O(n log n) worst case."""
    alerts.sort(key=lambda alert: alert[1], reverse=True)
    return alerts


def build_blocklist_index(blocklist):
    """Build once, then reuse the set for repeated membership checks."""
    return set(blocklist)


def is_blocked_indexed(blocked_ips, ip):
    """Average O(1) membership test against a prebuilt set."""
    return ip in blocked_ips


def find_signature_kmp(log, pattern):
    """Knuth-Morris-Pratt scan: O(n + m), with no backtracking in the log."""
    n, m = len(log), len(pattern)
    if m == 0:
        return list(range(n + 1))
    if m > n:
        return []

    # Longest proper prefix that is also a suffix for each pattern prefix.
    lps = [0] * m
    length = 0
    i = 1
    while i < m:
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        elif length:
            length = lps[length - 1]
        else:
            lps[i] = 0
            i += 1

    hits = []
    i = j = 0
    while i < n:
        if log[i] == pattern[j]:
            i += 1
            j += 1
            if j == m:
                hits.append(i - j)
                j = lps[j - 1]  # retain overlap without rescanning text
        elif j:
            j = lps[j - 1]
        else:
            i += 1
    return hits


def closest_logins_divide_conquer(events):
    """Closest pair in 2-D, O(n log n) expected/deterministic geometric bound.

    Uses squared distances internally (no square roots in pair comparisons).
    Returns original event indices. Equal-distance ties choose the
    lexicographically smallest index pair. Fewer than two events => (None, None).
    """
    n = len(events)
    if n < 2:
        return None, None

    points = [(x, y, idx) for idx, (x, y) in enumerate(events)]
    # Handle duplicate coordinates up front; the minimum distance is zero.
    duplicates = {}
    best_zero = None
    for x, y, idx in points:
        if (x, y) in duplicates:
            candidate = (duplicates[(x, y)], idx)
            if best_zero is None or candidate < best_zero:
                best_zero = candidate
        else:
            duplicates[(x, y)] = idx
    if best_zero is not None:
        return best_zero, 0.0

    points_x = sorted(points, key=lambda p: (p[0], p[1], p[2]))
    points_y = sorted(points, key=lambda p: (p[1], p[0], p[2]))

    def dist2(a, b):
        dx = a[0] - b[0]
        dy = a[1] - b[1]
        return dx * dx + dy * dy

    def choose(best, candidate_d2, candidate_pair):
        if candidate_pair[0] > candidate_pair[1]:
            candidate_pair = (candidate_pair[1], candidate_pair[0])
        if (candidate_d2 < best[0] or
            (candidate_d2 == best[0] and
             (best[1] is None or candidate_pair < best[1]))):
            return candidate_d2, candidate_pair
        return best

    def solve(px, py):
        size = len(px)
        if size <= 3:
            best = (math.inf, None)
            for a in range(size):
                for b in range(a + 1, size):
                    best = choose(best, dist2(px[a], px[b]),
                                  (px[a][2], px[b][2]))
            return best

        mid = size // 2
        left_x, right_x = px[:mid], px[mid:]
        left_ids = {p[2] for p in left_x}
        left_y, right_y = [], []
        for point in py:
            (left_y if point[2] in left_ids else right_y).append(point)

        best = solve(left_x, left_y)
        best = choose(best, *solve(right_x, right_y))
        split_x = right_x[0][0]
        strip = [p for p in py if (p[0] - split_x) ** 2 <= best[0]]

        # In 2-D, packing limits relevant successors to seven.
        for i in range(len(strip)):
            upper = min(i + 8, len(strip))
            for j in range(i + 1, upper):
                dy = strip[j][1] - strip[i][1]
                if dy * dy > best[0]:
                    break
                best = choose(best, dist2(strip[i], strip[j]),
                              (strip[i][2], strip[j][2]))
        return best

    best_d2, best_pair = solve(points_x, points_y)
    return best_pair, math.sqrt(best_d2)


if __name__ == "__main__":
    alerts = [("A1", 3), ("A2", 9), ("A3", 5), ("A4", 9), ("A5", 1)]
    blocklist = ["10.0.0.5", "10.0.0.9", "172.16.4.2"]
    queries = ["10.0.0.9", "10.0.0.5", "8.8.8.8"]
    events = [(2, 3), (12, 30), (40, 50), (5, 1), (12, 10), (3, 4)]
    print("Sorted alerts:", sort_alerts(alerts))
    index = build_blocklist_index(blocklist)
    print("Blocked queries:", [is_blocked_indexed(index, ip) for ip in queries])
    print("Signature positions:", find_signature_kmp("FAILFAIXFAIL", "FAIL"))
    print("Closest logins:", closest_logins_divide_conquer(events))
