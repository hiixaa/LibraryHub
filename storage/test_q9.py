
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "libraryhub.db"

connection = sqlite3.connect(DB_PATH)

query = """
SELECT
    m.name,
    COUNT(DISTINCT c.category_id) AS categories
FROM members AS m
INNER JOIN loans AS l
    ON m.member_id = l.member_id
INNER JOIN items AS i
    ON l.isbn = i.isbn
INNER JOIN categories AS c
    ON i.category_id = c.category_id
GROUP BY m.member_id, m.name
HAVING COUNT(DISTINCT c.category_id) >= 3
ORDER BY m.name;
"""

results = connection.execute(query).fetchall()

for row in results:
    print(row)

connection.close()
