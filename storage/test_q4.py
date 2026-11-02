
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "libraryhub.db"

connection = sqlite3.connect(DB_PATH)

query = """
SELECT
    i.title,
    COUNT(l.loan_id) AS loans
FROM items AS i
INNER JOIN loans AS l
    ON i.isbn = l.isbn
GROUP BY i.isbn, i.title
ORDER BY loans DESC, i.title ASC
LIMIT 3;
"""

results = connection.execute(query).fetchall()

for row in results:
    print(row)

connection.close()
