# Task 7 – Solve the Recurrence

Use the iteration method for T(n) = T(n/2) + c, with T(1) = d.

T(n) = T(n/2) + c
     = T(n/4) + 2c
     = T(n/8) + 3c
     = T(n/2^k) + kc

Stop when n/2^k ≈ 1:
n/2^k ≈ 1
2^k ≈ n
k ≈ log₂(n)

Substitute k:
T(n) = T(1) + c log₂(n)
     = d + c log₂(n)

Thus T(n) = Θ(log n).

The method applies because each recursive call reduces the input size by about half and performs constant non-recursive work. This explains why binary search grows much more slowly than linear search.
## Solving the Recurrence Using the Master Theorem

The recurrence relation obtained in Task 6 is:

\[
T(n) = T(n/2) + c
\]

We solve it using the Master Theorem.

### Step 1: Write the General Recurrence Form

\[
T(n) = aT(n/b) + f(n)
\]

### Step 2: Identify the Values

Comparing with Binary Search:

\[
a = 1
\]

\[
b = 2
\]

\[
f(n) = \Theta(1)
\]

### Step 3: Calculate the Critical Function

\[
n^{\log_b a}
\]

Substitute the values:

\[
= n^{\log_2 1}
\]

\[
= n^0
\]

\[
= 1
\]

Therefore:

\[
n^{\log_b a} = \Theta(1)
\]

### Step 4: Apply the Master Theorem

We have:

\[
f(n) = \Theta(n^{\log_b a})
\]

Therefore, Master Theorem Case 2 applies.

\[
T(n) = \Theta(n^{\log_b a}\log n)
\]

Substituting:

\[
T(n) = \Theta(1 \times \log n)
\]

### Final Answer

\[
\boxed{T(n) = \Theta(\log n)}
\]

**Interpretation:**

The recursive Binary Search algorithm has logarithmic time complexity. As the number of student records increases, the number of comparisons increases very slowly because half of the remaining records are eliminated during every recursive call.
