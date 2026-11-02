
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "libraryhub.db"

connection = sqlite3.connect(DB_PATH)

query = """
SELECT
    i.title,
    i.total_copies - COALESCE(active.active_loans, 0) AS available
FROM items AS i
LEFT JOIN (
    SELECT
        isbn,
        COUNT(*) AS active_loans
    FROM loans
    WHERE return_date IS NULL
    GROUP BY isbn
) AS active
    ON i.isbn = active.isbn
ORDER BY i.title;
"""

results = connection.execute(query).fetchall()

for row in results:
    print(row)

connection.close()
