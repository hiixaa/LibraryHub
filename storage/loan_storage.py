
from storage.database import get_connection


class LoanStorage:

    def get_all(self):
        with get_connection() as connection:
            return connection.execute("""
                SELECT
                    l.loan_id,
                    l.member_id,
                    m.name,
                    l.isbn,
                    i.title,
                    l.issue_date,
                    l.due_date,
                    l.return_date,
                    COALESCE(l.renewal_count, 0)
                FROM loans l
                JOIN members m ON m.member_id = l.member_id
                JOIN items i ON i.isbn = l.isbn
                ORDER BY l.loan_id
            """).fetchall()

    def get_by_id(self, loan_id):
        with get_connection() as connection:
            return connection.execute("""
                SELECT
                    loan_id,
                    member_id,
                    isbn,
                    issue_date,
                    due_date,
                    return_date,
                    COALESCE(renewal_count, 0)
                FROM loans
                WHERE loan_id = ?
            """, (loan_id,)).fetchone()

    def get_active_loans(self):
        with get_connection() as connection:
            return connection.execute("""
                SELECT
                    l.loan_id,
                    m.name,
                    i.title,
                    l.due_date
                FROM loans l
                JOIN members m ON m.member_id = l.member_id
                JOIN items i ON i.isbn = l.isbn
                WHERE l.return_date IS NULL
                ORDER BY l.loan_id
            """).fetchall()

    def add(self, loan):
        with get_connection() as connection:
            connection.execute("""
                INSERT INTO loans (
                    loan_id,
                    member_id,
                    isbn,
                    issue_date,
                    due_date,
                    return_date,
                    renewal_count
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                loan["loan_id"],
                loan["member_id"],
                loan["isbn"],
                loan["issue_date"],
                loan["due_date"],
                loan.get("return_date"),
                loan.get("renewal_count", 0)
            ))

    def mark_returned(self, loan_id, return_date):
        with get_connection() as connection:
            cursor = connection.execute("""
                UPDATE loans
                SET return_date = ?
                WHERE loan_id = ?
                  AND return_date IS NULL
            """, (return_date, loan_id))

            return cursor.rowcount > 0

    def get_fines(self):
        with get_connection() as connection:
            return connection.execute("""
                SELECT fine_id, loan_id, amount, paid
                FROM fines
                ORDER BY fine_id
            """).fetchall()

    def get_reservations(self):
        with get_connection() as connection:
            return connection.execute("""
                SELECT
                    reservation_id,
                    member_id,
                    isbn,
                    reservation_date,
                    status
                FROM reservations
                WHERE status = 'Waiting'
                ORDER BY reservation_id
            """).fetchall()

    # --------------------------------------------------
    # BORROW TRANSACTION
    # --------------------------------------------------

    def borrow_transaction(self, loan):
        with get_connection() as connection:

            connection.execute("""
                INSERT INTO loans (
                    loan_id,
                    member_id,
                    isbn,
                    issue_date,
                    due_date,
                    return_date,
                    renewal_count
                )
                VALUES (?, ?, ?, ?, ?, NULL, 0)
            """, (
                loan.loan_id,
                loan.member.member_id,
                loan.item.isbn,
                loan.borrowed_date.isoformat(),
                loan.due_date.isoformat()
            ))

            connection.execute("""
                INSERT INTO audit_log (
                    action,
                    entity_type,
                    entity_id,
                    details
                )
                VALUES (?, ?, ?, ?)
            """, (
                "BORROW",
                "Loan",
                loan.loan_id,
                f"Member {loan.member.member_id} borrowed {loan.item.title}"
            ))

    # --------------------------------------------------
    # RETURN TRANSACTION
    # --------------------------------------------------

    def return_transaction(self, loan, returned_date, fine_amount=0):
        with get_connection() as connection:

            cursor = connection.execute("""
                UPDATE loans
                SET return_date = ?
                WHERE loan_id = ?
                  AND return_date IS NULL
            """, (
                returned_date.isoformat(),
                loan.loan_id
            ))

            if cursor.rowcount != 1:
                raise ValueError(
                    "The loan is no longer active in the database."
                )

            if fine_amount > 0:
                connection.execute("""
                    INSERT INTO fines (loan_id, amount, paid)
                    VALUES (?, ?, 0)
                """, (loan.loan_id, fine_amount))

            reservation = connection.execute("""
                SELECT reservation_id, member_id
                FROM reservations
                WHERE isbn = ?
                  AND status = 'Waiting'
                ORDER BY reservation_id
                LIMIT 1
            """, (loan.item.isbn,)).fetchone()

            next_member_id = None

            if reservation:
                next_member_id = reservation["member_id"]

                connection.execute("""
                    UPDATE reservations
                    SET status = 'Fulfilled'
                    WHERE reservation_id = ?
                """, (reservation["reservation_id"],))

            connection.execute("""
                INSERT INTO audit_log (
                    action,
                    entity_type,
                    entity_id,
                    details
                )
                VALUES (?, ?, ?, ?)
            """, (
                "RETURN",
                "Loan",
                loan.loan_id,
                (
                    f"Member {loan.member.member_id} returned "
                    f"{loan.item.title}; fine={fine_amount}; "
                    f"next reservation={next_member_id}"
                )
            ))

            return next_member_id

    # --------------------------------------------------
    # RENEW TRANSACTION
    # --------------------------------------------------

    def renew_transaction(self, loan, new_due_date, new_count):
        with get_connection() as connection:

            cursor = connection.execute("""
                UPDATE loans
                SET due_date = ?,
                    renewal_count = ?
                WHERE loan_id = ?
                  AND return_date IS NULL
            """, (
                new_due_date.isoformat(),
                new_count,
                loan.loan_id
            ))

            if cursor.rowcount != 1:
                raise ValueError(
                    "The loan is no longer active in the database."
                )

            connection.execute("""
                INSERT INTO audit_log (
                    action,
                    entity_type,
                    entity_id,
                    details
                )
                VALUES (?, ?, ?, ?)
            """, (
                "RENEW",
                "Loan",
                loan.loan_id,
                (
                    f"New due date: {new_due_date.isoformat()}; "
                    f"renewal {new_count}"
                )
            ))

    # --------------------------------------------------
    # UNDO TRANSACTIONS
    # --------------------------------------------------

    def undo_borrow_transaction(self, loan):
        with get_connection() as connection:

            connection.execute("""
                DELETE FROM loans
                WHERE loan_id = ?
            """, (loan.loan_id,))

            connection.execute("""
                INSERT INTO audit_log (
                    action,
                    entity_type,
                    entity_id,
                    details
                )
                VALUES (?, ?, ?, ?)
            """, (
                "UNDO_BORROW",
                "Loan",
                loan.loan_id,
                "Borrow operation reversed"
            ))

    def undo_return_transaction(self, loan, previous_queue):
        with get_connection() as connection:

            connection.execute("""
                UPDATE loans
                SET return_date = NULL
                WHERE loan_id = ?
            """, (loan.loan_id,))

            connection.execute("""
                DELETE FROM fines
                WHERE loan_id = ?
            """, (loan.loan_id,))

            if previous_queue:
                member_id = previous_queue[0]

                reservation = connection.execute("""
                    SELECT reservation_id
                    FROM reservations
                    WHERE isbn = ?
                      AND member_id = ?
                      AND status = 'Fulfilled'
                    ORDER BY reservation_id DESC
                    LIMIT 1
                """, (
                    loan.item.isbn,
                    member_id
                )).fetchone()

                if reservation:
                    connection.execute("""
                        UPDATE reservations
                        SET status = 'Waiting'
                        WHERE reservation_id = ?
                    """, (reservation["reservation_id"],))

            connection.execute("""
                INSERT INTO audit_log (
                    action,
                    entity_type,
                    entity_id,
                    details
                )
                VALUES (?, ?, ?, ?)
            """, (
                "UNDO_RETURN",
                "Loan",
                loan.loan_id,
                "Return operation reversed"
            ))

    # --------------------------------------------------
    # RESERVATION TRANSACTIONS
    # --------------------------------------------------

    def reserve_transaction(self, isbn, member_id, reservation_date):
        with get_connection() as connection:

            connection.execute("""
                INSERT INTO reservations (
                    member_id,
                    isbn,
                    reservation_date,
                    status
                )
                VALUES (?, ?, ?, 'Waiting')
            """, (
                member_id,
                isbn,
                reservation_date.isoformat()
            ))

            connection.execute("""
                INSERT INTO audit_log (
                    action,
                    entity_type,
                    entity_id,
                    details
                )
                VALUES (?, ?, ?, ?)
            """, (
                "RESERVE",
                "Item",
                isbn,
                f"Member {member_id} joined waiting list"
            ))

    def fulfill_next_reservation(self, isbn):
        with get_connection() as connection:

            row = connection.execute("""
                SELECT reservation_id, member_id
                FROM reservations
                WHERE isbn = ?
                  AND status = 'Waiting'
                ORDER BY reservation_id
                LIMIT 1
            """, (isbn,)).fetchone()

            if row:
                connection.execute("""
                    UPDATE reservations
                    SET status = 'Fulfilled'
                    WHERE reservation_id = ?
                """, (row["reservation_id"],))

                connection.execute("""
                    INSERT INTO audit_log (
                        action,
                        entity_type,
                        entity_id,
                        details
                    )
                    VALUES (?, ?, ?, ?)
                """, (
                    "FULFILL_RESERVATION",
                    "Item",
                    isbn,
                    f"Reservation for member {row['member_id']} fulfilled"
                ))

                return row["member_id"]

            return None
