
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "libraryhub.db"

connection = sqlite3.connect(DB_PATH)

query = """
SELECT
    mt.type_name AS membership_type,
    strftime('%Y-%m', l.return_date) AS month,
    SUM(f.amount) AS total_fines
FROM fines AS f
INNER JOIN loans AS l
    ON f.loan_id = l.loan_id
INNER JOIN members AS m
    ON l.member_id = m.member_id
INNER JOIN membership_types AS mt
    ON m.membership_type_id = mt.membership_type_id
GROUP BY
    mt.type_name,
    strftime('%Y-%m', l.return_date)
ORDER BY
    month,
    membership_type;
"""

results = connection.execute(query).fetchall()

for row in results:
    print(row)

connection.close()
