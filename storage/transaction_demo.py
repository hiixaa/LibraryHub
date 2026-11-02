
import sqlite3
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent
DB_PATH = PROJECT_DIR / "libraryhub.db"

connection = sqlite3.connect(DB_PATH)
cursor = connection.cursor()

# -----------------------------------
# DEMO 1: Failed transaction
# -----------------------------------

print("DEMO 1: TESTING ROLLBACK")
print("-" * 40)

try:
    cursor.execute("BEGIN TRANSACTION")

    # Step 1: Insert a loan
    cursor.execute("""
        INSERT INTO loans (
            loan_id, member_id, isbn,
            issue_date, due_date
        )
        VALUES (?, ?, ?, ?, ?)
    """, (
        "L011",
        "M001",
        "9780000000011",
        "2026-11-01",
        "2026-11-15"
    ))

    print("Loan inserted successfully.")

    # Step 2: Deliberately insert an invalid audit record.
    # action is NOT NULL in the database schema.
    cursor.execute("""
        INSERT INTO audit_log (
            action, entity_type, entity_id, details
        )
        VALUES (?, ?, ?, ?)
    """, (
        None,
        "Loan",
        "L011",
        "Borrow operation"
    ))

    connection.commit()

except sqlite3.IntegrityError as error:
    print("Audit insertion failed:", error)

    # Undo the loan insertion too.
    connection.rollback()
    print("Transaction rolled back.")

# Verify that the loan was not saved.
cursor.execute(
    "SELECT loan_id FROM loans WHERE loan_id = ?",
    ("L011",)
)

result = cursor.fetchone()

print("Loan after rollback:", result)


# -----------------------------------
# DEMO 2: Successful transaction
# -----------------------------------

print("\nDEMO 2: TESTING COMMIT")
print("-" * 40)

try:
    cursor.execute("BEGIN TRANSACTION")

    # Step 1: Insert a loan
    cursor.execute("""
        INSERT INTO loans (
            loan_id, member_id, isbn,
            issue_date, due_date
        )
        VALUES (?, ?, ?, ?, ?)
    """, (
        "L011",
        "M001",
        "9780000000011",
        "2026-11-01",
        "2026-11-15"
    ))

    # Step 2: Insert a valid audit record
    cursor.execute("""
        INSERT INTO audit_log (
            action, entity_type, entity_id, details
        )
        VALUES (?, ?, ?, ?)
    """, (
        "BORROW",
        "Loan",
        "L011",
        "Member M001 borrowed Wings of Fire"
    ))

    connection.commit()
    print("Loan inserted successfully.")
    print("Audit record inserted successfully.")
    print("Transaction committed.")

except sqlite3.Error as error:
    connection.rollback()
    print("Transaction failed:", error)
    print("Transaction rolled back.")

# Verify both records exist.
cursor.execute(
    "SELECT loan_id FROM loans WHERE loan_id = ?",
    ("L011",)
)
print("Loan after commit:", cursor.fetchone())

cursor.execute(
    "SELECT action, entity_id FROM audit_log WHERE entity_id = ?",
    ("L011",)
)
print("Audit record after commit:", cursor.fetchone())

connection.close()
