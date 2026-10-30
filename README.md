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