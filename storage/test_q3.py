
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "libraryhub.db"

connection = sqlite3.connect(DB_PATH)

query = """
SELECT
    m.name AS member,
    i.title,
    l.due_date,
    CAST(
        julianday('2026-10-12') - julianday(l.due_date)
        AS INTEGER
    ) AS days_overdue
FROM loans AS l
INNER JOIN members AS m
    ON l.member_id = m.member_id
INNER JOIN items AS i
    ON l.isbn = i.isbn
WHERE l.return_date IS NULL
  AND l.due_date < '2026-10-12'
ORDER BY l.due_date;
"""

results = connection.execute(query).fetchall()

for row in results:
    print(row)

connection.close()
