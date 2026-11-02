-- Q1: Books in category 'Biography' with their authors
-- Join type: INNER JOIN
-- Reason: We only need items that have a matching category
-- and at least one matching author.

SELECT i.title, a.author_name AS author
FROM
    items AS i
    INNER JOIN categories AS c ON i.category_id = c.category_id
    INNER JOIN item_authors AS ia ON i.isbn = ia.isbn
    INNER JOIN authors AS a ON ia.author_id = a.author_id
WHERE
    c.category_name = 'Biography'
ORDER BY a.author_name;

-- Q2: Items currently on loan, and who has them
-- Join type: INNER JOIN
-- Reason: We need matching loan, member and item records.

SELECT l.loan_id, m.name AS member, i.title
FROM
    loans AS l
    INNER JOIN members AS m ON l.member_id = m.member_id
    INNER JOIN items AS i ON l.isbn = i.isbn
WHERE
    l.return_date IS NULL
ORDER BY l.loan_id;

-- Q3: Overdue loans with days overdue
-- Join type: INNER JOIN
-- Reason: We need matching loan, member and item records.

SELECT m.name AS member, i.title, l.due_date, CAST(
        julianday ('2026-10-12') - julianday (l.due_date) AS INTEGER
    ) AS days_overdue
FROM
    loans AS l
    INNER JOIN members AS m ON l.member_id = m.member_id
    INNER JOIN items AS i ON l.isbn = i.isbn
WHERE
    l.return_date IS NULL
    AND l.due_date < '2026-10-12'
ORDER BY l.due_date;

-- Q4: Top 3 titles by number of loans
-- Join type: INNER JOIN
-- Reason: We need matching loan records for each item.

SELECT i.title, COUNT(l.loan_id) AS loans
FROM items AS i
    INNER JOIN loans AS l ON i.isbn = l.isbn
GROUP BY
    i.isbn,
    i.title
ORDER BY loans DESC, i.title ASC
LIMIT 3;

-- Q5: Items that have never been borrowed
-- Join type: LEFT JOIN
-- Reason: We need to retain every item, including those
-- without a matching loan record.

SELECT i.title
FROM items AS i
    LEFT JOIN loans AS l ON i.isbn = l.isbn
WHERE
    l.loan_id IS NULL
ORDER BY i.title;

-- Q6: Members with no loan in the last 90 days
-- Join type: No JOIN; uses a correlated NOT EXISTS subquery.
-- Reason: We need members for whom no recent loan exists.

SELECT m.name
FROM members AS m
WHERE
    NOT EXISTS (
        SELECT 1
        FROM loans AS l
        WHERE
            l.member_id = m.member_id
            AND l.issue_date >= '2026-07-14'
    )
ORDER BY m.name;

-- Q7: Total fines per membership type per month
-- Join type: INNER JOIN
-- Reason: We need matching fine, loan, member and membership records.

SELECT
    mt.type_name AS membership_type,
    strftime ('%Y-%m', l.return_date) AS month,
    SUM(f.amount) AS total_fines
FROM
    fines AS f
    INNER JOIN loans AS l ON f.loan_id = l.loan_id
    INNER JOIN members AS m ON l.member_id = m.member_id
    INNER JOIN membership_types AS mt ON m.membership_type_id = mt.membership_type_id
GROUP BY
    mt.type_name,
    strftime ('%Y-%m', l.return_date)
ORDER BY month, membership_type;

-- Q8: Fines paid vs pending
-- Join type: No JOIN required; all information is in fines.

SELECT
    CASE
        WHEN paid = 1 THEN 'Paid'
        ELSE 'Pending'
    END AS status,
    SUM(amount) AS total
FROM fines
GROUP BY
    paid
ORDER BY paid DESC;

-- Q9: Members who borrowed from at least 3 different categories
-- Join type: INNER JOIN
-- Reason: We need matching members, loans, items and categories.

SELECT m.name, COUNT(DISTINCT c.category_id) AS categories
FROM
    members AS m
    INNER JOIN loans AS l ON m.member_id = l.member_id
    INNER JOIN items AS i ON l.isbn = i.isbn
    INNER JOIN categories AS c ON i.category_id = c.category_id
GROUP BY
    m.member_id,
    m.name
HAVING
    COUNT(DISTINCT c.category_id) >= 3
ORDER BY m.name;

-- Q10: Categories where average returned loan duration is more than 25 days
-- Join type: INNER JOIN
-- Reason: We need matching loans, items and categories.

-- Q10: Which categories have an average returned loan duration greater than 25 days?
-- INNER JOIN: Connects loans, items and categories.
-- Only returned loans are considered.

SELECT
    CASE
        WHEN c.category_name = 'SoftwareEngineering' THEN 'Software Engineering'
        ELSE c.category_name
    END AS category_name,
    ROUND(
        AVG(
            julianday (l.return_date) - julianday (l.issue_date)
        ),
        1
    ) AS average_duration
FROM
    loans l
    INNER JOIN items i ON l.isbn = i.isbn
    INNER JOIN categories c ON i.category_id = c.category_id
WHERE
    l.return_date IS NOT NULL
GROUP BY
    c.category_id,
    c.category_name
HAVING
    AVG(
        julianday (l.return_date) - julianday (l.issue_date)
    ) > 25
ORDER BY average_duration DESC;

-- Q11: Available copies per title
-- Join type: LEFT JOIN with an aggregated subquery.
-- Reason: We must retain every item, including those
-- that have no active loans.

SELECT i.title, i.total_copies - COALESCE(active.active_loans, 0) AS available
FROM items AS i
    LEFT JOIN (
        SELECT isbn, COUNT(*) AS active_loans
        FROM loans
        WHERE
            return_date IS NULL
        GROUP BY
            isbn
    ) AS active ON i.isbn = active.isbn
ORDER BY i.title;

-- Q12: Pair of titles most often borrowed by the same member
-- Join type: INNER SELF JOIN
-- Reason: We compare two loan records belonging to the same member.

SELECT
    CASE
        WHEN i1.title < i2.title THEN i1.title
        ELSE i2.title
    END AS title_a,
    CASE
        WHEN i1.title < i2.title THEN i2.title
        ELSE i1.title
    END AS title_b,
    COUNT(DISTINCT l1.member_id) AS members
FROM
    loans l1
    JOIN loans l2 ON l1.member_id = l2.member_id
    AND l1.isbn < l2.isbn
    JOIN items i1 ON l1.isbn = i1.isbn
    JOIN items i2 ON l2.isbn = i2.isbn
GROUP BY
    title_a,
    title_b
ORDER BY members DESC, title_a, title_b
LIMIT 1;