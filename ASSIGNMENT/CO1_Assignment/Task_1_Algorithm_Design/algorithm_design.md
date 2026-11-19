# Task 1 – Design the Algorithms

## Problem
Given unique student registration numbers and a target registration number, determine whether the target exists and return its position/record.

## Approach 1: Iterative Linear Search
**Strategy:** Sequential search. It checks records from the beginning until a match is found or the list ends. No preprocessing is required.

**Pseudocode**
```text
LINEAR_SEARCH(A, key)
    for i = 0 to length(A)-1
        if A[i] == key
            return i
    return -1
```

**Why investigate it:** It is simple, works on unsorted data, and provides a baseline. It becomes expensive for large datasets and repeated searches.

## Approach 2: Recursive Binary Search
**Strategy:** Divide and conquer. The input must be sorted. Each call checks the midpoint and recursively searches only the half that can contain the key.

**Pseudocode**
```text
BINARY_SEARCH(A, low, high, key)
    if low > high
        return -1
    mid = low + floor((high-low)/2)
    if A[mid] == key
        return mid
    if key < A[mid]
        return BINARY_SEARCH(A, low, mid-1, key)
    return BINARY_SEARCH(A, mid+1, high, key)
```

**Preprocessing:** Sort once before repeated queries; include and report the sorting cost. Recursive depth is logarithmic, so recursion-limit concerns are not expected for a million elements.

**Why investigate it:** It illustrates recursive divide-and-conquer and performs well when records are kept sorted. It also supports ordered/range-oriented use cases better than a hash table.

## Approach 3: Hash Table Search
**Strategy:** Transform the registration number into a hash-table lookup using a dictionary keyed by registration number.

**Pseudocode**
```text
BUILD_HASH(records)
    H = empty hash table
    for each record in records
        H[record.registration_number] = record
    return H

HASH_SEARCH(H, key)
    if key is in H
        return H[key]
    return NOT_FOUND
```

**Preprocessing:** Build the dictionary once and update it when new records arrive. Construction takes expected linear time and linear extra space.

**Why investigate it:** The scenario mostly asks exact-match existence/retrieval queries, making a hash index a strong candidate. Expected lookup is constant time under ordinary hashing assumptions; pathological collision behaviour can be linear.

## Fair-comparison notes
- Use the same unique keys and equivalent target cases for all algorithms.
- Measure preprocessing separately from lookup.
- Do not include data generation in search timing.
- Python's `dict` does not expose its internal equality-comparison count. Report its explicit membership/lookup operations separately rather than claiming a precise internal comparison count.
