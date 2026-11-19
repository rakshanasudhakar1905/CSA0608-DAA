# Task 3 – Mathematical Time-Complexity Derivation

Let n be the number of records. Assume each registration number comparison and basic index operation takes constant time.

## Linear search
For a missing target, every element is examined:
C_L(n) = 1 + 1 + ... + 1 (n terms) = n.
If each comparison costs c and loop overhead is represented by a, T_L(n) = a + cn, hence worst-case Θ(n). Preprocessing cost is zero.

## Recursive binary search
For a sorted array, one call performs constant work and recurses on at most half the interval:
T_B(n) = T_B(floor(n/2)) + c, for n > 1, with T_B(0) = d (or a constant-size base case).
After k levels, T_B(n) = T_B(n/2^k) + kc. The recursion stops when n/2^k is at most 1, so k ≈ log₂ n. Therefore search time is Θ(log n). If sorting is needed, comparison sorting costs O(n log n), so total initial cost is O(n log n) + O(log n) = O(n log n). For q searches on the same sorted data, total cost is O(n log n + q log n).

## Hash table
Building a dictionary from n keys performs n insertions. With ordinary hash distribution, construction is expected Θ(n) and additional space is Θ(n). Each lookup is expected Θ(1), so q lookups cost expected Θ(n + q), including construction. In a pathological collision case, an individual lookup can take Θ(n); actual Python dictionary performance depends on key type and implementation details.

## Preprocessing comparison
- Linear: no preprocessing; each query O(n).
- Binary: sort once O(n log n), then each query O(log n).
- Hash: build once expected O(n), then each query expected O(1).

The cost of preprocessing must be amortized over the number of queries; it should not be charged repeatedly if the prepared structure is reused.
