
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "libraryhub.db"

connection = sqlite3.connect(DB_PATH)

query = """
SELECT
    CASE
        WHEN paid = 1 THEN 'Paid'
        ELSE 'Pending'
    END AS status,
    SUM(amount) AS total
FROM fines
GROUP BY paid
ORDER BY paid DESC;
"""

results = connection.execute(query).fetchall()

for row in results:
    print(row)

connection.close()
