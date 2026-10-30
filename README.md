# LibraryHub – Library Management System

## 1. Project Overview

LibraryHub is a Library Management System developed using Python and Object-Oriented Programming (OOP).

It manages library items, members, borrowing, returning, renewals, reservations, overdue loans, and fines.

The project also incorporates Data Structures and Algorithms (DSA), SQL, and React as part of its development phases.

## 2. Technologies Used

- Python 3.14
- Object-Oriented Programming (OOP)
- Pytest
- CSV for starter data
- SQLite / SQL
- React
- Git and GitHub

## 3. Project Structure

```text
LibraryHub/
│
├── items.py
├── members.py
├── loans.py
├── library.py
├── errors.py
├── audit.py
├── main.py
│
├── books.csv
├── members.csv
├── loans.csv
├── fines.csv
│
├── test_items.py
├── test_members.py
├── test_loans.py
├── test_library.py
├── test_errors.py
├── test_overdue.py
│
├── requirements.txt
├── DECISIONS.md
└── README.md
```

## 4. Features

- Add and list library items.
- Search books by title or author.
- Manage different membership types.
- Borrow and return library items.
- Renew eligible loans.
- Reserve unavailable items.
- Maintain waiting lists.
- Track member loans.
- Generate overdue reports.
- Calculate overdue fines.
- Maintain an audit log.
- Handle custom exceptions.

## 5. Installation and Setup

Clone or download the project.

Navigate to the project directory:

```bash
cd LibraryHub
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

## 6. Running the Application

Run the console application:

```bash
python main.py
```

The application provides an interactive menu for library operations.

## 7. Running Tests

Run all tests:

```bash
python -m pytest -v
```

The test suite covers items, members, loans, library operations, custom exceptions, overdue calculations, and parameterized tests.

## 8. Project Phases

- Phase 1: Python and OOP implementation.
- Phase 1.5: Console application, testing, and project setup.
- Phase 2: Data Structures and Algorithms.
- Phase 3: SQL and database integration.
- Phase 4: React frontend.

## 9. Testing

Tests are written using Pytest.

The test suite includes:
- Unit tests.
- Exception tests.
- Parameterized tests.
- Loan and overdue calculations.
- Library operation tests.

## 10. Rule-to-Method-to-Test Mapping

| Rule | Implementation method | Test file |
|---|---|---|
| R1 – Reference items cannot be borrowed | `Library.borrow()` | `test_items.py`, `test_library.py` |
| R2 – Magazines have a 7-day loan period and cannot be renewed | `Magazine.loan_period()`, `Loan.renew()` | `test_items.py`, `test_loans.py` |
| R3 – Membership borrowing limit | `Library.borrow()` | `test_library.py` |
| R4 – Unpaid fine restriction | `Library.borrow()` | `test_library.py` |
| R5 – Fine calculation | `Loan.calculate_fine()` | `test_overdue.py` |
| R6 – Maximum two book renewals and waiting-list restriction | `Loan.renew()`, `Library.renew()` | `test_loans.py`, `test_library.py` |
| R7 – Waiting-list management | `Library.reserve()`, `Library.get_waiting_list()` | `test_library.py` |
| R8 – Duplicate title borrowing restriction | `Library.borrow()` | `test_library.py` |
| R9 – ISBN must contain exactly 13 digits and be unique | `LibraryItem` ISBN validation, `Library.add_item()` | `test_items.py`, `test_library.py` |
| R10 – Due date itself is not overdue | `Loan.is_overdue()` | `test_overdue.py` |

## 11. Sample Date

The project uses October 12, 2026 as its sample date.

Run the application with:

```powershell
$env:TODAY = "2026-10-12"
python main.py
```

## 12. Test Results

Automated tests are executed using Pytest.

The current test suite has been verified with:

```text
32+ tests passed
```

Run the tests using:

```powershell
python -m pytest -v
```

## 13. Design Documentation

- Library hub.docx – Contains the problem statement, objectives, requirements, UML class diagram, exception list and CRC cards.
- DECISIONS.md – Records design decisions and their rationale.