# Task 5 – Asymptotic Analysis

- **O(f(n))** gives an asymptotic upper bound.
- **Ω(f(n))** gives an asymptotic lower bound.
- **Θ(f(n))** gives a tight asymptotic bound when both upper and lower bounds match.

| Algorithm/operation | Best | Average/expected | Worst |
|---|---:|---:|---:|
| Linear search | Θ(1) | Θ(n) | Θ(n) |
| Binary search (sorted input) | Θ(1) | Θ(log n) | Θ(log n) |
| Hash lookup | expected Θ(1) | expected Θ(1) | Θ(n) |
###  Comparison for Large Datasets

For illustration, consider the following theoretical operation counts.

| Records | Linear Search (Worst) | Binary Search (Worst) | Hash Search (Expected) |
|--------:|----------------------:|----------------------:|-----------------------:|
| 1,000 | 1,000 | 10 | Constant |
| 10,000 | 10,000 | 14 | Constant |
| 100,000 | 100,000 | 17 | Constant |
| 1,000,000 | 1,000,000 | 20 | Constant |

When n grows from 1,000 to 1,000,000, n grows by a factor of 1,000. Linear worst-case comparisons can grow by roughly 1,000 times. Binary search needs around 10 additional halvings because log₂(1,000,000) is about 20 and log₂(1,000) is about 10. Expected hash lookup remains approximately independent of n under ordinary assumptions, but its memory and index-construction costs grow linearly.

Do not treat Big-O as an exact timing prediction. It describes growth for sufficiently large n, not hardware-specific seconds.
