# CO1 Assignment – Student Registration Number Search

## Objective
Design, implement, test, and compare three algorithmic approaches for locating university student registration numbers.

## Algorithms
1. Iterative Linear Search
2. Recursive Binary Search
3. Hash Table Search using Python's dictionary

## Dataset sizes
1,000; 10,000; 100,000; and 1,000,000 records.

## Requirements
- Python 3.10+
- pandas
- matplotlib

Install dependencies:
```bash
python -m pip install pandas matplotlib
```

## Run
From this folder:
```bash
python Task_8_Implementation_Testing/Source_Code/search_experiments.py
```

The program writes CSV files and PNG graphs to `Report/Tables_and_Graphs/`. It checks correctness, measures preprocessing and search time, and records comparison counts where the implementation can reliably count them. Dictionary internal equality checks are not directly exposed by Python, so the report distinguishes them from explicit comparisons.

## Repository contents
- `Task_1_Algorithm_Design/` through `Task_12_Design_Challenge/`: task write-ups and analysis
- `Task_8_Implementation_Testing/Source_Code/`: runnable Python benchmark
- `Report/Tables_and_Graphs/`: generated CSV results and graphs (run the program to generate these)
- `Report/Source_Code_Screenshots/` and `Report/Output_Screenshots/`: placeholders for screenshots captured from your own execution
- `Report/Documentation/`: report outline and instructions for creating the final PDF/DOCX

## Important
Experimental results are machine-dependent. Run the program on your computer before submitting and use the generated measurements in the report. Do not present estimated or placeholder results as measured evidence.
