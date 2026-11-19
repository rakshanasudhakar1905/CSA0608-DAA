# Task 6 – Recurrence Formulation

Let T(n) be the time for recursive binary search over an interval containing n elements.

For n > 1:
- The algorithm performs constant work: calculate the midpoint, compare the target and choose a branch.
- Exactly one recursive call is made on an interval of at most floor(n/2) elements.
- The base case is an empty interval (not found) or a constant-sized interval / matching midpoint.

A simplified recurrence is:
T(n) = T(n/2) + c, for n > 1
T(1) = d
where c and d are constants. For exact integer intervals, floor/ceiling terms may be used; they do not change the asymptotic result.
The recurrence relation is formulated for the Recursive Binary Search algorithm.
## Recurrence Relation for Recursive Binary Search

The recurrence relation is formulated for the Recursive Binary Search algorithm.

### Step 1: Identify the Input Size

Let:

\[
n = Number of records in the current search interval
\]

### Step 2: Identify the Recursive Subproblem

Binary Search divides the dataset into two halves and continues searching only one half.

Therefore:

\[
Subproblem size = n/2
\]

### Step 3: Identify the Number of Recursive Calls

Only one recursive call is executed in each step.

\[
a = 1
\]

### Step 4: Identify the Work Outside Recursion

The algorithm calculates the middle position and performs a constant number of comparisons.

Therefore:

\[
f(n) = c
\]

### Step 5: Identify the Base Case

When the search interval becomes empty, the record is not found.

\[
T(0) = c_0
\]

When one element remains, the algorithm performs a constant amount of work.

\[
T(1) = c_1
\]

### Step 6: Formulate the Recurrence

Combining these components:

\[
T(n) = T(n/2) + c
\]

Where \(c\) represents the constant work performed during each recursive call.


