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