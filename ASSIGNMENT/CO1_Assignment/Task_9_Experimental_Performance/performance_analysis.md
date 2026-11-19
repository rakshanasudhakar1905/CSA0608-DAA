# Task 9 – Experimental Performance

## How to run
Execute `python Task_8_Implementation_Testing/Source_Code/search_experiments.py` from the repository root. The program writes `performance_results.csv`, `execution_time.png`, `comparison_count.png`, and `preprocessing_time.png` into `Report/Tables_and_Graphs/`.

## Method
- Dataset sizes: 1,000; 10,000; 100,000; 1,000,000.
- Registration numbers are unique integers.
- Test cases: first, middle, last, and absent target.
- Search timing uses `time.perf_counter()` and the median of five repetitions.
- Preprocessing is measured separately.
- Correctness is checked for each algorithm and test case.
- Linear and binary search report explicit key comparisons. Python dictionary internal probes/equality comparisons are not exposed, so hash lookup comparison count is left blank rather than fabricated.

## Results
After running the benchmark, insert your measured summary tables and discuss the generated graphs here. Do not write invented timings. Record Python version, operating system, CPU/RAM if available, and any changes made to the benchmark.

## Interpretation prompts
1. How did linear search timing change with n?
2. Did binary search grow more slowly?
3. Did dictionary lookup stay approximately flat?
4. How did sorting and dictionary construction scale?
5. Were any results noisy or affected by system load?
