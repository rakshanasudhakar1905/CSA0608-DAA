# Task 4 – Best, Average, and Worst Cases

## Linear search
- Best: target is the first element; 1 comparison, Θ(1).
- Average successful search: if each of n positions is equally likely, expected comparisons are (1 + 2 + ... + n)/n = (n+1)/2, Θ(n).
- Worst: target is last or absent; n comparisons, Θ(n).

## Recursive binary search
- Best: target equals the midpoint of the first interval; one midpoint check, Θ(1).
- Average: target locations or unsuccessful gaps are reasonably distributed; the number of interval halvings is logarithmic, Θ(log n).
- Worst: target is at a leaf of the search process or absent; approximately floor(log₂ n)+1 midpoint checks, Θ(log n).

## Hash table search
- Best/expected: hash maps directly to a bucket/slot with no significant collision chain; expected Θ(1).
- Average: with a suitable hash distribution and controlled load factor, expected Θ(1).
- Worst: many keys collide or the structure suffers pathological probing; Θ(n) is possible.
  Comparison Table

Case analysis assumes unique registration numbers. For linear search, an absent key is a worst-case input. For binary search, the array must be sorted. For a dictionary, report the expected-case assumption rather than claiming a deterministic constant-time worst-case bound.
