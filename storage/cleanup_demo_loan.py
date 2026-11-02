
from storage.database import get_connection

with get_connection() as connection:
    cursor = connection.cursor()

    # Remove the audit record created by the transaction demo.
    cursor.execute("""
        DELETE FROM audit_log
        WHERE entity_id = ?
    """, ("L011",))

    # Remove the demonstration loan.
    cursor.execute("""
        DELETE FROM loans
        WHERE loan_id = ?
    """, ("L011",))

    print("Demo loan and audit record cleaned up.")

    cursor.execute("SELECT COUNT(*) FROM loans")
    print("Total loans:", cursor.fetchone()[0])

    cursor.execute("""
        SELECT COUNT(*)
        FROM loans
        WHERE return_date IS NULL
    """)
    print("Active loans:", cursor.fetchone()[0])
