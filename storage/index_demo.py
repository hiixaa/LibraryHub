
import sqlite3
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent
DB_PATH = PROJECT_DIR / "libraryhub.db"

connection = sqlite3.connect(DB_PATH)
cursor = connection.cursor()


# Query 1: Find overdue active loans
q3 = """
SELECT loan_id, member_id, isbn, due_date
FROM loans
WHERE return_date IS NULL
AND due_date < '2026-10-12';
"""


# Query 2: Find loans by member issued since a date
q6 = """
SELECT loan_id, member_id, issue_date
FROM loans
WHERE member_id = 'M002'
AND issue_date >= '2026-07-14';
"""


def show_query_plan(query, label):
    print(f"\n{label}")

    cursor.execute("EXPLAIN QUERY PLAN " + query)

    for row in cursor.fetchall():
        print(row)


# -----------------------------------
# PART 1: Query plans before indexes
# -----------------------------------

print("QUERY PLANS BEFORE INDEXING")
print("=" * 50)

# Remove these indexes first so we can compare fairly.
cursor.execute("DROP INDEX IF EXISTS idx_loans_return_due")
cursor.execute("DROP INDEX IF EXISTS idx_loans_member_issue")
connection.commit()

show_query_plan(q3, "Q3: Overdue loans")
show_query_plan(q6, "Q6: Loans by member and issue date")


# -----------------------------------
# PART 2: Create indexes
# -----------------------------------

print("\n\nCREATING INDEXES")
print("=" * 50)

cursor.execute("""
CREATE INDEX idx_loans_return_due
ON loans(return_date, due_date)
""")

cursor.execute("""
CREATE INDEX idx_loans_member_issue
ON loans(member_id, issue_date)
""")

connection.commit()

print("Index 1 created: idx_loans_return_due")
print("Index 2 created: idx_loans_member_issue")


# -----------------------------------
# PART 3: Query plans after indexes
# -----------------------------------

print("\n\nQUERY PLANS AFTER INDEXING")
print("=" * 50)

show_query_plan(q3, "Q3: Overdue loans")
show_query_plan(q6, "Q6: Loans by member and issue date")


connection.close()
