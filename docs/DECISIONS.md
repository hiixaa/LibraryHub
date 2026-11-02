# LibraryHub Mini — Design Decisions

## Phase 1: Python and OOP

### Decision 1: Use inheritance for common behaviour
`LibraryItem` will be the parent class for `Book`, `Magazine` and `ReferenceItem`. `Member` will be the parent class for `StudentMember`, `RegularMember` and `PremiumMember`.

### Decision 2: Use composition for library records
`Library` will manage collections of items, members and loans. Each `Loan` will reference the member and item involved in that borrowing transaction.

### Decision 3: Use polymorphism for membership rules
Each membership subclass will define its own borrowing limit, loan period and daily fine rate. This avoids repeating membership-type conditions throughout the code.

## Phase 1.5: Console Application and Testing

### Decision 1: Use CSV files for starter data
CSV files will store books, members, loans and fines. This separates the sample data from the application logic and makes it easier to load records.

### Decision 2: Use a menu-driven console interface
A menu-driven interface will allow users to perform library operations without directly interacting with Python classes or methods.

### Decision 3: Use custom exceptions for error handling
Custom exceptions will represent errors such as unavailable items, missing members, duplicate loans and unpaid fines. This makes error handling clearer and more specific.

### Decision 4: Use Pytest for automated testing
Pytest will be used to test individual classes and library operations. Parameterized tests will help verify multiple input cases efficiently.

### Decision 5: Use a virtual environment
A Python virtual environment will isolate project dependencies. `requirements.txt` will record the dependencies needed to set up the project.

### Decision 6: Maintain an audit log
Important library operations will be recorded in an audit log to support tracking and debugging.

## Phase 2.5 – Recursion

### Recursive algorithms

Implemented factorial, Fibonacci and sum of digits using recursion.

- Factorial uses 0 as its base case and reduces n by 1.
- Fibonacci uses 0 and 1 as base cases and adds the two previous values.
- Sum of digits uses a single-digit base case and removes the last digit using integer division.

### Category tree

Represented library categories using a tree structure.

Each CategoryNode stores:
- Category name
- Direct item count
- Child categories

Recursive functions:
- print_tree(): displays the category hierarchy.
- count_items(): finds a category and counts all items under it.
- count_subtree_items(): recursively counts items in a subtree.
- path_to(): finds the path from the root to a category.

### Recursion vs iteration

Implemented both recursive and iterative versions of subtree item counting.

Both returned 7 for the sample category tree.

Recursion is clearer for naturally hierarchical structures such as category trees. Iteration uses an explicit stack and avoids Python's recursion depth limit.

Python's sys.setrecursionlimit() changes the interpreter's recursion limit but does not remove memory or stack limitations.

## Phase 3.1 – Database Anomalies

### Update anomaly
If Rahul Mehta changes his email address, every row
containing his details must be updated. Updating only
some rows creates inconsistent information.

### Insert anomaly
Divya Rao (M005) has never borrowed a book. Since the
flat file requires loan and item information, her member
details cannot be inserted independently.

### Delete anomaly
Deleting a member's only loan row could also remove
their name, email and membership information.

### Conclusion
The flat-file design creates unnecessary duplication
and makes data maintenance difficult. We need to
normalise the data into related tables.

## Phase 3.2 – Normalisation

### First Normal Form (1NF)

The original flat file violated 1NF because the authors
column stored multiple author names in a single cell,
separated by semicolons.

To satisfy 1NF, each cell must contain one atomic value.
The authors were therefore separated so that each row
contains one author value.

This removes multiple values from a single cell. However,
it introduces repeated loan and item details when an item
has multiple authors. This duplication will be addressed
using separate Authors and Item_Authors tables.

### Second Normal Form (2NF)

2NF requires a table to be in 1NF and every non-key
attribute to depend on the whole candidate key.

In the Item_Authors example, the composite key consists
of ISBN and Author_ID.

Item_Title depends only on ISBN, while Author_Name
depends only on Author_ID. These are partial dependencies.

To remove them, item details are stored in the Items table,
author details are stored in the Authors table, and the
Item_Authors junction table connects the two using a
composite primary key (ISBN, Author_ID).

### Third Normal Form (3NF)

3NF requires a table to be in 2NF and have no transitive
dependencies between non-key attributes.

In the Members example, Member_ID determines
Membership_Type, and Membership_Type determines
Loan_Limit. Therefore, Loan_Limit is transitively
dependent on Member_ID.

To remove this dependency, membership rules are stored
in a separate Membership_Types table. Members refer to
that table through Membership_Type_ID.

Categories are also stored using Category_ID and a
self-referencing Parent_Category_ID foreign key.
This avoids repeating parent category names and
supports category hierarchies.

### Final Database Design

The database is divided into ten tables:
membership_types, members, categories, items, authors,
item_authors, loans, fines, reservations and audit_log.

Primary keys uniquely identify records. Foreign keys
connect related records and maintain referential integrity.

The item_authors table resolves the many-to-many
relationship between items and authors using a composite
primary key (isbn, author_id).

Categories use a self-referencing foreign key to represent
parent-child relationships.

Available copies will be calculated as total copies minus
the number of active loans. This avoids storing a value
that could become inconsistent with loan records.

## Phase 3.6 – Index Performance Report

### Objective
To compare SQLite query execution plans before and after creating indexes.

### Indexes created

| Index | Columns | Purpose |
|---|---|---|
| idx_loans_return_due | return_date, due_date | Improve overdue-loan searches |
| idx_loans_member_issue | member_id, issue_date | Improve member loan-history searches |

### Query plan comparison

**Q3 – Overdue loans**

Before indexing:
`SCAN loans`

After indexing:
`SEARCH loans USING INDEX idx_loans_return_due (return_date=? AND due_date<?)`

**Q6 – Members with recent loans**

Before indexing:
`SCAN loans`

After indexing:
`SEARCH loans USING INDEX idx_loans_member_issue (member_id=? AND issue_date>?)`

### Conclusion

Before indexing, SQLite performed full table scans for both queries. After creating the indexes, SQLite used index-based search operations.

This demonstrates how indexes can help reduce unnecessary table scanning and improve query performance.

Note: The database contains only 10 loan records, so this experiment demonstrates the query-plan change rather than a measurable real-world speed improvement.