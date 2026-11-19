# Task 12 – Day-4 Design Challenge 

Changed Requirement
The university now needs to process 50,000 search requests per hour using a database containing 1,000,000 student records.

New student records are added only once per day.

The original design must be re-evaluated to determine whether it should be retained, modified or redesigned.
TASK 12A – Impact Analysis 
1. Changes in Requirements
Original requirement	Changed requirement
Dataset size varies	Fixed database of 1,000,000 records
Search frequency unspecified	50,000 searches per hour
Update frequency unspecified	New records added once daily
General searching efficiency	High repeated-search performance

2. Impact of Changed Requirements
The new requirements increase the importance of searching efficiency because the university performs 50,000 search operations every hour.

The database receives updates only once per day, meaning that the search index does not need to be rebuilt continuously.

Therefore, preprocessing becomes more acceptable because its cost can be distributed across a large number of search requests.

Conclusion: The system should prioritize fast repeated searches and efficient management of the student records.
TASK 12B – Evaluation of the Original Design (2 Marks)
The original design contains Linear Search, Recursive Binary Search and Hash Table Search.

Their suitability under the changed requirements is evaluated below.
Algorithm	Complexity	Suitability
Linear Search	\(O(n)\)	Less suitable
Binary Search	\(O(\log n)\)	Suitable
Hash Table Search	Expected \(O(1)\)	Suitable for frequent lookups

Linear Search
For one million records, Linear Search may require one million comparisons for an unsuccessful search.

For 50,000 unsuccessful searches:
\[
50,000\times1,000,000
\]

\[
=50,000,000,000
\]

This is 50 billion comparisons in the worst case.

Therefore, Linear Search is not appropriate as the primary search strategy.
Binary Search
Binary Search requires approximately 20 comparisons in the worst case for one million records.

For 50,000 searches:
\[
50,000\times20
\]

\[
=1,000,000
\]

It provides efficient searching but requires sorted records.
Hash Table Search
Hash Table Search provides expected constant-time lookup.

The hash table can be constructed once and reused for repeated searches.

Therefore, it is highly suitable for the changed requirements.
TASK 12C – Adaptation or Redesign (2 Marks)
Proposed Decision: MODIFY
The original Hash Table Search approach is modified into a persistent, reusable hash-indexing system.
Revised Algorithm
1. Load student records from the database.
2. Create a hash table using registration numbers as keys.
3. Store student details as corresponding values.
4. Retain the hash table for repeated searches.
5. When a faculty member enters a registration number, retrieve the corresponding student record.
6. When new records are added daily, update the hash table or rebuild it.
7. Continue processing search requests using the updated hash table.
Revised Pseudocode
ALGORITHM OPTIMIZED_STUDENT_SEARCH

1. LOAD student records

2. CREATE HASH_TABLE

3. FOR each student record
4.     HASH_TABLE[registration_number] = student_record
5. END FOR

6. WHILE system is running

7.     READ target_registration_number

8.     IF target_registration_number EXISTS
           IN HASH_TABLE THEN

9.         DISPLAY student record

10.    ELSE

11.        DISPLAY "Student Not Found"

12.    END IF

13. END WHILE

14. WHEN daily records are updated:
15.     UPDATE HASH_TABLE with new records

16. STOP
