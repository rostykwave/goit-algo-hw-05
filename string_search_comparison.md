# String Searching Algorithms Performance Comparison

## Test Environment

- File 1: `article1.txt`
- File 2: `article2.txt`

### Search Patterns:

**Text 1:**
- Existing pattern: `algorithm`
- Fictional pattern: `xyz123notfound`

**Text 2:**
- Existing pattern: `research`
- Fictional pattern: `qwerty456notexist`

## Results

### Execution Times

| Algorithm | Text 1 (Existing) | Text 1 (Fictional) | Text 2 (Existing) | Text 2 (Fictional) | Overall |
|:----------|:-----------------|:-------------------|:------------------|:-------------------|:--------|
| boyer_moore | 166.5458 µs | 103.1458 µs | 241.0583 µs | 119.0792 µs | 157.4573 µs |
| kmp | 1.2234 ms | 1.2997 ms | 1.8463 ms | 1.8463 ms | 1.5539 ms |
| rabin_karp | 1.7902 ms | 1.8929 ms | 2.8015 ms | 2.7330 ms | 2.3044 ms |

### Fastest Algorithms

- **Text 1 (Existing pattern)**: boyer_moore - 166.5458 µs
- **Text 1 (Fictional pattern)**: boyer_moore - 103.1458 µs
- **Text 2 (Existing pattern)**: boyer_moore - 241.0583 µs
- **Text 2 (Fictional pattern)**: boyer_moore - 119.0792 µs
- **Overall fastest algorithm**: boyer_moore - 157.4573 µs

## Conclusion

Based on the performance measurements of the three string searching algorithms (Boyer-Moore, Knuth-Morris-Pratt, and Rabin-Karp) on two different texts with both existing and fictional patterns, we can observe:

- For existing patterns, the **boyer_moore** algorithm consistently performs best across both texts.
- For fictional (non-existing) patterns, the **boyer_moore** algorithm consistently performs best across both texts.

Overall, the **boyer_moore** algorithm demonstrates the best average performance across all test cases. This suggests it would be the most reliable choice for general-purpose string searching tasks with unknown patterns and texts.

### Algorithm Characteristics

- **Boyer-Moore**: Generally performs well, especially for longer patterns, as it can skip portions of the text. Its performance advantage is more pronounced in cases where the pattern is not found or appears near the end of the text.
- **Knuth-Morris-Pratt**: Ensures linear time complexity in the worst case and performs consistently across different scenarios.
- **Rabin-Karp**: Uses hashing to efficiently handle multiple pattern searches, but may not always outperform the other algorithms for single pattern searches.
