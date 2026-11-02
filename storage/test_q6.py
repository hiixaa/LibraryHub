
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "libraryhub.db"

connection = sqlite3.connect(DB_PATH)

query = """
SELECT
    m.name
FROM members AS m
WHERE NOT EXISTS (
    SELECT 1
    FROM loans AS l
    WHERE l.member_id = m.member_id
      AND l.issue_date >= '2026-07-14'
)
ORDER BY m.name;
"""

results = connection.execute(query).fetchall()

for row in results:
    print(row)

connection.close()
