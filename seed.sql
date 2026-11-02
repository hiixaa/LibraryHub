PRAGMA foreign_keys = ON;

-- 1. Membership types
INSERT INTO
    membership_types (
        type_name,
        loan_limit,
        loan_period,
        fine_per_day
    )
VALUES ('Student', 3, 14, 2),
    ('Regular', 5, 21, 5),
    ('Premium', 10, 30, 3);

-- 2. Members
INSERT INTO
    members (
        member_id,
        name,
        email,
        membership_type_id
    )
VALUES (
        'M001',
        'Asha Raman',
        'asha@example.com',
        (
            SELECT membership_type_id
            FROM membership_types
            WHERE
                type_name = 'Student'
        )
    ),
    (
        'M002',
        'Rahul Mehta',
        'rahul@example.com',
        (
            SELECT membership_type_id
            FROM membership_types
            WHERE
                type_name = 'Regular'
        )
    ),
    (
        'M003',
        'Sneha Iyer',
        'sneha@example.com',
        (
            SELECT membership_type_id
            FROM membership_types
            WHERE
                type_name = 'Premium'
        )
    ),
    (
        'M004',
        'Karthik N',
        'karthik@example.com',
        (
            SELECT membership_type_id
            FROM membership_types
            WHERE
                type_name = 'Student'
        )
    ),
    (
        'M005',
        'Divya Rao',
        'divya@example.com',
        (
            SELECT membership_type_id
            FROM membership_types
            WHERE
                type_name = 'Regular'
        )
    );

-- 3. Categories
-- Parent category is inserted before its child categories.
INSERT INTO
    categories (
        category_name,
        parent_category_id
    )
VALUES ('Technology', NULL);

INSERT INTO
    categories (
        category_name,
        parent_category_id
    )
VALUES ('Biography', NULL),
    ('Fiction', NULL),
    (
        'SoftwareEngineering',
        (
            SELECT category_id
            FROM categories
            WHERE
                category_name = 'Technology'
        )
    ),
    (
        'Programming',
        (
            SELECT category_id
            FROM categories
            WHERE
                category_name = 'Technology'
        )
    ),
    ('History', NULL),
    ('Reference', NULL),
    ('Magazines', NULL);

-- 4. Items
INSERT INTO
    items (
        isbn,
        title,
        item_type,
        category_id,
        pages,
        price,
        total_copies
    )
VALUES (
        '9780000000011',
        'Wings of Fire',
        'Book',
        (
            SELECT category_id
            FROM categories
            WHERE
                category_name = 'Biography'
        ),
        180,
        250,
        2
    ),
    (
        '9780000000028',
        'The Alchemist',
        'Book',
        (
            SELECT category_id
            FROM categories
            WHERE
                category_name = 'Fiction'
        ),
        208,
        300,
        1
    ),
    (
        '9780000000035',
        'Clean Code',
        'Book',
        (
            SELECT category_id
            FROM categories
            WHERE
                category_name = 'SoftwareEngineering'
        ),
        464,
        900,
        1
    ),
    (
        '9780000000042',
        'Python Crash Course',
        'Book',
        (
            SELECT category_id
            FROM categories
            WHERE
                category_name = 'Programming'
        ),
        544,
        700,
        2
    ),
    (
        '9780000000059',
        'Sapiens',
        'Book',
        (
            SELECT category_id
            FROM categories
            WHERE
                category_name = 'History'
        ),
        512,
        600,
        1
    ),
    (
        '9780000000066',
        'Encyclopaedia of Science',
        'Reference',
        (
            SELECT category_id
            FROM categories
            WHERE
                category_name = 'Reference'
        ),
        1200,
        2500,
        1
    ),
    (
        '9780000000073',
        'India Today (Oct 2026)',
        'Magazine',
        (
            SELECT category_id
            FROM categories
            WHERE
                category_name = 'Magazines'
        ),
        90,
        80,
        3
    );

-- 5. Authors
INSERT INTO
    authors (author_name)
VALUES ('A.P.J. Abdul Kalam'),
    ('Arun Tiwari'),
    ('Paulo Coelho'),
    ('Robert C. Martin'),
    ('Eric Matthes'),
    ('Yuval Noah Harari'),
    ('Various');

-- 6. Item-author relationships
INSERT INTO
    item_authors (isbn, author_id)
VALUES (
        '9780000000011',
        (
            SELECT author_id
            FROM authors
            WHERE
                author_name = 'A.P.J. Abdul Kalam'
        )
    ),
    (
        '9780000000011',
        (
            SELECT author_id
            FROM authors
            WHERE
                author_name = 'Arun Tiwari'
        )
    ),
    (
        '9780000000028',
        (
            SELECT author_id
            FROM authors
            WHERE
                author_name = 'Paulo Coelho'
        )
    ),
    (
        '9780000000035',
        (
            SELECT author_id
            FROM authors
            WHERE
                author_name = 'Robert C. Martin'
        )
    ),
    (
        '9780000000042',
        (
            SELECT author_id
            FROM authors
            WHERE
                author_name = 'Eric Matthes'
        )
    ),
    (
        '9780000000059',
        (
            SELECT author_id
            FROM authors
            WHERE
                author_name = 'Yuval Noah Harari'
        )
    ),
    (
        '9780000000066',
        (
            SELECT author_id
            FROM authors
            WHERE
                author_name = 'Various'
        )
    ),
    (
        '9780000000073',
        (
            SELECT author_id
            FROM authors
            WHERE
                author_name = 'Various'
        )
    );

-- 7. Loans
INSERT INTO
    loans (
        loan_id,
        member_id,
        isbn,
        issue_date,
        due_date,
        return_date
    )
VALUES (
        'L001',
        'M002',
        '9780000000028',
        '2026-09-01',
        '2026-09-22',
        NULL
    ),
    (
        'L002',
        'M004',
        '9780000000042',
        '2026-09-21',
        '2026-10-05',
        NULL
    ),
    (
        'L003',
        'M003',
        '9780000000059',
        '2026-09-20',
        '2026-10-20',
        NULL
    ),
    (
        'L004',
        'M001',
        '9780000000011',
        '2026-09-10',
        '2026-09-24',
        '2026-09-24'
    ),
    (
        'L005',
        'M001',
        '9780000000042',
        '2026-08-01',
        '2026-08-15',
        '2026-08-20'
    ),
    (
        'L006',
        'M003',
        '9780000000035',
        '2026-08-05',
        '2026-09-04',
        '2026-09-02'
    ),
    (
        'L007',
        'M002',
        '9780000000042',
        '2026-07-10',
        '2026-07-31',
        '2026-07-31'
    ),
    (
        'L008',
        'M002',
        '9780000000011',
        '2026-06-01',
        '2026-06-22',
        '2026-06-30'
    ),
    (
        'L009',
        'M004',
        '9780000000073',
        '2026-07-01',
        '2026-07-08',
        '2026-09-06'
    ),
    (
        'L010',
        'M004',
        '9780000000011',
        '2026-07-20',
        '2026-08-03',
        '2026-08-23'
    );

-- 8. Fines
-- CSV yes = 1 (paid), no = 0 (unpaid)
INSERT INTO
    fines (loan_id, amount, paid)
VALUES ('L005', 10, 1),
    ('L008', 40, 1),
    ('L009', 80, 0),
    ('L010', 40, 0);