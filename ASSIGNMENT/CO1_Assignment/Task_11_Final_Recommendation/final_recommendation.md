# Task 11 – Final Design Recommendation

## Candidate recommendation
For repeated exact-match lookup by a unique registration number, a hash-based index is a strong candidate because lookup is expected Θ(1) after expected Θ(n) construction. A database's persistent unique index is generally more suitable for a real university service than rebuilding an in-memory Python dictionary for every application start.

## Alternatives and trade-offs
- Linear search: minimal setup, but Θ(n) per lookup; appropriate mainly for tiny collections or rare queries.
- Binary search: Θ(log n) lookup after sorting; good when sorted order and range queries matter, but sorting is O(n log n) if needed.
- Hash table: expected Θ(1) exact lookup and expected Θ(n) construction, but requires memory and has Θ(n) pathological worst-case lookup.

## Evidence required
Insert measured timings from the benchmark. State the machine/Python environment, include preprocessing cost, and explain why the chosen structure suits the measured workload. Do not select an algorithm based on Big-O alone.

##  Recommended Algorithm

The recommended approach for repeated student-record retrieval is Hash Table Search.

### Reasons for Selection

1. Hash Table Search provides expected constant-time lookup.
2. It does not require sorting student records.
3. It supports frequent registration-number searches.
4. The hash table can be constructed once and reused.
5. It is suitable for large student databases.

###  Theoretical Efficiency

| Operation | Complexity |
|---|---|
| Hash table construction | \(O(n)\)expected |
| Successful lookup | \(O(n)\) expected |
| Unsuccessful lookup | \(O(n)\) expected |
| Worst-case lookup | \(O(n)\) |

### Trade-offs

- Hash tables require additional memory.
- Hash table construction takes time.
- Collisions may reduce lookup efficiency.
- Updates must be reflected in the hash table.

###  Final Recommendation
Hash Table Search is recommended because the university requires efficient retrieval of student information using unique registration numbers. Its expected constant-time lookup provides an advantage for repeated searches on large datasets. Although the hash table requires additional memory and preprocessing, these costs can be justified when the index is reused for many search operations.
