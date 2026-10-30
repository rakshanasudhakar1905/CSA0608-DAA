"""Automated correctness and boundary tests for corrected and optimised modules."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from corrected_module import sort_alerts as corrected_sort, is_blocked, find_signature, closest_logins
from optimized_module import (sort_alerts as optimized_sort, build_blocklist_index,
    is_blocked_indexed, find_signature_kmp, closest_logins_divide_conquer)


def run_tests():
    checks = 0

    def check(name, condition):
        nonlocal checks
        assert condition, f"FAILED: {name}"
        checks += 1
        print(f"PASS: {name}")

    sample = [("A1", 3), ("A2", 9), ("A3", 5), ("A4", 9), ("A5", 1)]
    expected = [("A2", 9), ("A4", 9), ("A3", 5), ("A1", 3), ("A5", 1)]
    check("corrected insertion sort + stability", corrected_sort(sample.copy()) == expected)
    check("optimised stable sort", optimized_sort(sample.copy()) == expected)
    check("empty sort", optimized_sort([]) == [])
    check("already sorted sort", optimized_sort(expected.copy()) == expected)

    blocklist = ["10.0.0.5", "10.0.0.9", "172.16.4.2"]
    check("sequential search: present", is_blocked(blocklist, "10.0.0.9") is True)
    check("sequential search: absent", is_blocked(blocklist, "8.8.8.8") is False)
    check("sequential search: empty blocklist", is_blocked([], "8.8.8.8") is False)
    index = build_blocklist_index(blocklist)
    check("set lookup: present", is_blocked_indexed(index, "10.0.0.5") is True)
    check("set lookup: absent", is_blocked_indexed(index, "8.8.8.8") is False)
    check("set lookup: empty set", is_blocked_indexed(set(), "8.8.8.8") is False)

    log, pattern = "FAILFAIXFAIL", "FAIL"
    check("brute-force scan: sample", find_signature(log, pattern) == [0, 8])
    check("KMP scan: sample", find_signature_kmp(log, pattern) == [0, 8])
    check("KMP overlapping matches", find_signature_kmp("AAAAA", "AAA") == [0, 1, 2])
    check("KMP final-position match", find_signature_kmp("XXABC", "ABC") == [2])
    check("KMP pattern longer than log", find_signature_kmp("AB", "ABCDE") == [])
    check("KMP empty pattern boundaries", find_signature_kmp("ABC", "") == [0, 1, 2, 3])
    check("KMP no match", find_signature_kmp("ABCDEFG", "XYZ") == [])

    events = [(2, 3), (12, 30), (40, 50), (5, 1), (12, 10), (3, 4)]
    cp, cd = closest_logins(events)
    op, od = closest_logins_divide_conquer(events)
    check("corrected closest pair sample", cp == (0, 5) and abs(cd - (2 ** 0.5)) < 1e-12)
    check("optimised closest pair matches corrected", op == cp and abs(od - cd) < 1e-12)
    check("closest pair: empty events", closest_logins_divide_conquer([]) == (None, None))
    check("closest pair: one event", closest_logins_divide_conquer([(1, 2)]) == (None, None))
    check("closest pair: duplicate coordinates", closest_logins_divide_conquer([(0, 0), (2, 2), (0, 0)]) == ((0, 2), 0.0))
    check("closest pair: two events", closest_logins_divide_conquer([(0, 0), (3, 4)]) == ((0, 1), 5.0))

    # Cross-check random small cases against the corrected brute-force reference.
    import random
    rng = random.Random(7)
    for size in range(2, 35):
        pts = [(rng.randrange(-100, 101), rng.randrange(-100, 101)) for _ in range(size)]
        expected_pair, expected_dist = closest_logins(pts)
        got_pair, got_dist = closest_logins_divide_conquer(pts)
        check(f"random closest-pair cross-check n={size}",
              got_pair == expected_pair and abs(got_dist - expected_dist) < 1e-9)

    print(f"\nALL TESTS PASSED: {checks}")
    return checks



if __name__ == "__main__":
    run_tests()
