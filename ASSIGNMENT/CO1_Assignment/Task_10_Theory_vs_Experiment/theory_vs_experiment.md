# Task 10 – Theory vs Experiment

Complete this section after running the benchmark and reviewing `Report/Tables_and_Graphs/performance_results.csv`.

## Expected theory
- Linear search: worst-case Θ(n); an absent target causes n comparisons.
- Recursive binary search: Θ(log n) search time after sorting.
- Hash table lookup: expected Θ(1), worst-case Θ(n); building the dictionary is expected Θ(n).

## Compare with measured results
Insert a table of measured search time and preprocessing time for each dataset size. Discuss whether the observed growth follows the theoretical trend.

## Why measurements differ from theory
Big-O ignores constants and hardware details. Timing can be influenced by interpreter overhead, cache effects, memory allocation, garbage collection, system load and measurement resolution. A benchmark across four input sizes supports a trend discussion but does not prove an asymptotic bound.

## Required conclusion
Write a conclusion based on the measurements from your own computer, including any anomalies and limitations. Do not claim a result that is not shown by your CSV/graphs.
