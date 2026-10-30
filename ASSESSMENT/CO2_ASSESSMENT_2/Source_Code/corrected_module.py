"""Corrected SentinelOps algorithms, retaining the original interfaces."""
import math


def sort_alerts(alerts):
    """Stable insertion sort: severity descending; equal severities keep arrival order."""
    for i in range(1, len(alerts)):
        key = alerts[i]
        j = i - 1
        while j >= 0 and alerts[j][1] < key[1]:
            alerts[j + 1] = alerts[j]
            j -= 1
        alerts[j + 1] = key
    return alerts


def is_blocked(blocklist, ip):
    """Return True only when ip occurs in blocklist (sequential search)."""
    for i in range(len(blocklist)):
        if blocklist[i] == ip:
            return True
    return False


def find_signature(log, pattern):
    """Return every occurrence, including overlapping and final-position matches."""
    n, m = len(log), len(pattern)
    if m == 0:
        return list(range(n + 1))
    if m > n:
        return []
    hits = []
    for i in range(n - m + 1):
        matched = True
        for j in range(m):
            if log[i + j] != pattern[j]:
                matched = False
                break
        if matched:
            hits.append(i)
    return hits


def closest_logins(events):
    """Return ((first_index, second_index), distance); fewer than 2 => (None, None)."""
    if len(events) < 2:
        return None, None
    min_dist = math.inf
    pair = None
    for i in range(len(events)):
        for j in range(i + 1, len(events)):
            d = math.hypot(events[i][0] - events[j][0],
                           events[i][1] - events[j][1])
            candidate = (i, j)
            if d < min_dist:
                min_dist = d
                pair = candidate
    return pair, min_dist
