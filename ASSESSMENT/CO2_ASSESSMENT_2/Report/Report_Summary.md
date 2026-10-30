# SentinelOps CO2 Report

## Expected sample outputs
- Alerts: `[('A2', 9), ('A4', 9), ('A3', 5), ('A1', 3), ('A5', 1)]`
- Blocked queries: `[True, True, False]`
- Signature positions: `[0, 8]`
- Closest pair: `(0, 5)`, distance `sqrt(2) = 1.4142 km`

## Original program output
```text
Sorted alerts: [('A4', 9), ('A3', 5), ('A3', 5), ('A5', 1), ('A5', 1)]
Blocked queries: [False, False, False]
Signature positions: [0, 4]
Closest logins: ((0, 2), 60.440052945046304)
```

## Nine defects
1. Insertion loop excludes index 0 (`j > 0`).
2. Insertion writes at `j`, not `j+1`.
3. Blocklist returns False on a match.
4. Signature outer loop excludes final legal start (`range(n-m)`).
5. Signature post-loop test mistakes a final-character mismatch for a match.
6. Closest-pair minimum starts at zero, not infinity.
7. Closest-pair comparison uses `>` instead of `<`.
8. Closest-pair checks self-pairs.
9. Closest-pair checks both pair orders, duplicating work.

## Debug traces
Insertion trace and KMP alignment are included in the DOCX report. The corrected test harness covers empty blocklists, final-position patterns, overlong patterns, overlapping patterns, equal severities, fewer than two events, duplicate coordinates, and random closest-pair cross-checks.

## Experimental closest-pair counts
| Events | Brute force | Divide and conquer |
|---:|---:|---:|
| 1,000 | 499,500 | 1,112 |\n| 4,000 | 7,998,000 | 4,605 |\n| 8,000 | 31,996,000 | 9,291 |\n\nInsertion-sort comparison measurements are in `insertion_sort_comparisons.csv`. See the DOCX report for analysis and graphs.\n