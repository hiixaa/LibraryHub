
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "libraryhub.db"

connection = sqlite3.connect(DB_PATH)

query = """
SELECT
    c.category_name AS category,
    ROUND(
        AVG(
            julianday(l.return_date) - julianday(l.issue_date)
        ),
        1
    ) AS avg_days
FROM loans AS l
INNER JOIN items AS i
    ON l.isbn = i.isbn
INNER JOIN categories AS c
    ON i.category_id = c.category_id
WHERE l.return_date IS NOT NULL
GROUP BY c.category_id, c.category_name
HAVING AVG(
    julianday(l.return_date) - julianday(l.issue_date)
) > 25
ORDER BY avg_days DESC;
"""

results = connection.execute(query).fetchall()

for row in results:
    print(row)

connection.close()