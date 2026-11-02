
# SQL Injection Experiment

## Objective
Demonstrate SQL injection using an unsafe SQL query and prevent it using parameterized queries.

## 1. Normal Search

Input:
Python Crash Course

| Method | Result count |
|---|---:|
| Unsafe query | 1 |
| Safe query | 1 |

## 2. Malicious Input

Input:
' OR '1'='1

| Method | Result count |
|---|---:|
| Unsafe query | 7 |
| Safe query | 0 |

## 3. Explanation

The unsafe query directly inserts user input into the SQL statement using an f-string.

The malicious input changes the SQL condition and returns all 7 items.

The safe query uses a parameterized placeholder (?) and passes the input separately.

SQLite treats the malicious input as ordinary text instead of executable SQL.

## 4. Conclusion

Parameterized queries prevent SQL injection by separating SQL instructions from user-supplied data.

All database queries that use user input should use parameterized statements.
