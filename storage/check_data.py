
import sqlite3
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DB_PATH = PROJECT_ROOT / "libraryhub.db"


def check_data():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row

    try:
        print("LIBRARY ITEMS")
        print("-" * 60)

        cursor = connection.execute("""
            SELECT
                i.isbn,
                i.title,
                c.category_name,
                i.total_copies
            FROM items AS i
            JOIN categories AS c
                ON i.category_id = c.category_id
            ORDER BY i.title
        """)

        for row in cursor.fetchall():
            print(
                f"{row['title']} | "
                f"{row['category_name']} | "
                f"Copies: {row['total_copies']}"
            )

        print("\nMEMBERS AND MEMBERSHIP TYPES")
        print("-" * 60)

        cursor = connection.execute("""
            SELECT
                m.member_id,
                m.name,
                mt.type_name,
                mt.loan_limit
            FROM members AS m
            JOIN membership_types AS mt
                ON m.membership_type_id = mt.membership_type_id
            ORDER BY m.member_id
        """)

        for row in cursor.fetchall():
            print(
                f"{row['member_id']} | "
                f"{row['name']} | "
                f"{row['type_name']} | "
                f"Loan limit: {row['loan_limit']}"
            )

        print("\nACTIVE LOANS")
        print("-" * 60)

        cursor = connection.execute("""
            SELECT
                l.loan_id,
                m.name,
                i.title,
                l.due_date
            FROM loans AS l
            JOIN members AS m
                ON l.member_id = m.member_id
            JOIN items AS i
                ON l.isbn = i.isbn
            WHERE l.return_date IS NULL
            ORDER BY l.loan_id
        """)

        for row in cursor.fetchall():
            print(
                f"{row['loan_id']} | "
                f"{row['name']} | "
                f"{row['title']} | "
                f"Due: {row['due_date']}"
            )

    finally:
        connection.close()


if __name__ == "__main__":
    check_data()
