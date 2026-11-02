import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "libraryhub.db"

connection = sqlite3.connect(DB_PATH)

query = """
SELECT
    i.title,
    a.author_name AS author
FROM items AS i
INNER JOIN categories AS c
    ON i.category_id = c.category_id
INNER JOIN item_authors AS ia
    ON i.isbn = ia.isbn
INNER JOIN authors AS a
    ON ia.author_id = a.author_id
WHERE c.category_name = ?
ORDER BY a.author_name;
"""

results = connection.execute(query, ("Biography",)).fetchall()

for row in results:
    print(row)

connection.close()