PRAGMA foreign_keys = ON;

-- 1. Membership types
CREATE TABLE membership_types (
    membership_type_id INTEGER PRIMARY KEY AUTOINCREMENT,
    type_name TEXT NOT NULL UNIQUE,
    loan_limit INTEGER NOT NULL CHECK (loan_limit > 0),
    loan_period INTEGER NOT NULL CHECK (loan_period > 0),
    fine_per_day REAL NOT NULL CHECK (fine_per_day >= 0)
);

-- 2. Members
CREATE TABLE members (
    member_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    membership_type_id INTEGER NOT NULL,
    FOREIGN KEY (membership_type_id) REFERENCES membership_types (membership_type_id) ON DELETE RESTRICT
);

-- 3. Categories
CREATE TABLE categories (
    category_id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_name TEXT NOT NULL UNIQUE,
    parent_category_id INTEGER,
    FOREIGN KEY (parent_category_id) REFERENCES categories (category_id) ON DELETE RESTRICT
);

-- 4. Items
CREATE TABLE items (
    isbn TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    item_type TEXT NOT NULL,
    category_id INTEGER NOT NULL,
    pages INTEGER CHECK (
        pages IS NULL
        OR pages > 0
    ),
    price REAL NOT NULL CHECK (price >= 0),
    total_copies INTEGER NOT NULL CHECK (total_copies >= 0),
    FOREIGN KEY (category_id) REFERENCES categories (category_id) ON DELETE RESTRICT
);

-- 5. Authors
CREATE TABLE authors (
    author_id INTEGER PRIMARY KEY AUTOINCREMENT,
    author_name TEXT NOT NULL UNIQUE
);

-- 6. Item-Author junction table
CREATE TABLE item_authors (
    isbn TEXT NOT NULL,
    author_id INTEGER NOT NULL,
    PRIMARY KEY (isbn, author_id),
    FOREIGN KEY (isbn) REFERENCES items (isbn) ON DELETE CASCADE,
    FOREIGN KEY (author_id) REFERENCES authors (author_id) ON DELETE RESTRICT
);

-- 7. Loans
CREATE TABLE loans (
    loan_id TEXT PRIMARY KEY,
    member_id TEXT NOT NULL,
    isbn TEXT NOT NULL,
    issue_date TEXT NOT NULL,
    due_date TEXT NOT NULL,
    return_date TEXT,
    CHECK (due_date >= issue_date),
    CHECK (
        return_date IS NULL
        OR return_date >= issue_date
    ),
    FOREIGN KEY (member_id) REFERENCES members (member_id) ON DELETE RESTRICT,
    FOREIGN KEY (isbn) REFERENCES items (isbn) ON DELETE RESTRICT
);

-- 8. Fines
CREATE TABLE fines (
    fine_id INTEGER PRIMARY KEY AUTOINCREMENT,
    loan_id TEXT NOT NULL UNIQUE,
    amount REAL NOT NULL CHECK (amount >= 0),
    paid INTEGER NOT NULL DEFAULT 0 CHECK (paid IN (0, 1)),
    FOREIGN KEY (loan_id) REFERENCES loans (loan_id) ON DELETE CASCADE
);

-- 9. Reservations
CREATE TABLE reservations (
    reservation_id INTEGER PRIMARY KEY AUTOINCREMENT,
    member_id TEXT NOT NULL,
    isbn TEXT NOT NULL,
    reservation_date TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'Waiting' CHECK (
        status IN (
            'Waiting',
            'Fulfilled',
            'Cancelled'
        )
    ),
    FOREIGN KEY (member_id) REFERENCES members (member_id) ON DELETE RESTRICT,
    FOREIGN KEY (isbn) REFERENCES items (isbn) ON DELETE RESTRICT
);

-- 10. Audit log
CREATE TABLE audit_log (
    audit_id INTEGER PRIMARY KEY AUTOINCREMENT,
    action TEXT NOT NULL,
    entity_type TEXT NOT NULL,
    entity_id TEXT NOT NULL,
    action_date TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    details TEXT
);