
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "libraryhub.db"

connection = sqlite3.connect(DB_PATH)

query = """
SELECT
    l.loan_id,
    m.name AS member,
    i.title
FROM loans AS l
INNER JOIN members AS m
    ON l.member_id = m.member_id
INNER JOIN items AS i
    ON l.isbn = i.isbn
WHERE l.return_date IS NULL
ORDER BY l.loan_id;
"""

results = connection.execute(query).fetchall()

for row in results:
    print(row)

connection.close()
