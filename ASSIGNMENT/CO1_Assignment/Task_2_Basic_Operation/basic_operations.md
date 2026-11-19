# Task 2 – Identify the Basic Operation

## Linear search
The dominant operation is comparing `A[i]` with the target key. It occurs in each loop iteration. For a missing key, it occurs n times; for a successful target at position i, it occurs i+1 times (zero-based indexing). The count grows linearly with n.

## Recursive binary search
The dominant operation is comparing the target against the midpoint element and deciding whether to stop or which half to search. Only one recursive branch is followed. The search interval is approximately halved on each call, so the number of levels grows logarithmically.

## Hash table search
The main work is hashing the key and checking the corresponding dictionary entry. Python dictionary lookup is a built-in operation, and its internal collision probes/equality checks are not exposed as a reliable counter. Therefore this benchmark reports the number of explicit lookup operations and timing, not a fabricated internal key-comparison count. Expected lookup is O(1) with good hashing and controlled load; worst case can be O(n).
