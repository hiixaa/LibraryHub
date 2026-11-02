
from storage.database import get_connection


class MemberStorage:

    def get_all(self):
        """Fetch all members and their membership details."""

        with get_connection() as connection:
            cursor = connection.cursor()

            cursor.execute("""
                SELECT
                    m.member_id,
                    m.name,
                    m.email,
                    mt.type_name,
                    mt.loan_limit,
                    mt.loan_period,
                    mt.fine_per_day
                FROM members m
                INNER JOIN membership_types mt
                    ON m.membership_type_id = mt.membership_type_id
                ORDER BY m.member_id
            """)

            return cursor.fetchall()

    def get_by_id(self, member_id):
        """Fetch one member using their ID."""

        with get_connection() as connection:
            cursor = connection.cursor()

            cursor.execute("""
                SELECT
                    m.member_id,
                    m.name,
                    m.email,
                    mt.type_name,
                    mt.loan_limit,
                    mt.loan_period,
                    mt.fine_per_day
                FROM members m
                INNER JOIN membership_types mt
                    ON m.membership_type_id = mt.membership_type_id
                WHERE m.member_id = ?
            """, (member_id,))

            return cursor.fetchone()

    def get_by_email(self, email):
        with get_connection() as connection:
            cursor = connection.cursor()

            cursor.execute("""
                SELECT
                    m.member_id,
                    m.name,
                    m.email,
                    mt.type_name,
                    mt.loan_limit,
                    mt.loan_period,
                    mt.fine_per_day
                FROM members m
                INNER JOIN membership_types mt
                    ON m.membership_type_id = mt.membership_type_id
                WHERE m.email = ?
            """, (email,))

            return cursor.fetchone()