# Phase 2.1 - Complexity Audit

## Predicted Time and Space Complexity

| Method | Time Complexity | Space Complexity |
|---|---|---|
| list_items() | O(n) | O(n) |
| search_items() | O(n) | O(r) |
| borrow() | O(L) | O(L) |
| return_item() | O(L + R) | O(1) auxiliary |
| overdue_report() | O(L log L) | O(L) |

n = catalogue size, L = loan count, R = reservation count, r = search results.

## Measured Results

Median execution time across five runs (milliseconds).

| Records | list_items | search_items | borrow | return_item | overdue_report |
|---:|---:|---:|---:|---:|---:|
| 1,000 | 0.0041 | 0.3620 | 0.0604 | 0.0453 | 0.2102 |
| 5,000 | 0.0273 | 3.0300 | 0.1185 | 0.2015 | 1.0457 |
| 10,000 | 0.0431 | 3.8567 | 0.2676 | 0.4045 | 2.2299 |
| 50,000 | 0.4647 | 20.7038 | 1.0949 | 2.1330 | 15.3770 |

## Queue Benchmark

| Operation | Median Time (seconds) |
|---|---:|
| list.pop(0) | 0.602115 |
| deque.popleft() | 0.005184 |

## Observations and Surprises

1. list_items() showed increasing execution time as the catalogue grew, which matches its predicted O(n) complexity. The increase at 50,000 records was larger than at smaller sizes, likely because of memory allocation and runtime overhead.
2. search_items() increased approximately in proportion to catalogue size, matching O(n). Searching for an item near the end requires checking almost the entire catalogue.
3. borrow() became slower as the loan count increased because it collects the member's active loans by scanning the loan list. Its measured growth is consistent with the O(L) prediction.
4. return_item() also became slower as the loan list grew. The benchmark places the target loan after the generated noise loans, so the method must scan many records before finding it.
5. overdue_report() increased in execution time as the number of loans grew because it scans the loan list and sorts the overdue results. The measured time also depends on how many loans qualify as overdue.
6. list.pop(0) took substantially longer than deque.popleft() for 100,000 entries. This is expected because list removal shifts remaining elements, whereas deque supports efficient removal from the front.

## Conclusion

The measured results generally support the predicted complexities. The deque benchmark demonstrates why a queue should use collections.deque rather than repeatedly removing the first element of a list. Small timing variations can occur because of operating-system scheduling, memory allocation and Python runtime overhead.