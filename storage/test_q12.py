
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "libraryhub.db"

connection = sqlite3.connect(DB_PATH)

query = """
SELECT
    i1.title AS title_a,
    i2.title AS title_b,
    COUNT(DISTINCT l1.member_id) AS members
FROM loans AS l1
INNER JOIN loans AS l2
    ON l1.member_id = l2.member_id
   AND l1.isbn < l2.isbn
INNER JOIN items AS i1
    ON l1.isbn = i1.isbn
INNER JOIN items AS i2
    ON l2.isbn = i2.isbn
GROUP BY
    l1.isbn,
    l2.isbn,
    i1.title,
    i2.title
ORDER BY
    members DESC,
    title_a,
    title_b
LIMIT 1;
"""

results = connection.execute(query).fetchall()

for row in results:
    print(row)

connection.close()
