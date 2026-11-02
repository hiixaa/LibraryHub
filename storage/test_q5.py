
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "libraryhub.db"

connection = sqlite3.connect(DB_PATH)

query = """
SELECT
    i.title
FROM items AS i
LEFT JOIN loans AS l
    ON i.isbn = l.isbn
WHERE l.loan_id IS NULL
ORDER BY i.title;
"""

results = connection.execute(query).fetchall()

for row in results:
    print(row)

connection.close()
